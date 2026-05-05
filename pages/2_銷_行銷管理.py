"""銷：行銷管理 — 平台別營收 (HPC / Smartphone / Auto / IoT / DCE)。"""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from lib.data import (
    CHART_HEIGHT,
    PLATFORM_LABELS,
    fmt_delta,
    latest_two,
    load_quarterly,
)
from lib.style import apply_branding, render_footer

st.set_page_config(page_title="銷 — 行銷管理", layout="wide")

df = load_quarterly()
latest, prev = latest_two(df)

apply_branding(page_subtitle="銷 — 行銷管理", accent_key="銷")

st.markdown(
    """
> **核心目標：** 市場佔有率最大化、提升企業利潤。
> **法說會訊號：** 平台別營收占比、客戶結構、地區別營收、價格策略。

台積電不直接面對消費者，而是把產能切成 **5 大平台** 賣給客戶。
平台組合的變動，就是它「客戶 mix」最直接的指標。
"""
)

c1, c2, c3, c4, c5 = st.columns(5)
metrics_cols = [c1, c2, c3, c4, c5]
for col, (key, label) in zip(metrics_cols, PLATFORM_LABELS.items()):
    val = latest.get(key)
    pv = prev.get(key)
    col.metric(
        label.split()[0],
        f"{val:.0f}%" if val is not None and not (val != val) else "—",
        fmt_delta(val, pv, pct=True, digits=0) if val is not None and pv is not None else None,
    )

st.divider()

st.subheader("平台別營收占比 — 堆疊面積圖")
fig = go.Figure()
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
for (key, label), color in zip(PLATFORM_LABELS.items(), colors):
    fig.add_trace(
        go.Scatter(
            x=df["quarter_label"],
            y=df[key],
            name=label,
            mode="lines",
            stackgroup="one",
            line=dict(width=0.5, color=color),
            fillcolor=color,
            opacity=0.85,
        )
    )
fig.update_layout(
    height=CHART_HEIGHT + 60,
    yaxis=dict(title="占當季營收 %", range=[0, 105]),
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    margin=dict(l=10, r=10, t=10, b=40),
    hovermode="x unified",
)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
**圖中的兩個結構性翻轉：**

- **2020 Q1 → 2024 Q4：HPC 從 30% → 53%、Smartphone 從 49% → 35%。**
  這是 5G 紅利消退、AI/HPC 接管的清楚證據——客戶從「Apple/Qualcomm 為主」轉向
  「NVIDIA / AMD / Broadcom 為主」。

- **2024 Q4：HPC 首度超過五成。** 這意味著 TSMC 已經是一家**以資料中心為主要客戶**的公司，
  不再只是「為手機做晶片」的代工廠。客戶集中風險的性質也跟著改變
  （從消費景氣循環風險，轉為大型雲廠 CapEx 循環風險）。
"""
)

st.divider()

st.subheader("HPC vs Smartphone：典型的代工廠 mix 翻轉")
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=df["quarter_label"],
        y=df["plat_hpc_pct"],
        name="HPC",
        mode="lines+markers",
        line=dict(color="#1f77b4", width=3),
    )
)
fig.add_trace(
    go.Scatter(
        x=df["quarter_label"],
        y=df["plat_smartphone_pct"],
        name="Smartphone",
        mode="lines+markers",
        line=dict(color="#ff7f0e", width=3),
    )
)
fig.update_layout(
    height=CHART_HEIGHT,
    yaxis=dict(title="占當季營收 %", range=[20, 65]),
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    margin=dict(l=10, r=10, t=10, b=40),
    annotations=[
        dict(
            x="2024 Q3",
            y=51,
            text="HPC 首度超越 Smartphone<br>(2024 Q3)",
            showarrow=True,
            arrowhead=2,
            ax=-60,
            ay=-40,
        ),
    ],
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("為什麼這對教學重要？")
st.markdown(
    """
1. **「行銷組合 4P」在 B2B 半導體的具體模樣：**
   - **產品 (Product)** = 製程節點 + 設計服務 + 封裝（CoWoS）
   - **價格 (Price)** = 由節點稀缺度與良率決定，TSMC 對 N3 / N5 採「value selling」
   - **通路 (Place)** = 海外擴廠（Arizona、熊本、Dresden）= 為客戶布建在地化供應
   - **推廣 (Promotion)** = 法說會 + 北美技術論壇 + 與 Apple/NVIDIA 的 design partnership

2. **客戶集中度是 B2B 行銷的核心議題。** 法說會中 CEO 一句「我們不挑客戶」
   （we do not pick-and-choose or play favorites）反映的是供需失衡時的產能分配權力。

3. **平台 mix 改變 = 全公司戰略重新定向。** 從手機代工廠變成 AI 代工廠，產能規劃、
   研發投入優先順序、海外布局選址（Arizona 為了 AI 客戶就近），全部都跟著重排。
"""
)

render_footer()
