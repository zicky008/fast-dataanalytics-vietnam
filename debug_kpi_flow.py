"""Debug KPI flow - trace where values come from"""
import pandas as pd
import os
import sys
import json
from dotenv import load_dotenv
import google.generativeai as genai

sys.path.insert(0, '/home/user/webapp/src')
load_dotenv()

from premium_lean_pipeline import PremiumLeanPipeline

# Load data
df = pd.read_csv('sample_data/Salary_Data.csv')
print("=" * 80)
print("🔍 DEBUG: KPI VALUE FLOW")
print("=" * 80)

# Real values
print(f"\n📊 STEP 0: Real Data (Ground Truth)")
print(f"   df['Salary'].mean():   ${df['Salary'].mean():,.2f}")
print(f"   df['Salary'].median(): ${df['Salary'].median():,.2f}")

# Calculate KPIs manually
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)
client = genai.GenerativeModel('gemini-2.0-flash')

pipeline = PremiumLeanPipeline(client)

from domain_detection import detect_domain
domain_info = detect_domain(df, "HR Salary dataset")

# Step 1: Calculate real KPIs
print(f"\n📊 STEP 0.5: Domain info")
print(f"   Domain: {domain_info.get('domain_name')}")
print(f"   Confidence: {domain_info.get('confidence')*100:.1f}%")

kpis_calc = pipeline._calculate_real_kpis(df, domain_info)
print(f"\n📊 STEP 1: _calculate_real_kpis() output")
print(f"   Total KPIs: {len(kpis_calc)}")
for kpi_name, kpi_data in kpis_calc.items():
    print(f"   {kpi_name}: ${kpi_data['value']:,.2f}")
    
if 'Average Salary' not in kpis_calc:
    print(f"   ❌ WARNING: 'Average Salary' not found!")
    print(f"   Available KPIs: {list(kpis_calc.keys())}")

# Step 2: Run full pipeline
print(f"\n📊 STEP 2: Running full pipeline...")
result = pipeline.run_pipeline(df=df, dataset_description="HR Salary dataset")

# Step 3: Check smart_blueprint KPIs
smart_blueprint = result.get('smart_blueprint', {})
kpis_from_blueprint = smart_blueprint.get('kpis_calculated', {})
print(f"\n📊 STEP 3: smart_blueprint['kpis_calculated']")
if 'Average Salary' in kpis_from_blueprint:
    print(f"   Average Salary: ${kpis_from_blueprint['Average Salary']['value']:,.2f}")
if 'Median Salary' in kpis_from_blueprint:
    print(f"   Median Salary:  ${kpis_from_blueprint['Median Salary']['value']:,.2f}")

# Step 4: Check dashboard KPIs
dashboard = result.get('dashboard', {})
kpis_from_dashboard = dashboard.get('kpis', {})
print(f"\n📊 STEP 4: dashboard['kpis'] (final output)")
if 'Average Salary' in kpis_from_dashboard:
    print(f"   Average Salary: ${kpis_from_dashboard['Average Salary']['value']:,.2f}")
if 'Median Salary' in kpis_from_dashboard:
    print(f"   Median Salary:  ${kpis_from_dashboard['Median Salary']['value']:,.2f}")

# Compare
print("\n" + "=" * 80)
print("🎯 ACCURACY CHECK")
print("=" * 80)

real_avg = df['Salary'].mean()
if 'Average Salary' in kpis_from_dashboard:
    final_avg = kpis_from_dashboard['Average Salary']['value']
    diff = abs(final_avg - real_avg)
    print(f"\nAverage Salary:")
    print(f"   Real:       ${real_avg:,.2f}")
    print(f"   Final:      ${final_avg:,.2f}")
    print(f"   Difference: ${diff:,.2f}")
    
    if diff < 0.01:
        print(f"   ✅ PERFECT MATCH!")
    else:
        print(f"   ❌ DISCREPANCY!")
        print(f"\n🔍 DEBUG: Where did the value change?")
        if 'Average Salary' in kpis_calc:
            if abs(kpis_calc['Average Salary']['value'] - real_avg) < 0.01:
                print(f"   ✅ _calculate_real_kpis() was correct: ${kpis_calc['Average Salary']['value']:,.2f}")
            else:
                print(f"   ❌ _calculate_real_kpis() was wrong!")
        
        if 'Average Salary' in kpis_from_blueprint:
            if abs(kpis_from_blueprint['Average Salary']['value'] - real_avg) < 0.01:
                print(f"   ✅ smart_blueprint was correct: ${kpis_from_blueprint['Average Salary']['value']:,.2f}")
            else:
                print(f"   ❌ smart_blueprint was wrong: ${kpis_from_blueprint['Average Salary']['value']:,.2f}")
                print(f"      (AI modified it after force replace?)")
        
        print(f"\n   → Issue: Values changed between smart_blueprint and dashboard")

print("=" * 80)
