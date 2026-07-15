import asyncio

import pandas as pd

from pipeline.benchmark import run_benchmark
from pipeline.config import DATA_DIR, REPORTS_DIR
from pipeline.fetch import fetch_all
from pipeline.schemas import CountryInfo, IPInfo
from pipeline.transform import transform_country, transform_ip, transform_weather


async def collect() -> tuple[list, IPInfo | None, CountryInfo | None]:
    weather_raw, ip_raw, country_raw = await fetch_all()
    weather_records = transform_weather(weather_raw)
    ip_record = transform_ip(ip_raw)
    country_record = transform_country(country_raw)
    return weather_records, ip_record, country_record


def main() -> None:
    weather_records, ip_record, country_record = asyncio.run(collect())

    print(f"weather: {len(weather_records)} valid rows")
    print(f"ip: {'1 valid row' if ip_record else '0 valid rows'}")
    print(f"country: {'1 valid row' if country_record else '0 valid rows'}")

    datasets = {"weather": pd.DataFrame([r.model_dump() for r in weather_records])}
    if ip_record is not None:
        datasets["ip"] = pd.DataFrame([ip_record.model_dump()])
    if country_record is not None:
        datasets["country"] = pd.DataFrame([country_record.model_dump()])

    results = run_benchmark(datasets, DATA_DIR)
    comparison = results.pivot(index=["dataset", "format"], columns="operation", values="seconds")
    caveat = (
        "(ip/country datasets have only 1 row, so their timing mostly reflects fixed"
        " overhead, not format scaling.)"
    )

    print("\nRead/Write benchmark (seconds):")
    print(comparison)
    print(f"\n{caveat}")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "benchmark_result.txt"
    report_path.write_text(f"Read/Write benchmark (seconds):\n{comparison}\n\n{caveat}\n")


if __name__ == "__main__":
    main()
