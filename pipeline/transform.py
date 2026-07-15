from pydantic import ValidationError

from .schemas import WeatherHourlyRecord


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
