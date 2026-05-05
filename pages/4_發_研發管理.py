"""發：研發管理 — 製程藍圖、CapEx、技術節點時間軸。"""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from lib.data import CHART_HEIGHT, load_quarterly
from lib.style import apply_branding, render_footer

st.set_page_config(page_title="發 — 研發管理", layout="wide")

df = load_quarterly()

apply_branding(page_subtitle="發 — 研發管理", accent_key="發")

st.markdown(
    """
> **核心目標：** 技術創新與產品開發，保持競爭力。
> **法說會訊號：** 製程節點時程（risk production / volume production）、CapEx 規模、R&D 投入比、客戶 design wins。

「發」對台積電而言 = **製程節點的迭代速度**。每 2 年推出一個新世代（N7 → N5 → N3 → N2 → A14），
這就是它的研發節奏。法說會中對未來節點的提及頻率，是研發優先順序的最直接信號。
"""
)

st.divider()

st.subheader("製程節點在法說會中的提及次數（投入注意力的代理指標）")
fig = go.Figure()
node_lines = [
    ("mentions_n7", "N7", "#9467bd"),
    ("mentions_n5", "N5", "#1f77b4"),
    ("mentions_n3", "N3", "#2ca02c"),
    ("mentions_n2", "N2", "#ff7f0e"),
    ("mentions_a16", "A16", "#d62728"),
    ("mentions_a14", "A14", "#8c564b"),
]
for key, label, color in node_lines:
    fig.add_trace(
        go.Scatter(
            x=df["quarter_label"],
            y=df[key],
            name=label,
            mode="lines+markers",
            line=dict(color=color, width=2),
        )
    )
fig.update_layout(
    height=CHART_HEIGHT + 40,
    yaxis=dict(title="每場次提及次數"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    margin=dict(l=10, r=10, t=10, b=40),
    hovermode="x unified",
)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
**節點生命週期在「文本注意力」上的呈現：**

- **N3 在 2022–2024 高峰**（量產前後 18 個月為話題核心）
- **N2 在 2024 後接棒**，2025 高峰時被提及次數超越 N3
- **A14 在 2024 開始出現**——這是下個世代（2028 量產）已經在 communicate 給客戶
- **N7 雖已是 8 年前節點，但仍持續被提及**——因為它是車用、CIS、特殊製程的主力
"""
)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("年度 CapEx 預算範圍")
    annual_data = df[(df["capex_year_low_usd_b"].notna()) & (df["capex_year_high_usd_b"].notna())]
    fig = go.Figure()
    if not annual_data.empty:
        fig.add_trace(
            go.Scatter(
                x=annual_data["quarter_label"],
                y=annual_data["capex_year_high_usd_b"],
                name="預算上限",
                mode="lines+markers",
                line=dict(color="#1f77b4", width=2),
                fill=None,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=annual_data["quarter_label"],
                y=annual_data["capex_year_low_usd_b"],
                name="預算下限",
                mode="lines+markers",
                line=dict(color="#1f77b4", width=2),
                fill="tonexty",
                fillcolor="rgba(31, 119, 180, 0.18)",
            )
        )
    fig.update_layout(
        height=CHART_HEIGHT,
        yaxis=dict(title="USD bn"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(l=10, r=10, t=10, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("CapEx 是「對未來幾年需求」的下注。2025 → 2026 從 USD30B 級跳到 USD52-56B。")

with right:
    st.subheader("AI 與 5G 的話術轉換點")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["quarter_label"],
            y=df["mentions_ai"],
            name="AI 提及次數",
            mode="lines+markers",
            line=dict(color="#2ca02c", width=3),
            fill="tozeroy",
            fillcolor="rgba(44, 160, 44, 0.15)",
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
    st.caption("2023 Q1 起 AI 超越 5G — 這是「研發語言」上 megatrend 接班的時點。")

st.divider()

st.subheader("製程藍圖時間軸")
roadmap = [
    ("N7", 2018, "EUV 起步、第一個量產的 7nm 製程"),
    ("N5", 2020, "Apple A14 首發；HPC 大規模採用"),
    ("N3", 2022, "FinFET 最後一代；HPC/AI 需求爆發"),
    ("N2", 2025, "首度導入 GAA Nanosheet"),
    ("A16", 2026, "Super Power Rail 背面供電"),
    ("A14", 2028, "次世代 GAA、2nm 後續延伸"),
]
for node, year, desc in roadmap:
    cols = st.columns([1, 1, 6])
    cols[0].markdown(f"**{node}**")
    cols[1].markdown(f"`{year}` 量產")
    cols[2].markdown(desc)

st.divider()

st.subheader("管理意涵")
st.markdown(
    """
**1. 半導體業的研發節奏 = 摩爾定律的時間表。** 每 2 年一個新世代（N7→N5→N3→N2），
這是台積電與三星、Intel 的競賽核心。落後一個世代 = 失去一整波客戶。

**2. CapEx 與研發 = 同一件事的兩面。** 在晶圓代工，研發成果只有透過 fab 設備才能變成產品。
USD52-56B 的 2026 CapEx 中，70% 投入在先進製程（N3/N2/A16），這就是研發投資的具體形式。

**3. 客戶 design wins 是研發成功的最終驗收。** CEO 在法說會中提到 N2 已有「smartphone 與 HPC/AI」客戶，
意味著 Apple 與 NVIDIA 都已 commit。客戶 commit 早於量產 12-18 個月，
所以 design wins 是領先指標、營收只是落後驗證。

**4. 智慧財產權管理多在文本之外。** 法說會少談專利，但 TSMC 有近 8 萬件專利，
是維持代工障礙的另一條防線。這部分需要看年報附錄而非法說會。
"""
)

render_footer()
