import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# .env에서 API 키 불러오기
load_dotenv()


class NaverCrawler:
    """
    네이버 뉴스 검색 및 본문 추출 기능을 제공하는 클래스
    """
    def __init__(self):
        self.base_url = "https://openapi.naver.com/v1/search/news.json"
        self.headers = {
            "X-Naver-Client-Id": os.getenv("NAVER_CLIENT_ID"),
            "X-Naver-Client-Secret": os.getenv("NAVER_CLIENT_SECRET")
        }

    def search(self, query, display=3):
        """
        네이버 뉴스 검색 API 호출 → 뉴스 제목 + 링크 리스트 반환
        """
        params = {
            "query": query,
            "display": display,
            "sort": "date"
        }

        try:
            res = requests.get(self.base_url, headers=self.headers, params=params)
            res.raise_for_status()
            items = res.json().get("items", [])

            results = []
            for item in items:
                results.append({
                    "title": item["title"],
                    "link": item["link"]
                })
            return results
        except Exception as e:
            print("❌ 네이버 뉴스 검색 실패:", e)
            return []

    def extract_text(self, url):
        """
        뉴스 본문 HTML에서 텍스트 추출 (네이버 뉴스 대응 포함)
        """
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers, timeout=5)
            res.encoding = res.apparent_encoding
            soup = BeautifulSoup(res.text, "html.parser")

            # ✅ 네이버 뉴스 전용 div
            naver_main = soup.select_one("div#newsct_article")
            if naver_main:
                return naver_main.get_text(" ", strip=True)

            # ✅ 일반 구조 백업 추출
            candidates = [
                soup.find("article"),
                soup.find("div", class_="content"),
                soup.find("main"),
                soup.find("body")
            ]

            for c in candidates:
                if c and c.get_text(strip=True):
                    return c.get_text(" ", strip=True)

            return ""
        except Exception as e:
            print("❌ 본문 추출 실패:", e)
            return ""
