# 요청/응답 데이터 구조를 정의하는 Pydantic 모델 모듈입니다.

from pydantic import BaseModel

class ScheduleRequest(BaseModel):
    """
    일정 생성 요청에서 message(자유 입력 텍스트)만 받습니다.
    """
    message: str
