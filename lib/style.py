"""Shared visual styling: CSS injection, Plotly template, branded header / footer."""
from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

UNIVERSITY = "實踐大學 國際企業管理學系"
PROJECT_TITLE = "台積電法說會 × 五管框架"
PROJECT_SUBTITLE = "解讀 2020 Q1 – 2026 Q1 共 25 場法說會"

PRIMARY = "#C8102E"        # TSMC red
DEEP_BLUE = "#1F4E79"
INK = "#1A1A1A"
MUTED = "#5A6C7D"
BG_SOFT = "#F5F5F7"
RULE = "#E5E5E8"

# 5-management palette (used per page accent)
MGMT_COLORS = {
    "財": "#C9A227",   # gold
    "銷": "#E76F51",   # marketing orange
    "產": "#1F4E79",   # industrial blue
    "發": "#6A1B9A",   # innovation purple
    "人": "#2A9D8F",   # teal
}

CHART_COLORWAY = [
    "#1F4E79", "#C8102E", "#2A9D8F", "#E76F51",
    "#6A1B9A", "#C9A227", "#5A6C7D", "#3B7A57",
]

_TEMPLATE_REGISTERED = False


def _register_plotly_template() -> None:
    global _TEMPLATE_REGISTERED
    if _TEMPLATE_REGISTERED:
        return
    pio.templates["tsmc"] = go.layout.Template(
        layout=go.Layout(
            font=dict(
                family="'Noto Sans TC', 'Microsoft JhengHei', 'PingFang TC', 'Source Han Sans TC', sans-serif",
                size=13,
                color=INK,
            ),
            paper_bgcolor="white",
            plot_bgcolor="white",
            colorway=CHART_COLORWAY,
            xaxis=dict(
                gridcolor=RULE,
                linecolor=MUTED,
                showline=True,
                ticks="outside",
                tickfont=dict(size=11, color=MUTED),
            ),
            yaxis=dict(
                gridcolor=RULE,
                linecolor=MUTED,
                showline=False,
                zeroline=False,
                tickfont=dict(size=11, color=MUTED),
            ),
            legend=dict(
                bgcolor="rgba(255,255,255,0)",
                font=dict(size=12, color=INK),
            ),
            margin=dict(l=10, r=10, t=20, b=40),
            hoverlabel=dict(
                bgcolor="white",
                font=dict(family="'Noto Sans TC', sans-serif", size=12, color=INK),
                bordercolor=RULE,
            ),
        )
    )
    pio.templates.default = "plotly_white+tsmc"
    _TEMPLATE_REGISTERED = True


def _css(accent: str) -> str:
    return f"""
    <style>
    /* Shrink top padding so brand band sits closer to top */
    .block-container {{ padding-top: 1.5rem; padding-bottom: 4rem; max-width: 1200px; }}

    /* Brand band */
    .tsmc-band {{
        background: linear-gradient(135deg, #0F2A45 0%, #1F4E79 100%);
        color: white;
        padding: 18px 28px 22px 28px;
        border-radius: 6px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }}
    .tsmc-band::before {{
        content: "";
        position: absolute;
        left: 0; top: 0; bottom: 0; width: 5px;
        background: {accent};
    }}
    .tsmc-band .tag {{
        font-size: 11px;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        opacity: 0.85;
        margin-bottom: 8px;
        font-weight: 500;
    }}
    .tsmc-band .title {{
        font-size: 26px;
        font-weight: 700;
        line-height: 1.25;
        margin: 0 0 4px 0;
        letter-spacing: 0.02em;
    }}
    .tsmc-band .sub {{
        font-size: 13px;
        opacity: 0.82;
        margin: 0;
    }}

    /* Page accent strip on h2 / h3 (st.header / st.subheader) */
    h2, h3 {{
        border-left: 4px solid {accent};
        padding-left: 12px !important;
        font-size: 20px !important;
        margin-top: 28px !important;
        margin-bottom: 12px !important;
        letter-spacing: 0.01em;
        color: {INK} !important;
    }}
    h3 {{ font-size: 18px !important; }}

    /* Metric card subtle styling */
    [data-testid="stMetric"] {{
        background: {BG_SOFT};
        padding: 14px 18px 14px 18px;
        border-radius: 6px;
        border-top: 3px solid {accent};
    }}
    [data-testid="stMetricLabel"] p {{
        color: {MUTED};
        font-size: 12px;
        font-weight: 500;
        letter-spacing: 0.05em;
    }}
    [data-testid="stMetricValue"] {{
        color: {INK};
        font-size: 28px !important;
    }}

    /* Blockquote — softer */
    blockquote {{
        border-left: 3px solid {accent} !important;
        background: {BG_SOFT};
        padding: 12px 16px !important;
        margin: 0 0 16px 0 !important;
        color: {INK};
        font-size: 14px;
    }}
    blockquote p {{ margin: 4px 0 !important; }}

    /* Divider — slightly darker */
    hr {{ border-color: {RULE} !important; margin: 28px 0 !important; }}

    /* Sidebar tighter */
    [data-testid="stSidebar"] {{
        background: {BG_SOFT};
    }}
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] {{ padding-top: 8px; }}

    /* Footer */
    .tsmc-footer {{
        margin-top: 64px;
        padding: 16px 0 8px 0;
        border-top: 1px solid {RULE};
        color: {MUTED};
        font-size: 12px;
        text-align: center;
        line-height: 1.6;
    }}
    .tsmc-footer .school {{ color: {INK}; font-weight: 500; }}
    </style>
    """


def apply_branding(page_subtitle: str | None = None, accent_key: str | None = None) -> None:
    """Inject CSS, register Plotly template, render branded header.
    `accent_key` is one of 財/銷/產/發/人 to color the page accent."""
    accent = MGMT_COLORS.get(accent_key, PRIMARY) if accent_key else PRIMARY
    _register_plotly_template()
    st.markdown(_css(accent), unsafe_allow_html=True)
    sub = page_subtitle or PROJECT_SUBTITLE
    st.markdown(
        f"""
        <div class="tsmc-band">
            <div class="tag">{UNIVERSITY}</div>
            <div class="title">{PROJECT_TITLE}</div>
            <div class="sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    st.markdown(
        f"""
        <div class="tsmc-footer">
            <span class="school">{UNIVERSITY}</span>　·　國際企業管理 教學展示
            <br/>資料來源：台積電歷年法說會逐字稿（LSEG / Refinitiv StreetEvents），數值以 regex 萃取自 CFO 開場與 CEO 重點段落。
        </div>
        """,
        unsafe_allow_html=True,
    )
