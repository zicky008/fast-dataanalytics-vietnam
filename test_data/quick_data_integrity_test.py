#!/usr/bin/env python3
"""
🎯 QUICK DATA INTEGRITY TEST - Core Protection Validation
Tests NEVER_IMPUTE protection without needing Gemini API

Focus: Validate that critical fields are protected from imputation
"""

import sys
from pathlib import Path
import pandas as pd

# Add project root
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from smart_oqmlb_pipeline import NEVER_IMPUTE_FIELDS

def check_field_protection(field_name: str) -> bool:
    """Check if a field is protected"""
    field_lower = field_name.lower()
    return any(critical in field_lower for critical in NEVER_IMPUTE_FIELDS)

def test_dataset(csv_path: str, persona_name: str):
    """Test one dataset for NEVER_IMPUTE protection"""
    print(f"\n{'='*80}")
    print(f"Testing: {persona_name}")
    print(f"File: {csv_path}")
    print(f"{'='*80}")
    
    df = pd.read_csv(csv_path)
    print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
    
    # Check each column for missing values
    print(f"\nMissing Value Analysis:")
    issues = []
    
    for col in df.columns:
        missing = df[col].isna().sum()
        if missing > 0:
            is_protected = check_field_protection(col)
            status = "✅ PROTECTED" if is_protected else "❌ NOT PROTECTED"
            print(f"  {col}: {missing} missing → {status}")
            if not is_protected and missing > 0:
                issues.append(f"{col} has {missing} missing values but NOT protected")
    
    if issues:
        print(f"\n⚠️  ISSUES FOUND ({len(issues)}):")
        for issue in issues:
            print(f"  • {issue}")
        return False
    else:
        print(f"\n🎉 NO ISSUES: All fields with missing data are properly protected!")
        return True

def main():
    """Run tests on all datasets"""
    datasets = {
        'Chị Mai (HR)': 'test_data/vietnam_hr_data.csv',
        'Anh Tuấn (E-commerce)': 'test_data/vietnam_ecommerce_data.csv',
        'Chị Lan (Marketing)': 'test_data/vietnam_marketing_campaign_data.csv',
        'Anh Hùng (Sales)': 'test_data/vietnam_sales_pipeline_data.csv',
        'Chị Ngọc (Customer Service)': 'test_data/vietnam_customer_service_data.csv',
    }
    
    print(f"""
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║             🎯 QUICK DATA INTEGRITY TEST - NEVER_IMPUTE 🎯                 ║
    ║                                                                           ║
    ║  Testing that critical fields are protected from imputation              ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    print(f"\nNEVER_IMPUTE_FIELDS ({len(NEVER_IMPUTE_FIELDS)} fields):")
    for field in sorted(NEVER_IMPUTE_FIELDS):
        print(f"  • {field}")
    
    results = []
    for persona, path in datasets.items():
        passed = test_dataset(path, persona)
        results.append((persona, passed))
    
    # Summary
    print(f"\n{'='*80}")
    print(f"FINAL SUMMARY")
    print(f"{'='*80}")
    
    for persona, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {persona}: {status}")
    
    all_pass = all(p for _, p in results)
    print(f"\n{'='*80}")
    if all_pass:
        print(f"🎉 ALL TESTS PASSED! Data integrity protected!")
    else:
        print(f"⚠️  SOME TESTS FAILED! Need to fix NEVER_IMPUTE_FIELDS")
    print(f"{'='*80}")
    
    return all_pass

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
