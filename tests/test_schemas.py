import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from pipeline.schemas import IPInfo, WeatherHourlyRecord
from pipeline.transform import transform_ip, transform_weather

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def weather_raw() -> dict:
    return json.loads((FIXTURES_DIR / "weather_sample.json").read_text())


@pytest.fixture
def ip_raw() -> dict:
    return json.loads((FIXTURES_DIR / "ip_sample.json").read_text())


def test_weather_hourly_record_valid():
    record = WeatherHourlyRecord(
        time="2026-07-15T00:00", temperature_2m=25.1, precipitation_probability=100
    )
    assert record.temperature_2m == 25.1
    assert record.precipitation_probability == 100


def test_weather_hourly_record_missing_field_raises():
    with pytest.raises(ValidationError):
        WeatherHourlyRecord(time="2026-07-15T00:00", precipitation_probability=50)


def test_weather_hourly_record_out_of_range_raises():
    with pytest.raises(ValidationError):
        WeatherHourlyRecord(
            time="2026-07-15T00:00", temperature_2m=25.1, precipitation_probability=150
        )


def test_transform_weather_from_fixture(weather_raw):
    records = transform_weather(weather_raw)
    assert len(records) == 72
    assert all(isinstance(r, WeatherHourlyRecord) for r in records)


def test_ip_info_valid_from_fixture(ip_raw):
    info = IPInfo.model_validate(ip_raw)
    assert info.query == "8.8.8.8"
    assert info.country_code == "US"


def test_ip_info_missing_required_field_raises(ip_raw):
    del ip_raw["status"]
    with pytest.raises(ValidationError):
        IPInfo.model_validate(ip_raw)


def test_ip_info_wrong_type_raises(ip_raw):
    ip_raw["lat"] = "not-a-number"
    with pytest.raises(ValidationError):
        IPInfo.model_validate(ip_raw)


def test_transform_ip_invalid_returns_none(ip_raw):
    del ip_raw["status"]
    assert transform_ip(ip_raw) is None
