"""
Test Enhanced Marketing Features:
1. 7 Marketing KPIs (including new CPA)
2. Campaign-level breakdown with ROAS, CPA, CPC
3. 5-star actionable insights with budget reallocation
"""

import pandas as pd
import sys
sys.path.insert(0, '/home/user/webapp/src')

from premium_lean_pipeline import PremiumLeanPipeline

# Load real marketing data
df = pd.read_csv('/home/user/webapp/sample_data/marketing_multichannel_campaigns.csv')

print("=" * 80)
print("📱 MARKETING ENHANCED FEATURES TEST")
print("=" * 80)
print(f"\nDataset: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Campaigns: {df['campaign_name'].unique().tolist()}\n")

# Manual calculations for validation
total_spend = df['spend'].sum()
total_revenue = df['revenue'].sum()
total_conversions = df['conversions'].sum()
overall_roas = total_revenue / total_spend

print("📊 MANUAL CALCULATIONS (Ground Truth):")
print("-" * 80)
print(f"Total Spend: {total_spend:,.0f} VND")
print(f"Total Revenue: {total_revenue:,.0f} VND")
print(f"Overall ROAS: {overall_roas:.2f}x")
print(f"Total Conversions: {total_conversions:,.0f}")
print(f"Overall CPA: {total_spend/total_conversions:,.0f} VND")

# Test pipeline
class MockGeminiClient:
    pass

pipeline = PremiumLeanPipeline(gemini_client=MockGeminiClient())

domain_info = {
    'domain_name': 'Marketing',
    'confidence': 0.95
}

print("\n" + "=" * 80)
print("TEST 1: ENHANCED MARKETING KPIs (Should be 7 total)")
print("=" * 80)

kpis = pipeline._calculate_real_kpis(df, domain_info)

print(f"\n✅ Total KPIs: {len(kpis)}")
print("\nKPI List:")
for idx, (kpi_name, kpi_data) in enumerate(kpis.items(), 1):
    print(f"{idx}. {kpi_name}: {kpi_data['value']:,.2f}")
    if 'insight' in kpi_data:
        print(f"   💡 {kpi_data['insight']}")

# Validate CPA
if 'Cost Per Acquisition (CPA)' in kpis:
    expected_cpa = total_spend / total_conversions
    actual_cpa = kpis['Cost Per Acquisition (CPA)']['value']
    diff = abs(actual_cpa - expected_cpa)
    if diff < 1.0:
        print(f"\n✅ CPA Validation: {actual_cpa:,.2f} VND (expected {expected_cpa:,.2f} VND)")
    else:
        print(f"\n❌ CPA Mismatch: {actual_cpa:,.2f} vs {expected_cpa:,.2f}")
else:
    print("\n❌ CPA KPI not found")

print("\n" + "=" * 80)
print("TEST 2: CAMPAIGN BREAKDOWN")
print("=" * 80)

analysis = pipeline._calculate_dimension_analysis(df, domain_info)

if 'campaign_breakdown' in analysis:
    campaigns = analysis['campaign_breakdown']
    print(f"\n✅ Campaign Analysis Found!")
    print(f"Best Campaign: {campaigns['best_campaign']}")
    print(f"Worst Campaign: {campaigns['worst_campaign']}")
    
    print("\n" + "-" * 80)
    print("Campaign Performance:")
    print("-" * 80)
    
    for campaign in campaigns['data']:
        print(f"\n📍 {campaign['campaign']}")
        print(f"   Spend: {campaign['spend']:,.0f} VND")
        print(f"   Revenue: {campaign['revenue']:,.0f} VND")
        print(f"   ROAS: {campaign['roas']:.2f}x")
        if 'cpa' in campaign:
            print(f"   CPA: {campaign['cpa']:,.0f} VND")
        if 'cpc' in campaign:
            print(f"   CPC: {campaign['cpc']:,.0f} VND")
    
    # Validate against manual calculations
    print("\n" + "=" * 80)
    print("VALIDATION: Email Campaign (Best)")
    print("=" * 80)
    
    email_data = df[df['campaign_name'] == 'Email Newsletter']
    email_spend = email_data['spend'].sum()
    email_revenue = email_data['revenue'].sum()
    email_roas = email_revenue / email_spend
    email_conversions = email_data['conversions'].sum()
    email_cpa = email_spend / email_conversions
    
    print(f"Expected Email ROAS: {email_roas:.2f}x")
    print(f"Expected Email CPA: {email_cpa:,.0f} VND")
    
    email_campaign = [c for c in campaigns['data'] if 'Email' in c['campaign']][0]
    print(f"Actual Email ROAS: {email_campaign['roas']:.2f}x")
    print(f"Actual Email CPA: {email_campaign.get('cpa', 0):,.0f} VND")
    
    if abs(email_campaign['roas'] - email_roas) < 0.01:
        print("✅ ROAS calculation correct!")
    else:
        print("❌ ROAS mismatch!")

else:
    print("❌ Campaign breakdown not found")

print("\n" + "=" * 80)
print("TEST 3: 5-STAR ACTIONABLE INSIGHTS")
print("=" * 80)

if 'campaign_breakdown' in analysis:
    insights = analysis['campaign_breakdown']['insights']
    print(f"\n✅ {len(insights)} insights generated:")
    
    for idx, insight in enumerate(insights, 1):
        print(f"\n{idx}. [{insight['type'].upper()}]")
        print(f"   {insight['message']}")
        print(f"   👉 {insight['action']}")
    
    # Check for critical insights
    insight_types = [i['type'] for i in insights]
    
    critical_checks = {
        'scale_winner': '✅ Scale winner insight' if 'scale_winner' in insight_types else '❌ Missing scale insight',
        'stop_bleeding': '✅ Stop bleeding insight' if 'stop_bleeding' in insight_types else '⚠️ No unprofitable campaigns',
        'budget_reallocation': '✅ Budget reallocation' if 'budget_reallocation' in insight_types else '⚠️ No reallocation needed'
    }
    
    print("\n" + "=" * 80)
    print("INSIGHT QUALITY CHECKS:")
    print("=" * 80)
    for check, status in critical_checks.items():
        print(f"  {status}")
else:
    print("❌ No insights generated")

# Summary
print("\n" + "=" * 80)
print("📊 TEST SUMMARY")
print("=" * 80)

errors = []

# Check 1: Should have 7+ KPIs
if len(kpis) >= 7:
    print(f"✅ KPI Count: {len(kpis)} (expected 7+)")
else:
    errors.append(f"Expected 7+ KPIs, got {len(kpis)}")

# Check 2: CPA must exist
if 'Cost Per Acquisition (CPA)' in kpis:
    print(f"✅ CPA KPI: Present")
else:
    errors.append("CPA KPI missing")

# Check 3: Campaign breakdown working
if 'campaign_breakdown' in analysis:
    print(f"✅ Campaign Breakdown: {len(analysis['campaign_breakdown']['data'])} campaigns")
else:
    errors.append("Campaign breakdown not working")

# Check 4: At least 3 insights
if 'campaign_breakdown' in analysis and len(analysis['campaign_breakdown']['insights']) >= 3:
    print(f"✅ Actionable Insights: {len(analysis['campaign_breakdown']['insights'])}")
else:
    errors.append("Insufficient insights (<3)")

if len(errors) == 0:
    print("\n🎉 ALL MARKETING FEATURES WORKING!")
    print("\n✨ Marketing module ready for:")
    print("   ✅ 7 accurate KPIs")
    print("   ✅ Campaign-level breakdown")
    print("   ✅ Budget reallocation recommendations")
    print("   ✅ 5-star actionable insights")
    sys.exit(0)
else:
    print(f"\n❌ {len(errors)} ERRORS:")
    for error in errors:
        print(f"  {error}")
    sys.exit(1)
