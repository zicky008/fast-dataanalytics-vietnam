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
    
    @rate_limit_handler(max_retries=3, backoff_base=2)
    @log_performance("Smart Blueprint")
    def step2_smart_blueprint(self, df: pd.DataFrame, domain_info: Dict) -> Dict:
        """
        Step 2: Smart Blueprint - Combined EDA + Blueprint (15s)
        Single AI call instead of 2 separate calls
        """
        
        domain_context = get_domain_specific_prompt_context(domain_info)
        
        # Get data statistics
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        all_cols = df.columns.tolist()
        
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

REQUIREMENTS:
1. Calculate domain KPIs (ROAS, CTR, AOV, etc.) with numeric values
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
    "kpis_calculated": {{
        "ROAS": {{"value": 5.2, "benchmark": "4:1", "status": "Above"}},
        "CTR": {{"value": 2.8, "benchmark": "3.17%", "status": "Below"}}
    }},
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

REMEMBER: Every chart MUST have x_axis and y_axis as actual column names from the data!
"""
        
        success, result = self._generate_ai_insight(prompt, temperature=0.3, max_tokens=6000)
        
        if not success:
            return {'success': False, 'error': result}
        
        try:
            smart_blueprint = json.loads(result)
            
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
                
                if chart_type == 'bar' and x_axis and y_axis:
                    fig = px.bar(df, x=x_axis, y=y_axis, title=chart_title)
                    
                    # Add benchmark line
                    if 'benchmark_line' in chart_spec:
                        fig.add_hline(
                            y=chart_spec['benchmark_line'],
                            line_dash="dash",
                            line_color="red",
                            annotation_text="Benchmark"
                        )
                
                elif chart_type == 'line' and x_axis and y_axis:
                    fig = px.line(df, x=x_axis, y=y_axis, title=chart_title)
                
                elif chart_type == 'scatter' and x_axis and y_axis:
                    fig = px.scatter(df, x=x_axis, y=y_axis, title=chart_title)
                
                elif chart_type == 'pie' and x_axis and y_axis:
                    fig = px.pie(df, names=x_axis, values=y_axis, title=chart_title)
                
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
        """Fast data cleaning execution"""
        df_clean = df.copy()
        
        # Handle missing values
        missing_handled = cleaning_plan.get('cleaning_summary', {}).get('missing_handled', {})
        for col, method in missing_handled.items():
            if col in df_clean.columns:
                if method == 'median' and df_clean[col].dtype in ['int64', 'float64']:
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)
                elif method == 'mode':
                    if len(df_clean[col].mode()) > 0:
                        df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
        
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
