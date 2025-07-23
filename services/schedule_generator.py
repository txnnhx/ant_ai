# 일정 생성 서비스 계층입니다.
# 프롬프트 빌더를 호출해 실제로 OpenAI로부터 일정을 받아옵니다.

from services.prompt_builder import build_prompt_and_call

def generate_schedule(user_message: str) -> str:
    """
    사용자 메시지를 받아 프롬프트 빌더를 통해 일정 생성 결과를 반환합니다.
    """
    result = build_prompt_and_call(user_message)
    print("[AI가 생성한 일정 텍스트]", result)
    return result
