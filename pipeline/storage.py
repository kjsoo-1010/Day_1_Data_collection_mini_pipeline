#---------------------------------
# 작성목적: 데이터 수집 미니 파이프라인에서 검증 완료된 데이터를 저장하고 불러오는 기능
#
# 작성일: 2026.07.15
# 설명: 
# 1. 데이터 수집 미니 파이프라인 5단계
# 2. 검증 완료된 데이터를 CSV 및 Parquet 형식으로 저장하고 불러오는 함수 정의
#---------------------------------

from pathlib import Path

import pandas as pd


def save_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def save_parquet(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, engine="pyarrow", index=False)


def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def load_parquet(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path, engine="pyarrow")
