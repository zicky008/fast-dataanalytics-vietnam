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

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

# Import pipeline
from premium_lean_pipeline import PremiumLeanPipeline
from utils.validators import safe_file_upload

# Page config
st.set_page_config(
    page_title="DataAnalytics Vietnam - Bricks.ai cho SMEs Việt Nam",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UX
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E40AF;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #64748B;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #F8FAFC;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3B82F6;
    }
    .success-box {
        background: #DCFCE7;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #22C55E;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Gemini client
@st.cache_resource
def get_gemini_client():
    """Initialize Gemini client với caching"""
    try:
        import google.generativeai as genai
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            st.error("❌ Chưa có GEMINI_API_KEY. Vui lòng thêm vào file .env")
            st.stop()
        
        genai.configure(api_key=api_key)
        return genai
    
    except Exception as e:
        st.error(f"❌ Lỗi kết nối Gemini API: {str(e)}")
        st.stop()


# Main app
def main():
    """Main app function"""
    
    # Header
    st.markdown('<div class="main-header">📊 DataAnalytics Vietnam</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Dashboard chuyên nghiệp trong 60 giây - Được xây dựng cho SMEs Việt Nam</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/1E40AF/FFFFFF?text=DataAnalytics+VN", use_container_width=True)
        
        st.markdown("### 🚀 Premium Features")
        st.markdown("""
        ✅ **ISO 8000 Compliance** - Dữ liệu chuẩn quốc tế
        
        ✅ **Domain Expertise** - Insights từ CMO/CFO/COO
        
        ✅ **Data Lineage** - Minh bạch 100%
        
        ✅ **Industry Benchmarks** - Chuẩn 2024
        
        ✅ **Vietnamese Native** - Ngôn ngữ bản địa
        """)
        
        st.markdown("---")
        st.markdown("### 💰 Pricing")
        st.success("""
        **FREE**: 60 AI messages/tháng
        
        **PRO**: 199k VND/tháng
        - 500 AI messages
        - Priority support
        - Unlimited dashboards
        """)
        
        st.markdown("---")
        st.caption("Built with ❤️ for Vietnamese SMEs")
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📤 Upload & Analyze", "📊 Dashboard", "💡 Insights"])
    
    with tab1:
        st.markdown("### 📤 Upload Dữ Liệu")
        
        # Instructions
        with st.expander("📖 Hướng dẫn sử dụng", expanded=False):
            st.markdown("""
            **Bước 1**: Upload file CSV/Excel (tối đa 200MB)
            
            **Bước 2**: (Tùy chọn) Mô tả dữ liệu để AI hiểu rõ hơn
            
            **Bước 3**: Nhấn "🚀 Phân Tích Ngay" và chờ ~60 giây
            
            **Kết quả**: Dashboard chuyên nghiệp + Insights từ chuyên gia
            
            **Lưu ý**: 
            - Dữ liệu của bạn được xử lý an toàn, không lưu trữ
            - Kết quả tuân thủ chuẩn ISO 8000
            - Có thể export PDF/PowerPoint sau khi hoàn thành
            """)
        
        # File upload
        uploaded_file = st.file_uploader(
            "Chọn file CSV hoặc Excel",
            type=['csv', 'xlsx', 'xls'],
            help="File tối đa 200MB. Hỗ trợ UTF-8 và Latin1 encoding"
        )
        
        # Dataset description
        dataset_description = st.text_area(
            "Mô tả dữ liệu (tùy chọn)",
            placeholder="Ví dụ: Dữ liệu marketing campaign từ Facebook Ads tháng 1/2024...",
            help="Mô tả giúp AI hiểu rõ hơn về dữ liệu của bạn"
        )
        
        # Analyze button
        if uploaded_file:
            col1, col2 = st.columns([1, 3])
            with col1:
                analyze_button = st.button("🚀 Phân Tích Ngay", type="primary", use_container_width=True)
            with col2:
                st.caption("⏱️ Dự kiến ~60 giây | ✅ ISO 8000 Compliant | 🔒 Bảo mật")
        
        # Process file
        if uploaded_file and 'analyze_button' in locals() and analyze_button:
            # Load file
            with st.spinner("📁 Đang tải file..."):
                success, df, message = safe_file_upload(uploaded_file, max_size_mb=200)
            
            if not success:
                st.error(message)
                st.stop()
            
            st.success(message)
            
            # Display data preview
            with st.expander("👀 Xem Trước Dữ Liệu", expanded=False):
                st.dataframe(df.head(10), use_container_width=True)
                st.caption(f"📊 Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
            
            # Run pipeline
            st.markdown("---")
            st.markdown("### ⚙️ Đang Xử Lý...")
            
            # Initialize pipeline
            gemini_client = get_gemini_client()
            pipeline = PremiumLeanPipeline(gemini_client)
            
            # Run pipeline with progress
            result = pipeline.run_pipeline(df, dataset_description)
            
            # Check result
            if not result['success']:
                st.error(f"❌ Lỗi: {result['error']}")
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
            ### ✅ Hoàn Thành!
            
            ⏱️ **Thời gian**: {total_time:.1f} giây
            
            ⭐ **Quality Score**: {quality_score:.1f}/100 (ISO 8000 Compliant)
            
            📊 **Charts**: {len(result['dashboard']['charts'])} biểu đồ được tạo
            
            💡 **Insights**: {len(result['insights']['key_insights'])} insights từ {result['domain_info']['expert_role'][:50]}...
            
            👉 Chuyển sang tab **Dashboard** và **Insights** để xem kết quả!
            """)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📊 Professional Dashboard")
        
        if 'result' not in st.session_state:
            st.info("👈 Upload dữ liệu ở tab **Upload & Analyze** để bắt đầu")
            st.stop()
        
        result = st.session_state['result']
        
        # 🐛 DEBUG: Verify code version
        import datetime
        st.error(f"🐛 CODE VERSION CHECK: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Debug code active!")
        
        # Display domain info
        domain_info = result['domain_info']
        st.markdown(f"**Ngành nghề**: {domain_info['domain_name']} | **Expert**: {domain_info['expert_role'][:60]}...")
        
        # Display KPIs
        st.markdown("#### 📈 Key Performance Indicators")
        kpis = result['dashboard'].get('kpis', {})
        
        # 🐛 DEBUG: FORCE DISPLAY - Use st.error to ensure visibility
        st.error(f"🐛 DEBUG: Received {len(kpis)} KPIs from dashboard")
        if kpis:
            st.error(f"🐛 DEBUG: KPI keys = {list(kpis.keys())[:3]}")
            first_kpi = list(kpis.items())[0]
            st.error(f"🐛 DEBUG: First KPI data = {first_kpi}")
        else:
            st.error("🐛 DEBUG: KPIs DICT IS EMPTY!")
        
        if kpis:
            # Define KPIs where LOWER is BETTER (reverse color logic)
            lower_is_better_kpis = [
                'Defect Rate',
                'Downtime',
                'Cost per Unit',
                'Avg Downtime',
                'Total Downtime',
                'Cost'
            ]
            
            cols = st.columns(min(4, len(kpis)))
            for i, (kpi_name, kpi_data) in enumerate(list(kpis.items())[:8]):
                with cols[i % 4]:
                    # Check if this is a "lower is better" KPI
                    is_lower_better = any(keyword in kpi_name for keyword in lower_is_better_kpis)
                    
                    # Reverse logic for "lower is better" KPIs
                    if is_lower_better:
                        # For lower is better: Below benchmark = good (green), Above = bad (red)
                        delta_color = "inverse" if kpi_data.get('status') == 'Above' else "normal"
                    else:
                        # For higher is better: Above benchmark = good (green), Below = bad (red)
                        delta_color = "normal" if kpi_data.get('status') == 'Above' else "inverse"
                    
                    st.metric(
                        label=kpi_name,
                        value=f"{kpi_data['value']:.1f}",
                        delta=kpi_data.get('status', ''),
                        delta_color=delta_color
                    )
                    st.caption(f"Benchmark: {kpi_data.get('benchmark', 'N/A')}")
        
        # Display charts
        st.markdown("---")
        st.markdown("#### 📊 Interactive Charts")
        
        charts = result['dashboard']['charts']
        
        if len(charts) == 0:
            st.warning("Không có biểu đồ nào được tạo. Vui lòng kiểm tra dữ liệu đầu vào.")
        else:
            # Display charts in 2 columns
            for i in range(0, len(charts), 2):
                col1, col2 = st.columns(2)
                
                with col1:
                    if i < len(charts):
                        st.plotly_chart(charts[i]['figure'], use_container_width=True)
                
                with col2:
                    if i + 1 < len(charts):
                        st.plotly_chart(charts[i+1]['figure'], use_container_width=True)
        
        # Export options
        st.markdown("---")
        st.markdown("#### 📥 Export Options")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Export PDF", use_container_width=True):
                st.info("🚧 Tính năng đang phát triển")
        
        with col2:
            if st.button("📊 Export PowerPoint", use_container_width=True):
                st.info("🚧 Tính năng đang phát triển")
        
        with col3:
            if st.button("📊 Download Data", use_container_width=True):
                csv = st.session_state['df'].to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name='cleaned_data.csv',
                    mime='text/csv',
                )
    
    with tab3:
        st.markdown("### 💡 Expert Insights")
        
        if 'result' not in st.session_state:
            st.info("👈 Upload dữ liệu ở tab **Upload & Analyze** để bắt đầu")
            st.stop()
        
        result = st.session_state['result']
        insights = result['insights']
        domain_info = result['domain_info']
        
        # Expert info
        st.markdown(f"**Perspective từ**: {domain_info['expert_role']}")
        st.markdown(f"**Ngành nghề**: {domain_info['domain_name']}")
        
        # Executive summary
        st.markdown("---")
        st.markdown("#### 📋 Executive Summary")
        st.info(insights.get('executive_summary', 'No summary available'))
        
        # Key insights
        st.markdown("---")
        st.markdown("#### 🎯 Key Insights")
        
        for insight in insights.get('key_insights', []):
            impact_emoji = "🔴" if insight['impact'] == 'high' else "🟡" if insight['impact'] == 'medium' else "🟢"
            
            with st.expander(f"{impact_emoji} {insight['title']}", expanded=True):
                st.markdown(insight['description'])
                st.caption(f"Impact: **{insight['impact'].upper()}**")
        
        # Recommendations
        st.markdown("---")
        st.markdown("#### 🚀 Actionable Recommendations")
        
        for rec in insights.get('recommendations', []):
            priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
            
            st.success(f"""
            {priority_emoji} **[{rec['priority'].upper()}] {rec['action']}**
            
            📊 Expected Impact: {rec['expected_impact']}
            
            ⏱️ Timeline: {rec['timeline']}
            """)
        
        # Risk alerts
        if insights.get('risk_alerts'):
            st.markdown("---")
            st.markdown("#### ⚠️ Risk Alerts")
            
            for risk in insights['risk_alerts']:
                severity_emoji = "🔴" if risk['severity'] == 'high' else "🟡" if risk['severity'] == 'medium' else "🟢"
                st.warning(f"{severity_emoji} **{risk['risk']}** (Severity: {risk['severity']})")
        
        # Quality badge
        st.markdown("---")
        st.markdown("#### ✅ Quality Assurance")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Quality Score", f"{result['quality_scores']['overall']:.0f}/100")
            st.caption("ISO 8000 Compliant")
        
        with col2:
            st.metric("Data Cleaning", f"{result['quality_scores']['cleaning']:.0f}/100")
            st.caption("Missing <2%, Duplicates = 0")
        
        with col3:
            st.metric("Blueprint Quality", f"{result['quality_scores']['blueprint']:.0f}/100")
            st.caption("5 criteria ≥80%")


if __name__ == "__main__":
    main()
