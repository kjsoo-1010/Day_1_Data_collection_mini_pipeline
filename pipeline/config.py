#---------------------------------
# 작성목적: 데이터 수집 미니 파이프라인에서 수집할 3가지 API 정보 저장
#
# 작성일: 2026.07.15
# 설명: 
# 1. 데이터 수집 미니 파이프라인 1단계
# 2. Open-Meteo, IP-API, Countries API 총 3가지 API의 
#    API URL, TIMEOUT, DATA_DIR, REPORTS_DIR 값
#---------------------------------

from pathlib import Path

# 3가지 API URL 정의

## 1. Open-Meteo API (서울 3일 시간대별 기온·강수확률)
WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=37.5665&longitude=126.9780"
    "&hourly=temperature_2m,precipitation_probability"
    "&forecast_days=3&timezone=Asia/Seoul"
)

## 2. IP-API (IP 기반 지역 정보)
IP_URL = "http://ip-api.com/json/8.8.8.8"

## 3. Countries API (한국 국가 정보)
COUNTRY_URL = "https://countries.dev/alpha/KR"

# API 요청 시 타임아웃 설정 (초 단위)
TIMEOUT = 10.0

# 받아온 데이터 저장 경로 및 보고서 저장 경로 정의
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
