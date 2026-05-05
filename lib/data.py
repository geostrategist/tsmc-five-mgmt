"""Data loaders for the TSMC five-management Streamlit demo."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
QUARTERLY_CSV = DATA_DIR / "quarterly.csv"
MARKDOWN_DIR = DATA_DIR / "transcripts"

CHART_HEIGHT = 420

PLATFORM_LABELS = {
    "plat_hpc_pct": "HPC 高效運算",
    "plat_smartphone_pct": "Smartphone 智慧手機",
    "plat_iot_pct": "IoT 物聯網",
    "plat_automotive_pct": "Automotive 車用",
    "plat_dce_pct": "DCE 數位消費電子",
}

NODE_LABELS = {
    "node_2nm_pct": "2nm",
    "node_3nm_pct": "3nm",
    "node_5nm_pct": "5nm",
    "node_7nm_pct": "7nm",
    "node_10nm_pct": "10nm",
    "node_16nm_pct": "16nm",
    "node_28nm_pct": "28nm",
}


@st.cache_data
def load_quarterly() -> pd.DataFrame:
    df = pd.read_csv(QUARTERLY_CSV)
    df["call_date"] = pd.to_datetime(df["call_date"], errors="coerce")
    quarter_int = df["quarter"].str.extract(r"Q(\d)").astype(int)
    df["quarter_idx"] = df["year"] * 4 + quarter_int.iloc[:, 0]
    df = df.sort_values("quarter_idx").reset_index(drop=True)
    df["quarter_label"] = df["year"].astype(str) + " " + df["quarter"]
    return df


@st.cache_data
def load_transcript(quarter_key: str) -> str:
    """Load full markdown transcript for a quarter, or empty string if missing."""
    path = MARKDOWN_DIR / f"{quarter_key}.md"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def latest_two(df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    return df.iloc[-1], df.iloc[-2]


def fmt_delta(curr, prev, pct: bool = False, digits: int = 1) -> str | None:
    if pd.isna(curr) or pd.isna(prev):
        return None
    diff = curr - prev
    if pct:
        return f"{diff:+.{digits}f} pp"
    return f"{diff:+.{digits}f}"
