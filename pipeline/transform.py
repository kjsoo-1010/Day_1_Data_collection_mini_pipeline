from pydantic import ValidationError

from .schemas import IPInfo, WeatherHourlyRecord


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
