def extract_titles_from_events(data: dict) -> list[str]:
    """
    calendar JSON에서 events 배열의 title만 뽑아서 리스트로 반환하는 함수
    """
    titles = []
    for event in data.get("events", []):
        title = event.get("title")
        if title:
            titles.append(title)
    return titles


# def json_to_text_list(data: dict) -> list[str]:
#     """
#     중첩 JSON 데이터를 '8월 3일 홍대에서 공연 관람' 같은
#     텍스트 일정 리스트로 변환하는 함수
#     """
#     result = []
#     for id_, years in data.items():
#         for year, months in years.items():
#             for month, days in months.items():
#                 for day, events in days.items():
#                     for event in events:
#                         text = f"{month}월 {day}일 {event}"
#                         result.append(text)
#     return result
