"""Data loaders for the TSMC five-management Streamlit demo."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
QUARTERLY_CSV = DATA_DIR / "quarterly.csv"
MARKDOWN_DIR = DATA_DIR / "transcripts"
NLP_PANEL_CSV = DATA_DIR / "nlp_panel.csv"
EVENT_STUDY_CSV = DATA_DIR / "event_study_panel.csv"
CROSS_MARKET_CSV = DATA_DIR / "cross_market.csv"
LDA_TOPICS_CSV = DATA_DIR / "lda_topics.csv"

FOCUS_YEAR_START = 2020

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


def _add_quarter_label(df: pd.DataFrame) -> pd.DataFrame:
    quarter_int = df["quarter"].str.extract(r"Q(\d)").astype(int)
    df["quarter_idx"] = df["year"] * 4 + quarter_int.iloc[:, 0]
    df = df.sort_values("quarter_idx").reset_index(drop=True)
    df["quarter_label"] = df["year"].astype(str) + " " + df["quarter"]
    return df


@st.cache_data
def load_nlp_panel(focus_year: int = FOCUS_YEAR_START) -> pd.DataFrame:
    """Sentiment lexicon rates, language drift, LDA topic weights per quarter."""
    df = pd.read_csv(NLP_PANEL_CSV)
    df["call_date"] = pd.to_datetime(df["call_date"], errors="coerce")
    df = df[df["year"] >= focus_year].copy()
    return _add_quarter_label(df)


@st.cache_data
def load_event_study(focus_year: int = FOCUS_YEAR_START) -> pd.DataFrame:
    """Cumulative abnormal return (CAR) windows per earnings call."""
    df = pd.read_csv(EVENT_STUDY_CSV)
    df["call_date"] = pd.to_datetime(df["call_date"], errors="coerce")
    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")
    df = df[df["year"] >= focus_year].copy()
    return _add_quarter_label(df)


@st.cache_data
def load_cross_market(focus_year: int = FOCUS_YEAR_START) -> pd.DataFrame:
    """TSM US vs 2330 TW CAR comparison around the same earnings event."""
    df = pd.read_csv(CROSS_MARKET_CSV)
    df["call_date"] = pd.to_datetime(df["call_date"], errors="coerce")
    df["year"] = df["quarter_key"].str.slice(0, 4).astype(int)
    df["quarter"] = df["quarter_key"].str.slice(5, 7)
    df = df[df["year"] >= focus_year].copy()
    return _add_quarter_label(df)


@st.cache_data
def load_lda_topics() -> pd.DataFrame:
    return pd.read_csv(LDA_TOPICS_CSV)


# === Geopolitical events (curated) ===
# Each entry: ISO date, short label (zh), category (used for color),
# detail (1-line context). Used to overlay vlines on time series and to render
# a dedicated timeline page.
GEO_EVENTS: list[dict] = [
    {"date": "2020-01-23", "label": "武漢封城", "cat": "pandemic",
     "detail": "中國武漢因 COVID-19 封城；半導體供應鏈受影響開端"},
    {"date": "2020-05-15", "label": "美國第一波華為禁令", "cat": "us_china",
     "detail": "美商務部限制使用美國技術製造的晶片出貨給華為，TSMC 被迫停接華為訂單"},
    {"date": "2020-09-15", "label": "華為禁令全面生效", "cat": "us_china",
     "detail": "9/15 起 TSMC 不再出貨華為；華為占 TSMC 約 14% 營收"},
    {"date": "2021-03-30", "label": "Intel IDM 2.0 宣布", "cat": "competitor",
     "detail": "Intel 宣布回歸晶圓代工，斥資 200 億美元在美建廠"},
    {"date": "2022-02-24", "label": "俄烏戰爭爆發", "cat": "geopolitics",
     "detail": "氖氣（俄烏供應半導體用量約 50%）供應鏈震盪"},
    {"date": "2022-08-02", "label": "Pelosi 訪台", "cat": "us_china",
     "detail": "中國對台軍演，美中緊張升級"},
    {"date": "2022-08-09", "label": "美國 CHIPS Act 簽署", "cat": "industry_policy",
     "detail": "527 億美元補貼，TSMC Arizona 廠後續獲得補助"},
    {"date": "2022-10-07", "label": "美國全面晶片管制", "cat": "us_china",
     "detail": "禁止 16/14nm 以下晶片設計與設備出口至中國；TSMC 中國客戶受影響"},
    {"date": "2023-01-30", "label": "美日荷三方協議", "cat": "us_china",
     "detail": "三國協議限制半導體設備出口至中國"},
    {"date": "2023-10-17", "label": "美國加碼晶片管制", "cat": "us_china",
     "detail": "管制再升級，AI 晶片出口受限"},
    {"date": "2024-04-08", "label": "TSMC Arizona 補助 66 億", "cat": "industry_policy",
     "detail": "美商務部 CHIPS Act 補助確定撥付，建廠進度加速"},
    {"date": "2024-11-06", "label": "Trump 當選 (2.0)", "cat": "geopolitics",
     "detail": "Trump 勝選，多次稱「台灣偷走美國晶片業」、威脅課關稅"},
    {"date": "2025-01-20", "label": "Trump 2.0 就職", "cat": "geopolitics",
     "detail": "正式上任後對台灣半導體政策不確定性升高"},
    {"date": "2025-04-02", "label": "Trump 對等關稅", "cat": "geopolitics",
     "detail": "全球關稅 10%、台灣 32%；半導體初期豁免但威脅後續"},
]


def geo_events_df() -> pd.DataFrame:
    df = pd.DataFrame(GEO_EVENTS)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date").reset_index(drop=True)


_NOISE_PATTERNS = [
    "STREETEVENTS",
    "lseg.com",
    "refinitiv.com",
    "thomsonreuters.com",
    "Republication or",
    "registered trademarks",
    "Contact Us",
    "All rights reserved",
    "prior written consent",
    "framing or similar",
    "(Chinese, English)",
]


def _clean_transcript(text: str) -> str:
    """Strip repeated LSEG / Refinitiv / Thomson Reuters boilerplate lines so
    full-text searches aren't dominated by copyright noise."""
    out = []
    for line in text.splitlines():
        if any(p in line for p in _NOISE_PATTERNS):
            continue
        if line.strip().startswith("©20"):
            continue
        out.append(line)
    return "\n".join(out)


@st.cache_data
def search_term(term: str, whole_word: bool = True, case_sensitive: bool = False) -> pd.DataFrame:
    """Full-text search across all transcripts (2020+).

    Returns one row per quarter with: quarter_key, year, quarter, count,
    sentences (list of strings containing the term), quarter_label, quarter_idx.
    """
    if not term or not term.strip():
        return pd.DataFrame(columns=["quarter_key", "year", "quarter", "count", "sentences"])

    import re as _re
    pattern = _re.escape(term.strip())
    if whole_word:
        pattern = rf"\b{pattern}\b"
    flags = 0 if case_sensitive else _re.IGNORECASE
    rx = _re.compile(pattern, flags)
    sent_split = _re.compile(r"(?<=[.!?])\s+")

    rows = []
    for path in sorted(MARKDOWN_DIR.glob("*.md")):
        qk = path.stem
        try:
            year = int(qk.split("_")[0])
            quarter = qk.split("_")[1]
        except (IndexError, ValueError):
            continue
        if year < FOCUS_YEAR_START:
            continue
        text = _clean_transcript(path.read_text(encoding="utf-8"))
        matches = rx.findall(text)
        count = len(matches)
        sentences: list[str] = []
        if count:
            for s in sent_split.split(text.replace("\n", " ")):
                s = " ".join(s.split())  # collapse whitespace
                if rx.search(s) and 20 < len(s) < 600:
                    sentences.append(s)
        rows.append({
            "quarter_key": qk,
            "year": year,
            "quarter": quarter,
            "count": count,
            "sentences": sentences,
        })

    df = pd.DataFrame(rows)
    if df.empty:
        return df
    return _add_quarter_label(df)


def highlight_term(sentence: str, term: str, case_sensitive: bool = False) -> str:
    """Wrap term occurrences in HTML <mark> tags for streamlit markdown rendering."""
    if not term:
        return sentence
    import re as _re
    flags = 0 if case_sensitive else _re.IGNORECASE
    pattern = _re.compile(f"({_re.escape(term)})", flags)
    return pattern.sub(r"<mark style='background:#FFE680;padding:0 2px;border-radius:2px;'>\1</mark>", sentence)


def add_geo_event_vlines(fig, x_dates: pd.Series, y_max=None, opacity: float = 0.25):
    """Overlay GEO_EVENTS as faint vertical lines + labels on a Plotly figure.
    Uses `add_shape` + `add_annotation` separately because `add_vline(annotation_*)`
    has a bug in plotly 5.x with datetime axes (it tries to .mean() Timestamps)."""
    if x_dates.empty:
        return fig
    lo, hi = x_dates.min(), x_dates.max()
    cat_colors = {
        "pandemic": "#888888",
        "us_china": "#8B0000",
        "geopolitics": "#5B2C6F",
        "industry_policy": "#1F4E79",
        "competitor": "#9C7A1A",
    }
    label_opacity = min(1.0, opacity * 3)
    for ev in GEO_EVENTS:
        d = pd.to_datetime(ev["date"])
        if d < lo or d > hi:
            continue
        color = cat_colors.get(ev["cat"], "#888888")
        # full-height dotted line
        fig.add_shape(
            type="line",
            x0=d, x1=d,
            y0=0, y1=1,
            xref="x",
            yref="paper",
            line=dict(color=color, width=1, dash="dot"),
            opacity=opacity,
            layer="below",
        )
        # label inside the plot at top, to avoid clipping by chart margin
        fig.add_annotation(
            x=d,
            y=0.98,
            xref="x",
            yref="paper",
            text=ev["label"],
            showarrow=False,
            yanchor="top",
            xanchor="left",
            font=dict(size=9, color=color),
            opacity=label_opacity,
            textangle=-90,
        )
    return fig
