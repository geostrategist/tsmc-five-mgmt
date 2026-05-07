"""地緣政治：把 2020-2026 影響台積電的關鍵事件放在時間軸上。"""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from lib.data import (
    CHART_HEIGHT,
    add_geo_event_vlines,
    geo_events_df,
    load_event_study,
    load_quarterly,
)
from lib.style import apply_branding, render_footer

st.set_page_config(page_title="地緣政治", layout="wide")

ev = geo_events_df()
qtr = load_quarterly()
es = load_event_study()

apply_branding(page_subtitle="地緣政治 — 國際企業環境如何形塑台積電")

st.markdown(
    """
> **問題：** 過去六年的台積電不是純商業故事。從 COVID、華為禁令、晶片戰爭到
> Trump 2.0 關稅威脅，每一個重大轉折都不是 CEO 能完全控制的——這就是國際企業管理的核心命題：
> **「公司處在政治、經濟、技術交織的環境中，必須同時做戰略與避險」**。
> **方法：** 手工策展 14 個關鍵事件，疊加在毛利率、CAR、營收結構之上。
"""
)

st.header("關鍵事件年表 (2020 – 2026)")

cat_label = {
    "pandemic": "疫情",
    "us_china": "美中",
    "geopolitics": "地緣政治",
    "industry_policy": "產業政策",
    "competitor": "競爭對手",
}
cat_color = {
    "pandemic": "#888888",
    "us_china": "#8B0000",
    "geopolitics": "#5B2C6F",
    "industry_policy": "#1F4E79",
    "competitor": "#9C7A1A",
}

display_df = ev.copy()
display_df["類別"] = display_df["cat"].map(cat_label)
display_df["日期"] = display_df["date"].dt.strftime("%Y-%m-%d")
display_df = display_df[["日期", "類別", "label", "detail"]].rename(
    columns={"label": "事件", "detail": "影響"}
)
st.dataframe(display_df, use_container_width=True, hide_index=True, height=520)

st.header("事件 × 毛利率時序")
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=qtr["call_date"],
        y=qtr["gross_margin"],
        name="毛利率 %",
        mode="lines+markers",
        line=dict(color="#8B0000", width=3),
    )
)
fig.update_layout(
    height=CHART_HEIGHT + 80,
    yaxis=dict(title="毛利率 %", range=[45, 70]),
    margin=dict(l=10, r=10, t=20, b=40),
    hovermode="x unified",
)
add_geo_event_vlines(fig, qtr["call_date"], opacity=0.32)
st.plotly_chart(fig, use_container_width=True)

st.markdown(
    """
**讀法：**

- **2020 Q1-Q3 毛利率反而衝高** → COVID 推升 work-from-home 與 5G 手機需求，HPC 客戶搶產能。
- **2022 Q3-Q4 毛利率高峰** → 缺晶片時代尾聲、定價權最強。
- **2023 全年回落** → 半導體景氣下行 + N3 ramp-up dilution，但同時是 AI 敘事接棒的開始。
- **2024 Q3 起重新爬升** → AI 結構性需求接力。10/7 出口管制（影響中國客戶）反而沒有重創 TSMC，
  因為大部分先進製程都流向美國 hyperscalers。
"""
)

st.header("事件 × 股價反應 (CAR -1 to +5)")
es_sorted = es.sort_values("event_date")
colors = ["#2D5F4E" if v >= 0 else "#8B0000" for v in es_sorted["CAR_m1p5"]]
fig2 = go.Figure()
fig2.add_trace(
    go.Bar(
        x=es_sorted["event_date"],
        y=es_sorted["CAR_m1p5"] * 100,
        marker_color=colors,
        opacity=0.75,
        hovertemplate="%{x|%Y-%m-%d}<br>CAR: %{y:.2f}%<extra></extra>",
    )
)
fig2.update_layout(
    height=CHART_HEIGHT,
    yaxis=dict(title="累積異常報酬 (%)"),
    margin=dict(l=10, r=10, t=20, b=40),
    showlegend=False,
)
add_geo_event_vlines(fig2, es_sorted["event_date"], opacity=0.32)
st.plotly_chart(fig2, use_container_width=True)

st.header("分類圖例")
cols = st.columns(len(cat_label))
for col, (k, v) in zip(cols, cat_label.items()):
    color = cat_color[k]
    col.markdown(
        f'<div style="border-left:3px solid {color}; padding:6px 10px; '
        f'background:#FAFAF9; font-size:13px;">{v}</div>',
        unsafe_allow_html=True,
    )

st.header("管理意涵")
st.markdown(
    """
**1. 「政治風險」是台積電不能裝沒看到的成本項。** Arizona、熊本、Dresden 三個海外廠的存在，
本質就是「把不可控政治風險，買成可預測的毛利率稀釋」。法說會中 CFO 公開承認「初期 2-3%、
後期 3-4% 毛利率 dilution」——這就是政治保險的明碼。

**2. 「中美博弈」對 TSMC 的雙向擠壓。** 美國要求對中國斷供（2020 華為禁令、2022 全面管制），
中國視 TSMC 為戰略資產（Pelosi 訪台後軍演升溫）。CEO 在每場法說會的開場與 Q&A 中，
怎麼**「不選邊但同時對兩邊都安全」** 的措辭策略，本身就是國際商業外交的範例。

**3. 「敘事轉換」是政治風險的對沖工具。** 2024 後 CEO 強調「AI 是長期結構性需求」、
「demand from cloud service providers is robust」——這不僅是商業判斷，
也是把投資人從「擔心關稅」拉回「相信 AI 故事」的話術操作。

**4. 對學生的提問：** 如果你是 TSMC CEO，2025 Q1 後 Trump 點名要求 50% 美國產能，
你會：(a) 加碼海外、(b) 拖延、(c) 公開抗議、(d) 找其他國家對沖？每個選項對應的成本、
風險、時間軸是什麼？這就是國際企業策略的真實題目。
"""
)

render_footer()
