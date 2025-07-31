from flask import Flask, request, jsonify
from chatbot.gpt_handler import get_ai_response, extract_schedule_from_text, extract_search_query
from chatbot.crawler import search_naver, extract_page_text
from chatbot.utils import is_valid_json
import json

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    ai_output, usage = get_ai_response(user_message)

    if is_valid_json(ai_output):
        return jsonify({
            "type": "schedule",
            "data": json.loads(ai_output),
            "token_usage": usage
        })

    search_result = search_naver(user_message)
    texts = [extract_page_text(item["link"]) for item in search_result]
    schedule_output, usage2 = extract_schedule_from_text(texts)

    if is_valid_json(schedule_output):
        return jsonify({
            "type": "schedule",
            "source": search_result,
            "data": json.loads(schedule_output),
            "token_usage": usage2
        })
    else:
        return jsonify({
            "type": "search",
            "query": user_message,
            "data": search_result,
            "token_usage": usage2
        })


# 🔁 터미널 테스트용 실행 흐름
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        user_message = input("💬 사용자 메시지를 입력하세요: ")

        print(f"\n📩 [입력 메시지] {user_message}")
        ai_output, usage = get_ai_response(user_message)

        print(f"\n🧠 [GPT 직접 판단 결과]\n{ai_output}")
        print(f"\n📊 토큰 사용량: {usage}")

        if is_valid_json(ai_output):
            print("\n✅ 직접 추출한 일정 JSON:")
            print(json.dumps(json.loads(ai_output), indent=2, ensure_ascii=False))
            sys.exit()

        print("\n❌ 직접 추출 실패 → 크롤링 후 재시도")

        search_query = extract_search_query(user_message)
        print(f"\n🔍 추출된 검색어: {search_query}")
        search_result = search_naver(search_query)

        if not search_result:
            print("❌ 검색 결과가 없습니다.")
            sys.exit()

        for idx, item in enumerate(search_result, 1):
            print(f"🔎 링크 {idx}: {item['title']} - {item['link']}")

        texts = [extract_page_text(item["link"]) for item in search_result]

        for i, text in enumerate(texts):
            print(f"\n📄 [페이지 {i+1} 본문 내용 미리보기]")
            if not text.strip():
                print("⚠️  본문 없음")
            else:
                print(text[:1000] + ("..." if len(text) > 1000 else ""))

        if all(len(t.strip()) == 0 for t in texts):
            print("❌ 본문이 비어 있어 GPT에게 전달할 수 없습니다.")
            sys.exit()

        schedule_output, usage2 = extract_schedule_from_text(texts)

        print(f"\n🧠 [GPT 크롤링 기반 판단 결과]\n{schedule_output}")
        print(f"\n📊 토큰 사용량: {usage2}")

        if is_valid_json(schedule_output):
            print("\n✅ 최종 추출한 일정 JSON:")
            print(json.dumps(json.loads(schedule_output), indent=2, ensure_ascii=False))
        else:
            print("\n❌ 최종 일정 추출 실패")
    else:
        print("🚀 Flask 서버 실행 중: http://localhost:5000/chat")
        app.run(debug=True)
