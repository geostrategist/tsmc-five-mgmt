"""Visual styling: editorial / academic-journal aesthetic.
Hero with large university name in serif, minimal ornament, single accent."""
from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

UNIVERSITY = "實踐大學"
DEPARTMENT = "國際企業管理學系"
DEPARTMENT_EN = "Department of International Business Management"
PROJECT_TITLE = "台積電法說會 × 五管框架"
PROJECT_SUBTITLE = "解讀 2020 Q1 – 2026 Q1 共 25 場法說會"

PRIMARY = "#8B0000"          # deep crimson — academic accent
INK = "#111111"
TEXT = "#2A2A2A"
MUTED = "#6B6B6B"
SOFT = "#9A9A9A"
RULE = "#E0E0E0"
SURFACE = "#FAFAF9"

# Per-management subtle accents (used for section markers, not full color blocks)
MGMT_COLORS = {
    "財": "#9C7A1A",   # restrained gold
    "銷": "#A0522D",   # sienna
    "產": "#1F4E79",   # navy
    "發": "#5B2C6F",   # deep purple
    "人": "#2D5F4E",   # forest
}

CHART_COLORWAY = [
    "#1F4E79", "#8B0000", "#2D5F4E", "#A0522D",
    "#5B2C6F", "#9C7A1A", "#5A6C7D", "#3B7A57",
]

GOOGLE_FONTS_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?'
    'family=Noto+Sans+TC:wght@300;400;500;700;900&'
    'family=Noto+Serif+TC:wght@500;700;900&'
    'family=Inter:wght@300;400;500;600;700&'
    'display=swap" rel="stylesheet">'
)

_TEMPLATE_REGISTERED = False


def _register_plotly_template() -> None:
    global _TEMPLATE_REGISTERED
    if _TEMPLATE_REGISTERED:
        return
    pio.templates["tsmc"] = go.layout.Template(
        layout=go.Layout(
            font=dict(
                family="'Inter', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif",
                size=13,
                color=TEXT,
            ),
            paper_bgcolor="white",
            plot_bgcolor="white",
            colorway=CHART_COLORWAY,
            xaxis=dict(
                gridcolor="#F0F0F0",
                linecolor=RULE,
                showline=True,
                ticks="outside",
                tickfont=dict(size=11, color=MUTED),
                title=dict(font=dict(size=12, color=MUTED)),
            ),
            yaxis=dict(
                gridcolor="#F0F0F0",
                linecolor=RULE,
                showline=False,
                zeroline=False,
                tickfont=dict(size=11, color=MUTED),
                title=dict(font=dict(size=12, color=MUTED)),
            ),
            legend=dict(
                bgcolor="rgba(255,255,255,0)",
                font=dict(size=12, color=TEXT),
                borderwidth=0,
            ),
            margin=dict(l=8, r=8, t=24, b=44),
            hoverlabel=dict(
                bgcolor="white",
                font=dict(family="'Inter', 'Noto Sans TC', sans-serif", size=12, color=INK),
                bordercolor=RULE,
            ),
        )
    )
    pio.templates.default = "plotly_white+tsmc"
    _TEMPLATE_REGISTERED = True


def _css(accent: str) -> str:
    return f"""
    {GOOGLE_FONTS_LINK}
    <style>
    /* === BASE TYPOGRAPHY === */
    html, body, [class*="css"] {{
        font-family: 'Inter', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif !important;
        color: {TEXT};
        font-feature-settings: "tnum", "ss01";
    }}
    .block-container {{
        padding-top: 2.5rem;
        padding-bottom: 5rem;
        max-width: 1100px;
    }}

    /* Default text */
    .stMarkdown, .stMarkdown p {{
        font-size: 15px;
        line-height: 1.75;
        color: {TEXT};
    }}
    .stMarkdown strong {{ color: {INK}; font-weight: 700; }}

    /* === HERO === */
    .hero {{
        padding: 8px 0 28px 0;
        margin-bottom: 36px;
        border-bottom: 1px solid {RULE};
    }}
    .hero .uni-tag {{
        font-family: 'Inter', 'Noto Sans TC', sans-serif;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.32em;
        text-transform: uppercase;
        color: {accent};
        margin-bottom: 14px;
    }}
    .hero .uni-name {{
        font-family: 'Noto Serif TC', 'Songti TC', serif;
        font-size: 56px;
        font-weight: 900;
        line-height: 1.0;
        letter-spacing: 0.06em;
        color: {INK};
        margin: 0 0 6px 0;
    }}
    .hero .dept-name {{
        font-family: 'Noto Serif TC', serif;
        font-size: 30px;
        font-weight: 700;
        line-height: 1.2;
        letter-spacing: 0.04em;
        color: {INK};
        margin: 0 0 10px 0;
    }}
    .hero .dept-en {{
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        font-weight: 500;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: {SOFT};
        margin: 0 0 28px 0;
    }}
    .hero .accent-rule {{
        width: 56px;
        height: 3px;
        background: {accent};
        margin: 0 0 22px 0;
    }}
    .hero .project-title {{
        font-family: 'Noto Serif TC', serif;
        font-size: 26px;
        font-weight: 700;
        color: {INK};
        margin: 0 0 6px 0;
        letter-spacing: 0.02em;
    }}
    .hero .project-sub {{
        font-family: 'Inter', 'Noto Sans TC', sans-serif;
        font-size: 14px;
        font-weight: 400;
        color: {MUTED};
        margin: 0;
        letter-spacing: 0.01em;
    }}

    /* === SECTION HEADINGS === */
    h1 {{ display: none; }}  /* Hide stray st.title — hero replaces it */
    h2, h3 {{
        font-family: 'Noto Serif TC', serif !important;
        color: {INK} !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        border: none !important;
        padding: 0 !important;
        margin-top: 44px !important;
        margin-bottom: 16px !important;
    }}
    h2 {{ font-size: 24px !important; }}
    h3 {{ font-size: 19px !important; }}

    /* Add small accent rule before h2/h3 */
    h2::before, h3::before {{
        content: "";
        display: block;
        width: 28px;
        height: 2px;
        background: {accent};
        margin-bottom: 12px;
    }}

    /* === BLOCKQUOTE — quietly emphasised callout === */
    blockquote {{
        border: none !important;
        border-left: 2px solid {accent} !important;
        background: transparent !important;
        padding: 4px 0 4px 18px !important;
        margin: 0 0 24px 0 !important;
        color: {TEXT} !important;
        font-size: 14px !important;
        line-height: 1.75 !important;
    }}
    blockquote p {{
        margin: 6px 0 !important;
        color: {TEXT} !important;
    }}
    blockquote strong {{ color: {INK}; }}

    /* === METRIC CARDS — minimal, top-rule only === */
    [data-testid="stMetric"] {{
        background: transparent;
        padding: 14px 4px 8px 4px;
        border-top: 2px solid {accent};
        border-radius: 0;
    }}
    [data-testid="stMetricLabel"] {{ margin-bottom: 6px; }}
    [data-testid="stMetricLabel"] p {{
        color: {MUTED};
        font-size: 11px !important;
        font-weight: 600 !important;
        letter-spacing: 0.18em !important;
        text-transform: uppercase !important;
    }}
    [data-testid="stMetricValue"] {{
        color: {INK} !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 30px !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
    }}
    [data-testid="stMetricDelta"] {{
        font-size: 12px !important;
        font-weight: 500 !important;
    }}

    /* === DIVIDER === */
    hr {{
        border: none !important;
        border-top: 1px solid {RULE} !important;
        margin: 36px 0 !important;
    }}

    /* === TABLES === */
    .stMarkdown table {{
        border-collapse: collapse;
        width: 100%;
        margin: 12px 0;
        font-size: 14px;
    }}
    .stMarkdown table th {{
        text-align: left;
        font-weight: 700;
        color: {INK};
        border-bottom: 2px solid {INK};
        padding: 10px 14px;
        background: {SURFACE};
    }}
    .stMarkdown table td {{
        padding: 10px 14px;
        border-bottom: 1px solid {RULE};
        color: {TEXT};
    }}

    /* === CAPTION === */
    .stCaption, [data-testid="stCaptionContainer"] {{
        color: {MUTED} !important;
        font-size: 12px !important;
        line-height: 1.6 !important;
        letter-spacing: 0.01em !important;
    }}

    /* === SIDEBAR === */
    [data-testid="stSidebar"] {{
        background: {SURFACE};
        border-right: 1px solid {RULE};
    }}
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] {{
        padding-top: 12px;
    }}
    [data-testid="stSidebarNav"] a {{
        font-family: 'Noto Sans TC', sans-serif !important;
        font-size: 14px !important;
        color: {TEXT} !important;
    }}
    [data-testid="stSidebarNav"] a[aria-current="page"] {{
        color: {INK} !important;
        font-weight: 700 !important;
    }}

    /* === EXPANDER === */
    [data-testid="stExpander"] {{
        border: 1px solid {RULE} !important;
        border-radius: 4px;
    }}

    /* === FOOTER === */
    .footer {{
        margin-top: 80px;
        padding: 24px 0 8px 0;
        border-top: 1px solid {RULE};
        color: {MUTED};
        font-size: 12px;
        line-height: 1.7;
        letter-spacing: 0.02em;
    }}
    .footer .school {{
        color: {INK};
        font-weight: 700;
        font-family: 'Noto Serif TC', serif;
        letter-spacing: 0.04em;
    }}
    .footer .sep {{
        color: {SOFT};
        margin: 0 8px;
    }}

    /* Hide only the Streamlit-default footer "Made with Streamlit" — keep the
       toolbar and hamburger menu so the user can collapse / reopen the sidebar
       and access settings. */
    footer {{ visibility: hidden; height: 0; }}

    /* === Sidebar collapse / expand buttons — strong contrast === */
    /* When sidebar is COLLAPSED: this is the "open sidebar" button (top-left). */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {{
        visibility: visible !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        opacity: 1 !important;
        background: {accent} !important;
        border: 2px solid white !important;
        border-radius: 8px !important;
        padding: 6px !important;
        margin: 12px 0 0 12px !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.22) !important;
        width: 44px !important;
        height: 44px !important;
        z-index: 999999 !important;
        position: fixed !important;
        top: 8px !important;
        left: 8px !important;
        transition: transform 0.15s ease, background 0.15s ease !important;
    }}
    [data-testid="stSidebarCollapsedControl"]:hover,
    [data-testid="collapsedControl"]:hover {{
        background: {INK} !important;
        transform: scale(1.06) !important;
    }}
    [data-testid="stSidebarCollapsedControl"] button,
    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="collapsedControl"] button,
    [data-testid="collapsedControl"] svg {{
        color: white !important;
        fill: white !important;
        stroke: white !important;
        width: 26px !important;
        height: 26px !important;
    }}

    /* When sidebar is OPEN: the "<<" close button — also prominent */
    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebar"] [data-testid="baseButton-headerNoPadding"] {{
        background: {accent} !important;
        border-radius: 6px !important;
        padding: 4px !important;
    }}
    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="stSidebar"] [data-testid="baseButton-headerNoPadding"] svg {{
        color: white !important;
        fill: white !important;
        stroke: white !important;
    }}
    </style>
    """


def apply_branding(page_subtitle: str | None = None, accent_key: str | None = None) -> None:
    """Render hero header. `accent_key` ∈ {財,銷,產,發,人}; defaults to crimson.
    Uses st.html() so the raw HTML/CSS isn't routed through the Markdown parser
    (which would otherwise treat 4-space-indented blocks as code)."""
    accent = MGMT_COLORS.get(accent_key, PRIMARY) if accent_key else PRIMARY
    _register_plotly_template()
    st.html(_css(accent))
    sub = page_subtitle or PROJECT_SUBTITLE
    st.html(
        f'<div class="hero">'
        f'<div class="uni-tag">Shih Chien University</div>'
        f'<div class="uni-name">{UNIVERSITY}</div>'
        f'<div class="dept-name">{DEPARTMENT}</div>'
        f'<div class="dept-en">{DEPARTMENT_EN}</div>'
        f'<div class="accent-rule"></div>'
        f'<div class="project-title">{PROJECT_TITLE}</div>'
        f'<div class="project-sub">{sub}</div>'
        f'</div>'
    )


def render_footer() -> None:
    st.html(
        f'<div class="footer">'
        f'<span class="school">{UNIVERSITY} {DEPARTMENT}</span>'
        f'<span class="sep">·</span>國際企業管理 教學展示'
        f'<span class="sep">·</span>2026'
        f'<br/>資料來源：台積電歷年法說會逐字稿（LSEG / Refinitiv StreetEvents）。'
        f'數值以 regex 萃取自 CFO 開場與 CEO 重點段落。'
        f'</div>'
    )
