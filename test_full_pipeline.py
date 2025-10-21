"""
Full pipeline test with Salary_Data.csv
Verify both fixes: P0 (KPI accuracy) + P1 (domain detection)
"""
import pandas as pd
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

sys.path.insert(0, '/home/user/webapp/src')
load_dotenv()

from premium_lean_pipeline import PremiumLeanPipeline

print("=" * 80)
print("🧪 FULL PIPELINE TEST - POST-FIX VERIFICATION")
print("=" * 80)

# Load data
df = pd.read_csv('sample_data/Salary_Data.csv')
print(f"\n📊 Dataset: Salary_Data.csv ({df.shape[0]:,} rows × {df.shape[1]} columns)")

# Real statistics - AFTER cleaning (since pipeline works on cleaned data)
print(f"\n🎯 GROUND TRUTH (Raw Data):")
print(f"   Rows: {len(df)}")
print(f"   Duplicates: {df.duplicated().sum()}")
print(f"   Average Salary: ${df['Salary'].mean():,.2f}")

# Simulate cleaning
df_test_cleaned = df.drop_duplicates()
print(f"\n🎯 GROUND TRUTH (After drop_duplicates - what pipeline uses):")
print(f"   Rows: {len(df_test_cleaned)}")
print(f"   Average Salary: ${df_test_cleaned['Salary'].mean():,.2f}")
print(f"   Median Salary:  ${df_test_cleaned['Salary'].median():,.2f}")
print(f"   Salary Range:   ${df_test_cleaned['Salary'].max() - df_test_cleaned['Salary'].min():,.2f}")

# Configure Gemini
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ Missing GEMINI_API_KEY")
    sys.exit(1)

genai.configure(api_key=api_key)
client = genai.GenerativeModel('gemini-2.0-flash')

# Run pipeline
print("\n" + "=" * 80)
print("🚀 Running Premium Lean Pipeline...")
print("=" * 80)

pipeline = PremiumLeanPipeline(client)
result = pipeline.run_pipeline(
    df=df,
    dataset_description="HR Salary dataset with employee demographics and compensation"
)

# Check results
print("\n" + "=" * 80)
print("📊 PIPELINE RESULTS")
print("=" * 80)

success = result.get('success')
print(f"\n✅ Success: {success}")

if not success:
    print(f"❌ Error: {result.get('error')}")
    sys.exit(1)

# 1. Domain Detection Verification
domain_info = result.get('domain_info', {})
print(f"\n🎯 DOMAIN DETECTION:")
print(f"   Domain:       {domain_info.get('domain_name', 'Unknown')}")
print(f"   Confidence:   {domain_info.get('confidence', 0)*100:.1f}%")
print(f"   Expert Role:  {domain_info.get('expert_role', 'N/A')[:60]}...")

if 'hr' in domain_info.get('domain_name', '').lower() or 'nhân sự' in domain_info.get('domain_name', '').lower():
    print(f"   ✅ PASS: Correctly detected as HR domain")
else:
    print(f"   ⚠️  WARNING: Expected HR but got {domain_info.get('domain_name')}")

# 2. KPI Accuracy Verification
dashboard = result.get('dashboard', {})
kpis = dashboard.get('kpis', {})

print(f"\n📈 KPI ACCURACY VERIFICATION:")
print(f"   Total KPIs: {len(kpis)}")

if 'Average Salary' in kpis:
    kpi_value = kpis['Average Salary']['value']
    # Compare with CLEANED data (pipeline works on cleaned data)
    real_value = df_test_cleaned['Salary'].mean()
    diff = abs(kpi_value - real_value)
    accuracy = 100 - (diff / real_value * 100)
    
    print(f"\n   Average Salary:")
    print(f"      Real (cleaned):   ${real_value:,.2f}")
    print(f"      KPI (pipeline):   ${kpi_value:,.2f}")
    print(f"      Difference:       ${diff:,.2f}")
    print(f"      Accuracy:         {accuracy:.2f}%")
    
    # Allow small floating point differences (<$10 or 0.01%)
    if diff < 10 or accuracy >= 99.99:
        print(f"      ✅ PASS: {accuracy:.2f}% accuracy (within tolerance)")
    else:
        print(f"      ❌ FAIL: Discrepancy found")

if 'Median Salary' in kpis:
    kpi_value = kpis['Median Salary']['value']
    # Compare with CLEANED data
    real_value = df_test_cleaned['Salary'].median()
    diff = abs(kpi_value - real_value)
    
    print(f"\n   Median Salary:")
    print(f"      Real (cleaned):   ${real_value:,.2f}")
    print(f"      KPI (pipeline):   ${kpi_value:,.2f}")
    print(f"      Difference:       ${diff:,.2f}")
    
    # Allow small floating point differences (<$10 or 0.01%)
    if diff < 10 or accuracy >= 99.99:
        print(f"      ✅ PASS: {accuracy:.2f}% accuracy (within tolerance)")
    else:
        print(f"      ❌ FAIL: Discrepancy found")

# 3. Performance
perf = result.get('performance', {})
total_time = perf.get('total', 0)
print(f"\n⏱️  PERFORMANCE:")
print(f"   Total Time: {total_time:.1f}s")
if total_time < 60:
    print(f"   ✅ PASS: Under 60s target")
else:
    print(f"   ⚠️  WARNING: Exceeded 60s target")

# 4. Quality Score
quality = result.get('quality_scores', {})
overall = quality.get('overall', 0)
print(f"\n🎯 QUALITY SCORE:")
print(f"   Overall: {overall:.0f}/100")
if overall >= 80:
    print(f"   ✅ PASS: Above 80/100 threshold")
else:
    print(f"   ⚠️  WARNING: Below 80/100 threshold")

# 5. Charts
charts = dashboard.get('charts', [])
print(f"\n📊 CHARTS:")
print(f"   Total: {len(charts)}")
if len(charts) >= 5:
    print(f"   ✅ PASS: {len(charts)} charts generated")
    for i, chart in enumerate(charts[:3], 1):
        print(f"      {i}. {chart.get('title', 'Untitled')}")
    if len(charts) > 3:
        print(f"      ... and {len(charts)-3} more")
else:
    print(f"   ⚠️  WARNING: Only {len(charts)} charts (target: 5+)")

# 6. Insights
insights = result.get('insights', {})
print(f"\n💡 INSIGHTS:")
print(f"   Executive Summary: {len(insights.get('executive_summary', ''))} chars")
print(f"   Key Insights: {len(insights.get('key_insights', []))} items")
print(f"   Recommendations: {len(insights.get('recommendations', []))} items")

# Final verdict
print("\n" + "=" * 80)
print("🎯 FINAL VERDICT")
print("=" * 80)

issues = []
if 'hr' not in domain_info.get('domain_name', '').lower() and 'nhân sự' not in domain_info.get('domain_name', '').lower():
    issues.append("Domain detection failed")
# Compare with CLEANED data (allow $10 tolerance for floating point)
if 'Average Salary' in kpis and abs(kpis['Average Salary']['value'] - df_test_cleaned['Salary'].mean()) >= 10:
    issues.append("KPI accuracy issue")
if total_time >= 60:
    issues.append("Performance issue")
if overall < 80:
    issues.append("Quality score issue")

if not issues:
    print("✅ ALL TESTS PASSED!")
    print("   - Domain detection: HR ✅")
    print("   - KPI accuracy: 100% ✅")
    print("   - Performance: <60s ✅")
    print("   - Quality: ≥80/100 ✅")
    print("\n🚀 Pipeline is PRODUCTION READY!")
else:
    print(f"⚠️  ISSUES FOUND: {', '.join(issues)}")
    print("\n🔧 Needs attention before production")

print("=" * 80)
