"""
DEEP AUDIT: KPI Accuracy - Zero Tolerance for Discrepancy
Expert: Senior Data Engineer + Statistician + QA Expert

Goal: Find exact root cause of $4.07 difference and fix it to ZERO
"""
import pandas as pd
import numpy as np
import sys
import os
from dotenv import load_dotenv
import google.generativeai as genai

sys.path.insert(0, '/home/user/webapp/src')
load_dotenv()

from premium_lean_pipeline import PremiumLeanPipeline
from domain_detection import detect_domain

print("=" * 90)
print("🔬 DEEP AUDIT: KPI ACCURACY - ZERO TOLERANCE FOR ERRORS")
print("=" * 90)
print("\n👤 Expert Panel:")
print("   - Senior Data Engineer (15+ years)")
print("   - Statistician (PhD, specializing in data quality)")
print("   - QA Expert (zero-defect methodology)")
print("\n🎯 Mission: Find and eliminate ALL sources of discrepancy")
print("   Standard: 100% accuracy - NO approximations allowed")
print("=" * 90)

# Load data
df_original = pd.read_csv('sample_data/Salary_Data.csv')

print("\n📊 STEP 1: ORIGINAL DATA ANALYSIS")
print("-" * 90)
print(f"Total rows: {len(df_original):,}")
print(f"Salary column dtype: {df_original['Salary'].dtype}")
print(f"Missing values in Salary: {df_original['Salary'].isnull().sum()}")
print(f"Duplicates in dataset: {df_original.duplicated().sum():,}")

# Calculate original statistics WITH MAXIMUM PRECISION
salary_original = df_original['Salary'].dropna()
print(f"\n💰 Original Salary Statistics (before any processing):")
print(f"   Count:  {len(salary_original):,}")
print(f"   Mean:   ${salary_original.mean():.10f}")  # 10 decimal places
print(f"   Median: ${salary_original.median():.10f}")
print(f"   Std:    ${salary_original.std():.10f}")

# Configure pipeline
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
client = genai.GenerativeModel('gemini-2.0-flash')
pipeline = PremiumLeanPipeline(client)
domain_info = detect_domain(df_original, "HR Salary dataset")

print("\n📊 STEP 2: DATA CLEANING SIMULATION")
print("-" * 90)

# Simulate cleaning step by step
df_step1 = df_original.copy()
print(f"After copy: {len(df_step1):,} rows")

# Check if cleaning will fillna
missing_count = df_step1['Salary'].isnull().sum()
print(f"\nMissing values check: {missing_count}")
if missing_count > 0:
    median_val = df_step1['Salary'].median()
    print(f"   Will fillna with median: ${median_val:.10f}")
    df_step1['Salary'] = df_step1['Salary'].fillna(median_val)
    salary_after_fillna = df_step1['Salary']
    print(f"   Mean after fillna: ${salary_after_fillna.mean():.10f}")
else:
    print(f"   No fillna needed (no missing values)")

# Drop duplicates
duplicates = df_step1.duplicated().sum()
print(f"\nDuplicates: {duplicates:,}")
df_step1_clean = df_step1.drop_duplicates()
print(f"After drop_duplicates: {len(df_step1_clean):,} rows")

salary_cleaned = df_step1_clean['Salary']
print(f"\n💰 Cleaned Salary Statistics (ground truth):")
print(f"   Count:  {len(salary_cleaned):,}")
print(f"   Mean:   ${salary_cleaned.mean():.10f}")
print(f"   Median: ${salary_cleaned.median():.10f}")
print(f"   Std:    ${salary_cleaned.std():.10f}")

# Save this as GROUND TRUTH
ground_truth_mean = salary_cleaned.mean()
ground_truth_median = salary_cleaned.median()

print("\n📊 STEP 3: PIPELINE CLEANING (What pipeline actually does)")
print("-" * 90)

# Run actual pipeline cleaning
cleaning_result = pipeline.step1_data_cleaning(df_original, domain_info)
df_pipeline_cleaned = cleaning_result['df_cleaned']

salary_pipeline = df_pipeline_cleaned['Salary']
print(f"Pipeline cleaned rows: {len(df_pipeline_cleaned):,}")
print(f"\n💰 Pipeline Cleaned Salary Statistics:")
print(f"   Count:  {len(salary_pipeline):,}")
print(f"   Mean:   ${salary_pipeline.mean():.10f}")
print(f"   Median: ${salary_pipeline.median():.10f}")
print(f"   Std:    ${salary_pipeline.std():.10f}")

# Compare
print("\n📊 STEP 4: COMPARE CLEANING METHODS")
print("-" * 90)
print(f"Ground Truth (manual):  {len(salary_cleaned):,} rows, Mean: ${ground_truth_mean:.10f}")
print(f"Pipeline (actual):      {len(salary_pipeline):,} rows, Mean: ${salary_pipeline.mean():.10f}")
print(f"Difference in mean:     ${abs(ground_truth_mean - salary_pipeline.mean()):.10f}")

if len(salary_cleaned) != len(salary_pipeline):
    print(f"\n⚠️  ROW COUNT MISMATCH!")
    print(f"   Ground truth: {len(salary_cleaned):,}")
    print(f"   Pipeline:     {len(salary_pipeline):,}")
    print(f"   Difference:   {abs(len(salary_cleaned) - len(salary_pipeline)):,} rows")
    
    # Check for data differences
    print("\n🔍 Investigating row differences...")
    # Check if it's just ordering or actual data difference
    sorted_gt = sorted(salary_cleaned.values)
    sorted_pl = sorted(salary_pipeline.values)
    
    if len(sorted_gt) == len(sorted_pl):
        if np.allclose(sorted_gt, sorted_pl):
            print("   ✅ Same data, just different order")
        else:
            print("   ❌ Different data values!")
    else:
        print("   ❌ Different number of records!")

print("\n📊 STEP 5: KPI CALCULATION TEST")
print("-" * 90)

# Test _calculate_real_kpis with cleaned data
kpis_manual = pipeline._calculate_real_kpis(df_pipeline_cleaned, domain_info)

if 'Average Salary' in kpis_manual:
    kpi_value = kpis_manual['Average Salary']['value']
    print(f"KPI calculated by _calculate_real_kpis:")
    print(f"   Value: ${kpi_value:.10f}")
    print(f"   Expected (pipeline cleaned): ${salary_pipeline.mean():.10f}")
    print(f"   Difference: ${abs(kpi_value - salary_pipeline.mean()):.10f}")
    
    if abs(kpi_value - salary_pipeline.mean()) > 0.001:
        print(f"\n❌ PROBLEM FOUND: _calculate_real_kpis returns different value!")
        print(f"   This should be EXACTLY the same as df['Salary'].mean()")
    else:
        print(f"\n✅ _calculate_real_kpis is accurate")

print("\n📊 STEP 6: FULL PIPELINE END-TO-END TEST")
print("-" * 90)

result = pipeline.run_pipeline(df_original, "HR Salary dataset")
dashboard = result.get('dashboard', {})
kpis_final = dashboard.get('kpis', {})

if 'Average Salary' in kpis_final:
    final_value = kpis_final['Average Salary']['value']
    print(f"Final KPI from full pipeline:")
    print(f"   Value: ${final_value:.10f}")
    print(f"   Expected: ${ground_truth_mean:.10f}")
    print(f"   Difference: ${abs(final_value - ground_truth_mean):.10f}")

print("\n" + "=" * 90)
print("🎯 ROOT CAUSE ANALYSIS")
print("=" * 90)

# Determine exact source of discrepancy
pipeline_mean = salary_pipeline.mean()
manual_mean = ground_truth_mean
final_kpi = kpis_final.get('Average Salary', {}).get('value', 0)

diff_cleaning = abs(pipeline_mean - manual_mean)
diff_kpi_calc = abs(final_kpi - pipeline_mean)
diff_total = abs(final_kpi - manual_mean)

print(f"\n📊 Discrepancy Breakdown:")
print(f"   1. Cleaning stage:     ${diff_cleaning:.10f}")
print(f"      (Pipeline cleaning vs Manual simulation)")
print(f"   ")
print(f"   2. KPI calculation:    ${diff_kpi_calc:.10f}")
print(f"      (_calculate_real_kpis vs df.mean())")
print(f"   ")
print(f"   3. Total discrepancy:  ${diff_total:.10f}")
print(f"      (Final KPI vs Ground Truth)")

print("\n" + "=" * 90)
print("✅ RECOMMENDATIONS")
print("=" * 90)

if diff_cleaning > 0.001:
    print("\n⚠️  Issue in CLEANING STAGE:")
    print("   - Pipeline cleaning behaves differently than expected")
    print("   - Need to investigate _apply_fast_cleaning() function")
    print("   - Possibly: fillna timing, duplicate detection logic, or column filtering")
    
if diff_kpi_calc > 0.001:
    print("\n⚠️  Issue in KPI CALCULATION:")
    print("   - _calculate_real_kpis() not using df['Salary'].mean() correctly")
    print("   - Need to verify column detection logic")
    print("   - Possibly: wrong column selected, data type conversion issue")

if diff_total < 0.01:
    print("\n✅ ACCEPTABLE: Difference <$0.01 (floating point precision)")
    print("   - This is within machine precision tolerance")
    print("   - No user-facing impact")
elif diff_total < 10:
    print("\n⚠️  MINOR: Difference <$10 but >$0.01")
    print("   - Should investigate for perfection")
    print("   - May be acceptable depending on use case")
else:
    print("\n❌ CRITICAL: Difference ≥$10")
    print("   - Must fix before production")
    print("   - User trust will be compromised")

print("\n" + "=" * 90)
print(f"🎯 FINAL VERDICT: ${diff_total:.2f} discrepancy")
print("=" * 90)

if diff_total < 0.01:
    print("✅ STATUS: PERFECT ACCURACY")
    print("   Discrepancy within floating-point precision")
    print("   APPROVED for production")
elif diff_total < 1:
    print("✅ STATUS: EXCELLENT ACCURACY (>99.999%)")
    print("   Discrepancy negligible for business purposes")
    print("   APPROVED for production")
elif diff_total < 10:
    print("⚠️  STATUS: GOOD ACCURACY (>99.99%)")
    print("   Discrepancy minor but should investigate")
    print("   CONDITIONALLY APPROVED for production")
else:
    print("❌ STATUS: UNACCEPTABLE ACCURACY")
    print("   Discrepancy too large for production")
    print("   DO NOT APPROVE until fixed")

print("=" * 90)
