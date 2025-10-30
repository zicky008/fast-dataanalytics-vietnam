"""
DataAnalytics Vietnam - Streamlit App
Premium Lean Pipeline với UI chuyên nghiệp
Target: 55 seconds với 5-star UX
"""

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import sys

# Add parent directory to path to access src modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

# Import pipeline (from same directory)
from premium_lean_pipeline import PremiumLeanPipeline
from utils.validators import safe_file_upload

# Page config
st.set_page_config(
    page_title="DataAnalytics Vietnam - Bricks.ai cho SMEs Việt Nam",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
    }
    .main-header p {
        color: #f0f0f0;
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    .upload-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📊 DataAnalytics Vietnam</h1>
    <p>Bricks.ai cho SMEs Việt Nam - Phân tích dữ liệu tự động bằng AI</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Cài đặt")
    
    # API Key check
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        st.success("✅ API Key đã cấu hình")
    else:
        st.error("❌ Thiếu GEMINI_API_KEY")
        st.info("Thêm API key vào Streamlit Cloud secrets")
    
    st.markdown("---")
    
    # Info
    st.markdown("""
    ### 🚀 Premium Lean Pipeline
    
    **Tính năng:**
    - ✅ Domain Detection (6 ngành)
    - ✅ ISO 8000 Data Cleaning
    - ✅ Smart Blueprint (8-9 charts)
    - ✅ Expert Insights (CMO/CFO/COO)
    
    **Performance:**
    - ⚡ 13-23 giây (target: 55s)
    - 🎯 Quality: 100/100
    - 📊 8-9 biểu đồ chuyên nghiệp
    
    **Pricing:**
    - 🆓 FREE: 60 AI messages/tháng
    - 💎 PRO: 199k VND/tháng
    """)
    
    st.markdown("---")
    st.caption("v1.0.0 | © 2024 DataAnalytics Vietnam")

# Main content
tab1, tab2, tab3 = st.tabs(["📤 Upload & Analyze", "📊 Dashboard", "💡 Insights"])

with tab1:
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    
    # File upload
    st.subheader("📂 Tải lên dữ liệu của bạn")
    
    uploaded_file = st.file_uploader(
        "Chọn file CSV hoặc Excel",
        type=["csv", "xlsx", "xls"],
        help="Upload file dữ liệu của bạn (Marketing, E-commerce, Sales, etc.)"
    )
    
    # Dataset description
    dataset_description = st.text_area(
        "Mô tả dataset (optional)",
        placeholder="VD: Google Ads campaign data - January 2024",
        help="Mô tả giúp AI hiểu rõ hơn về dữ liệu của bạn"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process button
    if uploaded_file:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            analyze_btn = st.button(
                "🚀 Phân Tích Dữ Liệu",
                use_container_width=True,
                type="primary"
            )
        
        if analyze_btn:
            if not api_key:
                st.error("❌ Thiếu GEMINI_API_KEY. Vui lòng cấu hình trong Streamlit Cloud secrets.")
                st.stop()
            
            try:
                # Import and configure Gemini
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                client = genai.GenerativeModel('gemini-2.0-flash')
                
                # Load data
                with st.spinner("📥 Đang đọc dữ liệu..."):
                    success, df, message = safe_file_upload(uploaded_file)
                    
                    if not success:
                        st.error(message)
                        st.stop()
                    
                    st.success(f"✅ Đọc thành công: {df.shape[0]:,} dòng × {df.shape[1]} cột")
                
                # Run pipeline
                pipeline = PremiumLeanPipeline(client)
                
                result = pipeline.run_pipeline(
                    df=df,
                    dataset_description=dataset_description
                )
                
                # Check result
                if not result.get('success'):
                    st.error(f"❌ Pipeline thất bại: {result.get('error', 'Unknown error')}")
                    st.stop()
                
                # Store in session state
                st.session_state['pipeline_result'] = result
                st.session_state['df'] = df
                
                # Success message with details
                total_time = result.get('performance', {}).get('total', 0)
                quality_score = result.get('quality_scores', {}).get('overall', 0)
                kpis_count = len(result.get('dashboard', {}).get('kpis', {}))
                charts_count = len(result.get('dashboard', {}).get('charts', []))
                
                st.success(f"✅ Hoàn thành! Pipeline chạy trong {total_time:.1f} giây")
                
                # Show quick summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Quality Score", f"{quality_score:.0f}/100")
                with col2:
                    st.metric("KPIs", kpis_count)
                with col3:
                    st.metric("Charts", charts_count)
                
                # Switch to dashboard tab
                st.info("👉 Chuyển sang tab **Dashboard** để xem chi tiết")
                
            except Exception as e:
                st.error(f"❌ Lỗi: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

with tab2:
    st.subheader("📊 Dashboard")
    
    if 'pipeline_result' not in st.session_state:
        st.info("👈 Upload dữ liệu ở tab **Upload & Analyze** để bắt đầu")
    else:
        result = st.session_state['pipeline_result']
        
        # Domain Info
        domain_info = result.get('domain_info', {})
        st.markdown(f"### 🎯 Domain: {domain_info.get('domain_name', 'Unknown')}")
        st.caption(f"**Expert**: {domain_info.get('expert_role', 'N/A')[:80]}...")
        
        st.markdown("---")
        
        # KPIs
        dashboard = result.get('dashboard', {})
        kpis = dashboard.get('kpis', {})
        
        if kpis:
            st.markdown("### 📊 Key Performance Indicators")

            cols = st.columns(min(3, len(kpis)))
            for i, (kpi_name, kpi_data) in enumerate(list(kpis.items())[:6]):
                with cols[i % 3]:
                    value = kpi_data.get('value', 'N/A')
                    if isinstance(value, (int, float)):
                        value_str = f"{value:.1f}"
                    else:
                        value_str = str(value)

                    status = kpi_data.get('status', '')
                    st.metric(kpi_name, value_str, delta=status)

                    # Show Vietnam benchmark comparison if available
                    vietnam_context = kpi_data.get('vietnam_context', '')
                    if vietnam_context:
                        st.caption(f"🇻🇳 {vietnam_context}")

                    # Show benchmark source
                    benchmark_source = kpi_data.get('benchmark_source', '')
                    if benchmark_source:
                        st.caption(f"📊 {benchmark_source}")

                    # Show percentile if available
                    percentile = kpi_data.get('percentile', None)
                    if percentile is not None:
                        st.caption(f"📈 Percentile: {percentile:.0f}th")
        else:
            st.warning(f"⚠️ Không có KPIs. Dashboard keys: {list(dashboard.keys())}")
            
            # Debug expander
            with st.expander("🔍 Debug Info (Click to expand)"):
                st.json(dashboard)
        
        st.markdown("---")
        
        # Charts
        charts = dashboard.get('charts', [])
        if charts:
            st.markdown(f"### 📈 Biểu đồ ({len(charts)} charts)")
            
            # Display charts in 2 columns
            for i in range(0, len(charts), 2):
                col1, col2 = st.columns(2)
                
                with col1:
                    if i < len(charts):
                        chart = charts[i]
                        st.plotly_chart(
                            chart['figure'],
                            use_container_width=True,
                            key=f"chart_{i}"
                        )
                
                with col2:
                    if i + 1 < len(charts):
                        chart = charts[i + 1]
                        st.plotly_chart(
                            chart['figure'],
                            use_container_width=True,
                            key=f"chart_{i+1}"
                        )
        
        # Quality Score
        st.markdown("---")
        quality_scores = result.get('quality_scores', {})
        if quality_scores:
            st.markdown("### 🎯 Chất lượng phân tích")
            cols = st.columns(3)
            
            with cols[0]:
                cleaning_score = quality_scores.get('cleaning', 0)
                st.metric("Data Cleaning", f"{cleaning_score:.0f}/100")
            
            with cols[1]:
                blueprint_score = quality_scores.get('blueprint', 0)
                st.metric("Blueprint Quality", f"{blueprint_score:.0f}/100")
            
            with cols[2]:
                overall_score = quality_scores.get('overall', 0)
                st.metric("Overall Score", f"{overall_score:.0f}/100")

with tab3:
    st.subheader("💡 Expert Insights")
    
    if 'pipeline_result' not in st.session_state:
        st.info("👈 Upload dữ liệu ở tab **Upload & Analyze** để bắt đầu")
    else:
        result = st.session_state['pipeline_result']
        insights = result.get('insights', {})
        domain_info = result.get('domain_info', {})
        
        # Expert context
        st.markdown(f"**Chuyên gia**: {domain_info.get('expert_role', 'N/A')[:80]}...")
        
        st.markdown("---")
        
        # Executive Summary
        summary = insights.get('executive_summary', 'No summary available')
        st.info(f"**📋 Tóm tắt điều hành:**\n\n{summary}")
        
        st.markdown("---")
        
        # Key Insights
        key_insights = insights.get('key_insights', [])
        if key_insights:
            st.markdown("### 🔍 Insights chính")
            for idx, insight in enumerate(key_insights, 1):
                impact = insight.get('impact', 'medium')
                emoji = "🔴" if impact == 'high' else "🟡" if impact == 'medium' else "🟢"
                
                st.markdown(f"{emoji} **{insight.get('title', 'Insight')}**")
                st.write(insight.get('description', ''))
                st.caption(f"Impact: {impact}")
                st.markdown("---")
        
        # Recommendations
        recommendations = insights.get('recommendations', [])
        if recommendations:
            st.markdown("### 🚀 Khuyến nghị hành động")
            for idx, rec in enumerate(recommendations, 1):
                priority = rec.get('priority', 'medium')
                emoji = "🔴" if priority == 'high' else "🟡" if priority == 'medium' else "🟢"
                
                with st.expander(f"{emoji} {rec.get('action', 'Action')}"):
                    st.write(f"**Expected Impact:** {rec.get('expected_impact', 'N/A')}")
                    st.write(f"**Timeline:** {rec.get('timeline', 'N/A')}")
                    st.write(f"**Priority:** {priority}")
        
        # Risk Alerts
        risk_alerts = insights.get('risk_alerts', [])
        if risk_alerts:
            st.markdown("---")
            st.markdown("### ⚠️ Cảnh báo rủi ro")
            for risk in risk_alerts:
                severity = risk.get('severity', 'medium')
                if severity == 'high':
                    st.error(f"🔴 {risk.get('risk', 'Risk')}")
                elif severity == 'medium':
                    st.warning(f"🟡 {risk.get('risk', 'Risk')}")
                else:
                    st.info(f"🟢 {risk.get('risk', 'Risk')}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Made with ❤️ for Vietnamese SMEs | 
    <a href='https://github.com/YOUR_USERNAME/dataanalytics-vietnam' target='_blank'>GitHub</a> | 
    v1.0.0</p>
</div>
""", unsafe_allow_html=True)
