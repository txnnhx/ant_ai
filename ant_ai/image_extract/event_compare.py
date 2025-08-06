import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class EventPhotoComparator:
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def compare(self, event_text: str, image_info: dict) -> tuple[bool, str, dict]:
        # 🧠 GPT에게 줄 프롬프트 구성
        prompt = f"""
아래는 이벤트 설명과 사진에서 추출한 내용입니다. 둘이 같은 이벤트를 묘사한 것인지 판단해주세요.
- 같으면 "True"
- 다르면 "False"

[이벤트 설명]
{event_text}

[사진 내용]
장소: {image_info.get("장소")}
활동: {image_info.get("활동")}
분위기: {image_info.get("분위기")}
시간대: {image_info.get("시간대")}
키워드: {", ".join(image_info.get("키워드", []))}
"""

        # 🔍 GPT 호출
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=100
        )

        reply = response.choices[0].message.content.strip()
        usage = response.usage  # ✅ 토큰 정보

        is_match = "true" in reply.lower()

        return is_match, reply, {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
        }


if __name__ == "__main__":
    comparator = EventPhotoComparator()

    # 임시 이벤트 설명
    event_description = "일본여행"

    # 사진 분석 결과
    photo_info = {
        "장소": "일본식 음식점",
        "활동": "요리 및 식사",
        "분위기": "아늑하고 현대적인",
        "시간대": "낮",
        "키워드": ["음식", "요리", "일본식", "아늑함", "모던"]
    }

    # 비교 실행
    result, explanation, token_usage = comparator.compare(event_description, photo_info)

    # 출력
    print("✅ 일치 여부:", result)
    print("💬 GPT 응답:\n", explanation)
    print("\n📊 토큰 사용량:")
    print(f" - Prompt tokens:     {token_usage['prompt_tokens']}")
    print(f" - Completion tokens: {token_usage['completion_tokens']}")
    print(f" - Total tokens:      {token_usage['total_tokens']}")
