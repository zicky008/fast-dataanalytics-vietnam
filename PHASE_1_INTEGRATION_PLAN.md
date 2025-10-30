# Phase 1 Integration Plan

## Current State Analysis

**Current Code Structure**:
```python
BENCHMARK_SOURCES = {
    'hr_salary': 'Mercer Vietnam 2025 Salary Report',  # Just strings
    'hr_turnover': 'Glassdoor 2025 Employment Trends',
    # ...
}

# Usage:
source_name = BENCHMARK_SOURCES['hr_salary']  # Returns string
```

**New Curated Structure**:
```python
CURATED_BENCHMARKS = {
    'hr_salary_vietnam': {
        'name': 'VietnamWorks...',
        'url': 'https://...',
        'credibility': '⭐⭐⭐⭐⭐',
        # ... full metadata
    }
}
```

## Integration Strategy: Dual Structure

### Option 1: Backward Compatible (Recommended)

Create TWO structures:

```python
# 1. BENCHMARK_SOURCES - Keep for backward compatibility (strings only)
BENCHMARK_SOURCES = {
    'hr_salary': 'Michael Page Vietnam Salary Guide 2025',
    'hr_turnover': 'LinkedIn Workforce Report',
    # ... all 24 sources
}

# 2. BENCHMARK_METADATA - New structure with full data
BENCHMARK_METADATA = {
    'hr_salary': {
        'name': 'Michael Page Vietnam Salary Guide 2025',
        'url': 'https://www.michaelpage.com.vn/salary-guide',
        'credibility': '⭐⭐⭐⭐⭐',
        'vietnam_specific': True,
        'cost': 'FREE',
        'last_verified': '2025-10-29'
    },
    # ... all 24 sources with full metadata
}
```

**Benefits**:
- ✅ Existing code continues to work (no breaking changes)
- ✅ Can enhance PDF export to show URLs from BENCHMARK_METADATA
- ✅ Clean separation: strings for logic, metadata for display

**Implementation Steps**:

1. Replace BENCHMARK_SOURCES with curated source names
2. Add new BENCHMARK_METADATA with full data
3. Update PDF export to show URLs + credibility from BENCHMARK_METADATA
4. Test backward compatibility

### Option 2: Full Migration (More work, higher risk)

Replace all BENCHMARK_SOURCES usage with new structure:

```python
# Change from:
source_name = BENCHMARK_SOURCES['hr_salary']

# To:
source_name = BENCHMARK_SOURCES['hr_salary']['name']
```

**Drawbacks**:
- ❌ Need to update all 50+ usages in code
- ❌ Higher risk of breaking existing functionality
- ❌ More testing required

## Decision: Use Option 1

**Rationale**:
- Safer (backward compatible)
- Faster (minimal code changes)
- Clean architecture (separation of concerns)

## Implementation Checklist

- [ ] Create new BENCHMARK_SOURCES dict (24 curated sources)
- [ ] Create new BENCHMARK_METADATA dict (full data)
- [ ] Map old keys to new keys (e.g., 'hr_salary' → 'hr_salary_michaelpage')
- [ ] Update PDF export to show URLs
- [ ] Test existing functionality
- [ ] Commit and push

## Mapping Old Keys to New Keys

```python
KEY_MAPPING = {
    # HR
    'hr_salary': 'hr_salary_michaelpage',  # Vietnam-specific now!
    'hr_turnover': 'hr_turnover_global',   # LinkedIn Workforce
    'hr_satisfaction': 'hr_engagement',     # Gallup
    'hr_productivity': 'hr_engagement',     # Use Gallup for productivity too

    # Marketing
    'marketing_roi': 'marketing_email',     # Mailchimp has ROI data
    'marketing_roas': 'marketing_ppc_benchmarks',  # WordStream → Better source
    'marketing_ctr': 'marketing_ppc_benchmarks',
    'marketing_conversion': 'marketing_conversion',  # Unbounce
    'marketing_cpa': 'marketing_ppc_benchmarks',
    'marketing_engagement': 'marketing_vietnam_digital',  # DataReportal

    # E-commerce
    'ecommerce_conversion': 'ecommerce_vietnam_ebi',  # VECOM Vietnam-specific!
    'ecommerce_aov': 'ecommerce_aov',  # Adobe
    'ecommerce_cart_abandonment': 'ecommerce_cart_abandonment',  # Baymard
    'ecommerce_mobile': 'ecommerce_mobile',  # Google Vietnam
    'ecommerce_repeat': 'ecommerce_aov',  # Adobe also has repeat customer data

    # Sales
    'sales_conversion': 'sales_hubspot',
    'sales_pipeline': 'sales_hubspot',
    'sales_cycle': 'sales_hubspot',
    'sales_win_rate': 'sales_hubspot',
    'sales_growth': 'sales_linkedin',

    # Finance (keep generic for now - not in curated list)
    'finance_margin': 'general',
    'finance_liquidity': 'general',
    'finance_growth': 'general',
    'finance_efficiency': 'general',
    'finance_cash': 'general',

    # Customer Service
    'cs_response_time': 'cs_zendesk',
    'cs_resolution': 'cs_zendesk',
    'cs_satisfaction': 'cs_zendesk',
    'cs_fcr': 'cs_zendesk',
    'cs_nps': 'cs_nps_global',  # Bain NPS

    # Manufacturing (not in curated - keep generic)
    'mfg_yield': 'general',
    'mfg_defect_rate': 'general',
    'mfg_oee': 'general',
    'mfg_downtime': 'general',
    'mfg_cost': 'general',

    # General
    'general': 'general',
    'calculated': 'calculated'
}
```

## Next: Create Update Script

I'll create a Python script to:
1. Generate new BENCHMARK_SOURCES from curated list
2. Generate BENCHMARK_METADATA
3. Apply to premium_lean_pipeline.py

**Timeline**: 30 minutes
**Risk**: Low (backward compatible approach)
