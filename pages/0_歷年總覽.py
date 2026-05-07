"""歷年總覽：1994-2026 共 32 年的 TSMC 股價、EPS、現金流結構。"""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from lib.data import CHART_HEIGHT, load_annual_history
from lib.style import apply_branding, render_footer

st.set_page_config(page_title="歷年總覽 1994-2026", layout="wide")

df = load_annual_history()

apply_branding(page_subtitle="歷年總覽 — 32 年 (1994 – 2026) 的 TSMC")

st.markdown(
    """
> **資料尺度：** 從 1994 上市那年開始，32 年完整年度數據。把焦點從「2020 後的 AI 故事」
> 拉回到「TSMC 從股本 144 億到 2,593 億」的長期軌跡。
> **教學意涵：** 真正的長期競爭優勢不是一兩季的數字，而是**幾十年的累積**——
> 用這個視角看，每一波景氣循環只是長期斜率上的小波紋。
"""
)

# === Big number summary ===
df_full = df.dropna(subset=["price_close"]).copy()
df_eps = df.dropna(subset=["eps_twd"]).copy()
df_fcf = df.dropna(subset=["fcf_b"]).copy()

p_first = df_full[df_full["year"] == 1994]["price_close"].iloc[0]
p_last = df_full[df_full["year"] == 2025]["price_close"].iloc[0]
eps_first_year = df_eps["year"].iloc[0]
eps_first = df_eps["eps_twd"].iloc[0]
eps_last = df_eps[df_eps["year"] == 2025]["eps_twd"].iloc[0]
fcf_total = df_fcf["fcf_b"].sum()
fcf_2025 = df_fcf[df_fcf["year"] == 2025]["fcf_b"].iloc[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "股價成長倍數",
    f"{p_last / p_first:.1f}x",
    f"1994 NT${p_first:.0f} → 2025 NT${p_last:.0f}",
)
c2.metric(
    "EPS 成長倍數",
    f"{eps_last / eps_first:.1f}x",
    f"{eps_first_year:.0f} {eps_first:.2f} → 2025 {eps_last:.2f}",
)
c3.metric(
    "30 年累計自由現金流",
    f"NT$ {fcf_total / 10000:.1f} 兆",
    f"2025 單年 {fcf_2025 / 10000:.2f} 兆",
)
c4.metric(
    "2025 vs 1995 營業活動現金流",
    f"{df[df['year']==2025]['cf_operating_b'].iloc[0] / df[df['year']==1995]['cf_operating_b'].iloc[0]:.0f}x",
    f"177 億 → 2.27 兆",
)

# === Annotated turning points ===
TURNING_POINTS = [
    (2000, "dot-com 高點"),
    (2001, "dot-com 崩盤"),
    (2008, "金融海嘯"),
    (2018, "N7 量產"),
    (2020, "COVID + 5G + AI 啟動"),
    (2022, "半導體大景氣高點"),
    (2024, "AI 結構性需求接管"),
]

st.header("年末股價 (1994 – 2026)")

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=df["year"],
        y=df["price_close"],
        mode="lines+markers",
        line=dict(color="#8B0000", width=3),
        marker=dict(size=6),
        name="年末收盤 (NTD)",
        hovertemplate="%{x}<br>收盤: NT$%{y:.1f}<extra></extra>",
    )
)
# turning point annotations
for yr, label in TURNING_POINTS:
    if yr in df["year"].values:
        y_val = df[df["year"] == yr]["price_close"].iloc[0]
        if pd.notna(y_val):
            fig.add_annotation(
                x=yr, y=y_val,
                text=label,
                showarrow=True,
                arrowhead=2,
                arrowsize=0.7,
                arrowwidth=1,
                arrowcolor="#5A6C7D",
                ax=0, ay=-30,
                font=dict(size=10, color="#1F4E79"),
                bgcolor="rgba(255,255,255,0.85)",
                borderpad=2,
            )
fig.update_layout(
    height=CHART_HEIGHT + 60,
    yaxis=dict(title="NT$ / 股", type="log"),
    margin=dict(l=10, r=10, t=20, b=40),
    hovermode="x",
)
st.plotly_chart(fig, use_container_width=True)
st.caption(
    "y 軸為 **對數刻度**——因為 32 年股價成長 24 倍，線性軸會把早年壓扁到看不見。"
    "對數軸下，每一段相同距離 = 相同百分比變化，更能看出長期斜率。"
)

st.header("年度 EPS (1995 – 2025)")
df_eps_show = df.dropna(subset=["eps_twd"])
fig2 = go.Figure()
fig2.add_trace(
    go.Bar(
        x=df_eps_show["year"],
        y=df_eps_show["eps_twd"],
        marker_color="#1F4E79",
        opacity=0.85,
        hovertemplate="%{x}<br>EPS: NT$%{y:.2f}<extra></extra>",
    )
)
fig2.update_layout(
    height=CHART_HEIGHT,
    yaxis=dict(title="EPS (NT$)"),
    margin=dict(l=10, r=10, t=20, b=40),
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown(
    """
**讀法：**

- **1995 後上市初期 EPS 10.48**——這是「上市紅利」效應，初期股本小、本益比高
- **2001 下殺到 0.83**——dot-com 崩盤 + 全球半導體大衰退
- **2014 起站穩兩位數**——進入 16/14nm 領導期
- **2022 → 39.2 → 2023 回落 → 2025 衝到 66.26**——景氣修正完，AI 拉爆
"""
)

st.header("現金流結構 (1995 – 2025)")
df_cf = df.dropna(subset=["cf_operating_b"])
fig3 = go.Figure()
fig3.add_trace(
    go.Bar(
        x=df_cf["year"],
        y=df_cf["cf_operating_b"] / 10000,
        name="營業活動",
        marker_color="#2D5F4E",
        opacity=0.9,
    )
)
fig3.add_trace(
    go.Bar(
        x=df_cf["year"],
        y=df_cf["cf_investing_b"] / 10000,
        name="投資活動 (CapEx)",
        marker_color="#8B0000",
        opacity=0.9,
    )
)
fig3.add_trace(
    go.Bar(
        x=df_cf["year"],
        y=df_cf["cf_financing_b"] / 10000,
        name="籌資活動",
        marker_color="#9C7A1A",
        opacity=0.9,
    )
)
fig3.update_layout(
    height=CHART_HEIGHT + 40,
    barmode="relative",
    yaxis=dict(title="兆 NT$", zeroline=True, zerolinewidth=1.5, zerolinecolor="#999"),
    margin=dict(l=10, r=10, t=20, b=40),
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    hovermode="x unified",
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown(
    """
**長期觀察：**

- **營業活動現金流（綠）持續長大**——這是真正的「賺錢能力」軌跡：
  1995 年 177 億 → 2025 年 2.27 兆 = **128 倍**
- **投資活動（紅）長期負值且加速**——TSMC 是個「永遠在蓋廠」的公司，
  CapEx 永遠 > 公司一半的現金流。這就是晶圓代工的本質。
- **籌資活動（金）在 2002 後翻負**——意味公司開始發股利、買回庫藏股，
  從「需要資金」變成「分配資金」。這是企業生命週期的關鍵轉折。
"""
)

st.header("自由現金流 (1995 – 2025)")
df_fcf_show = df.dropna(subset=["fcf_b"]).copy()
df_fcf_show["fcf_trillion"] = df_fcf_show["fcf_b"] / 10000
fig4 = go.Figure()
colors = ["#2D5F4E" if v >= 0 else "#8B0000" for v in df_fcf_show["fcf_trillion"]]
fig4.add_trace(
    go.Bar(
        x=df_fcf_show["year"],
        y=df_fcf_show["fcf_trillion"],
        marker_color=colors,
        opacity=0.85,
        hovertemplate="%{x}<br>FCF: NT$%{y:.3f} 兆<extra></extra>",
    )
)
fig4.update_layout(
    height=CHART_HEIGHT,
    yaxis=dict(
        title="兆 NT$",
        zeroline=True,
        zerolinewidth=1.5,
        zerolinecolor="#999",
    ),
    margin=dict(l=10, r=10, t=20, b=40),
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown(
    """
**FCF 分水嶺：**

- **1997 – 2001：FCF 為負**。建廠、buy land、買 EUV 機台燒錢期。
  傳統 finance 教科書會說「risky」，但這是基礎建設期不可避免的代價。
- **2002 起 FCF 由負轉正且持續長大**。從那一年開始，TSMC 變成
  **「能自我資助成長」** 的公司，不再依賴外部融資。
- **2024 – 2025 跳升到 9,613 → 11,306 億**（接近 1.1 兆）。
  這就是 AI 客戶高毛利訂單的具體現金顯現。
"""
)

st.header("管理意涵")
st.markdown(
    """
**1. 「30 年的累積」是台積電的核心競爭優勢。**
從這張表你會看到，TSMC 不是某一年突然變強——而是**從 1995 到 2025 連續 30 年**
營業活動現金流幾乎沒有負成長年。這種「穩定壓倒戲劇性」的累積，
才是真正讓三星、Intel 追不上的原因。

**2. 投資活動長期負值 = 護城河本身。**
教科書 textbook 看到「永遠負現金流的投資活動」會擔心，但對 TSMC，
這是**「拒絕讓對手追上」的承諾**。每年蓋的廠就是下一個 5 年的訂單入場券。

**3. 觀察學生提問：**
- 1997-2001 FCF 為負時，如果你是分析師，會怎麼評價這家公司？
- 2002 FCF 轉正的關鍵發生了什麼？（提示：N0.18 微米製程、Sony PlayStation 訂單）
- 為什麼 2009 金融海嘯時，營業現金流還能維持？

**4. 把這頁與「股價反應」「文本分析」對照：**
短期股價反應有時很情緒化（2008、2022），但 30 年走勢看，
EPS 與現金流的長期斜率才是真正驅動股價的東西。
這就是 **「短期是投票機，長期是稱重機」** 的具體圖示。
"""
)

render_footer()
