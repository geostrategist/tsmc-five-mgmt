# 台積電法說會 × 五管框架

實踐大學 國際企業管理學系 教學展示。

以「五管」（產／銷／人／發／財）視角解讀台積電 2020 Q1 – 2026 Q1 共 25 場法說會逐字稿。

## 線上展示

部署於 Streamlit Community Cloud（連結待補）。

## 本地執行

```bash
# 安裝 uv（若尚未安裝）
pip install uv

# 同步依賴並啟動
uv run streamlit run main.py
```

開啟 <http://localhost:8501>。

## 專案結構

```
streamlit_app/
├── main.py                    入口頁（總覽）
├── pages/                     五管子頁
│   ├── 1_財_財務管理.py
│   ├── 2_銷_行銷管理.py
│   ├── 3_產_生產管理.py
│   ├── 4_發_研發管理.py
│   └── 5_人_人力資源.py
├── lib/
│   ├── data.py                資料載入器
│   └── style.py               視覺樣式（CSS + Plotly template）
├── data/
│   ├── transcripts/           25 份法說會 markdown
│   ├── build_dataset.py       regex 萃取腳本
│   └── quarterly.csv          25 季 × 49 欄結構化資料
├── .streamlit/config.toml     主題設定
├── pyproject.toml             uv 依賴
└── requirements.txt           Streamlit Cloud pip 依賴
```

## 資料來源

台積電歷年法說會逐字稿（LSEG / Refinitiv StreetEvents）。
數值以 regex 萃取自 CFO 開場與 CEO 重點段落，覆蓋率：

| 欄位 | 覆蓋率 |
|---|---|
| 毛利率 / 營業利益率 / ROE | 100% |
| EPS / 平台占比 (HPC/Smartphone/...) | 96–100% |
| 季度 USD 營收 | 72%（部分 Q4 法說會只給 NT 數字） |
| N3 / N5 / N7 wafer 占比 | 44–92%（早年節點尚未量產） |

## 重新建構資料表

加入新季度 markdown 後，重跑：

```bash
uv run python data/build_dataset.py
```

## 五管 × 法說會訊號

| 管 | 法說會中可見的訊號 |
|---|---|
| 產 | 各製程節點 wafer 營收占比、海外擴廠、產能利用率 |
| 銷 | 平台別營收（HPC / Smartphone / Auto / IoT / DCE） |
| 人 | 員工 / 人才 / 訓練 / 文化在文本中的提及頻次 |
| 發 | 製程藍圖（N7 → N5 → N3 → N2 → A14）提及、CapEx |
| 財 | 毛利率、營業利益率、EPS、ROE、稅率、股利 |

## 授權

教學展示用途。法說會原文版權屬 LSEG / Refinitiv，本專案僅作為非營利教學素材轉錄與分析。
