"""
Test E-commerce 5-Star Features:
1. Cart Funnel Breakdown (2 new KPIs)
2. Enhanced Mobile Insights
3. Performance Trends Analysis
"""

import pandas as pd
import sys
sys.path.insert(0, '/home/user/webapp/src')

from premium_lean_pipeline import PremiumLeanPipeline

# Load real e-commerce data
df = pd.read_csv('/home/user/webapp/sample_data/ecommerce_shopify_daily.csv')

print("=" * 80)
print("🛒 E-COMMERCE 5-STAR FEATURES TEST")
print("=" * 80)
print(f"\nDataset: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Channels: {df['channel'].unique().tolist()}\n")

# Test pipeline
class MockGeminiClient:
    pass

pipeline = PremiumLeanPipeline(gemini_client=MockGeminiClient())

domain_info = {
    'domain_name': 'E-commerce',
    'confidence': 0.95
}

print("=" * 80)
print("TEST 1: ENHANCED KPIs (Should be 9 total now)")
print("=" * 80)

kpis = pipeline._calculate_real_kpis(df, domain_info)

print(f"\n✅ Total KPIs: {len(kpis)}")
print("\nKPI List:")
for idx, (kpi_name, kpi_data) in enumerate(kpis.items(), 1):
    print(f"{idx}. {kpi_name}: {kpi_data['value']:.2f}")
    if 'insight' in kpi_data:
        print(f"   💡 {kpi_data['insight']}")

# Check for new funnel KPIs
print("\n" + "=" * 80)
print("TEST 2: CART FUNNEL BREAKDOWN (NEW)")
print("=" * 80)

funnel_kpis = [k for k in kpis.keys() if 'Funnel' in k]
if len(funnel_kpis) >= 2:
    print(f"✅ Found {len(funnel_kpis)} funnel KPIs:")
    for kpi_name in funnel_kpis:
        kpi_data = kpis[kpi_name]
        print(f"\n{kpi_name}:")
        print(f"  Value: {kpi_data['value']:.2f}%")
        print(f"  Benchmark: {kpi_data['benchmark']:.2f}%")
        print(f"  Status: {kpi_data['status']}")
        print(f"  Insight: {kpi_data['insight']}")
else:
    print(f"❌ Expected 2 funnel KPIs, found {len(funnel_kpis)}")

# Check mobile insights enhancement
print("\n" + "=" * 80)
print("TEST 3: ENHANCED MOBILE INSIGHTS")
print("=" * 80)

if 'Mobile Traffic (%)' in kpis:
    mobile_kpi = kpis['Mobile Traffic (%)']
    print(f"✅ Mobile Traffic: {mobile_kpi['value']:.2f}%")
    print(f"   Insight: {mobile_kpi['insight']}")
    
    # Check if insight is enhanced (should be longer)
    if len(mobile_kpi['insight']) > 50:
        print("   ✅ Enhanced insight detected (detailed guidance)")
    else:
        print("   ⚠️ Basic insight (could be more detailed)")
else:
    print("❌ Mobile Traffic KPI not found")

# Test dimension analysis with trends
print("\n" + "=" * 80)
print("TEST 4: PERFORMANCE TRENDS ANALYSIS (NEW)")
print("=" * 80)

analysis = pipeline._calculate_dimension_analysis(df, domain_info)

if 'performance_trends' in analysis:
    trends = analysis['performance_trends']
    print(f"✅ Trend Analysis Found!")
    print(f"\nPeriod: {trends['period']}")
    print(f"Days Analyzed: {trends['days_analyzed']}")
    print(f"Overall Trend: {trends['overall_trend']}")
    print(f"CR Change: {trends['cr_change_pct']:.1f}%")
    print(f"Revenue Change: {trends['revenue_change_pct']:.1f}%")
    
    print(f"\nBest Day: {trends['best_day']['date']}")
    print(f"  CR: {trends['best_day']['conversion_rate']:.2f}%")
    print(f"  Revenue: {trends['best_day']['revenue']:,.0f} VND")
    
    print(f"\nWorst Day: {trends['worst_day']['date']}")
    print(f"  CR: {trends['worst_day']['conversion_rate']:.2f}%")
    print(f"  Revenue: {trends['worst_day']['revenue']:,.0f} VND")
    
    print(f"\n💡 TREND INSIGHTS ({len(trends['insights'])} total):")
    for idx, insight in enumerate(trends['insights'], 1):
        print(f"{idx}. {insight['message']}")
        print(f"   👉 {insight['action']}")
else:
    print("❌ Performance trends not found")

# Summary
print("\n" + "=" * 80)
print("📊 TEST SUMMARY")
print("=" * 80)

errors = []

# Validation 1: Should have 9+ KPIs now
if len(kpis) < 9:
    errors.append(f"Expected 9+ KPIs, got {len(kpis)}")
else:
    print(f"✅ KPI Count: {len(kpis)} (expected 9+)")

# Validation 2: Funnel KPIs present
if len(funnel_kpis) >= 2:
    print(f"✅ Funnel Breakdown: {len(funnel_kpis)} KPIs")
else:
    errors.append(f"Expected 2 funnel KPIs, got {len(funnel_kpis)}")

# Validation 3: Mobile insights enhanced
if 'Mobile Traffic (%)' in kpis and len(kpis['Mobile Traffic (%)']['insight']) > 50:
    print(f"✅ Mobile Insights: Enhanced")
else:
    errors.append("Mobile insights not enhanced")

# Validation 4: Trends present
if 'performance_trends' in analysis:
    print(f"✅ Trend Analysis: Working")
else:
    errors.append("Trend analysis not found")

# Validation 5: Channel breakdown still working
if 'channel_breakdown' in analysis:
    print(f"✅ Channel Breakdown: Still working ({len(analysis['channel_breakdown']['data'])} channels)")
else:
    errors.append("Channel breakdown broken")

if len(errors) == 0:
    print("\n🎉 ALL 5-STAR FEATURES WORKING!")
    print("\n✨ E-commerce module is now 5-STAR READY:")
    print("   ✅ 9+ accurate KPIs")
    print("   ✅ Cart funnel breakdown")
    print("   ✅ Enhanced mobile insights")
    print("   ✅ Performance trends")
    print("   ✅ Channel analysis")
    sys.exit(0)
else:
    print(f"\n❌ {len(errors)} ERRORS:")
    for error in errors:
        print(f"  {error}")
    sys.exit(1)
