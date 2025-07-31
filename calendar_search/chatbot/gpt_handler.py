# from openai import OpenAI
# import os
# from dotenv import load_dotenvz

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # ✅ 최신 방식으로 클라이언트 생성

# # 프롬프트 템플릿: 일정이 있는지 판단하고 JSON으로 만들도록 유도
# prompt_template = """
# 입력된 문장에 일정 관련 단어(예: 내일, 다음주, 3월 2일 등)가 포함되어 있다면 아래 JSON 형태로 추출합니다.
# 불가능하다면 추출하지 말고 빈 응답을 반환합니다.

# 예시:
# {
#   "calendar_id": "calendar_001",
#   "events": [
#     {
#       "id": "evt_001",
#       "start_date": "YYYY-MM-DD-HH:mm",
#       "end_date": "YYYY-MM-DD-HH:mm",
#       "title": "(일정내용)"
#     }
#   ]
# }
# """

# def get_ai_response(user_message):
#     """
#     사용자의 메시지를 기반으로 GPT에게 일정 판단 요청
#     """
#     full_prompt = prompt_template + "\n\n입력:\n" + user_message
#     res = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "너는 일정 분석과 정보 검색을 도와주는 AI야."},
#             {"role": "user", "content": full_prompt}
#         ]
#     )
#     content = res.choices[0].message.content
#     usage = {
#         "prompt_tokens": res.usage.prompt_tokens,
#         "completion_tokens": res.usage.completion_tokens,
#         "total_tokens": res.usage.total_tokens
#     }
#     return content, usage


# def extract_schedule_from_text(page_texts):
#     """
#     크롤링한 웹페이지 본문들을 기반으로 일정 정보를 추출하는 GPT 호출
#     """
#     content = "\n\n".join(page_texts)
#     prompt = f"""
# 다음 웹페이지 본문에서 일정 정보를 추출해 아래 JSON 형식으로 리턴하세요:

# \"\"\"
# {content}
# \"\"\"

# 예시:
# {{
#   "calendar_id": "calendar_001",
#   "events": [
#     {{
#       "id": "evt_001",
#       "start_date": "YYYY-MM-DD-HH:mm",
#       "end_date": "YYYY-MM-DD-HH:mm",
#       "title": "(일정내용)"
#     }}
#   ]
# }}
#     """
#     res = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "너는 웹페이지에서 일정 정보를 추출하는 AI야."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     content = res.choices[0].message.content
#     usage = {
#         "prompt_tokens": res.usage.prompt_tokens,
#         "completion_tokens": res.usage.completion_tokens,
#         "total_tokens": res.usage.total_tokens
#     }
#     return content, usage

# ↓검색어 추출한느거 추가한건데 아직 실행은 안 해봣음...
# def extract_search_query(user_input, model="gpt-4o-mini"):
#     """
#     사용자의 문장에서 웹 검색용 핵심 키워드만 추출한다.
#     예: "2025년 스트레이키즈 팬미팅 일정 알려줘" → "스트레이키즈 팬미팅"
#     """
#     prompt = f"""
# 다음 문장에서 웹 검색에 사용할 수 있는 핵심 키워드를 간결하게 뽑아줘.
# 날짜, '일정', '알려줘' 같은 일반적인 표현은 제외하고, 핵심 주제만 남겨줘.

# 예시:
# 입력: "2025년 스트레이키즈 팬미팅 일정 알려줘"
# 출력: "스트레이키즈 팬미팅"
# 입력: "플레이브 서울 콘서트 일정 알려줘"
# 출력: "플레이브 서울 콘서트"
# 입력: "뉴진스 컴백 날짜 알려줘"
# 출력: "뉴진스 컴백"


# 입력: "{user_input}"
# 출력:
#     """
#     try:
#         response = client.chat.completions.create(
#             model=model,
#             messages=[
#                 {"role": "system", "content": "너는 문장에서 핵심 검색어만 뽑아주는 AI야."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.2
#         )
#         return response.choices[0].message.content.strip().strip('"')
#     except Exception as e:
#         print(f"❌ OpenAI 호출 실패: {e}")
#         return "검색어 추출 실패"

import os
from dotenv import load_dotenv
import google.generativeai as genai

# 환경 변수 로드 (.env에서 GOOGLE_API_KEY 불러오기)
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini 모델 초기화
model = genai.GenerativeModel("gemini-1.5-flash")

# 일정 추출용 프롬프트 템플릿
prompt_template = """
입력된 문장에 일정 관련 단어(예: 내일, 다음주, 3월 2일 등)가 포함되어 있다면 아래 JSON 형태로 추출합니다.
불가능하다면 추출하지 말고 빈 응답을 반환합니다.

예시:
{
  "calendar_id": "calendar_001",
  "events": [
    {
      "id": "evt_001",
      "start_date": "YYYY-MM-DD-HH:mm",
      "end_date": "YYYY-MM-DD-HH:mm",
      "title": "(일정내용)"
    }
  ]
}
"""

def get_ai_response(user_message):
    """
    사용자의 메시지를 기반으로 일정 판단 요청 (Gemini 사용)
    """
    full_prompt = prompt_template + "\n\n입력:\n" + user_message
    response = model.generate_content(full_prompt)
    return response.text, None  # Gemini는 토큰 사용량 미제공


def extract_schedule_from_text(page_texts):
    """
    웹페이지 본문들을 기반으로 일정 정보를 추출 (Gemini 사용)
    """
    content = "\n\n".join(page_texts)
    prompt = f"""
다음 웹페이지 본문에서 일정 정보를 추출해 아래 JSON 형식으로 리턴하세요:

\"\"\"
{content}
\"\"\"

예시:
{{
  "calendar_id": "calendar_001",
  "events": [
    {{
      "id": "evt_001",
      "start_date": "YYYY-MM-DD-HH:mm",
      "end_date": "YYYY-MM-DD-HH:mm",
      "title": "(일정내용)"
    }}
  ]
}}
    """
    response = model.generate_content(prompt)
    return response.text, None  # 토큰 사용량 없음

def extract_search_query(user_input):
    """
    사용자의 문장에서 웹 검색에 적합한 핵심 검색어를 추출한다.
    """
    prompt = f"""
다음 문장에서 웹 검색에 가장 적합한 핵심 키워드만 뽑아줘.
너는 검색어 추출을 위한 시스템이야. 예시처럼 짧고 명확하게 추출해.

예시:
입력: "스트레이키즈 내한 일정 알려줘"
출력: "스트레이키즈 내한",
입력: "플레이브 서울 콘서트 일정 알려줘"
출력: "플레이브 서울 콘서트",
입력: "뉴진스 컴백 날짜 알려줘"
출력: "뉴진스 컴백"

입력: "{user_input}"
출력:
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip().strip('"').strip()
    except Exception as e:
        print(f"❌ Gemini 응답 오류: {e}")
        return "검색어 추출 실패"