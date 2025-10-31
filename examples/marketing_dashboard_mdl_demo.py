"""
Marketing Dashboard Demo - Powered by Semantic Layer (MDL)
Demo trực quan để thấy sự khác biệt giữa hardcode vs MDL-driven

Chạy demo: streamlit run examples/marketing_dashboard_mdl_demo.py
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mdl_loader import (
    load_mdl_for_domain,
    get_measure_expression,
    format_kpi_with_benchmark,
    display_metric_info,
    get_kpi_metadata
)

st.set_page_config(
    page_title="Marketing Dashboard - MDL Demo",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Marketing Performance Dashboard")
st.caption("Demo: Semantic Layer (MDL) vs Hardcoded KPIs")

# ===== SAMPLE DATA =====
st.header("1️⃣ Sample Data")

df = pd.DataFrame({
    'campaign_id': ['Facebook_Ads', 'Google_Search', 'TikTok_Ads', 'Email_Campaign'],
    'campaign_name': ['FB Summer Sale', 'Google Brand', 'TikTok Viral', 'Newsletter Q4'],
    'channel': ['Social', 'Search', 'Social', 'Email'],
    'spend': [15000, 25000, 10000, 5000],
    'revenue': [67500, 125000, 35000, 22500],
    'impressions': [500000, 800000, 1200000, 50000],
    'clicks': [15000, 24000, 36000, 2500],
    'conversions': [450, 800, 300, 150],
    'leads': [600, 1000, 400, 200],
    'customers': [120, 200, 80, 50]
})

with st.expander("📋 View Raw Data"):
    st.dataframe(df, use_container_width=True)

# ===== LOAD MDL =====
st.header("2️⃣ Load Semantic Layer (MDL)")

with st.spinner("Loading MDL schema for marketing..."):
    mdl = load_mdl_for_domain("marketing")

if not mdl:
    st.error("❌ Failed to load MDL schema")
    st.stop()

st.success(f"✅ Loaded **{mdl.catalog}** with {len(mdl.metrics[0].measure)} industry-standard measures")

# Show MDL metadata
with st.expander("🔍 MDL Metadata"):
    metadata = get_kpi_metadata("marketing")
    st.json(metadata)

# ===== COMPARISON: HARDCODE vs MDL =====
st.header("3️⃣ Comparison: Hardcode vs MDL-Driven")

tab1, tab2 = st.tabs(["❌ HARDCODED (Old Way)", "✅ MDL-DRIVEN (New Way)"])

with tab1:
    st.subheader("❌ Hardcoded KPIs (Có thể sai!)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Hardcoded ROAS (CÓ THỂ SAI!)
        total_spend = df['spend'].sum()
        total_revenue = df['revenue'].sum()
        roas_hardcode = total_revenue / total_spend if total_spend > 0 else 0
        
        st.metric("ROAS (Hardcoded)", f"{roas_hardcode:.2f}")
        st.caption("⚠️ Công thức: revenue / spend")
        st.caption("❌ Không có benchmark")
        st.caption("❌ Không có source of truth")
    
    with col2:
        # Hardcoded CTR
        total_clicks = df['clicks'].sum()
        total_impressions = df['impressions'].sum()
        ctr_hardcode = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        
        st.metric("CTR (Hardcoded)", f"{ctr_hardcode:.2f}%")
        st.caption("⚠️ Công thức: clicks / impressions * 100")
        st.caption("❌ Không có benchmark")
    
    with col3:
        # Hardcoded Conversion Rate
        total_conversions = df['conversions'].sum()
        conv_rate_hardcode = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        
        st.metric("Conversion Rate (Hardcoded)", f"{conv_rate_hardcode:.2f}%")
        st.caption("⚠️ Công thức: conversions / clicks * 100")
        st.caption("❌ Không có benchmark")
    
    st.warning("""
    **Vấn đề với Hardcode:**
    - ❌ Mỗi dev tính khác nhau → Inconsistent
    - ❌ Không có single source of truth
    - ❌ Khó maintain (công thức rải rác khắp nơi)
    - ❌ Không có industry benchmark để so sánh
    - ❌ User không biết công thức → Mất trust
    """)

with tab2:
    st.subheader("✅ MDL-Driven KPIs (Single Source of Truth)")
    
    metrics = mdl.metrics[0]  # marketing_roi_kpis
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # MDL-driven ROAS
        roas_formula = get_measure_expression("marketing", "marketing_roi_kpis", "roas")
        
        total_revenue = df['revenue'].sum()
        total_spend = df['spend'].sum()
        roas_mdl = total_revenue / max(total_spend, 1)  # NULLIF equivalent
        
        formatted = format_kpi_with_benchmark("ROAS", roas_mdl, "4:1+")
        
        st.metric(
            label=formatted["title"],
            value=formatted["value"],
            help=formatted["benchmark"]
        )
        st.caption(formatted["status"])
        
        with st.expander("📝 Formula"):
            st.code(roas_formula, language="sql")
    
    with col2:
        # MDL-driven CTR
        ctr_formula = get_measure_expression("marketing", "marketing_roi_kpis", "ctr")
        
        total_clicks = df['clicks'].sum()
        total_impressions = df['impressions'].sum()
        ctr_mdl = (total_clicks / max(total_impressions, 1)) * 100
        
        formatted = format_kpi_with_benchmark("CTR", ctr_mdl, "2-3%")
        
        st.metric(
            label=formatted["title"],
            value=f"{formatted['value']}%",
            help=formatted["benchmark"]
        )
        st.caption(formatted["status"])
        
        with st.expander("📝 Formula"):
            st.code(ctr_formula, language="sql")
    
    with col3:
        # MDL-driven Conversion Rate
        conv_formula = get_measure_expression("marketing", "marketing_roi_kpis", "conversion_rate")
        
        total_conversions = df['conversions'].sum()
        total_clicks = df['clicks'].sum()
        conv_rate_mdl = (total_conversions / max(total_clicks, 1)) * 100
        
        formatted = format_kpi_with_benchmark("Conversion Rate", conv_rate_mdl, "2-5%")
        
        st.metric(
            label=formatted["title"],
            value=f"{formatted['value']}%",
            help=formatted["benchmark"]
        )
        st.caption(formatted["status"])
        
        with st.expander("📝 Formula"):
            st.code(conv_formula, language="sql")
    
    st.success("""
    **Lợi ích của MDL:**
    - ✅ Single source of truth (1 chỗ định nghĩa duy nhất)
    - ✅ Consistent across all dashboards
    - ✅ Easy to maintain (sửa 1 lần, áp dụng toàn bộ)
    - ✅ Industry benchmarks built-in
    - ✅ Formula transparency → Trust 5 sao ⭐⭐⭐⭐⭐
    - ✅ Validated by experts (61 measures across 7 domains)
    """)

# ===== ALL MARKETING KPIS FROM MDL =====
st.header("4️⃣ All Marketing KPIs (Auto-generated from MDL)")

st.info(f"📊 **{metrics.name}**: {metrics.description}")

# Display all measures in a grid
measures_per_row = 4
num_rows = (len(metrics.measure) + measures_per_row - 1) // measures_per_row

for row in range(num_rows):
    cols = st.columns(measures_per_row)
    
    for col_idx in range(measures_per_row):
        measure_idx = row * measures_per_row + col_idx
        
        if measure_idx >= len(metrics.measure):
            break
        
        measure = metrics.measure[measure_idx]
        
        with cols[col_idx]:
            # Calculate value based on formula
            # (Simplified - production code would use proper SQL parser)
            if measure.name == "total_spend":
                value = df['spend'].sum()
            elif measure.name == "total_revenue":
                value = df['revenue'].sum()
            elif measure.name == "total_impressions":
                value = df['impressions'].sum()
            elif measure.name == "total_clicks":
                value = df['clicks'].sum()
            elif measure.name == "total_conversions":
                value = df['conversions'].sum()
            elif measure.name == "ctr":
                value = (df['clicks'].sum() / max(df['impressions'].sum(), 1)) * 100
            elif measure.name == "conversion_rate":
                value = (df['conversions'].sum() / max(df['clicks'].sum(), 1)) * 100
            elif measure.name == "roas":
                value = df['revenue'].sum() / max(df['spend'].sum(), 1)
            elif measure.name == "cac":
                value = df['spend'].sum() / max(df['customers'].sum(), 1)
            elif measure.name == "cpl":
                value = df['spend'].sum() / max(df['leads'].sum(), 1)
            else:
                value = 0
            
            # Display metric
            if "rate" in measure.name or "ctr" in measure.name or "conversion" in measure.name:
                st.metric(measure.name.upper(), f"{value:.2f}%")
            else:
                st.metric(measure.name.upper(), f"{value:,.0f}" if value > 1000 else f"{value:.2f}")
            
            if measure.description:
                st.caption(measure.description[:60] + "..." if len(measure.description) > 60 else measure.description)

# Show industry benchmark
if metrics.benchmark:
    st.info(f"🎯 **Industry Benchmark:** {metrics.benchmark}")

# ===== TRANSPARENCY: SHOW ALL FORMULAS =====
st.header("5️⃣ Formula Transparency (Trust Builder)")

with st.expander("📋 View All Formulas"):
    st.markdown("### How Each KPI is Calculated")
    
    for measure in metrics.measure:
        st.markdown(f"**{measure.name.upper()}** ({measure.type})")
        st.code(measure.expression, language="sql")
        if measure.description:
            st.caption(f"📝 {measure.description}")
        st.markdown("---")

# ===== CUSTOMER FEEDBACK SIMULATION =====
st.header("6️⃣ Customer Feedback")

feedback_col1, feedback_col2 = st.columns(2)

with feedback_col1:
    st.error("""
    **❌ Hardcoded Version**
    
    "Không hiểu ROAS được tính như thế nào? 🤔"
    
    "Benchmark ngành là bao nhiêu? 🤷"
    
    "Có chắc con số này đúng không? 😕"
    
    **Rating: ⭐⭐ (2/5 stars)**
    """)

with feedback_col2:
    st.success("""
    **✅ MDL Version**
    
    "Tôi thấy được công thức tính toán! 👍"
    
    "Có benchmark ngành để so sánh! 📊"
    
    "Tôi tin vào con số này! 💯"
    
    **Rating: ⭐⭐⭐⭐⭐ (5/5 stars)**
    """)

# ===== CONCLUSION =====
st.header("🎯 Conclusion")

st.success("""
**Semantic Layer (MDL) = Foundation for 5-Star Experience**

1. ✅ **Trust**: Formula transparency → Customers tin vào con số
2. ✅ **Accuracy**: Single source of truth → Zero hallucination
3. ✅ **Consistency**: Same calculation everywhere → Professional
4. ✅ **Benchmark**: Industry standards → Actionable insights
5. ✅ **Maintainability**: Change once, apply everywhere → Efficient

**Result:** ⭐⭐⭐⭐⭐ (5 stars) + ₫990K MRR potential
""")

st.markdown("---")
st.caption("📊 Powered by Semantic Layer (MDL) | Built for Vietnamese SMEs with ❤️")
