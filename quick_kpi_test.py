"""Quick test to verify KPI calculation accuracy"""
import pandas as pd
import sys
sys.path.insert(0, '/home/user/webapp/src')

from premium_lean_pipeline import PremiumLeanPipeline
from domain_detection import detect_domain

# Load data
df = pd.read_csv('sample_data/Salary_Data.csv')
print("=" * 70)
print("📊 REAL DATA STATISTICS (Ground Truth)")
print("=" * 70)
print(f"Dataset: {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"\nSalary Statistics:")
print(f"  Mean:   {df['Salary'].mean():,.2f}")
print(f"  Median: {df['Salary'].median():,.2f}")
print(f"  Min:    {df['Salary'].min():,.2f}")
print(f"  Max:    {df['Salary'].max():,.2f}")
print(f"  Range:  {df['Salary'].max() - df['Salary'].min():,.2f}")

# Detect domain
domain_info = detect_domain(df, "HR Salary dataset")
print(f"\n🎯 Domain: {domain_info.get('domain_name', 'Unknown')}")

# Initialize pipeline (create mock client)
class MockClient:
    pass

pipeline = PremiumLeanPipeline(MockClient())

# Test KPI calculation function
kpis = pipeline._calculate_real_kpis(df, domain_info)

print("\n" + "=" * 70)
print("🔍 CALCULATED KPIs (from _calculate_real_kpis)")
print("=" * 70)
for kpi_name, kpi_data in kpis.items():
    value = kpi_data.get('value')
    benchmark = kpi_data.get('benchmark')
    status = kpi_data.get('status')
    column = kpi_data.get('column', 'N/A')
    print(f"\n{kpi_name}:")
    print(f"  Value:     {value:,.2f}")
    print(f"  Benchmark: {benchmark:,.2f}")
    print(f"  Status:    {status}")
    print(f"  Column:    {column}")

# Verify accuracy
print("\n" + "=" * 70)
print("✅ ACCURACY VERIFICATION")
print("=" * 70)

if 'Average Salary' in kpis:
    calculated_avg = kpis['Average Salary']['value']
    real_avg = df['Salary'].mean()
    diff = abs(calculated_avg - real_avg)
    accuracy = 100 - (diff / real_avg * 100)
    
    print(f"\nAverage Salary:")
    print(f"  Real (pandas):      {real_avg:,.2f}")
    print(f"  Calculated (KPI):   {calculated_avg:,.2f}")
    print(f"  Difference:         {diff:,.2f}")
    print(f"  Accuracy:           {accuracy:.2f}%")
    
    if diff < 0.01:
        print(f"  ✅ PERFECT MATCH!")
    else:
        print(f"  ❌ DISCREPANCY FOUND!")

if 'Median Salary' in kpis:
    calculated_median = kpis['Median Salary']['value']
    real_median = df['Salary'].median()
    diff = abs(calculated_median - real_median)
    
    print(f"\nMedian Salary:")
    print(f"  Real (pandas):      {real_median:,.2f}")
    print(f"  Calculated (KPI):   {calculated_median:,.2f}")
    print(f"  Difference:         {diff:,.2f}")
    
    if diff < 0.01:
        print(f"  ✅ PERFECT MATCH!")
    else:
        print(f"  ❌ DISCREPANCY FOUND!")

print("\n" + "=" * 70)
print("✅ Test Complete!")
print("=" * 70)
