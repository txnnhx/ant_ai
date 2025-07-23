from models.model_interface import ask_gpt

def extract_keywords_from_calendar(sentences: list[str]) -> list[str]:
    """
    일정 데이터 리스트를 받아 GPT를 통해 키워드를 추출한다.
    """

    # ✅ 프롬프트 템플릿을 불러온다 (사용자가 직접 작성)
    with open("prompts/gpt_prompt.txt", "r", encoding="utf-8") as f:
        prompt_template = f.read()

    # ✅ 리스트 형태의 일정 데이터를 한 줄로 합친다
    joined_data = "\n".join(sentences)

    # ✅ 최종 GPT에게 보낼 프롬프트 구성 (프롬프트 + 일정 목록)
    full_prompt = f"{prompt_template}\n\n{joined_data}"

    # ✅ GPT 호출
    response = ask_gpt(full_prompt)

    # ✅ GPT 응답을 쉼표 기준으로 나눠 리스트로 정제
    keywords = [kw.strip() for kw in response.strip().split(",") if kw.strip()]
    
    return keywords
