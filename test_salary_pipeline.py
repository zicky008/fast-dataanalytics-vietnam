"""
Test pipeline with Salary_Data.csv to debug KPI display issue
"""

import pandas as pd
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Setup
sys.path.insert(0, '/home/user/webapp/src')
load_dotenv()

from premium_lean_pipeline import PremiumLeanPipeline

# Load data
print("=" * 60)
print("📥 Loading Salary_Data.csv...")
print("=" * 60)

df = pd.read_csv('sample_data/Salary_Data.csv')
print(f"✅ Loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"\nColumns: {list(df.columns)}")
print(f"\nFirst 3 rows:\n{df.head(3)}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nBasic stats:\n{df.describe()}")

# Configure Gemini
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ Missing GEMINI_API_KEY")
    sys.exit(1)

genai.configure(api_key=api_key)
client = genai.GenerativeModel('gemini-2.0-flash')

# Run pipeline
print("\n" + "=" * 60)
print("🚀 Running Premium Lean Pipeline...")
print("=" * 60)

pipeline = PremiumLeanPipeline(client)

result = pipeline.run_pipeline(
    df=df,
    dataset_description="HR Salary dataset with employee demographics and compensation"
)

# Check result structure
print("\n" + "=" * 60)
print("📊 PIPELINE RESULT ANALYSIS")
print("=" * 60)

print(f"\n✅ Success: {result.get('success')}")
print(f"⏱️  Total Time: {result.get('performance', {}).get('total', 0):.1f}s")

# Domain Info
domain_info = result.get('domain_info', {})
print(f"\n🎯 DOMAIN INFO:")
print(f"   - Domain: {domain_info.get('domain_name', 'Unknown')}")
print(f"   - Confidence: {domain_info.get('confidence', 0)*100:.0f}%")
print(f"   - Expert: {domain_info.get('expert_role', 'N/A')[:60]}...")

# Quality Scores
quality_scores = result.get('quality_scores', {})
print(f"\n🎯 QUALITY SCORES:")
print(f"   - Cleaning: {quality_scores.get('cleaning', 0):.0f}/100")
print(f"   - Blueprint: {quality_scores.get('blueprint', 0):.0f}/100")
print(f"   - Overall: {quality_scores.get('overall', 0):.0f}/100")

# Dashboard KPIs - THIS IS THE KEY PART
dashboard = result.get('dashboard', {})
kpis = dashboard.get('kpis', {})

print(f"\n📊 DASHBOARD KPIs (Count: {len(kpis)}):")
if kpis:
    for kpi_name, kpi_data in kpis.items():
        value = kpi_data.get('value', 'N/A')
        benchmark = kpi_data.get('benchmark', 'N/A')
        status = kpi_data.get('status', 'N/A')
        print(f"   ✅ {kpi_name}:")
        print(f"      - Value: {value}")
        print(f"      - Benchmark: {benchmark}")
        print(f"      - Status: {status}")
else:
    print("   ❌ NO KPIs FOUND! This is the problem!")
    print(f"   Dashboard keys: {list(dashboard.keys())}")
    print(f"   Dashboard content: {dashboard}")

# Charts
charts = dashboard.get('charts', [])
print(f"\n📈 CHARTS (Count: {len(charts)}):")
for i, chart in enumerate(charts, 1):
    print(f"   {i}. {chart.get('title', 'Untitled')}")

# Insights
insights = result.get('insights', {})
print(f"\n💡 INSIGHTS:")
print(f"   - Executive Summary: {insights.get('executive_summary', 'N/A')[:100]}...")
print(f"   - Key Insights: {len(insights.get('key_insights', []))} items")
print(f"   - Recommendations: {len(insights.get('recommendations', []))} items")

# DEEP DIVE: Check smart_blueprint (where KPIs should be calculated)
smart_blueprint = result.get('smart_blueprint', {})
blueprint_kpis = smart_blueprint.get('kpis_calculated', {})

print(f"\n🔍 DEEP DIVE - SMART BLUEPRINT KPIs (Count: {len(blueprint_kpis)}):")
if blueprint_kpis:
    for kpi_name, kpi_data in blueprint_kpis.items():
        print(f"   ✅ {kpi_name}: {kpi_data}")
else:
    print("   ❌ NO KPIs in smart_blueprint either!")
    print(f"   smart_blueprint keys: {list(smart_blueprint.keys())}")

print("\n" + "=" * 60)
print("✅ Test complete!")
print("=" * 60)
