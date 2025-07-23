import re
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pdfplumber
from docx import Document

class TextCalendar:
    def __init__(self):
        self.extracted_events = []
    
    def process_input(self, input_source, input_type="text"):
        """
        다양한 입력 소스를 텍스트로 변환
        
        Args:
            input_source: 입력 데이터 (파일경로, URL, 텍스트, JSON 등)
            input_type: "file", "url", "text", "json", "user_prompt"
        
        Returns:
            str: 정제된 텍스트
        """
        
        if input_type == "file":
            return self._process_file(input_source)
        elif input_type == "url":
            return self._process_url(input_source)
        elif input_type == "text":
            return input_source
        elif input_type == "json":
            return self._process_json(input_source)
        elif input_type == "user_prompt":
            return self._process_user_prompt(input_source)
        else:
            raise ValueError(f"Unsupported input type: {input_type}")
    
    def _process_file(self, file_path):
        """파일을 텍스트로 변환"""
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif file_path.endswith('.pdf'):
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text
        
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
    
    def _process_url(self, url):
        """웹페이지를 텍스트로 변환"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 불필요한 태그 제거
            for tag in soup(['script', 'style', 'nav', 'footer']):
                tag.decompose()
            
            return soup.get_text(separator=' ', strip=True)
        except Exception as e:
            raise Exception(f"URL 처리 실패: {str(e)}")
    
    def _process_json(self, json_data):
        """JSON 데이터를 텍스트로 변환"""
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        
        # JSON을 자연스러운 텍스트로 변환
        text = ""
        if 'events' in json_data:
            for event in json_data['events']:
                text += f"{event.get('date', '')} {event.get('time', '')}에 "
                text += f"{event.get('title', '')} {event.get('location', '')}\n"
        else:
            # 일반적인 JSON을 텍스트로 변환
            text = json.dumps(json_data, ensure_ascii=False, indent=2)
        
        return text
    
    def _process_user_prompt(self, prompt):
        """사용자 프롬프트 정제"""
        # 기본적으로는 그대로 반환, 필요시 전처리 추가
        return prompt.strip()
    
    def extract_schedule_info(self, text):
        """
        텍스트에서 일정 정보 추출
        
        Args:
            text (str): 정제된 텍스트
        
        Returns:
            list: 추출된 일정 정보 리스트
        """
        events = []
        
        # 날짜 패턴 매칭
        date_patterns = [
            r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})',  # 2024-12-15
            r'(\d{1,2}월\s*\d{1,2}일)',        # 12월 15일
            r'(오늘|내일|모레)',                # 상대적 날짜
            r'(\d{1,2}일부터\s*\d{1,2}일까지)', # 15일부터 17일까지
        ]
        
        # 시간 패턴 매칭
        time_patterns = [
            r'(\d{1,2}:\d{2})',              # 14:30
            r'(오전|오후)\s*(\d{1,2})시',     # 오후 2시
            r'(\d{1,2})시\s*(\d{1,2})분',    # 2시 30분
        ]
        
        # 활동/장소 패턴 매칭
        activity_patterns = [
            r'(미용실|병원|회의|약속|수업|운동)',
            r'(예약|방문|참석|진행)',
        ]
        
        lines = text.split('\n')
        for line in lines:
            if not line.strip():
                continue
                
            event_info = {
                'original_text': line,
                'title': '',
                'date': '',
                'time': '',
                'location': '',
                'description': ''
            }
            
            # 날짜 추출
            for pattern in date_patterns:
                matches = re.findall(pattern, line)
                if matches:
                    event_info['date'] = matches[0]
                    break
            
            # 시간 추출
            for pattern in time_patterns:
                matches = re.findall(pattern, line)
                if matches:
                    if isinstance(matches[0], tuple):
                        event_info['time'] = ' '.join(matches[0])
                    else:
                        event_info['time'] = matches[0]
                    break
            
            # 활동 추출
            for pattern in activity_patterns:
                matches = re.findall(pattern, line)
                if matches:
                    event_info['title'] = matches[0]
                    break
            
            # 제목이 없으면 전체 라인을 제목으로
            if not event_info['title']:
                event_info['title'] = line.strip()
            
            events.append(event_info)
        
        return events
    
    def process_text(self, input_source, input_type="text"):
        """
        전체 텍스트 처리 파이프라인
        
        Args:
            input_source: 입력 데이터
            input_type: 입력 타입
        
        Returns:
            list: 구조화된 일정 데이터
        """
        try:
            # 1단계: 입력을 텍스트로 변환
            text = self.process_input(input_source, input_type)
            
            # 2단계: 일정 정보 추출
            events = self.extract_schedule_info(text)
            
            # 3단계: 후처리 및 검증
            processed_events = self._post_process_events(events)
            
            return processed_events
            
        except Exception as e:
            raise Exception(f"텍스트 처리 중 오류 발생: {str(e)}")
    
    def _post_process_events(self, events):
        """추출된 이벤트 후처리"""
        processed = []
        
        for event in events:
            # 빈 이벤트 제거
            if not any([event['title'], event['date'], event['time']]):
                continue
            
            # 날짜 정규화
            if event['date']:
                event['date'] = self._normalize_date(event['date'])
            
            # 시간 정규화
            if event['time']:
                event['time'] = self._normalize_time(event['time'])
            
            processed.append(event)
        
        return processed
    
    def _normalize_date(self, date_str):
        """날짜 정규화"""
        # 여기서 다양한 날짜 형식을 표준 형식으로 변환
        # 예: "12월 15일" -> "2024-12-15"
        return date_str
    
    def _normalize_time(self, time_str):
        """시간 정규화"""
        # 여기서 다양한 시간 형식을 표준 형식으로 변환
        # 예: "오후 2시" -> "14:00"
        return time_str 