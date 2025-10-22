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
from typing import Dict, List, Tuple, Any
import streamlit as st
from datetime import datetime
import time
import google.generativeai as genai

# Import utilities
from utils.validators import safe_file_upload, sanitize_column_names
from utils.error_handlers import rate_limit_handler, user_friendly_error
from utils.performance import PerformanceMonitor, log_performance

# Import domain detection
from domain_detection import (
    detect_domain, 
    get_domain_specific_prompt_context,
    DOMAIN_PROFILES
)


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
    
    def __init__(self, gemini_client):
        self.client = gemini_client
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
                progress_placeholder.info("🔍 **Bước 0/4**: Nhận diện ngành nghề...")
            
            domain_info = self.step0_domain_detection(df, dataset_description)
            self._add_audit_trail("Domain Detection", domain_info)
            self._update_performance("domain_detection", time.time() - start_time)
            
            # Step 1: Data Cleaning (15s - ISO 8000)
            step1_start = time.time()
            if is_streamlit_context():
                progress_placeholder.info(f"🧹 **Bước 1/4**: Làm sạch dữ liệu (ISO 8000)... Domain: {domain_info['domain_name']}")
            
            cleaning_result = self.step1_data_cleaning(df, domain_info)
            if not cleaning_result['success']:
                return self._error_response(cleaning_result['error'])
            
            self._add_audit_trail("Data Cleaning", cleaning_result)
            self._update_performance("data_cleaning", time.time() - step1_start)
            
            # Step 2: Smart Blueprint (15s - EDA + Blueprint combined)
            step2_start = time.time()
            if is_streamlit_context():
                progress_placeholder.info(f"🎨 **Bước 2/4**: Tạo Dashboard Blueprint thông minh... Expert: {domain_info['expert_role'][:50]}...")
            
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
                progress_placeholder.info("🏗️ **Bước 3/4**: Xây dựng Dashboard (theo Blueprint)...")
            
            dashboard_result = self.step3_dashboard_build(
                cleaning_result['df_cleaned'],
                blueprint_result['smart_blueprint']
            )
            
            self._add_audit_trail("Dashboard Build", dashboard_result)
            self._update_performance("dashboard_build", time.time() - step3_start)
            
            # Step 4: Domain Insights (15s - expert perspective)
            step4_start = time.time()
            if is_streamlit_context():
                progress_placeholder.info(f"💡 **Bước 4/4**: Tạo Insights chuyên gia... Perspective: {domain_info['expert_role'][:50]}...")
            
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
                progress_placeholder.success(f"✅ **Hoàn thành!** Pipeline chạy trong {total_time:.1f} giây")
            
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
                    'cleaning': cleaning_result['quality_score'],
                    'blueprint': blueprint_result['quality_score'],
                    'overall': (cleaning_result['quality_score'] + blueprint_result['quality_score']) / 2
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
            with st.expander("🔍 Nhận Diện Ngành Nghề", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Ngành nghề", domain_info['domain_name'])
                    st.metric("Độ tin cậy", f"{domain_info['confidence']*100:.0f}%")
                with col2:
                    st.caption(f"**Chuyên gia**: {domain_info['expert_role'][:60]}...")
                    st.caption(f"**Key KPIs**: {', '.join(domain_info['key_kpis'][:3])}")
        
        return domain_info
    
    @rate_limit_handler(max_retries=3, backoff_base=2)
    @log_performance("Data Cleaning")
    def step1_data_cleaning(self, df: pd.DataFrame, domain_info: Dict) -> Dict:
        """
        Step 1: ISO 8000 data cleaning (15s)
        """
        
        domain_context = get_domain_specific_prompt_context(domain_info)
        
        # Simplified cleaning prompt (faster)
        prompt = f"""
{domain_context}

TASK: Fast Professional Data Cleaning (ISO 8000)

DATA: {df.shape[0]} rows × {df.shape[1]} columns
Columns: {', '.join(df.columns[:15])}
Missing: {df.isnull().sum().sum()} values
Duplicates: {df.duplicated().sum()} rows

REQUIREMENTS (Essential Only):
1. Fix missing values (median/mode)
2. Remove duplicates
3. Standardize formats (dates, numbers)
4. Basic validation against domain rules

QUALITY GATES:
- Missing <2%
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
            
            # Apply cleaning (simplified)
            df_cleaned = self._apply_fast_cleaning(df, cleaning_plan)
            
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
        domain = domain_info.get('domain_name', 'general').lower()
        
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
            kpis['Average Salary'] = {
                'value': float(df[salary_col].mean()),
                'benchmark': 75000,
                'status': 'Above' if df[salary_col].mean() >= 75000 else 'Below',
                'column': salary_col
            }
            
            kpis['Median Salary'] = {
                'value': float(df[salary_col].median()),
                'benchmark': 70000,
                'status': 'Above' if df[salary_col].median() >= 70000 else 'Below',
                'column': salary_col
            }
            
            kpis['Salary Range'] = {
                'value': float(df[salary_col].max() - df[salary_col].min()),
                'benchmark': 200000,
                'status': 'Wide Range',
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
            if roi_cols and len(roi_cols) > 0:
                roi_col = roi_cols[0]
                avg_roi = df[roi_col].mean()
                kpis['Average ROI'] = {
                    'value': float(avg_roi),
                    'benchmark': 4.0,
                    'status': 'Above' if avg_roi >= 4.0 else 'Below',
                    'column': roi_col
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
                        'benchmark': 4.0,
                        'status': 'Above' if roas >= 4.0 else 'Below',
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
                    kpis['CTR (%)'] = {
                        'value': float(ctr),
                        'benchmark': 2.0,  # Industry avg ~2%
                        'status': 'Above' if ctr >= 2.0 else 'Below',
                        'column': f"{click_col}/{impression_col}"
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
                        'benchmark': 2.5,  # Industry avg ~2.5%
                        'status': 'Above' if conv_rate >= 2.5 else 'Below',
                        'column': f"{conversion_col}/{click_col}"
                    }
            
            # 6. Total Spend (if available)
            if spend_cols:
                cost_col = spend_cols[0]
                kpis['Total Spend'] = {
                    'value': float(df[cost_col].sum()),
                    'benchmark': 100000,
                    'status': 'Check',
                    'column': cost_col
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
            
            # 1. Conversion Rate = (Transactions / Sessions) × 100
            if transaction_cols and session_cols:
                trans_col = transaction_cols[0]
                sess_col = session_cols[0]
                total_transactions = df[trans_col].sum()
                total_sessions = df[sess_col].sum()
                if total_sessions > 0:
                    conversion_rate = (total_transactions / total_sessions) * 100
                    kpis['Conversion Rate (%)'] = {
                        'value': float(conversion_rate),
                        'benchmark': 2.5,  # Industry avg 2.5-3%
                        'status': 'Above' if conversion_rate >= 2.5 else 'Below',
                        'column': f"{trans_col}/{sess_col}",
                        'insight': f"{'✅ Strong' if conversion_rate >= 3.0 else '⚠️ Room for improvement'} - Industry avg is 2.5-3%"
                    }
            
            # 2. Average Order Value (AOV) = Total Revenue / Total Transactions
            if revenue_cols and transaction_cols:
                rev_col = revenue_cols[0]
                trans_col = transaction_cols[0]
                total_revenue = df[rev_col].sum()
                total_transactions = df[trans_col].sum()
                if total_transactions > 0:
                    aov = total_revenue / total_transactions
                    # Smart benchmark: use currency detection
                    sample_revenue = df[rev_col].dropna().head(10).mean()
                    if sample_revenue > 1000:  # Likely VND
                        benchmark_aov = 150000  # 150K VND (~$6 USD)
                        currency = 'VND'
                    else:
                        benchmark_aov = 81.49  # $81.49 USD (Shopify global avg)
                        currency = 'USD'
                    
                    kpis['Average Order Value (AOV)'] = {
                        'value': float(aov),
                        'benchmark': benchmark_aov,
                        'status': 'Above' if aov >= benchmark_aov else 'Below',
                        'column': f"{rev_col}/{trans_col}",
                        'insight': f"{'✅' if aov >= benchmark_aov else '⚠️'} Benchmark: {benchmark_aov:,.0f} {currency}"
                    }
            
            # 3. Cart Abandonment Rate = (Add-to-Carts - Checkouts) / Add-to-Carts × 100
            if cart_cols and checkout_cols:
                cart_col = [col for col in cart_cols if 'add' in col.lower() or 'cart' in col.lower()][0]
                checkout_col = checkout_cols[0]
                total_carts = df[cart_col].sum()
                total_checkouts = df[checkout_col].sum()
                if total_carts > 0:
                    abandonment_rate = ((total_carts - total_checkouts) / total_carts) * 100
                    kpis['Cart Abandonment Rate (%)'] = {
                        'value': float(abandonment_rate),
                        'benchmark': 69.82,  # Industry avg
                        'status': 'Below' if abandonment_rate <= 69.82 else 'Above',  # Lower is better!
                        'column': f"({cart_col}-{checkout_col})/{cart_col}",
                        'insight': f"{'✅ Better than' if abandonment_rate < 69.82 else '⚠️ Worse than'} 69.82% industry avg"
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
                kpis['Mobile Traffic (%)'] = {
                    'value': float(avg_mobile),
                    'benchmark': 60.0,  # Mobile-first threshold
                    'status': 'Above' if avg_mobile >= 60.0 else 'Below',
                    'column': mobile_col,
                    'insight': f"{'📱 Mobile-first' if avg_mobile >= 60 else '💻 Desktop-focused'} - optimize accordingly"
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
        domain = domain_info.get('domain_name', 'general').lower()
        
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
        elif 'sales' in domain and (rep_cols or stage_cols):
            # Sales analysis will be implemented in next task
            pass
        
        return analysis
    
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
        
        # Insight 5: Conversion rate gaps (below 2.5% benchmark)
        low_cr_channels = [c for c in channel_breakdown if c['conversion_rate'] < 2.5]
        if low_cr_channels:
            channel_names = ', '.join([f"{c['channel']} ({c['conversion_rate']:.2f}%)" for c in low_cr_channels[:3]])
            insights.append({
                'type': 'low_conversion',
                'message': f"⚠️ {len(low_cr_channels)} channels below 2.5% CR benchmark: {channel_names}",
                'action': "Review landing pages, targeting, and messaging for these channels"
            })
        
        return insights[:5]  # Top 5 insights only
    
    def _generate_campaign_insights(self, campaign_breakdown: list) -> list:
        """Generate actionable insights from campaign breakdown"""
        insights = []
        
        if not campaign_breakdown:
            return insights
        
        # Find profitable vs unprofitable campaigns
        profitable = [c for c in campaign_breakdown if c['roas'] >= 1.0]
        unprofitable = [c for c in campaign_breakdown if c['roas'] < 1.0]
        
        best = campaign_breakdown[0]
        worst = campaign_breakdown[-1]
        
        # Insight 1: Best campaign
        insights.append({
            'type': 'best_performer',
            'message': f"🏆 {best['campaign']} is your top campaign with {best['roas']:.2f}x ROAS (${best['revenue']:,.0f} revenue)",
            'action': f"Scale budget for {best['campaign']} - it's profitable"
        })
        
        # Insight 2: Unprofitable campaigns
        if unprofitable:
            total_waste = sum(c['spend'] - c['revenue'] for c in unprofitable)
            campaign_names = ', '.join([c['campaign'] for c in unprofitable[:3]])
            insights.append({
                'type': 'money_wasted',
                'message': f"🚨 {len(unprofitable)} campaigns losing money (ROAS < 1.0): {campaign_names}",
                'action': f"PAUSE these campaigns immediately - wasting ${total_waste:,.0f}"
            })
        
        # Insight 3: Budget reallocation opportunity
        if profitable and unprofitable:
            reallocation_amount = sum(c['spend'] for c in unprofitable)
            potential_revenue = reallocation_amount * best['roas']
            insights.append({
                'type': 'reallocation',
                'message': f"💡 Shift ${reallocation_amount:,.0f} from unprofitable campaigns to {best['campaign']}",
                'action': f"Potential revenue increase: ${potential_revenue:,.0f} ({best['roas']:.2f}x ROAS)"
            })
        
        return insights
    
    @rate_limit_handler(max_retries=3, backoff_base=2)
    @log_performance("Smart Blueprint")
    def step2_smart_blueprint(self, df: pd.DataFrame, domain_info: Dict) -> Dict:
        """
        Step 2: Smart Blueprint - Combined EDA + Blueprint (15s)
        Single AI call instead of 2 separate calls
        
        ⭐ CRITICAL CHANGE: Now calculates KPIs from REAL DATA first,
        then passes to AI for INTERPRETATION only (not calculation)
        """
        
        domain_context = get_domain_specific_prompt_context(domain_info)
        
        # Get data statistics
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        all_cols = df.columns.tolist()
        
        # ⭐ NEW: Calculate KPIs from REAL DATA first
        kpis_calculated = self._calculate_real_kpis(df, domain_info)
        
        # DEBUG: Log real calculated values
        import logging
        logger = logging.getLogger(__name__)
        if 'Average Salary' in kpis_calculated:
            logger.info(f"🔍 STEP 2A - Real KPI calculated: ${kpis_calculated['Average Salary']['value']:,.2f}")
        
        # Combined prompt with STRICT chart requirements
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
{json.dumps(kpis_calculated, indent=2, ensure_ascii=False)}

REQUIREMENTS:
1. USE the above calculated KPIs (already computed from real data)
2. Design 8-10 charts based on OQMLB framework
3. Ensure 5 quality criteria ≥80% each
4. Include benchmark lines for KPIs

⚠️ CRITICAL CHART REQUIREMENTS (EVERY chart MUST have ALL of these):
- "x_axis": Must be a column name from the data (REQUIRED, cannot be null)
- "y_axis": Must be a column name from the data (REQUIRED, cannot be null)
- "type": One of ["bar", "line", "scatter", "pie"] (REQUIRED)
- "title": Clear Vietnamese title (REQUIRED)
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
    "title": "Doanh Thu Theo Kênh",
    "type": "bar",
    "x_axis": "{all_cols[0] if len(all_cols) > 0 else 'category'}",  // Actual column from data
    "y_axis": "{numeric_cols[0] if len(numeric_cols) > 0 else 'value'}",  // Actual numeric column
    "benchmark_line": 5000000,
    "question_answered": "Kênh nào có doanh thu cao nhất?"
}}

{{
    "id": "c2",
    "title": "Xu Hướng Theo Thời Gian",
    "type": "line",
    "x_axis": "date",  // Use actual date column if exists
    "y_axis": "{numeric_cols[1] if len(numeric_cols) > 1 else 'metric'}",
    "question_answered": "Xu hướng thay đổi như thế nào?"
}}

OUTPUT JSON (strictly follow this structure):
{{
    "kpis_calculated": {json.dumps(kpis_calculated, ensure_ascii=False)},
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
            
            # DEBUG: Check AI response before force replace
            ai_kpis = smart_blueprint.get('kpis_calculated', {})
            if 'Average Salary' in ai_kpis and 'Average Salary' in kpis_calculated:
                import logging
                logger = logging.getLogger(__name__)
                logger.info(f"🔍 DEBUG - AI returned: ${ai_kpis['Average Salary']['value']:,.2f}")
                logger.info(f"🔍 DEBUG - Real calculated: ${kpis_calculated['Average Salary']['value']:,.2f}")
            
            # ⭐ CRITICAL FIX: Force use real calculated KPIs (AI might modify them)
            # This ensures 100% accuracy - ignore whatever AI returns
            smart_blueprint['kpis_calculated'] = kpis_calculated
            
            # DEBUG: Verify after force replace
            if 'Average Salary' in smart_blueprint['kpis_calculated']:
                logger.info(f"🔍 DEBUG - After force replace: ${smart_blueprint['kpis_calculated']['Average Salary']['value']:,.2f}")
            
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
                    fig = px.bar(df_clean, x=x_axis, y=y_axis, title=chart_title)
                    
                    # Add benchmark line
                    if 'benchmark_line' in chart_spec:
                        fig.add_hline(
                            y=chart_spec['benchmark_line'],
                            line_dash="dash",
                            line_color="red",
                            annotation_text="Benchmark"
                        )
                
                elif chart_type == 'line' and x_axis and y_axis:
                    fig = px.line(df_clean, x=x_axis, y=y_axis, title=chart_title)
                
                elif chart_type == 'scatter' and x_axis and y_axis:
                    fig = px.scatter(df_clean, x=x_axis, y=y_axis, title=chart_title)
                
                elif chart_type == 'pie' and x_axis and y_axis:
                    fig = px.pie(df_clean, names=x_axis, values=y_axis, title=chart_title)
                
                if fig:
                    fig.update_layout(
                        font=dict(size=12),
                        title_font_size=16,
                        showlegend=True
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
                if is_streamlit_context():
                    st.warning(f"⚠️ Không tạo được chart '{chart_spec.get('title', 'Unknown')}': {str(e)}")
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
        
        domain_context = get_domain_specific_prompt_context(domain_info)
        
        # Get KPIs summary
        kpis_summary = []
        for kpi_name, kpi_data in smart_blueprint.get('kpis_calculated', {}).items():
            value = kpi_data.get('value', 'N/A')
            benchmark = kpi_data.get('benchmark', 'N/A')
            status = kpi_data.get('status', 'Unknown')
            kpis_summary.append(f"- {kpi_name}: {value} (Benchmark: {benchmark}, Status: {status})")
        
        kpis_text = chr(10).join(kpis_summary[:5]) if kpis_summary else "No KPIs calculated"
        
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

OUTPUT JSON:
{{
    "executive_summary": "Performance overview in 2-3 sentences",
    "key_insights": [
        {{
            "title": "Insight title",
            "description": "Brief insight with numbers",
            "impact": "high/medium/low"
        }}
    ],
    "recommendations": [
        {{
            "action": "Specific action",
            "priority": "high/medium/low",
            "expected_impact": "Quantified benefit",
            "timeline": "immediate/short/long"
        }}
    ],
    "risk_alerts": [
        {{"risk": "Risk description", "severity": "high/medium/low"}}
    ]
}}
"""
        
        success, result = self._generate_ai_insight(prompt, temperature=0.5, max_tokens=3000)
        
        if not success:
            return {'success': False, 'error': result, 'insights': {}}
        
        try:
            insights = json.loads(result)
            
            # Display insights (compact)
            self._display_compact_insights(insights, domain_info)
            
            return {
                'success': True,
                'insights': insights
            }
        
        except json.JSONDecodeError as e:
            return {'success': False, 'error': f"❌ Lỗi tạo insights: {str(e)}", 'insights': {}}
    
    # Helper methods
    
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
            
            response = self.client.generate_content(
                json_prompt,
                generation_config=genai.GenerationConfig(
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
    
    def _apply_fast_cleaning(self, df: pd.DataFrame, cleaning_plan: Dict) -> pd.DataFrame:
        """
        Fast data cleaning execution
        
        ⭐ CRITICAL: Only handle ACTUAL missing values to preserve data accuracy.
        Do NOT modify non-null values - this changes statistics (mean, median, etc.)
        """
        df_clean = df.copy()
        
        # Handle missing values - ONLY if they actually exist
        missing_handled = cleaning_plan.get('cleaning_summary', {}).get('missing_handled', {})
        for col, method in missing_handled.items():
            if col not in df_clean.columns:
                continue
            
            # ⭐ CRITICAL CHECK: Only proceed if column has actual missing values
            if df_clean[col].isnull().sum() == 0:
                continue  # Skip - no missing values to handle
            
            if method == 'median' and df_clean[col].dtype in ['int64', 'float64']:
                # Use proper pandas method (not inplace to avoid warnings)
                df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            elif method == 'mode':
                if len(df_clean[col].mode()) > 0:
                    df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
        
        # Remove duplicates
        df_clean = df_clean.drop_duplicates()
        
        return df_clean
    
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
                if is_streamlit_context():
                    st.warning(f"⚠️ Bỏ qua biểu đồ thiếu thông tin: {chart.get('title', 'Unknown')} (thiếu: {', '.join(missing_fields)})")
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
            if is_streamlit_context():
                st.error(f"❌ Chỉ có {len(valid_charts)} biểu đồ hợp lệ, cần tối thiểu 3 biểu đồ")
            
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
        with st.expander("📋 Báo Cáo Làm Sạch Dữ Liệu", expanded=False):
            summary = cleaning_plan.get('cleaning_summary', {})
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Số dòng", f"{summary.get('rows_after', 0):,}", 
                         delta=f"{summary.get('rows_after', 0) - summary.get('rows_before', 0)}")
            with col2:
                st.metric("Duplicates đã xóa", summary.get('duplicates_removed', 0))
            with col3:
                st.metric("✅ Quality Score", f"{validation['score']:.0f}%", 
                         delta="ISO 8000" if validation['passed'] else "Failed")
    
    def _display_compact_blueprint(self, smart_blueprint: Dict, domain_info: Dict):
        """Display compact blueprint"""
        with st.expander("🎨 Dashboard Blueprint", expanded=False):
            st.caption(f"**Domain**: {domain_info['domain_name']} | **Expert**: {domain_info['expert_role'][:40]}...")
            
            # KPIs
            kpis = smart_blueprint.get('kpis_calculated', {})
            if kpis:
                st.markdown("**📊 Key KPIs:**")
                cols = st.columns(min(3, len(kpis)))
                for i, (kpi_name, kpi_data) in enumerate(list(kpis.items())[:6]):
                    with cols[i % 3]:
                        # ✅ Issue #3 Fix: Handle None or non-numeric KPI values
                        kpi_value = kpi_data.get('value')
                        if isinstance(kpi_value, (int, float)):
                            value_str = f"{kpi_value:.1f}"
                        elif kpi_value is not None:
                            value_str = str(kpi_value)
                        else:
                            value_str = "N/A"
                        
                        st.metric(kpi_name, value_str, delta=kpi_data.get('status', ''))
    
    def _display_compact_insights(self, insights: Dict, domain_info: Dict):
        """Display compact insights"""
        with st.expander("💡 Insights Chuyên Gia", expanded=True):
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
