"""
E2E Test - Real User Simulation
Test như một real user thật sự:
1. Open browser
2. Navigate to app
3. Upload CSV file
4. Wait for processing
5. Verify Dashboard displays
6. Download PDF
7. Verify PDF content
"""
import time
import os
from playwright.sync_api import sync_playwright, expect

# App URL
APP_URL = "https://fast-dataanalytics-vietnam.streamlit.app"
TEST_DATA = "sample_data/manufacturing_production_30days.csv"

def test_real_user_workflow():
    """
    Simulate real user workflow - 5-star experience test
    """
    print("\n" + "="*80)
    print("🎭 REAL USER E2E TEST - 5-STAR EXPERIENCE VALIDATION")
    print("="*80)
    
    with sync_playwright() as p:
        print("\n📱 Step 1: Launch browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print(f"🌐 Step 2: Navigate to {APP_URL}...")
        try:
            page.goto(APP_URL, timeout=30000)
            print("✅ App loaded successfully")
        except Exception as e:
            print(f"❌ CRITICAL: Cannot access app - {str(e)}")
            browser.close()
            return False
        
        print("\n📂 Step 3: Upload CSV file...")
        # Wait for file uploader to appear
        try:
            uploader = page.locator('input[type="file"]')
            uploader.set_input_files(TEST_DATA)
            print(f"✅ File '{TEST_DATA}' uploaded")
        except Exception as e:
            print(f"❌ FAIL: Cannot upload file - {str(e)}")
            browser.close()
            return False
        
        print("\n⏳ Step 4: Wait for processing (max 60s)...")
        time.sleep(5)  # Give it time to process
        
        # Check for success message or dashboard
        try:
            # Look for KPI cards or dashboard elements
            page.wait_for_selector("text=Quality Score", timeout=60000)
            print("✅ Dashboard loaded with KPIs")
        except Exception as e:
            print(f"❌ FAIL: Dashboard did not load - {str(e)}")
            
            # Capture error message if visible
            error_text = page.locator("text=Error").text_content() if page.locator("text=Error").count() > 0 else "No error message"
            print(f"🔍 Error details: {error_text}")
            
            # Take screenshot for debugging
            page.screenshot(path="error_screenshot.png")
            print("📸 Screenshot saved: error_screenshot.png")
            
            browser.close()
            return False
        
        print("\n📊 Step 5: Verify Dashboard content...")
        # Check for key elements
        checks = [
            ("Domain detection", "text=Manufacturing"),
            ("Quality Score", "text=Quality Score"),
            ("KPI cards", "[data-testid='stMetric']"),
        ]
        
        passed = 0
        for check_name, selector in checks:
            try:
                element = page.locator(selector).first
                if element.is_visible():
                    print(f"✅ {check_name} visible")
                    passed += 1
                else:
                    print(f"⚠️  {check_name} not visible")
            except:
                print(f"❌ {check_name} not found")
        
        print(f"\n📈 Dashboard checks: {passed}/{len(checks)} passed")
        
        print("\n📥 Step 6: Download PDF...")
        # Click download button if exists
        try:
            download_button = page.locator("text=Download PDF")
            if download_button.count() > 0:
                with page.expect_download() as download_info:
                    download_button.click()
                download = download_info.value
                download_path = f"/tmp/{download.suggested_filename}"
                download.save_as(download_path)
                print(f"✅ PDF downloaded: {download_path}")
                
                # Verify PDF file size
                file_size = os.path.getsize(download_path)
                if file_size > 10000:  # At least 10KB
                    print(f"✅ PDF size valid: {file_size:,} bytes")
                else:
                    print(f"⚠️  PDF too small: {file_size:,} bytes")
            else:
                print("⚠️  Download button not found")
        except Exception as e:
            print(f"⚠️  PDF download failed: {str(e)}")
        
        print("\n🏁 Step 7: Test complete")
        browser.close()
        
        # Final verdict
        success_rate = passed / len(checks)
        if success_rate >= 0.8:
            print("\n✅ 5-STAR EXPERIENCE: PASSED")
            return True
        else:
            print(f"\n❌ NEEDS IMPROVEMENT: Only {success_rate*100:.0f}% checks passed")
            return False

if __name__ == "__main__":
    # Check if sample data exists
    if not os.path.exists(TEST_DATA):
        print(f"❌ ERROR: Sample data '{TEST_DATA}' not found")
        print("Please create sample manufacturing data first")
        exit(1)
    
    try:
        success = test_real_user_workflow()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
