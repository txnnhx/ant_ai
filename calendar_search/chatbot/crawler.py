# import requests
# from bs4 import BeautifulSoup
# import os
# from dotenv import load_dotenv

# load_dotenv()

# NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
# NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

# def search_naver(query):
#     """
#     네이버 뉴스 검색 Open API로 뉴스 제목과 링크 3개 추출
#     """
#     url = "https://openapi.naver.com/v1/search/news.json"
#     headers = {
#         "X-Naver-Client-Id": NAVER_CLIENT_ID,
#         "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
#     }
#     params = {
#         "query": query,
#         "display": 3,
#         "sort": "date"
#     }

#     res = requests.get(url, headers=headers, params=params)
#     items = res.json().get("items", [])

#     results = []
#     for item in items:
#         results.append({
#             "title": item["title"],
#             "link": item["link"]
#         })

#     return results


# def extract_page_text(url):
#     """
#     뉴스 링크에 접속해 본문 텍스트 추출 (가능한 경우)
#     """
#     try:
#         headers = {"User-Agent": "Mozilla/5.0"}
#         res = requests.get(url, headers=headers, timeout=5)
#         res.encoding = res.apparent_encoding
#         soup = BeautifulSoup(res.text, "html.parser")

#         candidates = [
#             soup.find(id="newsct_article"),
#             soup.find("article"),
#             soup.find("div", class_="content"),
#             soup.find("main"),
#             soup.find("body")
#         ]

#         for c in candidates:
#             if c and c.get_text(strip=True):
#                 return c.get_text(" ", strip=True)

#         return ""
#     except:
#         return ""

import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# .env에서 API 키 불러오기
load_dotenv()
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")


def search_naver(query):
    """
    네이버 뉴스 검색 Open API로 뉴스 제목과 링크 3개 추출
    """
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    params = {
        "query": query,
        "display": 3,
        "sort": "date"
    }

    try:
        res = requests.get(url, headers=headers, params=params)
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


def extract_page_text(url):
    """
    뉴스 링크에 접속해 본문 텍스트 추출 (네이버 뉴스 및 기타 사이트 대응)
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=5)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, "html.parser")

        # ✅ 네이버 뉴스 본문 특화 처리
        naver_main = soup.select_one("div#newsct_article")
        if naver_main:
            return naver_main.get_text(" ", strip=True)

        # ✅ 일반 뉴스 구조 대응 백업
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
