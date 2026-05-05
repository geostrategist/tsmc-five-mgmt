"""產：生產管理 — 製程節點 wafer 營收占比、海外擴廠、先進製程比重。"""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from lib.data import CHART_HEIGHT, NODE_LABELS, load_quarterly
from lib.style import apply_branding, render_footer

st.set_page_config(page_title="產 — 生產管理", layout="wide")

df = load_quarterly()
latest = df.iloc[-1]

apply_branding(page_subtitle="產 — 生產管理", accent_key="產")

st.markdown(
    """
> **核心目標：** 高效率、低成本製造產品，同時保證品質。
> **法說會訊號：** 各製程節點 wafer 營收占比、先進製程比重、海外擴廠進度、產能利用率。

「產」對台積電的特殊意義：它的產品就是**製程**本身。每個節點（N7、N5、N3、N2…）
就是一條「產品線」，每季的營收 mix = 產能與良率分配的結果。
"""
)

st.divider()

st.subheader("各製程節點 wafer 營收占比 — 堆疊面積圖")
node_keys = ["node_2nm_pct", "node_3nm_pct", "node_5nm_pct", "node_7nm_pct", "node_16nm_pct"]
node_colors = {
    "node_2nm_pct": "#08306b",
    "node_3nm_pct": "#2171b5",
    "node_5nm_pct": "#6baed6",
    "node_7nm_pct": "#c6dbef",
    "node_16nm_pct": "#deebf7",
}
fig = go.Figure()
for key in node_keys:
    if key not in df.columns:
        continue
    fig.add_trace(
        go.Scatter(
            x=df["quarter_label"],
            y=df[key].fillna(0),
            name=NODE_LABELS.get(key, key),
            mode="lines",
            stackgroup="one",
            line=dict(width=0.5, color=node_colors[key]),
            fillcolor=node_colors[key],
        )
    )
fig.update_layout(
    height=CHART_HEIGHT + 60,
    yaxis=dict(title="占當季 wafer 營收 %", range=[0, 110]),
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    margin=dict(l=10, r=10, t=10, b=40),
    hovermode="x unified",
)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
**製程世代的「世代交替」清楚可見：**

- **2020 Q1：N7 是當家節點 (35%)**，N5 還沒量產
- **2022 Q4：N5 接班 (32%)、N7 退到 22%、N3 即將量產**
- **2026 Q1：N5 (36%) + N3 (25%) = 6 成營收**，N7 退到 13% 變成「成熟製程」

每個節點從 0% → 高峰 → 下滑大約 4–5 年。這個生命週期就是 TSMC「產」的時間骨架。
"""
)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("先進製程占比")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["quarter_label"],
            y=df["node_advanced_pct"],
            name="先進製程 (7nm 以下)",
            mode="lines+markers",
            line=dict(color="#08519c", width=3),
            fill="tozeroy",
            fillcolor="rgba(8, 81, 156, 0.15)",
        )
    )
    fig.update_layout(
        height=CHART_HEIGHT,
        yaxis=dict(title="占 wafer 營收 %", range=[40, 85]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(l=10, r=10, t=10, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("先進製程占比從 2020 Q2 的 54% 上升到 2026 Q1 的 74%，是技術領先程度的直接量化指標。")

with right:
    st.subheader("海外廠在文本中的提及次數")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["quarter_label"],
            y=df["mentions_arizona"],
            name="Arizona 美國",
            mode="lines+markers",
            line=dict(color="#d62728", width=2),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["quarter_label"],
            y=df["mentions_japan"],
            name="Japan 日本（熊本 JASM）",
            mode="lines+markers",
            line=dict(color="#ff7f0e", width=2),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["quarter_label"],
            y=df["mentions_germany"],
            name="Germany 德國（Dresden ESMC）",
            mode="lines+markers",
            line=dict(color="#2ca02c", width=2),
        )
    )
    fig.update_layout(
        height=CHART_HEIGHT,
        yaxis=dict(title="每場次提及次數"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(l=10, r=10, t=10, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("提及次數激增的時點 = 該地策略升級／新建宣布的時間。Arizona 在 2024 後幾乎每場都被討論。")

st.divider()

st.subheader("管理意涵")
st.markdown(
    """
**1. 「產能規劃」是供應鏈管理的最高層級。** TSMC 一座 fab 從動工到量產約 2–3 年，從決定建廠到回收約 7 年。
這意味著 **2026 的營收結構是 2019 的決定**。CEO 反覆強調「we plan our capacity based on long-term demand profile」
就是這個邏輯——他們無法用一兩個月的訂單變化來決策。

**2. 海外擴廠的本質是「政治風險分散」。** Arizona、熊本、Dresden 三廠的成本（毛利率稀釋 2-4%）
被 CFO 公開承認，但仍堅持推進——這是把「地緣政治不可控風險」轉換為「可預測的成本項目」。
法說會中海外廠的提及頻率，反映該地策略的當期重要性。

**3. 「成熟製程」不是被淘汰，而是策略性留存。** 2026 Q1 仍有 13% 的 N7 營收，而 N7 已是 8 年前的節點。
TSMC 對 mature node 的策略是「focus on specialized technologies and high yield」——
為車用、CIS、特殊製程留下產能，而不是純粹追求最大化 advanced nodes 占比。

**4. 良率（yield）是「品質保證」在代工業的具體形式。** 法說會反覆強調 N3、N2 的 ramp-up 都是
「good yield」，這個詞背後是龐大的工程投入。一旦良率落後 6 個月，客戶就會轉單。
"""
)

render_footer()
