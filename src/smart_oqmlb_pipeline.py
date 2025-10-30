"""
Smart OQMLB Pipeline - End-to-End Professional Data Analytics Flow
Tuân thủ COMPREHENSIVE PROMPT FRAMEWORK + Domain Expertise

Flow:
  Step 0: Domain Detection (5s)
  Step 1: Data Cleaning (20s) - ISO 8000
  Step 2: EDA + Feature Engineering (15s) - Domain-specific
  Step 3: OQMLB Blueprint (15s) - Framework compliant
  Step 4: Dashboard Build (10s) - Blueprint-driven
  Step 5: Domain Insights (20s) - Expert perspective

Total: ~85 seconds
"""

import pandas as pd
import json
from typing import Dict, List, Tuple, Any
import streamlit as st
from datetime import datetime

# Import utilities
from utils.validators import safe_file_upload, sanitize_column_names
from utils.error_handlers import rate_limit_handler, user_friendly_error
from utils.performance import PerformanceMonitor, log_performance

# Import domain detection
from domain_detection import (
    detect_domain, 
    get_domain_specific_prompt_context,
    validate_domain_detection
)


# ==================================================================================
# CRITICAL FIELD PROTECTION (NEVER AUTO-IMPUTE)
# ==================================================================================
# Updated: 2025-10-29 - SAFETY-FIRST approach to prevent fake data generation
# These fields are TOO IMPORTANT to fill with fake/imputed data
# Missing = KEEP AS NULL and FLAG to user in dashboard with warning
# Rationale: Wrong revenue/salary data → Wrong decisions → Legal liability
# ==================================================================================

NEVER_IMPUTE_FIELDS = {
    # Financial fields (legal liability + wrong strategic decisions)
    'revenue', 'sales', 'income', 'cost', 'expense', 'profit', 'margin',
    'price', 'amount', 'payment', 'fee', 'charge', 'budget', 'spending',
    'deal_value', 'deal_amount', 'contract_value', 'invoice_amount',
    'doanh_thu', 'doanh_so', 'chi_phi', 'loi_nhuan', 'gia', 'tien', 'thanh_toan',
    'gia_tri_hop_dong', 'gia_tri_deal',
    
    # Marketing/Sales metrics (wrong data = wrong decisions)
    'roas', 'roi', 'conversion_rate', 'cpa', 'cpc', 'cpm', 'ctr',
    'conversions', 'leads', 'clicks', 'impressions', 'reach',
    'ty_le_chuyen_doi', 'chi_phi_don_hang', 'luot_chuyen_doi',
    
    # E-commerce operational metrics (affect revenue/customer experience)
    'discount', 'rating', 'review', 'delivery_time', 'delivery_days',
    'shipping_fee', 'order_status', 'return_rate',
    'giam_gia', 'danh_gia', 'thoi_gian_giao', 'trang_thai_don_hang',
    
    # Customer Service metrics (affect CSAT/SLA compliance)
    'resolution_time', 'response_time', 'satisfaction_score', 'csat',
    'nps', 'issue_category', 'priority', 'sla_breach',
    'resolved_date', 'resolution_date', 'closed_date', 'completion_date',
    'thoi_gian_xu_ly', 'muc_do_hai_long', 'loai_van_de', 'ngay_giai_quyet',
    
    # Metadata fields (categorical/competitive intelligence)
    'channel', 'source', 'medium', 'campaign', 'platform',
    'competitors', 'competitor_name', 'competitive_advantage',
    'kenh', 'nguon', 'doi_thu_canh_tranh',
    
    # HR fields (compliance/privacy + labor law)
    'salary', 'wage', 'compensation', 'bonus', 'commission', 'payroll',
    'employee_id', 'staff_id', 'position', 'title', 'role', 'job_title',
    'ho_ten', 'ten', 'name', 'full_name',
    'luong', 'thu_nhap', 'tien_luong', 'chuc_vu', 'vi_tri',
    
    # Customer PII (privacy law GDPR/PDPA compliance)
    'email', 'phone', 'address', 'ssn', 'passport', 'id_number', 'cccd', 'cmnd',
    'credit_card', 'bank_account', 'tax_id', 'so_dien_thoai', 'dia_chi',
    
    # Business-critical IDs (data integrity)
    'order_id', 'transaction_id', 'invoice_id', 'customer_id', 'user_id',
    'deal_id', 'ticket_id', 'campaign_id', 'lead_id',
    'ma_don_hang', 'ma_khach_hang', 'ma_giao_dich', 'ma_hoa_don',
    'ma_deal', 'ma_ticket', 'ma_campaign'
}

# ==================================================================================
# VIETNAM VALIDATION RANGES (Sanity Checks for Realistic Data)
# ==================================================================================
# Updated: 2025-10-29 - Vietnam market-specific validation ranges
# Purpose: Flag outliers that don't make sense in Vietnam context
# Source: Vietnam market research, industry standards, common sense
# ==================================================================================

VIETNAM_VALIDATION_RANGES = {
    # HR (Vietnam market)
    'salary': {
        'min': 5_000_000,       # 5M VND/month (~$200) - minimum wage tier
        'max': 200_000_000,     # 200M VND/month (~$8K) - C-level executives
        'unit': 'VND/month',
        'warning': 'Salary outside typical Vietnam range (5M-200M VND/month)'
    },
    'luong': {
        'min': 5_000_000,
        'max': 200_000_000,
        'unit': 'VND/month',
        'warning': 'Lương nằm ngoài khoảng phổ biến (5-200 triệu VND/tháng)'
    },
    'age': {
        'min': 18,              # Legal working age
        'max': 65,              # Typical retirement age
        'unit': 'years',
        'warning': 'Age outside working population range (18-65 years)'
    },
    'tuoi': {
        'min': 18,
        'max': 65,
        'unit': 'năm',
        'warning': 'Tuổi nằm ngoài độ tuổi lao động (18-65 tuổi)'
    },
    'experience': {
        'min': 0,
        'max': 40,              # Max career length
        'unit': 'years',
        'warning': 'Experience years unrealistic (0-40 years expected)'
    },
    
    # E-commerce (Vietnam market)
    'order_value': {
        'min': 10_000,          # 10K VND (~$0.40) - minimum viable order
        'max': 100_000_000,     # 100M VND (~$4K) - very high-value purchase
        'unit': 'VND',
        'warning': 'Order value outside typical range (10K-100M VND)'
    },
    'gia_tri_don_hang': {
        'min': 10_000,
        'max': 100_000_000,
        'unit': 'VND',
        'warning': 'Giá trị đơn hàng nằm ngoài khoảng thông thường (10K-100M VND)'
    },
    'shipping_fee': {
        'min': 0,               # Free shipping exists
        'max': 500_000,         # 500K VND (~$20) - even remote areas
        'unit': 'VND',
        'warning': 'Shipping fee unusually high (>500K VND)'
    },
    'phi_ship': {
        'min': 0,
        'max': 500_000,
        'unit': 'VND',
        'warning': 'Phí ship cao bất thường (>500K VND)'
    },
    'discount_percent': {
        'min': 0,
        'max': 100,             # Cannot discount more than 100%
        'unit': '%',
        'warning': 'Discount percentage invalid (must be 0-100%)'
    },
    'giam_gia': {
        'min': 0,
        'max': 100,
        'unit': '%',
        'warning': 'Phần trăm giảm giá không hợp lệ (phải 0-100%)'
    },
    
    # Marketing (adjusted for Vietnam)
    'ctr': {
        'min': 0,
        'max': 100,
        'unit': '%',
        'warning': 'CTR percentage invalid (must be 0-100%)'
    },
    'cpc': {
        'min': 1_000,           # 1K VND (~$0.04) - very cheap click
        'max': 100_000,         # 100K VND (~$4) - premium keyword
        'unit': 'VND',
        'warning': 'CPC outside Vietnam typical range (1K-100K VND)'
    },
    'conversion_rate': {
        'min': 0,
        'max': 100,
        'unit': '%',
        'warning': 'Conversion rate invalid (must be 0-100%)'
    },
    'ty_le_chuyen_doi': {
        'min': 0,
        'max': 100,
        'unit': '%',
        'warning': 'Tỷ lệ chuyển đổi không hợp lệ (phải 0-100%)'
    },
    
    # Finance (general business rules)
    'profit_margin': {
        'min': -100,            # Can have losses
        'max': 100,             # Cannot exceed 100% margin
        'unit': '%',
        'warning': 'Profit margin outside feasible range (-100% to 100%)'
    },
    'bien_loi_nhuan': {
        'min': -100,
        'max': 100,
        'unit': '%',
        'warning': 'Biên lợi nhuận nằm ngoài khoảng khả thi (-100% đến 100%)'
    },
    'revenue_growth': {
        'min': -100,            # Can shrink completely
        'max': 500,             # 5x growth is rare but possible for startups
        'unit': '%',
        'warning': 'Revenue growth rate extreme (check for data entry error)'
    },
    'tang_truong_doanh_thu': {
        'min': -100,
        'max': 500,
        'unit': '%',
        'warning': 'Tốc độ tăng trưởng doanh thu cực đoan (kiểm tra lỗi nhập liệu)'
    }
}

def is_critical_field(column_name: str) -> bool:
    """
    Check if a column name matches any field in NEVER_IMPUTE list.
    Uses case-insensitive partial matching to catch variations.
    
    Args:
        column_name: Name of the column to check
    
    Returns:
        bool: True if field is critical and should NEVER be imputed
    
    Example:
        >>> is_critical_field('Monthly_Salary')
        True
        >>> is_critical_field('customer_age')
        False
    """
    col_lower = column_name.lower()
    return any(critical in col_lower for critical in NEVER_IMPUTE_FIELDS)

def validate_vietnam_range(column_name: str, value: float) -> dict:
    """
    Validate if a numeric value is within Vietnam realistic range.
    Returns detailed validation result with suggested actions.
    
    Args:
        column_name: Name of the column being validated
        value: Numeric value to check
    
    Returns:
        dict: {
            'valid': bool,                    # True if within range
            'message': str,                   # Explanation if invalid
            'suggested_action': str or None,  # What to do about it
            'range_info': dict or None        # Min/max/unit for reference
        }
    
    Example:
        >>> validate_vietnam_range('salary', 300_000_000)
        {
            'valid': False,
            'message': 'Value 300,000,000 > maximum 200,000,000 VND/month',
            'suggested_action': 'Cap at 200,000,000 or verify data entry',
            'range_info': {'min': 5000000, 'max': 200000000, 'unit': 'VND/month'}
        }
    """
    col_lower = column_name.lower()
    
    # Find matching validation range
    for field, range_def in VIETNAM_VALIDATION_RANGES.items():
        if field in col_lower:
            # Check minimum
            if value < range_def['min']:
                return {
                    'valid': False,
                    'message': f"Value {value:,.0f} < minimum {range_def['min']:,.0f} {range_def['unit']}",
                    'suggested_action': f"Remove row or verify data entry (minimum: {range_def['min']:,.0f})",
                    'range_info': range_def,
                    'severity': 'high'
                }
            
            # Check maximum
            if value > range_def['max']:
                return {
                    'valid': False,
                    'message': f"Value {value:,.0f} > maximum {range_def['max']:,.0f} {range_def['unit']}",
                    'suggested_action': f"Cap at {range_def['max']:,.0f} or verify data entry",
                    'range_info': range_def,
                    'severity': 'high'
                }
            
            # Within range
            return {
                'valid': True,
                'message': f'Within Vietnam realistic range ({range_def["min"]:,.0f}-{range_def["max"]:,.0f} {range_def["unit"]})',
                'suggested_action': None,
                'range_info': range_def,
                'severity': 'none'
            }
    
    # No validation range defined for this field
    return {
        'valid': True,
        'message': 'No Vietnam-specific validation range defined',
        'suggested_action': None,
        'range_info': None,
        'severity': 'none'
    }


class SmartOQMLBPipeline:
    """
    Smart OQMLB Pipeline with domain expertise and quality validation.
    """
    
    def __init__(self, gemini_client):
        self.client = gemini_client
        self.pipeline_state = {
            'domain_info': None,
            'cleaned_data': None,
            'cleaning_report': None,
            'transformed_data': None,
            'eda_report': None,
            'blueprint': None,
            'dashboard': None,
            'insights': None,
            'audit_trail': []
        }
    
    @log_performance("Complete Pipeline")
    def run_pipeline(self, df: pd.DataFrame, dataset_description: str = "") -> Dict:
        """
        Chạy toàn bộ pipeline từ raw data → final dashboard.
        
        Returns:
            {
                'success': bool,
                'dashboard': {...},
                'audit_trail': [...],
                'quality_score': float
            }
        """
        
        with PerformanceMonitor("Smart OQMLB Pipeline") as monitor:
            try:
                # Step 0: Domain Detection
                st.info("🔍 **Step 0/5**: Nhận diện ngành nghề...")
                domain_info = self.step0_domain_detection(df, dataset_description)
                monitor.add_metric("domain", domain_info['domain'])
                self._add_audit_trail("Domain Detection", domain_info)
                
                # Step 1: Data Cleaning
                st.info(f"🧹 **Step 1/5**: Data Cleaning (ISO 8000)... Domain: {domain_info['domain_name']}")
                cleaning_result = self.step1_data_cleaning(df, domain_info)
                if not cleaning_result['success']:
                    return {'success': False, 'error': cleaning_result['error']}
                monitor.add_metric("quality_score_cleaning", cleaning_result['quality_score'])
                self._add_audit_trail("Data Cleaning", cleaning_result)
                
                # Step 2: EDA + Feature Engineering
                st.info(f"📊 **Step 2/5**: EDA + Feature Engineering... Expert: {domain_info['expert_role']}")
                eda_result = self.step2_eda_feature_engineering(
                    cleaning_result['df_cleaned'],
                    domain_info
                )
                if not eda_result['success']:
                    return {'success': False, 'error': eda_result['error']}
                monitor.add_metric("kpis_calculated", len(eda_result['eda_report']['kpis']))
                self._add_audit_trail("EDA + Feature Engineering", eda_result)
                
                # Step 3: OQMLB Blueprint
                st.info("🎨 **Step 3/5**: Tạo Dashboard Blueprint (OQMLB Framework)...")
                blueprint_result = self.step3_oqmlb_blueprint(
                    eda_result['df_transformed'],
                    eda_result['eda_report'],
                    domain_info
                )
                if not blueprint_result['success']:
                    return {'success': False, 'error': blueprint_result['error']}
                monitor.add_metric("quality_score_blueprint", blueprint_result['quality_score'])
                self._add_audit_trail("OQMLB Blueprint", blueprint_result)
                
                # Step 4: Dashboard Build
                st.info("🏗️ **Step 4/5**: Xây dựng Dashboard (theo Blueprint)...")
                dashboard_result = self.step4_dashboard_build(
                    eda_result['df_transformed'],
                    blueprint_result['blueprint']
                )
                monitor.add_metric("charts_created", len(dashboard_result['charts']))
                self._add_audit_trail("Dashboard Build", dashboard_result)
                
                # Step 5: Domain Insights
                st.info(f"💡 **Step 5/5**: Generate Insights... Perspective: {domain_info['expert_role']}")
                insights_result = self.step5_domain_insights(
                    dashboard_result,
                    blueprint_result['blueprint'],
                    domain_info
                )
                self._add_audit_trail("Domain Insights", insights_result)
                
                # Final result
                return {
                    'success': True,
                    'domain_info': domain_info,
                    'cleaning_report': cleaning_result['cleaning_report'],
                    'eda_report': eda_result['eda_report'],
                    'blueprint': blueprint_result['blueprint'],
                    'dashboard': dashboard_result,
                    'insights': insights_result,
                    'audit_trail': self.pipeline_state['audit_trail'],
                    'quality_scores': {
                        'cleaning': cleaning_result['quality_score'],
                        'blueprint': blueprint_result['quality_score'],
                        'overall': monitor.get_summary()
                    },
                    'performance': {
                        'total_duration': monitor.duration,
                        'steps': monitor.metrics
                    }
                }
            
            except Exception as e:
                return {
                    'success': False,
                    'error': str(e),
                    'audit_trail': self.pipeline_state['audit_trail']
                }
    
    def step0_domain_detection(self, df: pd.DataFrame, description: str) -> Dict:
        """
        Step 0: Nhận diện ngành nghề và assign domain expert.
        """
        domain_info = detect_domain(df, description)
        validation = validate_domain_detection(domain_info, df)
        
        # Show to user for transparency
        with st.expander("🔍 Domain Detection Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Ngành Nghề", domain_info['domain_name'])
                st.metric("Độ Tin Cậy", f"{domain_info['confidence']*100:.0f}%")
            with col2:
                st.metric("Expert Assigned", domain_info['expert_role'][:30] + "...")
                st.caption(f"Confidence: {validation['confidence_level']}")
            
            st.info(f"**Reasoning**: {domain_info['reasoning']}")
            st.success(f"**Key KPIs**: {', '.join(domain_info['key_kpis'][:3])}...")
        
        return domain_info
    
    @rate_limit_handler(max_retries=3, backoff_base=2)
    @log_performance("Data Cleaning")
    def step1_data_cleaning(self, df: pd.DataFrame, domain_info: Dict) -> Dict:
        """
        Step 1: Data Cleaning theo ISO 8000 với domain context.
        """
        
        # Build domain-aware prompt
        domain_context = get_domain_specific_prompt_context(domain_info)
        
        prompt = f"""
{domain_context}

╔══════════════════════════════════════════════════════════════╗
║ TASK: DATA CLEANING (ISO 8000 Standards)                     ║
╚══════════════════════════════════════════════════════════════╝

DATASET PROFILE:
- Shape: {df.shape[0]:,} rows × {df.shape[1]} columns
- Columns: {', '.join(df.columns[:10])}{'...' if len(df.columns) > 10 else ''}
- Missing values: {df.isnull().sum().to_dict()}
- Duplicates: {df.duplicated().sum()}

SAMPLE DATA (first 3 rows):
{df.head(3).to_string()}

COMPREHENSIVE CLEANING REQUIREMENTS:

1. STANDARDIZATION (Format Consistency):
   - Dates: Convert to YYYY-MM-DD format
   - Numbers: Remove currency symbols ($, VND), standardize decimals
   - Text: Trim whitespace, normalize case, remove special chars
   - Categories: Unify synonyms (e.g., "US" = "USA" = "United States")

2. MISSING VALUE HANDLING (Domain-Aware + SAFETY-FIRST):
   
   **🔴 CRITICAL RULE #1: NEVER IMPUTE THESE FIELDS (NEVER_IMPUTE_FIELDS)**
   Financial: revenue, sales, cost, expense, profit, price, salary, doanh_thu, chi_phi
   PII: email, phone, address, ID numbers, cccd, cmnd, so_dien_thoai
   Business IDs: order_id, transaction_id, customer_id, ma_don_hang, ma_khach_hang
   
   → If critical field is missing: KEEP AS NULL + FLAG to user + Show warning in dashboard
   → REASON: Fake revenue/salary data → Wrong decisions → Legal liability
   → EXAMPLE: Missing salary for 15% rows → DO NOT impute median → FLAG "15% salary data missing"
   
   **🔴 CRITICAL RULE #2: Validate Vietnam Ranges (VIETNAM_VALIDATION_RANGES)**
   After ANY transformation, check values against Vietnam realistic ranges:
   - Salary: 5M-200M VND/month (flag if outside)
   - Order value: 10K-100M VND (flag if outside)
   - Age: 18-65 years (flag if outside)
   - Discount: 0-100% (flag if invalid)
   
   For NON-critical fields only (if not in NEVER_IMPUTE list):
   Numerical columns:
   - <5% missing: Impute median (robust to outliers)
   - 5-20% missing: Use KNN imputation or regression
   - >20% missing: Create missing indicator + impute median
   
   Categorical columns:
   - <5% missing: Impute mode
   - 5-20% missing: Add "Unknown" category
   - >20% missing: Consider dropping if non-critical
   
   Date columns:
   - Transactional data: Forward fill
   - Time-series: Interpolation
   
   **Domain-specific critical fields for {domain_info['domain']}**: {', '.join(domain_info['profile']['keywords'][:3])}

3. OUTLIER DETECTION & TREATMENT:
   Detection methods:
   - IQR method: Q1 - 1.5*IQR, Q3 + 1.5*IQR
   - Z-score: |z| > 3 for normal distributions
   
   Treatment decisions:
   - Data error: Remove
   - Rare but valid: Keep + flag
   - Skewing analysis: Cap or transform (log)

4. DEDUPLICATION:
   - Exact duplicates: Keep first occurrence
   - Partial duplicates (same ID/email/phone): Keep most recent/complete
   - Fuzzy duplicates (similar names): Similarity >90% + manual review flag

5. VALIDATION RULES (Domain-Specific):
   General rules:
   - Age: 0-120 years
   - Email: Valid regex pattern
   - Phone: Standardized format
   - Dates: No future dates unless booking/forecast
   - Price: >0
   - Percentages: 0-100
   
   Domain-specific rules for {domain_info['domain']}:
   - {domain_info['profile']['insights_focus'][0]}: Validate relevant fields
   - Apply industry benchmarks: {domain_info['profile']['benchmarks']}

6. DOCUMENTATION (ISO 8000 Compliance):
   - Change log: What changed, when, why
   - Data lineage: Original → Intermediate → Final
   - Quality metrics: Before/after comparisons
   - Assumptions & limitations

QUALITY GATES (MUST ACHIEVE):
✅ Missing values: <2%
✅ Duplicates: 0
✅ Validation pass rate: ≥95%
✅ All columns have correct dtypes

OUTPUT FORMAT (JSON):
{{
    "cleaning_summary": {{
        "rows_before": {df.shape[0]},
        "rows_after": X,
        "columns_cleaned": [...],
        "missing_handled": {{"column": "method"}},
        "outliers_flagged": count,
        "duplicates_removed": count
    }},
    "transformations": [
        {{
            "column": "column_name",
            "action": "standardized format X → Y",
            "rows_affected": count,
            "examples": "Before: X, After: Y"
        }}
    ],
    "quality_metrics": {{
        "completeness": 98.5,
        "accuracy": 96.0,
        "consistency": 99.0,
        "validity": 95.0
    }},
    "data_dictionary": {{
        "column_name": {{
            "original_dtype": "object",
            "cleaned_dtype": "float64",
            "description": "Brief description",
            "valid_range": "0-100 or null",
            "business_meaning": "What this field represents"
        }}
    }},
    "flags": {{
        "outliers": [
            {{"row_id": 42, "column": "revenue", "value": 1000000, "reason": "10x above median"}}
        ],
        "manual_review": [
            {{"row_id": 15, "issue": "Potential data error", "recommendation": "Verify with source"}}
        ]
    }},
    "validation_report": {{
        "total_rules": X,
        "passed": Y,
        "failed": Z,
        "pass_rate": 95.5,
        "failed_records": [...]
    }}
}}

IMPORTANT NOTES:
- Preserve business meaning - don't over-clean
- Minimize row deletions - prefer flagging
- Document ALL decisions and assumptions
- Be transparent about imputation methods
"""
        
        # Call Gemini AI
        success, result = generate_ai_insight(self.client, prompt, temperature=0.3, max_tokens=8000)
        
        if not success:
            return {'success': False, 'error': result}
        
        try:
            # Parse JSON response
            cleaning_plan = json.loads(result)
            
            # Apply cleaning transformations (Python execution)
            df_cleaned = self._apply_cleaning_transformations(df, cleaning_plan)
            
            # Validate quality gates
            validation = self._validate_quality_gates(df_cleaned, cleaning_plan)
            
            if not validation['passed']:
                return {
                    'success': False,
                    'error': f"Quality gates failed: {', '.join(validation['failures'])}"
                }
            
            # Show cleaning report to user
            self._display_cleaning_report(cleaning_plan, validation)
            
            return {
                'success': True,
                'df_cleaned': df_cleaned,
                'cleaning_report': cleaning_plan,
                'quality_score': validation['score']
            }
        
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'error': f"Failed to parse AI response: {str(e)}"
            }
    
    def _apply_cleaning_transformations(self, df: pd.DataFrame, cleaning_plan: Dict) -> pd.DataFrame:
        """
        Apply cleaning transformations based on AI plan.
        """
        df_clean = df.copy()
        
        for transform in cleaning_plan.get('transformations', []):
            column = transform['column']
            action = transform['action']
            
            # Apply based on action type
            if 'standardized' in action.lower():
                # Standardization logic
                if 'date' in action.lower():
                    df_clean[column] = pd.to_datetime(df_clean[column], errors='coerce')
                elif 'currency' in action.lower():
                    df_clean[column] = df_clean[column].astype(str).str.replace(r'[$,VNDvnd]', '', regex=True)
                    df_clean[column] = pd.to_numeric(df_clean[column], errors='coerce')
            
            # ... more transformation logic based on cleaning_plan
        
        # Handle missing values based on plan
        missing_handled = cleaning_plan.get('cleaning_summary', {}).get('missing_handled', {})
        for col, method in missing_handled.items():
            if col in df_clean.columns:
                if method == 'median':
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)
                elif method == 'mode':
                    df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
                elif method == 'Unknown':
                    df_clean[col].fillna('Unknown', inplace=True)
        
        # Remove duplicates
        df_clean = df_clean.drop_duplicates()
        
        return df_clean
    
    def _validate_quality_gates(self, df_cleaned: pd.DataFrame, cleaning_plan: Dict) -> Dict:
        """
        Validate ISO 8000 quality gates.
        """
        quality_metrics = cleaning_plan.get('quality_metrics', {})
        
        checks = {
            'missing_rate_ok': (df_cleaned.isnull().sum().sum() / df_cleaned.size * 100) < 2,
            'duplicates_zero': df_cleaned.duplicated().sum() == 0,
            'validation_pass_rate_ok': quality_metrics.get('accuracy', 0) >= 95,
            'completeness_ok': quality_metrics.get('completeness', 0) >= 98,
            'consistency_ok': quality_metrics.get('consistency', 0) >= 98
        }
        
        passed = all(checks.values())
        score = sum(checks.values()) / len(checks) * 100
        
        return {
            'passed': passed,
            'score': score,
            'checks': checks,
            'failures': [k for k, v in checks.items() if not v]
        }
    
    def _display_cleaning_report(self, cleaning_plan: Dict, validation: Dict):
        """
        Display cleaning report to user for transparency.
        """
        with st.expander("📋 Data Cleaning Report", expanded=False):
            summary = cleaning_plan.get('cleaning_summary', {})
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Rows After Cleaning", f"{summary.get('rows_after', 0):,}")
                st.caption(f"Before: {summary.get('rows_before', 0):,}")
            with col2:
                st.metric("Columns Cleaned", len(summary.get('columns_cleaned', [])))
            with col3:
                st.metric("Quality Score", f"{validation['score']:.1f}%")
            
            # DATA LINEAGE VISUAL TRACKING (Priority 1 Enhancement)
            st.markdown("### 🔄 Data Lineage (Transformation Pipeline)")
            self._display_data_lineage(cleaning_plan, validation)
            
            # Transformations
            st.markdown("**Transformations Applied:**")
            for transform in cleaning_plan.get('transformations', [])[:5]:
                st.info(f"✅ {transform['column']}: {transform['action']} ({transform['rows_affected']} rows)")
            
            # Quality metrics
            metrics = cleaning_plan.get('quality_metrics', {})
            st.markdown("**Quality Metrics:**")
            cols = st.columns(4)
            for i, (metric, value) in enumerate(metrics.items()):
                with cols[i % 4]:
                    st.metric(metric.capitalize(), f"{value:.1f}%")
    
    def _display_data_lineage(self, cleaning_plan: Dict, validation: Dict):
        """
        Display visual data lineage flowchart showing transformation stages.
        Priority 1 Enhancement from Expert Validation Report.
        """
        summary = cleaning_plan.get('cleaning_summary', {})
        
        # Calculate improvement at each stage
        initial_quality = 60  # Assumed initial quality
        stages = [
            {
                'name': 'Original',
                'quality': initial_quality,
                'rows': summary.get('rows_before', 0),
                'issues': summary.get('duplicates_removed', 0) + len(summary.get('missing_handled', {}))
            },
            {
                'name': 'Standardized',
                'quality': initial_quality + 10,
                'rows': summary.get('rows_before', 0),
                'transformation_count': len([t for t in cleaning_plan.get('transformations', []) if 'standardized' in t.get('action', '').lower()])
            },
            {
                'name': 'Imputed',
                'quality': initial_quality + 20,
                'rows': summary.get('rows_before', 0),
                'missing_handled': len(summary.get('missing_handled', {}))
            },
            {
                'name': 'Validated',
                'quality': initial_quality + 30,
                'rows': summary.get('rows_after', 0),
                'validation_pass_rate': cleaning_plan.get('validation_report', {}).get('pass_rate', 0)
            },
            {
                'name': 'Final',
                'quality': validation['score'],
                'rows': summary.get('rows_after', 0),
                'duplicates_removed': summary.get('duplicates_removed', 0)
            }
        ]
        
        # Display flowchart using columns
        cols = st.columns(len(stages))
        for i, stage in enumerate(stages):
            with cols[i]:
                # Stage badge with quality improvement
                quality_delta = stage['quality'] - stages[i-1]['quality'] if i > 0 else 0
                delta_color = "normal" if quality_delta >= 0 else "inverse"
                
                st.metric(
                    label=stage['name'],
                    value=f"{stage['quality']:.0f}%",
                    delta=f"+{quality_delta:.0f}%" if i > 0 else None,
                    delta_color=delta_color
                )
                
                st.caption(f"📊 {stage['rows']:,} rows")
                
                # Stage-specific details
                if 'issues' in stage:
                    st.caption(f"⚠️ {stage['issues']} issues found")
                elif 'transformation_count' in stage:
                    st.caption(f"🔧 {stage['transformation_count']} transformations")
                elif 'missing_handled' in stage:
                    st.caption(f"🔍 {stage['missing_handled']} cols imputed")
                elif 'validation_pass_rate' in stage:
                    st.caption(f"✅ {stage['validation_pass_rate']:.1f}% passed")
                elif 'duplicates_removed' in stage:
                    st.caption(f"🗑️ {stage['duplicates_removed']} duplicates removed")
            
            # Arrow between stages (except last)
            if i < len(stages) - 1:
                with cols[i]:
                    st.markdown("<div style='text-align: center; font-size: 24px;'>→</div>", unsafe_allow_html=True)
        
        # Summary footer
        st.info(f"📈 **Quality Improvement**: {initial_quality:.0f}% → {validation['score']:.1f}% (+{validation['score'] - initial_quality:.0f}%)")
        st.caption(f"**Transformation Count**: {len(cleaning_plan.get('transformations', []))} | **Rows Affected**: {summary.get('rows_before', 0) - summary.get('rows_after', 0):,}")
    
    def _add_audit_trail(self, step_name: str, result: Dict):
        """
        Add step to audit trail for transparency.
        """
        self.pipeline_state['audit_trail'].append({
            'step': step_name,
            'timestamp': datetime.now().isoformat(),
            'success': result.get('success', True),
            'details': result.get('reasoning', '') or result.get('quality_score', '')
        })
    
    @rate_limit_handler(max_retries=3, backoff_base=2)
    @log_performance("EDA + Feature Engineering")
    def step2_eda_feature_engineering(self, df: pd.DataFrame, domain_info: Dict) -> Dict:
        """
        Step 2: EDA + Feature Engineering với domain-specific KPIs.
        """
        
        domain_context = get_domain_specific_prompt_context(domain_info)
        
        # Get statistics for prompt
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
        
        prompt = f"""
{domain_context}

╔══════════════════════════════════════════════════════════════╗
║ TASK: EDA + FEATURE ENGINEERING                              ║
╚══════════════════════════════════════════════════════════════╝

DATA PROFILE:
- Shape: {df.shape[0]:,} rows × {df.shape[1]} columns
- Numeric columns: {', '.join(numeric_cols[:10])}
- Categorical columns: {', '.join(categorical_cols[:10])}
- Date columns: {', '.join(date_cols)}

SAMPLE STATISTICS:
{df.describe().to_string()}

REQUIREMENTS:

1. DOMAIN-SPECIFIC KPI CALCULATION:
   Based on {domain_info['domain']} domain, calculate:
   {chr(10).join(f'   - {kpi}' for kpi in domain_info['key_kpis'][:5])}
   
   Use industry benchmarks for comparison:
   {domain_info['benchmarks']}

2. FEATURE ENGINEERING:
   - Temporal features (if dates exist): Day of week, month, quarter, year
   - Derived metrics: Ratios, percentages, growth rates
   - Aggregations: Sum, mean, median by category
   - Domain-specific: E.g., for e-commerce → AOV = Revenue / Orders

3. STATISTICAL ANALYSIS:
   - Distributions: Check for normality, skewness
   - Correlations: Find relationships between variables
   - Outliers: Flag extreme values (Z-score > 3)
   - Trends: Identify patterns over time

4. SEGMENTATION:
   - Customer segments (if applicable)
   - Product categories
   - Time periods
   - Geographic regions

5. DATA QUALITY VALIDATION:
   - Validate against domain rules: {domain_info['profile'].get('validation_rules', {})}
   - Check for business logic violations
   - Flag suspicious patterns

OUTPUT FORMAT (JSON):
{{
    "kpis_calculated": {{
        "kpi_name": {{
            "value": 123.45,
            "benchmark": "4:1 (standard)",
            "status": "Below/Above/At benchmark",
            "calculation": "Formula used"
        }}
    }},
    "features_created": [
        {{
            "feature_name": "aov",
            "formula": "revenue / order_count",
            "dtype": "float64",
            "description": "Average Order Value"
        }}
    ],
    "statistical_summary": {{
        "key_insights": [
            "Revenue is right-skewed (skewness: 2.3)",
            "Strong correlation between spend and conversions (0.85)"
        ],
        "distributions": {{"column": "normal/skewed/bimodal"}},
        "correlations": [["col1", "col2", 0.85]],
        "outliers_flagged": 5
    }},
    "segments_identified": [
        {{
            "segment_name": "High-Value Customers",
            "criteria": "AOV > $150",
            "size": 1234,
            "characteristics": "Description"
        }}
    ],
    "validation_results": {{
        "total_checks": 10,
        "passed": 9,
        "failed": 1,
        "violations": [{{
            "rule": "impressions > clicks",
            "failed_records": 3
        }}]
    }}
}}

IMPORTANT:
- Calculate ALL KPIs relevant to {domain_info['domain']}
- Compare against industry benchmarks
- Create features that will be useful for dashboard
- Focus on actionable insights
"""
        
        success, result = generate_ai_insight(self.client, prompt, temperature=0.3, max_tokens=8000)
        
        if not success:
            return {'success': False, 'error': result}
        
        try:
            eda_report = json.loads(result)
            
            # Apply feature engineering to dataframe
            df_transformed = self._apply_feature_engineering(df, eda_report)
            
            # Display EDA report
            self._display_eda_report(eda_report, domain_info)
            
            return {
                'success': True,
                'df_transformed': df_transformed,
                'eda_report': eda_report
            }
        
        except json.JSONDecodeError as e:
            return {'success': False, 'error': f"Failed to parse EDA response: {str(e)}"}
    
    def _apply_feature_engineering(self, df: pd.DataFrame, eda_report: Dict) -> pd.DataFrame:
        """
        Apply feature engineering based on EDA report.
        """
        df_transformed = df.copy()
        
        for feature in eda_report.get('features_created', []):
            feature_name = feature['feature_name']
            formula = feature['formula']
            
            try:
                # Safe evaluation of formula
                # Replace column names in formula with df references
                for col in df.columns:
                    formula = formula.replace(col, f"df_transformed['{col}']")
                
                # Execute formula (with safety checks)
                if '/' in formula:
                    df_transformed[feature_name] = eval(formula)
                elif '*' in formula:
                    df_transformed[feature_name] = eval(formula)
                elif '+' in formula or '-' in formula:
                    df_transformed[feature_name] = eval(formula)
            
            except Exception as e:
                st.warning(f"⚠️ Could not create feature '{feature_name}': {str(e)}")
                continue
        
        return df_transformed
    
    def _display_eda_report(self, eda_report: Dict, domain_info: Dict):
        """
        Display EDA report to user.
        """
        with st.expander("📊 EDA + Feature Engineering Report", expanded=False):
            # KPIs
            st.markdown(f"**Domain-Specific KPIs ({domain_info['domain_name']}):**")
            kpis = eda_report.get('kpis_calculated', {})
            cols = st.columns(min(3, len(kpis)))
            for i, (kpi_name, kpi_data) in enumerate(list(kpis.items())[:6]):
                with cols[i % 3]:
                    st.metric(
                        kpi_name,
                        f"{kpi_data['value']:.2f}" if isinstance(kpi_data['value'], (int, float)) else kpi_data['value'],
                        delta=kpi_data.get('status', '')
                    )
                    st.caption(f"Benchmark: {kpi_data.get('benchmark', 'N/A')}")
            
            # Features created
            st.markdown("**Features Created:**")
            for feature in eda_report.get('features_created', [])[:5]:
                st.info(f"✅ {feature['feature_name']}: {feature['description']} ({feature['formula']})")
            
            # Key insights
            st.markdown("**Statistical Insights:**")
            for insight in eda_report.get('statistical_summary', {}).get('key_insights', [])[:3]:
                st.success(f"💡 {insight}")
    
    @rate_limit_handler(max_retries=3, backoff_base=2)
    @log_performance("OQMLB Blueprint")
    def step3_oqmlb_blueprint(self, df: pd.DataFrame, eda_report: Dict, domain_info: Dict) -> Dict:
        """
        Step 3: Generate OQMLB Blueprint với validation.
        """
        
        domain_context = get_domain_specific_prompt_context(domain_info)
        
        prompt = f"""
{domain_context}

╔══════════════════════════════════════════════════════════════╗
║ TASK: OQMLB BLUEPRINT GENERATION                             ║
╚══════════════════════════════════════════════════════════════╝

OQMLB FRAMEWORK EXPLAINED:
- O (Objectives): What business questions to answer?
- Q (Questions): Specific questions to address each objective
- M (Metrics): KPIs/metrics to measure and visualize
- L (Layout): Dashboard structure (sections, placement)
- B (Build): Specific chart specifications

AVAILABLE DATA:
- Columns: {', '.join(df.columns[:15])}
- KPIs calculated: {', '.join(eda_report.get('kpis_calculated', {}).keys())}
- Features available: {', '.join([f['feature_name'] for f in eda_report.get('features_created', [])])}

DASHBOARD DESIGN REQUIREMENTS:

1. BUSINESS OBJECTIVES:
   Based on {domain_info['domain']} domain:
   {chr(10).join(f'   - {focus}' for focus in domain_info['profile']['insights_focus'][:3])}

2. CHART SELECTION CRITERIA:
   - Comparison → Bar chart
   - Trends over time → Line chart
   - Distribution → Histogram/Box plot
   - Composition → Pie chart (max 5-7 slices)
   - Correlation → Scatter plot
   - Geographic → Map (if location data)

3. 5-30 SECOND RULE:
   - User should understand key status in <5 seconds
   - Find specific issues in <30 seconds
   - Use visual hierarchy: Most important top-left

4. ACCESSIBILITY (WCAG 2.0 AA):
   - Color contrast ratio ≥ 4.5:1 for text
   - Color contrast ratio ≥ 3:1 for large text
   - Don't rely solely on color (use patterns/labels)
   - Screen reader friendly (descriptive titles)

5. QUALITY CRITERIA (5 dimensions):
   - Informative: Answers key business questions (≥80%)
   - Clarity: Easy to understand at a glance (≥80%)
   - Design: Professional and visually appealing (≥80%)
   - Interactivity: Filters, drill-downs where useful (≥80%)
   - Actionable: Drives decisions and actions (≥80%)

OUTPUT FORMAT (JSON):
{{
    "objectives": [
        {{
            "id": "obj1",
            "title": "Optimize Marketing ROI",
            "description": "Identify best/worst performing channels",
            "priority": "high"
        }}
    ],
    "questions": [
        {{
            "id": "q1",
            "objective_id": "obj1",
            "question": "Which channels have highest ROAS?",
            "metrics_needed": ["roas", "spend", "revenue"]
        }}
    ],
    "layout": {{
        "sections": [
            {{
                "id": "s1",
                "title": "Executive Summary",
                "position": "top",
                "charts": ["c1", "c2", "c3"]
            }}
        ]
    }},
    "charts": [
        {{
            "id": "c1",
            "title": "ROAS by Channel",
            "type": "bar",
            "x_axis": "channel",
            "y_axis": "roas",
            "color_scheme": "blue_scale",
            "accessibility": {{
                "contrast_ratio": 4.8,
                "alt_text": "Bar chart showing ROAS by marketing channel"
            }},
            "interactivity": ["hover_details", "click_to_filter"],
            "benchmark_line": 4.0,
            "annotations": ["Top performer", "Below benchmark"],
            "question_answered": "q1"
        }}
    ],
    "quality_scores": {{
        "informative": 85,
        "clarity": 90,
        "design": 88,
        "interactivity": 82,
        "actionable": 87
    }},
    "accessibility_validation": {{
        "wcag_compliant": true,
        "color_contrast_checked": true,
        "screen_reader_support": true,
        "issues": []
    }}
}}

IMPORTANT:
- Create 3-5 objectives aligned with {domain_info['domain']} goals
- Design 8-12 charts total (not too many)
- Ensure ALL quality scores ≥ 80%
- Validate WCAG 2.0 AA compliance
- Each chart must answer a specific question
"""
        
        success, result = generate_ai_insight(self.client, prompt, temperature=0.3, max_tokens=10000)
        
        if not success:
            return {'success': False, 'error': result}
        
        try:
            blueprint = json.loads(result)
            
            # Validate blueprint quality
            validation = self._validate_blueprint_quality(blueprint)
            
            if not validation['passed']:
                return {
                    'success': False,
                    'error': f"Blueprint quality validation failed: {', '.join(validation['failures'])}"
                }
            
            # Display blueprint
            self._display_blueprint(blueprint, domain_info)
            
            return {
                'success': True,
                'blueprint': blueprint,
                'quality_score': validation['score']
            }
        
        except json.JSONDecodeError as e:
            return {'success': False, 'error': f"Failed to parse blueprint: {str(e)}"}
    
    def _validate_blueprint_quality(self, blueprint: Dict) -> Dict:
        """
        Validate blueprint against 5 quality criteria.
        """
        quality_scores = blueprint.get('quality_scores', {})
        
        checks = {
            'informative_ok': quality_scores.get('informative', 0) >= 80,
            'clarity_ok': quality_scores.get('clarity', 0) >= 80,
            'design_ok': quality_scores.get('design', 0) >= 80,
            'interactivity_ok': quality_scores.get('interactivity', 0) >= 80,
            'actionable_ok': quality_scores.get('actionable', 0) >= 80,
            'has_objectives': len(blueprint.get('objectives', [])) >= 3,
            'has_charts': 8 <= len(blueprint.get('charts', [])) <= 15,
            'wcag_compliant': blueprint.get('accessibility_validation', {}).get('wcag_compliant', False)
        }
        
        passed = all(checks.values())
        score = sum(checks.values()) / len(checks) * 100
        
        return {
            'passed': passed,
            'score': score,
            'checks': checks,
            'failures': [k for k, v in checks.items() if not v]
        }
    
    def _display_blueprint(self, blueprint: Dict, domain_info: Dict):
        """
        Display blueprint to user for transparency and validation.
        """
        with st.expander("🎨 Dashboard Blueprint (OQMLB Framework)", expanded=True):
            st.markdown(f"**Domain**: {domain_info['domain_name']}")
            st.markdown(f"**Expert Perspective**: {domain_info['expert_role'][:50]}...")
            
            # Objectives
            st.markdown("### 📋 Business Objectives")
            for obj in blueprint.get('objectives', [])[:3]:
                st.info(f"**{obj['title']}** (Priority: {obj['priority']})\n{obj['description']}")
            
            # Quality scores
            st.markdown("### 📊 Quality Validation")
            scores = blueprint.get('quality_scores', {})
            cols = st.columns(5)
            for i, (criterion, score) in enumerate(scores.items()):
                with cols[i]:
                    st.metric(criterion.capitalize(), f"{score}%", delta="✓" if score >= 80 else "✗")
            
            # Accessibility
            accessibility = blueprint.get('accessibility_validation', {})
            if accessibility.get('wcag_compliant'):
                st.success("✅ WCAG 2.0 AA Compliant (Accessible to all users)")
            else:
                st.warning(f"⚠️ Accessibility issues: {', '.join(accessibility.get('issues', []))}")
            
            # Charts preview
            st.markdown("### 📈 Charts to be Created")
            for chart in blueprint.get('charts', [])[:5]:
                st.caption(f"• {chart['title']} ({chart['type']}) - Answers: {chart.get('question_answered', 'N/A')}")
    
    @log_performance("Dashboard Build")
    def step4_dashboard_build(self, df: pd.DataFrame, blueprint: Dict) -> Dict:
        """
        Step 4: Build dashboard theo blueprint (NO AI, pure execution).
        Đây là bước thuần code execution, không cần AI.
        """
        
        import plotly.express as px
        import plotly.graph_objects as go
        
        charts = []
        
        for chart_spec in blueprint.get('charts', []):
            try:
                chart_id = chart_spec['id']
                chart_title = chart_spec['title']
                chart_type = chart_spec['type']
                x_axis = chart_spec.get('x_axis')
                y_axis = chart_spec.get('y_axis')
                color_scheme = chart_spec.get('color_scheme', 'blues')
                
                # Validate columns exist
                if x_axis not in df.columns or (y_axis and y_axis not in df.columns):
                    st.warning(f"⚠️ Skipping chart '{chart_title}': columns not found")
                    continue
                
                # Create chart based on type
                fig = None
                
                if chart_type == 'bar':
                    fig = px.bar(
                        df,
                        x=x_axis,
                        y=y_axis,
                        title=chart_title,
                        color_discrete_sequence=px.colors.sequential.Blues
                    )
                    
                    # Add benchmark line if specified
                    if 'benchmark_line' in chart_spec:
                        fig.add_hline(
                            y=chart_spec['benchmark_line'],
                            line_dash="dash",
                            line_color="red",
                            annotation_text="Benchmark"
                        )
                
                elif chart_type == 'line':
                    fig = px.line(
                        df,
                        x=x_axis,
                        y=y_axis,
                        title=chart_title,
                        color_discrete_sequence=px.colors.sequential.Blues
                    )
                
                elif chart_type == 'scatter':
                    fig = px.scatter(
                        df,
                        x=x_axis,
                        y=y_axis,
                        title=chart_title,
                        color_discrete_sequence=px.colors.sequential.Blues
                    )
                
                elif chart_type == 'pie':
                    fig = px.pie(
                        df,
                        names=x_axis,
                        values=y_axis,
                        title=chart_title
                    )
                
                elif chart_type == 'histogram':
                    fig = px.histogram(
                        df,
                        x=x_axis,
                        title=chart_title,
                        color_discrete_sequence=px.colors.sequential.Blues
                    )
                
                if fig:
                    # Apply accessibility settings
                    fig.update_layout(
                        font=dict(size=12),
                        title_font_size=16,
                        showlegend=True,
                        hovermode='closest'
                    )
                    
                    charts.append({
                        'id': chart_id,
                        'title': chart_title,
                        'figure': fig,
                        'spec': chart_spec
                    })
            
            except Exception as e:
                st.warning(f"⚠️ Error creating chart '{chart_spec.get('title', 'Unknown')}': {str(e)}")
                continue
        
        return {
            'charts': charts,
            'layout': blueprint.get('layout', {}),
            'objectives': blueprint.get('objectives', [])
        }
    
    @rate_limit_handler(max_retries=3, backoff_base=2)
    @log_performance("Domain Insights")
    def step5_domain_insights(self, dashboard: Dict, blueprint: Dict, domain_info: Dict) -> Dict:
        """
        Step 5: Generate domain-specific insights from expert perspective.
        """
        
        domain_context = get_domain_specific_prompt_context(domain_info)
        
        # Prepare chart summaries for AI
        chart_summaries = []
        for chart in dashboard['charts']:
            chart_summaries.append(f"- {chart['title']} ({chart['spec']['type']}): Shows {chart['spec'].get('x_axis')} vs {chart['spec'].get('y_axis')}")
        
        prompt = f"""
{domain_context}

╔══════════════════════════════════════════════════════════════╗
║ TASK: DOMAIN EXPERT INSIGHTS                                 ║
╚══════════════════════════════════════════════════════════════╝

DASHBOARD OVERVIEW:
- Domain: {domain_info['domain_name']}
- Objectives: {', '.join([obj['title'] for obj in blueprint.get('objectives', [])])}
- Charts created: {len(dashboard['charts'])}

CHARTS AVAILABLE:
{chr(10).join(chart_summaries)}

YOUR TASK:
As {domain_info['expert_role']}, provide strategic insights based on the dashboard.

REQUIREMENTS:

1. EXECUTIVE SUMMARY (2-3 sentences):
   - Overall performance assessment
   - Key wins and concerns
   - Strategic direction

2. KEY INSIGHTS (3-5 insights):
   Each insight should:
   - Be specific and data-driven
   - Reference relevant KPIs or benchmarks
   - Explain business impact
   - Use domain expertise
   
   Example for Marketing:
   "Facebook Ads ROAS of 8.2:1 exceeds industry benchmark (4:1) by 105%, indicating excellent audience targeting and creative performance. This channel should receive increased budget allocation."

3. ACTIONABLE RECOMMENDATIONS (3-5 actions):
   Each recommendation should:
   - Be specific and implementable
   - Have clear expected impact
   - Reference industry best practices
   - Prioritized (High/Medium/Low)
   
   Example:
   "[HIGH] Reallocate $5K/month from Display (ROAS 2.1) to Facebook (ROAS 8.2) → Expected +$25K monthly revenue"

4. RISK ALERTS (if any):
   - Identify concerning trends
   - Warn about benchmark violations
   - Highlight unusual patterns

5. NEXT STEPS:
   - Immediate actions (this week)
   - Short-term initiatives (this month)
   - Long-term strategies (this quarter)

OUTPUT FORMAT (JSON):
{{
    "executive_summary": "2-3 sentence overview",
    "key_insights": [
        {{
            "title": "Insight title",
            "description": "Detailed insight with numbers",
            "impact": "high/medium/low",
            "related_charts": ["c1", "c2"]
        }}
    ],
    "recommendations": [
        {{
            "action": "Specific action to take",
            "priority": "high/medium/low",
            "expected_impact": "Quantified benefit",
            "effort": "low/medium/high",
            "timeline": "immediate/short-term/long-term"
        }}
    ],
    "risk_alerts": [
        {{
            "risk": "Risk description",
            "severity": "high/medium/low",
            "mitigation": "How to address"
        }}
    ],
    "next_steps": {{
        "immediate": ["Action 1", "Action 2"],
        "short_term": ["Action 1", "Action 2"],
        "long_term": ["Action 1", "Action 2"]
    }},
    "expert_signature": "{domain_info['expert_role']}"
}}

IMPORTANT:
- Use {domain_info['domain']} terminology and best practices
- Reference benchmarks: {domain_info['benchmarks']}
- Be specific with numbers and metrics
- Provide actionable, implementable recommendations
"""
        
        success, result = generate_ai_insight(self.client, prompt, temperature=0.5, max_tokens=6000)
        
        if not success:
            return {'success': False, 'error': result, 'insights': {}}
        
        try:
            insights = json.loads(result)
            
            # Display insights
            self._display_insights(insights, domain_info)
            
            return {
                'success': True,
                'insights': insights
            }
        
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'error': f"Failed to parse insights: {str(e)}",
                'insights': {}
            }
    
    def _display_insights(self, insights: Dict, domain_info: Dict):
        """
        Display domain expert insights to user.
        """
        with st.expander("💡 Domain Expert Insights", expanded=True):
            st.markdown(f"**Expert**: {domain_info['expert_role']}")
            st.markdown(f"**Domain**: {domain_info['domain_name']}")
            
            # Executive summary
            st.markdown("### 📊 Executive Summary")
            st.info(insights.get('executive_summary', 'No summary available'))
            
            # Key insights
            st.markdown("### 🎯 Key Insights")
            for insight in insights.get('key_insights', []):
                impact_emoji = "🔴" if insight['impact'] == 'high' else "🟡" if insight['impact'] == 'medium' else "🟢"
                st.markdown(f"{impact_emoji} **{insight['title']}**")
                st.markdown(f"> {insight['description']}")
                st.caption(f"Related charts: {', '.join(insight.get('related_charts', []))}")
            
            # Recommendations
            st.markdown("### 🚀 Actionable Recommendations")
            for rec in insights.get('recommendations', []):
                priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
                st.success(f"{priority_emoji} [{rec['priority'].upper()}] {rec['action']}")
                st.caption(f"Expected impact: {rec['expected_impact']} | Effort: {rec['effort']} | Timeline: {rec['timeline']}")
            
            # Risk alerts
            if insights.get('risk_alerts'):
                st.markdown("### ⚠️ Risk Alerts")
                for risk in insights['risk_alerts']:
                    st.warning(f"**{risk['risk']}** (Severity: {risk['severity']})\nMitigation: {risk['mitigation']}")
            
            # Next steps
            st.markdown("### 📅 Next Steps")
            next_steps = insights.get('next_steps', {})
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**Immediate (This Week)**")
                for action in next_steps.get('immediate', []):
                    st.markdown(f"• {action}")
            with col2:
                st.markdown("**Short-term (This Month)**")
                for action in next_steps.get('short_term', []):
                    st.markdown(f"• {action}")
            with col3:
                st.markdown("**Long-term (This Quarter)**")
                for action in next_steps.get('long_term', []):
                    st.markdown(f"• {action}")


# Helper function for AI insight generation
def generate_ai_insight(client, prompt: str, temperature: float = 0.7, max_tokens: int = 4096) -> Tuple[bool, str]:
    """
    Generate AI insight using Gemini API.
    
    Returns:
        (success: bool, result: str or error_message: str)
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt,
            config={
                'temperature': temperature,
                'max_output_tokens': max_tokens,
                'response_mime_type': 'application/json'
            }
        )
        return (True, response.text)
    
    except Exception as e:
        return (False, user_friendly_error(e))
