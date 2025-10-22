"""
Test Manufacturing Domain Detection Fix
Verify that manufacturing data is correctly detected
"""

import pandas as pd
import sys
sys.path.insert(0, 'src')

from domain_detection import detect_domain

# Load manufacturing sample data
df = pd.read_csv("sample_data/manufacturing_production_30days.csv")

print("=" * 80)
print("🧪 TESTING MANUFACTURING DOMAIN DETECTION")
print("=" * 80 + "\n")

print(f"📊 Data Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"📋 Columns: {', '.join(df.columns[:5])}...\n")

# Test domain detection
result = detect_domain(df, dataset_description="Manufacturing production data")

print("🔍 DOMAIN DETECTION RESULTS:")
print(f"   Domain: {result['domain']}")
print(f"   Domain Name: {result['domain_name']}")
print(f"   Confidence: {result['confidence']*100:.1f}%")
print(f"   Expert Role: {result['expert_role']}")
print(f"   Reasoning: {result['reasoning']}\n")

print("📊 KEY KPIs:")
for kpi in result['key_kpis']:
    print(f"   • {kpi}")

print("\n🎯 BENCHMARKS:")
for key, value in result['benchmarks'].items():
    print(f"   • {key}: {value}")

# Validation
print("\n" + "=" * 80)
print("✅ VALIDATION")
print("=" * 80)

if result['domain'] == 'manufacturing':
    print("✅ PASS: Domain correctly detected as 'manufacturing'")
else:
    print(f"❌ FAIL: Expected 'manufacturing', got '{result['domain']}'")

if result['confidence'] >= 0.2:
    print(f"✅ PASS: Confidence {result['confidence']*100:.1f}% >= 20%")
else:
    print(f"❌ FAIL: Confidence {result['confidence']*100:.1f}% < 20%")

if 'operations manager' in result['expert_role'].lower():
    print("✅ PASS: Expert role is Operations Manager")
else:
    print(f"⚠️  WARNING: Expected 'Operations Manager', got '{result['expert_role']}'")

if 'OEE' in result['key_kpis'] or 'Overall Equipment Effectiveness' in str(result['key_kpis']):
    print("✅ PASS: OEE found in key KPIs")
else:
    print("❌ FAIL: OEE not found in key KPIs")

print("\n" + "=" * 80)
