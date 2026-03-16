# -----------------------------------------------------------------------------
# KONFIGURACIJA: CSS stilovi, konstante i UI teme
# Stil: Trust-Centric Svicarski Minimalizam
# Paleta: Navy autoritet + zlatni naglasci + neutralne sive
# Tipografija: Inter, modular scale Major Third (1.250)
# Pristupacnost: WCAG 2.1 AA (min 4.5:1 kontrast za tekst)
# Referenca: agent_docs/ui_strategy.md
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
       TIPOGRAFIJA - Inter, Major Third skala (1.250)
       ================================================================ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ================================================================
       LAYOUT - Ogranicen sirinom za citljivost
       ================================================================ */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }}

    /* ================================================================
       SIDEBAR - Tamna navy pozadina, visok kontrast teksta
       Kontrast: #CBD5E1 na #0F1B2D = 11.1:1 (AAA)
       ================================================================ */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {_SIDEBAR_BG} 0%, #081220 100%);
        border-right: 1px solid rgba(30, 58, 95, 0.3);
    }}

    /* Sidebar tekst - svijetlo sivi na tamnoj pozadini */
    [data-testid="stSidebar"] * {{
        color: {_SIDEBAR_TEXT} !important;
    }}

    /* Sidebar naslov - zlato na tamnoj */
    [data-testid="stSidebar"] h1 {{
        color: {_ACCENT_LIGHT} !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px;
        padding-bottom: 0.2rem;
    }}

    /* Sidebar radio - cistiji razmak, hover s visokim kontrastom */
    [data-testid="stSidebar"] .stRadio > div {{
        gap: 0px !important;
    }}
    [data-testid="stSidebar"] .stRadio label {{
        font-family: 'Inter', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 400 !important;
        padding: 0.5rem 0.75rem !important;
        border-radius: 6px !important;
        margin: 1px 0 !important;
        transition: background-color 0.15s ease !important;
        cursor: pointer !important;
    }}
    [data-testid="stSidebar"] .stRadio label:hover {{
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: #FFFFFF !important;
    }}

    /* Sidebar markdown */
    [data-testid="stSidebar"] .stMarkdown p {{
        font-family: 'Inter', sans-serif !important;
    }}
    [data-testid="stSidebar"] hr {{
        border-color: rgba(203, 213, 225, 0.12) !important;
        margin: 0.5rem 0 !important;
    }}

    /* Sidebar section headers - zlatne oznake */
    .sidebar-section {{
        font-family: 'Inter', sans-serif !important;
        font-size: 0.65rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1.8px !important;
        color: {_ACCENT_LIGHT} !important;
        font-weight: 600 !important;
        margin-top: 1.2rem !important;
        margin-bottom: 0.3rem !important;
        padding-left: 0.75rem !important;
        opacity: 0.9;
    }}

    /* ================================================================
       GLAVNI SADRZAJ - Zaglavlja, forme, gumbi
       ================================================================ */

    /* H1 - Naslov modula */
    h1 {{
        font-family: 'Inter', sans-serif !important;
        color: {_TEXT} !important;
        font-weight: 700 !important;
        font-size: 1.95rem !important;
        line-height: 1.2 !important;
        border-bottom: 2px solid {_BORDER} !important;
        padding-bottom: 0.6rem !important;
        margin-bottom: 1.5rem !important;
    }}

    /* H2, H3 - Podnaslovi */
    h2 {{
        font-family: 'Inter', sans-serif !important;
        color: {_TEXT} !important;
        font-weight: 600 !important;
        font-size: 1.56rem !important;
        line-height: 1.3 !important;
    }}
    h3 {{
        font-family: 'Inter', sans-serif !important;
        color: {_TEXT} !important;
        font-weight: 600 !important;
        font-size: 1.25rem !important;
        line-height: 1.4 !important;
    }}

    /* Labels - Svi form widgeti */
    .stSelectbox label, .stRadio > label, .stTextInput label,
    .stTextArea label, .stNumberInput label, .stDateInput label,
    .stCheckbox label {{
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: {_TEXT} !important;
        font-size: 0.875rem !important;
    }}

    /* Input polja - ciste granice, suptilan fokus */
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

    /* Primary gumbi - Navy gradient, profesionalan */
    button[data-testid="stBaseButton-primary"] {{
        background: linear-gradient(135deg, {_BRAND} 0%, {_BRAND_LIGHT} 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.6rem 1.8rem !important;
        letter-spacing: 0.2px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(15, 27, 45, 0.2) !important;
    }}
    button[data-testid="stBaseButton-primary"]:hover {{
        background: linear-gradient(135deg, {_BRAND_LIGHT} 0%, {_BRAND} 100%) !important;
        box-shadow: 0 3px 8px rgba(15, 27, 45, 0.25) !important;
        transform: translateY(-1px) !important;
    }}

    /* Secondary gumbi */
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

    /* Download gumb - Smaragdna zelena za "sigurnu akciju" */
    .stDownloadButton > button {{
        background: linear-gradient(135deg, {_SUCCESS} 0%, {_SUCCESS_DARK} 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.8rem !important;
        box-shadow: 0 1px 3px rgba(5, 150, 105, 0.2) !important;
        transition: all 0.2s ease !important;
    }}
    .stDownloadButton > button:hover {{
        box-shadow: 0 3px 8px rgba(5, 150, 105, 0.3) !important;
        transform: translateY(-1px) !important;
    }}

    /* Expander - suptilan, ne natjece se za paznju */
    .streamlit-expanderHeader {{
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: {_TEXT} !important;
        font-size: 0.9rem !important;
        background-color: {_BRAND_SURFACE} !important;
        border-radius: 8px !important;
    }}

    /* Info / Warning / Alert kutije */
    .stAlert {{
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
    }}

    /* Metric - brojcane vrijednosti */
    [data-testid="stMetricValue"] {{
        font-family: 'Inter', sans-serif !important;
        color: {_BRAND} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stMetricLabel"] {{
        font-family: 'Inter', sans-serif !important;
        color: {_TEXT_SEC} !important;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
    }}
    .stTabs [data-baseweb="tab"] {{
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        border-radius: 6px 6px 0 0 !important;
    }}

    /* ================================================================
       GENERIRANI DOKUMENT - Print-friendly pravni stil
       Times New Roman je obavezan za pravne dokumente u RH.
       Ove klase NE mijenjamo - one su standard.
       ================================================================ */
    .legal-doc {{
        background-color: white;
        padding: 60px 65px;
        color: black;
        border: 1px solid {_BORDER};
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-radius: 2px;
        margin: 20px auto;
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
       PRINT STILOVI
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
