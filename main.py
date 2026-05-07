"""Multipage entrypoint with custom Chinese navigation labels.

Using st.navigation() so sidebar shows clean Chinese titles regardless of
underlying filenames. Each page module sets its own st.set_page_config().
"""
import streamlit as st

home = st.Page("home.py", title="首頁", default=True, url_path="home")
finance = st.Page("pages/1_財_財務管理.py", title="財  財務管理", url_path="finance")
marketing = st.Page("pages/2_銷_行銷管理.py", title="銷  行銷管理", url_path="marketing")
production = st.Page("pages/3_產_生產管理.py", title="產  生產管理", url_path="production")
rd = st.Page("pages/4_發_研發管理.py", title="發  研發管理", url_path="rd")
hr = st.Page("pages/5_人_人力資源.py", title="人  人力資源", url_path="hr")
stock = st.Page("pages/6_股價反應.py", title="股價反應", url_path="stock-reaction")
nlp = st.Page("pages/7_文本分析.py", title="文本分析", url_path="text-analysis")
geo = st.Page("pages/8_地緣政治.py", title="地緣政治", url_path="geopolitics")
search = st.Page("pages/9_詞彙搜尋.py", title="詞彙搜尋", url_path="search")

pg = st.navigation(
    {
        "首頁": [home],
        "五管框架": [finance, marketing, production, rd, hr],
        "延伸分析": [stock, nlp, geo],
        "互動工具": [search],
    }
)
pg.run()
