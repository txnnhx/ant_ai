# 챗봇 기반 일정 처리 라우트 모듈입니다.
# /chat 엔드포인트에서 사용자의 일정 요청을 받아 서비스 계층에 위임합니다.

from flask import Blueprint, request, jsonify
from services.schedule_generator import generate_schedule
from models.schema import ScheduleRequest

# Flask 블루프린트 객체 생성
chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    # JSON 요청에서 message 추출
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        # message가 없으면 에러 반환
        return jsonify({'error': '메시지를 입력해주세요.'}), 400

    # Pydantic 모델로 요청 검증
    req = ScheduleRequest(message=user_message)
    try:
        # 서비스 계층에 일정 생성 요청
        result = generate_schedule(req.message)
        return jsonify({'result': result})
    except Exception as e:
        # 예외 발생 시 에러 반환
        return jsonify({'error': str(e)}), 500
