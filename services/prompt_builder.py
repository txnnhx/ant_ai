# 프롬프트 구성 및 OpenAI API 호출을 담당하는 모듈입니다.

import openai
import os

# 일정 생성에 특화된 프롬프트 템플릿
chatbot_prompt = """
    당신은 일정을 만드는 것에 특화된 능숙한 AI입니다.
    다음 텍스트를 기반으로 일정을 만듭니다.
    일정은 간결하게 적어놓으며, 일정이 추가될 날짜가 포함되어야합니다.
    """

# OpenAI API 키 설정 (환경변수 사용 권장)
OPENAI_API_KEY = os.getenv('OPEN_API_KEY')
DEFAULT_MODEL = os.getenv("GET_DEFAULT_MODEL", "gpt-4o-mini")

def build_prompt_and_call(user_message: str) -> str:
    """
    사용자 메시지와 프롬프트를 결합해 GPT-4o-mini로 일정 생성을 요청합니다.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": chatbot_prompt},
            {"role": "user", "content": user_message}
        ],
        max_tokens=100,
        temperature=0.5
    )
    # AI가 생성한 일정 텍스트 반환
    return response['choices'][0]['message']['content'].strip()
