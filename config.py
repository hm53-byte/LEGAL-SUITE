# -----------------------------------------------------------------------------
# KONFIGURACIJA: CSS stilovi, konstante i UI teme
# Stil: Trust-Centric Swiss Minimalism + Aurora Dark sidebar
# Paleta: Navy autoritet + zlatni naglasci + neutralne sive (OKLCH-informed)
# Tipografija: Inter Variable Font, font-feature-settings, weight 425 body
# Pristupacnost: WCAG 2.2 AA (focus-visible, reduced-motion, scroll-padding,
#                target-size 24px, SC 2.4.11/2.5.8/3.3.8 compliance)
# Shadow System: Hierarchical (nav > card > button) + colored accent shadows
# Anti-Slop: Variable border-radius, atmospheric sidebar, tabular numbers
# -----------------------------------------------------------------------------

PAGE_TITLE = "LegalTech Suite Pro"
PAGE_ICON = "\u2696\ufe0f"
PAGE_LAYOUT = "wide"

# ============================================================================
# DESIGN TOKENI (HEX fallback — OKLCH-informed values)
# ============================================================================
# Background / Surface
_BG = "#FAFBFC"            # oklch(0.985 0.003 248) — not pure white
_SURFACE = "#F8FAFC"       # oklch(0.980 0.005 248)
_CARD = "#FFFFFF"
_SUNKEN = "#F1F5F9"        # oklch(0.960 0.008 248)

# Brand Navy (hue ~260)
_BRAND = "#1E3A5F"         # oklch(0.340 0.060 255)
_BRAND_LIGHT = "#2D4A6F"   # oklch(0.390 0.060 255)
_BRAND_SURFACE = "#EFF3F8" # oklch(0.960 0.012 250)

# Accent Gold
_ACCENT = "#B8860B"
_ACCENT_LIGHT = "#D4A843"

# Text
_TEXT = "#0F172A"           # oklch(0.200 0.030 260)
_TEXT_SEC = "#475569"       # oklch(0.420 0.030 255)
_TEXT_MUTED = "#94A3B8"     # oklch(0.600 0.025 250)

# Borders
_BORDER = "#E2E8F0"        # oklch(0.900 0.010 250)
_BORDER_STRONG = "#CBD5E1"  # oklch(0.850 0.015 250)

# Semantic
_SUCCESS = "#059669"
_SUCCESS_DARK = "#047857"
_WARNING = "#D97706"
_DANGER = "#DC2626"

# Sidebar
_SIDEBAR_BG = "#0F1B2D"    # oklch(0.160 0.030 255)
_SIDEBAR_DEEP = "#081220"  # oklch(0.120 0.025 255)
_SIDEBAR_TEXT = "#CBD5E1"

# ============================================================================
# CSS STILOVI — Premium Redesign
# ============================================================================
CSS_STILOVI = f"""
<link rel="stylesheet" href="https://rsms.me/inter/inter.css">
<style>
    /* ================================================================
       INTER VARIABLE FONT — Full OpenType Features
       (loaded via non-blocking <link> above, NOT @import)
       ================================================================ */
    html, body, [class*="css"], [class*="st-"],
    .stApp, .main, div, span, p, label, input, textarea, select, button {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        font-feature-settings: 'liga' 1, 'calt' 1;
        font-optical-sizing: auto;
    }}

    /* Body text weight 425 — premium variable font technique */
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li,
    .stMarkdown p {{
        font-weight: 425;
        letter-spacing: -0.011em;
        line-height: 1.6;
    }}

    /* ================================================================
       LAYOUT
       ================================================================ */
    .main .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }}

    /* Scroll padding for sticky header — WCAG 2.2 SC 2.4.11 */
    section.main {{
        scroll-padding-top: 3.5rem;
    }}

    /* ================================================================
       SIDEBAR — Aurora Dark Atmosphere
       ================================================================ */
    [data-testid="stSidebar"] {{
        background: {_SIDEBAR_BG};
        background-image:
            radial-gradient(ellipse at 20% 85%, rgba(30, 58, 95, 0.5) 0%, transparent 55%),
            radial-gradient(ellipse at 75% 15%, rgba(45, 74, 111, 0.35) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, rgba(15, 27, 45, 0.6) 0%, transparent 70%);
        border-right: 1px solid rgba(30, 58, 95, 0.25);
    }}
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
        color: {_SIDEBAR_TEXT} !important;
    }}
    [data-testid="stSidebar"] h1 {{
        color: {_ACCENT_LIGHT} !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
    }}

    /* Sidebar gumbi — navigacija (min target 24x24 — SC 2.5.8) */
    [data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"],
    [data-testid="stSidebar"] .stButton button[kind="secondary"],
    [data-testid="stSidebar"] .stButton > button:not([kind="primary"]) {{
        background-color: transparent !important;
        background: transparent !important;
        border: 1px solid rgba(203, 213, 225, 0.1) !important;
        color: {_SIDEBAR_TEXT} !important;
        font-size: 0.82rem !important;
        font-weight: 425 !important;
        padding: 0.5rem 0.7rem !important;
        min-height: 2rem !important;
        border-radius: 6px !important;
        transition: all 0.15s ease !important;
        text-align: left !important;
    }}
    [data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"]:hover,
    [data-testid="stSidebar"] .stButton button[kind="secondary"]:hover,
    [data-testid="stSidebar"] .stButton > button:not([kind="primary"]):hover {{
        background-color: rgba(255, 255, 255, 0.08) !important;
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(203, 213, 225, 0.25) !important;
        color: #FFFFFF !important;
    }}
    [data-testid="stSidebar"] button[data-testid="stBaseButton-primary"],
    [data-testid="stSidebar"] .stButton button[kind="primary"] {{
        background: linear-gradient(135deg, {_BRAND} 0%, {_BRAND_LIGHT} 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        padding: 0.5rem 0.7rem !important;
        min-height: 2rem !important;
        border-radius: 6px !important;
        text-align: left !important;
        box-shadow: 0 2px 8px rgba(30, 58, 95, 0.3) !important;
    }}
    [data-testid="stSidebar"] button {{
        color: {_SIDEBAR_TEXT} !important;
    }}
    [data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] p,
    [data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] span {{
        color: #FFFFFF !important;
    }}
    [data-testid="stSidebar"] .stMarkdown p {{
        font-weight: 425;
    }}
    [data-testid="stSidebar"] hr {{
        border-color: rgba(203, 213, 225, 0.08) !important;
        margin: 0.4rem 0 !important;
    }}

    /* Sidebar search input */
    [data-testid="stSidebar"] .stTextInput div,
    [data-testid="stSidebar"] .stTextInput > div,
    [data-testid="stSidebar"] .stTextInput > div > div,
    section[data-testid="stSidebar"] .stTextInput div {{
        background: transparent !important;
        background-color: transparent !important;
    }}
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] input[type="text"],
    [data-testid="stSidebar"] [data-testid="stTextInput"] input,
    [data-testid="stSidebar"] .stTextInput > div > input,
    [data-testid="stSidebar"] .stTextInput > div > div > input,
    section[data-testid="stSidebar"] input {{
        background: rgba(255,255,255,0.06) !important;
        background-color: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(203,213,225,0.15) !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-size: 0.8rem !important;
        padding: 0.45rem 0.6rem !important;
        border-radius: 6px !important;
        caret-color: #FFFFFF !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }}
    [data-testid="stSidebar"] .stTextInput input::placeholder,
    [data-testid="stSidebar"] input[type="text"]::placeholder,
    [data-testid="stSidebar"] [data-testid="stTextInput"] input::placeholder,
    section[data-testid="stSidebar"] input::placeholder {{
        color: rgba(203,213,225,0.45) !important;
        -webkit-text-fill-color: rgba(203,213,225,0.45) !important;
        opacity: 1 !important;
    }}
    [data-testid="stSidebar"] .stTextInput input:focus,
    [data-testid="stSidebar"] input[type="text"]:focus,
    [data-testid="stSidebar"] [data-testid="stTextInput"] input:focus,
    section[data-testid="stSidebar"] input:focus {{
        border-color: {_ACCENT_LIGHT} !important;
        box-shadow: 0 0 0 2px rgba(212,168,67,0.12) !important;
        background: rgba(255,255,255,0.08) !important;
        background-color: rgba(255,255,255,0.08) !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }}

    /* Sidebar section headers */
    .sidebar-section {{
        font-size: 0.6rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        color: {_ACCENT_LIGHT} !important;
        font-weight: 600 !important;
        margin-top: 0.8rem !important;
        margin-bottom: 0.2rem !important;
        padding-left: 0.7rem !important;
    }}

    /* ================================================================
       TIPOGRAFIJA — Premium Variable Font Hierarchy
       ================================================================ */
    h1 {{
        color: {_TEXT} !important;
        font-weight: 700 !important;
        font-size: 1.7rem !important;
        line-height: 1.2 !important;
        letter-spacing: -0.025em !important;
        border-bottom: 2px solid {_BORDER} !important;
        padding-bottom: 0.5rem !important;
        margin-bottom: 1.2rem !important;
    }}
    h2 {{
        color: {_TEXT} !important;
        font-weight: 650 !important;
        font-size: 1.4rem !important;
        letter-spacing: -0.02em !important;
    }}
    h3 {{
        color: {_TEXT} !important;
        font-weight: 600 !important;
        font-size: 1.15rem !important;
        letter-spacing: -0.015em !important;
    }}

    /* ================================================================
       FORME
       ================================================================ */
    .stSelectbox label, .stRadio > label, .stTextInput label,
    .stTextArea label, .stNumberInput label, .stDateInput label,
    .stCheckbox label {{
        font-weight: 550 !important;
        color: {_TEXT} !important;
        font-size: 0.85rem !important;
    }}
    .stTextInput input, .stNumberInput input, .stTextArea textarea {{
        border: 1px solid {_BORDER} !important;
        border-radius: 6px !important;
        background-color: {_CARD} !important;
        color: {_TEXT} !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }}
    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {{
        border-color: {_BRAND} !important;
        box-shadow: 0 0 0 3px rgba(30, 58, 95, 0.08) !important;
    }}

    /* ================================================================
       GUMBI — Shadow Hierarchy
       ================================================================ */
    /* Primary: navy gradient + colored shadow */
    button[data-testid="stBaseButton-primary"] {{
        background: linear-gradient(135deg, {_BRAND} 0%, {_BRAND_LIGHT} 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 0.55rem 1.5rem !important;
        min-height: 2.25rem !important;
        letter-spacing: 0.01em !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 8px rgba(30, 58, 95, 0.2) !important;
    }}
    button[data-testid="stBaseButton-primary"]:hover {{
        box-shadow: 0 4px 14px rgba(30, 58, 95, 0.28) !important;
        transform: translateY(-1px) !important;
    }}
    button[data-testid="stBaseButton-primary"]:active {{
        transform: translateY(0) !important;
        box-shadow: 0 1px 4px rgba(30, 58, 95, 0.2) !important;
    }}

    /* Secondary: subtle border, no shadow */
    button[data-testid="stBaseButton-secondary"] {{
        border: 1px solid {_BORDER} !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        color: {_TEXT} !important;
        background-color: {_CARD} !important;
        min-height: 2.25rem !important;
        transition: all 0.15s ease !important;
    }}
    button[data-testid="stBaseButton-secondary"]:hover {{
        border-color: {_BRAND} !important;
        background-color: {_BRAND_SURFACE} !important;
        color: {_BRAND} !important;
    }}

    /* Download: green gradient + green shadow */
    .stDownloadButton > button {{
        background: linear-gradient(135deg, {_SUCCESS} 0%, {_SUCCESS_DARK} 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.5rem !important;
        min-height: 2.25rem !important;
        box-shadow: 0 2px 8px rgba(5, 150, 105, 0.2) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    .stDownloadButton > button:hover {{
        box-shadow: 0 4px 14px rgba(5, 150, 105, 0.3) !important;
        transform: translateY(-1px) !important;
    }}
    .stDownloadButton > button:active {{
        transform: translateY(0) !important;
    }}

    /* ================================================================
       FOCUS VISIBLE — WCAG 2.2 SC 2.4.13
       ================================================================ */
    button:focus-visible,
    input:focus-visible,
    textarea:focus-visible,
    select:focus-visible,
    [role="tab"]:focus-visible,
    a:focus-visible {{
        outline: 2px solid {_BRAND} !important;
        outline-offset: 2px !important;
    }}

    /* ================================================================
       PREFERS-REDUCED-MOTION — WCAG 2.2 Motion
       ================================================================ */
    @media (prefers-reduced-motion: reduce) {{
        *, *::before, *::after {{
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
        }}
    }}

    /* ================================================================
       EXPANDER
       ================================================================ */
    .streamlit-expanderHeader {{
        font-weight: 600 !important;
        color: {_TEXT} !important;
        font-size: 0.88rem !important;
        background-color: {_BRAND_SURFACE} !important;
        border-radius: 8px !important;
    }}

    /* Alerts */
    .stAlert {{
        border-radius: 8px !important;
    }}

    /* ================================================================
       METRICKI PRIKAZ — Tabular Numbers
       ================================================================ */
    [data-testid="stMetricValue"] {{
        color: {_BRAND} !important;
        font-weight: 700 !important;
        font-feature-settings: 'tnum' 1, 'zero' 1 !important;
        letter-spacing: -0.02em !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {_TEXT_SEC} !important;
        font-weight: 500 !important;
        letter-spacing: 0.01em !important;
    }}

    /* ================================================================
       TABS — Pill Style
       ================================================================ */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2px;
        background-color: {_BRAND_SURFACE};
        padding: 3px;
        border-radius: 8px;
        border: 1px solid {_BORDER};
    }}
    .stTabs [data-baseweb="tab"] {{
        font-weight: 500 !important;
        border-radius: 6px !important;
        padding: 0.45rem 0.9rem !important;
        font-size: 0.82rem !important;
        color: {_TEXT_SEC} !important;
        background-color: transparent !important;
        border: none !important;
        transition: all 0.15s ease !important;
        min-height: 1.75rem !important;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: rgba(30, 58, 95, 0.06) !important;
        color: {_TEXT} !important;
    }}
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        background-color: {_CARD} !important;
        color: {_BRAND} !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
    }}
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {{
        display: none !important;
    }}

    /* ================================================================
       POCETNA STRANICA
       ================================================================ */
    .module-card {{
        background: {_CARD};
        border: 1px solid {_BORDER};
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.5rem;
        transition: border-color 0.15s ease, box-shadow 0.2s ease !important;
    }}
    .module-card:hover {{
        border-color: {_BRAND};
        box-shadow: 0 4px 12px rgba(30, 58, 95, 0.08);
    }}

    /* Hero — Atmospheric depth */
    .hero-section {{
        background: {_BRAND};
        background-image:
            radial-gradient(ellipse at 15% 80%, rgba(45, 74, 111, 0.6) 0%, transparent 55%),
            radial-gradient(ellipse at 85% 20%, rgba(30, 58, 95, 0.5) 0%, transparent 50%);
        color: white;
        padding: 1.8rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }}
    .hero-section h2 {{
        color: white !important;
        margin-bottom: 0.3rem !important;
        letter-spacing: -0.02em !important;
    }}
    .hero-section p {{
        color: rgba(255,255,255,0.85) !important;
        font-size: 0.9rem !important;
        font-weight: 425 !important;
        margin: 0 !important;
    }}

    /* ================================================================
       GENERIRANI DOKUMENT - Pravni stil (Times New Roman)
       Ovo se NE mijenja — zakonski format
       ================================================================ */
    .legal-doc {{
        background-color: white;
        padding: 50px 55px;
        color: black;
        border: 1px solid {_BORDER};
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border-radius: 2px;
        margin: 15px auto;
        max-width: 800px;
    }}
    .header-doc {{
        text-align: center;
        font-weight: bold;
        font-size: 14pt;
        margin-bottom: 20px;
        text-transform: uppercase;
        font-family: 'Times New Roman', serif !important;
        letter-spacing: 0.5px;
    }}
    .party-info {{
        text-align: left;
        margin-bottom: 15px;
        font-family: 'Times New Roman', serif !important;
        line-height: 1.5;
    }}
    .doc-body {{
        text-align: justify;
        text-justify: inter-word;
        margin-bottom: 10px;
        font-family: 'Times New Roman', serif !important;
        line-height: 1.5;
    }}
    .justified {{
        text-align: justify;
        text-justify: inter-word;
        font-family: 'Times New Roman', serif !important;
        line-height: 1.5;
    }}
    .section-title {{
        font-weight: bold;
        margin-top: 18px;
        margin-bottom: 8px;
        font-family: 'Times New Roman', serif !important;
        text-transform: uppercase;
        font-size: 11pt;
    }}
    .cost-table {{
        margin-top: 20px;
        width: 100%;
        border-collapse: collapse;
        font-family: 'Times New Roman', serif !important;
    }}
    .cost-table td {{
        padding: 6px 12px;
        border-bottom: 1px solid #ddd;
    }}
    .clausula {{
        font-style: italic;
        border: 1px solid #ccc;
        padding: 15px;
        margin: 20px 0;
        background-color: #fafaf5;
        font-family: 'Times New Roman', serif !important;
    }}
    .signature-row {{
        display: flex;
        justify-content: space-between;
        margin-top: 60px;
        font-family: 'Times New Roman', serif !important;
    }}
    .signature-block {{
        text-align: center;
        width: 45%;
        font-family: 'Times New Roman', serif !important;
    }}

    /* ================================================================
       PRINT
       ================================================================ */
    @media print {{
        .legal-doc {{
            box-shadow: none;
            border: none;
            padding: 0;
            margin: 0;
        }}
        [data-testid="stSidebar"],
        .stButton, .stDownloadButton,
        header, footer {{
            display: none !important;
        }}
    }}
</style>
"""
