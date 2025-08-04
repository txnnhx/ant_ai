from gpt_search.naver_crawler import NaverCrawler
from openai import OpenAI
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import json
import re

# ✅ 환경 변수 불러오기
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class NewsScheduleExtractor:
    """
    기사 본문들로부터 일정 정보를 추출하는 클래스
    """
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        self.client = client

    def _clean_json_output(self, text):
        return re.sub(r"^```json|```$", "", text.strip()).strip()

    def extract_from_texts(self, page_texts):
        today = datetime.now().strftime("%Y-%m-%d")
        content = "\n\n".join(page_texts)
        prompt = f"""
다음 뉴스 기사 본문 내용에서 일정 정보를 추출해 아래 JSON 형식으로 반환하세요:

'~부터', '~까지' 등의 표현은 start, end로 분리하세요.
'~예정', '~하자' 포함 문장은 event로 간주하세요.
start와 end는 동일해도 허용됩니다.

\"\"\"
{content}
\"\"\"

예시 형식:
{{
  "events": [
    {{
      "start_date": "YYYY-MM-DD-HH:mm",
      "end_date": "YYYY-MM-DD-HH:mm",
      "title": "일정 내용"
    }}
  ]
}}
        """
        try:
            res = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"너는 뉴스 기사에서 일정 정보를 추출하는 AI야. 현재 날짜:{today}, 현재 날짜 기준으로 과거의 일정은 추출하지마."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            raw_output = res.choices[0].message.content
            cleaned = self._clean_json_output(raw_output)
            return cleaned
        except Exception as e:
            print("❌ 일정 추출 실패:", e)
            return json.dumps({"events": []}, ensure_ascii=False)

    def extract_search_query(self, user_input):
        """
        사용자의 문장에서 웹 검색용 핵심 키워드만 추출
        """
        prompt = f"""
다음 문장에서 웹 검색에 사용할 수 있는 핵심 키워드를 간결하게 뽑아줘.
날짜, '일정', '알려줘' 같은 일반적인 표현은 제외하고, 핵심 주제만 남겨줘.

예시:
입력: "플레이브 서울 콘서트 일정 알려줘"
출력: "플레이브 서울 콘서트"
입력: "뉴진스 컴백 날짜 알려줘"
출력: "뉴진스 컴백"

입력: "{user_input}"
출력:
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "너는 문장에서 핵심 검색어만 뽑아주는 AI야."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            return response.choices[0].message.content.strip().strip('"')
        except Exception as e:
            print(f"❌ OpenAI 호출 실패: {e}")
            return "검색어 추출 실패"
        
    def extraction(self, query: str = None):
        """
        뉴스 검색어를 기반으로 네이버에서 기사들을 검색하고,
        기사 본문을 GPT에게 넘겨서 일정 정보를 추출하는 클래스 메서드.

        :param query: 직접 전달할 검색어 (None이면 사용자 입력 받음)
        :return: GPT로부터 받은 일정 JSON 문자열
        """
        if query is None:
            query = input("🔍 검색어를 입력하세요: ")

        # ✅ self 메서드 사용
        extracted_query = self.extract_search_query(query)

        # ✅ 외부 모듈 사용
        crawler = NaverCrawler()
        search_results = crawler.search(extracted_query)

        if not search_results:
            print("❌ 뉴스 검색 결과 없음")
            return None

        page_texts = []
        for item in search_results:
            print(f"📰 기사: {item['title']}")
            text = crawler.extract_text(item["link"])
            page_texts.append(text)

        # ✅ self 메서드 사용
        result = self.extract_from_texts(page_texts)

        print("\n📅 추출된 일정 JSON:\n")
        print(result)

        return result


# if __name__ == "__main__":
#     # ✅ 테스트 실행 흐름
#     query = input("🔍 검색어를 입력하세요: ")

#     extractor = NewsScheduleExtractor()
#     extracted_query = extractor.extract_search_query(query)
#     # print(f"\n🧠 GPT가 추출한 핵심 검색어: {extracted_query}")

#     crawler = NaverCrawler()
#     search_results = crawler.search(extracted_query)

#     if not search_results:
#         print("❌ 뉴스 검색 결과 없음")
#         exit()

#     page_texts = []
#     for item in search_results:
#         print(f"📰 기사: {item['title']}")
#         text = crawler.extract_text(item["link"])
#         page_texts.append(text)

#     result = extractor.extract_from_texts(page_texts)

#     print("\n📅 추출된 일정 JSON:\n")
#     print(result)