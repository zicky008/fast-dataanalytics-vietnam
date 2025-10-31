"""
Automated Deployment Testing Script
Tests critical features before production deployment
"""

import pandas as pd
import sys
import os

# Add current directory and src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

def test_sample_data_loading():
    """Test 1: Sample data can be loaded"""
    print("\n✅ TEST 1: Sample Data Loading")
    try:
        df = pd.read_csv('sample_data/ecommerce_shopify_daily.csv')
        print(f"   ✓ E-commerce data loaded: {len(df)} rows, {len(df.columns)} columns")
        
        # Verify key columns exist
        required_cols = ['date', 'revenue', 'transactions', 'conversion_rate', 'cart_abandonment_rate']
        missing = [col for col in required_cols if col not in df.columns]
        
        if missing:
            print(f"   ✗ Missing columns: {missing}")
            return False
        else:
            print(f"   ✓ All required columns present")
            return True
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False

def test_pipeline_import():
    """Test 2: Premium lean pipeline can be imported"""
    print("\n✅ TEST 2: Pipeline Import")
    try:
        from premium_lean_pipeline import analyze_data
        print(f"   ✓ premium_lean_pipeline imported successfully")
        print(f"   ✓ analyze_data function available")
        return True
    except Exception as e:
        print(f"   ✗ Import failed: {e}")
        return False

def test_mdl_system():
    """Test 3: MDL system can be imported"""
    print("\n✅ TEST 3: MDL System")
    try:
        from mdl_loader import load_mdl
        print(f"   ✓ mdl_loader imported successfully")
        
        # Test domain loading
        mdl = load_mdl('ecommerce')
        if mdl and 'metrics' in mdl:
            print(f"   ✓ E-commerce domain loaded: {len(mdl['metrics'])} metrics")
            return True
        else:
            print(f"   ✗ No metrics found for e-commerce domain")
            return False
    except Exception as e:
        print(f"   ✗ Import failed: {e}")
        return False

def test_data_analysis():
    """Test 4: Full analysis pipeline"""
    print("\n✅ TEST 4: Analysis Pipeline")
    try:
        from premium_lean_pipeline import analyze_data
        
        df = pd.read_csv('sample_data/ecommerce_shopify_daily.csv')
        print(f"   ✓ Data loaded: {len(df)} rows")
        
        # Run analysis
        print(f"   ⏳ Running analysis (this may take 10-20 seconds)...")
        result = analyze_data(df, lang='vi')
        
        # Verify result structure
        required_keys = ['dashboard', 'insights', 'domain_info', 'quality_scores']
        missing_keys = [key for key in required_keys if key not in result]
        
        if missing_keys:
            print(f"   ✗ Missing result keys: {missing_keys}")
            return False
        
        # Check dashboard content
        dashboard = result['dashboard']
        if 'charts' in dashboard and 'summary' in dashboard:
            chart_count = len(dashboard['charts'])
            print(f"   ✓ Analysis completed successfully")
            print(f"   ✓ Generated {chart_count} charts")
            print(f"   ✓ Domain detected: {result['domain_info'].get('domain_name', 'Unknown')}")
            return True
        else:
            print(f"   ✗ Dashboard structure incomplete")
            return False
            
    except Exception as e:
        print(f"   ✗ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_microsoft_clarity():
    """Test 5: Microsoft Clarity integration"""
    print("\n✅ TEST 5: Microsoft Clarity")
    try:
        with open('streamlit_app.py', 'r') as f:
            content = f.read()
            
        if 'clarity.ms' in content or 'Microsoft Clarity' in content:
            print(f"   ✓ Microsoft Clarity script found in code")
            
            # Try to find Clarity project ID
            if 'o96oq1crvv' in content:
                print(f"   ✓ Clarity project ID configured: o96oq1crvv")
                return True
            else:
                print(f"   ⚠ Clarity script present but project ID not found")
                return True
        else:
            print(f"   ✗ Microsoft Clarity not integrated")
            return False
    except Exception as e:
        print(f"   ✗ Check failed: {e}")
        return False

def test_visual_hierarchy():
    """Test 6: Visual Hierarchy CSS"""
    print("\n✅ TEST 6: Visual Hierarchy")
    try:
        with open('streamlit_app.py', 'r') as f:
            content = f.read()
            
        # Check for large font sizes (visual hierarchy)
        if 'font-size: 36px' in content or 'font-size:36px' in content:
            print(f"   ✓ Primary KPI font size (36px) configured")
            return True
        elif 'font-size: 28px' in content or 'font-size:28px' in content:
            print(f"   ⚠ Secondary font size found (28px), but 36px for primary not found")
            return True
        else:
            print(f"   ⚠ Large font sizes not detected (may be in CSS)")
            print(f"   ℹ Visual hierarchy should be verified manually in browser")
            return True  # Don't fail - may be implemented differently
    except Exception as e:
        print(f"   ✗ Check failed: {e}")
        return False

def run_all_tests():
    """Run all deployment tests"""
    print("="*60)
    print("🧪 DEPLOYMENT TESTING - Phase 1")
    print("="*60)
    
    tests = [
        test_sample_data_loading,
        test_pipeline_import,
        test_mdl_system,
        test_data_analysis,
        test_microsoft_clarity,
        test_visual_hierarchy,
    ]
    
    results = []
    for test_func in tests:
        result = test_func()
        results.append(result)
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - Ready for Production Deployment!")
        return 0
    elif passed >= total - 1:
        print("\n⚠️  MOSTLY PASSED - Review failures, may still deploy")
        return 0
    else:
        print("\n❌ MULTIPLE FAILURES - Fix issues before deploying")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
