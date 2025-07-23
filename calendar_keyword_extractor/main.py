import json
from utils.preprocessing import extract_titles_from_events
from services.keyword_extractor import extract_keywords_from_calendar

# JSON 데이터 읽기
with open("data/sample_calendar.json", "r", encoding="utf-8") as f:
    calendar_data = json.load(f)

# events 배열에서 title 리스트 추출
titles = extract_titles_from_events(calendar_data)

# GPT 호출해서 키워드 뽑기
keywords = extract_keywords_from_calendar(titles)

print("📌 추출된 주요 키워드:")
print(keywords)
