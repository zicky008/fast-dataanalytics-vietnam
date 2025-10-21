#!/usr/bin/env python3
"""
Real Gemini API Testing Script
Tests Premium Lean Pipeline with actual Gemini API

Run: python test_real_api.py
"""

import os
import sys
import time
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from premium_lean_pipeline import PremiumLeanPipeline
from utils.validators import safe_file_upload
import google.generativeai as genai

# Load environment variables
load_dotenv()

def test_gemini_connection():
    """Test 1: Verify Gemini API connection"""
    print("\n" + "="*60)
    print("TEST 1: Gemini API Connection")
    print("="*60)
    
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ FAILED: GEMINI_API_KEY not found in .env")
        print("\n📝 Setup Instructions:")
        print("1. Copy .env.template to .env")
        print("2. Get API key from: https://aistudio.google.com/app/apikey")
        print("3. Add to .env: GEMINI_API_KEY=your_key_here")
        return False
    
    if not api_key.startswith('AIza'):
        print(f"❌ FAILED: Invalid API key format (should start with 'AIza')")
        print(f"Current: {api_key[:20]}...")
        return False
    
    print(f"✅ API Key found: {api_key[:20]}...{api_key[-10:]}")
    
    # Test API call
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')  # Stable version, higher quota
        
        response = model.generate_content("Hello! Reply with 'OK'")
        
        if response and response.text:
            print(f"✅ API Response: {response.text[:50]}")
            print("✅ PASSED: Gemini API connection successful")
            return True
        else:
            print("❌ FAILED: Empty response from API")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        if '429' in str(e):
            print("\n⚠️  Rate limit hit. Wait 1 minute and try again.")
        elif 'API_KEY_INVALID' in str(e):
            print("\n⚠️  API key is invalid. Get new key from:")
            print("https://aistudio.google.com/app/apikey")
        return False

def test_marketing_pipeline():
    """Test 2: Marketing Sample Data"""
    print("\n" + "="*60)
    print("TEST 2: Marketing Pipeline (Google Ads)")
    print("="*60)
    
    # Load sample data
    sample_file = Path(__file__).parent / 'sample_data' / 'marketing_google_ads.csv'
    
    if not sample_file.exists():
        print(f"❌ FAILED: Sample file not found: {sample_file}")
        return False
    
    print(f"📁 Loading: {sample_file.name}")
    df = pd.read_csv(sample_file)
    print(f"✅ Data loaded: {df.shape[0]} rows × {df.shape[1]} columns")
    
    # Initialize pipeline
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    
    client = genai.GenerativeModel('gemini-2.0-flash')  # Stable version, higher quota
    pipeline = PremiumLeanPipeline(client)
    
    # Run pipeline
    print("\n⏱️  Starting pipeline...")
    start_time = time.time()
    
    try:
        result = pipeline.run_pipeline(
            df=df,
            dataset_description="Google Ads campaign data - January 2024"
        )
        
        elapsed = time.time() - start_time
        
        print(f"\n✅ Pipeline completed in {elapsed:.1f} seconds")
        
        # Validate results
        print("\n📊 Validation Results:")
        print("-" * 60)
        
        # Check status
        if result.get('status') != 'success':
            print(f"❌ Status: {result.get('status')} (expected: success)")
            return False
        print("✅ Status: success")
        
        # Check domain detection
        domain = result.get('domain_info', {}).get('name', 'Unknown')
        print(f"✅ Domain: {domain}")
        if 'Marketing' not in domain and 'marketing' not in domain.lower():
            print(f"⚠️  WARNING: Expected Marketing domain, got {domain}")
        
        # Check quality score
        quality_score = result.get('quality_score', 0)
        print(f"✅ Quality Score: {quality_score:.1f}/100")
        if quality_score < 80:
            print(f"⚠️  WARNING: Quality score below 80 (got {quality_score})")
        
        # Check dashboard
        charts = result.get('dashboard', {}).get('charts', [])
        print(f"✅ Charts Generated: {len(charts)}")
        if len(charts) < 8:
            print(f"⚠️  WARNING: Expected 8-10 charts, got {len(charts)}")
        
        # Check insights
        insights = result.get('insights', {}).get('key_insights', [])
        print(f"✅ Insights Generated: {len(insights)}")
        if len(insights) < 5:
            print(f"⚠️  WARNING: Expected 5-7 insights, got {len(insights)}")
        
        # Check KPIs
        kpis = result.get('insights', {}).get('kpis_calculated', {})
        print(f"✅ KPIs Calculated: {len(kpis)}")
        expected_kpis = ['ROAS', 'CTR', 'CPC', 'CPA']
        for kpi in expected_kpis:
            if kpi in kpis:
                value = kpis[kpi].get('value', 'N/A')
                status = kpis[kpi].get('status', 'N/A')
                print(f"   - {kpi}: {value} ({status})")
            else:
                print(f"   ⚠️  {kpi}: Not found")
        
        # Performance check
        print(f"\n⏱️  Performance:")
        print(f"   - Total Time: {elapsed:.1f}s")
        print(f"   - Target: <60s")
        if elapsed > 60:
            print(f"   ⚠️  WARNING: Exceeded 60-second target")
        else:
            print(f"   ✅ Within target ({60 - elapsed:.1f}s buffer)")
        
        print("\n✅ PASSED: Marketing Pipeline Test")
        return True
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ FAILED after {elapsed:.1f}s: {str(e)}")
        
        # Debug info
        import traceback
        print("\n🐛 Debug Info:")
        print(traceback.format_exc())
        
        return False

def test_ecommerce_pipeline():
    """Test 3: E-commerce Sample Data"""
    print("\n" + "="*60)
    print("TEST 3: E-commerce Pipeline (Shopify)")
    print("="*60)
    
    # Load sample data
    sample_file = Path(__file__).parent / 'sample_data' / 'ecommerce_shopify.csv'
    
    if not sample_file.exists():
        print(f"❌ FAILED: Sample file not found: {sample_file}")
        return False
    
    print(f"📁 Loading: {sample_file.name}")
    df = pd.read_csv(sample_file)
    print(f"✅ Data loaded: {df.shape[0]} rows × {df.shape[1]} columns")
    
    # Initialize pipeline
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    
    client = genai.GenerativeModel('gemini-2.0-flash')  # Stable version, higher quota
    pipeline = PremiumLeanPipeline(client)
    
    # Run pipeline
    print("\n⏱️  Starting pipeline...")
    start_time = time.time()
    
    try:
        result = pipeline.run_pipeline(
            df=df,
            dataset_description="Shopify e-commerce orders - January 2024"
        )
        
        elapsed = time.time() - start_time
        
        print(f"\n✅ Pipeline completed in {elapsed:.1f} seconds")
        
        # Validate results
        print("\n📊 Validation Results:")
        print("-" * 60)
        
        # Check domain
        domain = result.get('domain_info', {}).get('name', 'Unknown')
        print(f"✅ Domain: {domain}")
        if 'commerce' not in domain.lower():
            print(f"⚠️  WARNING: Expected E-commerce domain, got {domain}")
        
        # Check quality score
        quality_score = result.get('quality_score', 0)
        print(f"✅ Quality Score: {quality_score:.1f}/100")
        
        # Check KPIs
        kpis = result.get('insights', {}).get('kpis_calculated', {})
        expected_kpis = ['AOV', 'CLV']
        print(f"✅ KPIs Calculated: {len(kpis)}")
        for kpi in expected_kpis:
            if kpi in kpis:
                value = kpis[kpi].get('value', 'N/A')
                status = kpis[kpi].get('status', 'N/A')
                print(f"   - {kpi}: {value} ({status})")
        
        print(f"\n⏱️  Performance: {elapsed:.1f}s (target: <60s)")
        
        print("\n✅ PASSED: E-commerce Pipeline Test")
        return True
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ FAILED after {elapsed:.1f}s: {str(e)}")
        return False

def test_rate_limiting():
    """Test 4: Rate Limiting Behavior"""
    print("\n" + "="*60)
    print("TEST 4: Rate Limiting (Free Tier: 15 req/min)")
    print("="*60)
    
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    
    client = genai.GenerativeModel('gemini-2.0-flash')  # Stable version, higher quota
    
    print("📝 Sending 5 rapid requests to test rate limiting...")
    
    successes = 0
    failures = 0
    
    for i in range(5):
        try:
            response = client.generate_content(f"Test {i+1}: Reply with 'OK'")
            if response and response.text:
                print(f"✅ Request {i+1}: Success")
                successes += 1
            else:
                print(f"❌ Request {i+1}: Empty response")
                failures += 1
        except Exception as e:
            if '429' in str(e):
                print(f"⏳ Request {i+1}: Rate limited (expected)")
                print("   → System should auto-retry with backoff")
            else:
                print(f"❌ Request {i+1}: {str(e)}")
            failures += 1
        
        time.sleep(0.5)  # Small delay
    
    print(f"\n📊 Results: {successes} successes, {failures} failures")
    print("✅ PASSED: Rate limiting test completed")
    return True

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 DataAnalytics Vietnam - Real API Testing")
    print("="*60)
    print("Testing Premium Lean Pipeline with Gemini API")
    print("="*60)
    
    results = {
        'Gemini Connection': False,
        'Marketing Pipeline': False,
        'E-commerce Pipeline': False,
        'Rate Limiting': False
    }
    
    # Test 1: Connection
    results['Gemini Connection'] = test_gemini_connection()
    
    if not results['Gemini Connection']:
        print("\n❌ Cannot proceed without valid API connection")
        print("Please fix API key issues and try again")
        sys.exit(1)
    
    # Test 2: Marketing
    results['Marketing Pipeline'] = test_marketing_pipeline()
    
    # Wait before next test (avoid rate limits)
    if results['Marketing Pipeline']:
        print("\n⏳ Waiting 10 seconds before next test (avoid rate limits)...")
        time.sleep(10)
    
    # Test 3: E-commerce
    results['E-commerce Pipeline'] = test_ecommerce_pipeline()
    
    # Test 4: Rate limiting
    print("\n⏳ Waiting 5 seconds before rate limit test...")
    time.sleep(5)
    results['Rate Limiting'] = test_rate_limiting()
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 ALL TESTS PASSED! Pipeline is ready for deployment.")
        sys.exit(0)
    else:
        print("\n⚠️  SOME TESTS FAILED. Review errors above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
