from gpt_extractor.datapcr_gpt import CalendarDataProcessor
from gpt_search.naver_text_extract import NewsScheduleExtractor
processor = CalendarDataProcessor()
search = NewsScheduleExtractor()

def run_datapcr(input_data: str, is_file: bool = True) -> dict:
    """
    GPT Mediator: 파일/텍스트 여부만 판단 → 실제 분기/판단은 CalendarDataProcessor 내부에서 처리
    :param input_data: 파일 경로 또는 일반 텍스트
    :param is_file: True = 파일, False = 일반 텍스트
    :return: {"type": "schedule"/"search", "data"/"query": ...}
    """
    if is_file:
        return processor.process(input_data)
    else:
        # 텍스트 직접 넣어서 처리하는 별도 함수가 datapcr_gpt.py 안에 있다면 이걸로 대체
        return search.extraction(input_data)