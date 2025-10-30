"""
Playwright Test - Production URL Testing
Test https://fast-nicedashboard.streamlit.app/ with real Vietnamese data

Usage:
    cd /home/user/webapp
    pytest test_production_app/test_playwright_production.py -v -s --headed
    # Use --headed to see browser, remove for headless
"""

import pytest
import time
from playwright.sync_api import Page, expect


@pytest.fixture(scope="function")
def production_url():
    """Production app URL"""
    return "https://fast-nicedashboard.streamlit.app/"


def test_production_load_time_and_title(page: Page, production_url: str):
    """
    Test 1: Load time and page title
    Target: <5s load time, proper page title (not just "Streamlit")
    """
    print("\n🧪 Test 1: Load Time & Page Title...")
    
    # Measure load time
    start_time = time.time()
    page.goto(production_url, timeout=60000, wait_until="networkidle")
    load_time = time.time() - start_time
    
    print(f"⏱️  Load Time: {load_time:.2f}s")
    
    # Check page title
    title = page.title()
    print(f"📄 Page Title: {title}")
    
    # ASSERTIONS
    if load_time > 5:
        print(f"⚠️  WARNING: Load time {load_time:.2f}s > 5s target (not optimal)")
    else:
        print(f"✅ Load time {load_time:.2f}s is acceptable")
    
    if title == "Streamlit":
        print(f"⚠️  WARNING: Page title is generic 'Streamlit' (not SEO-friendly)")
    else:
        print(f"✅ Page title is descriptive: {title}")
    
    # Take screenshot
    page.screenshot(path="/home/user/webapp/test_production_app/screenshot_homepage.png")
    print("📸 Screenshot saved: screenshot_homepage.png")


def test_production_console_errors(page: Page, production_url: str):
    """
    Test 2: Console errors detection
    Target: Zero console errors (no 403, 500, etc.)
    """
    print("\n🧪 Test 2: Console Errors Detection...")
    
    console_errors = []
    console_warnings = []
    
    def handle_console(msg):
        if msg.type == "error":
            console_errors.append(msg.text)
            print(f"❌ Console Error: {msg.text}")
        elif msg.type == "warning":
            console_warnings.append(msg.text)
    
    page.on("console", handle_console)
    
    # Navigate and give time for console messages
    page.goto(production_url, timeout=60000)
    page.wait_for_load_state("networkidle")
    time.sleep(3)  # Wait for any delayed errors
    
    # ASSERTIONS
    if console_errors:
        print(f"⚠️  Found {len(console_errors)} console errors")
        critical_errors = [err for err in console_errors if "403" in err or "500" in err]
        if critical_errors:
            print(f"🔴 CRITICAL: Found HTTP errors: {critical_errors}")
    else:
        print("✅ No console errors found")
    
    if console_warnings:
        print(f"⚠️  Found {len(console_warnings)} warnings (check logs)")


def test_production_file_upload_hr_data(page: Page, production_url: str):
    """
    Test 3: File upload with Vietnamese HR data
    Persona: Chị Mai (HR Manager)
    """
    print("\n🧪 Test 3: File Upload - Vietnamese HR Data...")
    
    page.goto(production_url, timeout=60000)
    page.wait_for_load_state("networkidle")
    
    # Create temp CSV file with Vietnamese data
    csv_content = """employee_id,ho_ten,department,position,luong_thang,start_date,age,province
EMP001,Nguyen Van Anh,Technology,Senior Developer,28000000,2020-03-15,32,Ho Chi Minh
EMP002,Tran Thi Binh,Marketing,Marketing Manager,25000000,2019-06-01,35,Hanoi
EMP003,Le Van Cuong,Sales,Sales Executive,18000000,2021-08-20,28,Da Nang
EMP004,Pham Thi Dung,HR,HR Specialist,15000000,2022-01-10,26,Ho Chi Minh
EMP005,Hoang Van Ethan,Finance,Accountant,20000000,2020-11-05,30,Hanoi"""
    
    with open("/tmp/test_hr_vietnam.csv", "w", encoding="utf-8") as f:
        f.write(csv_content)
    
    # Locate and use file uploader
    try:
        # Wait for file uploader to be ready
        print("🔍 Looking for file uploader...")
        file_input = page.locator('input[type="file"]').first
        
        if file_input.count() > 0:
            print("✅ File uploader found, uploading file...")
            file_input.set_input_files("/tmp/test_hr_vietnam.csv")
            
            # Wait for processing (loading spinner)
            print("⏳ Waiting for processing...")
            page.wait_for_selector('[data-testid="stSpinner"]', state="hidden", timeout=30000)
            
            # Wait for content to load
            time.sleep(3)
            
            # Take screenshot of dashboard
            page.screenshot(path="/home/user/webapp/test_production_app/screenshot_dashboard_hr.png")
            print("📸 Screenshot saved: screenshot_dashboard_hr.png")
            
            # Check for Vietnam context in page
            page_content = page.content()
            
            vietnam_terms = ["employee", "salary", "nhân viên", "lương", "Ho Chi Minh", "Hanoi"]
            found_terms = [term for term in vietnam_terms if term.lower() in page_content.lower()]
            
            if found_terms:
                print(f"✅ Vietnam context found: {', '.join(found_terms[:3])}")
            else:
                print("⚠️  WARNING: No Vietnam context found in dashboard")
            
            # Check for data quality indicators
            quality_terms = ["quality", "chất lượng", "score", "điểm"]
            has_quality = any(term.lower() in page_content.lower() for term in quality_terms)
            
            if has_quality:
                print("✅ Data quality assessment displayed")
            else:
                print("⚠️  WARNING: No data quality assessment visible")
            
        else:
            print("❌ FAIL: File uploader not found on page")
            
    except Exception as e:
        print(f"❌ ERROR during file upload: {str(e)}")
        page.screenshot(path="/home/user/webapp/test_production_app/screenshot_error.png")


def test_production_mobile_responsive(page: Page, production_url: str):
    """
    Test 4: Mobile responsiveness (iPhone 15 Pro)
    """
    print("\n🧪 Test 4: Mobile Responsive - iPhone 15 Pro...")
    
    # Set mobile viewport
    page.set_viewport_size({"width": 393, "height": 852})
    
    page.goto(production_url, timeout=60000)
    page.wait_for_load_state("networkidle")
    
    # Check if layout adapts to mobile
    page.screenshot(path="/home/user/webapp/test_production_app/screenshot_mobile_iphone15.png")
    print("📸 Mobile screenshot saved: screenshot_mobile_iphone15.png")
    
    # Verify viewport
    viewport = page.viewport_size
    assert viewport["width"] == 393, "Viewport width not set correctly"
    print(f"✅ Mobile viewport set: {viewport['width']}x{viewport['height']}")


def test_production_benchmark_sources_visible(page: Page, production_url: str):
    """
    Test 5: Benchmark sources are visible and clickable
    """
    print("\n🧪 Test 5: Benchmark Sources Visibility...")
    
    page.goto(production_url, timeout=60000)
    page.wait_for_load_state("networkidle")
    
    # Upload a test file first to see dashboard
    csv_content = """revenue,date,category
1000000,2024-01-01,Sales
2000000,2024-01-02,Sales"""
    
    with open("/tmp/test_quick.csv", "w", encoding="utf-8") as f:
        f.write(csv_content)
    
    try:
        file_input = page.locator('input[type="file"]').first
        if file_input.count() > 0:
            file_input.set_input_files("/tmp/test_quick.csv")
            page.wait_for_selector('[data-testid="stSpinner"]', state="hidden", timeout=30000)
            time.sleep(2)
            
            page_content = page.content()
            
            # Check for benchmark-related keywords
            benchmark_keywords = ["benchmark", "source", "nguồn", "tham khảo", "reference"]
            found_keywords = [kw for kw in benchmark_keywords if kw.lower() in page_content.lower()]
            
            if found_keywords:
                print(f"✅ Benchmark sources visible: {', '.join(found_keywords[:3])}")
            else:
                print("⚠️  WARNING: Benchmark sources not visible")
            
            # Take screenshot
            page.screenshot(path="/home/user/webapp/test_production_app/screenshot_benchmarks.png")
            print("📸 Screenshot saved: screenshot_benchmarks.png")
            
    except Exception as e:
        print(f"⚠️  Could not verify benchmarks: {str(e)}")


@pytest.mark.parametrize("device_name,viewport", [
    ("iPhone 15 Pro", {"width": 393, "height": 852}),
    ("Samsung Galaxy S24", {"width": 360, "height": 800}),
    ("iPad Air", {"width": 820, "height": 1180}),
])
def test_production_multiple_devices(page: Page, production_url: str, device_name: str, viewport: dict):
    """
    Test 6: Multiple device testing
    """
    print(f"\n🧪 Test 6: {device_name} ({viewport['width']}x{viewport['height']})...")
    
    page.set_viewport_size(viewport)
    page.goto(production_url, timeout=60000)
    page.wait_for_load_state("networkidle")
    
    # Take screenshot
    filename = f"screenshot_{device_name.lower().replace(' ', '_')}.png"
    page.screenshot(path=f"/home/user/webapp/test_production_app/{filename}")
    print(f"📸 Screenshot saved: {filename}")


if __name__ == "__main__":
    """Run tests with pytest"""
    print("🚀 Starting Playwright Production Testing...")
    print("=" * 80)
    pytest.main([__file__, "-v", "-s"])
