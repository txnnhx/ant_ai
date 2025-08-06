import os
import base64
import datetime
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
from PIL.ExifTags import TAGS

class PhotoAnalyzer:
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ OpenAI API 키가 설정되지 않았습니다.")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def get_taken_date(self, file_path):
        """EXIF에서 촬영일자 추출"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"❌ 파일이 존재하지 않습니다: {file_path}")
        try:
            image = Image.open(file_path)
            exif_data = image._getexif()
            if not exif_data:
                return None
            for tag, value in exif_data.items():
                if TAGS.get(tag) == "DateTimeOriginal":
                    return datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
            return None
        except Exception as e:
            print(f"❌ EXIF 오류: {e}")
            return None

    def image_to_base64(self, image_path):
        """이미지를 base64 인코딩"""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def extract_summary(self, image_path):
        """이미지 요약 및 토큰 사용량 반환"""
        base64_image = self.image_to_base64(image_path)
        prompt = """
다음 이미지를 보고 아래 항목에 따라 요약해줘. 딱 아래 json 형식 그대로만 응답해줘.

{
  "장소": (예상 장소),
  "활동": (주요 활동),
  "분위기": (사진 분위기),
  "시간대": (낮/밤/해질녘 등),
  "키워드": (단어 나열)
}
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "이미지 분석 전문가로서 사용자 요청에 따라 이미지를 정리해줘."},
                    {"role": "user", "content": prompt},
                    {"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}
                ],
                max_tokens=512,
                temperature=0.4
            )
            reply = response.choices[0].message.content.strip()
            token_info = response.usage
            return reply, token_info
        except Exception as e:
            print(f"❌ GPT 호출 오류: {e}")
            return None, None




if __name__ == "__main__":
    # ✅ 분석기 객체 생성
    analyzer = PhotoAnalyzer()

    # ✅ 분석할 이미지 경로
    image_path = "IMG_6284.jpeg"

    # ✅ 촬영일자 추출
    taken_date = analyzer.get_taken_date(image_path)
    print("📷 촬영일자:", taken_date.strftime('%Y-%m-%d %H:%M:%S') if taken_date else "없음")

    # ✅ GPT 요약 및 토큰 사용량
    summary, usage = analyzer.extract_summary(image_path)

    if summary:
        print("\n🤖 GPT 요약:\n", summary)
    else:
        print("\n❌ 요약 실패")

    if usage:
        print("\n📊 토큰 사용량:")
        print(f" - Prompt tokens:     {usage.prompt_tokens}")
        print(f" - Completion tokens: {usage.completion_tokens}")
        print(f" - Total tokens:      {usage.total_tokens}")
    else:
        print("\n❌ 토큰 사용량 확인 실패")