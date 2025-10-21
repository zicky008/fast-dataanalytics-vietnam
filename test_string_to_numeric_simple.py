#!/usr/bin/env python3
"""
Simple test for string-to-numeric conversion WITHOUT API calls
Tests the fix for P0: KPIs empty due to string numeric columns
"""

import sys
import os
import pandas as pd

# Mock gemini_client to avoid API calls
class MockGeminiClient:
    pass

# Add src to path
sys.path.insert(0, '/home/user/webapp')

from src.premium_lean_pipeline import PremiumLeanPipeline

def test_european_format():
    """Test European CSV format (comma as decimal separator)"""
    print("\n" + "="*60)
    print("TEST: European Format (Comma as Decimal)")
    print("="*60)
    
    # Test data matching user's debug info
    test_data = {
        'Channel_Used': ['Twitter', 'Pinterest', 'Instagram', 'Facebook'],
        'ROI': ['5,43', '0,943785552', '2,27', '4,16'],  # Comma as decimal
        'Spend': ['8311,42', '7762,14', '10376,37', '8332,93'],
        'Clicks': [1250, 890, 1100, 950],
        'Impressions': [25000, 18000, 22000, 19000]
    }
    
    df = pd.DataFrame(test_data)
    
    print("\n📊 Original DataFrame:")
    print(df.head())
    print(f"\nOriginal data types:")
    for col in df.columns:
        print(f"  {col}: {df[col].dtype}")
    
    # Test conversion with mock client
    pipeline = PremiumLeanPipeline(MockGeminiClient())
    df_converted = pipeline._convert_string_to_numeric(df)
    
    print(f"\n✅ Converted data types:")
    for col in df_converted.columns:
        print(f"  {col}: {df_converted[col].dtype}")
    
    print(f"\n✅ Converted values (first 3 rows):")
    print(df_converted.head(3))
    
    # Verify numeric conversion
    assert pd.api.types.is_numeric_dtype(df_converted['ROI']), "ROI should be numeric"
    assert pd.api.types.is_numeric_dtype(df_converted['Spend']), "Spend should be numeric"
    
    # Verify values
    expected_roi_0 = 5.43
    actual_roi_0 = df_converted['ROI'].iloc[0]
    assert abs(actual_roi_0 - expected_roi_0) < 0.01, f"Expected {expected_roi_0}, got {actual_roi_0}"
    
    expected_spend_0 = 8311.42
    actual_spend_0 = df_converted['Spend'].iloc[0]
    assert abs(actual_spend_0 - expected_spend_0) < 0.01, f"Expected {expected_spend_0}, got {actual_spend_0}"
    
    print("\n✅ PASS: European format conversion works correctly!")
    print(f"   ROI: '{test_data['ROI'][0]}' → {actual_roi_0}")
    print(f"   Spend: '{test_data['Spend'][0]}' → {actual_spend_0}")
    
    return True

def test_kpi_detection_logic():
    """Test that KPIs will be detected after conversion"""
    print("\n" + "="*60)
    print("TEST: KPI Detection After Conversion")
    print("="*60)
    
    # Create marketing-like data
    test_data = {
        'Channel_Used': ['Twitter', 'Pinterest', 'Instagram'],
        'ROI': ['5,43', '0,94', '2,27'],
        'Spend': ['8311,42', '7762,14', '10376,37'],
        'Clicks': [1250, 890, 1100],
        'Impressions': [25000, 18000, 22000],
        'Conversions': [45, 32, 38],
        'Conversion_Rate': ['0,07', '0,13', '0,14']
    }
    
    df = pd.DataFrame(test_data)
    
    # Convert
    pipeline = PremiumLeanPipeline(MockGeminiClient())
    df_converted = pipeline._convert_string_to_numeric(df)
    
    # Check numeric columns
    numeric_cols = df_converted.select_dtypes(include=['number']).columns.tolist()
    
    print(f"\n📊 Numeric columns detected: {len(numeric_cols)}")
    for col in numeric_cols:
        print(f"  • {col}")
    
    # Verify expected columns are numeric
    expected_numeric = ['ROI', 'Spend', 'Clicks', 'Impressions', 'Conversions', 'Conversion_Rate']
    
    for col in expected_numeric:
        if col in df_converted.columns:
            is_numeric = pd.api.types.is_numeric_dtype(df_converted[col])
            status = "✅" if is_numeric else "❌"
            print(f"{status} {col}: {df_converted[col].dtype}")
            assert is_numeric, f"{col} should be numeric after conversion"
    
    print(f"\n✅ PASS: All expected columns are numeric!")
    print(f"   This fixes the 'kpis: {{}}' empty issue")
    
    return True

def test_us_format_unchanged():
    """Test that US format (period as decimal) is unchanged"""
    print("\n" + "="*60)
    print("TEST: US Format Unchanged")
    print("="*60)
    
    test_data = {
        'Channel': ['Twitter', 'Facebook'],
        'ROI': [5.43, 2.18],  # Already numeric
        'Cost': [8311.42, 5000.00],
        'Revenue': [45000.00, 10900.00]
    }
    
    df = pd.DataFrame(test_data)
    
    print(f"\n📊 Original (already numeric):")
    print(df)
    print(f"\nOriginal types:")
    print(df.dtypes)
    
    # Convert (should not change)
    pipeline = PremiumLeanPipeline(MockGeminiClient())
    df_converted = pipeline._convert_string_to_numeric(df)
    
    print(f"\n✅ After conversion (should be same):")
    print(df_converted)
    
    # Verify values unchanged
    assert (df['ROI'] == df_converted['ROI']).all(), "ROI should be unchanged"
    assert (df['Cost'] == df_converted['Cost']).all(), "Cost should be unchanged"
    
    print("\n✅ PASS: US format data remains unchanged!")
    
    return True

def main():
    print("\n" + "🧪 STRING-TO-NUMERIC CONVERSION TEST".center(60, "="))
    print("Testing fix for P0: Empty KPIs due to string columns\n")
    
    tests = [
        ("European Format Conversion", test_european_format),
        ("KPI Detection Logic", test_kpi_detection_logic),
        ("US Format Unchanged", test_us_format_unchanged)
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
        print("\n🎉 ALL TESTS PASSED!")
        print("\n📊 This fix resolves:")
        print("   • P0: Empty KPIs ('kpis: {}') due to string columns")
        print("   • European CSV format support (comma as decimal)")
        print("   • Preserves US format data")
        return 0
    else:
        print(f"\n⚠️ {total - passed} test(s) failed.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
