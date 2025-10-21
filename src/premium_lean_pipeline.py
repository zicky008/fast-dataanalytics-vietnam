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
from typing import Dict, List, Tuple, Any
import streamlit as st
from datetime import datetime
import time

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
            progress_placeholder = st.empty()
            progress_placeholder.info("🔍 **Bước 0/4**: Nhận diện ngành nghề...")
            
            domain_info = self.step0_domain_detection(df, dataset_description)
            self._add_audit_trail("Domain Detection", domain_info)
            self._update_performance("domain_detection", time.time() - start_time)
            
            # Step 1: Data Cleaning (15s - ISO 8000)
            step1_start = time.time()
            progress_placeholder.info(f"🧹 **Bước 1/4**: Làm sạch dữ liệu (ISO 8000)... Domain: {domain_info['domain_name']}")
            
            cleaning_result = self.step1_data_cleaning(df, domain_info)
            if not cleaning_result['success']:
                return self._error_response(cleaning_result['error'])
            
            self._add_audit_trail("Data Cleaning", cleaning_result)
            self._update_performance("data_cleaning", time.time() - step1_start)
            
            # Step 2: Smart Blueprint (15s - EDA + Blueprint combined)
            step2_start = time.time()
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
            progress_placeholder.info("🏗️ **Bước 3/4**: Xây dựng Dashboard (theo Blueprint)...")
            
            dashboard_result = self.step3_dashboard_build(
                cleaning_result['df_cleaned'],
                blueprint_result['smart_blueprint']
            )
            
            self._add_audit_trail("Dashboard Build", dashboard_result)
            self._update_performance("dashboard_build", time.time() - step3_start)
            
            # Step 4: Domain Insights (15s - expert perspective)
            step4_start = time.time()
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
        
        # Display to user
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
        
        # Combined prompt
        prompt = f"""
{domain_context}

TASK: Smart Dashboard Blueprint (Combined EDA + Design)

DATA PROFILE:
- Shape: {df.shape[0]:,} rows × {df.shape[1]} columns
- Numeric: {', '.join(numeric_cols[:10])}
- Sample: {df.head(3).to_dict('records')}

REQUIREMENTS:
1. Calculate domain KPIs (ROAS, CTR, AOV, etc.)
2. Design 8-10 charts based on OQMLB framework
3. Ensure 5 quality criteria ≥80% each
4. Include benchmark lines

OUTPUT JSON:
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
"""
        
        success, result = self._generate_ai_insight(prompt, temperature=0.3, max_tokens=6000)
        
        if not success:
            return {'success': False, 'error': result}
        
        try:
            smart_blueprint = json.loads(result)
            
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
        
        charts = []
        
        for chart_spec in smart_blueprint.get('charts', [])[:10]:  # Limit to 10 charts
            try:
                chart_id = chart_spec['id']
                chart_title = chart_spec['title']
                chart_type = chart_spec['type']
                x_axis = chart_spec.get('x_axis')
                y_axis = chart_spec.get('y_axis')
                
                # Validate columns exist
                if x_axis and x_axis not in df.columns:
                    continue
                if y_axis and y_axis not in df.columns:
                    continue
                
                # Create chart
                fig = None
                
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
            kpis_summary.append(f"- {kpi_name}: {kpi_data['value']} (Benchmark: {kpi_data['benchmark']}, Status: {kpi_data['status']})")
        
        prompt = f"""
{domain_context}

TASK: Expert Insights (Concise & Actionable)

KPIs:
{chr(10).join(kpis_summary[:5])}

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
        """Generate AI insight với error handling"""
        try:
            response = self.client.models.generate_content(
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
                        st.metric(kpi_name, f"{kpi_data['value']:.1f}", delta=kpi_data.get('status', ''))
    
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
