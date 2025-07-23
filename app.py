# Flask 앱의 진입점 파일입니다.
# 블루프린트(라우트 모듈)만 등록하고, 실제 비즈니스 로직은 각 모듈에서 처리합니다.

from flask import Flask
from routes.chatbot import chatbot_bp

app = Flask(__name__)

# 챗봇 라우트 블루프린트 등록
app.register_blueprint(chatbot_bp)

if __name__ == '__main__':
    # 개발용 서버 실행 (실서비스는 WSGI 서버 권장)
    app.run(host='0.0.0.0', port=5000, debug=True)
