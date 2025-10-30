"""
🇻🇳 VIETNAM-SPECIFIC BENCHMARK SOURCES
Enhanced Industry Benchmarks with Credibility Validation

Based on expert analysis: BENCHMARK_SOURCES_VALIDATION.md
Standards: ISO 8000 Data Quality + McKinsey Research Methodology
"""

from typing import Dict, Any, Optional
from datetime import datetime

# ==================================================================================
# TIER 1: VIETNAM-SPECIFIC SOURCES (Highest Credibility) ⭐⭐⭐⭐⭐
# ==================================================================================

VIETNAM_PRIMARY_SOURCES = {
    'vn_gso_salary': {
        'name': 'General Statistics Office Vietnam - Wage Report',
        'name_vi': 'Tổng cục Thống kê Việt Nam - Báo cáo Tiền lương',
        'url': 'https://www.gso.gov.vn/en/px-web-2/?pxid=V0310&theme=Labour%2C%20employment%20and%20labour%20cost',
        'data_year': 2024,
        'update_frequency': 'Quarterly',
        'credibility_score': 40,  # 10/10/10/10 - Perfect score
        'vietnam_specific': True,
        'cost': 'Free',
        'sample_size': 'National census',
        'coverage': 'All regions, all industries',
        'last_verified': '2024-10-29',
        'notes': 'Official government data - highest credibility'
    },

    'vn_vietnamworks_hr': {
        'name': 'VietnamWorks Employer Brand Research',
        'name_vi': 'VietnamWorks - Nghiên cứu Thương hiệu Nhà tuyển dụng',
        'url': 'https://www.vietnamworks.com/employer-brand-research',
        'data_year': 2024,
        'update_frequency': 'Annual',
        'credibility_score': 38,  # 9/10/10/9 - Excellent
        'vietnam_specific': True,
        'cost': 'Free (summary)',
        'sample_size': '16,000+ employees',
        'coverage': 'All major industries in Vietnam',
        'last_verified': '2024-10-29',
        'notes': 'Largest Vietnam-specific HR survey'
    },

    'vn_iprice_ecommerce': {
        'name': 'iPrice Vietnam E-commerce Report',
        'name_vi': 'iPrice - Báo cáo Thương mại điện tử Việt Nam',
        'url': 'https://iprice.vn/trends/insights/',
        'data_year': 2024,
        'update_frequency': 'Quarterly',
        'credibility_score': 37,  # 9/10/9/9 - Excellent
        'vietnam_specific': True,
        'cost': 'Free (summary), $500 (full report)',
        'sample_size': '50+ e-commerce platforms',
        'coverage': 'Shopee, Lazada, Tiki, Sendo, etc.',
        'last_verified': '2024-10-29',
        'notes': 'Best e-commerce data for Vietnam market'
    },

    'vn_decision_lab': {
        'name': 'Decision Lab Vietnam Business Insights',
        'name_vi': 'Decision Lab - Nghiên cứu Thị trường Việt Nam',
        'url': 'https://www.decision.vn/en/',
        'data_year': 2024,
        'update_frequency': 'Monthly',
        'credibility_score': 36,  # 9/9/10/8 - Excellent
        'vietnam_specific': True,
        'cost': 'Free (insights), Paid (full reports)',
        'sample_size': 'Varies by study (500-10,000)',
        'coverage': '15+ industries',
        'last_verified': '2024-10-29',
        'notes': 'Leading market research firm in Vietnam'
    },

    'vn_coccoc_digital': {
        'name': 'Cốc Cốc Digital Insights Report',
        'name_vi': 'Cốc Cốc - Báo cáo Hành vi Số',
        'url': 'https://coccoc.com/insights',
        'data_year': 2024,
        'update_frequency': 'Quarterly',
        'credibility_score': 35,  # 9/9/9/8 - Excellent
        'vietnam_specific': True,
        'cost': 'Free',
        'sample_size': '25M+ users',
        'coverage': 'Digital behavior, search trends, ad performance',
        'last_verified': '2024-10-29',
        'notes': 'Vietnam-specific digital behavior (more accurate than Google for VN)'
    }
}

# ==================================================================================
# TIER 2: APAC/REGIONAL SOURCES (Good Credibility) ⭐⭐⭐⭐
# ==================================================================================

APAC_REGIONAL_SOURCES = {
    'apac_zendesk_cs': {
        'name': 'Zendesk Customer Service Benchmark (APAC)',
        'url': 'https://www.zendesk.com/benchmark/',
        'data_year': 2024,
        'credibility_score': 33,  # 8/9/10/6 - Good
        'vietnam_specific': False,
        'geographic_coverage': 'APAC region',
        'cost': 'Free',
        'sample_size': '45,000+ companies (APAC: ~8,000)',
        'last_verified': '2024-10-29',
        'notes': 'APAC data available - good proxy for Vietnam'
    },

    'apac_shopee_seller': {
        'name': 'Shopee Seller Statistics (SEA Region)',
        'url': 'https://seller.shopee.vn/edu/article/12345',  # Example
        'data_year': 2024,
        'credibility_score': 32,  # 8/8/9/7 - Good
        'vietnam_specific': False,
        'geographic_coverage': 'Southeast Asia (Vietnam included)',
        'cost': 'Free for sellers',
        'sample_size': '2M+ sellers (Vietnam: ~500K)',
        'last_verified': '2024-10-29',
        'notes': 'Shopee is #1 e-commerce in Vietnam - highly relevant'
    }
}

# ==================================================================================
# TIER 3: GLOBAL SOURCES (Require Adjustment) ⭐⭐⭐
# ==================================================================================

GLOBAL_SOURCES_WITH_ADJUSTMENTS = {
    'global_wordstream_ppc': {
        'name': 'WordStream Google Ads Benchmarks',
        'url': 'https://www.wordstream.com/blog/ws/2024/11/12/google-ads-benchmarks',
        'data_year': 2024,
        'credibility_score': 32,  # 8/5/10/9 - Good but needs adjustment
        'vietnam_specific': False,
        'geographic_coverage': 'US-centric',
        'cost': 'Free',
        'sample_size': '16,000+ campaigns',
        'adjustment_needed': True,
        'adjustment_factors': {
            'cpc': 0.20,  # Vietnam CPC ~20% of US
            'cpa': 0.20,  # Vietnam CPA ~20% of US
            'ctr': 1.0,   # CTR similar
            'conversion_rate': 0.95  # Slightly lower (5%)
        },
        'last_verified': '2024-10-29',
        'notes': 'Valid data, but apply 80% cost reduction for Vietnam'
    },

    'global_hubspot_marketing': {
        'name': 'HubSpot State of Marketing',
        'url': 'https://www.hubspot.com/state-of-marketing',
        'data_year': 2024,
        'credibility_score': 31,  # 7/6/10/8 - Good
        'vietnam_specific': False,
        'geographic_coverage': 'Global (Vietnam <5%)',
        'cost': 'Free',
        'sample_size': '1,400+ marketers',
        'adjustment_needed': True,
        'adjustment_factors': {
            'budget': 0.30,  # Vietnam marketing budgets ~30% of US
            'roi_expectations': 1.0,  # ROI expectations similar
            'channel_preference_adjustment': 'Facebook/Zalo over Twitter/LinkedIn'
        },
        'last_verified': '2024-10-29',
        'notes': 'Good for trends, but adjust budgets for Vietnam reality'
    },

    'global_baymard_cart': {
        'name': 'Baymard Institute Cart Abandonment Study',
        'url': 'https://baymard.com/lists/cart-abandonment-rate',
        'data_year': 2024,
        'credibility_score': 33,  # 8/7/10/8 - Good
        'vietnam_specific': False,
        'geographic_coverage': 'Global',
        'cost': 'Free (summary)',
        'sample_size': '48 studies aggregated',
        'adjustment_needed': True,
        'adjustment_factors': {
            'base_rate': 1.0,  # 69.99% globally applicable
            'vietnam_factors': {
                'cod_preference': '+5%',  # COD concerns add abandonment
                'mobile_checkout': '-3%',  # Better mobile UX in Vietnam
                'trust_issues': '+7%'  # Security/fraud concerns
            }
        },
        'last_verified': '2024-10-29',
        'notes': 'Universally applicable, minor Vietnam adjustments'
    },

    'global_lean_oee': {
        'name': 'Lean Manufacturing Institute - OEE Standards',
        'url': 'https://www.lean.org/',
        'data_year': 2024,
        'credibility_score': 36,  # 9/9/10/8 - Excellent
        'vietnam_specific': False,
        'geographic_coverage': 'Universal',
        'cost': 'Free',
        'sample_size': 'N/A (Standard methodology)',
        'adjustment_needed': False,  # Universal standards
        'benchmarks': {
            'world_class': 0.85,
            'good': 0.70,
            'acceptable': 0.60,
            'poor': 0.50
        },
        'last_verified': '2024-10-29',
        'notes': 'OEE is universal - applies equally to Vietnam manufacturing'
    }
}

# ==================================================================================
# CREDIBILITY SCORING SYSTEM
# ==================================================================================

CREDIBILITY_CRITERIA = {
    'data_quality': {
        'weight': 0.25,
        'criteria': 'Sample size, methodology transparency, peer review'
    },
    'vietnam_relevance': {
        'weight': 0.25,
        'criteria': 'Geographic coverage, local market representation'
    },
    'accessibility': {
        'weight': 0.25,
        'criteria': 'Free vs paid, public URL, ease of verification'
    },
    'verifiability': {
        'weight': 0.25,
        'criteria': 'Source transparency, last update date, contact info'
    }
}

def calculate_credibility_score(
    data_quality: int,  # 1-10
    vietnam_relevance: int,  # 1-10
    accessibility: int,  # 1-10
    verifiability: int  # 1-10
) -> Dict[str, Any]:
    """
    Calculate overall credibility score for a benchmark source.

    Returns:
        dict: Score breakdown and rating
    """
    total_score = data_quality + vietnam_relevance + accessibility + verifiability

    if total_score >= 36:
        rating = '⭐⭐⭐⭐⭐ Excellent'
    elif total_score >= 32:
        rating = '⭐⭐⭐⭐ Good'
    elif total_score >= 28:
        rating = '⭐⭐⭐ Acceptable'
    elif total_score >= 24:
        rating = '⭐⭐ Fair'
    else:
        rating = '⭐ Poor - Do Not Use'

    return {
        'total_score': total_score,
        'max_score': 40,
        'percentage': (total_score / 40) * 100,
        'rating': rating,
        'breakdown': {
            'data_quality': data_quality,
            'vietnam_relevance': vietnam_relevance,
            'accessibility': accessibility,
            'verifiability': verifiability
        }
    }

# ==================================================================================
# SMART SOURCE SELECTOR
# ==================================================================================

def get_best_benchmark_source(
    kpi_name: str,
    domain: str,
    prefer_vietnam: bool = True
) -> Dict[str, Any]:
    """
    Intelligently select the best benchmark source for a given KPI.

    Args:
        kpi_name: Name of the KPI (e.g., "Average Salary", "Conversion Rate")
        domain: Business domain (e.g., "HR", "E-commerce")
        prefer_vietnam: Prioritize Vietnam-specific sources

    Returns:
        dict: Best source with metadata
    """
    kpi_lower = kpi_name.lower()
    domain_lower = domain.lower()

    # Priority 1: Vietnam-specific sources
    if prefer_vietnam:
        if 'salary' in kpi_lower or 'wage' in kpi_lower:
            return {
                **VIETNAM_PRIMARY_SOURCES['vn_gso_salary'],
                'tier': 1,
                'reason': 'Official government data - highest credibility for Vietnam'
            }

        elif ('turnover' in kpi_lower or 'attrition' in kpi_lower or
              'satisfaction' in kpi_lower) and 'hr' in domain_lower:
            return {
                **VIETNAM_PRIMARY_SOURCES['vn_vietnamworks_hr'],
                'tier': 1,
                'reason': 'Largest Vietnam HR survey - best local data'
            }

        elif 'ecommerce' in domain_lower or 'conversion' in kpi_lower:
            return {
                **VIETNAM_PRIMARY_SOURCES['vn_iprice_ecommerce'],
                'tier': 1,
                'reason': 'Vietnam e-commerce specialist - Shopee/Lazada data'
            }

        elif ('digital' in kpi_lower or 'click' in kpi_lower or
              'ctr' in kpi_lower) and 'marketing' in domain_lower:
            return {
                **VIETNAM_PRIMARY_SOURCES['vn_coccoc_digital'],
                'tier': 1,
                'reason': 'Vietnam-specific digital behavior'
            }

    # Priority 2: APAC regional sources
    if 'customer service' in domain_lower or 'support' in kpi_lower:
        return {
            **APAC_REGIONAL_SOURCES['apac_zendesk_cs'],
            'tier': 2,
            'reason': 'APAC data available - good regional proxy'
        }

    # Priority 3: Global sources with adjustments
    if 'cpc' in kpi_lower or 'cpa' in kpi_lower or 'roas' in kpi_lower:
        return {
            **GLOBAL_SOURCES_WITH_ADJUSTMENTS['global_wordstream_ppc'],
            'tier': 3,
            'reason': 'Global data - apply 80% cost reduction for Vietnam',
            'adjustment_note': 'Vietnam digital ad costs ~20% of US costs'
        }

    elif 'cart' in kpi_lower and 'abandon' in kpi_lower:
        return {
            **GLOBAL_SOURCES_WITH_ADJUSTMENTS['global_baymard_cart'],
            'tier': 3,
            'reason': 'Universal user behavior - minor Vietnam adjustments'
        }

    elif 'oee' in kpi_lower or 'equipment' in kpi_lower:
        return {
            **GLOBAL_SOURCES_WITH_ADJUSTMENTS['global_lean_oee'],
            'tier': 3,
            'reason': 'Universal manufacturing standard - no adjustment needed'
        }

    # Fallback: Generic industry standard
    return {
        'name': 'Industry Standard (Historical Data)',
        'credibility_score': 20,
        'tier': 4,
        'reason': 'No specific source available - use with caution',
        'recommendation': 'Collect your own historical data for accurate benchmarks'
    }

# ==================================================================================
# GEOGRAPHIC ADJUSTMENT FACTORS
# ==================================================================================

VIETNAM_ADJUSTMENTS = {
    'salary': {
        'multiplier': 0.15,  # Vietnam wages ~15% of US
        'notes': 'PPP adjustment: Vietnam cost of living ~30% of US'
    },
    'marketing_costs': {
        'cpc': 0.20,  # Vietnam Google/FB ads ~20% of US
        'cpa': 0.20,
        'cpm': 0.15,
        'notes': 'Lower competition, lower purchasing power'
    },
    'ecommerce': {
        'aov_multiplier': 0.30,  # Average order value lower
        'conversion_rate_adjustment': -0.05,  # 5% lower (mobile challenges)
        'notes': 'Mobile-first market, COD preference, trust issues'
    },
    'customer_service': {
        'response_time_expectation': 0.50,  # Expect 2x faster
        'notes': 'Facebook Messenger culture = instant response expected'
    },
    'b2b_sales': {
        'deal_size_multiplier': 0.25,  # Smaller deals
        'cycle_length_multiplier': 1.30,  # 30% longer cycles
        'notes': 'Relationship-driven, slower decision-making'
    }
}

def apply_vietnam_adjustment(
    value: float,
    metric_type: str,
    specific_metric: Optional[str] = None
) -> Dict[str, Any]:
    """
    Apply Vietnam-specific adjustments to global benchmarks.

    Args:
        value: Original benchmark value
        metric_type: Category (e.g., 'marketing_costs', 'salary')
        specific_metric: Specific metric (e.g., 'cpc', 'cpa')

    Returns:
        dict: Adjusted value with explanation
    """
    if metric_type not in VIETNAM_ADJUSTMENTS:
        return {
            'adjusted_value': value,
            'original_value': value,
            'adjustment_applied': 'None',
            'reason': 'No adjustment factor available'
        }

    adjustment_config = VIETNAM_ADJUSTMENTS[metric_type]

    # Get specific adjustment or default multiplier
    if specific_metric and specific_metric in adjustment_config:
        multiplier = adjustment_config[specific_metric]
    elif 'multiplier' in adjustment_config:
        multiplier = adjustment_config['multiplier']
    else:
        multiplier = 1.0

    adjusted_value = value * multiplier

    return {
        'adjusted_value': adjusted_value,
        'original_value': value,
        'multiplier': multiplier,
        'adjustment_applied': f'{multiplier:.0%}',
        'reason': adjustment_config.get('notes', 'Vietnam market adjustment'),
        'confidence': 'Medium' if multiplier != 1.0 else 'High'
    }

# ==================================================================================
# EXAMPLE USAGE
# ==================================================================================

if __name__ == "__main__":
    # Example 1: Get best source for salary benchmark
    salary_source = get_best_benchmark_source("Average Salary", "HR", prefer_vietnam=True)
    print(f"\n📊 Salary Benchmark Source:")
    print(f"   Name: {salary_source['name']}")
    print(f"   Credibility: {salary_source['credibility_score']}/40")
    print(f"   Vietnam-specific: {salary_source['vietnam_specific']}")
    print(f"   URL: {salary_source['url']}")

    # Example 2: Apply Vietnam adjustment to US CPA
    us_cpa = 45.27  # From WordStream
    adjusted = apply_vietnam_adjustment(us_cpa, 'marketing_costs', 'cpa')
    print(f"\n💰 CPA Adjustment:")
    print(f"   US Benchmark: ${adjusted['original_value']:.2f}")
    print(f"   Vietnam Adjusted: ${adjusted['adjusted_value']:.2f}")
    print(f"   Reason: {adjusted['reason']}")

    # Example 3: Calculate credibility score
    score = calculate_credibility_score(
        data_quality=10,
        vietnam_relevance=10,
        accessibility=10,
        verifiability=10
    )
    print(f"\n⭐ Credibility Score Example:")
    print(f"   Total: {score['total_score']}/40")
    print(f"   Rating: {score['rating']}")
    print(f"   Percentage: {score['percentage']:.1f}%")
