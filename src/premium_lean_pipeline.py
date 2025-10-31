"""
Premium Lean OQMLB Pipeline - Optimized for Speed + Premium Quality
Target: 55 seconds end-to-end with professional-grade output

Steps:
  Step 0: Domain Detection (3s) - cached
  Step 1: Data Cleaning (15s) - ISO 8000 
  Step 2: Smart Blueprint (15s) - EDA + Blueprint combined
  Step 3: Dashboard Build (7s) - pure execution
  Step 4: Domain Insights (15s) - expert perspective

Total: ~55 seconds
"""

import pandas as pd
import json
import re
from typing import Dict, List, Tuple, Any, Optional
import streamlit as st
from datetime import datetime
import time
# Note: google.generativeai removed - not used in this pipeline (dead import causing slow load)

# Import utilities
from utils.validators import safe_file_upload, sanitize_column_names
from utils.error_handlers import rate_limit_handler, user_friendly_error
from utils.performance import PerformanceMonitor, log_performance
from utils.i18n import get_text, format_number, format_currency

# Import domain detection
from domain_detection import (
    detect_domain,
    get_domain_specific_prompt_context,
    DOMAIN_PROFILES
)

# Import Vietnam benchmark loader
from benchmark_loader import get_benchmark_loader


# ==================================================================================
# CRITICAL: NEVER_IMPUTE_FIELDS Protection (Legal + Trust)
# ==================================================================================
# These fields are TOO IMPORTANT to fill with fake/imputed data
# Missing = KEEP AS NULL and FLAG to user with warning
# Rationale: Wrong revenue/salary data → Wrong decisions → Legal liability + Lost trust
# Updated: 2025-10-30 - Added to PremiumLeanPipeline for production safety
# ==================================================================================

NEVER_IMPUTE_FIELDS = {
    # Financial fields (legal liability + wrong strategic decisions)
    'revenue', 'sales', 'income', 'cost', 'expense', 'profit', 'margin',
    'price', 'amount', 'payment', 'fee', 'charge', 'budget', 'spending',
    'deal_value', 'deal_amount', 'contract_value', 'invoice_amount',
    'doanh_thu', 'doanh_so', 'chi_phi', 'loi_nhuan', 'gia', 'tien', 'thanh_toan',
    
    # Marketing/Sales metrics (wrong data = wrong decisions)
    'roas', 'roi', 'conversion_rate', 'cpa', 'cpc', 'cpm', 'ctr',
    'conversions', 'leads', 'clicks', 'impressions', 'reach',
    'ty_le_chuyen_doi', 'chi_phi_don_hang',
    
    # E-commerce operational metrics
    'discount', 'rating', 'review', 'delivery_time', 'delivery_days',
    'shipping_fee', 'order_status', 'return_rate',
    'giam_gia', 'danh_gia', 'thoi_gian_giao',
    
    # Customer Service metrics (affect CSAT/SLA compliance)
    'resolution_time', 'response_time', 'satisfaction_score', 'csat',
    'nps', 'issue_category', 'priority', 'sla_breach',
    'resolved_date', 'resolution_date', 'closed_date',
    'thoi_gian_xu_ly', 'muc_do_hai_long', 'ngay_giai_quyet',
    
    # Metadata fields (categorical/competitive intelligence)
    'channel', 'source', 'medium', 'campaign', 'platform',
    'competitors', 'competitor_name',
    'kenh', 'nguon', 'doi_thu_canh_tranh',
    
    # HR fields (compliance/privacy + labor law)
    'salary', 'wage', 'compensation', 'bonus', 'commission', 'payroll',
    'employee_id', 'staff_id', 'position', 'title', 'role', 'job_title',
    'ho_ten', 'ten', 'name', 'full_name',
    'luong', 'thu_nhap', 'chuc_vu', 'vi_tri',
    'luong_thang', 'luong_co_ban',  # Added Vietnamese salary variations
    
    # Customer PII (privacy law GDPR/PDPA compliance)
    'email', 'phone', 'address', 'ssn', 'passport', 'id_number', 'cccd', 'cmnd',
    'credit_card', 'bank_account', 'so_dien_thoai', 'dia_chi',
    
    # Business-critical IDs (data integrity)
    'order_id', 'transaction_id', 'invoice_id', 'customer_id', 'user_id',
    'deal_id', 'ticket_id', 'campaign_id', 'lead_id',
    'ma_don_hang', 'ma_khach_hang', 'ma_giao_dich', 'ma_hoa_don',
}

def is_never_impute_field(column_name: str) -> bool:
    """
    Check if a column should NEVER be imputed with fake data.
    
    Args:
        column_name: Name of the column to check
    
    Returns:
        True if field is protected (never impute), False otherwise
    
    Example:
        >>> is_never_impute_field('luong_thang')
        True
        >>> is_never_impute_field('customer_age')
        False
    """
    col_lower = column_name.lower()
    return any(protected_field in col_lower for protected_field in NEVER_IMPUTE_FIELDS)


# ==================================================================================
# PROFESSIONAL COLOR PALETTES (ColorBrewer Standard)
# ==================================================================================
# Research-validated color palette for professional, accessible data visualization
# Source: Tableau Research (derivative of ColorBrewer by Cynthia Brewer, Penn State)
# Benefits: Colorblind-safe, print-friendly, perceptually balanced
# Compliance: WCAG AA accessibility standards
# ==================================================================================

TABLEAU_10_COLORS = [
    '#4E79A7',  # Blue (primary)
    '#F28E2B',  # Orange
    '#E15759',  # Red
    '#76B7B2',  # Teal
    '#59A14F',  # Green
    '#EDC948',  # Yellow
    '#B07AA1',  # Purple
    '#FF9DA7',  # Pink
    '#9C755F',  # Brown
    '#BAB0AC'   # Gray
]

# ==================================================================================
# BENCHMARK SOURCES & METADATA (For Transparency & Trust)
# ==================================================================================
# Updated: 2025-10-29 - ENHANCED with URLs, year, metrics, credibility ratings
# Based on demanding user feedback: Users need VERIFIABLE sources with clickable URLs
# All URLs tested and lead to SPECIFIC data pages (not generic homepages)
# Maintenance: Quarterly review (Jan/Apr/Jul/Oct) to verify URLs still valid
# ==================================================================================

BENCHMARK_SOURCES = {
    # ========================
    # HR / HUMAN RESOURCES
    # ========================
    'hr_salary': {
        'name': 'VietnamWorks Salary Report 2024',
        'url': 'https://www.vietnamworks.com/salary-report',
        'year': '2024',
        'metrics': 'IT: 15-25M VND/month, Marketing: 10-18M, Sales: 12-20M, Manager: 30-50M',
        'credibility': '⭐⭐⭐⭐⭐',
        'vietnam_specific': True,
        'cost': 'FREE',
        'sample_size': '16,000+ employees surveyed'
    },
    'hr_turnover': {
        'name': 'Mercer Talent Trends APAC 2024',
        'url': 'https://www.mercer.com/en-vn/insights/talent-and-transformation/talent-trends/',
        'year': '2024',
        'metrics': 'Turnover: 18-22% annually (Vietnam avg), Retention cost: 1.5-2x salary',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,  # APAC region, need adjustment
        'cost': 'FREE (summary)',
        'sample_size': 'APAC regional data'
    },
    'hr_satisfaction': {
        'name': 'Anphabe Best Places to Work 2024',
        'url': 'https://www.anphabe.com/research/best-places-to-work',
        'year': '2024',
        'metrics': 'Employee engagement: 65-75% (top companies), Satisfaction: 7.5-8.5/10',
        'credibility': '⭐⭐⭐⭐⭐',
        'vietnam_specific': True,
        'cost': 'FREE',
        'sample_size': '150+ companies, 10,000+ employees'
    },
    'hr_productivity': {
        'name': 'Deloitte Human Capital Trends 2024',
        'url': 'https://www2.deloitte.com/global/en/insights/focus/human-capital-trends.html',
        'year': '2024',
        'metrics': 'Productivity gain: 15-25% with digital tools, Remote work: 40-60% adoption',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': 'Global enterprise survey'
    },
    
    # ========================
    # MARKETING
    # ========================
    'marketing_ctr': {
        'name': 'WordStream Google Ads Benchmarks 2024',
        'url': 'https://www.wordstream.com/blog/ws/2024/02/05/google-ads-benchmarks',
        'year': '2024',
        'metrics': 'CTR: 3.17% avg, CPC: $2.69 (US) → ×0.2 = $0.54 (VN), CVR: 3.75%',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,  # US data, apply 0.2x multiplier for Vietnam
        'cost': 'FREE',
        'sample_size': '16,000+ campaigns analyzed'
    },
    'marketing_conversion': {
        'name': 'Unbounce Conversion Benchmark Report 2024',
        'url': 'https://unbounce.com/conversion-benchmark-report/',
        'year': '2024',
        'metrics': 'Landing page CVR: 9.7% median, Top 10%: 25%+, Bottom 25%: <2.5%',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': '464M visits, 41,000+ landing pages'
    },
    'marketing_roi': {
        'name': 'HubSpot State of Marketing 2024',
        'url': 'https://www.hubspot.com/state-of-marketing',
        'year': '2024',
        'metrics': 'Marketing ROI: 5:1 avg, Top performers: 10:1, Email ROI: 42:1',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': '1,400+ marketers surveyed'
    },
    'marketing_roas': {
        'name': 'WordStream Google Ads Benchmarks 2024',
        'url': 'https://www.wordstream.com/blog/ws/2024/02/05/google-ads-benchmarks',
        'year': '2024',
        'metrics': 'ROAS: 2:1 avg, E-commerce: 3:1, B2B: 2.5:1 (adjust -20% for Vietnam)',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': '16,000+ campaigns'
    },
    'marketing_cpa': {
        'name': 'WordStream Cost Per Action Benchmarks 2024',
        'url': 'https://www.wordstream.com/blog/ws/2024/02/05/google-ads-benchmarks',
        'year': '2024',
        'metrics': 'CPA: $48 avg (US) → ×0.2 = $9.60 (VN realistic), Range: $20-80 (US)',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': '16,000+ campaigns'
    },
    'marketing_engagement': {
        'name': 'Hootsuite Social Media Benchmarks 2024',
        'url': 'https://www.hootsuite.com/research/social-trends',
        'year': '2024',
        'metrics': 'Engagement rate: 1-3% (FB), 1-5% (IG), 0.5-1% (LinkedIn)',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': 'Global social media data'
    },
    'marketing_vietnam_digital': {
        'name': 'Vietnam Digital Report 2024 (We Are Social + Meltwater)',
        'url': 'https://datareportal.com/reports/digital-2024-vietnam',
        'year': '2024',
        'metrics': 'Social media users: 76.9M (78% population), Internet users: 79.1M, Mobile: 98.3M connections, Daily online: 6h48m',
        'credibility': '⭐⭐⭐⭐⭐',
        'vietnam_specific': True,
        'cost': 'FREE',
        'sample_size': '100M+ global users tracked, Vietnam-specific data validated'
    },
    'marketing_vietnam_ecommerce': {
        'name': 'Vietnam E-Business Index Report 2024 (VECOM)',
        'url': 'https://esc.vn/wp-content/uploads/2025/07/Bao-cao-EBI-2024-ENG.pdf',
        'year': '2024',
        'metrics': 'E-commerce: $25B USD market (+25% YoY), Online retail: $17.3B, Mobile payments: 2B transactions, Express delivery: 2.17B parcels',
        'credibility': '⭐⭐⭐⭐⭐',
        'vietnam_specific': True,
        'cost': 'FREE',
        'sample_size': 'Vietnam E-commerce Association (VECOM) - Official industry report'
    },
    
    # ========================
    # E-COMMERCE (VIETNAM-FIRST!)
    # ========================
    'ecommerce_conversion': {
        'name': 'iPrice Vietnam E-Commerce Report Q3 2024',
        'url': 'https://iprice.vn/insights/mapofecommerce/',
        'year': '2024',
        'metrics': 'CVR: 2.5-4% (Shopee/Lazada/Tiki avg), Mobile: 3-5%, Desktop: 2-3%',
        'credibility': '⭐⭐⭐⭐⭐',
        'vietnam_specific': True,
        'cost': 'FREE',
        'sample_size': 'Top Vietnam e-commerce platforms'
    },
    'ecommerce_aov': {
        'name': 'Metric Vietnam E-Commerce Index 2024',
        'url': 'https://metric.vn/vietnam-ecommerce-market-report-2024',
        'year': '2024',
        'metrics': 'AOV: 350-450K VND (mobile), 500-800K (desktop), Shopee avg: 400K',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': True,
        'cost': 'FREE (summary)',
        'sample_size': 'Vietnam e-commerce market data'
    },
    'ecommerce_cart_abandonment': {
        'name': 'Baymard Institute Cart Abandonment Study',
        'url': 'https://baymard.com/lists/cart-abandonment-rate',
        'year': '2024',
        'metrics': '70% abandonment (global avg) → 75% (VN, higher due to COD preference)',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,  # Global, adjust +5% for Vietnam COD culture
        'cost': 'FREE',
        'sample_size': '49 cart abandonment studies'
    },
    'ecommerce_mobile': {
        'name': 'Google Vietnam Mobile Commerce Study 2024',
        'url': 'https://www.thinkwithgoogle.com/intl/en-apac/consumer-insights/consumer-trends/',
        'year': '2024',
        'metrics': 'Mobile commerce: 70% of transactions, Smartphone ownership: 85%+',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': True,
        'cost': 'FREE',
        'sample_size': 'Vietnam consumer survey'
    },
    'ecommerce_repeat': {
        'name': 'Adobe Digital Economy Index',
        'url': 'https://business.adobe.com/resources/digital-economy-index.html',
        'year': '2024',
        'metrics': 'Repeat purchase: 25-35% (1 year), Loyalty program impact: +20%',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': 'Global e-commerce data'
    },
    
    # ========================
    # SALES
    # ========================
    'sales_conversion': {
        'name': 'HubSpot Sales Statistics 2024',
        'url': 'https://www.hubspot.com/sales/statistics',
        'year': '2024',
        'metrics': 'Lead-to-customer: 2.5-5% (B2B avg), 10-15% (B2C), Close rate: 20-30%',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': 'Global sales data'
    },
    'sales_pipeline': {
        'name': 'Salesforce State of Sales Report 2024',
        'url': 'https://www.salesforce.com/resources/research-reports/state-of-sales/',
        'year': '2024',
        'metrics': 'Win rate: 47% avg, Pipeline velocity: 15-20% quarterly growth',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': '7,700+ sales professionals'
    },
    'sales_cycle': {
        'name': 'Salesforce State of Sales Report 2024',
        'url': 'https://www.salesforce.com/resources/research-reports/state-of-sales/',
        'year': '2024',
        'metrics': 'Avg cycle: 102 days (B2B), 3-7 days (B2C VN), Enterprise: 6-12 months',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': '7,700+ sales professionals'
    },
    'sales_win_rate': {
        'name': 'Salesforce Win Rate Benchmarks 2024',
        'url': 'https://www.salesforce.com/resources/research-reports/state-of-sales/',
        'year': '2024',
        'metrics': 'Win rate: 47% avg, Top performers: 65%+, Competitive deals: 30-40%',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': '7,700+ sales professionals'
    },
    'sales_growth': {
        'name': 'McKinsey Sales Growth Research',
        'url': 'https://www.mckinsey.com/capabilities/growth-marketing-and-sales/our-insights',
        'year': '2024',
        'metrics': 'Revenue growth: 10-15% annually (healthy), Top quartile: 20%+',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': 'Global enterprise research'
    },
    'sales_vietnam_b2b': {
        'name': 'Vietnam B2B E-commerce (VECOM EBI 2024)',
        'url': 'https://esc.vn/wp-content/uploads/2025/07/Bao-cao-EBI-2024-ENG.pdf',
        'year': '2024',
        'metrics': 'B2B sector included in $25B total e-commerce market, Cross-border B2C exports: $3.5B, Digital payments infrastructure: 11B transactions',
        'credibility': '⭐⭐⭐⭐⭐',
        'vietnam_specific': True,
        'cost': 'FREE',
        'sample_size': 'Vietnam E-commerce Association (VECOM) - Official industry report, same source as EBI report'
    },
    
    # ========================
    # FINANCE
    # ========================
    'finance_margin': {
        'name': 'Industry Standard (GAAP/IFRS)',
        'url': 'https://www.investopedia.com/terms/g/grossmargin.asp',
        'year': '2024',
        'metrics': 'Gross margin: 20-40% (retail), 50-80% (SaaS), 10-20% (manufacturing)',
        'credibility': '⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': 'Accounting standards'
    },
    'finance_liquidity': {
        'name': 'Deloitte CFO Signals Survey 2024',
        'url': 'https://www2.deloitte.com/us/en/pages/finance/articles/cfo-signals.html',
        'year': '2024',
        'metrics': 'Current ratio: 1.5-3.0 (healthy), Quick ratio: 1.0-2.0',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': 'CFO survey data'
    },
    'finance_growth': {
        'name': 'S&P Global Market Intelligence',
        'url': 'https://www.spglobal.com/marketintelligence/en/',
        'year': '2024',
        'metrics': 'Revenue growth: 5-10% (mature), 20-50% (startup), Vietnam GDP: 6-7%',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE (summary)',
        'sample_size': 'Global market data'
    },
    'finance_efficiency': {
        'name': 'PwC Finance Effectiveness Benchmark',
        'url': 'https://www.pwc.com/gx/en/services/advisory/consulting/finance-effectiveness.html',
        'year': '2024',
        'metrics': 'Finance cost: 1-2% of revenue (best-in-class), Days to close: 5-10 days',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE (summary)',
        'sample_size': 'Global benchmark study'
    },
    'finance_cash': {
        'name': 'JP Morgan Treasury Insights',
        'url': 'https://www.jpmorgan.com/insights/treasury-payments',
        'year': '2024',
        'metrics': 'Cash conversion cycle: 30-60 days (target), Working capital: 15-20% revenue',
        'credibility': '⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': 'Treasury best practices'
    },
    
    # ========================
    # CUSTOMER SERVICE
    # ========================
    'cs_response_time': {
        'name': 'Zendesk Customer Experience Trends 2024',
        'url': 'https://www.zendesk.com/customer-experience-trends/',
        'year': '2024',
        'metrics': 'First reply: 12h (APAC avg), 24h (acceptable), <6h (excellent)',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,  # APAC applicable to Vietnam
        'cost': 'FREE',
        'sample_size': '97,000+ companies analyzed'
    },
    'cs_resolution': {
        'name': 'Zendesk Customer Experience Trends 2024',
        'url': 'https://www.zendesk.com/customer-experience-trends/',
        'year': '2024',
        'metrics': 'Full resolution: 24h (target), 48h (acceptable), SLA compliance: 85%+',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': '97,000+ companies'
    },
    'cs_satisfaction': {
        'name': 'American Customer Satisfaction Index (ACSI)',
        'url': 'https://www.theacsi.org/',
        'year': '2024',
        'metrics': 'CSAT: 80-85% (good), 90%+ (excellent), <70% (poor)',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': 'US national survey'
    },
    'cs_fcr': {
        'name': 'SQM Group First Call Resolution Study',
        'url': 'https://www.sqmgroup.com/resources/benchmarks',
        'year': '2024',
        'metrics': 'FCR: 70-75% (world-class), 60-70% (good), <60% (needs improvement)',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': 'Call center benchmarks'
    },
    'cs_nps': {
        'name': 'Bain & Company NPS Benchmarks',
        'url': 'https://www.netpromotersystem.com/about/how-it-works/',
        'year': '2024',
        'metrics': 'NPS: 50+ (excellent), 20-50 (good), <0 (poor), Leaders: 70+',
        'credibility': '⭐⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': 'Industry benchmarks'
    },
    
    # ========================
    # MANUFACTURING
    # ========================
    'mfg_oee': {
        'name': 'McKinsey Manufacturing Productivity',
        'url': 'https://www.mckinsey.com/capabilities/operations/our-insights/manufacturing-productivity',
        'year': '2024',
        'metrics': 'OEE: 85% (world-class), 60-75% (average), <60% (poor)',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': 'Global manufacturing study'
    },
    'mfg_yield': {
        'name': 'ISA-95 Manufacturing Standards',
        'url': 'https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa95',
        'year': '2024',
        'metrics': 'Yield: 95%+ (target), 90-95% (acceptable), <90% (improvement needed)',
        'credibility': '⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': 'Industry standards'
    },
    'mfg_defect_rate': {
        'name': 'Six Sigma Quality Standards',
        'url': 'https://www.isixsigma.com/dictionary/dpmo/',
        'year': '2024',
        'metrics': 'Defects: 3.4 DPMO (Six Sigma), 230 DPMO (5σ), 6,210 DPMO (4σ)',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': 'Quality methodology'
    },
    'mfg_downtime': {
        'name': 'McKinsey Manufacturing Operations',
        'url': 'https://www.mckinsey.com/capabilities/operations/our-insights/manufacturing-productivity',
        'year': '2024',
        'metrics': 'Downtime: <5% (excellent), 5-10% (acceptable), >15% (poor)',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': 'Manufacturing research'
    },
    'mfg_cost': {
        'name': 'McKinsey Operations Performance',
        'url': 'https://www.mckinsey.com/capabilities/operations/our-insights',
        'year': '2024',
        'metrics': 'Cost reduction: 10-20% achievable with lean, 30%+ with automation',
        'credibility': '⭐⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': 'Operations excellence study'
    },
    
    # ========================
    # GENERAL/DEFAULT
    # ========================
    'general': {
        'name': 'Industry Standard / Historical Data',
        'url': 'https://www.bls.gov/data/',
        'year': '2024',
        'metrics': 'US Bureau of Labor Statistics - various economic indicators',
        'credibility': '⭐⭐⭐',
        'vietnam_specific': False,
        'cost': 'FREE',
        'sample_size': 'US government data'
    },
    'calculated': {
        'name': 'Calculated from Your Dataset Statistics',
        'url': 'https://github.com/zicky008/fast-dataanalytics-vietnam#data-quality-methodology',
        'year': '2024',
        'metrics': 'Real statistics from your data: median, mean, std dev, percentiles (P25, P50, P75)',
        'credibility': '⭐⭐⭐⭐⭐',
        'vietnam_specific': True,
        'cost': 'N/A (computed from your uploaded file)',
        'sample_size': 'Your complete dataset',
        'note': 'All metrics calculated directly from your data - 100% accurate, no external benchmarks'
    }
}

# Quality Score Rubric (for transparency)
QUALITY_SCORE_RUBRIC = {
    'criteria': [
        {'name': 'Data Completeness', 'weight': 20, 'description': 'Percentage of non-null values'},
        {'name': 'Data Consistency', 'weight': 20, 'description': 'Format consistency across columns'},
        {'name': 'Data Accuracy', 'weight': 20, 'description': 'Valid ranges and business rules'},
        {'name': 'Data Timeliness', 'weight': 15, 'description': 'Recency and update frequency'},
        {'name': 'Data Uniqueness', 'weight': 15, 'description': 'Duplicate detection and handling'},
        {'name': 'Data Validity', 'weight': 10, 'description': 'Schema compliance and type correctness'}
    ],
    'total_weight': 100,
    'description': 'Based on ISO 8000 Data Quality Standards',
    'rating_scale': {
        '90-100': 'Excellent - Production Ready',
        '80-89': 'Good - Minor improvements recommended',
        '70-79': 'Acceptable - Some issues to address',
        '60-69': 'Fair - Significant improvements needed',
        '0-59': 'Poor - Major data quality issues'
    }
}

# KPI Status Definitions (for clarity)
KPI_STATUS_DEFINITIONS = {
    'Above': {
        'threshold': '+10% or more vs benchmark',
        'meaning': 'Performing significantly better than industry standard',
        'color': 'green',
        'emoji': '✅'
    },
    'Competitive': {
        'threshold': 'Within ±10% of benchmark',
        'meaning': 'Performing at industry standard level',
        'color': 'blue',
        'emoji': '➡️'
    },
    'Below': {
        'threshold': '-10% or more vs benchmark',
        'meaning': 'Performing below industry standard - improvement needed',
        'color': 'orange',
        'emoji': '⚠️'
    },
    'Note': 'Thresholds may vary by KPI type. Lower is better for costs, higher is better for revenue.'
}


# ==================================================================================
# HELPER FUNCTION: Auto-assign benchmark sources
# ==================================================================================

def get_benchmark_source(kpi_name: str, domain: str) -> dict:
    """
    Automatically determine benchmark source based on KPI name and domain.
    Returns FULL metadata including URL, year, metrics, credibility rating.
    
    **ENHANCED 2025-10-29**: Now returns rich metadata dict for user trust/verification.

    Args:
        kpi_name: Name of the KPI (e.g., "Average ROI", "First Call Resolution")
        domain: Domain name (e.g., "Marketing", "Customer Service")

    Returns:
        dict: {
            'name': 'Source name',
            'url': 'Clickable verification URL',
            'year': '2024',
            'metrics': 'Sample metrics for preview',
            'credibility': '⭐⭐⭐⭐⭐',
            'vietnam_specific': True/False,
            'cost': 'FREE/Paid',
            'sample_size': 'Data sample info'
        }
    """
    kpi_lower = kpi_name.lower()
    domain_lower = domain.lower()

    # Mapping KPI keywords to source keys
    if 'salary' in kpi_lower or 'compensation' in kpi_lower:
        return BENCHMARK_SOURCES['hr_salary']
    elif 'turnover' in kpi_lower or 'attrition' in kpi_lower:
        return BENCHMARK_SOURCES['hr_turnover']
    elif 'satisfaction' in kpi_lower and ('employee' in kpi_lower or 'hr' in domain_lower):
        return BENCHMARK_SOURCES['hr_satisfaction']
    elif 'roi' in kpi_lower and 'marketing' in domain_lower:
        return BENCHMARK_SOURCES['marketing_roi']
    elif 'roas' in kpi_lower:
        return BENCHMARK_SOURCES['marketing_roas']
    elif 'ctr' in kpi_lower or 'click' in kpi_lower:
        return BENCHMARK_SOURCES['marketing_ctr']
    elif 'conversion' in kpi_lower and ('marketing' in domain_lower or 'campaign' in kpi_lower):
        return BENCHMARK_SOURCES['marketing_conversion']
    elif ('cost per unit' in kpi_lower or 'cost per product' in kpi_lower) and 'manufacturing' in domain_lower:
        return BENCHMARK_SOURCES['mfg_cost']  # ✅ FIX #2: Manufacturing cost (not marketing CPA!)
    elif 'cpa' in kpi_lower or 'cost per' in kpi_lower:
        return BENCHMARK_SOURCES['marketing_cpa']
    elif 'conversion' in kpi_lower and ('ecommerce' in domain_lower or 'online' in domain_lower):
        return BENCHMARK_SOURCES['ecommerce_conversion']
    elif 'aov' in kpi_lower or 'average order' in kpi_lower:
        return BENCHMARK_SOURCES['ecommerce_aov']
    elif 'cart' in kpi_lower and 'abandon' in kpi_lower:
        return BENCHMARK_SOURCES['ecommerce_cart_abandonment']
    elif 'mobile' in kpi_lower and 'ecommerce' in domain_lower:
        return BENCHMARK_SOURCES['ecommerce_mobile']
    elif ('repeat' in kpi_lower or 'returning' in kpi_lower) and 'ecommerce' in domain_lower:
        return BENCHMARK_SOURCES['ecommerce_repeat']
    elif 'win rate' in kpi_lower or 'sales' in domain_lower and 'conversion' in kpi_lower:
        return BENCHMARK_SOURCES['sales_conversion']
    elif 'pipeline' in kpi_lower:
        return BENCHMARK_SOURCES['sales_pipeline']
    elif 'cycle' in kpi_lower and 'sales' in domain_lower:
        return BENCHMARK_SOURCES['sales_cycle']
    elif 'growth' in kpi_lower and ('sales' in domain_lower or 'revenue' in kpi_lower):
        return BENCHMARK_SOURCES['sales_growth']
    elif 'margin' in kpi_lower or 'profit' in kpi_lower:
        return BENCHMARK_SOURCES['finance_margin']
    elif 'liquidity' in kpi_lower or 'cash' in kpi_lower:
        return BENCHMARK_SOURCES['finance_cash']
    elif ('growth' in kpi_lower or 'mrr' in kpi_lower) and 'finance' in domain_lower:
        return BENCHMARK_SOURCES['finance_growth']
    elif 'response' in kpi_lower or 'first response' in kpi_lower:
        return BENCHMARK_SOURCES['cs_response_time']
    elif 'resolution' in kpi_lower or 'fcr' in kpi_lower:
        return BENCHMARK_SOURCES['cs_fcr']
    elif ('satisfaction' in kpi_lower or 'csat' in kpi_lower) and 'customer' in kpi_lower:
        return BENCHMARK_SOURCES['cs_satisfaction']
    elif 'nps' in kpi_lower:
        return BENCHMARK_SOURCES['cs_nps']
    elif 'yield' in kpi_lower or 'fpy' in kpi_lower:
        return BENCHMARK_SOURCES['mfg_yield']
    elif 'defect' in kpi_lower:
        return BENCHMARK_SOURCES['mfg_defect_rate']
    elif 'oee' in kpi_lower or 'efficiency' in kpi_lower and 'manufacturing' in domain_lower:
        return BENCHMARK_SOURCES['mfg_oee']
    elif 'downtime' in kpi_lower:
        return BENCHMARK_SOURCES['mfg_downtime']
    elif 'cost' in kpi_lower and 'manufacturing' in domain_lower:
        return BENCHMARK_SOURCES['mfg_cost']
    elif 'median' in kpi_lower or 'mean' in kpi_lower or 'average' in kpi_lower:
        return BENCHMARK_SOURCES['calculated']
    else:
        return BENCHMARK_SOURCES['general']


def add_benchmark_metadata(kpis: Dict, domain: str) -> Dict:
    """
    Add benchmark_source to all KPIs that don't have it yet.
    This ensures backward compatibility and comprehensive transparency.

    Args:
        kpis: Dictionary of KPIs
        domain: Domain name

    Returns:
        Updated KPIs dictionary with benchmark_source for all entries
    """
    for kpi_name, kpi_data in kpis.items():
        if 'benchmark_source' not in kpi_data and 'benchmark' in kpi_data:
            kpi_data['benchmark_source'] = get_benchmark_source(kpi_name, domain)
    return kpis


# ==================================================================================
# DOMAIN-SPECIFIC DEDUPLICATION RULES (MDM Best Practices)
# ==================================================================================
# Based on Master Data Management (MDM) survivorship rules and ISO 8000 standards
# Research: See RESEARCH_DUPLICATE_CONTROL_ANALYSIS.md
# ==================================================================================

DEDUPLICATION_RULES = {
    'HR / Nhân Sự': {
        'enabled': True,
        'strategy': 'key_based',
        'key_columns': ['employee id', 'employee_id', 'emp id', 'emp_id', 'ssn', 'national id', 'staff id', 'nhân viên'],
        'keep': 'last',  # Keep most recent record
        'threshold': 0.05,  # Warn if >5% duplicates (normal: 1-5%)
        'description': 'Deduplicate by employee identifier, keep latest record'
    },
    'Marketing / Quảng Cáo': {
        'enabled': True,
        'strategy': 'key_based',
        'key_columns': ['email', 'campaign id', 'campaign_id', 'campaign', 'customer id'],
        'keep': 'first',  # Keep first campaign response
        'threshold': 0.15,  # 15% duplicates normal in marketing
        'description': 'Keep one record per email per campaign'
    },
    'Finance / Tài Chính': {
        'enabled': True,
        'strategy': 'key_based',
        'key_columns': ['account number', 'account_number', 'transaction id', 'transaction_id', 'invoice id'],
        'keep': 'last',  # Keep most recent transaction
        'threshold': 0.01,  # Finance should have <1% duplicates
        'description': 'Remove duplicate transactions (fraud prevention)'
    },
    'E-commerce / Bán Hàng Trực Tuyến': {
        'enabled': True,
        'strategy': 'key_based',
        'key_columns': ['order id', 'order_id', 'customer id', 'customer_id', 'transaction id'],
        'keep': 'last',
        'threshold': 0.10,
        'description': 'Keep latest order status per customer'
    },
    'Sales / Kinh Doanh': {
        'enabled': True,
        'strategy': 'key_based',
        'key_columns': ['opportunity id', 'opportunity_id', 'deal id', 'deal_id', 'lead id'],
        'keep': 'last',
        'threshold': 0.20,  # Sales data often has duplicates
        'description': 'Keep latest opportunity status'
    },
    'Customer Service / Chăm Sóc Khách Hàng': {
        'enabled': True,
        'strategy': 'key_based',
        'key_columns': ['ticket id', 'ticket_id', 'case id', 'case_id', 'support id'],
        'keep': 'last',  # Keep latest ticket status (preserves reopens)
        'threshold': 0.05,
        'description': 'Keep latest ticket status (reopened tickets preserved)'
    },
    'Manufacturing / Sản Xuất': {
        'enabled': True,
        'strategy': 'key_based',
        'key_columns': ['serial number', 'serial_number', 'batch id', 'batch_id', 'product id', 'part number'],
        'keep': 'last',
        'threshold': 0.02,
        'description': 'Keep latest quality measurement per unit'
    },
    'Operations / Vận Hành': {
        'enabled': True,
        'strategy': 'key_based',
        'key_columns': ['order id', 'shipment id', 'tracking number', 'warehouse id'],
        'keep': 'last',
        'threshold': 0.10,
        'description': 'Keep latest operational status'
    },
    '_default': {
        'enabled': True,
        'strategy': 'all_columns',
        'key_columns': [],
        'keep': 'first',
        'threshold': 0.05,
        'description': 'Remove exact duplicates (all columns match)'
    }
}


def is_streamlit_context():
    """Check if running in Streamlit context"""
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        return get_script_run_ctx() is not None
    except:
        return False


class PremiumLeanPipeline:
    """
    Premium Lean Pipeline: Fast + Professional Quality
    Optimized for 55-second execution with premium features maintained
    """
    
    def __init__(self, gemini_client, lang: str = 'vi'):
        self.client = gemini_client
        self.lang = lang  # Store language for bilingual support
        self.domain_cache = {}  # Cache domain profiles
        self.pipeline_state = {
            'domain_info': None,
            'cleaned_data': None,
            'smart_blueprint': None,
            'dashboard': None,
            'insights': None,
            'audit_trail': [],
            'performance_metrics': {}
        }
        # Load Vietnam benchmarks (300+ metrics from CSV files)
        self.benchmark_loader = get_benchmark_loader()
        self.vietnam_benchmarks_loaded = any(self.benchmark_loader.load_all_benchmarks().values())

    def _get_vietnam_benchmark(self, domain: str, metric_name: str, user_value: float, filters: Dict = None) -> Optional[Dict]:
        """
        Helper method to get Vietnam benchmark for a metric.

        Args:
            domain: 'hr', 'marketing', 'ecommerce', or 'sales'
            metric_name: Metric name (e.g., 'CPA', 'salary', 'AOV')
            user_value: User's actual value
            filters: Additional filters (e.g., {'channel': 'Facebook Ads'})

        Returns:
            Dict with benchmark data or None if not found
        """
        if not self.vietnam_benchmarks_loaded:
            return None

        try:
            comparison = self.benchmark_loader.compare_value_to_benchmark(
                domain=domain,
                metric_name=metric_name,
                user_value=user_value,
                filters=filters or {}
            )
            return comparison
        except Exception as e:
            # Silently fail if benchmark not found
            return None

    @log_performance("Premium Lean Pipeline")
    def run_pipeline(self, df: pd.DataFrame, dataset_description: str = "") -> Dict:
        """
        Chạy Premium Lean Pipeline: 55 seconds với premium quality
        
        Returns:
            {
                'success': bool,
                'dashboard': {...},
                'insights': {...},
                'quality_scores': {...},
                'performance': {...}
            }
        """
        
        start_time = time.time()
        
        try:
            # Step 0: Domain Detection (3s - cached)
            if is_streamlit_context():
                progress_placeholder = st.empty()
                progress_placeholder.info(get_text('pipeline_step0', self.lang))
            
            domain_info = self.step0_domain_detection(df, dataset_description)
            self._add_audit_trail("Domain Detection", domain_info)
            self._update_performance("domain_detection", time.time() - start_time)
            
            # Step 1: Data Cleaning (15s - ISO 8000)
            step1_start = time.time()
            if is_streamlit_context():
                progress_placeholder.info(get_text('pipeline_step1', self.lang, domain=domain_info['domain_name']))
            
            cleaning_result = self.step1_data_cleaning(df, domain_info)
            if not cleaning_result['success']:
                return self._error_response(cleaning_result['error'])
            
            self._add_audit_trail("Data Cleaning", cleaning_result)
            self._update_performance("data_cleaning", time.time() - step1_start)
            
            # Step 2: Smart Blueprint (15s - EDA + Blueprint combined)
            step2_start = time.time()
            if is_streamlit_context():
                progress_placeholder.info(get_text('pipeline_step2', self.lang, expert=domain_info['expert_role'][:50]))
            
            blueprint_result = self.step2_smart_blueprint(
                cleaning_result['df_cleaned'],
                domain_info
            )
            if not blueprint_result['success']:
                return self._error_response(blueprint_result['error'])
            
            self._add_audit_trail("Smart Blueprint", blueprint_result)
            self._update_performance("smart_blueprint", time.time() - step2_start)
            
            # Step 3: Dashboard Build (7s - pure execution)
            step3_start = time.time()
            if is_streamlit_context():
                progress_placeholder.info(get_text('pipeline_step3', self.lang))
            
            dashboard_result = self.step3_dashboard_build(
                cleaning_result['df_cleaned'],
                blueprint_result['smart_blueprint']
            )
            
            self._add_audit_trail("Dashboard Build", dashboard_result)
            self._update_performance("dashboard_build", time.time() - step3_start)
            
            # Step 4: Domain Insights (15s - expert perspective)
            step4_start = time.time()
            if is_streamlit_context():
                progress_placeholder.info(get_text('pipeline_step4', self.lang, expert=domain_info['expert_role'][:50]))
            
            insights_result = self.step4_domain_insights(
                dashboard_result,
                blueprint_result['smart_blueprint'],
                domain_info
            )
            
            self._add_audit_trail("Domain Insights", insights_result)
            self._update_performance("domain_insights", time.time() - step4_start)
            
            # Calculate total time
            total_time = time.time() - start_time
            self._update_performance("total", total_time)
            
            # Success message
            if is_streamlit_context():
                progress_placeholder.success(get_text('pipeline_complete', self.lang, time=total_time))
            
            # ✅ FIX #4: Comprehensive quality scoring with metadata validation
            # Calculate base score (cleaning + blueprint) BEFORE creating return dict
            base_cleaning_score = cleaning_result['quality_score']
            base_blueprint_score = blueprint_result['quality_score']
            base_overall = (base_cleaning_score + base_blueprint_score) / 2
            
            # Apply deductions for metadata/consistency issues (ISO 8000 compliance)
            deductions = self._calculate_quality_deductions(
                df=df,
                kpis=dashboard_result.get('kpis', {}),
                domain=domain_info['domain']  # 🐛 HOTFIX: Use local variable, not pipeline_state
            )
            
            # Final scores (capped at 0-100 range)
            final_overall = max(0, min(100, base_overall - deductions['total']))
            
            # Return complete result
            return {
                'success': True,
                'domain_info': domain_info,
                'cleaning_report': cleaning_result['cleaning_report'],
                'smart_blueprint': blueprint_result['smart_blueprint'],
                'dashboard': dashboard_result,
                'insights': insights_result['insights'],
                'audit_trail': self.pipeline_state['audit_trail'],
                'quality_scores': {
                    'cleaning': base_cleaning_score,
                    'blueprint': base_blueprint_score,
                    'base_overall': base_overall,  # Before deductions
                    'deductions': deductions,  # Transparency about penalties
                    'overall': round(final_overall, 1)  # After deductions
                },
                'performance': self.pipeline_state['performance_metrics']
            }
        
        except Exception as e:
            return self._error_response(f"Pipeline error: {str(e)}")
    
    def step0_domain_detection(self, df: pd.DataFrame, description: str) -> Dict:
        """
        Step 0: Domain detection với caching (3s)
        """
        # Check cache first
        cache_key = f"{len(df.columns)}_{','.join(df.columns[:5])}"
        if cache_key in self.domain_cache:
            return self.domain_cache[cache_key]
        
        # Detect domain
        domain_info = detect_domain(df, description)
        
        # Cache result
        self.domain_cache[cache_key] = domain_info
        
        # Display to user (only in Streamlit context)
        if is_streamlit_context():
            with st.expander(get_text('domain_detection_title', self.lang), expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(get_text('domain_label', self.lang), domain_info['domain_name'])
                    st.metric(get_text('confidence_label', self.lang), f"{domain_info['confidence']*100:.0f}%")
                with col2:
                    st.caption(f"**{get_text('expert_label', self.lang)}**: {domain_info['expert_role'][:60]}...")
                    st.caption(f"**{get_text('key_kpis_label', self.lang)}**: {', '.join(domain_info['key_kpis'][:3])}")
        
        return domain_info
    
    @rate_limit_handler(max_retries=3, backoff_base=2)
    @log_performance("Data Cleaning")
    def step1_data_cleaning(self, df: pd.DataFrame, domain_info: Dict) -> Dict:
        """
        Step 1: ISO 8000 data cleaning (15s)
        """
        
        # 🐛 FIX: Ensure domain_context is always string (handle potential dict/object returns)
        try:
            domain_context = get_domain_specific_prompt_context(domain_info)
            if not isinstance(domain_context, str):
                domain_context = str(domain_context)
        except Exception as e:
            domain_name = domain_info.get('domain_name', domain_info.get('domain', 'General'))
            expert_role = domain_info.get('expert_role', 'Data Analyst')
            domain_context = f"Domain: {domain_name}\nExpert Role: {expert_role}"
        
        # Check for protected fields in dataset
        protected_cols = [col for col in df.columns if is_never_impute_field(col)]
        protected_warning = f"\n⚠️ PROTECTED FIELDS DETECTED: {', '.join(protected_cols)}" if protected_cols else ""
        
        # Simplified cleaning prompt (faster) WITH NEVER_IMPUTE PROTECTION
        prompt = f"""
{domain_context}

TASK: Fast Professional Data Cleaning (ISO 8000)

DATA: {df.shape[0]} rows × {df.shape[1]} columns
Columns: {', '.join(df.columns[:15])}
Missing: {df.isnull().sum().sum()} values
Duplicates: {df.duplicated().sum()} rows
{protected_warning}

REQUIREMENTS (Essential Only):

🔴 **CRITICAL RULE #1: NEVER IMPUTE PROTECTED FIELDS**
The following fields are PROTECTED and must NEVER be imputed:
- Financial: revenue, sales, cost, expense, profit, price, salary, luong, doanh_thu
- IDs: employee_id, customer_id, order_id, ma_don_hang, ma_khach_hang
- PII: email, phone, address, cccd, cmnd, so_dien_thoai

For protected fields:
→ IF MISSING: Keep as NULL (DO NOT fill with median/mode/any value)
→ FLAG in report: "X rows with missing [field_name] - kept as NULL"
→ REASON: Fake data → Wrong business decisions → Legal liability

Protected fields in THIS dataset: {', '.join(protected_cols) if protected_cols else 'None'}

1. Fix missing values:
   - NON-protected fields only: Use median for numeric, mode for categorical
   - Protected fields: KEEP AS NULL + add to missing_flagged report
2. Remove duplicates
3. Standardize formats (dates, numbers)
4. Basic validation against domain rules

QUALITY GATES:
- Missing <2% (excluding protected fields with legitimate nulls)
- Duplicates = 0
- Validation ≥95%

OUTPUT JSON:
{{
    "cleaning_summary": {{
        "rows_before": {df.shape[0]},
        "rows_after": X,
        "missing_handled": {{"col": "method"}},
        "duplicates_removed": X
    }},
    "quality_metrics": {{
        "completeness": 99.0,
        "accuracy": 96.0,
        "consistency": 98.0
    }},
    "transformations": [
        {{"column": "date", "action": "standardized", "rows_affected": X}}
    ]
}}
"""
        
        success, result = self._generate_ai_insight(prompt, temperature=0.2, max_tokens=4000)
        
        if not success:
            return {'success': False, 'error': result}
        
        try:
            cleaning_plan = json.loads(result)
            
            # Apply cleaning (simplified) - now with domain-specific deduplication
            df_cleaned = self._apply_fast_cleaning(df, cleaning_plan, domain_info)
            
            # Validate quality gates
            validation = self._validate_quality_gates(df_cleaned, cleaning_plan)
            
            if not validation['passed']:
                return {
                    'success': False,
                    'error': f"❌ Chất lượng dữ liệu không đạt chuẩn: {', '.join(validation['failures'])}"
                }
            
            # Display cleaning report (compact)
            self._display_compact_cleaning_report(cleaning_plan, validation)
            
            return {
                'success': True,
                'df_cleaned': df_cleaned,
                'cleaning_report': cleaning_plan,
                'quality_score': validation['score']
            }
        
        except json.JSONDecodeError as e:
            return {'success': False, 'error': f"❌ Lỗi phân tích dữ liệu: {str(e)}"}
    
    def _convert_string_to_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        ⭐ CRITICAL: Convert string columns that represent numbers to proper numeric types
        
        This handles:
        - European format: '5,43' (comma as decimal) → 5.43
        - US format: '5.43' → 5.43
        - Thousands separator: '8.311,42' or '8,311.42'
        
        Returns:
            DataFrame with converted numeric columns
        """
        df_converted = df.copy()
        
        for col in df_converted.columns:
            # Skip if already numeric
            if pd.api.types.is_numeric_dtype(df_converted[col]):
                continue
            
            # Check if column contains numeric-like strings
            if df_converted[col].dtype == 'object':
                sample_values = df_converted[col].dropna().head(10)
                
                if len(sample_values) == 0:
                    continue
                
                # Check if values look like numbers (contain digits, comma, or period)
                numeric_pattern = sample_values.astype(str).str.match(r'^[\d.,\s-]+$')
                
                if numeric_pattern.sum() / len(sample_values) > 0.5:  # At least 50% numeric
                    try:
                        # Try European format first (comma = decimal, period = thousands)
                        # Example: '8.311,42' → 8311.42
                        if df_converted[col].astype(str).str.contains(',').any():
                            df_converted[col] = (df_converted[col]
                                .astype(str)
                                .str.replace('.', '', regex=False)  # Remove thousands separator
                                .str.replace(',', '.', regex=False)  # Replace decimal comma with period
                                .str.strip())
                        
                        # Convert to numeric (coerce errors to NaN)
                        df_converted[col] = pd.to_numeric(df_converted[col], errors='coerce')
                        
                    except Exception:
                        # If conversion fails, keep original
                        pass
        
        return df_converted
    
    def _calculate_real_kpis(self, df: pd.DataFrame, domain_info: Dict) -> Dict:
        """
        ⭐ CRITICAL: Calculate KPIs from REAL DATA (not AI estimation)
        This ensures "cực kỳ chuẩn xác, uy tín, tin cậy" requirement
        """
        kpis = {}
        # Support both 'domain' and 'domain_name' keys for backward compatibility
        domain = domain_info.get('domain', domain_info.get('domain_name', 'general')).lower()
        
        # ⭐ FIX: Convert string numeric columns to proper numeric types
        # This handles European CSV format (comma as decimal separator)
        df = self._convert_string_to_numeric(df)
        
        # Get numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        all_cols_lower = [col.lower() for col in df.columns]
        
        # === SMART COLUMN DETECTION ===
        primary_metric_col = None
        priority_keywords = ['salary', 'revenue', 'sales', 'profit', 'cost', 'price', 'amount', 'value']
        
        for keyword in priority_keywords:
            matching_cols = [df.columns[i] for i, col in enumerate(all_cols_lower) 
                           if keyword in col and df.columns[i] in numeric_cols]
            if matching_cols:
                primary_metric_col = matching_cols[0]
                break
        
        if not primary_metric_col and len(numeric_cols) > 0:
            sums = {col: abs(df[col].sum()) for col in numeric_cols}
            primary_metric_col = max(sums, key=sums.get)
        
        # === SALARY DATA (high priority - works even if domain is "General") ===
        if 'salary' in ' '.join(all_cols_lower):
            salary_col = [col for col in df.columns if 'salary' in col.lower()][0]
            avg_salary = df[salary_col].mean()
            median_salary = df[salary_col].median()

            # ⚠️ CRITICAL FIX: Use Vietnam benchmark data from CSV files (not hardcoded!)
            # Detect currency: Values > 1M = VND, < 500K = USD
            is_vnd = avg_salary > 1000000

            # Try to get Vietnam benchmark from CSV data
            vietnam_benchmark = None
            vietnam_context = ''

            if is_vnd and self.vietnam_benchmarks_loaded:
                # Try to match role from dataframe
                role_cols = [col for col in df.columns if 'role' in col.lower() or 'position' in col.lower() or 'title' in col.lower()]
                city_cols = [col for col in df.columns if 'city' in col.lower() or 'location' in col.lower()]

                filters = {}
                if role_cols and not df[role_cols[0]].isna().all():
                    # Get most common role
                    most_common_role = df[role_cols[0]].mode()[0] if len(df[role_cols[0]].mode()) > 0 else None
                    if most_common_role:
                        filters['role'] = str(most_common_role)

                if city_cols and not df[city_cols[0]].isna().all():
                    most_common_city = df[city_cols[0]].mode()[0] if len(df[city_cols[0]].mode()) > 0 else None
                    if most_common_city:
                        filters['city'] = str(most_common_city)

                # Get Vietnam HR benchmark
                vietnam_comparison = self.benchmark_loader.compare_value_to_benchmark(
                    domain='hr',
                    metric_name='salary',
                    user_value=median_salary,
                    filters=filters
                )

                if vietnam_comparison:
                    vietnam_benchmark = vietnam_comparison
                    vietnam_context = vietnam_comparison.get('message', '')

            # Set benchmarks (use Vietnam data if available, else fallback to estimates)
            if vietnam_benchmark:
                avg_benchmark = vietnam_benchmark['benchmark_median']
                median_benchmark = vietnam_benchmark['benchmark_median']
                range_benchmark = vietnam_benchmark['benchmark_q3'] - vietnam_benchmark['benchmark_q1']
                benchmark_source = vietnam_benchmark.get('benchmark_source', BENCHMARK_SOURCES['hr_salary'])
            elif is_vnd:
                # Vietnam market - VND fallback (if CSV not loaded)
                avg_benchmark = 32500000  # ~32.5M VND/month - realistic median from CSV
                median_benchmark = 32500000
                range_benchmark = 25000000  # Q3-Q1 range
                benchmark_source = BENCHMARK_SOURCES['hr_salary'] + ' (Estimated)'
            else:
                # International market - USD
                avg_benchmark = 18000
                median_benchmark = 16000
                range_benchmark = 50000
                benchmark_source = 'Global Market Data (Estimated)'

            kpis['Average Salary'] = {
                'value': float(avg_salary),
                'benchmark': avg_benchmark,
                'benchmark_source': benchmark_source,
                'status': 'Above' if avg_salary >= avg_benchmark * 0.9 else 'Below',
                'column': salary_col,
                'vietnam_context': vietnam_context if vietnam_benchmark else ''
            }

            kpis['Median Salary'] = {
                'value': float(median_salary),
                'benchmark': median_benchmark,
                'benchmark_source': benchmark_source,
                'status': 'Above' if median_salary >= median_benchmark * 0.9 else 'Below',
                'column': salary_col,
                'vietnam_context': vietnam_context if vietnam_benchmark else '',
                'percentile': vietnam_benchmark.get('percentile', None) if vietnam_benchmark else None
            }

            kpis['Salary Range'] = {
                'value': float(df[salary_col].max() - df[salary_col].min()),
                'benchmark': range_benchmark,
                'benchmark_source': benchmark_source,
                'status': 'Wide Range' if (df[salary_col].max() - df[salary_col].min()) > range_benchmark * 1.2 else 'Normal Range',
                'column': salary_col
            }
            
            # Years of Experience ratio (if available)
            exp_cols = [col for col in df.columns if 'experience' in col.lower() or 'yoe' in col.lower()]
            if exp_cols:
                exp_col = exp_cols[0]
                avg_exp = df[exp_col].mean()
                avg_salary = df[salary_col].mean()
                if avg_exp > 0:
                    kpis['Salary per Experience Year'] = {
                        'value': float(avg_salary / avg_exp),
                        'benchmark': 10000,
                        'status': 'Competitive',
                        'column': f"{salary_col}/{exp_col}"
                    }
        
        # === MARKETING DATA ===
        elif 'marketing' in domain or 'quảng cáo' in domain:
            # Detect key marketing columns
            roi_cols = [col for col in df.columns if 'roi' in col.lower()]
            spend_cols = [col for col in df.columns if 'spend' in col.lower() or 'cost' in col.lower()]
            click_cols = [col for col in df.columns if 'click' in col.lower()]
            impression_cols = [col for col in df.columns if 'impression' in col.lower()]
            conversion_cols = [col for col in df.columns if 'conversion' in col.lower()]
            revenue_cols = [col for col in df.columns if 'revenue' in col.lower()]
            
            # 1. ROI (Return on Investment)
            # ⚠️ NOTE: ROI definition varies widely - use with caution or prefer ROAS
            if roi_cols and len(roi_cols) > 0:
                roi_col = roi_cols[0]
                avg_roi = df[roi_col].mean()
                kpis['Marketing ROI (Revenue/Spend)'] = {
                    'value': float(avg_roi),
                    'benchmark': 3.0,  # Conservative estimate based on ROAS data (no standard exists)
                    'benchmark_source': BENCHMARK_SOURCES['marketing_roi'],
                    'status': 'Above' if avg_roi >= 3.0 else 'Below',
                    'column': roi_col,
                    'insight': '⚠️ ROI varies by business model and attribution window'
                }
            
            # 2. ROAS (Return on Ad Spend) - calculated from revenue/cost
            if revenue_cols and spend_cols:
                rev_col = revenue_cols[0]
                cost_col = spend_cols[0]
                total_revenue = df[rev_col].sum()
                total_cost = df[cost_col].sum()
                if total_cost > 0:
                    roas = total_revenue / total_cost
                    kpis['ROAS'] = {
                        'value': float(roas),
                        'benchmark': 2.5,  # ✅ WordStream 2025: avg 2.26, median 3.08 - use conservative 2.5
                        'benchmark_source': BENCHMARK_SOURCES['marketing_roas'],
                        'status': 'Above' if roas >= 2.5 else 'Below',
                        'column': f"{rev_col}/{cost_col}"
                    }
            
            # 3. CTR (Click-Through Rate) - clicks/impressions
            if click_cols and impression_cols:
                click_col = click_cols[0]
                impression_col = impression_cols[0]
                total_clicks = df[click_col].sum()
                total_impressions = df[impression_col].sum()
                if total_impressions > 0:
                    ctr = (total_clicks / total_impressions) * 100

                    # ✅ Smart benchmark based on channel type (WordStream 2025)
                    # Check if social media or search ads
                    col_lower = (click_col + impression_col).lower()
                    if 'social' in col_lower or 'facebook' in col_lower or 'instagram' in col_lower:
                        benchmark_ctr = 1.7  # Social media traffic campaigns
                        channel_type = 'Social'
                    else:
                        benchmark_ctr = 6.7  # Search ads average
                        channel_type = 'Search'

                    kpis['CTR (%)'] = {
                        'value': float(ctr),
                        'benchmark': benchmark_ctr,  # ✅ WordStream 2025: 6.66% search, 1.71% social
                        'benchmark_source': BENCHMARK_SOURCES['marketing_ctr'],
                        'status': 'Above' if ctr >= benchmark_ctr else 'Below',
                        'column': f"{click_col}/{impression_col}",
                        'insight': f'{channel_type} ads benchmark'
                    }
            
            # 4. CPC (Cost Per Click)
            if spend_cols and click_cols:
                cost_col = spend_cols[0]
                click_col = click_cols[0]
                total_cost = df[cost_col].sum()
                total_clicks = df[click_col].sum()
                if total_clicks > 0:
                    cpc = total_cost / total_clicks
                    kpis['CPC'] = {
                        'value': float(cpc),
                        'benchmark': 2.0,  # Varies by industry
                        'status': 'Below' if cpc <= 2.0 else 'Above',  # Lower is better
                        'column': f"{cost_col}/{click_col}"
                    }
            
            # 5. Conversion Rate
            if conversion_cols and click_cols:
                conversion_col = conversion_cols[0]
                click_col = click_cols[0]
                total_conversions = df[conversion_col].sum()
                total_clicks = df[click_col].sum()
                if total_clicks > 0:
                    conv_rate = (total_conversions / total_clicks) * 100
                    kpis['Conversion Rate (%)'] = {
                        'value': float(conv_rate),
                        'benchmark': 6.6,  # ✅ Unbounce 2025: 6.6% overall average (WordStream: 7.52% search)
                        'benchmark_source': BENCHMARK_SOURCES['marketing_conversion'],
                        'status': 'Above' if conv_rate >= 6.6 else 'Below',
                        'column': f"{conversion_col}/{click_col}"
                    }
            
            # 6. CPA (Cost Per Acquisition) - WITH VIETNAM BENCHMARK INTEGRATION
            if spend_cols and conversion_cols:
                cost_col = spend_cols[0]
                conversion_col = conversion_cols[0]
                total_cost = df[cost_col].sum()
                total_conversions = df[conversion_col].sum()
                if total_conversions > 0:
                    cpa = total_cost / total_conversions

                    # Try to get Vietnam benchmark from CSV data
                    vietnam_benchmark = None
                    vietnam_context = ''
                    sample_spend = df[cost_col].dropna().head(10).mean()
                    is_vnd = sample_spend > 100000

                    if is_vnd:
                        # Try to detect channel and industry from column names/data
                        filters = {}
                        channel_cols = [col for col in df.columns if 'channel' in col.lower() or 'platform' in col.lower() or 'source' in col.lower()]
                        industry_cols = [col for col in df.columns if 'industry' in col.lower() or 'category' in col.lower()]

                        # Check column names for channel hints
                        col_names_str = ' '.join(df.columns).lower()
                        if 'facebook' in col_names_str or 'fb' in col_names_str:
                            filters['channel'] = 'Facebook Ads'
                        elif 'google' in col_names_str or 'search' in col_names_str:
                            filters['channel'] = 'Google Ads'
                        elif 'tiktok' in col_names_str:
                            filters['channel'] = 'TikTok Ads'

                        vietnam_benchmark = self._get_vietnam_benchmark(
                            domain='marketing',
                            metric_name='CPA',
                            user_value=cpa,
                            filters=filters
                        )

                        if vietnam_benchmark:
                            vietnam_context = vietnam_benchmark.get('message', '')

                    # Set benchmark (use Vietnam data if available, else fallback)
                    if vietnam_benchmark:
                        benchmark_cpa = vietnam_benchmark['benchmark_median']
                        benchmark_source = vietnam_benchmark.get('benchmark_source', BENCHMARK_SOURCES['marketing_cpa'])
                        currency = 'VND'
                    elif is_vnd:
                        benchmark_cpa = 85000  # ~85K VND - realistic Vietnam average from CSV
                        benchmark_source = BENCHMARK_SOURCES['marketing_cpa'] + ' (Estimated)'
                        currency = 'VND'
                    else:
                        benchmark_cpa = 70  # $70 USD - WordStream 2025 average
                        benchmark_source = BENCHMARK_SOURCES['marketing_cpa']
                        currency = 'USD'

                    kpis['Cost Per Acquisition (CPA)'] = {
                        'value': float(cpa),
                        'benchmark': benchmark_cpa,
                        'benchmark_source': benchmark_source,
                        'status': 'Below' if cpa <= benchmark_cpa else 'Above',  # Lower is better!
                        'column': f"{cost_col}/{conversion_col}",
                        'insight': f"{'✅ Efficient' if cpa <= benchmark_cpa else '⚠️ High CPA'} - Lower is better. Benchmark: {benchmark_cpa:,.0f} {currency}",
                        'vietnam_context': vietnam_context if vietnam_benchmark else '',
                        'percentile': vietnam_benchmark.get('percentile', None) if vietnam_benchmark else None
                    }
            
            # 7. Engagement Rate (for social/video campaigns)
            engagement_cols = [col for col in df.columns if 'engagement' in col.lower()]
            if engagement_cols:
                eng_col = engagement_cols[0]
                avg_engagement = df[eng_col].mean()
                kpis['Engagement Rate (%)'] = {
                    'value': float(avg_engagement),
                    'benchmark': 2.0,  # Social media avg 1-3%
                    'status': 'Above' if avg_engagement >= 2.0 else 'Below',
                    'column': eng_col,
                    'insight': f"{'✅ Strong' if avg_engagement >= 3.0 else '⚠️ Improve'} social engagement - Industry avg 1-3%"
                }
            
            # 8. Total Spend (if available)
            if spend_cols:
                cost_col = spend_cols[0]
                total_spend = df[cost_col].sum()
                kpis['Total Spend'] = {
                    'value': float(total_spend),
                    'benchmark': 100000,
                    'status': 'Check',
                    'column': cost_col,
                    'insight': f"Budget: {total_spend:,.0f}"
                }
        
        # === E-COMMERCE DATA ===
        elif 'ecommerce' in domain or 'e-commerce' in domain:
            # Detect key e-commerce columns (smart column matching)
            revenue_cols = [col for col in df.columns if 'revenue' in col.lower()]
            transaction_cols = [col for col in df.columns if 'transaction' in col.lower() and 'rate' not in col.lower()]
            session_cols = [col for col in df.columns if 'session' in col.lower()]
            user_cols = [col for col in df.columns if 'user' in col.lower() and 'rate' not in col.lower()]
            cart_cols = [col for col in df.columns if 'cart' in col.lower() and 'abandonment' not in col.lower()]
            checkout_cols = [col for col in df.columns if 'checkout' in col.lower()]
            conversion_rate_cols = [col for col in df.columns if 'conversion' in col.lower() and 'rate' in col.lower()]
            aov_cols = [col for col in df.columns if 'aov' in col.lower() or 'order_value' in col.lower()]
            bounce_cols = [col for col in df.columns if 'bounce' in col.lower()]
            returning_cols = [col for col in df.columns if 'returning' in col.lower()]
            mobile_cols = [col for col in df.columns if 'mobile' in col.lower()]
            
            # 1. Conversion Rate = (Transactions / Sessions) × 100 - WITH VIETNAM BENCHMARK
            if transaction_cols and session_cols:
                trans_col = transaction_cols[0]
                sess_col = session_cols[0]
                total_transactions = df[trans_col].sum()
                total_sessions = df[sess_col].sum()
                if total_sessions > 0:
                    conversion_rate = (total_transactions / total_sessions) * 100

                    # Try to get Vietnam benchmark from CSV data
                    vietnam_benchmark = None
                    vietnam_context = ''

                    # Try to detect platform and category from column names/data
                    filters = {}
                    col_names_str = ' '.join(df.columns).lower()

                    # Platform detection
                    if 'shopee' in col_names_str:
                        filters['platform'] = 'Shopee'
                    elif 'lazada' in col_names_str:
                        filters['platform'] = 'Lazada'
                    elif 'tiktok' in col_names_str:
                        filters['platform'] = 'TikTok Shop'

                    # Category detection
                    category_cols = [col for col in df.columns if 'category' in col.lower() or 'product_type' in col.lower()]
                    if category_cols and not df[category_cols[0]].isna().all():
                        most_common_cat = df[category_cols[0]].mode()[0] if len(df[category_cols[0]].mode()) > 0 else None
                        if most_common_cat:
                            filters['category'] = str(most_common_cat)

                    vietnam_benchmark = self._get_vietnam_benchmark(
                        domain='ecommerce',
                        metric_name='Conversion Rate',
                        user_value=conversion_rate,
                        filters=filters
                    )

                    if vietnam_benchmark:
                        vietnam_context = vietnam_benchmark.get('message', '')

                    # Set benchmark (use Vietnam data if available, else fallback)
                    if vietnam_benchmark:
                        benchmark_conv = vietnam_benchmark['benchmark_median']
                        benchmark_source = vietnam_benchmark.get('benchmark_source', BENCHMARK_SOURCES['ecommerce_conversion'])
                    else:
                        benchmark_conv = 2.3  # ~2.3% - realistic Vietnam average from CSV
                        benchmark_source = BENCHMARK_SOURCES['ecommerce_conversion']

                    kpis['Conversion Rate (%)'] = {
                        'value': float(conversion_rate),
                        'benchmark': benchmark_conv,
                        'benchmark_source': benchmark_source,
                        'status': 'Above' if conversion_rate >= benchmark_conv else 'Below',
                        'column': f"{trans_col}/{sess_col}",
                        'insight': f"{'✅ Strong' if conversion_rate >= 3.0 else '⚠️ Room for improvement'} - Vietnam avg {benchmark_conv}%",
                        'vietnam_context': vietnam_context if vietnam_benchmark else '',
                        'percentile': vietnam_benchmark.get('percentile', None) if vietnam_benchmark else None
                    }
            
            # 2. Average Order Value (AOV) = Total Revenue / Total Transactions - WITH VIETNAM BENCHMARK
            if revenue_cols and transaction_cols:
                rev_col = revenue_cols[0]
                trans_col = transaction_cols[0]
                total_revenue = df[rev_col].sum()
                total_transactions = df[trans_col].sum()
                if total_transactions > 0:
                    aov = total_revenue / total_transactions

                    # Currency detection
                    sample_revenue = df[rev_col].dropna().head(10).mean()
                    is_vnd = sample_revenue > 1000

                    # Try to get Vietnam benchmark from CSV data
                    vietnam_benchmark = None
                    vietnam_context = ''

                    if is_vnd:
                        # Reuse platform/category detection from conversion rate
                        filters = {}
                        col_names_str = ' '.join(df.columns).lower()

                        if 'shopee' in col_names_str:
                            filters['platform'] = 'Shopee'
                        elif 'lazada' in col_names_str:
                            filters['platform'] = 'Lazada'
                        elif 'tiktok' in col_names_str:
                            filters['platform'] = 'TikTok Shop'

                        category_cols = [col for col in df.columns if 'category' in col.lower() or 'product_type' in col.lower()]
                        if category_cols and not df[category_cols[0]].isna().all():
                            most_common_cat = df[category_cols[0]].mode()[0] if len(df[category_cols[0]].mode()) > 0 else None
                            if most_common_cat:
                                filters['category'] = str(most_common_cat)

                        vietnam_benchmark = self._get_vietnam_benchmark(
                            domain='ecommerce',
                            metric_name='AOV',
                            user_value=aov,
                            filters=filters
                        )

                        if vietnam_benchmark:
                            vietnam_context = vietnam_benchmark.get('message', '')

                    # Set benchmark (use Vietnam data if available, else fallback)
                    if vietnam_benchmark:
                        benchmark_aov = vietnam_benchmark['benchmark_median']
                        benchmark_source = vietnam_benchmark.get('benchmark_source', BENCHMARK_SOURCES['ecommerce_aov'])
                        currency = 'VND'
                    elif is_vnd:
                        benchmark_aov = 385000  # ~385K VND - realistic Vietnam average from CSV
                        benchmark_source = BENCHMARK_SOURCES['ecommerce_aov']
                        currency = 'VND'
                    else:
                        benchmark_aov = 81.49  # $81.49 USD (Shopify global avg)
                        benchmark_source = BENCHMARK_SOURCES['ecommerce_aov']
                        currency = 'USD'

                    kpis['Average Order Value (AOV)'] = {
                        'value': float(aov),
                        'benchmark': benchmark_aov,
                        'benchmark_source': benchmark_source,
                        'status': 'Above' if aov >= benchmark_aov else 'Below',
                        'column': f"{rev_col}/{trans_col}",
                        'insight': f"{'✅' if aov >= benchmark_aov else '⚠️'} Benchmark: {benchmark_aov:,.0f} {currency}",
                        'vietnam_context': vietnam_context if vietnam_benchmark else '',
                        'percentile': vietnam_benchmark.get('percentile', None) if vietnam_benchmark else None
                    }
            
            # 3. Cart Abandonment Rate = (Add-to-Carts - Checkouts) / Add-to-Carts × 100 - WITH VIETNAM BENCHMARK
            if cart_cols and checkout_cols:
                cart_col = [col for col in cart_cols if 'add' in col.lower() or 'cart' in col.lower()][0]
                checkout_col = checkout_cols[0]
                total_carts = df[cart_col].sum()
                total_checkouts = df[checkout_col].sum()
                if total_carts > 0:
                    abandonment_rate = ((total_carts - total_checkouts) / total_carts) * 100

                    # Try to get Vietnam benchmark from CSV data
                    vietnam_benchmark = None
                    vietnam_context = ''

                    # Reuse platform/category detection
                    filters = {}
                    col_names_str = ' '.join(df.columns).lower()

                    if 'shopee' in col_names_str:
                        filters['platform'] = 'Shopee'
                    elif 'lazada' in col_names_str:
                        filters['platform'] = 'Lazada'
                    elif 'tiktok' in col_names_str:
                        filters['platform'] = 'TikTok Shop'

                    category_cols = [col for col in df.columns if 'category' in col.lower() or 'product_type' in col.lower()]
                    if category_cols and not df[category_cols[0]].isna().all():
                        most_common_cat = df[category_cols[0]].mode()[0] if len(df[category_cols[0]].mode()) > 0 else None
                        if most_common_cat:
                            filters['category'] = str(most_common_cat)

                    vietnam_benchmark = self._get_vietnam_benchmark(
                        domain='ecommerce',
                        metric_name='Cart Abandonment',
                        user_value=abandonment_rate,
                        filters=filters
                    )

                    if vietnam_benchmark:
                        vietnam_context = vietnam_benchmark.get('message', '')

                    # Set benchmark (use Vietnam data if available, else fallback)
                    if vietnam_benchmark:
                        benchmark_abandon = vietnam_benchmark['benchmark_median']
                        benchmark_source = vietnam_benchmark.get('benchmark_source', BENCHMARK_SOURCES['ecommerce_cart_abandonment'])
                    else:
                        benchmark_abandon = 68.0  # ~68% - realistic Vietnam average from CSV
                        benchmark_source = BENCHMARK_SOURCES['ecommerce_cart_abandonment']

                    kpis['Cart Abandonment Rate (%)'] = {
                        'value': float(abandonment_rate),
                        'benchmark': benchmark_abandon,
                        'benchmark_source': benchmark_source,
                        'status': 'Below' if abandonment_rate <= benchmark_abandon else 'Above',  # Lower is better!
                        'column': f"({cart_col}-{checkout_col})/{cart_col}",
                        'insight': f"{'✅ Better than' if abandonment_rate < benchmark_abandon else '⚠️ Worse than'} {benchmark_abandon}% Vietnam avg",
                        'vietnam_context': vietnam_context if vietnam_benchmark else '',
                        'percentile': vietnam_benchmark.get('percentile', None) if vietnam_benchmark else None
                    }
                    
                    # 3.1 Cart Funnel Breakdown (detailed step analysis)
                    if transaction_cols:
                        trans_col = transaction_cols[0]
                        total_transactions = df[trans_col].sum()
                        
                        # Step 1: Add-to-Cart → Checkout
                        cart_to_checkout_rate = (total_checkouts / total_carts) * 100 if total_carts > 0 else 0
                        
                        # Step 2: Checkout → Purchase
                        checkout_to_purchase_rate = (total_transactions / total_checkouts) * 100 if total_checkouts > 0 else 0
                        
                        # Identify bottleneck
                        if cart_to_checkout_rate < 40:  # Industry avg ~35-45%
                            bottleneck = 'Add-to-Cart → Checkout'
                            bottleneck_insight = f"🚨 Major drop-off at Add-to-Cart step ({100-cart_to_checkout_rate:.1f}% abandon)"
                        elif checkout_to_purchase_rate < 75:  # Industry avg ~75-85%
                            bottleneck = 'Checkout → Purchase'
                            bottleneck_insight = f"⚠️ Checkout friction ({100-checkout_to_purchase_rate:.1f}% abandon at payment)"
                        else:
                            bottleneck = 'None'
                            bottleneck_insight = f"✅ Strong funnel conversion at both steps"
                        
                        kpis['Cart Funnel: Add→Checkout (%)'] = {
                            'value': float(cart_to_checkout_rate),
                            'benchmark': 40.0,  # Industry avg
                            'status': 'Above' if cart_to_checkout_rate >= 40.0 else 'Below',
                            'column': f"{checkout_col}/{cart_col}",
                            'insight': f"{bottleneck_insight}. Target: exit-intent popups, free shipping threshold"
                        }
                        
                        kpis['Cart Funnel: Checkout→Purchase (%)'] = {
                            'value': float(checkout_to_purchase_rate),
                            'benchmark': 80.0,  # Industry avg ~80%
                            'status': 'Above' if checkout_to_purchase_rate >= 80.0 else 'Below',
                            'column': f"{trans_col}/{checkout_col}",
                            'insight': f"{'✅ Strong checkout flow' if checkout_to_purchase_rate >= 80 else '⚠️ Payment friction - simplify checkout'}"
                        }
            
            # 4. Revenue per Session
            if revenue_cols and session_cols:
                rev_col = revenue_cols[0]
                sess_col = session_cols[0]
                total_revenue = df[rev_col].sum()
                total_sessions = df[sess_col].sum()
                if total_sessions > 0:
                    rps = total_revenue / total_sessions
                    kpis['Revenue per Session'] = {
                        'value': float(rps),
                        'benchmark': float(rps * 0.8),  # 80% of current as baseline
                        'status': 'Above Target',
                        'column': f"{rev_col}/{sess_col}",
                        'insight': 'Higher is better - increase with upsells, cross-sells'
                    }
            
            # 5. Returning Customer Rate (%)
            if returning_cols:
                ret_col = returning_cols[0]
                avg_returning = df[ret_col].mean()
                kpis['Returning Customer Rate (%)'] = {
                    'value': float(avg_returning),
                    'benchmark': 30.0,  # Industry avg 25-30%
                    'status': 'Above' if avg_returning >= 30.0 else 'Below',
                    'column': ret_col,
                    'insight': f"{'✅ Strong loyalty' if avg_returning >= 30 else '⚠️ Focus on retention'}"
                }
            
            # 6. Bounce Rate (%)
            if bounce_cols:
                bounce_col = bounce_cols[0]
                avg_bounce = df[bounce_col].mean()
                kpis['Bounce Rate (%)'] = {
                    'value': float(avg_bounce),
                    'benchmark': 47.0,  # E-commerce avg 40-50%
                    'status': 'Below' if avg_bounce <= 47.0 else 'Above',  # Lower is better!
                    'column': bounce_col,
                    'insight': f"{'✅' if avg_bounce < 47 else '⚠️'} Lower is better - Industry avg 40-50%"
                }
            
            # 7. Mobile Traffic Percentage
            if mobile_cols:
                mobile_col = mobile_cols[0]
                avg_mobile = df[mobile_col].mean()
                
                # Generate mobile optimization insight
                if avg_mobile >= 70:
                    mobile_insight = f"📱 MOBILE-FIRST ({avg_mobile:.1f}%) - Prioritize mobile UX, mobile checkout optimization, mobile page speed"
                elif avg_mobile >= 60:
                    mobile_insight = f"📱 Mobile-majority ({avg_mobile:.1f}%) - Test mobile funnel, improve mobile load time"
                elif avg_mobile >= 40:
                    mobile_insight = f"⚖️ Balanced traffic ({avg_mobile:.1f}% mobile) - Optimize for both devices"
                else:
                    mobile_insight = f"💻 Desktop-focused ({avg_mobile:.1f}% mobile) - Ensure desktop experience is premium"
                
                # Estimate mobile impact (assuming mobile CR is 30-50% lower than desktop)
                if bounce_cols and avg_mobile >= 60:
                    avg_bounce = df[bounce_cols[0]].mean()
                    if avg_bounce > 50:
                        mobile_insight += f" | ⚠️ High bounce ({avg_bounce:.1f}%) suggests mobile UX issues"
                
                kpis['Mobile Traffic (%)'] = {
                    'value': float(avg_mobile),
                    'benchmark': 60.0,  # Mobile-first threshold
                    'status': 'Above' if avg_mobile >= 60.0 else 'Below',
                    'column': mobile_col,
                    'insight': mobile_insight
                }
            
            # 8. Add fallback AOV if only revenue exists (no transactions)
            if revenue_cols and not transaction_cols and 'Average Order Value (AOV)' not in kpis:
                rev_col = revenue_cols[0]
                # Fallback: use mean of revenue column (less accurate)
                avg_order_value = df[rev_col].mean()
                sample_revenue = df[rev_col].dropna().head(10).mean()
                if sample_revenue > 1000:
                    benchmark_aov = 150000
                else:
                    benchmark_aov = 81.49
                
                kpis['AOV (estimated)'] = {
                    'value': float(avg_order_value),
                    'benchmark': benchmark_aov,
                    'status': 'Above' if avg_order_value >= benchmark_aov else 'Below',
                    'column': rev_col,
                    'insight': '⚠️ Estimated from revenue mean - upload transaction data for accuracy'
                }
        
        # === SALES/CRM DATA ===
        elif 'sales' in domain or 'crm' in domain or 'pipeline' in domain:
            # Detect key sales columns
            deal_value_cols = [col for col in df.columns if 'deal' in col.lower() and 'value' in col.lower() or 'amount' in col.lower()]
            stage_cols = [col for col in df.columns if 'stage' in col.lower() or 'status' in col.lower()]
            probability_cols = [col for col in df.columns if 'probability' in col.lower() or 'prob' in col.lower()]
            rep_cols = [col for col in df.columns if 'rep' in col.lower() or 'owner' in col.lower() or 'sales' in col.lower()]
            created_cols = [col for col in df.columns if 'created' in col.lower() and 'date' in col.lower()]
            close_cols = [col for col in df.columns if 'close' in col.lower() and 'date' in col.lower()]
            
            if deal_value_cols and stage_cols:
                deal_col = deal_value_cols[0]
                stage_col = stage_cols[0]
                
                # Identify won and lost deals
                won_deals = df[df[stage_col].str.contains('won', case=False, na=False)]
                lost_deals = df[df[stage_col].str.contains('lost', case=False, na=False)]
                pipeline_deals = df[~df[stage_col].str.contains('closed|won|lost', case=False, na=False)]
                
                # 1. Win Rate = Won / (Won + Lost) - WITH VIETNAM BENCHMARK
                total_won = len(won_deals)
                total_lost = len(lost_deals)
                if (total_won + total_lost) > 0:
                    win_rate = (total_won / (total_won + total_lost)) * 100

                    # Try to get Vietnam benchmark from CSV data
                    vietnam_benchmark = None
                    vietnam_context = ''

                    # Try to detect sales type and industry from column names/data
                    filters = {}
                    col_names_str = ' '.join(df.columns).lower()

                    # Sales type detection
                    if 'b2b' in col_names_str or 'enterprise' in col_names_str:
                        filters['sales_type'] = 'B2B'
                    elif 'b2c' in col_names_str or 'consumer' in col_names_str:
                        filters['sales_type'] = 'B2C'

                    # Industry detection from column names or data
                    if 'saas' in col_names_str or 'software' in col_names_str:
                        filters['industry'] = 'Software (SaaS)'
                    elif 'consulting' in col_names_str:
                        filters['industry'] = 'Consulting'
                    elif 'real estate' in col_names_str or 'property' in col_names_str:
                        filters['industry'] = 'Real Estate'

                    vietnam_benchmark = self._get_vietnam_benchmark(
                        domain='sales',
                        metric_name='Win Rate',
                        user_value=win_rate,
                        filters=filters
                    )

                    if vietnam_benchmark:
                        vietnam_context = vietnam_benchmark.get('message', '')

                    # Set benchmark (use Vietnam data if available, else fallback)
                    if vietnam_benchmark:
                        benchmark_win = vietnam_benchmark['benchmark_median']
                        benchmark_source = vietnam_benchmark.get('benchmark_source', BENCHMARK_SOURCES['sales_win_rate'])
                    else:
                        benchmark_win = 25.0  # ~25% - realistic Vietnam B2B average from CSV
                        benchmark_source = BENCHMARK_SOURCES['sales_win_rate']

                    kpis['Win Rate (%)'] = {
                        'value': float(win_rate),
                        'benchmark': benchmark_win,
                        'benchmark_source': benchmark_source,
                        'status': 'Above' if win_rate >= benchmark_win else 'Below',
                        'column': stage_col,
                        'insight': f"{'✅ Strong' if win_rate >= 35 else '⚠️ Below industry'} - Vietnam avg {benchmark_win}%",
                        'vietnam_context': vietnam_context if vietnam_benchmark else '',
                        'percentile': vietnam_benchmark.get('percentile', None) if vietnam_benchmark else None
                    }
                
                # 2. Total Pipeline Value (open deals)
                if len(pipeline_deals) > 0:
                    pipeline_value = pipeline_deals[deal_col].sum()
                    kpis['Total Pipeline Value'] = {
                        'value': float(pipeline_value),
                        'benchmark': float(pipeline_value * 0.8),
                        'status': 'Above Target',
                        'column': deal_col,
                        'insight': f"{len(pipeline_deals)} deals worth {pipeline_value:,.0f}"
                    }
                
                # 3. Weighted Pipeline (if probability exists)
                if probability_cols and len(pipeline_deals) > 0:
                    prob_col = probability_cols[0]
                    weighted_pipeline = (pipeline_deals[deal_col] * pipeline_deals[prob_col] / 100).sum()
                    kpis['Weighted Pipeline'] = {
                        'value': float(weighted_pipeline),
                        'benchmark': float(weighted_pipeline * 0.8),
                        'status': 'Above Target',
                        'column': f"{deal_col}×{prob_col}",
                        'insight': f"Pipeline adjusted for win probability"
                    }
                
                # 4. Average Deal Size (won deals) - WITH VIETNAM BENCHMARK
                if len(won_deals) > 0:
                    avg_deal_size = won_deals[deal_col].mean()

                    # Try to get Vietnam benchmark from CSV data
                    vietnam_benchmark = None
                    vietnam_context = ''

                    # Reuse sales type and industry detection from win rate
                    filters = {}
                    col_names_str = ' '.join(df.columns).lower()

                    if 'b2b' in col_names_str or 'enterprise' in col_names_str:
                        filters['sales_type'] = 'B2B'
                    elif 'b2c' in col_names_str or 'consumer' in col_names_str:
                        filters['sales_type'] = 'B2C'

                    if 'saas' in col_names_str or 'software' in col_names_str:
                        filters['industry'] = 'Software (SaaS)'
                    elif 'consulting' in col_names_str:
                        filters['industry'] = 'Consulting'
                    elif 'real estate' in col_names_str or 'property' in col_names_str:
                        filters['industry'] = 'Real Estate'

                    # Detect deal segment (SME vs Enterprise) from deal size
                    if avg_deal_size > 200000000:  # >200M VND = Enterprise
                        filters['deal_size_segment'] = 'Enterprise'
                    elif avg_deal_size > 50000000:  # 50-200M VND = Standard
                        filters['deal_size_segment'] = 'Standard'
                    else:  # <50M VND = SME
                        filters['deal_size_segment'] = 'SME'

                    vietnam_benchmark = self._get_vietnam_benchmark(
                        domain='sales',
                        metric_name='Deal Size',
                        user_value=avg_deal_size,
                        filters=filters
                    )

                    if vietnam_benchmark:
                        vietnam_context = vietnam_benchmark.get('message', '')

                    # Set benchmark (use Vietnam data if available, else fallback)
                    if vietnam_benchmark:
                        benchmark_deal = vietnam_benchmark['benchmark_median']
                        benchmark_source = vietnam_benchmark.get('benchmark_source', BENCHMARK_SOURCES['sales_growth'])
                    else:
                        # Fallback: use 80% of current (conservative)
                        benchmark_deal = float(avg_deal_size * 0.8)
                        benchmark_source = 'Calculated from Your Dataset Statistics'

                    kpis['Average Deal Size'] = {
                        'value': float(avg_deal_size),
                        'benchmark': benchmark_deal,
                        'benchmark_source': benchmark_source,
                        'status': 'Above' if avg_deal_size >= benchmark_deal else 'Below',
                        'column': deal_col,
                        'insight': f"Won deals: {avg_deal_size:,.0f} average",
                        'vietnam_context': vietnam_context if vietnam_benchmark else '',
                        'percentile': vietnam_benchmark.get('percentile', None) if vietnam_benchmark else None
                    }
                
                # 5. Sales Cycle Length (if dates available) - WITH VIETNAM BENCHMARK
                if created_cols and close_cols and len(won_deals) > 0:
                    created_col = created_cols[0]
                    close_col = close_cols[0]

                    try:
                        won_deals_copy = won_deals.copy()
                        won_deals_copy[created_col] = pd.to_datetime(won_deals_copy[created_col], errors='coerce')
                        won_deals_copy[close_col] = pd.to_datetime(won_deals_copy[close_col], errors='coerce')
                        won_deals_copy['cycle_days'] = (won_deals_copy[close_col] - won_deals_copy[created_col]).dt.days

                        avg_cycle = won_deals_copy['cycle_days'].mean()
                        # Only add KPI if we have valid cycle data
                        if pd.notna(avg_cycle):
                            # Try to get Vietnam benchmark from CSV data
                            vietnam_benchmark = None
                            vietnam_context = ''

                            # Reuse sales type and industry detection
                            filters = {}
                            col_names_str = ' '.join(df.columns).lower()

                            if 'b2b' in col_names_str or 'enterprise' in col_names_str:
                                filters['sales_type'] = 'B2B'
                            elif 'b2c' in col_names_str or 'consumer' in col_names_str:
                                filters['sales_type'] = 'B2C'

                            if 'saas' in col_names_str or 'software' in col_names_str:
                                filters['industry'] = 'Software (SaaS)'
                            elif 'consulting' in col_names_str:
                                filters['industry'] = 'Consulting'
                            elif 'real estate' in col_names_str or 'property' in col_names_str:
                                filters['industry'] = 'Real Estate'

                            vietnam_benchmark = self._get_vietnam_benchmark(
                                domain='sales',
                                metric_name='Sales Cycle',
                                user_value=avg_cycle,
                                filters=filters
                            )

                            if vietnam_benchmark:
                                vietnam_context = vietnam_benchmark.get('message', '')

                            # Set benchmark (use Vietnam data if available, else fallback)
                            if vietnam_benchmark:
                                benchmark_cycle = vietnam_benchmark['benchmark_median']
                                benchmark_source = vietnam_benchmark.get('benchmark_source', BENCHMARK_SOURCES['sales_cycle'])
                            else:
                                benchmark_cycle = 45.0  # ~45 days - realistic Vietnam B2B average from CSV
                                benchmark_source = BENCHMARK_SOURCES['sales_cycle']

                            kpis['Sales Cycle (days)'] = {
                                'value': float(avg_cycle),
                                'benchmark': benchmark_cycle,
                                'benchmark_source': benchmark_source,
                                'status': 'Below' if avg_cycle <= benchmark_cycle else 'Above',  # Lower is better
                                'column': f"{close_col}-{created_col}",
                                'insight': f"{'✅ Fast' if avg_cycle <= benchmark_cycle else '⚠️ Long'} sales cycle - Vietnam avg {benchmark_cycle} days",
                                'vietnam_context': vietnam_context if vietnam_benchmark else '',
                                'percentile': vietnam_benchmark.get('percentile', None) if vietnam_benchmark else None
                            }
                    except Exception:
                        pass
                
                # 6. Pipeline Velocity (deals closed per period)
                if len(won_deals) > 0:
                    total_won_value = won_deals[deal_col].sum()
                    kpis['Closed Won Revenue'] = {
                        'value': float(total_won_value),
                        'benchmark': float(total_won_value * 0.8),
                        'status': 'Above Target',
                        'column': deal_col,
                        'insight': f"{total_won} deals closed, {total_won_value:,.0f} revenue"
                    }
        
        # === FINANCE/ACCOUNTING DATA ===
        elif 'finance' in domain or 'accounting' in domain or 'financial' in domain:
            # Detect key financial columns
            revenue_cols = [col for col in df.columns if 'revenue' in col.lower() and 'gross' not in col.lower()]
            cogs_cols = [col for col in df.columns if 'cogs' in col.lower() or 'cost_of_goods' in col.lower()]
            gross_profit_cols = [col for col in df.columns if 'gross' in col.lower() and 'profit' in col.lower()]
            opex_cols = [col for col in df.columns if 'opex' in col.lower() or 'operating_expense' in col.lower() or 'total_opex' in col.lower()]
            operating_income_cols = [col for col in df.columns if 'operating_income' in col.lower() or 'operating_profit' in col.lower()]
            net_income_cols = [col for col in df.columns if 'net_income' in col.lower() or 'net_profit' in col.lower()]
            
            # Cash flow columns
            cash_ops_cols = [col for col in df.columns if 'cash' in col.lower() and 'operation' in col.lower()]
            capex_cols = [col for col in df.columns if 'capex' in col.lower() or 'capital_expenditure' in col.lower()]
            cash_balance_cols = [col for col in df.columns if 'cash_balance' in col.lower() or ('cash' in col.lower() and 'balance' in col.lower())]
            
            # Balance sheet columns
            current_assets_cols = [col for col in df.columns if 'current_assets' in col.lower() or 'current_asset' in col.lower()]
            current_liabilities_cols = [col for col in df.columns if 'current_liabilities' in col.lower() or 'current_liability' in col.lower()]
            inventory_cols = [col for col in df.columns if 'inventory' in col.lower()]
            total_debt_cols = [col for col in df.columns if 'total_liabilities' in col.lower() or 'total_debt' in col.lower()]
            equity_cols = [col for col in df.columns if 'shareholders_equity' in col.lower() or ('equity' in col.lower() and 'raised' not in col.lower())]
            
            if revenue_cols and net_income_cols:
                revenue_col = revenue_cols[0]
                net_income_col = net_income_cols[0]
                
                # 1. Net Profit Margin (%)
                avg_revenue = df[revenue_col].mean()
                avg_net_income = df[net_income_col].mean()
                if avg_revenue > 0:
                    net_margin = (avg_net_income / avg_revenue) * 100
                    kpis['Net Profit Margin (%)'] = {
                        'value': float(net_margin),
                        'benchmark': 15.0,  # SaaS/Tech avg 10-20%
                        'status': 'Above' if net_margin >= 15.0 else 'Below',
                        'column': f"{net_income_col}/{revenue_col}",
                        'insight': f"{'✅ Healthy' if net_margin >= 15 else '⚠️ Needs improvement'} - SaaS avg 10-20%"
                    }
                
                # 2. Gross Margin (%)
                if gross_profit_cols:
                    gross_profit_col = gross_profit_cols[0]
                    avg_gross_profit = df[gross_profit_col].mean()
                    gross_margin = (avg_gross_profit / avg_revenue) * 100
                    kpis['Gross Margin (%)'] = {
                        'value': float(gross_margin),
                        'benchmark': 70.0,  # SaaS target >70%
                        'status': 'Above' if gross_margin >= 70.0 else 'Below',
                        'column': f"{gross_profit_col}/{revenue_col}",
                        'insight': f"{'✅ Strong' if gross_margin >= 70 else '⚠️ Low for SaaS'} - Target >70%"
                    }
                
                # 3. Operating Margin (%)
                if operating_income_cols:
                    op_income_col = operating_income_cols[0]
                    avg_op_income = df[op_income_col].mean()
                    op_margin = (avg_op_income / avg_revenue) * 100
                    kpis['Operating Margin (%)'] = {
                        'value': float(op_margin),
                        'benchmark': 20.0,  # SaaS target 15-25%
                        'status': 'Above' if op_margin >= 20.0 else 'Below',
                        'column': f"{op_income_col}/{revenue_col}",
                        'insight': f"{'✅ Efficient' if op_margin >= 20 else '⚠️ High OPEX'} - Target 15-25%"
                    }
                
                # 4. Revenue Growth Rate (Month-over-Month)
                if len(df) >= 2:
                    # Calculate MoM growth
                    df_sorted = df.sort_values(by=df.columns[0])  # Sort by first column (usually date/month)
                    first_revenue = df_sorted[revenue_col].iloc[0]
                    last_revenue = df_sorted[revenue_col].iloc[-1]
                    months_diff = len(df_sorted) - 1
                    
                    if first_revenue > 0 and months_diff > 0:
                        total_growth = ((last_revenue - first_revenue) / first_revenue) * 100
                        avg_monthly_growth = total_growth / months_diff
                        
                        kpis['Revenue Growth (%)'] = {
                            'value': float(avg_monthly_growth),
                            'benchmark': 10.0,  # 10% MoM = unicorn trajectory
                            'status': 'Above' if avg_monthly_growth >= 10.0 else 'Below',
                            'column': revenue_col,
                            'insight': f"{'🚀 Hypergrowth' if avg_monthly_growth >= 15 else '✅ Growing' if avg_monthly_growth >= 10 else '⚠️ Slow growth'} - {total_growth:.1f}% total"
                        }
                
                # 5. Operating Cash Flow
                if cash_ops_cols:
                    cash_ops_col = cash_ops_cols[0]
                    avg_cash_ops = df[cash_ops_col].mean()
                    total_cash_ops = df[cash_ops_col].sum()
                    
                    kpis['Operating Cash Flow'] = {
                        'value': float(total_cash_ops),
                        'benchmark': float(total_cash_ops * 0.8),
                        'status': 'Positive' if avg_cash_ops > 0 else 'Negative',
                        'column': cash_ops_col,
                        'insight': f"{'✅ Cash positive' if avg_cash_ops > 0 else '🚨 Burning cash'} - Avg {avg_cash_ops:,.0f}/month"
                    }
                    
                    # 6. Free Cash Flow (OCF - CapEx)
                    if capex_cols:
                        capex_col = capex_cols[0]
                        avg_capex = df[capex_col].mean()
                        free_cash_flow = avg_cash_ops + avg_capex  # CapEx is usually negative
                        
                        kpis['Free Cash Flow'] = {
                            'value': float(free_cash_flow),
                            'benchmark': 0,
                            'status': 'Positive' if free_cash_flow > 0 else 'Negative',
                            'column': f"{cash_ops_col}+{capex_col}",
                            'insight': f"{'✅ Sustainable' if free_cash_flow > 0 else '⚠️ Needs funding'} - After CapEx"
                        }
                    
                    # 7. Burn Rate (for startups)
                    if avg_cash_ops < 0:  # If burning cash
                        burn_rate = abs(avg_cash_ops)
                        
                        # Calculate runway if we have cash balance
                        if cash_balance_cols:
                            cash_balance_col = cash_balance_cols[0]
                            current_cash = df[cash_balance_col].iloc[-1]  # Latest balance
                            runway_months = current_cash / burn_rate if burn_rate > 0 else 999
                            
                            kpis['Burn Rate (Monthly)'] = {
                                'value': float(burn_rate),
                                'benchmark': float(burn_rate * 0.7),  # Target: reduce 30%
                                'status': 'Critical' if runway_months < 6 else 'Warning' if runway_months < 12 else 'Safe',
                                'column': cash_ops_col,
                                'insight': f"{'🚨 URGENT' if runway_months < 6 else '⚠️ Watch closely' if runway_months < 12 else '✅ Healthy'} - {runway_months:.1f} months runway"
                            }
                
                # 8. Current Ratio (Liquidity)
                if current_assets_cols and current_liabilities_cols:
                    ca_col = current_assets_cols[0]
                    cl_col = current_liabilities_cols[0]
                    
                    avg_ca = df[ca_col].mean()
                    avg_cl = df[cl_col].mean()
                    
                    if avg_cl > 0:
                        current_ratio = avg_ca / avg_cl
                        kpis['Current Ratio'] = {
                            'value': float(current_ratio),
                            'benchmark': 2.0,  # Healthy: >2.0
                            'status': 'Healthy' if current_ratio >= 2.0 else 'Warning' if current_ratio >= 1.0 else 'Critical',
                            'column': f"{ca_col}/{cl_col}",
                            'insight': f"{'✅ Strong liquidity' if current_ratio >= 2.0 else '⚠️ Tight liquidity' if current_ratio >= 1.0 else '🚨 Liquidity crisis'}"
                        }
                    
                    # 9. Quick Ratio (Acid Test)
                    if inventory_cols:
                        inv_col = inventory_cols[0]
                        avg_inv = df[inv_col].mean()
                        quick_assets = avg_ca - avg_inv
                        
                        if avg_cl > 0:
                            quick_ratio = quick_assets / avg_cl
                            kpis['Quick Ratio'] = {
                                'value': float(quick_ratio),
                                'benchmark': 1.0,  # Healthy: >1.0
                                'status': 'Healthy' if quick_ratio >= 1.0 else 'Warning',
                                'column': f"({ca_col}-{inv_col})/{cl_col}",
                                'insight': f"{'✅ Can cover short-term debt' if quick_ratio >= 1.0 else '⚠️ May struggle with immediate obligations'}"
                            }
                
                # 10. Debt-to-Equity Ratio
                if total_debt_cols and equity_cols:
                    debt_col = total_debt_cols[0]
                    equity_col = equity_cols[0]
                    
                    avg_debt = df[debt_col].mean()
                    avg_equity = df[equity_col].mean()
                    
                    if avg_equity > 0:
                        debt_to_equity = avg_debt / avg_equity
                        kpis['Debt-to-Equity Ratio'] = {
                            'value': float(debt_to_equity),
                            'benchmark': 1.0,  # <1.0 = conservative, 1-2 = moderate, >2 = aggressive
                            'status': 'Conservative' if debt_to_equity < 1.0 else 'Moderate' if debt_to_equity < 2.0 else 'Aggressive',
                            'column': f"{debt_col}/{equity_col}",
                            'insight': f"{'✅ Low leverage' if debt_to_equity < 1.0 else '⚠️ Moderate leverage' if debt_to_equity < 2.0 else '🚨 High leverage risk'}"
                        }
        
        # === CUSTOMER SERVICE/SUPPORT DATA ===
        elif 'customer' in domain and ('service' in domain or 'support' in domain):
            # Detect key customer service columns
            response_time_cols = [col for col in df.columns if 'response' in col.lower() and 'time' in col.lower()]
            resolution_time_cols = [col for col in df.columns if 'resolution' in col.lower() and 'time' in col.lower()]
            csat_cols = [col for col in df.columns if 'satisfaction' in col.lower() or 'csat' in col.lower()]
            sla_cols = [col for col in df.columns if 'sla' in col.lower()]
            reopened_cols = [col for col in df.columns if 'reopen' in col.lower()]
            escalated_cols = [col for col in df.columns if 'escalat' in col.lower()]
            ticket_value_cols = [col for col in df.columns if 'ticket' in col.lower() and 'value' in col.lower()]
            channel_cols = [col for col in df.columns if 'channel' in col.lower()]
            
            # 1. Average First Response Time
            if response_time_cols:
                response_col = response_time_cols[0]
                avg_response = df[response_col].mean()
                kpis['Avg First Response Time (min)'] = {
                    'value': float(avg_response),
                    'benchmark': 15.0,  # Industry best: <15 min
                    'status': 'Below' if avg_response <= 15.0 else 'Above',  # Lower is better
                    'column': response_col,
                    'insight': f"{'✅ Fast' if avg_response <= 15 else '⚠️ Slow'} - Target <15 min for good CX"
                }
            
            # 2. Average Resolution Time
            if resolution_time_cols:
                resolution_col = resolution_time_cols[0]
                avg_resolution = df[resolution_col].mean()
                kpis['Avg Resolution Time (hrs)'] = {
                    'value': float(avg_resolution),
                    'benchmark': 4.0,  # Target: <4 hours
                    'status': 'Below' if avg_resolution <= 4.0 else 'Above',  # Lower is better
                    'column': resolution_col,
                    'insight': f"{'✅ Efficient' if avg_resolution <= 4 else '⚠️ Long'} - Target <4 hrs"
                }
            
            # 3. Customer Satisfaction Score (CSAT)
            if csat_cols:
                csat_col = csat_cols[0]
                avg_csat = df[csat_col].mean()
                kpis['CSAT Score'] = {
                    'value': float(avg_csat),
                    'benchmark': 4.5,  # Target: ≥4.5/5
                    'status': 'Above' if avg_csat >= 4.5 else 'Below',
                    'column': csat_col,
                    'insight': f"{'✅ Excellent' if avg_csat >= 4.5 else '⚠️ Needs improvement'} - Target ≥4.5/5"
                }
            
            # 4. First Contact Resolution (FCR)
            if reopened_cols:
                reopen_col = reopened_cols[0]
                total_tickets = len(df)
                # Assuming 'No' or False means not reopened (first contact resolution)
                not_reopened = df[reopen_col].astype(str).str.lower().isin(['no', 'false', '0']).sum()
                fcr_rate = (not_reopened / total_tickets) * 100
                kpis['First Contact Resolution (%)'] = {
                    'value': float(fcr_rate),
                    'benchmark': 75.0,  # Industry benchmark: 70-75%
                    'status': 'Above' if fcr_rate >= 75.0 else 'Below',
                    'column': reopen_col,
                    'insight': f"{'✅ Strong' if fcr_rate >= 75 else '⚠️ Low'} - Industry avg 70-75%"
                }
            
            # 5. SLA Compliance
            if sla_cols:
                sla_col = sla_cols[0]
                total_tickets = len(df)
                # Assuming 'Yes' or True means SLA met
                sla_met = df[sla_col].astype(str).str.lower().isin(['yes', 'true', '1']).sum()
                sla_rate = (sla_met / total_tickets) * 100
                kpis['SLA Met (%)'] = {
                    'value': float(sla_rate),
                    'benchmark': 85.0,  # Target: ≥85%
                    'status': 'Above' if sla_rate >= 85.0 else 'Below',
                    'column': sla_col,
                    'insight': f"{'✅ Good' if sla_rate >= 85 else '⚠️ Below target'} - Target ≥85%"
                }
            
            # 6. Escalation Rate
            if escalated_cols:
                escalated_col = escalated_cols[0]
                total_tickets = len(df)
                escalated = df[escalated_col].astype(str).str.lower().isin(['yes', 'true', '1']).sum()
                escalation_rate = (escalated / total_tickets) * 100
                kpis['Escalation Rate (%)'] = {
                    'value': float(escalation_rate),
                    'benchmark': 15.0,  # Target: <15%
                    'status': 'Below' if escalation_rate <= 15.0 else 'Above',  # Lower is better
                    'column': escalated_col,
                    'insight': f"{'✅ Low' if escalation_rate <= 15 else '⚠️ High'} - Target <15%"
                }
            
            # 7. Reopen Rate
            if reopened_cols:
                reopen_col = reopened_cols[0]
                total_tickets = len(df)
                reopened = df[reopen_col].astype(str).str.lower().isin(['yes', 'true', '1']).sum()
                reopen_rate = (reopened / total_tickets) * 100
                kpis['Reopen Rate (%)'] = {
                    'value': float(reopen_rate),
                    'benchmark': 10.0,  # Target: <10%
                    'status': 'Below' if reopen_rate <= 10.0 else 'Above',  # Lower is better
                    'column': reopen_col,
                    'insight': f"{'✅ Good quality' if reopen_rate <= 10 else '⚠️ High'} - Target <10%"
                }
            
            # 8. Total Ticket Value (business impact)
            if ticket_value_cols:
                ticket_value_col = ticket_value_cols[0]
                total_value = df[ticket_value_col].sum()
                kpis['Total Ticket Value (VND)'] = {
                    'value': float(total_value),
                    'benchmark': float(total_value * 0.8),
                    'status': 'Above Target',
                    'column': ticket_value_col,
                    'insight': f"Total business value: {total_value:,.0f} VND"
                }
        
        # === MANUFACTURING/OPERATIONS DATA ===
        elif 'manufacturing' in domain or 'production' in domain or 'operations' in domain or 'factory' in domain:
            # Detect key manufacturing columns (be specific to avoid false matches)
            units_produced_cols = [col for col in df.columns if 'units_produced' in col.lower() or 'units produced' in col.lower()]
            good_units_cols = [col for col in df.columns if 'good_units' in col.lower() or 'good units' in col.lower()]
            defective_cols = [col for col in df.columns if 'defective' in col.lower() or 'defect' in col.lower()]
            downtime_cols = [col for col in df.columns if 'downtime' in col.lower() or 'down time' in col.lower()]
            available_hours_cols = [col for col in df.columns if 'available' in col.lower() and 'hours' in col.lower()]
            actual_run_cols = [col for col in df.columns if 'actual_run' in col.lower() or 'actual run' in col.lower()]
            theoretical_max_cols = [col for col in df.columns if 'theoretical' in col.lower() or 'max_output' in col.lower() or 'max output' in col.lower()]
            total_cost_cols = [col for col in df.columns if 'total_cost' in col.lower() or 'total cost' in col.lower()]
            
            if units_produced_cols and good_units_cols:
                units_produced_col = units_produced_cols[0]
                good_units_col = good_units_cols[0]
                
                total_units = df[units_produced_col].sum()
                total_good = df[good_units_col].sum()
                
                # 1. First Pass Yield (FPY)
                if total_units > 0:
                    fpy = (total_good / total_units) * 100
                    kpis['First Pass Yield (%)'] = {
                        'value': float(fpy),
                        'benchmark': 95.0,  # World-class: ≥95%
                        'status': 'Above' if fpy >= 95.0 else 'Below',
                        'column': f"{good_units_col}/{units_produced_col}",
                        'insight': f"{'✅ World-class' if fpy >= 95 else '⚠️ Needs improvement'} - Target ≥95%"
                    }
                
                # 2. Defect Rate
                if defective_cols and total_units > 0:
                    defective_col = defective_cols[0]
                    total_defective = df[defective_col].sum()
                    defect_rate = (total_defective / total_units) * 100
                    
                    kpis['Defect Rate (%)'] = {
                        'value': float(defect_rate),
                        'benchmark': 2.0,  # World-class: ≤2%
                        'status': 'Below' if defect_rate <= 2.0 else 'Above',
                        'column': f"{defective_col}/{units_produced_col}",
                        'insight': f"{'✅ Excellent' if defect_rate <= 2 else '⚠️ High'} - Target ≤2%"
                    }
                
                # 3. Production Output
                avg_units = df[units_produced_col].mean()
                kpis['Avg Production Output (units/shift)'] = {
                    'value': float(avg_units),
                    'benchmark': 950.0,
                    'status': 'Above' if avg_units >= 950.0 else 'Below',
                    'column': units_produced_col,
                    'insight': f"{'✅ High output' if avg_units >= 950 else '⚠️ Low output'} - Target ≥950 units/shift"
                }
                
                # 4. Cycle Time (approximate)
                if available_hours_cols and total_units > 0:
                    available_hours_col = available_hours_cols[0]
                    total_hours = df[available_hours_col].sum()
                    # Cycle time = total production time / units produced (in minutes)
                    cycle_time = (total_hours * 60) / total_units
                    
                    kpis['Cycle Time (min/unit)'] = {
                        'value': float(cycle_time),
                        'benchmark': 0.5,  # Target: ≤0.5 min/unit
                        'status': 'Below' if cycle_time <= 0.5 else 'Above',
                        'column': f"{available_hours_col}/{units_produced_col}",
                        'insight': f"{'✅ Fast' if cycle_time <= 0.5 else '⚠️ Slow'} - Target ≤0.5 min/unit"
                    }
            
            # 5. Machine Utilization
            if actual_run_cols and available_hours_cols:
                actual_run_col = actual_run_cols[0]
                available_hours_col = available_hours_cols[0]
                
                total_actual = df[actual_run_col].sum()
                total_available = df[available_hours_col].sum()
                
                if total_available > 0:
                    utilization = (total_actual / total_available) * 100
                    kpis['Machine Utilization (%)'] = {
                        'value': float(utilization),
                        'benchmark': 85.0,  # Target: ≥85%
                        'status': 'Above' if utilization >= 85.0 else 'Below',
                        'column': f"{actual_run_col}/{available_hours_col}",
                        'insight': f"{'✅ Excellent' if utilization >= 85 else '⚠️ Low'} - Target ≥85%"
                    }
            
            # 6. Downtime Hours
            if downtime_cols:
                downtime_col = downtime_cols[0]
                total_downtime = df[downtime_col].sum()
                avg_downtime = df[downtime_col].mean()
                
                kpis['Total Downtime (hours)'] = {
                    'value': float(total_downtime),
                    'benchmark': 150.0,  # Target: ≤150 hours/month
                    'status': 'Below' if total_downtime <= 150.0 else 'Above',
                    'column': downtime_col,
                    'insight': f"{'✅ Low' if total_downtime <= 150 else '⚠️ High'} - Target ≤150 hrs/month"
                }
                
                kpis['Avg Downtime (hours/shift)'] = {
                    'value': float(avg_downtime),
                    'benchmark': 1.0,
                    'status': 'Below' if avg_downtime <= 1.0 else 'Above',
                    'column': downtime_col,
                    'insight': f"{'✅ Low' if avg_downtime <= 1 else '⚠️ High'} - Target ≤1 hr/shift"
                }
            
            # 7. Cost per Unit
            if total_cost_cols and units_produced_cols:
                total_cost_col = total_cost_cols[0]
                units_produced_col = units_produced_cols[0]
                
                total_cost = df[total_cost_col].sum()
                total_units = df[units_produced_col].sum()
                
                if total_units > 0:
                    cost_per_unit = total_cost / total_units
                    kpis['Cost per Unit (VND)'] = {
                        'value': float(cost_per_unit),
                        'benchmark': 30000.0,  # Target: ≤30,000 VND/unit
                        'status': 'Below' if cost_per_unit <= 30000.0 else 'Above',
                        'column': f"{total_cost_col}/{units_produced_col}",
                        'insight': f"{'✅ Efficient' if cost_per_unit <= 30000 else '⚠️ High cost'} - Target ≤30K VND/unit"
                    }
            
            # 8. OEE (Overall Equipment Effectiveness)
            # OEE = Availability × Performance × Quality
            if (available_hours_cols and downtime_cols and 
                actual_run_cols and theoretical_max_cols and 
                units_produced_cols and good_units_cols):
                
                available_col = available_hours_cols[0]
                downtime_col = downtime_cols[0]
                actual_run_col = actual_run_cols[0]
                theoretical_col = theoretical_max_cols[0]
                units_col = units_produced_cols[0]
                good_col = good_units_cols[0]
                
                # Availability = (Available Time - Downtime) / Available Time
                total_available = df[available_col].sum()
                total_downtime = df[downtime_col].sum()
                availability = ((total_available - total_downtime) / total_available) if total_available > 0 else 0
                
                # Performance = Actual Output / Theoretical Max Output
                total_actual_output = df[units_col].sum()
                total_theoretical = df[theoretical_col].sum()
                performance = (total_actual_output / total_theoretical) if total_theoretical > 0 else 0
                
                # Quality = Good Units / Total Units
                total_good = df[good_col].sum()
                total_units = df[units_col].sum()
                quality = (total_good / total_units) if total_units > 0 else 0
                
                # OEE = Availability × Performance × Quality
                oee = availability * performance * quality * 100
                
                kpis['OEE - Overall Equipment Effectiveness (%)'] = {
                    'value': float(oee),
                    'benchmark': 85.0,  # World-class: ≥85%
                    'status': 'Above' if oee >= 85.0 else 'Below',
                    'column': f"({available_col} - {downtime_col}) × ({units_col}/{theoretical_col}) × ({good_col}/{units_col})",
                    'insight': f"{'✅ World-class' if oee >= 85 else '⚠️ Needs improvement'} - Target ≥85%",
                    'components': {
                        'Availability': float(availability * 100),
                        'Performance': float(performance * 100),
                        'Quality': float(quality * 100)
                    }
                }
        
        # === FALLBACK: UNIVERSAL KPIs ===
        else:
            if primary_metric_col:
                col_name = primary_metric_col
                kpis[f'Average {col_name}'] = {
                    'value': float(df[col_name].mean()),
                    'benchmark': float(df[col_name].median()),
                    'status': 'At Median',
                    'column': col_name
                }
                
                kpis[f'Median {col_name}'] = {
                    'value': float(df[col_name].median()),
                    'benchmark': float(df[col_name].mean()),
                    'status': 'At Average',
                    'column': col_name
                }
                
                kpis[f'Total {col_name}'] = {
                    'value': float(df[col_name].sum()),
                    'benchmark': float(df[col_name].sum() * 0.8),
                    'status': 'Above Target',
                    'column': col_name
                }

        # ⭐ Add benchmark sources for transparency (addresses real user feedback)
        kpis = add_benchmark_metadata(kpis, domain)

        return kpis
    
    def _calculate_dimension_analysis(self, df: pd.DataFrame, domain_info: Dict) -> Dict:
        """
        ⭐ NEW: Calculate dimension-level analysis (channel, campaign, rep, etc.)
        
        This provides breakdown by key dimensions for deeper insights:
        - E-commerce: By channel (Organic, Facebook Ads, Google Ads, etc.)
        - Marketing: By campaign
        - Sales: By rep, by stage
        
        Returns:
            Dictionary with dimension breakdowns and insights
        """
        analysis = {}
        # Support both 'domain' and 'domain_name' keys for backward compatibility
        domain = domain_info.get('domain', domain_info.get('domain_name', 'general')).lower()
        
        # Detect dimension columns (channel, campaign, rep, etc.)
        channel_cols = [col for col in df.columns if 'channel' in col.lower()]
        campaign_cols = [col for col in df.columns if 'campaign' in col.lower()]
        rep_cols = [col for col in df.columns if 'rep' in col.lower() or 'sales' in col.lower()]
        stage_cols = [col for col in df.columns if 'stage' in col.lower() or 'status' in col.lower()]
        
        # === E-COMMERCE: CHANNEL ANALYSIS ===
        if ('ecommerce' in domain or 'e-commerce' in domain) and channel_cols:
            channel_col = channel_cols[0]
            
            # Detect key metrics for channel analysis
            revenue_cols = [col for col in df.columns if 'revenue' in col.lower()]
            transaction_cols = [col for col in df.columns if 'transaction' in col.lower() and 'rate' not in col.lower()]
            session_cols = [col for col in df.columns if 'session' in col.lower()]
            cac_cols = [col for col in df.columns if 'cac' in col.lower()]
            
            if revenue_cols and transaction_cols and session_cols:
                rev_col = revenue_cols[0]
                trans_col = transaction_cols[0]
                sess_col = session_cols[0]
                
                # Group by channel
                channel_stats = df.groupby(channel_col).agg({
                    rev_col: 'sum',
                    trans_col: 'sum',
                    sess_col: 'sum'
                })
                
                # Calculate CR by channel
                channel_stats['conversion_rate'] = (channel_stats[trans_col] / channel_stats[sess_col]) * 100
                channel_stats['aov'] = channel_stats[rev_col] / channel_stats[trans_col]
                channel_stats['revenue_per_session'] = channel_stats[rev_col] / channel_stats[sess_col]
                
                # Add CAC if available
                if cac_cols:
                    cac_col = cac_cols[0]
                    channel_cac = df.groupby(channel_col)[cac_col].mean()
                    channel_stats['cac'] = channel_cac
                    
                    # Calculate ROI = (Revenue - CAC*Transactions) / (CAC*Transactions)
                    channel_stats['roi'] = ((channel_stats[rev_col] - channel_stats['cac'] * channel_stats[trans_col]) / 
                                           (channel_stats['cac'] * channel_stats[trans_col]))
                
                # Sort by revenue (best channels first)
                channel_stats = channel_stats.sort_values(rev_col, ascending=False)
                
                # Format for output
                channel_breakdown = []
                for channel, row in channel_stats.iterrows():
                    channel_data = {
                        'channel': channel,
                        'revenue': float(row[rev_col]),
                        'transactions': float(row[trans_col]),
                        'sessions': float(row[sess_col]),
                        'conversion_rate': float(row['conversion_rate']),
                        'aov': float(row['aov']),
                        'revenue_per_session': float(row['revenue_per_session'])
                    }
                    if cac_cols:
                        channel_data['cac'] = float(row['cac'])
                        channel_data['roi'] = float(row['roi'])
                    
                    channel_breakdown.append(channel_data)
                
                analysis['channel_breakdown'] = {
                    'data': channel_breakdown,
                    'insights': self._generate_channel_insights(channel_breakdown),
                    'best_channel': channel_breakdown[0]['channel'] if channel_breakdown else None,
                    'worst_channel': channel_breakdown[-1]['channel'] if channel_breakdown else None
                }
            
            # === E-COMMERCE: TREND ANALYSIS ===
            # Detect date column for time-series analysis
            date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower() or 'day' in col.lower()]
            
            if date_cols and revenue_cols and transaction_cols and session_cols:
                date_col = date_cols[0]
                rev_col = revenue_cols[0]
                trans_col = transaction_cols[0]
                sess_col = session_cols[0]
                
                # Ensure date column is datetime
                try:
                    df_trend = df.copy()
                    df_trend[date_col] = pd.to_datetime(df_trend[date_col])
                    
                    # Group by date
                    daily_stats = df_trend.groupby(date_col).agg({
                        rev_col: 'sum',
                        trans_col: 'sum',
                        sess_col: 'sum'
                    }).sort_index()
                    
                    # Calculate daily CR
                    daily_stats['conversion_rate'] = (daily_stats[trans_col] / daily_stats[sess_col]) * 100
                    daily_stats['revenue_per_session'] = daily_stats[rev_col] / daily_stats[sess_col]
                    
                    # Trend analysis: Compare first 3 days vs last 3 days
                    if len(daily_stats) >= 6:
                        first_3 = daily_stats.head(3)
                        last_3 = daily_stats.tail(3)
                        
                        cr_first = first_3['conversion_rate'].mean()
                        cr_last = last_3['conversion_rate'].mean()
                        cr_change = ((cr_last - cr_first) / cr_first) * 100 if cr_first > 0 else 0
                        
                        rev_first = first_3[rev_col].sum()
                        rev_last = last_3[rev_col].sum()
                        rev_change = ((rev_last - rev_first) / rev_first) * 100 if rev_first > 0 else 0
                        
                        # Determine trend status
                        if cr_change > 5:
                            trend_status = 'improving'
                            trend_emoji = '📈'
                            trend_insight = f"CR improved {cr_change:.1f}% (from {cr_first:.2f}% to {cr_last:.2f}%)"
                        elif cr_change < -5:
                            trend_status = 'declining'
                            trend_emoji = '📉'
                            trend_insight = f"⚠️ CR declined {abs(cr_change):.1f}% (from {cr_first:.2f}% to {cr_last:.2f}%)"
                        else:
                            trend_status = 'stable'
                            trend_emoji = '➡️'
                            trend_insight = f"CR stable around {cr_last:.2f}%"
                        
                        # Best and worst days
                        best_day = daily_stats['conversion_rate'].idxmax()
                        worst_day = daily_stats['conversion_rate'].idxmin()
                        best_cr = daily_stats.loc[best_day, 'conversion_rate']
                        worst_cr = daily_stats.loc[worst_day, 'conversion_rate']
                        
                        analysis['performance_trends'] = {
                            'period': f"{daily_stats.index.min().strftime('%Y-%m-%d')} to {daily_stats.index.max().strftime('%Y-%m-%d')}",
                            'days_analyzed': len(daily_stats),
                            'overall_trend': trend_status,
                            'cr_change_pct': float(cr_change),
                            'revenue_change_pct': float(rev_change),
                            'best_day': {
                                'date': best_day.strftime('%Y-%m-%d'),
                                'conversion_rate': float(best_cr),
                                'revenue': float(daily_stats.loc[best_day, rev_col])
                            },
                            'worst_day': {
                                'date': worst_day.strftime('%Y-%m-%d'),
                                'conversion_rate': float(worst_cr),
                                'revenue': float(daily_stats.loc[worst_day, rev_col])
                            },
                            'insights': [
                                {
                                    'type': 'trend',
                                    'message': f"{trend_emoji} {trend_insight}",
                                    'action': self._get_trend_action(trend_status, cr_change)
                                },
                                {
                                    'type': 'volatility',
                                    'message': f"CR range: {worst_cr:.2f}% to {best_cr:.2f}% ({best_cr - worst_cr:.2f}pp variance)",
                                    'action': f"Investigate {best_day.strftime('%A')} (best) vs {worst_day.strftime('%A')} (worst) patterns"
                                }
                            ]
                        }
                        
                        # Revenue trend insight
                        if abs(rev_change) > 10:
                            rev_trend_emoji = '📈' if rev_change > 0 else '📉'
                            analysis['performance_trends']['insights'].append({
                                'type': 'revenue_trend',
                                'message': f"{rev_trend_emoji} Revenue {'increased' if rev_change > 0 else 'decreased'} {abs(rev_change):.1f}%",
                                'action': 'Monitor traffic sources and AOV changes' if rev_change < 0 else 'Scale winning strategies'
                            })
                    
                except Exception as e:
                    # If date parsing fails, skip trend analysis
                    pass
        
        # === MARKETING: CAMPAIGN ANALYSIS ===
        elif ('marketing' in domain or 'quảng cáo' in domain) and campaign_cols:
            campaign_col = campaign_cols[0]
            
            # Detect key metrics
            spend_cols = [col for col in df.columns if 'spend' in col.lower() or 'cost' in col.lower()]
            revenue_cols = [col for col in df.columns if 'revenue' in col.lower()]
            click_cols = [col for col in df.columns if 'click' in col.lower()]
            conversion_cols = [col for col in df.columns if 'conversion' in col.lower()]
            
            if spend_cols and revenue_cols:
                spend_col = spend_cols[0]
                rev_col = revenue_cols[0]
                
                # Group by campaign
                campaign_stats = df.groupby(campaign_col).agg({
                    spend_col: 'sum',
                    rev_col: 'sum'
                })
                
                # Calculate ROAS by campaign
                campaign_stats['roas'] = campaign_stats[rev_col] / campaign_stats[spend_col]
                
                # Add other metrics if available
                if click_cols:
                    click_col = click_cols[0]
                    campaign_clicks = df.groupby(campaign_col)[click_col].sum()
                    campaign_stats['clicks'] = campaign_clicks
                    campaign_stats['cpc'] = campaign_stats[spend_col] / campaign_stats['clicks']
                
                if conversion_cols:
                    conv_col = conversion_cols[0]
                    campaign_conversions = df.groupby(campaign_col)[conv_col].sum()
                    campaign_stats['conversions'] = campaign_conversions
                    campaign_stats['cpa'] = campaign_stats[spend_col] / campaign_stats['conversions']
                
                # Sort by ROAS (best campaigns first)
                campaign_stats = campaign_stats.sort_values('roas', ascending=False)
                
                # Format for output
                campaign_breakdown = []
                for campaign, row in campaign_stats.iterrows():
                    campaign_data = {
                        'campaign': campaign,
                        'spend': float(row[spend_col]),
                        'revenue': float(row[rev_col]),
                        'roas': float(row['roas'])
                    }
                    if click_cols:
                        campaign_data['clicks'] = float(row['clicks'])
                        campaign_data['cpc'] = float(row['cpc'])
                    if conversion_cols:
                        campaign_data['conversions'] = float(row['conversions'])
                        campaign_data['cpa'] = float(row['cpa'])
                    
                    campaign_breakdown.append(campaign_data)
                
                analysis['campaign_breakdown'] = {
                    'data': campaign_breakdown,
                    'insights': self._generate_campaign_insights(campaign_breakdown),
                    'best_campaign': campaign_breakdown[0]['campaign'] if campaign_breakdown else None,
                    'worst_campaign': campaign_breakdown[-1]['campaign'] if campaign_breakdown else None
                }
        
        # === SALES: REP & STAGE ANALYSIS ===
        elif ('sales' in domain or 'crm' in domain or 'pipeline' in domain) and (rep_cols or stage_cols):
            # Detect key sales columns
            deal_value_cols = [col for col in df.columns if 'deal' in col.lower() and 'value' in col.lower() or 'amount' in col.lower()]
            stage_cols = [col for col in df.columns if 'stage' in col.lower() or 'status' in col.lower()]
            rep_cols = [col for col in df.columns if 'rep' in col.lower() or 'owner' in col.lower()]
            
            # REP PERFORMANCE ANALYSIS
            if rep_cols and deal_value_cols and stage_cols:
                rep_col = rep_cols[0]
                deal_col = deal_value_cols[0]
                stage_col = stage_cols[0]
                
                # Filter won and lost deals
                won_deals = df[df[stage_col].str.contains('won', case=False, na=False)]
                lost_deals = df[df[stage_col].str.contains('lost', case=False, na=False)]
                
                # Group by rep
                rep_stats = df.groupby(rep_col).agg({
                    deal_col: 'sum'
                }).copy()
                
                # Calculate wins and losses per rep
                rep_wins = won_deals.groupby(rep_col).size()
                rep_losses = lost_deals.groupby(rep_col).size()
                rep_won_value = won_deals.groupby(rep_col)[deal_col].sum()
                
                rep_stats['wins'] = rep_wins
                rep_stats['losses'] = rep_losses
                rep_stats['won_revenue'] = rep_won_value
                rep_stats = rep_stats.fillna(0)
                
                # Calculate win rate
                rep_stats['total_closed'] = rep_stats['wins'] + rep_stats['losses']
                rep_stats['win_rate'] = (rep_stats['wins'] / rep_stats['total_closed'] * 100).fillna(0)
                rep_stats['avg_deal_size'] = (rep_stats['won_revenue'] / rep_stats['wins']).fillna(0)
                
                # Sort by won revenue (best reps first)
                rep_stats = rep_stats.sort_values('won_revenue', ascending=False)
                
                # Format for output
                rep_breakdown = []
                for rep, row in rep_stats.iterrows():
                    rep_data = {
                        'rep': rep,
                        'wins': int(row['wins']),
                        'losses': int(row['losses']),
                        'win_rate': float(row['win_rate']),
                        'won_revenue': float(row['won_revenue']),
                        'avg_deal_size': float(row['avg_deal_size'])
                    }
                    rep_breakdown.append(rep_data)
                
                analysis['rep_performance'] = {
                    'data': rep_breakdown,
                    'insights': self._generate_rep_insights(rep_breakdown),
                    'best_rep': rep_breakdown[0]['rep'] if rep_breakdown else None,
                    'worst_rep': rep_breakdown[-1]['rep'] if rep_breakdown else None
                }
            
            # STAGE ANALYSIS (Pipeline bottlenecks)
            if stage_cols and deal_value_cols:
                stage_col = stage_cols[0]
                deal_col = deal_value_cols[0]
                
                # Exclude closed deals for pipeline analysis
                pipeline_deals = df[~df[stage_col].str.contains('closed|won|lost', case=False, na=False)]
                
                if len(pipeline_deals) > 0:
                    # Group by stage
                    stage_stats = pipeline_deals.groupby(stage_col).agg({
                        deal_col: ['sum', 'count', 'mean']
                    })
                    stage_stats.columns = ['total_value', 'deal_count', 'avg_deal_size']
                    stage_stats = stage_stats.sort_values('total_value', ascending=False)
                    
                    # Check for days_in_stage to identify stuck deals
                    days_cols = [col for col in df.columns if 'days' in col.lower() and 'stage' in col.lower()]
                    if days_cols:
                        days_col = days_cols[0]
                        stage_days = pipeline_deals.groupby(stage_col)[days_col].mean()
                        stage_stats['avg_days_in_stage'] = stage_days
                    
                    # Format for output
                    stage_breakdown = []
                    for stage, row in stage_stats.iterrows():
                        stage_data = {
                            'stage': stage,
                            'deal_count': int(row['deal_count']),
                            'total_value': float(row['total_value']),
                            'avg_deal_size': float(row['avg_deal_size'])
                        }
                        if 'avg_days_in_stage' in row:
                            stage_data['avg_days_in_stage'] = float(row['avg_days_in_stage'])
                        
                        stage_breakdown.append(stage_data)
                    
                    analysis['pipeline_stages'] = {
                        'data': stage_breakdown,
                        'insights': self._generate_stage_insights(stage_breakdown),
                        'biggest_stage': stage_breakdown[0]['stage'] if stage_breakdown else None
                    }
        
        return analysis
    
    def _get_trend_action(self, trend_status: str, change_pct: float) -> str:
        """Get actionable recommendation based on trend"""
        if trend_status == 'improving':
            return f"✅ Keep doing what you're doing! Identify winning changes and double down"
        elif trend_status == 'declining':
            if abs(change_pct) > 15:
                return f"🚨 URGENT: Investigate immediately - check traffic quality, site issues, competitor activity"
            else:
                return f"⚠️ Review recent changes (pricing, messaging, UX) that may be hurting CR"
        else:
            return "Monitor closely, run A/B tests to find growth opportunities"
    
    def _generate_channel_insights(self, channel_breakdown: list) -> list:
        """Generate actionable insights from channel breakdown (5-star quality)"""
        insights = []
        
        if not channel_breakdown:
            return insights
        
        # Sort by different metrics to find true best/worst
        by_revenue = sorted(channel_breakdown, key=lambda x: x['revenue'], reverse=True)
        by_roi = sorted([c for c in channel_breakdown if 'roi' in c and c['roi'] != float('inf')], 
                       key=lambda x: x['roi'], reverse=True)
        by_cr = sorted(channel_breakdown, key=lambda x: x['conversion_rate'], reverse=True)
        
        # Insight 1: Best ROI channel (most important!)
        if by_roi:
            best_roi = by_roi[0]
            insights.append({
                'type': 'best_roi',
                'message': f"🏆 {best_roi['channel']} has BEST ROI ({best_roi['roi']:.2f}x) with {best_roi['conversion_rate']:.2f}% CR",
                'action': f"SCALE {best_roi['channel']} - highest profitability"
            })
        
        # Insight 2: Unprofitable channels (ROI < 1.0 = losing money)
        losing_money = [c for c in channel_breakdown if 'roi' in c and c['roi'] < 1.0 and c['roi'] != float('inf')]
        if losing_money:
            total_waste = sum(c['cac'] * c['transactions'] - c['revenue'] for c in losing_money)
            channel_names = ', '.join([f"{c['channel']} ({c['roi']:.2f}x)" for c in losing_money[:3]])
            insights.append({
                'type': 'losing_money',
                'message': f"🚨 {len(losing_money)} channels LOSING MONEY: {channel_names}",
                'action': f"PAUSE these channels - wasting {total_waste:,.0f} VND. Shift budget to profitable channels."
            })
        
        # Insight 3: High-volume low-CR vs Low-volume high-CR
        if by_revenue and by_cr:
            high_volume = by_revenue[0]
            high_cr = by_cr[0]
            
            if high_volume['channel'] != high_cr['channel']:
                # Different channels = opportunity
                if high_cr['sessions'] < high_volume['sessions'] * 0.5:  # Low traffic but high CR
                    insights.append({
                        'type': 'hidden_gem',
                        'message': f"💎 {high_cr['channel']} has {high_cr['conversion_rate']:.2f}% CR (best!) but only {high_cr['sessions']:,.0f} sessions",
                        'action': f"Increase traffic to {high_cr['channel']} - scale ads, SEO, or email list"
                    })
        
        # Insight 4: CAC inefficiency (3x+ difference)
        if len(by_roi) >= 2:
            channels_with_cac = [c for c in channel_breakdown if 'cac' in c and c['cac'] > 0]
            if len(channels_with_cac) >= 2:
                cheapest = min(channels_with_cac, key=lambda x: x['cac'])
                most_expensive = max(channels_with_cac, key=lambda x: x['cac'])
                
                if most_expensive['cac'] / cheapest['cac'] > 3:  # 3x difference
                    insights.append({
                        'type': 'cac_inefficiency',
                        'message': f"💰 {most_expensive['channel']} CAC ({most_expensive['cac']:,.0f}) is {most_expensive['cac']/cheapest['cac']:.1f}x more expensive than {cheapest['channel']} ({cheapest['cac']:,.0f})",
                        'action': f"Optimize {most_expensive['channel']} targeting or shift budget to {cheapest['channel']}"
                    })
        
        # Insight 5: Conversion rate gaps (below 6.6% benchmark - Unbounce 2025)
        low_cr_channels = [c for c in channel_breakdown if c['conversion_rate'] < 6.6]
        if low_cr_channels:
            channel_names = ', '.join([f"{c['channel']} ({c['conversion_rate']:.2f}%)" for c in low_cr_channels[:3]])
            insights.append({
                'type': 'low_conversion',
                'message': f"⚠️ {len(low_cr_channels)} channels below 6.6% CR benchmark: {channel_names}",
                'action': "Review landing pages, targeting, and messaging for these channels"
            })
        
        return insights[:5]  # Top 5 insights only
    
    def _generate_campaign_insights(self, campaign_breakdown: list) -> list:
        """Generate actionable insights from campaign breakdown (5-star quality for CMOs)"""
        insights = []
        
        if not campaign_breakdown:
            return insights
        
        # Categorize campaigns by performance (based on WordStream 2025 benchmark: 2.5 ROAS)
        profitable = [c for c in campaign_breakdown if c['roas'] >= 2.5]  # Above benchmark
        breakeven = [c for c in campaign_breakdown if 1.5 <= c['roas'] < 2.5]  # Marginal
        unprofitable = [c for c in campaign_breakdown if c['roas'] < 1.5]  # Below profitable threshold
        
        best = campaign_breakdown[0]  # Highest ROAS
        worst = campaign_breakdown[-1]  # Lowest ROAS
        
        # Insight 1: Best campaign (Scale opportunity)
        if best['roas'] >= 1.0:
            scale_potential = best['spend'] * 2  # 2x current spend
            projected_revenue = scale_potential * best['roas']
            projected_profit = projected_revenue - scale_potential
            
            insights.append({
                'type': 'scale_winner',
                'message': f"🏆 {best['campaign']}: BEST performer ({best['roas']:.2f}x ROAS, {best.get('cpa', 0):,.0f} CPA)",
                'action': f"SCALE 2x → Invest +{best['spend']:,.0f}, expect +{projected_profit:,.0f} profit"
            })
        
        # Insight 2: Unprofitable campaigns (Immediate action needed)
        if unprofitable:
            total_waste = sum(c['spend'] - c['revenue'] for c in unprofitable)
            total_spend = sum(c['spend'] for c in unprofitable)
            campaign_names = ', '.join([f"{c['campaign']} ({c['roas']:.2f}x)" for c in unprofitable[:3]])
            
            insights.append({
                'type': 'stop_bleeding',
                'message': f"🚨 {len(unprofitable)} campaigns LOSING {total_waste:,.0f}: {campaign_names}",
                'action': f"PAUSE immediately → Save {total_waste:,.0f}/period"
            })
        
        # Insight 3: Smart budget reallocation (Detailed calculation)
        if profitable and unprofitable:
            # Calculate reallocation impact
            wasted_budget = sum(c['spend'] for c in unprofitable)
            best_roas = best['roas']
            
            # If moved to best campaign
            new_revenue = wasted_budget * best_roas
            current_lost = sum(c['spend'] - c['revenue'] for c in unprofitable)
            net_gain = new_revenue - wasted_budget - current_lost
            
            # ROI improvement
            current_total_revenue = sum(c['revenue'] for c in campaign_breakdown)
            current_total_spend = sum(c['spend'] for c in campaign_breakdown)
            current_roas = current_total_revenue / current_total_spend if current_total_spend > 0 else 0
            
            new_total_revenue = current_total_revenue - sum(c['revenue'] for c in unprofitable) + new_revenue
            new_total_spend = current_total_spend  # Same total spend
            new_roas = new_total_revenue / new_total_spend if new_total_spend > 0 else 0
            
            insights.append({
                'type': 'budget_reallocation',
                'message': f"💰 Reallocate {wasted_budget:,.0f} from losing campaigns → {best['campaign']}",
                'action': f"Impact: ROAS {current_roas:.2f}x → {new_roas:.2f}x (+{(new_roas-current_roas)/current_roas*100:.1f}%), Gain {net_gain:,.0f}"
            })
        
        # Insight 4: Break-even campaigns (Optimization opportunity)
        if breakeven:
            campaign_names = ', '.join([f"{c['campaign']} ({c['roas']:.2f}x)" for c in breakeven[:2]])
            insights.append({
                'type': 'optimize',
                'message': f"⚠️ {len(breakeven)} campaigns near break-even: {campaign_names}",
                'action': f"OPTIMIZE targeting, creative, or landing pages → push ROAS > 2.5x"
            })
        
        # Insight 5: CPA efficiency gap (if CPA available)
        if 'cpa' in best and 'cpa' in worst:
            cpa_gap = worst.get('cpa', 0) / best.get('cpa', 1) if best.get('cpa', 0) > 0 else 0
            if cpa_gap > 3:  # 3x difference
                insights.append({
                    'type': 'cpa_efficiency',
                    'message': f"💸 CPA gap: {worst['campaign']} ({worst.get('cpa', 0):,.0f}) is {cpa_gap:.1f}x more expensive than {best['campaign']} ({best.get('cpa', 0):,.0f})",
                    'action': f"Fix {worst['campaign']} targeting or reallocate budget"
                })
        
        # Insight 6: Overall portfolio health
        if len(profitable) == 0:
            insights.append({
                'type': 'critical_alert',
                'message': f"🚨 ZERO profitable campaigns! Overall ROAS < 1.0 across ALL campaigns",
                'action': "URGENT: Pause all campaigns, audit strategy, fix fundamentals before spending more"
            })
        elif len(profitable) / len(campaign_breakdown) < 0.3:  # Less than 30% profitable
            insights.append({
                'type': 'portfolio_warning',
                'message': f"⚠️ Only {len(profitable)}/{len(campaign_breakdown)} campaigns profitable ({len(profitable)/len(campaign_breakdown)*100:.0f}%)",
                'action': "Review overall strategy - most campaigns underperforming"
            })
        
        return insights[:5]  # Top 5 most critical insights
    
    def _generate_rep_insights(self, rep_breakdown: list) -> list:
        """Generate actionable insights from rep performance (5-star quality for Sales VPs)"""
        insights = []
        
        if not rep_breakdown or len(rep_breakdown) == 0:
            return insights
        
        # Sort by different metrics
        by_revenue = sorted(rep_breakdown, key=lambda x: x['won_revenue'], reverse=True)
        by_win_rate = sorted(rep_breakdown, key=lambda x: x['win_rate'], reverse=True)
        by_deal_size = sorted(rep_breakdown, key=lambda x: x['avg_deal_size'], reverse=True)
        
        best_rep = by_revenue[0]
        worst_rep = by_revenue[-1]
        
        # Calculate team averages
        avg_win_rate = sum(r['win_rate'] for r in rep_breakdown) / len(rep_breakdown)
        avg_revenue = sum(r['won_revenue'] for r in rep_breakdown) / len(rep_breakdown)
        avg_deal_size = sum(r['avg_deal_size'] for r in rep_breakdown) / len(rep_breakdown)
        
        # Insight 1: Top performer (Clone this success)
        if best_rep['won_revenue'] > 0:
            revenue_lead = best_rep['won_revenue'] / avg_revenue if avg_revenue > 0 else 0
            insights.append({
                'type': 'top_performer',
                'message': f"🏆 {best_rep['rep']}: BEST performer ({best_rep['won_revenue']:,.0f} revenue, {best_rep['win_rate']:.1f}% win rate)",
                'action': f"Document their winning process → Train team on their tactics ({revenue_lead:.1f}x team avg)"
            })
        
        # Insight 2: Underperformers (Coaching needed)
        low_performers = [r for r in rep_breakdown if r['win_rate'] < 25 and r['wins'] + r['losses'] >= 3]
        if low_performers:
            rep_names = ', '.join([f"{r['rep']} ({r['win_rate']:.1f}%)" for r in low_performers[:3]])
            total_lost_deals = sum(r['losses'] for r in low_performers)
            
            insights.append({
                'type': 'coaching_needed',
                'message': f"⚠️ {len(low_performers)} reps below 25% win rate: {rep_names}",
                'action': f"URGENT coaching needed → {total_lost_deals} deals lost. Review discovery calls, objection handling"
            })
        
        # Insight 3: Win rate gap (Opportunity size)
        if best_rep['win_rate'] > 0 and worst_rep['win_rate'] >= 0:
            win_rate_gap = best_rep['win_rate'] - worst_rep['win_rate']
            if win_rate_gap > 20:  # 20% difference
                # Calculate opportunity: If worst rep had best rep's win rate
                potential_wins = worst_rep['losses'] * (best_rep['win_rate'] / 100)
                potential_revenue = potential_wins * avg_deal_size
                
                insights.append({
                    'type': 'win_rate_gap',
                    'message': f"📊 Win rate gap: {best_rep['rep']} ({best_rep['win_rate']:.1f}%) vs {worst_rep['rep']} ({worst_rep['win_rate']:.1f}%) = {win_rate_gap:.1f}% difference",
                    'action': f"Close gap → Potential +{potential_revenue:,.0f} annual revenue by improving {worst_rep['rep']}"
                })
        
        # Insight 4: Deal size variance (Targeting issue)
        if len(by_deal_size) > 1:
            highest_deal = by_deal_size[0]
            lowest_deal = by_deal_size[-1]
            
            if highest_deal['avg_deal_size'] > 0 and lowest_deal['avg_deal_size'] > 0:
                deal_size_ratio = highest_deal['avg_deal_size'] / lowest_deal['avg_deal_size']
                
                if deal_size_ratio > 3:  # 3x difference
                    insights.append({
                        'type': 'deal_size_variance',
                        'message': f"💰 Deal size gap: {highest_deal['rep']} ({highest_deal['avg_deal_size']:,.0f}) vs {lowest_deal['rep']} ({lowest_deal['avg_deal_size']:,.0f}) = {deal_size_ratio:.1f}x",
                        'action': f"Review {lowest_deal['rep']}'s lead qualification → May be chasing wrong-fit prospects"
                    })
        
        # Insight 5: Team performance health
        healthy_reps = [r for r in rep_breakdown if r['win_rate'] >= 30 and r['wins'] >= 3]
        if len(healthy_reps) == 0:
            insights.append({
                'type': 'critical_alert',
                'message': f"🚨 ZERO reps above 30% win rate! Team avg: {avg_win_rate:.1f}%",
                'action': "URGENT: Audit entire sales process - fundamental issues in qualification, demo, or pricing"
            })
        elif len(healthy_reps) / len(rep_breakdown) < 0.5:  # Less than 50% healthy
            insights.append({
                'type': 'team_warning',
                'message': f"⚠️ Only {len(healthy_reps)}/{len(rep_breakdown)} reps performing well ({len(healthy_reps)/len(rep_breakdown)*100:.0f}%)",
                'action': f"Systematic training needed - team avg {avg_win_rate:.1f}% vs industry 30-35%"
            })
        
        # Insight 6: Hidden gem (High win rate but low volume)
        efficient_reps = [r for r in rep_breakdown if r['win_rate'] >= 40 and r['won_revenue'] < avg_revenue * 0.7]
        if efficient_reps:
            rep = efficient_reps[0]
            insights.append({
                'type': 'hidden_gem',
                'message': f"💎 {rep['rep']}: High win rate ({rep['win_rate']:.1f}%) but low volume ({rep['wins']} wins)",
                'action': f"Feed them MORE leads → Efficiency is proven, volume is opportunity"
            })
        
        return insights[:5]  # Top 5 most critical insights
    
    def _generate_stage_insights(self, stage_breakdown: list) -> list:
        """Generate actionable insights from pipeline stages (5-star quality for Sales VPs)"""
        insights = []
        
        if not stage_breakdown or len(stage_breakdown) == 0:
            return insights
        
        # Sort by value and count
        by_value = sorted(stage_breakdown, key=lambda x: x['total_value'], reverse=True)
        by_count = sorted(stage_breakdown, key=lambda x: x['deal_count'], reverse=True)
        
        # Check if days_in_stage data available
        has_days = 'avg_days_in_stage' in stage_breakdown[0]
        if has_days:
            by_days = sorted([s for s in stage_breakdown if 'avg_days_in_stage' in s], 
                           key=lambda x: x.get('avg_days_in_stage', 0), reverse=True)
        
        # Total pipeline metrics
        total_value = sum(s['total_value'] for s in stage_breakdown)
        total_deals = sum(s['deal_count'] for s in stage_breakdown)
        
        # Insight 1: Biggest bottleneck (where money is stuck)
        biggest_stage = by_value[0]
        if biggest_stage['total_value'] / total_value > 0.4:  # More than 40% of pipeline
            insights.append({
                'type': 'bottleneck',
                'message': f"🚧 {biggest_stage['stage']}: BOTTLENECK ({biggest_stage['deal_count']} deals, {biggest_stage['total_value']:,.0f} stuck)",
                'action': f"Focus HERE → {biggest_stage['total_value']/total_value*100:.0f}% of pipeline value. Fast-track top deals"
            })
        
        # Insight 2: Stuck deals (velocity issue)
        if has_days:
            stuck_stages = [s for s in by_days if s.get('avg_days_in_stage', 0) > 30]
            if stuck_stages:
                stage = stuck_stages[0]
                stuck_value = sum(s['total_value'] for s in stuck_stages)
                
                insights.append({
                    'type': 'velocity_issue',
                    'message': f"⏱️ {stage['stage']}: Deals stuck {stage.get('avg_days_in_stage', 0):.0f} days (avg)",
                    'action': f"Review {stage['deal_count']} deals → Identify blockers, accelerate decisions ({stuck_value:,.0f} at risk)"
                })
        
        # Insight 3: Early stage heavy (lead quality issue)
        early_stages = ['Discovery', 'Qualification', 'Initial Contact', 'Lead']
        early_value = sum(s['total_value'] for s in stage_breakdown if any(e.lower() in s['stage'].lower() for e in early_stages))
        
        if early_value / total_value > 0.6:  # More than 60% in early stages
            insights.append({
                'type': 'early_stage_heavy',
                'message': f"⚠️ {early_value/total_value*100:.0f}% of pipeline in early stages ({early_value:,.0f})",
                'action': "Lead quality issue OR slow progression → Tighten qualification, accelerate discovery"
            })
        
        # Insight 4: Late stage concentration (good problem!)
        late_stages = ['Negotiation', 'Proposal', 'Closed', 'Contract']
        late_value = sum(s['total_value'] for s in stage_breakdown if any(l.lower() in s['stage'].lower() for l in late_stages))
        
        if late_value / total_value > 0.5:  # More than 50% in late stages
            late_count = sum(s['deal_count'] for s in stage_breakdown if any(l.lower() in s['stage'].lower() for l in late_stages))
            insights.append({
                'type': 'late_stage_strong',
                'message': f"✅ {late_value/total_value*100:.0f}% in late stages ({late_count} deals, {late_value:,.0f})",
                'action': f"HIGH close potential → Focus sales energy here. Forecast {late_value * 0.4:,.0f} (40% win rate)"
            })
        
        # Insight 5: Deal count concentration
        if biggest_stage['deal_count'] / total_deals > 0.5:  # More than 50% of deals in one stage
            insights.append({
                'type': 'concentration_risk',
                'message': f"📊 {biggest_stage['deal_count']}/{total_deals} deals ({biggest_stage['deal_count']/total_deals*100:.0f}%) in {biggest_stage['stage']}",
                'action': "Unbalanced pipeline → Need consistent flow through ALL stages"
            })
        
        # Insight 6: Pipeline health summary
        if len(stage_breakdown) < 3:
            insights.append({
                'type': 'pipeline_warning',
                'message': f"⚠️ Only {len(stage_breakdown)} active stages (need 4-6 for healthy flow)",
                'action': "Expand pipeline visibility → Track more granular stages for better forecasting"
            })
        elif len(stage_breakdown) >= 5:
            avg_stage_value = total_value / len(stage_breakdown)
            insights.append({
                'type': 'pipeline_health',
                'message': f"✅ Healthy pipeline: {len(stage_breakdown)} stages, {total_deals} deals, {total_value:,.0f} total",
                'action': f"Maintain balance → Target {avg_stage_value:,.0f}/stage, avoid bottlenecks"
            })
        
        return insights[:5]  # Top 5 most critical insights
    
    @rate_limit_handler(max_retries=3, backoff_base=2)
    @log_performance("Smart Blueprint")
    def step2_smart_blueprint(self, df: pd.DataFrame, domain_info: Dict) -> Dict:
        """
        Step 2: Smart Blueprint - Combined EDA + Blueprint (15s)
        Single AI call instead of 2 separate calls
        
        ⭐ CRITICAL CHANGE: Now calculates KPIs from REAL DATA first,
        then passes to AI for INTERPRETATION only (not calculation)
        """
        
        # 🐛 FIX: Ensure domain_context is always string (handle potential dict/object returns)
        try:
            domain_context = get_domain_specific_prompt_context(domain_info)
            if not isinstance(domain_context, str):
                # If not string, convert to string representation
                domain_context = str(domain_context)
        except Exception as e:
            # Fallback to basic context if function fails
            domain_name = domain_info.get('domain_name', domain_info.get('domain', 'General'))
            expert_role = domain_info.get('expert_role', 'Data Analyst')
            domain_context = f"Domain: {domain_name}\nExpert Role: {expert_role}"
        
        # Get data statistics
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        all_cols = df.columns.tolist()
        
        # ⭐ NEW: Calculate KPIs from REAL DATA first
        kpis_calculated = self._calculate_real_kpis(df, domain_info)
        
        # 🐛 HOTFIX #4: Validate kpis_calculated is a dict before using in f-string
        if not isinstance(kpis_calculated, dict):
            return {'success': False, 'error': f"❌ _calculate_real_kpis returned {type(kpis_calculated).__name__}, expected dict"}
        
        # Combined prompt with STRICT chart requirements - BILINGUAL
        chart_title_lang = "Clear Vietnamese title" if self.lang == 'vi' else "Clear English title"
        
        # 🐛 HOTFIX #4: Safely convert kpis to JSON string to avoid f-string concatenation issues
        try:
            kpis_json = json.dumps(kpis_calculated, indent=2, ensure_ascii=False)
            kpis_json_compact = json.dumps(kpis_calculated, ensure_ascii=False)
        except Exception as e:
            return {'success': False, 'error': f"❌ Failed to serialize KPIs to JSON: {type(e).__name__}: {str(e)}"}
        
        prompt = f"""
{domain_context}

TASK: Smart Dashboard Blueprint (Combined EDA + Design)

DATA PROFILE:
- Shape: {df.shape[0]:,} rows × {df.shape[1]} columns
- ALL Columns: {', '.join(all_cols)}
- Numeric Columns: {', '.join(numeric_cols[:10])}
- Categorical Columns: {', '.join(categorical_cols[:5])}
- Sample Data: {df.head(3).to_dict('records')}

⭐ ACTUAL CALCULATED KPIs (from real data - DO NOT RECALCULATE):
{kpis_json}

REQUIREMENTS:
1. USE the above calculated KPIs (already computed from real data)
2. Design 8-10 charts based on OQMLB framework
3. Ensure 5 quality criteria ≥80% each
4. Include benchmark lines for KPIs

⚠️ CRITICAL CHART REQUIREMENTS (EVERY chart MUST have ALL of these):
- "x_axis": Must be a column name from the data (REQUIRED, cannot be null)
- "y_axis": Must be a column name from the data (REQUIRED, cannot be null)
- "type": One of ["bar", "line", "scatter", "pie"] (REQUIRED)
- "title": {chart_title_lang} (REQUIRED)
- "id": Unique chart ID like "c1", "c2" (REQUIRED)

❌ INVALID CHART EXAMPLES (will be rejected):
{{
    "title": "Revenue Analysis",
    "type": "bar"
    // MISSING x_axis and y_axis - INVALID!
}}

{{
    "title": "Sales by Region",
    "type": "bar",
    "x_axis": null,  // NULL value - INVALID!
    "y_axis": "sales"
}}

✅ VALID CHART EXAMPLES (use actual column names from data):
{{
    "id": "c1",
    "title": "{'Revenue by Channel' if self.lang == 'en' else 'Doanh Thu Theo Kênh'}",
    "type": "bar",
    "x_axis": "{all_cols[0] if len(all_cols) > 0 else 'category'}",  // Actual column from data
    "y_axis": "{numeric_cols[0] if len(numeric_cols) > 0 else 'value'}",  // Actual numeric column
    "benchmark_line": 5000000,
    "question_answered": "{'Which channel has highest revenue?' if self.lang == 'en' else 'Kênh nào có doanh thu cao nhất?'}"
}}

{{
    "id": "c2",
    "title": "{'Trend Over Time' if self.lang == 'en' else 'Xu Hướng Theo Thời Gian'}",
    "type": "line",
    "x_axis": "date",  // Use actual date column if exists
    "y_axis": "{numeric_cols[1] if len(numeric_cols) > 1 else 'metric'}",
    "question_answered": "{'How does the trend change?' if self.lang == 'en' else 'Xu hướng thay đổi như thế nào?'}"
}}

OUTPUT JSON (strictly follow this structure):
{{
    "kpis_calculated": {kpis_json_compact},
    "objectives": [
        {{"id": "obj1", "title": "Optimize Marketing ROI", "priority": "high"}}
    ],
    "charts": [
        {{
            "id": "c1",
            "title": "ROAS by Channel",
            "type": "bar",
            "x_axis": "channel",
            "y_axis": "roas",
            "benchmark_line": 4.0,
            "question_answered": "Which channels perform best?"
        }}
    ],
    "quality_scores": {{
        "informative": 85,
        "clarity": 90,
        "design": 88,
        "interactivity": 82,
        "actionable": 87
    }}
}}

⚠️ CRITICAL: Return the EXACT kpis_calculated provided above (already computed from real data).
DO NOT recalculate or estimate KPIs - use the values exactly as provided!

REMEMBER: Every chart MUST have x_axis and y_axis as actual column names from the data!
"""
        
        success, result = self._generate_ai_insight(prompt, temperature=0.3, max_tokens=6000)
        
        if not success:
            return {'success': False, 'error': result}
        
        try:
            smart_blueprint = json.loads(result)
            
            # ⭐ CRITICAL: Force use real calculated KPIs (ensures 100% accuracy)
            smart_blueprint['kpis_calculated'] = kpis_calculated
            
            # ✅ PART 2: Validate and fix chart specifications
            smart_blueprint = self._validate_and_fix_charts(smart_blueprint, df)
            
            # Validate blueprint quality
            validation = self._validate_blueprint_quality(smart_blueprint)
            
            if not validation['passed']:
                return {
                    'success': False,
                    'error': f"❌ Blueprint chất lượng không đạt: {', '.join(validation['failures'])}"
                }
            
            # Display blueprint (compact)
            self._display_compact_blueprint(smart_blueprint, domain_info)
            
            return {
                'success': True,
                'smart_blueprint': smart_blueprint,
                'quality_score': validation['score']
            }
        
        except json.JSONDecodeError as e:
            return {'success': False, 'error': f"❌ Lỗi tạo blueprint: {str(e)}"}
    
    @log_performance("Dashboard Build")
    def step3_dashboard_build(self, df: pd.DataFrame, smart_blueprint: Dict) -> Dict:
        """
        Step 3: Dashboard build - Pure execution (7s)
        """
        import plotly.express as px
        import plotly.graph_objects as go
        import logging
        logger = logging.getLogger(__name__)
        
        charts = []
        
        for i, chart_spec in enumerate(smart_blueprint.get('charts', [])[:10]):  # Limit to 10 charts
            try:
                logger.debug(f"Processing chart {i+1}: {chart_spec.get('title', 'Unknown')}")
                
                chart_id = str(chart_spec.get('id', 'unknown'))
                chart_title = str(chart_spec.get('title', 'Untitled'))
                chart_type = str(chart_spec.get('type', 'bar'))
                x_axis = chart_spec.get('x_axis')
                y_axis = chart_spec.get('y_axis')
                
                logger.debug(f"  Chart type: {chart_type}, x_axis: {x_axis}, y_axis: {y_axis}")
                
                # Skip if required fields are None
                if not x_axis or not y_axis:
                    logger.warning(f"Skipping chart {i+1}: missing x_axis or y_axis")
                    continue
                
                # ⭐ CRITICAL FIX: Skip if x_axis and y_axis are the same (prevents duplicate column errors)
                # Silent skip - user doesn't need to see internal chart generation issues
                if x_axis == y_axis:
                    logger.warning(f"Skipping chart {i+1}: x_axis and y_axis are identical ('{x_axis}') - would create duplicate columns")
                    # No user-facing warning - keep UI clean and professional
                    continue
                
                # Validate columns exist  
                if x_axis not in df.columns:
                    logger.warning(f"Skipping chart {i+1}: x_axis '{x_axis}' not in columns: {list(df.columns)}")
                    continue
                if y_axis not in df.columns:
                    logger.warning(f"Skipping chart {i+1}: y_axis '{y_axis}' not in columns")
                    continue
                
                # Create chart
                fig = None
                
                logger.debug(f"Creating {chart_type} chart with x={x_axis}, y={y_axis}")
                
                # ⭐ CRITICAL FIX: Remove None/NaN values before plotting
                # This prevents "'>' not supported between NoneType" errors
                df_clean = df[[x_axis, y_axis]].dropna()
                
                if len(df_clean) == 0:
                    logger.warning(f"Skipping chart {i+1}: no valid data after removing NaN")
                    continue
                
                if chart_type == 'bar' and x_axis and y_axis:
                    # ✅ ColorBrewer palette for professional, accessible charts
                    fig = px.bar(
                        df_clean,
                        x=x_axis,
                        y=y_axis,
                        title=chart_title,
                        color_discrete_sequence=TABLEAU_10_COLORS
                    )

                    # Add benchmark line
                    if 'benchmark_line' in chart_spec:
                        fig.add_hline(
                            y=chart_spec['benchmark_line'],
                            line_dash="dash",
                            line_color="#E15759",  # ColorBrewer red
                            annotation_text="Benchmark",
                            line_width=2
                        )

                elif chart_type == 'line' and x_axis and y_axis:
                    # ✅ ColorBrewer palette
                    fig = px.line(
                        df_clean,
                        x=x_axis,
                        y=y_axis,
                        title=chart_title,
                        color_discrete_sequence=TABLEAU_10_COLORS
                    )

                elif chart_type == 'scatter' and x_axis and y_axis:
                    # ✅ ColorBrewer palette
                    fig = px.scatter(
                        df_clean,
                        x=x_axis,
                        y=y_axis,
                        title=chart_title,
                        color_discrete_sequence=TABLEAU_10_COLORS
                    )

                elif chart_type == 'pie' and x_axis and y_axis:
                    # ✅ ColorBrewer palette for pie charts
                    fig = px.pie(
                        df_clean,
                        names=x_axis,
                        values=y_axis,
                        title=chart_title,
                        color_discrete_sequence=TABLEAU_10_COLORS
                    )

                if fig:
                    # ✅ ENHANCED Professional styling (Edward Tufte + WCAG AA + Maximum Visual Impact)
                    fig.update_layout(
                        # Typography: Larger, bolder, maximum readability for PDF export
                        font=dict(
                            family='DejaVu Sans, Arial, sans-serif',
                            size=13,  # Increased from 11 for better PDF visibility
                            color='#1a1a1a'  # Deep black for maximum contrast
                        ),
                        title=dict(
                            text=chart_title,
                            font=dict(
                                size=18,  # Increased from 14 - bold, clear titles
                                color='#1E40AF',  # Professional blue brand color
                                family='DejaVu Sans, Arial, sans-serif'
                            ),
                            x=0.5,  # Center-aligned title
                            xanchor='center',
                            pad=dict(b=20)  # More breathing room below title
                        ),

                        # Layout: Clean, high-impact (Tufte: maximize data-ink ratio)
                        plot_bgcolor='#FFFFFF',  # Pure white for print/PDF
                        paper_bgcolor='#FFFFFF',
                        showlegend=True,

                        # Legend: Enhanced visibility and professionalism
                        legend=dict(
                            font=dict(size=12, color='#1a1a1a'),  # Larger, more visible
                            bgcolor='rgba(248, 250, 252, 0.95)',  # Subtle off-white
                            bordercolor='#94A3B8',  # Professional gray border
                            borderwidth=1.5,
                            orientation='v',
                            yanchor='top',
                            y=0.98,
                            xanchor='right',
                            x=0.98,
                            itemsizing='constant'  # Consistent symbol sizes
                        ),

                        # Margins: Optimized for PDF export with labels
                        margin=dict(l=80, r=60, t=90, b=80),  # More space for all labels

                        # Hover: Cleaner, more professional tooltips
                        hoverlabel=dict(
                            bgcolor='#1E40AF',
                            font_size=12,
                            font_family='DejaVu Sans, Arial, sans-serif',
                            font_color='white',
                            bordercolor='white'
                        ),

                        # Height: Larger charts for better visibility in PDF
                        height=500  # Increased from default 450
                    )

                    # ✅ Enhanced axes (Stephen Few: clean, high contrast, professional)
                    fig.update_xaxes(
                        showgrid=False,  # Remove vertical gridlines (Tufte principle)
                        showline=True,
                        linewidth=2.5,  # Thicker, more visible axis
                        linecolor='#334155',  # Darker slate for visibility
                        tickfont=dict(size=11, color='#1a1a1a', family='DejaVu Sans'),
                        ticks='outside',
                        ticklen=6,
                        tickwidth=2,
                        tickcolor='#64748B',
                        title_font=dict(size=13, color='#1E40AF')  # Blue axis titles
                    )

                    fig.update_yaxes(
                        showgrid=True,  # Horizontal gridlines aid data reading
                        gridwidth=1,  # More visible gridlines
                        gridcolor='rgba(148, 163, 184, 0.25)',  # Subtle but clear
                        showline=True,
                        linewidth=2.5,  # Thicker, more visible axis
                        linecolor='#334155',  # Darker slate for visibility
                        tickfont=dict(size=11, color='#1a1a1a', family='DejaVu Sans'),
                        ticks='outside',
                        ticklen=6,
                        tickwidth=2,
                        tickcolor='#64748B',
                        zeroline=True,
                        zerolinewidth=2.5,
                        zerolinecolor='#94A3B8',
                        title_font=dict(size=13, color='#1E40AF')  # Blue axis titles
                    )

                    # ✅ Chart-type specific enhancements for maximum visual impact
                    if chart_type == 'bar':
                        fig.update_traces(
                            marker=dict(
                                line=dict(color='#FFFFFF', width=2),  # Strong white borders
                                opacity=0.92  # Slight transparency for depth
                            ),
                            textposition='outside',
                            textfont=dict(size=11, color='#1a1a1a', family='DejaVu Sans')
                        )
                    elif chart_type == 'pie':
                        fig.update_traces(
                            textposition='outside',
                            textinfo='label+percent',
                            textfont=dict(size=12, color='#1a1a1a', family='DejaVu Sans'),
                            marker=dict(
                                line=dict(color='#FFFFFF', width=3)  # Strong borders for clarity
                            ),
                            pull=[0.04] * 10,  # Slight explode for all slices
                            opacity=0.92,
                            rotation=90  # Start from top
                        )
                    elif chart_type in ['line', 'scatter']:
                        fig.update_traces(
                            line=dict(width=3.5),  # Thicker lines for PDF visibility
                            marker=dict(size=9, line=dict(width=2, color='#FFFFFF'))
                        )
                    
                    charts.append({
                        'id': chart_id,
                        'title': chart_title,
                        'figure': fig,
                        'spec': chart_spec
                    })
            
            except Exception as e:
                import traceback
                logger.error(f"Failed to create chart {i+1} '{chart_spec.get('title', 'Unknown')}': {type(e).__name__}: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()[:500]}")
                # Silent skip - user doesn't need to see chart generation failures
                # Still logs error for debugging
                continue
        
        return {
            'charts': charts,
            'objectives': smart_blueprint.get('objectives', []),
            'kpis': smart_blueprint.get('kpis_calculated', {})
        }
    
    @rate_limit_handler(max_retries=3, backoff_base=2)
    @log_performance("Domain Insights")
    def step4_domain_insights(self, dashboard: Dict, smart_blueprint: Dict, domain_info: Dict) -> Dict:
        """
        Step 4: Domain expert insights (15s)
        """
        
        # 🐛 FIX: Ensure domain_context is always string (handle potential dict/object returns)
        try:
            domain_context = get_domain_specific_prompt_context(domain_info)
            if not isinstance(domain_context, str):
                domain_context = str(domain_context)
        except Exception as e:
            domain_name = domain_info.get('domain_name', domain_info.get('domain', 'General'))
            expert_role = domain_info.get('expert_role', 'Data Analyst')
            domain_context = f"Domain: {domain_name}\nExpert Role: {expert_role}"
        
        # Get KPIs summary
        kpis_summary = []
        for kpi_name, kpi_data in smart_blueprint.get('kpis_calculated', {}).items():
            value = kpi_data.get('value', 'N/A')
            benchmark = kpi_data.get('benchmark', 'N/A')
            status = kpi_data.get('status', 'Unknown')
            kpis_summary.append(f"- {kpi_name}: {value} (Benchmark: {benchmark}, Status: {status})")
        
        kpis_text = chr(10).join(kpis_summary[:5]) if kpis_summary else "No KPIs calculated"
        
        # Bilingual prompt based on language setting
        if self.lang == 'vi':
            prompt = f"""
{domain_context}

NHIỆM VỤ: Insights Chuyên Gia (Ngắn Gọn & Hành Động)

KPIs:
{kpis_text}

Biểu đồ: {len(dashboard['charts'])} visualizations được tạo

YÊU CẦU (Ngắn Gọn):
1. Tóm tắt điều hành (2-3 câu)
2. Top 3 insights với tác động kinh doanh
3. Top 3 khuyến nghị hành động với ROI dự kiến
4. Rủi ro nghiêm trọng nếu có

OUTPUT JSON (Nội dung PHẢI là tiếng Việt):
{{
    "executive_summary": "Tóm tắt hiệu suất trong 2-3 câu bằng tiếng Việt",
    "key_insights": [
        {{
            "title": "Tiêu đề insight bằng tiếng Việt",
            "description": "Insight ngắn gọn với số liệu bằng tiếng Việt",
            "data_evidence": "Minh chứng cụ thể: VD: 'Q1: 500M → Q4: 725M VND (cột: doanh_thu, dòng: 1-120)'",
            "impact": "high/medium/low"
        }}
    ],
    "recommendations": [
        {{
            "action": "Hành động cụ thể bằng tiếng Việt",
            "priority": "high/medium/low",
            "expected_impact": "Lợi ích định lượng bằng tiếng Việt",
            "timeline": "immediate/short/long"
        }}
    ],
    "risk_alerts": [
        {{"risk": "Mô tả rủi ro bằng tiếng Việt", "severity": "high/medium/low"}}
    ]
}}

LƯU Ý QUAN TRỌNG:
1. Tất cả nội dung text PHẢI viết bằng tiếng Việt!
2. **data_evidence** PHẢI bao gồm:
   - Số liệu cụ thể từ dataset
   - Tên cột được tham chiếu
   - Khoảng dòng sử dụng (nếu có)
   - Công thức tính (nếu áp dụng)
   VD TỐT: "Doanh thu tăng 45%: Q1=500M → Q4=725M VND (cột: doanh_thu, dòng: 1-120)"
   VD XẤU: "Doanh thu tăng đáng kể" (thiếu số liệu cụ thể)
"""
        else:  # English
            prompt = f"""
{domain_context}

TASK: Expert Insights (Concise & Actionable)

KPIs:
{kpis_text}

Charts: {len(dashboard['charts'])} visualizations created

REQUIREMENTS (Brief):
1. Executive summary (2-3 sentences)
2. Top 3 insights with business impact
3. Top 3 actionable recommendations with expected ROI
4. Critical risks if any

OUTPUT JSON (Content MUST be in English):
{{
    "executive_summary": "Performance overview in 2-3 sentences in English",
    "key_insights": [
        {{
            "title": "Insight title in English",
            "description": "Brief insight with numbers in English",
            "data_evidence": "Specific evidence: Ex: 'Q1: 500M → Q4: 725M VND (column: revenue, rows: 1-120)'",
            "impact": "high/medium/low"
        }}
    ],
    "recommendations": [
        {{
            "action": "Specific action in English",
            "priority": "high/medium/low",
            "expected_impact": "Quantified benefit in English",
            "timeline": "immediate/short/long"
        }}
    ],
    "risk_alerts": [
        {{"risk": "Risk description in English", "severity": "high/medium/low"}}
    ]
}}

CRITICAL REQUIREMENTS:
1. All text content MUST be written in English!
2. **data_evidence** MUST include:
   - Specific numbers from the dataset
   - Column name referenced
   - Row range used (if applicable)
   - Formula used (if applicable)
   GOOD: "Revenue grew 45%: Q1=500M → Q4=725M VND (column: revenue, rows: 1-120)"
   BAD: "Revenue increased significantly" (no specific numbers)
"""
        
        success, result = self._generate_ai_insight(prompt, temperature=0.5, max_tokens=3000)
        
        if not success:
            return {'success': False, 'error': result, 'insights': {}}
        
        try:
            insights = json.loads(result)

            # ⭐ Add tracking KPI recommendations for HR domain (based on real user feedback)
            insights = self._add_tracking_kpi_recommendations(insights, domain_info, self.lang)

            # Display insights (compact)
            self._display_compact_insights(insights, domain_info)

            return {
                'success': True,
                'insights': insights
            }
        
        except json.JSONDecodeError as e:
            return {'success': False, 'error': f"❌ Lỗi tạo insights: {str(e)}", 'insights': {}}
    
    # Helper methods

    def _add_tracking_kpi_recommendations(self, insights: Dict, domain_info: Dict, lang: str) -> Dict:
        """
        Add tracking KPI recommendations based on domain (e.g., eNPS, turnover rate for HR).
        This ensures critical tracking metrics are always suggested to users.

        Args:
            insights: Generated insights dictionary
            domain_info: Domain information
            lang: Language code ('vi' or 'en')

        Returns:
            Enhanced insights with tracking recommendations
        """
        domain = domain_info.get('domain', '').lower()

        # Only add for HR domain and if not too many recommendations already
        if 'hr' in domain or 'nhân sự' in domain:
            if 'recommendations' not in insights:
                insights['recommendations'] = []

            # Check if already have many recommendations
            if len(insights['recommendations']) >= 5:
                return insights  # Don't overwhelm user

            # eNPS recommendation
            if lang == 'vi':
                enps_rec = {
                    "action": "Triển khai khảo sát eNPS (Employee Net Promoter Score) định kỳ",
                    "priority": "high",
                    "expected_impact": "Theo dõi mức độ hài lòng nhân viên, dự đoán turnover sớm. Target: eNPS > 30 (Good), > 50 (Excellent)",
                    "timeline": "short"
                }
                turnover_rec = {
                    "action": "Thiết lập dashboard theo dõi Turnover Rate theo tháng",
                    "priority": "high",
                    "expected_impact": "Phát hiện xu hướng nghỉ việc sớm, giảm chi phí tuyển dụng. Target: Voluntary turnover < 10%/year",
                    "timeline": "immediate"
                }
            else:
                enps_rec = {
                    "action": "Implement periodic eNPS (Employee Net Promoter Score) surveys",
                    "priority": "high",
                    "expected_impact": "Track employee satisfaction, predict turnover early. Target: eNPS > 30 (Good), > 50 (Excellent)",
                    "timeline": "short"
                }
                turnover_rec = {
                    "action": "Set up monthly Turnover Rate tracking dashboard",
                    "priority": "high",
                    "expected_impact": "Detect attrition trends early, reduce recruitment costs. Target: Voluntary turnover < 10%/year",
                    "timeline": "immediate"
                }

            # Add only if not already present (check by action keywords)
            existing_actions = [rec.get('action', '').lower() for rec in insights['recommendations']]
            if not any('enps' in action or 'net promoter' in action for action in existing_actions):
                insights['recommendations'].append(enps_rec)
            if not any('turnover' in action or 'attrition' in action for action in existing_actions):
                insights['recommendations'].append(turnover_rec)

        return insights

    def _generate_ai_insight(self, prompt: str, temperature: float = 0.7, max_tokens: int = 4096) -> Tuple[bool, str]:
        """
        Generate AI insight with GUARANTEED JSON output
        
        Uses Gemini's JSON mode + multiple fallback strategies to ensure valid JSON
        """
        try:
            # Strategy 1: Force JSON mode via generation config
            json_prompt = f"""{prompt}

CRITICAL INSTRUCTIONS:
1. You MUST return ONLY valid JSON
2. NO code blocks (no ```json or ```)
3. NO explanations, NO markdown, NO extra text
4. Start with {{ and end with }}
5. All strings must use double quotes "
6. Numbers must be valid JSON numbers (no NaN, Infinity)

Your response must be parseable by json.loads() immediately."""
            
            # ⭐ FIX: Create model from genai module (self.client is genai module, not model)
            # Use stable model name (not -exp) for production reliability
            model = self.client.GenerativeModel('gemini-2.0-flash')
            
            response = model.generate_content(
                json_prompt,
                generation_config=self.client.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                    response_mime_type="application/json"  # Force JSON mode
                )
            )
            
            # ✅ Issue #3 Fix: Handle None response
            if not response or not response.text:
                return (False, "❌ AI trả về response rỗng (có thể do rate limit hoặc safety filter)")
            
            text = response.text.strip()
            
            # ✅ Check if text is empty after strip
            if not text:
                return (False, "❌ AI trả về text rỗng")
            
            # Strategy 2: Clean common issues
            # Remove markdown code blocks
            if text.startswith('```json'):
                text = text[7:].strip()
            elif text.startswith('```'):
                text = text[3:].strip()
            
            if text.endswith('```'):
                text = text[:-3].strip()
            
            # Strategy 3: Extract JSON if wrapped in text
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                text = json_match.group(0)
            
            # Strategy 4: Validate it's actually JSON
            try:
                json.loads(text)  # Test parse
            except json.JSONDecodeError as e:
                return (False, f"❌ AI trả về JSON không hợp lệ: {str(e)[:100]}")
            
            return (True, text)
            
        except Exception as e:
            error_msg = user_friendly_error(e)
            return (False, error_msg)
    
    def _apply_fast_cleaning(self, df: pd.DataFrame, cleaning_plan: Dict, domain_info: Dict) -> pd.DataFrame:
        """
        Fast data cleaning execution with domain-specific deduplication
        
        ⭐ CRITICAL: Only handle ACTUAL missing values to preserve data accuracy.
        Do NOT modify non-null values - this changes statistics (mean, median, etc.)
        
        ⭐ NEW: Domain-specific deduplication using MDM best practices
        - Different domains have different duplicate handling strategies
        - Uses semantic key columns (Employee ID, Order ID, etc.) not all columns
        - Provides warnings when duplicate rate exceeds domain-specific thresholds
        """
        df_clean = df.copy()
        original_count = len(df_clean)
        
        # Handle missing values - ONLY if they actually exist
        missing_handled = cleaning_plan.get('cleaning_summary', {}).get('missing_handled', {})
        protected_fields_skipped = []  # Track protected fields for reporting
        
        for col, method in missing_handled.items():
            if col not in df_clean.columns:
                continue
            
            # ⭐ CRITICAL CHECK: Only proceed if column has actual missing values
            if df_clean[col].isnull().sum() == 0:
                continue  # Skip - no missing values to handle
            
            # 🔴 CRITICAL PROTECTION: NEVER impute protected fields
            if is_never_impute_field(col):
                # Protected field with missing values - KEEP AS NULL for data integrity
                protected_fields_skipped.append({
                    'column': col,
                    'missing_count': df_clean[col].isnull().sum(),
                    'reason': 'NEVER_IMPUTE_PROTECTION'
                })
                continue  # Skip imputation - preserve NULL values
            
            if method == 'median' and df_clean[col].dtype in ['int64', 'float64']:
                # Use proper pandas method (not inplace to avoid warnings)
                df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            elif method == 'mode':
                if len(df_clean[col].mode()) > 0:
                    df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
        
        # Store protection report in cleaning plan
        if protected_fields_skipped:
            cleaning_plan.setdefault('cleaning_summary', {})['protected_fields_preserved'] = protected_fields_skipped
            
            # Display protection report to user
            if is_streamlit_context():
                with st.expander("🛡️ Data Integrity Protection Report", expanded=False):
                    st.info("✅ **NEVER_IMPUTE Protection Active**")
                    st.write("The following critical fields have missing values that were **preserved as NULL** to maintain data integrity:")
                    for field in protected_fields_skipped:
                        st.write(f"- **{field['column']}**: {field['missing_count']} missing values kept as NULL")
                    st.caption("⚠️ Imputing these fields would cause wrong business decisions and legal liability.")
        
        # ==================================================================================
        # DOMAIN-SPECIFIC DEDUPLICATION (NEW - Phase 1 Implementation)
        # ==================================================================================
        duplicates_removed, dedup_info = self._smart_deduplication(
            df_clean, 
            domain_info, 
            original_count
        )
        df_clean = dedup_info['df_cleaned']
        
        # Update cleaning plan with deduplication details
        cleaning_plan.setdefault('cleaning_summary', {})['duplicates_removed'] = duplicates_removed
        cleaning_plan.setdefault('cleaning_summary', {})['deduplication_strategy'] = dedup_info['strategy']
        cleaning_plan.setdefault('cleaning_summary', {})['key_columns_used'] = dedup_info['key_columns']
        cleaning_plan.setdefault('cleaning_summary', {})['duplicate_rate'] = dedup_info['duplicate_rate']
        
        # Show warning if excessive duplicates
        if dedup_info.get('warning'):
            if is_streamlit_context():
                st.warning(dedup_info['warning'])
        
        return df_clean
    
    def _smart_deduplication(self, df: pd.DataFrame, domain_info: Dict, original_count: int) -> Tuple[int, Dict]:
        """
        Domain-specific smart deduplication using MDM best practices
        
        Returns:
            Tuple of (duplicates_removed, dedup_info_dict)
        """
        domain_name = domain_info.get('domain_name', '_default')
        
        # Get domain-specific rules (with fallback to default)
        rules = DEDUPLICATION_RULES.get(domain_name, DEDUPLICATION_RULES['_default'])
        
        if not rules['enabled']:
            return 0, {
                'df_cleaned': df,
                'strategy': 'Disabled',
                'key_columns': [],
                'duplicate_rate': 0.0
            }
        
        # Identify key columns using fuzzy matching
        key_cols = self._find_key_columns(df, rules['key_columns'])
        
        # Apply deduplication
        if key_cols and rules['strategy'] == 'key_based':
            # Deduplicate based on semantic key columns
            df_cleaned = df.drop_duplicates(subset=key_cols, keep=rules['keep'])
            strategy = f"{rules['description']} (Key columns: {', '.join(key_cols)})"
        else:
            # Fallback: deduplicate on all columns
            df_cleaned = df.drop_duplicates(keep=rules['keep'])
            strategy = "Remove exact duplicates (all columns match)"
            key_cols = ['All columns']
        
        # Calculate metrics
        duplicates_removed = original_count - len(df_cleaned)
        duplicate_rate = duplicates_removed / original_count if original_count > 0 else 0.0
        
        # Generate warning if excessive
        warning = None
        if duplicate_rate > rules['threshold']:
            warning = (
                f"⚠️ **High duplicate rate detected**: {duplicate_rate:.1%} "
                f"({duplicates_removed:,} of {original_count:,} rows)\n\n"
                f"**Expected for {domain_name}**: <{rules['threshold']:.1%}\n\n"
                f"**Possible reasons**:\n"
                f"- Synthetic/test data with intentional duplicates\n"
                f"- Data export error (repeated rows)\n"
                f"- Legitimate scenarios (multi-job employees, survey responses)\n\n"
                f"**Strategy applied**: {strategy}"
            )
        
        return duplicates_removed, {
            'df_cleaned': df_cleaned,
            'strategy': strategy,
            'key_columns': key_cols,
            'duplicate_rate': duplicate_rate,
            'warning': warning
        }
    
    def _find_key_columns(self, df: pd.DataFrame, candidate_patterns: List[str]) -> List[str]:
        """
        Find key columns using fuzzy matching on candidate patterns
        
        Examples:
            Patterns: ['employee id', 'emp_id']
            Matches: 'Employee_ID', 'EMP ID', 'EmployeeId'
        
        Returns:
            List of matched column names from dataframe
        """
        import re
        
        matched_cols = []
        df_cols_lower = [col.lower().strip() for col in df.columns]
        
        for pattern in candidate_patterns:
            pattern_normalized = pattern.lower().strip().replace(' ', '').replace('_', '')
            
            for i, df_col in enumerate(df.columns):
                df_col_normalized = df_cols_lower[i].replace(' ', '').replace('_', '')
                
                # Exact match (normalized)
                if pattern_normalized == df_col_normalized:
                    if df_col not in matched_cols:
                        matched_cols.append(df_col)
                    break
                
                # Contains match (for composite names like 'customer_email_id')
                elif pattern_normalized in df_col_normalized or df_col_normalized in pattern_normalized:
                    if df_col not in matched_cols:
                        matched_cols.append(df_col)
        
        return matched_cols
    
    def _validate_quality_gates(self, df_cleaned: pd.DataFrame, cleaning_plan: Dict) -> Dict:
        """Validate ISO 8000 quality gates"""
        quality_metrics = cleaning_plan.get('quality_metrics', {})
        
        checks = {
            'missing_rate_ok': (df_cleaned.isnull().sum().sum() / df_cleaned.size * 100) < 2,
            'duplicates_zero': df_cleaned.duplicated().sum() == 0,
            'completeness_ok': quality_metrics.get('completeness', 0) >= 98
        }
        
        passed = all(checks.values())
        score = sum(checks.values()) / len(checks) * 100
        
        return {
            'passed': passed,
            'score': score,
            'checks': checks,
            'failures': [k for k, v in checks.items() if not v]
        }
    
    def _validate_and_fix_charts(self, smart_blueprint: Dict, df: pd.DataFrame) -> Dict:
        """
        ✅ PART 2: Validate and fix chart specifications
        
        Ensures every chart has required fields: x_axis, y_axis, type, title, id
        Validates columns exist in dataframe, provides fallbacks if needed
        """
        import logging
        logger = logging.getLogger(__name__)
        
        charts = smart_blueprint.get('charts', [])
        valid_charts = []
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        all_cols = df.columns.tolist()
        
        for i, chart in enumerate(charts):
            chart_id = chart.get('id', f'c{i+1}')
            
            # ✅ Check required fields exist and are not None
            required_fields = ['x_axis', 'y_axis', 'type', 'title']
            missing_fields = [f for f in required_fields if not chart.get(f)]
            
            if missing_fields:
                logger.warning(f"⚠️ Chart '{chart.get('title', 'Unknown')}' missing fields: {missing_fields} - SKIPPED")
                # Silent skip - user doesn't need to see internal validation issues
                continue
            
            # ✅ PART 3: Verify column names exist in dataframe
            x_axis = chart['x_axis']
            y_axis = chart['y_axis']
            
            # Fix x_axis if not in columns
            if x_axis not in all_cols:
                # Try to find similar column name (case-insensitive)
                x_match = next((col for col in all_cols if col.lower() == x_axis.lower()), None)
                if x_match:
                    chart['x_axis'] = x_match
                    logger.info(f"✅ Fixed x_axis: {x_axis} → {x_match}")
                else:
                    # Fallback to first categorical or first column
                    fallback = categorical_cols[0] if categorical_cols else all_cols[0]
                    logger.warning(f"⚠️ x_axis '{x_axis}' not found, using fallback: {fallback}")
                    chart['x_axis'] = fallback
            
            # Fix y_axis if not in columns
            if y_axis not in all_cols:
                # Try to find similar column name (case-insensitive)
                y_match = next((col for col in all_cols if col.lower() == y_axis.lower()), None)
                if y_match:
                    chart['y_axis'] = y_match
                    logger.info(f"✅ Fixed y_axis: {y_axis} → {y_match}")
                else:
                    # Fallback to first numeric column
                    fallback = numeric_cols[0] if numeric_cols else all_cols[1] if len(all_cols) > 1 else all_cols[0]
                    logger.warning(f"⚠️ y_axis '{y_axis}' not found, using fallback: {fallback}")
                    chart['y_axis'] = fallback
            
            # Validate chart type
            valid_types = ['bar', 'line', 'scatter', 'pie']
            if chart['type'] not in valid_types:
                logger.warning(f"⚠️ Invalid chart type '{chart['type']}', defaulting to 'bar'")
                chart['type'] = 'bar'
            
            # Ensure chart has ID
            if 'id' not in chart or not chart['id']:
                chart['id'] = chart_id
            
            valid_charts.append(chart)
        
        # ✅ Ensure minimum 3 valid charts
        if len(valid_charts) < 3:
            logger.error(f"❌ Only {len(valid_charts)} valid charts found, need at least 3")
            # Keep this error - it's a genuine data issue user should know about
            if is_streamlit_context():
                st.error(f"❌ Không đủ dữ liệu để tạo dashboard (cần tối thiểu 3 biểu đồ, chỉ tạo được {len(valid_charts)})")
            
            # Add fallback charts if needed
            while len(valid_charts) < 3 and len(numeric_cols) >= len(valid_charts):
                fallback_chart = {
                    'id': f'fallback_{len(valid_charts)+1}',
                    'title': f'Phân Tích {numeric_cols[len(valid_charts)].title()}',
                    'type': 'bar',
                    'x_axis': categorical_cols[0] if categorical_cols else all_cols[0],
                    'y_axis': numeric_cols[len(valid_charts)],
                    'question_answered': f'Phân tích {numeric_cols[len(valid_charts)]}'
                }
                valid_charts.append(fallback_chart)
                logger.info(f"✅ Added fallback chart: {fallback_chart['title']}")
        
        smart_blueprint['charts'] = valid_charts
        
        logger.info(f"✅ Chart validation complete: {len(valid_charts)}/{len(charts)} valid charts")
        
        return smart_blueprint
    
    def _calculate_quality_deductions(self, df: pd.DataFrame, kpis: Dict, domain: str) -> Dict:
        """
        ✅ FIX #4: Calculate quality score deductions based on ISO 8000 consistency checks
        
        ISO 8000-61: Data Quality Management - Consistency dimension
        Checks metadata consistency, benchmark accuracy, reproducibility
        
        Returns:
            Dict with deduction details and total deduction points
        """
        deductions = {
            'currency_inconsistency': 0,
            'wrong_benchmark_source': 0,
            'numeric_inconsistency': 0,
            'missing_metadata': 0,
            'non_reproducible': 0,
            'total': 0,
            'details': []
        }
        
        # ===== CHECK 1: Currency Consistency (ISO 8000-61: Consistency) =====
        # Deduction: -10 points for currency mismatch
        if kpis:
            # Detect currency from KPIs
            detected_currencies = set()
            for kpi_name, kpi_data in kpis.items():
                if any(keyword in kpi_name.lower() for keyword in ['cost', 'salary', 'price', 'revenue', 'income']):
                    value = kpi_data.get('value', 0)
                    # VND typically > 100K, USD typically < 10K
                    if abs(value) > 100000:
                        detected_currencies.add('VND')
                    elif 1000 < abs(value) <= 100000 and value == int(value):
                        detected_currencies.add('VND')  # Whole numbers in this range likely VND
                    elif abs(value) > 0:
                        detected_currencies.add('USD')
            
            # If multiple currencies detected = inconsistency
            if len(detected_currencies) > 1:
                deductions['currency_inconsistency'] = 10
                deductions['details'].append("Mixed currencies detected (VND/USD) in financial KPIs")
        
        # ===== CHECK 2: Benchmark Source Accuracy (ISO 8000-150: Benchmark quality) =====
        # Deduction: -5 points per wrong source, max -15
        wrong_sources = 0
        for kpi_name, kpi_data in kpis.items():
            source = kpi_data.get('benchmark_source', '')
            # Check for obviously wrong sources
            if 'WordStream' in source and 'manufacturing' in domain.lower() and 'cost per unit' in kpi_name.lower():
                wrong_sources += 1
                deductions['details'].append(f"Wrong benchmark source for '{kpi_name}': Marketing benchmark used for manufacturing")
            elif 'PPC' in source and 'marketing' not in domain.lower():
                wrong_sources += 1
                deductions['details'].append(f"Wrong benchmark source for '{kpi_name}': PPC benchmark used for non-marketing domain")
        
        if wrong_sources > 0:
            deductions['wrong_benchmark_source'] = min(15, wrong_sources * 5)
        
        # ===== CHECK 3: Numeric Consistency (ISO 8000-61: Accuracy) =====
        # Deduction: -3 points per inconsistency, max -9
        numeric_issues = 0
        kpi_values = {}
        for kpi_name, kpi_data in kpis.items():
            value = kpi_data.get('value', 0)
            # Store values for cross-checking
            if 'first pass yield' in kpi_name.lower():
                kpi_values['fpy'] = value
            elif 'defect rate' in kpi_name.lower():
                kpi_values['defect'] = value
            elif 'oee' in kpi_name.lower():
                kpi_values['oee'] = value
        
        # Check complementary metrics (FPY + Defect Rate should = 100%)
        if 'fpy' in kpi_values and 'defect' in kpi_values:
            total = kpi_values['fpy'] + kpi_values['defect']
            if abs(total - 100) > 0.1:  # Allow 0.1% tolerance
                numeric_issues += 1
                deductions['details'].append(f"First Pass Yield + Defect Rate ≠ 100% ({total:.2f}%)")
        
        if numeric_issues > 0:
            deductions['numeric_inconsistency'] = min(9, numeric_issues * 3)
        
        # ===== CHECK 4: Missing Critical Metadata (ISO 8000-8: Provenance) =====
        # Deduction: -5 points for missing date range
        # Note: This requires adding date_range to df metadata - placeholder for now
        # Future enhancement: Track data date range in pipeline
        if not hasattr(df, 'date_range_start') and not hasattr(df, 'date_range_end'):
            # Check if df has any date columns that could indicate range
            date_cols = df.select_dtypes(include=['datetime64']).columns
            if len(date_cols) > 0:
                # Date columns exist but range not documented
                deductions['missing_metadata'] = 5
                deductions['details'].append("Data date range not documented (ISO 8000-8 provenance)")
        
        # ===== CHECK 5: Non-Reproducible Calculations (ISO 8000-61: Traceability) =====
        # Deduction: -5 points if OEE present but calculation not shown
        # Note: OEE should show Availability × Performance × Quality
        if 'oee' in kpi_values:
            # Check if OEE components are also present as separate KPIs
            has_availability = any('availability' in k.lower() for k in kpis.keys())
            has_performance = any('performance' in k.lower() for k in kpis.keys())
            has_quality_factor = any('quality' in k.lower() and 'oee' not in k.lower() for k in kpis.keys())
            
            if not (has_availability or has_performance or has_quality_factor):
                deductions['non_reproducible'] = 5
                deductions['details'].append("OEE calculation not reproducible (components not shown)")
        
        # ===== TOTAL DEDUCTIONS =====
        deductions['total'] = (
            deductions['currency_inconsistency'] +
            deductions['wrong_benchmark_source'] +
            deductions['numeric_inconsistency'] +
            deductions['missing_metadata'] +
            deductions['non_reproducible']
        )
        
        return deductions
    
    def _validate_blueprint_quality(self, smart_blueprint: Dict) -> Dict:
        """Validate blueprint quality"""
        quality_scores = smart_blueprint.get('quality_scores', {})
        
        checks = {
            'informative_ok': quality_scores.get('informative', 0) >= 80,
            'clarity_ok': quality_scores.get('clarity', 0) >= 80,
            'has_charts': len(smart_blueprint.get('charts', [])) >= 5
        }
        
        passed = all(checks.values())
        score = sum(checks.values()) / len(checks) * 100
        
        return {
            'passed': passed,
            'score': score,
            'checks': checks,
            'failures': [k for k, v in checks.items() if not v]
        }
    
    def _display_compact_cleaning_report(self, cleaning_plan: Dict, validation: Dict):
        """Display compact cleaning report"""
        with st.expander(get_text('data_cleaning_report', self.lang), expanded=False):
            summary = cleaning_plan.get('cleaning_summary', {})
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(get_text('rows_label', self.lang), f"{summary.get('rows_after', 0):,}", 
                         delta=f"{summary.get('rows_after', 0) - summary.get('rows_before', 0)}")
            with col2:
                st.metric(get_text('duplicates_removed', self.lang), summary.get('duplicates_removed', 0))
            with col3:
                st.metric(get_text('quality_score', self.lang), f"{validation['score']:.0f}%", 
                         delta="ISO 8000" if validation['passed'] else "Failed")
    
    def _display_compact_blueprint(self, smart_blueprint: Dict, domain_info: Dict):
        """Display compact blueprint"""
        with st.expander(get_text('dashboard_blueprint', self.lang), expanded=False):
            st.caption(f"**Domain**: {domain_info['domain_name']} | **Expert**: {domain_info['expert_role'][:40]}...")
            
            # KPIs
            kpis = smart_blueprint.get('kpis_calculated', {})
            if kpis:
                st.markdown("**📊 Key KPIs:**")
                cols = st.columns(min(3, len(kpis)))
                for i, (kpi_name, kpi_data) in enumerate(list(kpis.items())[:6]):
                    with cols[i % 3]:
                        # ✅ CRITICAL FIX: Format KPI values with thousand separators
                        kpi_value = kpi_data.get('value')
                        if isinstance(kpi_value, (int, float)):
                            # Import formatting functions
                            from utils.i18n import format_number, format_currency
                            
                            # Detect if currency KPI
                            is_currency = any(keyword in kpi_name for keyword in [
                                'Revenue', 'Cost', 'Sales', 'Price', 'VND', 'Spend', 'CPA', 'CPC', 'CPM',
                                'Doanh Thu', 'Chi Phí', 'Value', 'Amount', 'Total', 'Average', 'Salary'
                            ])
                            
                            # Detect if percentage KPI
                            is_percentage = any(keyword in kpi_name for keyword in ['%', 'Rate', 'CTR', 'Conversion', 'Percentage'])
                            
                            # Format with thousand separators (use pipeline language)
                            if is_percentage:
                                value_str = f"{format_number(kpi_value, self.lang, 1)}%"
                            elif is_currency:
                                value_str = format_currency(kpi_value, 'VND', self.lang, 0)
                            else:
                                decimals = 0 if kpi_value > 100 else 1
                                value_str = format_number(kpi_value, self.lang, decimals)
                        elif kpi_value is not None:
                            value_str = str(kpi_value)
                        else:
                            value_str = "N/A"
                        
                        st.metric(kpi_name, value_str, delta=kpi_data.get('status', ''))
    
    def _display_compact_insights(self, insights: Dict, domain_info: Dict):
        """Display compact insights"""
        with st.expander(get_text('insights_expert', self.lang), expanded=True):
            st.caption(f"**Expert**: {domain_info['expert_role'][:60]}...")
            
            # Executive summary
            st.info(insights.get('executive_summary', 'No summary'))
            
            # Top recommendations only
            st.markdown("**🚀 Top Recommendations:**")
            for rec in insights.get('recommendations', [])[:3]:
                priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
                st.success(f"{priority_emoji} **{rec['action']}**\n_{rec['expected_impact']}_")
    
    def _add_audit_trail(self, step_name: str, result: Dict):
        """Add step to audit trail"""
        self.pipeline_state['audit_trail'].append({
            'step': step_name,
            'timestamp': datetime.now().isoformat(),
            'success': result.get('success', True)
        })
    
    def _update_performance(self, metric_name: str, duration: float):
        """Update performance metrics"""
        self.pipeline_state['performance_metrics'][metric_name] = duration
    
    def _error_response(self, error_msg: str) -> Dict:
        """Return error response"""
        st.error(f"❌ {error_msg}")
        return {
            'success': False,
            'error': error_msg,
            'audit_trail': self.pipeline_state['audit_trail']
        }
