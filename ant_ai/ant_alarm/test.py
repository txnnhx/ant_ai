from mediator import ScheduleMediator

# 🔧 테스트용 일정 직접 입력 (여기만 바꾸면 됨)
schedules = [
        {
            "title": "종강",
            "start_date": "2025-06-20T10:00:00",
            "end_date": "2025-06-20T11:00:00"
        },
        {
            "title": "서울주류박람회",
            "start_date": "2025-06-26T10:00:00",
            "end_date": "2025-06-26T11:00:00"
        },
        {
            "title": "일본여행",
            "start_date": "2025-06-27T10:00:00",
            "end_date": "2025-06-30T11:00:00"
        },
        {
            "title": "중간발표",
            "start_date": "2025-08-08T10:00:00",
            "end_date": "2025-08-08T11:00:00"
        },
]

# ✅ 중재자 실행
mediator = ScheduleMediator()
result = mediator.run(schedules)

# ✅ 결과 출력
print("🧠 중재자 결과:", result)