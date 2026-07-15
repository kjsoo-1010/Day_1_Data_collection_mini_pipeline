#---------------------------------
# 작성목적: 데이터 수집 미니 파이프라인에서 수집한 JSON 데이터를 Pydantic 모델로 변환 및 검증하는 함수 정의
#
# 작성일: 2026.07.15
# 설명: 
# 1. 데이터 수집 미니 파이프라인 4단계
# 2. Open-Meteo, IP-API, Countries API 총 3가지 API에서 수집한 JSON 파일(tests/fixtures 의 {API}_sample.json 참고)에서 필요한 필드 추출하여 Pydantic 모델 정의
#---------------------------------


from pydantic import ValidationError
from .schemas import CountryInfo, IPInfo, WeatherHourlyRecord

## Open-Meteo API 
def transform_weather(raw: dict) -> list[WeatherHourlyRecord]:
    hourly = raw["hourly"]
    records = []
    for t, temp, precip in zip(
        hourly["time"], hourly["temperature_2m"], hourly["precipitation_probability"], strict=True
    ):
        try:
            records.append(
                WeatherHourlyRecord(
                    time=t, temperature_2m=temp, precipitation_probability=precip
                )
            )
        except ValidationError as e:
            print(f"skip invalid weather row: {e}")
    return records

## IP-API
def transform_ip(raw: dict) -> IPInfo | None:
    try:
        return IPInfo.model_validate(raw)
    except ValidationError as e:
        print(f"invalid ip record: {e}")
        return None

## Countries API
def transform_country(raw: dict) -> CountryInfo | None:
    try:
        return CountryInfo(
            name=raw["name"],
            capital=raw["capital"],
            region=raw["region"],
            subregion=raw["subregion"],
            population=raw["population"],
            area=raw["area"],
            alpha2_code=raw["alpha2Code"],
            alpha3_code=raw["alpha3Code"],
            languages=", ".join(lang["name"] for lang in raw["languages"]),
            currencies=", ".join(cur["code"] for cur in raw["currencies"]),
            flag_png=raw["flags"]["png"],
        )
    except (ValidationError, KeyError) as e:
        print(f"invalid country record: {e}")
        return None
