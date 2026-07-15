from pydantic import ValidationError

from .schemas import CountryInfo, IPInfo, WeatherHourlyRecord


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


def transform_ip(raw: dict) -> IPInfo | None:
    try:
        return IPInfo.model_validate(raw)
    except ValidationError as e:
        print(f"invalid ip record: {e}")
        return None


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
