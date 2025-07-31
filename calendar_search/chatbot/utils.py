import json

def is_valid_json(text):
    """
    문자열이 JSON 형식이며 'events' 키가 포함된 일정 JSON인지 확인
    """
    try:
        data = json.loads(text)
        return "events" in data
    except:
        return False
