"""
Domain Detection Module - Nhận diện ngành nghề từ dữ liệu
Mục đích: Xác định domain để apply domain-specific expertise trong toàn bộ pipeline
"""

import pandas as pd
from typing import Dict, List, Tuple
import re

# Domain profiles với expert roles và KPIs đặc thù
DOMAIN_PROFILES = {
    'e-commerce': {
        'name': 'E-commerce / Bán Hàng Trực Tuyến',
        'expert_role': 'E-commerce Growth Manager (10+ years experience, specialized in conversion optimization)',
        'keywords': ['order', 'product', 'customer', 'cart', 'checkout', 'revenue', 'quantity', 'price', 'sku', 'inventory'],
        'key_kpis': ['Total Revenue', 'AOV (Average Order Value)', 'Conversion Rate', 'Cart Abandonment Rate', 'Add-to-Cart Rate', 'Customer Lifetime Value (CLV)', 'Repeat Purchase Rate'],
        'insights_focus': ['Revenue optimization', 'Product performance', 'Customer behavior', 'Checkout funnel', 'Inventory management'],
        'benchmarks': {
            'conversion_rate': '2.5-3% (median), 5%+ (excellent)',
            'cart_abandonment': '76-79% (average), 23% (best-in-class)',
            'aov': '$81.49 (2024 median)',
            'add_to_cart_rate': '6.4% (average)',
            'repeat_purchase_rate': '30%+ (healthy)',
            'clv': 'AOV × Purchase Frequency × Customer Lifespan (3-5 years typical)'
        },
        'validation_rules': {
            'conversion_rate': '> 0, < 100',
            'cart_abandonment': '> 0, < 100',
            'aov': '> 0',
            'revenue': '= quantity * price',
            'clv': '= aov * purchase_frequency * customer_lifespan'
        },
        'data_sources': 'Smartinsights E-commerce Benchmarks 2024, Dynamic Yield, Shopify 70+ KPIs Guide',
        'clv_formula': {
            'description': 'Customer Lifetime Value',
            'formula': 'AOV × Purchase Frequency × Customer Lifespan',
            'components': {
                'aov': 'Average Order Value = Total Revenue / Number of Orders',
                'purchase_frequency': 'Average number of orders per customer per year',
                'customer_lifespan': 'Average number of years customer stays active (typically 3-5 years)',
                'alternative': 'CLV = (Annual Revenue per Customer × Customer Lifespan) - Customer Acquisition Cost'
            },
            'example': 'AOV $100 × 4 purchases/year × 3 years = $1,200 CLV'
        }
    },
    'marketing': {
        'name': 'Marketing / Quảng Cáo',
        'expert_role': 'Chief Marketing Officer (CMO) with 15+ years data-driven marketing experience',
        'keywords': ['campaign', 'channel', 'ad', 'impression', 'click', 'ctr', 'cpc', 'roas', 'spend', 'conversion'],
        'key_kpis': ['ROAS (Return on Ad Spend)', 'CPA (Cost Per Acquisition)', 'CTR', 'CPC', 'Conversion Rate', 'Customer Lifetime Value (CLV)', 'LTV:CAC Ratio'],
        'insights_focus': ['Channel performance', 'Budget allocation', 'Campaign effectiveness', 'Audience targeting', 'ROI optimization'],
        'benchmarks': {
            'ctr_search': '3.17% (average), 6.42% (top performers)',
            'ctr_display': '0.46%',
            'cpc_search': '$59.18',
            'cpc_display': '$60.76',
            'roas': '4:1 minimum (standard), 8:1 (excellent)',
            'cpa': '$59.18 (search), $60.76 (display)',
            'conversion_rate': '2-3%',
            'ltv_cac_ratio': '3:1 minimum (healthy), 5:1+ (excellent)',
            'clv': 'Varies by industry, calculate using revenue per customer × lifespan'
        },
        'validation_rules': {
            'roas': '>= 4.0',
            'ctr': '> 0',
            'spend': '> 0',
            'impressions': '> clicks',
            'ltv_cac_ratio': '>= 3.0',
            'clv': '= (avg_revenue_per_customer * customer_lifespan) - cac'
        },
        'data_sources': 'Wordstream Google Ads Benchmarks 2024, Databox Marketing KPIs Survey',
        'clv_formula': {
            'description': 'Customer Lifetime Value',
            'formula': 'CLV = (Average Revenue per Customer × Customer Lifespan) - Customer Acquisition Cost',
            'components': {
                'avg_revenue_per_customer': 'Total revenue / Number of customers',
                'customer_lifespan': 'Average number of years/months customer stays (cohort analysis)',
                'cac': 'Customer Acquisition Cost = Total Marketing Spend / New Customers',
                'ltv_cac_ratio': 'CLV / CAC (should be ≥3:1)',
                'payback_period': 'CAC / (Monthly Revenue per Customer) - should be <12 months'
            },
            'example': 'Monthly revenue $100 × 24 months - $300 CAC = $2,100 CLV (LTV:CAC = 7:1)'
        }
    },
    'sales': {
        'name': 'Sales / Kinh Doanh',
        'expert_role': 'VP of Sales (Strategic Sales Leadership)',
        'keywords': ['lead', 'opportunity', 'pipeline', 'deal', 'close', 'quota', 'rep', 'territory', 'forecast'],
        'key_kpis': ['Sales Revenue', 'Win Rate', 'Avg Deal Size', 'Sales Cycle Length', 'Quota Attainment'],
        'insights_focus': ['Pipeline health', 'Sales productivity', 'Win/loss analysis', 'Territory performance'],
        'benchmarks': {'win_rate': '15-30%', 'quota_attainment': '80%+'}
    },
    'finance': {
        'name': 'Finance / Tài Chính',
        'expert_role': 'Chief Financial Officer (CFO)',
        'keywords': ['revenue', 'expense', 'profit', 'margin', 'cost', 'budget', 'forecast', 'cash', 'invoice'],
        'key_kpis': ['Gross Profit Margin', 'Operating Margin', 'Cash Flow', 'Revenue Growth', 'Burn Rate'],
        'insights_focus': ['Profitability', 'Cost control', 'Cash management', 'Financial health'],
        'benchmarks': {'gross_margin': '40%+ (SaaS)', 'operating_margin': '20%+'}
    },
    'manufacturing': {
        'name': 'Manufacturing / Sản Xuất',
        'expert_role': 'Operations Manager (20+ years manufacturing experience, Six Sigma Black Belt)',
        'keywords': ['production', 'machine', 'units_produced', 'good_units', 'defective', 'defect', 
                     'downtime', 'oee', 'yield', 'shift', 'production_line', 'manufacturing',
                     'theoretical_max', 'actual_run', 'available_hours', 'scrap', 'quality'],
        'key_kpis': ['OEE (Overall Equipment Effectiveness)', 'First Pass Yield', 'Defect Rate', 
                     'Machine Utilization', 'Cycle Time', 'Downtime %', 'Cost per Unit', 
                     'Scrap Rate', 'Throughput'],
        'insights_focus': ['OEE optimization', 'Quality improvement', 'Downtime reduction', 
                          'Defect root cause analysis', 'Cost per unit reduction'],
        'benchmarks': {
            'oee': '85% (world-class), 60% (average)',
            'first_pass_yield': '95%+ (excellent)',
            'defect_rate': '≤2% (world-class)',
            'machine_utilization': '90%+ (excellent)',
            'downtime': '≤5% (target)'
        },
        'validation_rules': {
            'oee': '= availability × performance × quality',
            'units_produced': '= good_units + defective_units',
            'availability': '= (available_hours - downtime_hours) / available_hours',
            'performance': '= units_produced / theoretical_max_output',
            'quality': '= good_units / units_produced'
        },
        'data_sources': 'Industry standard OEE calculations, Six Sigma methodology'
    },
    'operations': {
        'name': 'Operations / Vận Hành',
        'expert_role': 'Chief Operations Officer (COO)',
        'keywords': ['inventory', 'stock', 'fulfillment', 'delivery', 'warehouse', 'logistics', 'turnaround'],
        'key_kpis': ['Inventory Turnover', 'Fulfillment Time', 'Order Accuracy', 'On-time Delivery', 'Operational Efficiency'],
        'insights_focus': ['Process efficiency', 'Inventory optimization', 'Delivery performance', 'Cost reduction'],
        'benchmarks': {'on_time_delivery': '95%+', 'order_accuracy': '99%+'}
    },
    'customer_service': {
        'name': 'Customer Service / Chăm Sóc Khách Hàng',
        'expert_role': 'Head of Customer Success',
        'keywords': ['ticket', 'support', 'response', 'resolution', 'satisfaction', 'nps', 'csat', 'churn'],
        'key_kpis': ['NPS (Net Promoter Score)', 'CSAT', 'First Response Time', 'Resolution Rate', 'Churn Rate'],
        'insights_focus': ['Customer satisfaction', 'Support efficiency', 'Churn prevention', 'Service quality'],
        'benchmarks': {'nps': '50+', 'csat': '80%+', 'first_response': '<1 hour'}
    },
    'hr': {
        'name': 'HR / Nhân Sự',
        'expert_role': 'Chief Human Resources Officer (CHRO)',
        'keywords': ['employee', 'hire', 'attrition', 'salary', 'compensation', 'payroll', 
                     'performance', 'training', 'recruitment', 'job', 'title', 'position', 
                     'experience', 'tenure', 'age', 'gender', 'education', 'department'],
        'key_kpis': ['Attrition Rate', 'Time to Hire', 'Cost per Hire', 'Employee Satisfaction', 'Training ROI', 'Average Salary', 'Salary Range'],
        'insights_focus': ['Talent retention', 'Recruitment efficiency', 'Employee engagement', 'Compensation analysis'],
        'benchmarks': {'attrition': '<15% annually', 'time_to_hire': '<30 days', 'avg_salary': '$75,000 (industry median)'}
    },
    'general': {
        'name': 'General Business Analytics',
        'expert_role': 'Senior Business Analyst',
        'keywords': [],  # Fallback domain
        'key_kpis': ['Key Metrics (Auto-detected)', 'Trends', 'Comparisons', 'Distributions'],
        'insights_focus': ['Data patterns', 'Trends', 'Anomalies', 'Relationships'],
        'benchmarks': {}
    }
}


def detect_domain(df: pd.DataFrame, dataset_description: str = "") -> Dict:
    """
    Phát hiện domain/ngành nghề từ dữ liệu và description.
    
    Args:
        df: Raw DataFrame
        dataset_description: User-provided description (optional)
    
    Returns:
        {
            'domain': 'marketing',
            'confidence': 0.85,
            'profile': {...},
            'reasoning': 'Detected keywords: campaign, channel, spend, roas...'
        }
    """
    
    # 1. Normalize text for matching
    all_text = ' '.join([
        dataset_description.lower(),
        ' '.join(df.columns.str.lower()),
        ' '.join(df.select_dtypes(include=['object']).columns.str.lower())
    ])
    
    # 2. Score each domain
    domain_scores = {}
    for domain_key, profile in DOMAIN_PROFILES.items():
        if domain_key == 'general':
            continue  # Skip general, use as fallback
        
        # Count keyword matches
        keyword_matches = sum(1 for kw in profile['keywords'] if kw in all_text)
        score = keyword_matches / len(profile['keywords']) if profile['keywords'] else 0
        
        domain_scores[domain_key] = {
            'score': score,
            'matched_keywords': [kw for kw in profile['keywords'] if kw in all_text]
        }
    
    # 3. Find best match
    if not domain_scores:
        best_domain = 'general'
        confidence = 0.0
        matched_keywords = []
    else:
        best_domain = max(domain_scores, key=lambda k: domain_scores[k]['score'])
        confidence = domain_scores[best_domain]['score']
        matched_keywords = domain_scores[best_domain]['matched_keywords']
    
    # 4. Use 'general' if confidence too low
    # Lowered threshold to 0.15 (1-2 keyword matches sufficient for small datasets)
    if confidence < 0.15:
        best_domain = 'general'
        confidence = 0.5  # Low confidence, but still proceed
    
    profile = DOMAIN_PROFILES[best_domain]
    
    return {
        'domain': best_domain,
        'domain_name': profile['name'],
        'confidence': confidence,
        'profile': profile,
        'reasoning': f"Detected {len(matched_keywords)} domain keywords: {', '.join(matched_keywords[:5])}..." if matched_keywords else "No specific domain detected, using general analytics",
        'expert_role': profile['expert_role'],
        'key_kpis': profile['key_kpis'],
        'benchmarks': profile['benchmarks']
    }


def get_domain_specific_prompt_context(domain_info: Dict) -> str:
    """
    Tạo context cho AI prompt dựa trên domain.
    Giúp AI đóng đúng vai trò expert của ngành.
    """
    
    profile = domain_info['profile']
    
    context = f"""
╔══════════════════════════════════════════════════════════════╗
║ DOMAIN CONTEXT (Ngành Nghề)                                  ║
╚══════════════════════════════════════════════════════════════╝

Domain: {domain_info['domain_name']}
Confidence: {domain_info['confidence']*100:.0f}%
Reasoning: {domain_info['reasoning']}

╔══════════════════════════════════════════════════════════════╗
║ YOUR EXPERT ROLE                                              ║
╚══════════════════════════════════════════════════════════════╝

You are: {profile['expert_role']}

Key Responsibilities:
- Apply domain-specific best practices
- Use industry-standard KPIs: {', '.join(profile['key_kpis'])}
- Focus insights on: {', '.join(profile['insights_focus'])}
- Compare against benchmarks: {profile['benchmarks']}

╔══════════════════════════════════════════════════════════════╗
║ DOMAIN EXPERTISE GUIDELINES                                   ║
╚══════════════════════════════════════════════════════════════╝

1. Use industry-specific terminology
2. Apply domain best practices (e.g., {profile['insights_focus'][0]})
3. Reference relevant benchmarks when available
4. Provide actionable recommendations from expert perspective
5. Consider domain-specific constraints and opportunities

"""
    return context


def validate_domain_detection(domain_info: Dict, df: pd.DataFrame) -> Dict:
    """
    Validate domain detection quality.
    Show confidence metrics to user for transparency.
    """
    
    validation = {
        'is_valid': domain_info['confidence'] >= 0.3,
        'confidence_level': 'High' if domain_info['confidence'] >= 0.7 else 'Medium' if domain_info['confidence'] >= 0.5 else 'Low',
        'detected_domain': domain_info['domain_name'],
        'expert_assigned': domain_info['expert_role'],
        'relevant_kpis': domain_info['key_kpis'],
        'data_compatibility': check_data_compatibility(df, domain_info)
    }
    
    return validation


def check_data_compatibility(df: pd.DataFrame, domain_info: Dict) -> Dict:
    """
    Kiểm tra xem data có phù hợp với domain detected không.
    Ví dụ: Marketing domain cần có columns như spend, impressions, etc.
    """
    
    profile = domain_info['profile']
    required_cols = profile['keywords']
    
    # Check how many expected columns exist
    existing_cols = [kw for kw in required_cols if any(kw in col.lower() for col in df.columns)]
    compatibility_score = len(existing_cols) / len(required_cols) if required_cols else 0.5
    
    return {
        'score': compatibility_score,
        'existing_columns': existing_cols,
        'missing_columns': [kw for kw in required_cols if kw not in existing_cols][:5],  # Show top 5
        'recommendation': 'Data structure matches domain expectations' if compatibility_score >= 0.5 else 'Data may require additional columns for full domain analysis'
    }
