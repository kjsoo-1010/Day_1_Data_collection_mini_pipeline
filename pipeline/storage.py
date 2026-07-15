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
