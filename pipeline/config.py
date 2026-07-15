from pathlib import Path

WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=37.5665&longitude=126.9780"
    "&hourly=temperature_2m,precipitation_probability"
    "&forecast_days=3&timezone=Asia/Seoul"
)
IP_URL = "http://ip-api.com/json/8.8.8.8"
COUNTRY_URL = "https://countries.dev/alpha/KR"

TIMEOUT = 10.0

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
