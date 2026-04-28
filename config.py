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
# DESIGN TOKENI — Atmospheric Premium (Linear/Stripe inspired)
# ============================================================================
# Background / Surface — warm tinted, never flat white
_BG = "#F5F5F0"            # warm off-white, slight warmth
_SURFACE = "#F0F0EB"       # slightly deeper warm
_CARD = "#FFFFFF"
_SUNKEN = "#EAEAE5"        # warm sunken

# Brand Navy (hue ~260) — deeper, richer
_BRAND = "#162D50"         # deeper navy for authority
_BRAND_LIGHT = "#1E3A5F"   # medium navy
_BRAND_MID = "#2D4A6F"     # lighter navy
_BRAND_SURFACE = "#E8EDF5" # tinted surface

# Accent Gold — warmer, more saturated
_ACCENT = "#C4930A"
_ACCENT_LIGHT = "#E0B73B"
_ACCENT_GLOW = "rgba(224, 183, 59, 0.15)"

# Text — high contrast
_TEXT = "#0A0F1A"           # near-black
_TEXT_SEC = "#3D4A5C"       # readable secondary
_TEXT_MUTED = "#8494A7"     # muted

# Borders — warmer
_BORDER = "#DDD8D0"        # warm border
_BORDER_STRONG = "#C5BFB6"  # stronger warm border

# Semantic
_SUCCESS = "#059669"
_SUCCESS_DARK = "#047857"
_WARNING = "#D97706"
_DANGER = "#DC2626"

# Sidebar — deep rich dark with more color
_SIDEBAR_BG = "#0B1628"    # very deep navy-black
_SIDEBAR_DEEP = "#060E1C"  # deepest
_SIDEBAR_TEXT = "#C8D4E4"
_SIDEBAR_GLOW1 = "rgba(30, 80, 160, 0.45)"  # visible blue blob
_SIDEBAR_GLOW2 = "rgba(100, 60, 180, 0.25)"  # subtle purple blob
_SIDEBAR_GLOW3 = "rgba(20, 120, 140, 0.20)"  # teal accent

# ============================================================================
# CSS STILOVI — Premium Redesign
# ============================================================================
CSS_STILOVI = f"""
<link rel="stylesheet" href="https://rsms.me/inter/inter.css">
<style>
    /* ================================================================
       INTER VARIABLE FONT — Full OpenType Features
       Exclude Material Symbols used by Streamlit internals
       ================================================================ */
    html, body, [class*="css"], [class*="st-"],
    .stApp, .main, div, p, label, input, textarea, select, button {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        font-feature-settings: 'liga' 1, 'calt' 1;
        font-optical-sizing: auto;
    }}
    /* Preserve Material Symbols for ALL Streamlit internal icons */
    [data-testid="stIconMaterial"],
    [data-testid="stIconMaterial"] * {{
        font-family: 'Material Symbols Rounded', sans-serif !important;
    }}

    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li,
    .stMarkdown p {{
        font-weight: 425;
        letter-spacing: -0.011em;
        line-height: 1.65;
        color: {_TEXT_SEC};
    }}

    /* Force white text inside primary buttons (all children) */
    button[data-testid="stBaseButton-primary"] *,
    button[data-testid="stBaseButton-primary"] p,
    button[data-testid="stBaseButton-primary"] span,
    button[data-testid="stBaseButton-primary"] div {{
        color: #FFFFFF !important;
    }}
    .stDownloadButton > button *,
    .stDownloadButton > button p,
    .stDownloadButton > button span {{
        color: #FFFFFF !important;
    }}

    /* ================================================================
       APP BACKGROUND — Warm atmospheric gradient
       ================================================================ */
    .stApp {{
        background: linear-gradient(165deg, {_BG} 0%, #EDECE6 35%, #E8E6E0 70%, #F0EEEA 100%) !important;
    }}
    section.main {{
        scroll-padding-top: 3.5rem;
    }}

    /* ================================================================
       LAYOUT
       ================================================================ */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }}

    /* ================================================================
       SIDEBAR — Vivid Aurora Dark
       ================================================================ */
    [data-testid="stSidebar"] {{
        background: {_SIDEBAR_BG};
        background-image:
            radial-gradient(ellipse 130% 80% at 10% 90%, {_SIDEBAR_GLOW1} 0%, transparent 60%),
            radial-gradient(ellipse 100% 100% at 85% 10%, {_SIDEBAR_GLOW2} 0%, transparent 55%),
            radial-gradient(ellipse 80% 60% at 40% 50%, {_SIDEBAR_GLOW3} 0%, transparent 50%),
            linear-gradient(180deg, {_SIDEBAR_DEEP} 0%, {_SIDEBAR_BG} 30%, {_SIDEBAR_DEEP} 100%);
        border-right: 1px solid rgba(100, 140, 220, 0.15);
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.15);
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

    /* Sidebar gumbi — navigacija */
    [data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"],
    [data-testid="stSidebar"] .stButton button[kind="secondary"],
    [data-testid="stSidebar"] .stButton > button:not([kind="primary"]) {{
        background-color: transparent !important;
        background: transparent !important;
        border: 1px solid rgba(200, 212, 228, 0.08) !important;
        color: {_SIDEBAR_TEXT} !important;
        font-size: 0.82rem !important;
        font-weight: 425 !important;
        padding: 0.55rem 0.75rem !important;
        min-height: 2.1rem !important;
        border-radius: 8px !important;
        transition: all 0.2s cubic-bezier(0.4,0,0.2,1) !important;
        text-align: left !important;
    }}
    [data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"]:hover,
    [data-testid="stSidebar"] .stButton button[kind="secondary"]:hover,
    [data-testid="stSidebar"] .stButton > button:not([kind="primary"]):hover {{
        background-color: rgba(255, 255, 255, 0.1) !important;
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(200, 212, 228, 0.25) !important;
        color: #FFFFFF !important;
        transform: translateX(2px) !important;
    }}
    [data-testid="stSidebar"] button[data-testid="stBaseButton-primary"],
    [data-testid="stSidebar"] .stButton button[kind="primary"] {{
        background: linear-gradient(135deg, {_BRAND_LIGHT} 0%, {_BRAND_MID} 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        padding: 0.55rem 0.75rem !important;
        min-height: 2.1rem !important;
        border-radius: 8px !important;
        text-align: left !important;
        box-shadow: 0 2px 12px rgba(30, 80, 160, 0.35), inset 0 1px 0 rgba(255,255,255,0.1) !important;
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
        border-color: rgba(200, 212, 228, 0.06) !important;
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
        background: rgba(255,255,255,0.05) !important;
        background-color: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(200,212,228,0.12) !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-size: 0.8rem !important;
        padding: 0.45rem 0.6rem !important;
        border-radius: 8px !important;
        caret-color: #FFFFFF !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }}
    [data-testid="stSidebar"] .stTextInput input::placeholder,
    [data-testid="stSidebar"] input[type="text"]::placeholder,
    [data-testid="stSidebar"] [data-testid="stTextInput"] input::placeholder,
    section[data-testid="stSidebar"] input::placeholder {{
        color: rgba(200,212,228,0.4) !important;
        -webkit-text-fill-color: rgba(200,212,228,0.4) !important;
        opacity: 1 !important;
    }}
    [data-testid="stSidebar"] .stTextInput input:focus,
    [data-testid="stSidebar"] input[type="text"]:focus,
    [data-testid="stSidebar"] [data-testid="stTextInput"] input:focus,
    section[data-testid="stSidebar"] input:focus {{
        border-color: {_ACCENT_LIGHT} !important;
        box-shadow: 0 0 0 2px {_ACCENT_GLOW} !important;
        background: rgba(255,255,255,0.08) !important;
        background-color: rgba(255,255,255,0.08) !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }}

    /* Sidebar section headers */
    .sidebar-section {{
        font-size: 0.6rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
        color: {_ACCENT_LIGHT} !important;
        font-weight: 700 !important;
        margin-top: 1rem !important;
        margin-bottom: 0.25rem !important;
        padding-left: 0.75rem !important;
        text-shadow: 0 0 12px {_ACCENT_GLOW} !important;
    }}

    /* ================================================================
       TIPOGRAFIJA — Dramatic Scale
       ================================================================ */
    h1 {{
        color: {_TEXT} !important;
        font-weight: 760 !important;
        font-size: 2.1rem !important;
        line-height: 1.15 !important;
        letter-spacing: -0.035em !important;
        border-bottom: none !important;
        padding-bottom: 0.3rem !important;
        margin-bottom: 1.5rem !important;
    }}
    h2 {{
        color: {_TEXT} !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        letter-spacing: -0.025em !important;
    }}
    h3 {{
        color: {_TEXT} !important;
        font-weight: 650 !important;
        font-size: 1.2rem !important;
        letter-spacing: -0.02em !important;
    }}
    h5 {{
        color: {_TEXT_SEC} !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        margin-top: 2rem !important;
        margin-bottom: 0.8rem !important;
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
        border-radius: 8px !important;
        background-color: {_CARD} !important;
        color: {_TEXT} !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
    }}
    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {{
        border-color: {_BRAND_LIGHT} !important;
        box-shadow: 0 0 0 3px rgba(22, 45, 80, 0.1), 0 1px 2px rgba(0,0,0,0.04) !important;
    }}

    /* ================================================================
       GUMBI — Elevated with Colored Shadows
       ================================================================ */
    button[data-testid="stBaseButton-primary"] {{
        background: linear-gradient(135deg, {_BRAND} 0%, {_BRAND_MID} 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 0.6rem 1.6rem !important;
        min-height: 2.4rem !important;
        letter-spacing: 0.01em !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px rgba(22, 45, 80, 0.25), 0 1px 3px rgba(22, 45, 80, 0.15) !important;
    }}
    button[data-testid="stBaseButton-primary"]:hover {{
        box-shadow: 0 8px 25px rgba(22, 45, 80, 0.35), 0 2px 6px rgba(22, 45, 80, 0.2) !important;
        transform: translateY(-2px) !important;
    }}
    button[data-testid="stBaseButton-primary"]:active {{
        transform: translateY(0) !important;
        box-shadow: 0 2px 8px rgba(22, 45, 80, 0.2) !important;
    }}

    button[data-testid="stBaseButton-secondary"] {{
        border: 1px solid {_BORDER} !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        color: {_TEXT} !important;
        background-color: {_CARD} !important;
        min-height: 2.4rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    }}
    button[data-testid="stBaseButton-secondary"]:hover {{
        border-color: {_BRAND_LIGHT} !important;
        background-color: {_BRAND_SURFACE} !important;
        color: {_BRAND} !important;
        box-shadow: 0 4px 12px rgba(22, 45, 80, 0.1) !important;
        transform: translateY(-1px) !important;
    }}

    .stDownloadButton > button {{
        background: linear-gradient(135deg, {_SUCCESS} 0%, {_SUCCESS_DARK} 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.6rem !important;
        min-height: 2.4rem !important;
        box-shadow: 0 4px 14px rgba(5, 150, 105, 0.25), 0 1px 3px rgba(5, 150, 105, 0.15) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    .stDownloadButton > button:hover {{
        box-shadow: 0 8px 25px rgba(5, 150, 105, 0.35), 0 2px 6px rgba(5, 150, 105, 0.2) !important;
        transform: translateY(-2px) !important;
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
        outline: 2px solid {_BRAND_LIGHT} !important;
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
        border-radius: 10px !important;
    }}

    .stAlert {{
        border-radius: 10px !important;
    }}

    /* ================================================================
       METRICKI PRIKAZ — Tabular Numbers
       ================================================================ */
    [data-testid="stMetricValue"] {{
        color: {_BRAND} !important;
        font-weight: 760 !important;
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
        gap: 3px;
        background-color: {_SURFACE};
        padding: 4px;
        border-radius: 10px;
        border: 1px solid {_BORDER};
    }}
    .stTabs [data-baseweb="tab"] {{
        font-weight: 500 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.82rem !important;
        color: {_TEXT_SEC} !important;
        background-color: transparent !important;
        border: none !important;
        transition: all 0.2s ease !important;
        min-height: 1.85rem !important;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: rgba(22, 45, 80, 0.06) !important;
        color: {_TEXT} !important;
    }}
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        background-color: {_CARD} !important;
        color: {_BRAND} !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04) !important;
    }}
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {{
        display: none !important;
    }}

    /* ================================================================
       POCETNA STRANICA — Cards with depth
       ================================================================ */
    .module-card {{
        background: {_CARD};
        border: 1px solid {_BORDER};
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.6rem;
        transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        position: relative;
        overflow: hidden;
    }}
    .module-card::before {{
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 3px;
        background: linear-gradient(180deg, {_BRAND_LIGHT}, {_BRAND_MID});
        opacity: 0;
        transition: opacity 0.25s ease;
    }}
    /* Subtle hover: only border accent — kartica je info, ne button.
       Click target je gumb ispod kartice (afford. mismatch fix). */
    .module-card:hover {{
        border-color: rgba(22, 45, 80, 0.18);
    }}
    .module-card:hover::before {{
        opacity: 0.5;
    }}

    /* Hero — Large atmospheric gradient */
    .hero-section {{
        background: linear-gradient(135deg, {_BRAND} 0%, {_BRAND_LIGHT} 40%, {_BRAND_MID} 100%);
        background-size: 200% 200%;
        color: white;
        padding: 2.8rem 2.5rem;
        border-radius: 18px;
        margin-bottom: 2.5rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 40px rgba(22, 45, 80, 0.25), 0 2px 10px rgba(22, 45, 80, 0.15);
    }}
    .hero-section::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 60%;
        height: 200%;
        background: radial-gradient(ellipse, rgba(224, 183, 59, 0.08) 0%, transparent 70%);
        pointer-events: none;
    }}
    .hero-section::after {{
        content: '';
        position: absolute;
        bottom: -30%;
        left: -10%;
        width: 50%;
        height: 150%;
        background: radial-gradient(ellipse, rgba(100, 180, 255, 0.1) 0%, transparent 65%);
        pointer-events: none;
    }}
    .hero-section h2 {{
        color: white !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.03em !important;
        font-size: 1.85rem !important;
        font-weight: 760 !important;
        position: relative;
        z-index: 1;
    }}
    .hero-section p {{
        color: rgba(255,255,255,0.8) !important;
        font-size: 1rem !important;
        font-weight: 425 !important;
        margin: 0 !important;
        position: relative;
        z-index: 1;
        max-width: 540px;
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
       DOCUMENT TYPE PICKER — Navy left-bar label
       ================================================================ */
    .doc-selector-label {{
        display: block;
        font-size: 0.67rem;
        text-transform: uppercase;
        letter-spacing: 0.13em;
        font-weight: 700;
        color: {_BRAND};
        background: linear-gradient(90deg, rgba(22,45,80,0.08) 0%, transparent 90%);
        border-left: 3px solid {_BRAND};
        padding: 0.4rem 0.8rem 0.4rem 0.7rem;
        border-radius: 0 6px 6px 0;
        margin-bottom: 0.3rem;
        margin-top: 0.8rem;
    }}

    /* Category button-pill row */
    .cat-btn-row {{
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1rem;
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

    /* =========================================================================
       Sidebar collapse button — zamijeniti default ">>"/"<<" strelice
       sa vertikalnim trima tockama (kebab menu style "⋮")
       ========================================================================= */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stBaseButton-headerNoPadding"][aria-label*="sidebar" i],
    [kind="headerNoPadding"][aria-label*="sidebar" i] {{
        position: relative !important;
    }}
    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="stBaseButton-headerNoPadding"][aria-label*="sidebar" i] svg,
    [kind="headerNoPadding"][aria-label*="sidebar" i] svg {{
        display: none !important;
    }}
    [data-testid="stSidebarCollapseButton"]::after,
    [data-testid="stBaseButton-headerNoPadding"][aria-label*="sidebar" i]::after,
    [kind="headerNoPadding"][aria-label*="sidebar" i]::after {{
        content: "⋮";
        font-size: 22px;
        font-weight: 700;
        line-height: 1;
        color: #94A3B8;
        display: inline-block;
        text-align: center;
        width: 100%;
    }}
    [data-testid="stSidebarCollapseButton"]:hover::after,
    [data-testid="stBaseButton-headerNoPadding"][aria-label*="sidebar" i]:hover::after,
    [kind="headerNoPadding"][aria-label*="sidebar" i]:hover::after {{
        color: #D4A843;
    }}
</style>
"""
