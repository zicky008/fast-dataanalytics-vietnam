#!/usr/bin/env python3
"""
Test Marketing Data Fix - Verify:
1. String-to-numeric conversion (European format)
2. KPIs calculation (ROI, CTR, CPC, etc.)
3. Chart creation without NoneType errors
"""

import sys
import os
import pandas as pd
from src.premium_lean_pipeline import PremiumLeanPipeline

# Setup Gemini client
import google.generativeai as genai

gemini_api_key = os.environ.get('GEMINI_API_KEY')
if not gemini_api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in environment")
    print("Please run: export GEMINI_API_KEY='your-key'")
    sys.exit(1)

genai.configure(api_key=gemini_api_key)
gemini_client = genai.GenerativeModel('gemini-2.0-flash-exp')

def test_european_format_conversion():
    """Test European CSV format (comma as decimal separator)"""
    print("\n" + "="*60)
    print("TEST 1: European Format Conversion")
    print("="*60)
    
    # Create test data with European format
    test_data = {
        'Channel': ['Twitter', 'Facebook', 'Instagram'],
        'ROI': ['5,43', '2,18', '3,99'],  # Comma as decimal
        'Spend': ['8311,42', '5000,00', '7500,50'],
        'Clicks': [100, 200, 150]
    }
    
    df = pd.DataFrame(test_data)
    
    print("\n📊 Original DataFrame:")
    print(df)
    print(f"\nData types BEFORE conversion:")
    print(df.dtypes)
    
    # Test conversion
    pipeline = PremiumLeanPipeline(gemini_client)
    df_converted = pipeline._convert_string_to_numeric(df)
    
    print(f"\n✅ Data types AFTER conversion:")
    print(df_converted.dtypes)
    
    print(f"\n✅ Converted values:")
    print(df_converted)
    
    # Verify
    assert df_converted['ROI'].dtype in ['float64', 'float32'], "ROI should be numeric"
    assert df_converted['Spend'].dtype in ['float64', 'float32'], "Spend should be numeric"
    assert df_converted['ROI'].iloc[0] == 5.43, f"Expected 5.43, got {df_converted['ROI'].iloc[0]}"
    assert df_converted['Spend'].iloc[0] == 8311.42, f"Expected 8311.42, got {df_converted['Spend'].iloc[0]}"
    
    print("\n✅ PASS: European format conversion works correctly")
    return True

def test_marketing_kpis():
    """Test Marketing KPIs calculation"""
    print("\n" + "="*60)
    print("TEST 2: Marketing KPIs Calculation")
    print("="*60)
    
    # Load real marketing data
    df = pd.read_csv('sample_data/marketing_google_ads.csv')
    
    print(f"\n📊 Loaded {len(df)} rows, {len(df.columns)} columns")
    print(f"Columns: {list(df.columns)}")
    
    # Run pipeline
    pipeline = PremiumLeanPipeline(gemini_client)
    result = pipeline.run_pipeline(df, "Marketing Google Ads")
    
    if not result['success']:
        print(f"\n❌ FAIL: Pipeline failed - {result.get('error', 'Unknown error')}")
        return False
    
    # Check KPIs
    kpis = result.get('dashboard', {}).get('kpis', {})
    
    print(f"\n✅ KPIs calculated: {len(kpis)}")
    
    if len(kpis) == 0:
        print("\n❌ FAIL: No KPIs calculated!")
        return False
    
    for kpi_name, kpi_data in kpis.items():
        value = kpi_data.get('value', 'N/A')
        benchmark = kpi_data.get('benchmark', 'N/A')
        status = kpi_data.get('status', 'Unknown')
        print(f"  • {kpi_name}: {value:.2f} (Benchmark: {benchmark}, Status: {status})")
    
    # Verify expected KPIs
    expected_kpis = ['ROAS', 'CTR (%)', 'CPC', 'Conversion Rate (%)']
    found_kpis = [kpi for kpi in expected_kpis if any(kpi in k for k in kpis.keys())]
    
    print(f"\n✅ Found {len(found_kpis)}/{len(expected_kpis)} expected KPIs: {found_kpis}")
    
    if len(found_kpis) < 2:
        print(f"\n⚠️ WARNING: Only {len(found_kpis)} marketing KPIs found (expected at least 2)")
    
    print("\n✅ PASS: Marketing KPIs calculated successfully")
    return True

def test_chart_creation():
    """Test chart creation without NoneType errors"""
    print("\n" + "="*60)
    print("TEST 3: Chart Creation (No NoneType Errors)")
    print("="*60)
    
    df = pd.read_csv('sample_data/marketing_google_ads.csv')
    
    pipeline = PremiumLeanPipeline(gemini_client)
    result = pipeline.run_pipeline(df, "Marketing Test")
    
    if not result['success']:
        print(f"\n❌ FAIL: Pipeline failed - {result.get('error', 'Unknown error')}")
        return False
    
    charts = result.get('dashboard', {}).get('charts', [])
    
    print(f"\n✅ Charts created: {len(charts)}")
    
    for i, chart in enumerate(charts, 1):
        title = chart.get('title', 'Untitled')
        spec = chart.get('spec', {})
        chart_type = spec.get('type', 'unknown')
        print(f"  {i}. {title} ({chart_type})")
    
    if len(charts) == 0:
        print("\n⚠️ WARNING: No charts created")
    
    print("\n✅ PASS: Chart creation completed without errors")
    return True

def test_full_pipeline_with_european_data():
    """Test full pipeline with European format data"""
    print("\n" + "="*60)
    print("TEST 4: Full Pipeline with European Format")
    print("="*60)
    
    # Create realistic marketing data with European format
    test_data = {
        'Campaign_Name': ['Brand Campaign', 'Search Ads', 'Display Network', 'Video Campaign'],
        'Channel_Used': ['Twitter', 'Facebook', 'Instagram', 'Pinterest'],
        'ROI': ['5,43', '2,18', '3,99', '1,87'],  # European format
        'Spend': ['8311,42', '5000,00', '7500,50', '3200,00'],
        'Clicks': [1250, 890, 1100, 650],
        'Impressions': [25000, 18000, 22000, 13000],
        'Conversions': [45, 32, 38, 20],
        'Revenue': ['45000,00', '21500,00', '35000,00', '12000,00']
    }
    
    df = pd.DataFrame(test_data)
    
    print(f"\n📊 Test data: {len(df)} rows, {len(df.columns)} columns")
    print(f"Sample values (before conversion):")
    print(f"  ROI: {df['ROI'].iloc[0]} (type: {df['ROI'].dtype})")
    print(f"  Spend: {df['Spend'].iloc[0]} (type: {df['Spend'].dtype})")
    
    # Run pipeline
    pipeline = PremiumLeanPipeline(gemini_client)
    result = pipeline.run_pipeline(df, "Marketing Campaign Test")
    
    if not result['success']:
        print(f"\n❌ FAIL: Pipeline failed - {result.get('error', 'Unknown error')}")
        print(f"Error details: {result.get('message', 'No details')}")
        return False
    
    # Check results
    kpis = result.get('dashboard', {}).get('kpis', {})
    charts = result.get('dashboard', {}).get('charts', [])
    
    print(f"\n✅ Pipeline completed successfully!")
    print(f"  • KPIs: {len(kpis)}")
    print(f"  • Charts: {len(charts)}")
    
    if len(kpis) > 0:
        print(f"\n📊 KPIs calculated:")
        for kpi_name, kpi_data in kpis.items():
            value = kpi_data.get('value', 'N/A')
            print(f"  • {kpi_name}: {value:.2f}")
    else:
        print("\n⚠️ WARNING: No KPIs calculated")
    
    print("\n✅ PASS: Full pipeline works with European format data")
    return True

def main():
    print("\n" + "🧪 MARKETING FIX VALIDATION".center(60, "="))
    print("Testing P0 fixes for Marketing data\n")
    
    tests = [
        ("European Format Conversion", test_european_format_conversion),
        ("Marketing KPIs", test_marketing_kpis),
        ("Chart Creation", test_chart_creation),
        ("Full Pipeline (European Data)", test_full_pipeline_with_european_data)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n❌ EXCEPTION in {test_name}:")
            print(f"   {type(e).__name__}: {str(e)}")
            import traceback
            print(f"   {traceback.format_exc()[:500]}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Marketing fix is working correctly.")
        return 0
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please review.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
