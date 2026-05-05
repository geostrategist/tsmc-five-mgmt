"""人：人力資源 — 以法說會中員工/人才/訓練/文化的提及頻次為代理指標。"""
from __future__ import annotations

import re

import plotly.graph_objects as go
import streamlit as st

from lib.data import CHART_HEIGHT, load_quarterly, load_transcript
from lib.style import apply_branding, render_footer

st.set_page_config(page_title="人 — 人力資源", layout="wide")

df = load_quarterly()
latest = df.iloc[-1]

apply_branding(page_subtitle="人 — 人力資源", accent_key="人")

st.markdown(
    """
> **核心目標：** 招募、培訓、留住人才，優化組織績效。
> **法說會訊號：** 員工 / 人才 / 訓練 / 安全 / 文化等關鍵字的提及頻次。
> **資料說明：** 法說會主要對投資人，對「人」的著墨遠少於「財／產／銷」。
> 本頁以**關鍵字提及頻次**作為 HR 議題在 CEO/CFO 注意力中的代理指標——並非完整人資數據。
> 真正的 HR 數字（員工人數、薪酬、流動率）需參閱 TSMC 永續報告書 / 年報。
"""
)

st.divider()

st.subheader("HR 相關關鍵字提及頻次")
fig = go.Figure()
hr_lines = [
    ("employee_mentions", "員工 employee", "#1f77b4"),
    ("talent_mentions", "人才 talent", "#ff7f0e"),
    ("training_mentions", "訓練 training", "#2ca02c"),
    ("safety_mentions", "安全 safety", "#d62728"),
    ("culture_mentions", "文化 culture", "#9467bd"),
    ("workforce_mentions", "勞動力 workforce", "#8c564b"),
]
for key, label, color in hr_lines:
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
**幾個提及頻次的轉折點：**

- **2020 Q1：員工提及暴增** — COVID-19 期間，CEO 大段討論員工健康與防疫措施。
- **2022 後：talent 提及上升** — 這對應海外擴廠（Arizona / 熊本）的人才招聘瓶頸。
- **safety 在 2020 Q1 大幅突起** — 這是疫情敘事的痕跡，不是常態。

換言之，**HR 在法說會中只有「危機時刻」會被詳細討論**——這本身就是有意義的觀察：
平常的人資管理是日常營運，不需要對投資人解釋。
"""
)

st.divider()

st.subheader("法說會原文：被提到「talent」的段落（最新一季）")

text = load_transcript(latest["quarter_key"])
if text:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    matched = [s.strip() for s in sentences if re.search(r"\btalent[s]?\b", s, re.IGNORECASE)]
    if matched:
        for s in matched[:8]:
            st.markdown(f"> {s}")
    else:
        st.info(f"{latest['quarter_label']} 的逐字稿中沒有 talent 提及。")
else:
    st.info("找不到逐字稿。")

st.divider()

st.subheader("管理意涵")
st.markdown(
    """
**1. 半導體業的「人才戰爭」是這 5 年的明顯主題。** 海外擴廠的最大瓶頸不是錢、不是設備，
而是**能夠操作這些設備的人**。Arizona 廠延期的官方理由就是「skilled worker shortage」。

**2. TSMC 的 HR 模型仰賴台灣本地工程師密度。** 台灣每年產出的半導體相關碩博士遠多於美國，
這是台積電在台量產仍是主力的真正原因——不只是稅務或政治，而是**人才供應鏈的根**。

**3. 企業文化的「無形資產」。** 法說會極少提到 culture / values，但 CEO C.C. Wei 個人風格
（直接、技術導向、不畫大餅）就是文化的具現。法說會的問答風格就是 TSMC 文化的縮影：
「demand is robust」「we don't pick-and-choose customers」這些 boilerplate 已經是品牌資產的一部分。

**4. 數位轉型對 HR 的影響在文本中極少被討論。** 這暗示 TSMC 的 HR 數位化（電子簽核、AI 招募）
還沒到對外溝通的層級，或被視為內部營運細節。
"""
)

render_footer()
