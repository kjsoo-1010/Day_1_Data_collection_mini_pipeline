import asyncio

import pandas as pd

from pipeline.benchmark import run_benchmark
from pipeline.config import DATA_DIR
from pipeline.fetch import fetch_all
from pipeline.schemas import IPInfo
from pipeline.transform import transform_ip, transform_weather


async def collect() -> tuple[list, IPInfo | None]:
    weather_raw, ip_raw = await fetch_all()
    weather_records = transform_weather(weather_raw)
    ip_record = transform_ip(ip_raw)
    return weather_records, ip_record


def main() -> None:
    weather_records, ip_record = asyncio.run(collect())

    print(f"weather: {len(weather_records)} valid rows")
    print(f"ip: {'1 valid row' if ip_record else '0 valid rows'}")

    datasets = {"weather": pd.DataFrame([r.model_dump() for r in weather_records])}
    if ip_record is not None:
        datasets["ip"] = pd.DataFrame([ip_record.model_dump()])

    results = run_benchmark(datasets, DATA_DIR)
    print("\nRead/Write benchmark (seconds):")
    print(results.pivot(index=["dataset", "format"], columns="operation", values="seconds"))
    print(
        "\n(ip dataset has only 1 row, so its timing mostly reflects fixed overhead,"
        " not format scaling.)"
    )


if __name__ == "__main__":
    main()
