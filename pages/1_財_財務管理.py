"""財：財務管理 — 毛利率、營業利益率、EPS、ROE、CapEx、稅率。"""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from lib.data import CHART_HEIGHT, fmt_delta, latest_two, load_quarterly, load_transcript
from lib.style import apply_branding, render_footer

st.set_page_config(page_title="財 — 財務管理", layout="wide")

df = load_quarterly()
latest, prev = latest_two(df)

apply_branding(page_subtitle="財 — 財務管理", accent_key="財")

st.markdown(
    """
> **核心目標：** 資本利潤最大化、風險管理。
> **法說會訊號：** 毛利率、營業利益率、EPS、ROE、稅率、CapEx、股利政策。
"""
)

c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "毛利率",
    f"{latest['gross_margin']:.1f}%",
    fmt_delta(latest["gross_margin"], prev["gross_margin"], pct=True),
)
c2.metric(
    "營業利益率",
    f"{latest['operating_margin']:.1f}%",
    fmt_delta(latest["operating_margin"], prev["operating_margin"], pct=True),
)
c3.metric(
    "EPS (TWD)",
    f"{latest['eps_twd']:.2f}" if latest["eps_twd"] else "—",
    fmt_delta(latest["eps_twd"], prev["eps_twd"], digits=2),
)
c4.metric(
    "ROE",
    f"{latest['roe']:.1f}%",
    fmt_delta(latest["roe"], prev["roe"], pct=True),
)

st.divider()

st.subheader("毛利率 vs 營業利益率")
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=df["quarter_label"],
        y=df["gross_margin"],
        name="毛利率 (Gross Margin)",
        mode="lines+markers",
        line=dict(color="#d62728", width=3),
    )
)
fig.add_trace(
    go.Scatter(
        x=df["quarter_label"],
        y=df["operating_margin"],
        name="營業利益率 (Operating Margin)",
        mode="lines+markers",
        line=dict(color="#1f77b4", width=3),
    )
)
fig.update_layout(
    height=CHART_HEIGHT,
    yaxis=dict(title="%", range=[35, 70]),
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    margin=dict(l=10, r=10, t=10, b=40),
)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
**幾個轉折點：**

- **2020 Q1：51.8%** — 疫情爆發初期，遠距辦公與 5G 推升 HPC/手機需求。
- **2022 Q3：60.4%** — 半導體大景氣高點，全產能利用率。
- **2023 Q2：54.1%** — 庫存修正、N3 量產初期 dilution，毛利率回落。
- **2024 Q4：59.0% → 2025 Q4：62.3%** — AI 需求接力，N3 攤提改善 + 漲價拉抬毛利。
"""
)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("EPS 與 ROE")
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df["quarter_label"],
            y=df["eps_twd"],
            name="EPS (TWD)",
            marker_color="#9467bd",
            opacity=0.75,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["quarter_label"],
            y=df["roe"],
            name="ROE %",
            mode="lines+markers",
            line=dict(color="#e377c2", width=3),
            yaxis="y2",
        )
    )
    fig.update_layout(
        height=CHART_HEIGHT,
        yaxis=dict(title="EPS (TWD)", side="left"),
        yaxis2=dict(title="ROE %", overlaying="y", side="right", range=[20, 50]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(l=10, r=10, t=10, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("CapEx：季度 vs 年度預算")
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df["quarter_label"],
            y=df["capex_quarter_usd_b"],
            name="當季 CapEx (USD bn)",
            marker_color="#ff7f0e",
            opacity=0.85,
        )
    )
    # Annual budget mid-point as line
    annual_mid = (df["capex_year_low_usd_b"] + df["capex_year_high_usd_b"]) / 2
    fig.add_trace(
        go.Scatter(
            x=df["quarter_label"],
            y=annual_mid,
            name="年度預算中位 (USD bn)",
            mode="lines+markers",
            line=dict(color="#7f7f7f", width=2, dash="dash"),
            yaxis="y2",
        )
    )
    fig.update_layout(
        height=CHART_HEIGHT,
        yaxis=dict(title="季 USD bn", side="left", range=[0, 14]),
        yaxis2=dict(title="年度 USD bn", overlaying="y", side="right", range=[0, 60]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(l=10, r=10, t=10, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("法說會原文摘錄（最新一季）")
with st.expander(f"{latest['quarter_label']} CFO 開場（前 1500 字）"):
    text = load_transcript(latest["quarter_key"])
    if text:
        # crop to CFO opening — start near "financial highlights"
        idx = text.find("financial highlights")
        snippet = text[idx : idx + 1500] if idx >= 0 else text[:1500]
        st.text(snippet)
    else:
        st.info("找不到逐字稿。")

st.markdown(
    """
### 管理意涵

**1. 毛利率是技術領先的價格證據。** 60% 毛利率在晶圓代工是壓倒性的數字（聯電、GlobalFoundries 約 30%），代表客戶願意為「能準時交付的尖端製程」付更高價。

**2. CapEx 與營收同步上升 = 對未來需求的承諾。** 2025 全年 CapEx 從 USD30B → USD41B，是對 AI 需求結構性、非短期波動的判斷。

**3. 毛利率短期 dilution 不等於商業模式破壞。** N3 ramp-up 讓 2023 毛利率回到 54%，但 18 個月後（2025 Q4）已超越前波高點。新節點初期成本被吸收後，價格與良率的結構性領先即重新顯現。
"""
)

render_footer()
