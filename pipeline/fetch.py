#---------------------------------
# 작성목적: 데이터 수집 미니 파이프라인에서 3가지 API를 JSON 파일로 동시에 수집하는 비동기 함수 정의
#
# 작성일: 2026.07.15
# 설명: 
# 1. 데이터 수집 미니 파이프라인 2단계
# 2. Open-Meteo, IP-API, Countries API config를 바탕으로 raw json 데이터 수집.
# (Sample : tests/fixtures/{API}_sample.json)
#---------------------------------

import asyncio

import httpx

from .config import COUNTRY_URL, IP_URL, TIMEOUT, WEATHER_URL


# API 수집 공통 함수 정의
async def _get_json(client: httpx.AsyncClient, url: str) -> dict:
    resp = await client.get(url, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


## 각 API별 비동기 함수 정의

### Open-meteo API
async def fetch_weather(client: httpx.AsyncClient) -> dict:
    return await _get_json(client, WEATHER_URL)

### IP-API
async def fetch_ip(client: httpx.AsyncClient) -> dict:
    return await _get_json(client, IP_URL)

### Countries API
async def fetch_country(client: httpx.AsyncClient) -> dict:
    return await _get_json(client, COUNTRY_URL)

## 정의한 비동기 함수들을 asyncio.gather()를 이용하여 동시에 실행하는 함수 정의
async def fetch_all() -> tuple[dict, dict, dict]:
    async with httpx.AsyncClient() as client:
        return await asyncio.gather(
            fetch_weather(client),
            fetch_ip(client),
            fetch_country(client),
        )
