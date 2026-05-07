"""股價反應：法說會事件研究 — CAR、跨市場分歧、最大反應季排行。"""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from lib.data import (
    CHART_HEIGHT,
    add_geo_event_vlines,
    load_cross_market,
    load_event_study,
)
from lib.style import apply_branding, render_footer

st.set_page_config(page_title="股價反應", layout="wide")

es = load_event_study()
cm = load_cross_market()

apply_branding(page_subtitle="股價反應 — 把「說了什麼」連到「市場怎麼回應」")

st.markdown(
    """
> **方法：** 對每場法說會做「事件研究」（event study）：
> 用 TSMC 與大盤的歷史關係（α、β）估算正常報酬，扣掉之後就是「異常報酬」。
> **CAR_-1_+5** = 法說會前 1 天到後 5 天的累積異常報酬，正值代表市場喜歡聽到的內容。
> **教學意涵：** 把「公開揭露」與「市場定價」放在同一張圖上，看資訊如何被消化。
"""
)

st.header("各場法說會的市場反應 (CAR -1 to +5)")
es_sorted = es.sort_values("event_date").copy()
colors = ["#2D5F4E" if v >= 0 else "#8B0000" for v in es_sorted["CAR_m1p5"]]
fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=es_sorted["event_date"],
        y=es_sorted["CAR_m1p5"] * 100,
        marker_color=colors,
        opacity=0.85,
        name="CAR -1 → +5 (%)",
        hovertemplate="%{x|%Y-%m-%d}<br>CAR: %{y:.2f}%<extra></extra>",
    )
)
fig.update_layout(
    height=CHART_HEIGHT + 60,
    yaxis=dict(title="累積異常報酬 (%)", zeroline=True, zerolinewidth=1, zerolinecolor="#999"),
    margin=dict(l=10, r=10, t=20, b=40),
    hovermode="x",
)
add_geo_event_vlines(fig, es_sorted["event_date"], opacity=0.22)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
**怎麼讀：**

- **柱子高 = 市場買單** TSMC 該季的訊息與展望。
- **柱子深綠** 通常出現在 AI 敘事接棒的關鍵季（2023 Q2、2024 Q1、2024 Q4）。
- **柱子深紅** 對應市場已經 priced in、實際數字略低於預期的季別。
- **背景虛線**為地緣政治事件——可看到 2022 Q3（Pelosi 訪台）、2025 Q2（Trump 關稅）等
  事件對股價反應的影響。
"""
)

st.header("最大反應排行")
top_pos = es_sorted.nlargest(5, "CAR_m1p5")[["quarter_label", "event_date", "CAR_m1p5"]]
top_neg = es_sorted.nsmallest(5, "CAR_m1p5")[["quarter_label", "event_date", "CAR_m1p5"]]

c1, c2 = st.columns(2)
with c1:
    st.markdown("**市場最買單的 5 場**")
    st.dataframe(
        top_pos.assign(**{"CAR (%)": (top_pos["CAR_m1p5"] * 100).round(2)})
        .drop(columns=["CAR_m1p5"])
        .rename(columns={"quarter_label": "季別", "event_date": "法說會日"}),
        hide_index=True,
        use_container_width=True,
    )
with c2:
    st.markdown("**市場最失望的 5 場**")
    st.dataframe(
        top_neg.assign(**{"CAR (%)": (top_neg["CAR_m1p5"] * 100).round(2)})
        .drop(columns=["CAR_m1p5"])
        .rename(columns={"quarter_label": "季別", "event_date": "法說會日"}),
        hide_index=True,
        use_container_width=True,
    )

st.header("跨市場分歧：TSM (NYSE) vs 2330 (TWSE)")
fig2 = go.Figure()
fig2.add_trace(
    go.Scatter(
        x=cm["call_date"],
        y=cm["TSM_CAR_m1p5"] * 100,
        name="TSM (NYSE)",
        mode="lines+markers",
        line=dict(color="#1F4E79", width=2.5),
    )
)
fig2.add_trace(
    go.Scatter(
        x=cm["call_date"],
        y=cm["TW_CAR_m1p5"] * 100,
        name="2330 (TWSE)",
        mode="lines+markers",
        line=dict(color="#8B0000", width=2.5),
    )
)
fig2.update_layout(
    height=CHART_HEIGHT,
    yaxis=dict(title="CAR -1 → +5 (%)", zeroline=True, zerolinewidth=1, zerolinecolor="#999"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    margin=dict(l=10, r=10, t=20, b=40),
    hovermode="x unified",
)
add_geo_event_vlines(fig2, cm["call_date"], opacity=0.18)
st.plotly_chart(fig2, use_container_width=True)

st.markdown(
    """
**為什麼兩個市場反應不同？**

- **投資人結構差異：** TSM (NYSE) 由大型機構（Vanguard、BlackRock、退休基金）主導；
  2330 (TWSE) 散戶比重高、外資進出快。
- **資訊管道差異：** 美股投資人主要靠英文逐字稿與外資分析師；台股投資人有 PTT、媒體、
  地緣政治直覺加成。
- **典型樣態：** 重大利多時，TSM 漲得比 2330 多（機構放大 momentum）；地緣政治事件中，
  2330 跌得比 TSM 多（散戶恐慌、外資抽資金）。

這是 **「同一家公司，兩種市場敘事」** 的活教材。
"""
)

st.header("管理意涵")
st.markdown(
    """
**1. 法說會是「定價事件」，不是公關活動。** 6 小時內市場給出折現後的判斷。
CFO 講話順序、用字、避而不答的問題，全部進入定價。

**2. Guidance 可信度是長期資產。** TSMC 多年下來「指引偏保守、實際略好」，
建立了「他們說會做到的，通常會超過」的市場預期。這個信譽降低了股價波動率，
也讓融資成本長期偏低。

**3. 跨市場 arbitrage 不是套利機會，是「資訊不對稱的可視化」。** 重大消息時兩市場
反應差距可能達 3-5 個百分點——投資銀行的 dual-listing arb 部門就是吃這口飯。
"""
)

render_footer()
