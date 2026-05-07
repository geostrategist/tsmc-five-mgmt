"""詞彙搜尋：對 25 場法說會逐字稿做全文檢索 — 跨季趨勢 + 原文佐證。"""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from lib.data import (
    CHART_HEIGHT,
    add_geo_event_vlines,
    highlight_term,
    search_term,
)
from lib.style import apply_branding, render_footer

st.set_page_config(page_title="詞彙搜尋", layout="wide")

apply_branding(page_subtitle="詞彙搜尋 — 任意字詞跨 25 場法說會的軌跡")

st.markdown(
    """
> **方法：** 對 25 份逐字稿（2020 Q1 – 2026 Q1）做全文檢索，先濾掉 LSEG／Refinitiv 版權聲明等樣板雜訊，
> 再回報該字詞在各場法說會的提及次數與原句。
> **怎麼用：** 用你自己的問題探索。「Apple 何時被點名最多？」「Arizona 在哪一季變成熱話題？」
> 「tariff 出現的脈絡是什麼？」
"""
)


# === Search controls ===
def _set_term(t: str) -> None:
    st.session_state["search_input"] = t


PRESETS = ["AI", "geopolitical", "Apple", "NVIDIA", "Arizona", "China",
           "CoWoS", "tariff", "Japan", "yield", "demand", "robust"]

st.markdown("**常見詞** — 點選快速代入：")
preset_cols = st.columns(len(PRESETS))
for col, p in zip(preset_cols, PRESETS):
    col.button(p, on_click=_set_term, args=(p,), use_container_width=True)

c1, c2, c3 = st.columns([6, 1, 1])
with c1:
    term = st.text_input(
        "輸入要查的字詞（區分大小寫請勾選；用「完整字」避免誤抓子字串）",
        value="AI",
        key="search_input",
        placeholder="AI / geopolitical / Apple / Arizona / CoWoS / tariff",
    )
with c2:
    whole_word = st.checkbox("完整字", value=True)
with c3:
    case_sensitive = st.checkbox("區分大小寫", value=False)

if not term or not term.strip():
    st.info("請輸入要查的字詞。")
    render_footer()
    st.stop()

df = search_term(term, whole_word=whole_word, case_sensitive=case_sensitive)

total = int(df["count"].sum())
covered = int((df["count"] > 0).sum())

m1, m2, m3 = st.columns(3)
m1.metric("總提及次數", f"{total:,}")
m2.metric("出現於幾季", f"{covered} / {len(df)}")
m3.metric("平均每季", f"{(total / max(len(df),1)):.1f}")

if total == 0:
    st.warning(f"「{term}」在 25 場法說會中沒有出現。試試其他字詞或關閉「完整字」。")
    render_footer()
    st.stop()


# === Time series ===
st.header(f"「{term}」每季提及次數")

fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=df["call_date"] if "call_date" in df.columns else df["quarter_label"],
        y=df["count"],
        marker_color="#8B0000",
        opacity=0.8,
        hovertemplate="%{x}<br>提及 %{y} 次<extra></extra>",
        customdata=df["quarter_label"],
    )
)
# x axis: prefer dates if we can derive them, else use labels
fig.update_xaxes(type="category" if "call_date" not in df.columns else "date")
fig.update_layout(
    height=CHART_HEIGHT,
    yaxis=dict(title="提及次數"),
    margin=dict(l=10, r=10, t=20, b=40),
    xaxis=dict(tickangle=-45),
)
# overlay geo events if x is dates
if "call_date" in df.columns:
    pass  # df doesn't have call_date in search_term return; skip
st.plotly_chart(fig, use_container_width=True)


# === Sentences ===
st.header(f"「{term}」出現的原句（按季別分組）")

st.caption(
    "句子已濾掉 LSEG／Refinitiv 版權聲明等模板雜訊；只保留 20–600 字的有意義原句。"
    "命中字以黃底反白標示。"
)

# Sort by quarter (newest first by default)
sort_newest_first = st.toggle("最新季別優先", value=True)
df_display = df[df["count"] > 0].copy()
df_display = df_display.sort_values(
    "quarter_idx", ascending=not sort_newest_first
)

for _, row in df_display.iterrows():
    sents = row["sentences"]
    if not sents:
        continue
    with st.expander(
        f"**{row['quarter_label']}** — {row['count']} 次提及，{len(sents)} 句命中",
        expanded=False,
    ):
        for s in sents:
            highlighted = highlight_term(s, term, case_sensitive=case_sensitive)
            st.markdown(f"<div style='margin:6px 0; line-height:1.7;'>{highlighted}</div>",
                        unsafe_allow_html=True)


# === Tips ===
st.header("用法提示")
st.markdown(
    """
**幾個有意思的查詢想法：**

| 查 | 觀察 |
|---|---|
| `AI` | 從 2023 起急速崛起，曲線替代 5G 成為主敘事 |
| `geopolitical` | 一年只出現幾次，但每次都是 CEO 在 prepared remarks 主動提起，意味是策略訊號 |
| `Apple` / `NVIDIA` | TSMC 從不點名客戶，但分析師會問——出現的脈絡幾乎都在 Q&A |
| `Arizona` | 2024 後爆增（量產接近）；對比 `Japan` 與 `Germany` 看海外擴廠注意力分配 |
| `tariff` | 2025 後大量出現，反映川普第二任期對台積電的政策衝擊 |
| `CoWoS` | 2023 後重要性上升——反映 AI 時代「先進封裝」的戰略地位 |
| `yield` | 高頻常駐詞，但每次量產新節點就會集中出現 |
"""
)

render_footer()
