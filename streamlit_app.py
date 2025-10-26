"""
DataAnalytics Vietnam - Streamlit App
Premium Lean Pipeline with 5-Star UX
Version: 2.0 (Bilingual, Dark Mode, Export Features)
Target: 55 seconds with professional UX
"""

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import sys
import base64
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

# Import pipeline and utilities
from premium_lean_pipeline import PremiumLeanPipeline
from utils.validators import safe_file_upload
from utils.i18n import get_text, format_number, format_currency, convert_vnd_to_usd
from utils.branding import get_logo_svg, get_brand_colors

# Import export utilities with error handling
try:
    from utils.export_utils import export_to_pdf, export_to_powerpoint
    EXPORT_AVAILABLE = True
except ImportError:
    EXPORT_AVAILABLE = False
    print("⚠️ Export libraries not installed. PDF/PPT export disabled.")

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
def initialize_session_state():
    """Initialize session state variables"""
    if 'language' not in st.session_state:
        st.session_state['language'] = 'vi'  # Default Vietnamese
    
    if 'theme' not in st.session_state:
        st.session_state['theme'] = 'dark'  # Default dark theme (better for first impression)
    
    if 'currency' not in st.session_state:
        st.session_state['currency'] = 'VND'  # Default VND
    
    if 'result' not in st.session_state:
        st.session_state['result'] = None
    
    if 'df' not in st.session_state:
        st.session_state['df'] = None

# ============================================
# THEME MANAGEMENT
# ============================================
def get_theme_css(theme='light'):
    """Generate CSS for light/dark theme with STRONG overrides"""
    colors = get_brand_colors()
    theme_colors = colors['light_theme'] if theme == 'light' else colors['dark_theme']
    
    return f"""
    <style>
        /* Global Theme Variables */
        :root {{
            --primary-color: {theme_colors['primary']};
            --secondary-color: {theme_colors['secondary']};
            --accent-color: {theme_colors['accent']};
            --success-color: {theme_colors['success']};
            --warning-color: {theme_colors['warning']};
            --danger-color: {theme_colors['danger']};
            --text-primary: {theme_colors['text_primary']};
            --text-secondary: {theme_colors['text_secondary']};
            --background: {theme_colors['background']};
            --surface: {theme_colors['surface']};
            --border: {theme_colors['border']};
        }}
        
        /* FORCE Global Background - Override Streamlit */
        .stApp {{
            background-color: {theme_colors['background']} !important;
        }}
        
        /* FORCE Main Container Theme */
        .main,
        .block-container,
        [data-testid="stAppViewContainer"],
        section[data-testid="stMain"] {{
            background-color: {theme_colors['background']} !important;
            color: {theme_colors['text_primary']} !important;
        }}
        
        /* FORCE Sidebar Theme - Most Important! */
        [data-testid="stSidebar"],
        [data-testid="stSidebar"] > div,
        section[data-testid="stSidebar"],
        .css-1d391kg {{
            background-color: {theme_colors['surface']} !important;
            color: {theme_colors['text_primary']} !important;
        }}
        
        /* FORCE Sidebar Content Text Color */
        [data-testid="stSidebar"] *,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] div,
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
            color: {theme_colors['text_primary']} !important;
        }}
        
        /* Sidebar Buttons - COMPREHENSIVE */
        [data-testid="stSidebar"] button,
        [data-testid="stSidebar"] .stButton > button {{
            color: {theme_colors['text_primary']} !important;
            background-color: {theme_colors['surface']} !important;
            border: 1px solid {theme_colors['border']} !important;
        }}
        
        /* Sidebar Primary Buttons */
        [data-testid="stSidebar"] button[kind="primary"],
        [data-testid="stSidebar"] .stButton > button[kind="primary"] {{
            background-color: {theme_colors['primary']} !important;
            color: white !important;
            border-color: {theme_colors['primary']} !important;
        }}
        
        /* Sidebar Success/Alert Boxes (for Pricing) */
        [data-testid="stSidebar"] .stSuccess,
        [data-testid="stSidebar"] .stAlert {{
            background-color: {theme_colors['success']}22 !important;
            color: {theme_colors['text_primary']} !important;
            border-color: {theme_colors['success']} !important;
        }}
        
        [data-testid="stSidebar"] .stSuccess *,
        [data-testid="stSidebar"] .stAlert * {{
            color: {theme_colors['text_primary']} !important;
        }}
        
        /* FORCE Sidebar Headers */
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4 {{
            color: {theme_colors['primary']} !important;
        }}
        
        /* Headers in Main Content */
        .main-header {{
            font-size: 2.5rem;
            font-weight: 700;
            color: {theme_colors['primary']} !important;
            margin-bottom: 0.5rem;
            font-family: 'Inter', -apple-system, sans-serif;
        }}
        
        .subtitle {{
            font-size: 1.2rem;
            color: {theme_colors['text_secondary']} !important;
            margin-bottom: 2rem;
        }}
        
        /* FORCE Tab Background */
        [data-testid="stTabs"],
        .stTabs [data-baseweb="tab-list"],
        .stTabs [data-baseweb="tab-panel"] {{
            background-color: {theme_colors['background']} !important;
        }}
        
        /* FORCE Tab Text Color */
        .stTabs [data-baseweb="tab"] {{
            color: {theme_colors['text_primary']} !important;
        }}
        
        /* Cards */
        .metric-card {{
            background: {theme_colors['surface']} !important;
            color: {theme_colors['text_primary']} !important;
            padding: 1.5rem;
            border-radius: 0.75rem;
            border-left: 4px solid {theme_colors['accent']};
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }}
        
        .success-box {{
            background: {theme_colors['success']}22 !important;
            color: {theme_colors['text_primary']} !important;
            padding: 1.5rem;
            border-radius: 0.75rem;
            border-left: 4px solid {theme_colors['success']};
            margin: 1rem 0;
        }}
        
        .info-box {{
            background: {theme_colors['accent']}22 !important;
            color: {theme_colors['text_primary']} !important;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid {theme_colors['accent']};
        }}
        
        .warning-box {{
            background: {theme_colors['warning']}22 !important;
            color: {theme_colors['text_primary']} !important;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid {theme_colors['warning']};
        }}
        
        /* FORCE Streamlit Success/Info/Warning/Error Boxes - COMPREHENSIVE */
        .stAlert, 
        .stSuccess, 
        .stInfo, 
        .stWarning, 
        .stError,
        [data-testid="stNotification"],
        [data-testid="stAlert"] {{
            background-color: {theme_colors['surface']} !important;
            color: {theme_colors['text_primary']} !important;
            border-color: {theme_colors['border']} !important;
        }}
        
        /* Force Text Inside Alert Boxes - CRITICAL FIX */
        .stAlert *,
        .stSuccess *,
        .stInfo *,
        .stWarning *,
        .stError *,
        [data-testid="stNotification"] *,
        [data-testid="stAlert"] * {{
            color: {theme_colors['text_primary']} !important;
        }}
        
        /* White Background Insight Boxes - CRITICAL FIX FOR INSIGHTS TAB */
        div[style*="background: white"],
        div[style*="background:white"],
        div[style*="background-color: white"],
        div[style*="background-color:white"],
        div[style*="background: #FFFFFF"],
        div[style*="background-color: #FFFFFF"] {{
            background-color: {theme_colors['surface']} !important;
            color: {theme_colors['text_primary']} !important;
        }}
        
        div[style*="background: white"] *,
        div[style*="background:white"] *,
        div[style*="background-color: white"] *,
        div[style*="background-color:white"] *,
        div[style*="background: #FFFFFF"] *,
        div[style*="background-color: #FFFFFF"] * {{
            color: {theme_colors['text_primary']} !important;
        }}
        
        /* Buttons - COMPREHENSIVE OVERRIDE */
        .stButton > button {{
            border-radius: 0.5rem;
            font-weight: 500;
            transition: all 0.3s ease;
            color: {theme_colors['text_primary']} !important;
            background-color: {theme_colors['surface']} !important;
            border: 1px solid {theme_colors['border']} !important;
        }}
        
        /* Primary Button Override */
        .stButton > button[kind="primary"],
        .stButton > button[data-baseweb="button"][kind="primary"] {{
            background-color: {theme_colors['primary']} !important;
            color: white !important;
            border-color: {theme_colors['primary']} !important;
        }}
        
        /* Secondary Button Override - CRITICAL FIX */
        .stButton > button[kind="secondary"],
        .stButton > button[data-baseweb="button"][kind="secondary"] {{
            background-color: {theme_colors['surface']} !important;
            color: {theme_colors['text_primary']} !important;
            border: 1px solid {theme_colors['border']} !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        /* Metrics */
        [data-testid="stMetricValue"] {{
            font-size: 2rem;
            font-weight: 700;
            color: {theme_colors['primary']} !important;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: {theme_colors['text_secondary']} !important;
        }}
        
        /* FORCE File Uploader - COMPREHENSIVE */
        [data-testid="stFileUploader"],
        [data-testid="stFileUploader"] section,
        [data-testid="stFileUploader"] > div,
        .uploadedFile {{
            background-color: {theme_colors['surface']} !important;
            color: {theme_colors['text_primary']} !important;
            border-color: {theme_colors['border']} !important;
        }}
        
        /* File Uploader "Browse files" Button - CRITICAL FIX */
        [data-testid="stFileUploader"] button,
        [data-testid="stFileUploader"] button span {{
            background-color: {theme_colors['primary']} !important;
            color: white !important;
            border-color: {theme_colors['primary']} !important;
        }}
        
        /* Uploaded File Name Display - CRITICAL FIX for Issue #3 */
        .uploadedFileName,
        .uploadedFile,
        [data-testid="stFileUploader"] small,
        [data-testid="stFileUploader"] .stMarkdown,
        [data-testid="stFileUploader"] span,
        [data-testid="stFileUploader"] label,
        [data-testid="stFileUploader"] p,
        [data-testid="stFileUploader"] div[data-testid="stMarkdownContainer"],
        [data-testid="stFileUploadDropzone"] span,
        [data-testid="stFileUploadDropzone"] p {{
            color: {theme_colors['text_primary']} !important;
            font-weight: 500 !important;
        }}
        
        /* File Uploader Helper Text */
        [data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] {{
            color: {theme_colors['text_secondary']} !important;
        }}
        
        /* FORCE Text Input - COMPREHENSIVE */
        .stTextInput input,
        .stTextArea textarea,
        [data-baseweb="input"],
        [data-baseweb="textarea"] {{
            background-color: {theme_colors['surface']} !important;
            color: {theme_colors['text_primary']} !important;
            border-color: {theme_colors['border']} !important;
        }}
        
        /* Placeholder Text - CRITICAL FIX */
        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder,
        [data-baseweb="input"]::placeholder,
        [data-baseweb="textarea"]::placeholder {{
            color: {theme_colors['text_secondary']} !important;
            opacity: 0.7 !important;
        }}
        
        /* Text Input Labels */
        .stTextInput label,
        .stTextArea label {{
            color: {theme_colors['text_primary']} !important;
        }}
        
        /* Tables */
        .dataframe {{
            background-color: {theme_colors['surface']} !important;
            color: {theme_colors['text_primary']} !important;
            border: 1px solid {theme_colors['border']};
            border-radius: 0.5rem;
        }}
        
        /* FORCE Expander Headers - COMPREHENSIVE */
        .streamlit-expanderHeader,
        [data-testid="stExpander"],
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] > div > div > div {{
            background-color: {theme_colors['surface']} !important;
            color: {theme_colors['text_primary']} !important;
            border-radius: 0.5rem;
        }}
        
        /* Expander Header Text - CRITICAL FIX for Issue #4 */
        .streamlit-expanderHeader p,
        .streamlit-expanderHeader span,
        [data-testid="stExpander"] summary p,
        [data-testid="stExpander"] summary span,
        [data-testid="stExpander"] [data-testid="stMarkdownContainer"] p {{
            color: {theme_colors['text_primary']} !important;
            font-weight: 600 !important;
        }}
        
        /* Expander Content */
        [data-testid="stExpander"] [data-testid="stMarkdownContainer"] {{
            color: {theme_colors['text_primary']} !important;
        }}
        
        /* Professional number formatting */
        .formatted-number {{
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-weight: 600;
            color: {theme_colors['text_primary']} !important;
        }}
        
        /* Logo container */
        .logo-container {{
            padding: 1rem;
            text-align: center;
            margin-bottom: 1rem;
            background-color: {theme_colors['surface']} !important;
        }}
        
        /* Language selector */
        .language-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            background: {theme_colors['accent']};
            color: white !important;
            border-radius: 1rem;
            font-size: 0.875rem;
            font-weight: 500;
            margin: 0.25rem;
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .language-badge:hover {{
            transform: scale(1.05);
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }}
        
        /* FORCE All Markdown Text */
        .stMarkdown, .stMarkdown p, .stMarkdown span {{
            color: {theme_colors['text_primary']} !important;
        }}
        
        /* FORCE Radio Buttons */
        .stRadio label,
        .stRadio > label > div {{
            color: {theme_colors['text_primary']} !important;
        }}
        
        /* FORCE Selectbox */
        .stSelectbox label,
        .stSelectbox div,
        [data-baseweb="select"] {{
            color: {theme_colors['text_primary']} !important;
        }}
        
        /* Captions and Helper Text - COMPREHENSIVE */
        .stCaption,
        [data-testid="stCaptionContainer"],
        small,
        .caption-text {{
            color: {theme_colors['text_secondary']} !important;
        }}
        
        /* Empty State Messages - CRITICAL FIX FOR DASHBOARD TAB */
        .element-container p,
        [data-testid="stMarkdownContainer"] p {{
            color: {theme_colors['text_primary']} !important;
        }}
        
        /* Links */
        a, a:visited {{
            color: {theme_colors['accent']} !important;
        }}
        
        a:hover {{
            color: {theme_colors['primary']} !important;
        }}
        
        /* Dividers */
        hr, .stDivider {{
            border-color: {theme_colors['border']} !important;
        }}
        
        /* Checkbox */
        .stCheckbox label {{
            color: {theme_colors['text_primary']} !important;
        }}
        
        /* Download Button */
        [data-testid="stDownloadButton"] button {{
            background-color: {theme_colors['accent']} !important;
            color: white !important;
        }}
        
        /* Spinner Container - CRITICAL FIX for Issue #1 */
        [data-testid="stSpinner"],
        [data-testid="stSpinner"] > div,
        .stSpinner,
        .stSpinner > div {{
            background-color: {theme_colors['background']} !important;
            color: {theme_colors['text_primary']} !important;
        }}
        
        /* Spinner Text */
        [data-testid="stSpinner"] p,
        [data-testid="stSpinner"] span,
        .stSpinner p,
        .stSpinner span {{
            color: {theme_colors['text_primary']} !important;
        }}
    </style>
    """

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="DataAnalytics Vietnam - AI-Powered Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://dataanalytics.vn/help',
        'Report a bug': 'https://dataanalytics.vn/support',
        'About': 'DataAnalytics Vietnam - Professional BI for Vietnamese SMEs'
    }
)

# Initialize session state
initialize_session_state()

# Apply theme CSS
st.markdown(get_theme_css(st.session_state['theme']), unsafe_allow_html=True)

# ============================================
# GEMINI CLIENT
# ============================================
@st.cache_resource
def get_gemini_client():
    """Initialize Gemini client with caching"""
    try:
        import google.generativeai as genai
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            lang = st.session_state.get('language', 'vi')
            error_msg = "❌ GEMINI_API_KEY not found. Please add to .env file" if lang == 'en' else "❌ Chưa có GEMINI_API_KEY. Vui lòng thêm vào file .env"
            st.error(error_msg)
            st.stop()
        
        genai.configure(api_key=api_key)
        return genai
    
    except Exception as e:
        lang = st.session_state.get('language', 'vi')
        error_msg = f"❌ Gemini API connection error: {str(e)}" if lang == 'en' else f"❌ Lỗi kết nối Gemini API: {str(e)}"
        st.error(error_msg)
        st.stop()

# ============================================
# UTILITY FUNCTIONS
# ============================================
def format_kpi_value(value: float, kpi_name: str, lang: str = 'vi', currency: str = 'VND') -> str:
    """
    Format KPI value with proper thousand separators and currency conversion
    
    Args:
        value: Numeric value
        kpi_name: Name of KPI to determine formatting
        lang: Language code
        currency: Currency preference
    
    Returns:
        Formatted string
    """
    # Detect if this is a percentage KPI
    is_percentage = any(keyword in kpi_name for keyword in ['%', 'Rate', 'CTR', 'Conversion', 'Percentage'])
    
    # Detect if this is a currency KPI (VND) - IMPROVED DETECTION for Issue #2
    is_currency = any(keyword in kpi_name for keyword in [
        'Revenue', 'Cost', 'Sales', 'Price', 'VND', 'Spend', 'CPA', 'CPC', 'CPM',
        'Doanh Thu', 'Chi Phí', 'Value', 'Amount', 'Total', 'Average'
    ])
    
    # CRITICAL FIX Issue #2: Percentage KPIs should NOT have thousand separators in the % value
    # But if it's "Conversion Rate (%)" we want just the number with %, not formatted
    if is_percentage and '%' in kpi_name:
        # For percentage KPIs with explicit % in name, return plain value with %
        # Example: "CTR (%): 3.5" should be "3.5%" NOT "3,5%" or "3.5%"
        decimals = 1 if value < 10 else 1
        return f"{value:.{decimals}f}%"
    elif is_percentage:
        # For rate KPIs without % in name (e.g., "Conversion Rate")
        return f"{format_number(value, lang, 1)}%"
    elif is_currency and currency == 'USD' and lang == 'en':
        # Convert VND to USD for English mode with thousand separators
        usd_value = convert_vnd_to_usd(value)
        return format_currency(usd_value, 'USD', lang, 2)
    elif is_currency:
        # Display as VND with thousand separators - CRITICAL for Issue #2
        return format_currency(value, 'VND', lang, 0)
    else:
        # Regular number with thousand separators - CRITICAL for Issue #2
        decimals = 0 if value > 100 else 1
        return format_number(value, lang, decimals)

def get_data_quality_guide(lang='vi'):
    """Get data quality guide content"""
    return get_text('data_guide_content', lang)

# ============================================
# MAIN APP
# ============================================
def main():
    """Main application function"""
    
    lang = st.session_state['language']
    theme = st.session_state['theme']
    currency = st.session_state['currency']
    
    # ============================================
    # SIDEBAR
    # ============================================
    with st.sidebar:
        # Logo
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        logo_svg = get_logo_svg(variant='dark' if theme == 'dark' else 'light')
        st.markdown(logo_svg, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Settings Section
        st.markdown(f"### {get_text('settings', lang)}")
        
        # Language Selector
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🇻🇳 Tiếng Việt", use_container_width=True, type="primary" if lang == 'vi' else "secondary"):
                st.session_state['language'] = 'vi'
                st.rerun()
        
        with col2:
            if st.button("🇬🇧 English", use_container_width=True, type="primary" if lang == 'en' else "secondary"):
                st.session_state['language'] = 'en'
                st.rerun()
        
        # Theme Selector
        st.markdown(f"**{get_text('theme', lang)}**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(get_text('light_mode', lang), use_container_width=True, type="primary" if theme == 'light' else "secondary"):
                st.session_state['theme'] = 'light'
                st.rerun()
        
        with col2:
            if st.button(get_text('dark_mode', lang), use_container_width=True, type="primary" if theme == 'dark' else "secondary"):
                st.session_state['theme'] = 'dark'
                st.rerun()
        
        # Currency Selector (for English mode)
        if lang == 'en':
            st.markdown(f"**{get_text('currency_display', lang)}**")
            currency_option = st.radio(
                "",
                ['VND', 'USD'],
                index=0 if currency == 'VND' else 1,
                label_visibility="collapsed"
            )
            if currency_option != st.session_state['currency']:
                st.session_state['currency'] = currency_option
                st.rerun()
        
        st.markdown("---")
        
        # Premium Features
        st.markdown(f"### {get_text('premium_features', lang)}")
        st.markdown(f"""
        ✅ {get_text('iso_compliance', lang)}
        
        ✅ {get_text('domain_expertise', lang)}
        
        ✅ {get_text('data_lineage', lang)}
        
        ✅ {get_text('industry_benchmarks', lang)}
        
        ✅ {get_text('vietnamese_native', lang)}
        """)
        
        st.markdown("---")
        
        # Pricing
        st.markdown(f"### {get_text('pricing', lang)}")
        st.success(f"""
        {get_text('free_plan', lang)}
        
        {get_text('pro_plan', lang)}
        {get_text('pro_features', lang)}
        """)
        
        st.markdown("---")
        
        # Data Quality Guide
        with st.expander(get_text('data_guide_title', lang), expanded=False):
            st.markdown(get_data_quality_guide(lang))
        
        st.markdown("---")
        st.caption(get_text('app_tagline', lang))
    
    # ============================================
    # HEADER
    # ============================================
    st.markdown(f'<div class="main-header">📊 DataAnalytics Vietnam</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{get_text("app_subtitle", lang)}</div>', unsafe_allow_html=True)
    
    # ============================================
    # MAIN TABS
    # ============================================
    tab1, tab2, tab3 = st.tabs([
        get_text('tab_upload', lang),
        get_text('tab_dashboard', lang),
        get_text('tab_insights', lang)
    ])
    
    # ============================================
    # TAB 1: UPLOAD & ANALYZE
    # ============================================
    with tab1:
        st.markdown(f"### {get_text('upload_title', lang)}")
        
        # Instructions
        with st.expander(get_text('instructions_title', lang), expanded=False):
            st.markdown(get_text('instructions_content', lang))
        
        # File upload
        uploaded_file = st.file_uploader(
            get_text('choose_file', lang),
            type=['csv', 'xlsx', 'xls'],
            help=get_text('file_help', lang)
        )
        
        # Display uploaded filename explicitly for better UX
        if uploaded_file is not None:
            file_size_kb = uploaded_file.size / 1024
            if file_size_kb < 1024:
                size_str = f"{file_size_kb:.1f}KB"
            else:
                size_str = f"{file_size_kb / 1024:.1f}MB"
            
            st.success(f"📎 **{uploaded_file.name}** ({size_str})")
        
        # Dataset description
        dataset_description = st.text_area(
            get_text('dataset_description', lang),
            placeholder=get_text('dataset_placeholder', lang),
            help=get_text('dataset_help', lang)
        )
        
        # Analyze button
        if uploaded_file:
            col1, col2 = st.columns([1, 3])
            with col1:
                analyze_button = st.button(get_text('analyze_button', lang), type="primary", use_container_width=True)
            with col2:
                st.caption(get_text('time_estimate', lang))
        
        # Process file
        if uploaded_file and 'analyze_button' in locals() and analyze_button:
            # Load file
            with st.spinner(get_text('loading_file', lang)):
                success, df, message = safe_file_upload(uploaded_file, max_size_mb=200)
            
            if not success:
                st.error(message)
                st.stop()
            
            st.success(message)
            
            # Display data preview
            with st.expander(get_text('preview_data', lang), expanded=False):
                st.dataframe(df.head(10), use_container_width=True)
                st.caption(get_text('shape_info', lang).format(rows=df.shape[0], cols=df.shape[1]))
            
            # Run pipeline
            st.markdown("---")
            st.markdown(f"### {get_text('processing', lang)}")
            
            # Initialize pipeline
            gemini_client = get_gemini_client()
            pipeline = PremiumLeanPipeline(gemini_client)
            
            # Run pipeline with progress
            result = pipeline.run_pipeline(df, dataset_description)
            
            # Check result
            if not result['success']:
                st.error(f"❌ {get_text('error', lang) if lang == 'en' else 'Lỗi'}: {result['error']}")
                st.stop()
            
            # Save to session state
            st.session_state['result'] = result
            st.session_state['df'] = df
            
            # Success message
            st.balloons()
            
            total_time = result['performance']['total']
            quality_score = result['quality_scores']['overall']
            
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown(f"""
            ### {get_text('success_title', lang)}
            
            {get_text('success_time', lang).format(time=total_time)}
            
            {get_text('success_quality', lang).format(score=quality_score)}
            
            {get_text('success_charts', lang).format(count=len(result['dashboard']['charts']))}
            
            {get_text('success_insights', lang).format(count=len(result['insights']['key_insights']), expert=result['domain_info']['expert_role'][:50])}
            
            {get_text('success_next', lang)}
            """)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ============================================
    # TAB 2: DASHBOARD
    # ============================================
    with tab2:
        st.markdown(f"### {get_text('dashboard_title', lang)}")
        
        if 'result' not in st.session_state or st.session_state['result'] is None:
            st.info(get_text('upload_prompt', lang))
            st.stop()
        
        result = st.session_state['result']
        
        # Display domain info
        domain_info = result['domain_info']
        st.markdown(get_text('industry', lang).format(
            domain=domain_info['domain_name'],
            expert=domain_info['expert_role'][:60]
        ))
        
        # Display KPIs
        st.markdown(f"#### {get_text('kpis_title', lang)}")
        kpis = result['dashboard'].get('kpis', {})
        
        if kpis:
            # ⭐ VALIDATION: Check for suspicious KPI values
            validation_warnings = []
            for kpi_name, kpi_data in kpis.items():
                value = kpi_data.get('value', 0)
                
                # CTR should be 0-100% (percentage)
                if 'CTR' in kpi_name and '(%)' in kpi_name:
                    if value > 100:
                        validation_warnings.append(f"⚠️ {kpi_name} = {value:.1f} (Should be 0-100%). Possible unit error.")
                    elif value > 50:
                        validation_warnings.append(f"⚠️ {kpi_name} = {value:.1f}% (Unusually high, verify data).")
                
                # Conversion Rate should be 0-100%
                if 'Conversion Rate' in kpi_name and '(%)' in kpi_name:
                    if value > 100:
                        validation_warnings.append(f"⚠️ {kpi_name} = {value:.1f} (Should be 0-100%). Possible unit error.")
                
                # ROAS should be reasonable (typically 0-20)
                if 'ROAS' in kpi_name:
                    if value > 100:
                        validation_warnings.append(f"⚠️ {kpi_name} = {value:.1f} (Unusually high, verify calculation).")
            
            # Show validation warnings if any
            if validation_warnings:
                with st.expander(get_text('data_quality_warnings', lang), expanded=False):
                    for warning in validation_warnings:
                        st.warning(warning)
            
            # Define KPIs where LOWER is BETTER (reverse color logic)
            lower_is_better_kpis = [
                'Defect Rate', 'Downtime', 'Cost per Unit', 'Avg Downtime',
                'Total Downtime', 'Cost', 'Churn Rate', 'Error Rate'
            ]
            
            cols = st.columns(min(4, len(kpis)))
            for i, (kpi_name, kpi_data) in enumerate(list(kpis.items())[:12]):
                with cols[i % 4]:
                    # Check if this is a "lower is better" KPI
                    is_lower_better = any(keyword in kpi_name for keyword in lower_is_better_kpis)
                    
                    # Reverse logic for "lower is better" KPIs
                    if is_lower_better:
                        delta_color = "inverse" if kpi_data.get('status') == 'Above' else "normal"
                    else:
                        delta_color = "normal" if kpi_data.get('status') == 'Above' else "inverse"
                    
                    # Format value with thousand separators and currency conversion
                    # CRITICAL: Convert to float in case Gemini returns string
                    try:
                        kpi_value = float(kpi_data['value'])
                    except (ValueError, TypeError):
                        kpi_value = kpi_data['value']  # Keep as-is if conversion fails
                    
                    formatted_value = format_kpi_value(kpi_value, kpi_name, lang, currency)
                    
                    st.metric(
                        label=kpi_name,
                        value=formatted_value,
                        delta=kpi_data.get('status', ''),
                        delta_color=delta_color
                    )
                    
                    # Format benchmark
                    benchmark_value = kpi_data.get('benchmark', 'N/A')
                    if benchmark_value != 'N/A' and isinstance(benchmark_value, (int, float)):
                        benchmark_formatted = format_kpi_value(benchmark_value, kpi_name, lang, currency)
                    else:
                        benchmark_formatted = benchmark_value
                    
                    st.caption(get_text('benchmark', lang).format(value=benchmark_formatted))
        
        # Display charts
        st.markdown("---")
        st.markdown(f"#### {get_text('charts_title', lang)}")
        
        charts = result['dashboard']['charts']
        
        if len(charts) == 0:
            st.warning(get_text('no_charts', lang))
        else:
            # Display charts in 2 columns
            for i in range(0, len(charts), 2):
                col1, col2 = st.columns(2)
                
                with col1:
                    if i < len(charts):
                        st.plotly_chart(charts[i]['figure'], use_container_width=True, key=f"chart_{i}")
                
                with col2:
                    if i + 1 < len(charts):
                        st.plotly_chart(charts[i+1]['figure'], use_container_width=True, key=f"chart_{i+1}")
        
        # Export options
        st.markdown("---")
        st.markdown(f"#### {get_text('export_title', lang)}")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button(get_text('export_pdf', lang), use_container_width=True):
                if EXPORT_AVAILABLE:
                    try:
                        with st.spinner("🔄 Generating PDF..."):
                            pdf_bytes = export_to_pdf(result, st.session_state['df'], lang)
                        
                        # Offer download
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=pdf_bytes,
                            file_name=f"DataAnalytics_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                        st.success("✅ PDF ready for download!")
                    except Exception as e:
                        st.error(f"❌ PDF generation failed: {str(e)}")
                else:
                    st.info(get_text('feature_coming', lang))
        
        with col2:
            if st.button(get_text('export_ppt', lang), use_container_width=True):
                if EXPORT_AVAILABLE:
                    try:
                        with st.spinner("🔄 Generating PowerPoint..."):
                            ppt_bytes = export_to_powerpoint(result, st.session_state['df'], lang)
                        
                        # Offer download
                        st.download_button(
                            label="⬇️ Download PPT",
                            data=ppt_bytes,
                            file_name=f"DataAnalytics_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            use_container_width=True
                        )
                        st.success("✅ PowerPoint ready for download!")
                    except Exception as e:
                        st.error(f"❌ PowerPoint generation failed: {str(e)}")
                else:
                    st.info(get_text('feature_coming', lang))
        
        with col3:
            if st.button(get_text('export_data', lang), use_container_width=True):
                csv = st.session_state['df'].to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=get_text('download_csv', lang),
                    data=csv,
                    file_name=f'cleaned_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                    mime='text/csv',
                    use_container_width=True
                )
        
        with col4:
            if st.button("📧 Share via Email", use_container_width=True):
                st.info(get_text('feature_coming', lang))
    
    # ============================================
    # TAB 3: INSIGHTS
    # ============================================
    with tab3:
        st.markdown(f"### {get_text('insights_title', lang)}")
        
        if 'result' not in st.session_state or st.session_state['result'] is None:
            st.info(get_text('upload_prompt', lang))
            st.stop()
        
        result = st.session_state['result']
        insights = result['insights']
        domain_info = result['domain_info']
        
        # Expert info
        st.markdown(get_text('perspective', lang).format(expert=domain_info['expert_role']))
        st.markdown(get_text('industry_label', lang).format(domain=domain_info['domain_name']))
        
        # Executive summary
        st.markdown("---")
        st.markdown(f"#### {get_text('executive_summary', lang)}")
        st.info(insights.get('executive_summary', get_text('no_summary', lang)))
        
        # Key insights
        st.markdown("---")
        st.markdown(f"#### {get_text('key_insights', lang)}")
        
        for insight in insights.get('key_insights', []):
            impact_emoji = "🔴" if insight['impact'] == 'high' else "🟡" if insight['impact'] == 'medium' else "🟢"
            
            with st.expander(f"{impact_emoji} {insight['title']}", expanded=True):
                st.markdown(insight['description'])
                st.caption(get_text('impact', lang).format(level=insight['impact'].upper()))
        
        # Recommendations
        st.markdown("---")
        st.markdown(f"#### {get_text('recommendations', lang)}")
        
        for rec in insights.get('recommendations', []):
            priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
            
            st.success(f"""
            {priority_emoji} **[{rec['priority'].upper()}] {rec['action']}**
            
            {get_text('expected_impact', lang).format(impact=rec['expected_impact'])}
            
            {get_text('timeline', lang).format(time=rec['timeline'])}
            """)
        
        # Risk alerts
        if insights.get('risk_alerts'):
            st.markdown("---")
            st.markdown(f"#### {get_text('risk_alerts', lang)}")
            
            for risk in insights['risk_alerts']:
                severity_emoji = "🔴" if risk['severity'] == 'high' else "🟡" if risk['severity'] == 'medium' else "🟢"
                st.warning(f"{severity_emoji} **{risk['risk']}** ({get_text('severity', lang).format(level=risk['severity'])})")
        
        # Quality badge
        st.markdown("---")
        st.markdown(f"#### {get_text('quality_assurance', lang)}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(get_text('quality_score', lang), f"{result['quality_scores']['overall']:.0f}/100")
            st.caption(get_text('iso_compliant', lang))
        
        with col2:
            st.metric(get_text('data_cleaning', lang), f"{result['quality_scores']['cleaning']:.0f}/100")
            st.caption(get_text('cleaning_note', lang))
        
        with col3:
            st.metric(get_text('blueprint_quality', lang), f"{result['quality_scores']['blueprint']:.0f}/100")
            st.caption(get_text('blueprint_note', lang))


# ============================================
# RUN APP
# ============================================
if __name__ == "__main__":
    main()
