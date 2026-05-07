"""文本分析：法說會的語言訊號 — 詞彙強度、主題權重、語言漂移。"""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from lib.data import (
    CHART_HEIGHT,
    add_geo_event_vlines,
    load_lda_topics,
    load_nlp_panel,
)
from lib.style import apply_branding, render_footer

st.set_page_config(page_title="文本分析", layout="wide")

df = load_nlp_panel()
topics = load_lda_topics()

apply_branding(page_subtitle="文本分析 — 法說會的語言訊號")

st.markdown(
    """
> **方法：** 把 25 場法說會逐字稿切成文本特徵——五組詞彙頻率（定價意圖、需求強度、
> 供給緊縮、避險語言、技術定位）、季度間語言漂移（TF-IDF 餘弦距離）、LDA 主題權重。
> **教學意涵：** 企業敘事是策略資產。CFO/CEO 用什麼字、何時換字，是公開市場上「不能說但能聽」的訊號。
"""
)

st.header("詞彙強度時序")
fig = go.Figure()
lex_lines = [
    ("pricing_intent_rate", "定價意圖 (pricing intent)", "#8B0000"),
    ("demand_strength_rate", "需求強度 (demand strength)", "#1F4E79"),
    ("supply_tightness_rate", "供給緊縮 (supply tightness)", "#9C7A1A"),
    ("hedging_language_rate", "避險語言 (hedging)", "#5A6C7D"),
    ("tech_positioning_rate", "技術定位 (tech positioning)", "#2D5F4E"),
]
for col, label, color in lex_lines:
    if col not in df.columns:
        continue
    fig.add_trace(
        go.Scatter(
            x=df["call_date"],
            y=df[col],
            name=label,
            mode="lines+markers",
            line=dict(color=color, width=2),
        )
    )
fig.update_layout(
    height=CHART_HEIGHT + 60,
    yaxis=dict(title="每千字提及率"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    margin=dict(l=10, r=10, t=20, b=40),
    hovermode="x unified",
)
add_geo_event_vlines(fig, df["call_date"], opacity=0.18)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
**怎麼讀：**

- **「需求強度」上升**通常領先當季營收幾個月——CEO 對需求的描述語言是領先指標。
- **「供給緊縮」高峰**是 2021–2022（缺晶片時代），這是賣方權力最強的時點。
- **「避險語言」（will, may, could）峰值** = 高度不確定的季別，常見於地緣政治事件後。
- **「技術定位」（leadership, ahead）長期高位** = TSMC 最自信的話術，也最少波動。
"""
)

st.header("法說會語言漂移")
df["language_change"] = (1 - df["tfidf_cosine_similarity"]).fillna(0)
fig2 = go.Figure()
fig2.add_trace(
    go.Bar(
        x=df["call_date"],
        y=df["language_change"],
        marker_color="#8B0000",
        opacity=0.75,
        name="與上季語言距離",
        hovertemplate="%{x|%Y Q%{customdata}}<br>距離: %{y:.3f}<extra></extra>",
        customdata=df["quarter"].str.replace("Q", ""),
    )
)
fig2.update_layout(
    height=CHART_HEIGHT,
    yaxis=dict(title="1 − TF-IDF 餘弦相似度"),
    margin=dict(l=10, r=10, t=20, b=40),
)
add_geo_event_vlines(fig2, df["call_date"], opacity=0.18)
st.plotly_chart(fig2, use_container_width=True)

st.caption(
    "高峰季 = CFO/CEO 的話題大幅換軌的時點。COVID 爆發、AI 接管、川普關稅威脅都會在這條曲線上留下痕跡。"
)

st.header("LDA 主題權重熱圖")
topic_cols = [c for c in df.columns if c.startswith("topic_") and c.endswith("_weight")]
if topic_cols:
    z = df[topic_cols].T.values
    fig3 = go.Figure(
        data=go.Heatmap(
            z=z,
            x=df["quarter_label"],
            y=[f"主題 {c.split('_')[1]}" for c in topic_cols],
            colorscale="Reds",
            colorbar=dict(title="權重", thickness=12, len=0.7),
            hovertemplate="%{x}<br>%{y}<br>權重: %{z:.3f}<extra></extra>",
        )
    )
    fig3.update_layout(
        height=CHART_HEIGHT,
        margin=dict(l=10, r=10, t=20, b=40),
        xaxis=dict(tickangle=-45),
    )
    st.plotly_chart(fig3, use_container_width=True)

with st.expander("各主題的關鍵字（LDA 結果）"):
    st.dataframe(topics, use_container_width=True, hide_index=True)

st.header("管理意涵")
st.markdown(
    """
**1. 「敘事優勢」是無形護城河。** TSMC 的法說會語言極度自信、boilerplate 重複度極高
（語言距離曲線常態低）。這種「冷靜可預測」本身就是品牌資產——
讓投資人相信「公司在掌控之中」，反向降低融資成本。

**2. 詞彙突變 = 市場結構轉折。** 2020 Q1 與 2023 Q1 都是顯著的語言距離高峰，
分別對應 COVID 衝擊與 AI 敘事接管。**敘事換軌領先財務指標**——
聽法說會的人比看財報的人早三個月知道下一季發生什麼。

**3. 對學生的方法論：** 公司公告、年報、法說會都可以這樣拆解。
詞頻、TF-IDF、LDA 是基本工具——加上時間軸與股價，就能做策略傳播研究。
"""
)

render_footer()
