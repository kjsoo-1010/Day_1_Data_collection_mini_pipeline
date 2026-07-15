#---------------------------------
# 작성목적: 데이터 수집 미니 파이프라인에서 API Pydantic 모델 정의
#
# 작성일: 2026.07.15
# 설명: 
# 1. 데이터 수집 미니 파이프라인 3단계
# 2. Open-Meteo, IP-API, Countries API 총 3가지 API에서 수집한 JSON 파일(tests/fixtures 의 {API}_sample.json 참고)에서 필요한 필드 추출하여 Pydantic 모델 정의
#---------------------------------

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


## 1. Open-Meteo API (서울 3일 시간대별 기온·강수확률) Pydantic v2 모델 정의
class WeatherHourlyRecord(BaseModel):
    time: datetime # 시간
    temperature_2m: float # 기온
    precipitation_probability: int = Field(ge=0, le=100) # 강수 확률 

## 2. IP-API (IP 기반 지역 정보) Pydantic v2 모델 정의
class IPInfo(BaseModel):
    # 필드명 변경을 위한 ConfigDict 설정
    model_config = ConfigDict(populate_by_name=True)

    query: str
    status: str
    country: str
    country_code: str = Field(alias="countryCode") # 카멜 케이스에서 스네이크 케이스로 변경
    region_name: str = Field(alias="regionName") # 카멜 케이스에서 스네이크 케이스로 변경
    city: str
    lat: float
    lon: float
    timezone: str
    isp: str
    org: str | None = None
    as_number: str | None = Field(default=None, alias="as") # as는 파이썬 예약어이므로 as_number로 변경

## 3. Countries API (한국 국가 정보) Pydantic v2 모델 정의
class CountryInfo(BaseModel):
    name: str
    capital: str
    region: str
    subregion: str
    population: int
    area: float
    alpha2_code: str
    alpha3_code: str
    languages: str
    currencies: str
    flag_png: str
