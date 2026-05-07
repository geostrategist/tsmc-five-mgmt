"""TSMC 法說會 × 五管框架展示首頁。"""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from lib.data import CHART_HEIGHT, fmt_delta, latest_two, load_quarterly
from lib.style import apply_branding, render_footer

st.set_page_config(
    page_title="台積電法說會 × 五管框架",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

df = load_quarterly()
latest, prev = latest_two(df)

apply_branding(
    page_subtitle=f"解讀 2020 Q1 – {latest['quarter_label']} 共 {len(df)} 場法說會逐字稿"
)

st.markdown(
    """
台積電每季的法說會是研究**國際企業管理**的活教材。CFO 在開場 15 分鐘按固定模板報告：
**營收結構（產品與製程組合）、毛利率、CapEx、稅率變動**；CEO 接著談**技術藍圖、海外擴廠、產能與客戶策略**。

這份展示把 25 季逐字稿拆解成「五管」視角：

| 管 | 法說會中可見的訊號 |
|---|---|
| **產** 生產管理 | 各製程節點 wafer 營收占比、海外擴廠、產能利用率 |
| **銷** 行銷管理 | 平台別營收（HPC / Smartphone / Auto / IoT / DCE） |
| **人** 人力資源 | 員工 / 人才 / 訓練 / 文化在文本中的提及頻次 |
| **發** 研發管理 | 製程藍圖（N7 → N5 → N3 → N2 → A14）提及、CapEx |
| **財** 財務管理 | 毛利率、營業利益率、EPS、ROE、稅率、股利 |

從左側選單進入各管的詳細分析。下方先看四個總覽指標。
"""
)

st.subheader("最新一季關鍵指標")

c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "營收 (USD bn)",
    f"{latest['revenue_usd_b']:.1f}" if latest["revenue_usd_b"] else "—",
    delta=fmt_delta(latest["revenue_usd_b"], prev["revenue_usd_b"]),
)
c2.metric(
    "毛利率",
    f"{latest['gross_margin']:.1f}%",
    delta=fmt_delta(latest["gross_margin"], prev["gross_margin"], pct=True),
)
c3.metric(
    "EPS (TWD)",
    f"{latest['eps_twd']:.2f}" if latest["eps_twd"] else "—",
    delta=fmt_delta(latest["eps_twd"], prev["eps_twd"], digits=2),
)
c4.metric(
    "ROE",
    f"{latest['roe']:.1f}%",
    delta=fmt_delta(latest["roe"], prev["roe"], pct=True),
)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("營收與毛利率走勢")
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df["quarter_label"],
            y=df["revenue_usd_b"],
            name="季營收 (USD bn)",
            marker_color="#1f77b4",
            opacity=0.7,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["quarter_label"],
            y=df["gross_margin"],
            name="毛利率 %",
            mode="lines+markers",
            line=dict(color="#d62728", width=3),
            yaxis="y2",
        )
    )
    fig.update_layout(
        height=CHART_HEIGHT,
        yaxis=dict(title="USD bn", side="left"),
        yaxis2=dict(title="毛利率 %", overlaying="y", side="right", range=[40, 70]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(l=10, r=10, t=10, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("AI / 5G 在法說會的話術強度")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["quarter_label"],
            y=df["mentions_ai"],
            name="AI 提及次數",
            mode="lines+markers",
            line=dict(color="#2ca02c", width=2),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["quarter_label"],
            y=df["mentions_5g"],
            name="5G 提及次數",
            mode="lines+markers",
            line=dict(color="#ff7f0e", width=2),
        )
    )
    fig.update_layout(
        height=CHART_HEIGHT,
        yaxis=dict(title="每場次提及次數"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(l=10, r=10, t=10, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)

render_footer()
