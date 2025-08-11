import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class CalendarCommentator:
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def generate_comment(self, schedule_list: list) -> tuple[str, dict]:
        """
        일정 리스트를 받아서 캘린더에 대한 한 줄 요약 코멘트를 생성하고,
        토큰 사용량도 함께 반환함.
        """
        if not schedule_list:
            return "이번 달은 등록된 일정이 없어요. 여유로운 한 달이 되겠네요!", {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

        # 일정 요약 문자열 생성
        schedule_summary = "\n".join([
            f"- {item['title']} ({item['start_date']} ~ {item['end_date']})"
            for item in schedule_list
        ])
        today = datetime.now().strftime("%Y-%m-%d")
        prompt = f"""
다음은 한 캘린더에 등록된 일정 목록입니다. 일정 내용을 분석하여, 일정 내용에 대한 코멘트를 작성해주세요. 친근한 말투로 한 줄만 생성하세요.
오늘 날짜({today})를 고려하여 생성해주세요.


[일정 목록]
{schedule_summary}
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.7
            )
            comment = response.choices[0].message.content.strip()
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
            return comment, usage

        except Exception as e:
            return f"⚠️ GPT 요청 실패: {str(e)}", {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

# ✅ 테스트 코드 (독립 실행용)
if __name__ == "__main__":
    sample_schedule = [
        {
            "title": "종강",
            "start_date": "2025-06-20T10:00:00",
            "end_date": "2025-06-20T11:00:00"
        },
        {
            "title": "서울주류박람회",
            "start_date": "2025-06-26T10:00:00",
            "end_date": "2025-06-26T11:00:00"
        },
        {
            "title": "일본여행",
            "start_date": "2025-06-27T10:00:00",
            "end_date": "2025-06-30T11:00:00"
        }
    ]

    commentator = CalendarCommentator()
    comment, usage = commentator.generate_comment(sample_schedule)
    print("🗨️ 캘린더 코멘트:", comment)
    print("📊 토큰 사용량:", usage)
