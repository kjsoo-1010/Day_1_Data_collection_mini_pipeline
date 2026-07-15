#---------------------------------
# 작성목적: 데이터 수집 미니 파이프라인에서 수집된 데이터 및 저장/불러오기 성능 벤치마크
#
# 작성일: 2026.07.15
# 설명: 
# 1. 데이터 수집 미니 파이프라인 검증 단계
# 2. CSV 및 Parquet 형식으로 저장/불러오기 성능 벤치마크
#---------------------------------

import time
from pathlib import Path
import pandas as pd

from .storage import load_csv, load_parquet, save_csv, save_parquet

# CSV, Parquet 저장/불러오기 성능 벤치마크 함수 정의
def run_benchmark(datasets: dict[str, pd.DataFrame], out_dir: Path) -> pd.DataFrame:
    rows = []
    for name, df in datasets.items():
        csv_path = out_dir / f"{name}.csv"
        parquet_path = out_dir / f"{name}.parquet"

        start = time.perf_counter()
        save_csv(df, csv_path)
        rows.append(_row(name, "csv", "write", time.perf_counter() - start))

        start = time.perf_counter()
        save_parquet(df, parquet_path)
        rows.append(_row(name, "parquet", "write", time.perf_counter() - start))

        start = time.perf_counter()
        load_csv(csv_path)
        rows.append(_row(name, "csv", "read", time.perf_counter() - start))

        start = time.perf_counter()
        load_parquet(parquet_path)
        rows.append(_row(name, "parquet", "read", time.perf_counter() - start))

    return pd.DataFrame(rows)


def _row(dataset: str, fmt: str, operation: str, seconds: float) -> dict:
    return {"dataset": dataset, "format": fmt, "operation": operation, "seconds": seconds}
