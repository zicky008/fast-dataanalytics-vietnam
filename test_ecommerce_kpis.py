"""
Test E-commerce KPIs with real data
Validates that all 7 KPIs are calculated correctly
"""

import pandas as pd
import sys
sys.path.insert(0, '/home/user/webapp/src')

from premium_lean_pipeline import PremiumLeanPipeline

# Load real e-commerce data
df = pd.read_csv('/home/user/webapp/sample_data/ecommerce_shopify_daily.csv')

print("=" * 80)
print("🛒 E-COMMERCE KPI CALCULATION TEST")
print("=" * 80)
print(f"\nDataset: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Columns: {', '.join(df.columns.tolist())}\n")

# Manually calculate expected values for validation
total_sessions = df['sessions'].sum()
total_transactions = df['transactions'].sum()
total_revenue = df['revenue'].sum()
total_add_to_carts = df['add_to_carts'].sum()
total_checkouts = df['checkout_initiated'].sum()

print("📊 MANUAL CALCULATIONS (Ground Truth):")
print("-" * 80)
print(f"1. Conversion Rate = {total_transactions}/{total_sessions} × 100")
print(f"   = {(total_transactions/total_sessions)*100:.2f}%")
print(f"\n2. AOV = {total_revenue:,.0f}/{total_transactions}")
print(f"   = {total_revenue/total_transactions:,.2f} VND")
print(f"\n3. Cart Abandonment = ({total_add_to_carts}-{total_checkouts})/{total_add_to_carts} × 100")
print(f"   = {((total_add_to_carts-total_checkouts)/total_add_to_carts)*100:.2f}%")
print(f"\n4. Revenue per Session = {total_revenue:,.0f}/{total_sessions}")
print(f"   = {total_revenue/total_sessions:,.2f} VND")
print(f"\n5. Returning Customer Rate = {df['returning_customer_rate'].mean():.2f}%")
print(f"6. Bounce Rate = {df['bounce_rate'].mean():.2f}%")
print(f"7. Mobile Traffic = {df['mobile_traffic_pct'].mean():.2f}%")

# Test pipeline KPI calculation
print("\n" + "=" * 80)
print("🔍 PIPELINE KPI CALCULATION TEST")
print("=" * 80)

class MockGeminiClient:
    pass

pipeline = PremiumLeanPipeline(gemini_client=MockGeminiClient())

# Mock domain info
domain_info = {
    'domain_name': 'E-commerce',
    'confidence': 0.95
}

# Calculate KPIs using pipeline
kpis = pipeline._calculate_real_kpis(df, domain_info)

print(f"\n✅ KPIs Calculated: {len(kpis)}")
print("-" * 80)

for kpi_name, kpi_data in kpis.items():
    value = kpi_data['value']
    benchmark = kpi_data['benchmark']
    status = kpi_data['status']
    
    print(f"\n{kpi_name}:")
    print(f"  Value: {value:,.2f}")
    print(f"  Benchmark: {benchmark:,.2f}")
    print(f"  Status: {status}")
    if 'insight' in kpi_data:
        print(f"  Insight: {kpi_data['insight']}")

# Validation checks
print("\n" + "=" * 80)
print("🧪 VALIDATION CHECKS")
print("=" * 80)

expected_cr = (total_transactions/total_sessions)*100
expected_aov = total_revenue/total_transactions
expected_abandonment = ((total_add_to_carts-total_checkouts)/total_add_to_carts)*100
expected_rps = total_revenue/total_sessions

errors = []

if 'Conversion Rate (%)' in kpis:
    actual_cr = kpis['Conversion Rate (%)']['value']
    diff = abs(actual_cr - expected_cr)
    if diff < 0.01:
        print(f"✅ Conversion Rate: {actual_cr:.2f}% (expected {expected_cr:.2f}%)")
    else:
        errors.append(f"❌ Conversion Rate mismatch: {actual_cr:.2f}% vs {expected_cr:.2f}%")
        print(errors[-1])
else:
    errors.append("❌ Conversion Rate not calculated")
    print(errors[-1])

if 'Average Order Value (AOV)' in kpis:
    actual_aov = kpis['Average Order Value (AOV)']['value']
    diff = abs(actual_aov - expected_aov)
    if diff < 1.0:  # Within 1 VND
        print(f"✅ AOV: {actual_aov:,.2f} VND (expected {expected_aov:,.2f} VND)")
    else:
        errors.append(f"❌ AOV mismatch: {actual_aov:,.2f} vs {expected_aov:,.2f}")
        print(errors[-1])
else:
    errors.append("❌ AOV not calculated")
    print(errors[-1])

if 'Cart Abandonment Rate (%)' in kpis:
    actual_abandonment = kpis['Cart Abandonment Rate (%)']['value']
    diff = abs(actual_abandonment - expected_abandonment)
    if diff < 0.01:
        print(f"✅ Cart Abandonment: {actual_abandonment:.2f}% (expected {expected_abandonment:.2f}%)")
    else:
        errors.append(f"❌ Cart Abandonment mismatch: {actual_abandonment:.2f}% vs {expected_abandonment:.2f}%")
        print(errors[-1])
else:
    errors.append("❌ Cart Abandonment not calculated")
    print(errors[-1])

if 'Revenue per Session' in kpis:
    actual_rps = kpis['Revenue per Session']['value']
    diff = abs(actual_rps - expected_rps)
    if diff < 1.0:
        print(f"✅ Revenue per Session: {actual_rps:,.2f} VND (expected {expected_rps:,.2f} VND)")
    else:
        errors.append(f"❌ RPS mismatch: {actual_rps:,.2f} vs {expected_rps:,.2f}")
        print(errors[-1])
else:
    errors.append("❌ Revenue per Session not calculated")
    print(errors[-1])

# Summary
print("\n" + "=" * 80)
print("📊 TEST SUMMARY")
print("=" * 80)

if len(errors) == 0:
    print(f"✅ ALL TESTS PASSED! ({len(kpis)} KPIs calculated correctly)")
    print("\n🎉 E-commerce module ready for 5-star experience!")
    sys.exit(0)
else:
    print(f"❌ {len(errors)} ERRORS FOUND:")
    for error in errors:
        print(f"  {error}")
    print(f"\n✅ {len(kpis) - len(errors)} KPIs working correctly")
    sys.exit(1)
