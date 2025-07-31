# import os
# from openai import OpenAI
# from dotenv import load_dotenv
# import tiktoken

# # ✅ .env에서 API 키 로드
# load_dotenv()
# # 환경 변수 로드 (create_app 내에서 호출하여 앱 컨텍스트에 종속되도록)
# load_dotenv(override=True)
# OPENAI_API_KEY = os.getenv('OPEN_API_KEY')
# DEFAULT_MODEL = os.getenv("GET_DEFAULT_MODEL", "gpt-4o-mini")
# client = OpenAI(api_key=OPENAI_API_KEY)
# encoding = tiktoken.encoding_for_model(DEFAULT_MODEL)

# # # ✅ OpenAI 클라이언트 초기화
# # client = OpenAI(api_key=OPENAI_API_KEY)

# def ask_gpt(prompt: str, model="gpt-4o"):
#     """
#     최신 openai 패키지(v1 이상) 방식으로 GPT 호출
#     """
#     response = client.chat.completions.create(
#         model=model,
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.3
#     )

#     return response.choices[0].message.content.strip()

import os
from dotenv import load_dotenv
import google.generativeai as genai

# ✅ 환경 변수 로드 (.env에서 GOOGLE_API_KEY 불러오기)
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# DEFAULT_MODEL = os.getenv("GET_DEFAULT_MODEL", "gemini-1.5-pro")

# ✅ Gemini API 클라이언트 설정
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def ask_gpt(prompt: str, model_name=None):
    """
    Google Gemini API로 프롬프트 전달해 응답 받는 함수
    """
    try:
        use_model = genai.GenerativeModel("gemini-1.5-flash")
        response = use_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("❌ Gemini 응답 오류:", e)
        return "서버 오류로 응답을 받지 못했습니다."
