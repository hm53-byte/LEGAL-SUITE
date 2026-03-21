# -----------------------------------------------------------------------------
# KONFIGURACIJA: CSS stilovi, konstante i UI teme
# Stil: Trust-Centric Svicarski Minimalizam
# Paleta: Navy autoritet + zlatni naglasci + neutralne sive
# Tipografija: Inter, modular scale Major Third (1.250)
# Pristupacnost: WCAG 2.1 AA (min 4.5:1 kontrast za tekst)
# -----------------------------------------------------------------------------

PAGE_TITLE = "LegalTech Suite Pro"
PAGE_ICON = "\u2696\ufe0f"
PAGE_LAYOUT = "wide"

# Design Tokeni
_BRAND = "#1E3A5F"
_BRAND_LIGHT = "#2D4A6F"
_BRAND_SURFACE = "#EFF3F8"
_ACCENT = "#B8860B"
_ACCENT_LIGHT = "#D4A843"
_SURFACE = "#F8FAFC"
_CARD = "#FFFFFF"
_TEXT = "#0F172A"
_TEXT_SEC = "#475569"
_TEXT_MUTED = "#94A3B8"
_BORDER = "#E2E8F0"
_SUCCESS = "#059669"
_SUCCESS_DARK = "#047857"
_WARNING = "#D97706"
_SIDEBAR_BG = "#0F1B2D"
_SIDEBAR_TEXT = "#CBD5E1"

CSS_STILOVI = f"""
<style>
    /* ================================================================
       LAYOUT
       ================================================================ */
    .main .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }}

    /* ================================================================
       SIDEBAR
       ================================================================ */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {_SIDEBAR_BG} 0%, #081220 100%);
        border-right: 1px solid rgba(30, 58, 95, 0.3);
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
        font-family: 'Inter', sans-serif !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
    }}

    /* Sidebar gumbi - navigacija */
    [data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"],
    [data-testid="stSidebar"] .stButton button[kind="secondary"],
    [data-testid="stSidebar"] .stButton > button:not([kind="primary"]) {{
        background-color: transparent !important;
        background: transparent !important;
        border: 1px solid rgba(203, 213, 225, 0.1) !important;
        color: {_SIDEBAR_TEXT} !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.82rem !important;
        font-weight: 400 !important;
        padding: 0.4rem 0.7rem !important;
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
        font-family: 'Inter', sans-serif !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        padding: 0.4rem 0.7rem !important;
        border-radius: 6px !important;
        text-align: left !important;
    }}
    [data-testid="stSidebar"] button {{
        color: {_SIDEBAR_TEXT} !important;
    }}
    [data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] p,
    [data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] span {{
        color: #FFFFFF !important;
    }}
    [data-testid="stSidebar"] .stMarkdown p {{
        font-family: 'Inter', sans-serif !important;
    }}
    [data-testid="stSidebar"] hr {{
        border-color: rgba(203, 213, 225, 0.1) !important;
        margin: 0.4rem 0 !important;
    }}

    /* Sidebar search input — multiple selectors for Cloud compat */
    [data-testid="stSidebar"] .stTextInput input,
    [data-testid="stSidebar"] input[type="text"],
    [data-testid="stSidebar"] [data-testid="stTextInput"] input,
    [data-testid="stSidebar"] .stTextInput > div > input,
    [data-testid="stSidebar"] .stTextInput > div > div > input,
    section[data-testid="stSidebar"] input {{
        background: rgba(255,255,255,0.08) !important;
        background-color: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(203,213,225,0.2) !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-size: 0.8rem !important;
        padding: 0.4rem 0.6rem !important;
        border-radius: 6px !important;
        caret-color: #FFFFFF !important;
    }}
    [data-testid="stSidebar"] .stTextInput input::placeholder,
    [data-testid="stSidebar"] input[type="text"]::placeholder,
    [data-testid="stSidebar"] [data-testid="stTextInput"] input::placeholder,
    section[data-testid="stSidebar"] input::placeholder {{
        color: rgba(203,213,225,0.5) !important;
        -webkit-text-fill-color: rgba(203,213,225,0.5) !important;
        opacity: 1 !important;
    }}
    [data-testid="stSidebar"] .stTextInput input:focus,
    [data-testid="stSidebar"] input[type="text"]:focus,
    [data-testid="stSidebar"] [data-testid="stTextInput"] input:focus,
    section[data-testid="stSidebar"] input:focus {{
        border-color: {_ACCENT_LIGHT} !important;
        box-shadow: 0 0 0 2px rgba(212,168,67,0.15) !important;
        background: rgba(255,255,255,0.1) !important;
        background-color: rgba(255,255,255,0.1) !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }}

    /* Sidebar section headers */
    .sidebar-section {{
        font-family: 'Inter', sans-serif !important;
        font-size: 0.6rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        color: {_ACCENT_LIGHT} !important;
        font-weight: 600 !important;
        margin-top: 0.8rem !important;
        margin-bottom: 0.2rem !important;
        padding-left: 0.7rem !important;
        opacity: 0.85;
    }}

    /* ================================================================
       TIPOGRAFIJA
       ================================================================ */
    h1 {{
        font-family: 'Inter', sans-serif !important;
        color: {_TEXT} !important;
        font-weight: 700 !important;
        font-size: 1.7rem !important;
        line-height: 1.2 !important;
        border-bottom: 2px solid {_BORDER} !important;
        padding-bottom: 0.5rem !important;
        margin-bottom: 1.2rem !important;
    }}
    h2 {{
        font-family: 'Inter', sans-serif !important;
        color: {_TEXT} !important;
        font-weight: 600 !important;
        font-size: 1.4rem !important;
    }}
    h3 {{
        font-family: 'Inter', sans-serif !important;
        color: {_TEXT} !important;
        font-weight: 600 !important;
        font-size: 1.15rem !important;
    }}

    /* ================================================================
       FORME
       ================================================================ */
    .stSelectbox label, .stRadio > label, .stTextInput label,
    .stTextArea label, .stNumberInput label, .stDateInput label,
    .stCheckbox label {{
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: {_TEXT} !important;
        font-size: 0.85rem !important;
    }}
    .stTextInput input, .stNumberInput input, .stTextArea textarea {{
        font-family: 'Inter', sans-serif !important;
        border: 1px solid {_BORDER} !important;
        border-radius: 8px !important;
        background-color: {_CARD} !important;
        color: {_TEXT} !important;
        transition: border-color 0.15s ease !important;
    }}
    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {{
        border-color: {_BRAND} !important;
        box-shadow: 0 0 0 3px rgba(30, 58, 95, 0.1) !important;
    }}

    /* ================================================================
       GUMBI
       ================================================================ */
    button[data-testid="stBaseButton-primary"] {{
        background: linear-gradient(135deg, {_BRAND} 0%, {_BRAND_LIGHT} 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 0.55rem 1.5rem !important;
        letter-spacing: 0.2px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(15, 27, 45, 0.15) !important;
    }}
    button[data-testid="stBaseButton-primary"]:hover {{
        box-shadow: 0 3px 8px rgba(15, 27, 45, 0.2) !important;
        transform: translateY(-1px) !important;
    }}
    button[data-testid="stBaseButton-secondary"] {{
        border: 1px solid {_BORDER} !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: {_TEXT} !important;
        background-color: {_CARD} !important;
        transition: all 0.15s ease !important;
    }}
    button[data-testid="stBaseButton-secondary"]:hover {{
        border-color: {_BRAND} !important;
        background-color: {_BRAND_SURFACE} !important;
    }}

    /* Download gumb */
    .stDownloadButton > button {{
        background: linear-gradient(135deg, {_SUCCESS} 0%, {_SUCCESS_DARK} 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.5rem !important;
        box-shadow: 0 1px 3px rgba(5, 150, 105, 0.15) !important;
        transition: all 0.2s ease !important;
    }}
    .stDownloadButton > button:hover {{
        box-shadow: 0 3px 8px rgba(5, 150, 105, 0.25) !important;
        transform: translateY(-1px) !important;
    }}

    /* Expander */
    .streamlit-expanderHeader {{
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: {_TEXT} !important;
        font-size: 0.88rem !important;
        background-color: {_BRAND_SURFACE} !important;
        border-radius: 8px !important;
    }}

    /* Alerts */
    .stAlert {{
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
    }}

    /* Metric */
    [data-testid="stMetricValue"] {{
        font-family: 'Inter', sans-serif !important;
        color: {_BRAND} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stMetricLabel"] {{
        font-family: 'Inter', sans-serif !important;
        color: {_TEXT_SEC} !important;
    }}

    /* ================================================================
       TABS
       ================================================================ */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2px;
        background-color: {_BRAND_SURFACE};
        padding: 3px;
        border-radius: 8px;
        border: 1px solid {_BORDER};
    }}
    .stTabs [data-baseweb="tab"] {{
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        border-radius: 6px !important;
        padding: 0.45rem 0.9rem !important;
        font-size: 0.82rem !important;
        color: {_TEXT_SEC} !important;
        background-color: transparent !important;
        border: none !important;
        transition: all 0.15s ease !important;
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
    .stTabs [data-baseweb="tab-highlight"] {{
        display: none !important;
    }}
    .stTabs [data-baseweb="tab-border"] {{
        display: none !important;
    }}

    /* ================================================================
       POCETNA STRANICA
       ================================================================ */
    .module-card {{
        background: {_CARD};
        border: 1px solid {_BORDER};
        border-radius: 8px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.5rem;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }}
    .module-card:hover {{
        border-color: {_BRAND};
        box-shadow: 0 2px 6px rgba(30, 58, 95, 0.06);
    }}

    /* Hero */
    .hero-section {{
        background: linear-gradient(135deg, {_BRAND} 0%, {_BRAND_LIGHT} 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 10px;
        margin-bottom: 1.2rem;
    }}
    .hero-section h2 {{
        color: white !important;
        margin-bottom: 0.3rem !important;
    }}
    .hero-section p {{
        color: rgba(255,255,255,0.85) !important;
        font-size: 0.9rem !important;
        margin: 0 !important;
    }}

    /* ================================================================
       GENERIRANI DOKUMENT - Pravni stil (Times New Roman)
       ================================================================ */
    .legal-doc {{
        background-color: white;
        padding: 50px 55px;
        color: black;
        border: 1px solid {_BORDER};
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
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
        font-family: 'Times New Roman', serif;
        letter-spacing: 0.5px;
    }}
    .party-info {{
        text-align: left;
        margin-bottom: 15px;
        font-family: 'Times New Roman', serif;
        line-height: 1.5;
    }}
    .doc-body {{
        text-align: justify;
        text-justify: inter-word;
        margin-bottom: 10px;
        font-family: 'Times New Roman', serif;
        line-height: 1.5;
    }}
    .justified {{
        text-align: justify;
        text-justify: inter-word;
        font-family: 'Times New Roman', serif;
        line-height: 1.5;
    }}
    .section-title {{
        font-weight: bold;
        margin-top: 18px;
        margin-bottom: 8px;
        font-family: 'Times New Roman', serif;
        text-transform: uppercase;
        font-size: 11pt;
    }}
    .cost-table {{
        margin-top: 20px;
        width: 100%;
        border-collapse: collapse;
        font-family: 'Times New Roman', serif;
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
    }}
    .signature-row {{
        display: flex;
        justify-content: space-between;
        margin-top: 60px;
    }}
    .signature-block {{
        text-align: center;
        width: 45%;
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
