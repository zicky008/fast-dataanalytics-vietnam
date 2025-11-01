#!/usr/bin/env python3
"""
Proper Screenshot Capture Script - Light & Dark Modes
======================================================

This script properly captures screenshots in BOTH modes by:
1. Using Playwright's color_scheme context option to FORCE the mode
2. Waiting sufficient time for Streamlit to fully render
3. Verifying the detected mode by checking background color
4. Capturing multiple scroll positions if needed
5. Logging everything for transparency

User's concerns addressed:
- "Rồi bạn có thực sự chụp màn hình ở chế độ light mode chưa, hay chỉ mới dark mode"
- "check thì check đầy đủ các tabs"
"""

import asyncio
from playwright.async_api import async_playwright
import os
from datetime import datetime

# Production URL
PRODUCTION_URL = "https://fast-nicedashboard.streamlit.app/"

# Output directory
OUTPUT_DIR = "verified_mode_screenshots"

async def capture_mode(mode: str):
    """
    Capture screenshots in a specific mode with verification
    
    Args:
        mode: 'light' or 'dark'
    """
    print(f"\n{'='*60}")
    print(f"CAPTURING {mode.upper()} MODE")
    print(f"{'='*60}")
    
    async with async_playwright() as p:
        # Launch browser with FORCED color scheme
        print(f"🚀 Launching browser with color_scheme='{mode}'...")
        browser = await p.chromium.launch(headless=True)
        
        # Create context with EXPLICIT color scheme preference
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            color_scheme=mode  # FORCE the mode - 'light' or 'dark'
        )
        
        page = await context.new_page()
        
        # Navigate to production URL
        print(f"🌐 Navigating to {PRODUCTION_URL}...")
        await page.goto(PRODUCTION_URL, wait_until="networkidle", timeout=60000)
        
        # Wait for Streamlit to fully render
        print(f"⏳ Waiting 25 seconds for Streamlit to fully render...")
        await asyncio.sleep(25)
        
        # VERIFY the mode by checking background color
        print(f"🔍 Verifying that we're actually in {mode} mode...")
        bg_color = await page.evaluate("""
            () => {
                const body = document.body;
                const computed = window.getComputedStyle(body);
                return computed.backgroundColor;
            }
        """)
        print(f"   Detected background color: {bg_color}")
        
        # Check if background matches expected mode
        if mode == 'light':
            # Light mode should have light background (high RGB values)
            is_light = 'rgb(255' in bg_color or 'rgb(240' in bg_color or 'rgb(250' in bg_color
            print(f"   Is light background? {is_light}")
            if not is_light:
                print(f"   ⚠️  WARNING: Expected light background but got {bg_color}")
        else:  # dark mode
            # Dark mode should have dark background (low RGB values)
            is_dark = 'rgb(14' in bg_color or 'rgb(0' in bg_color or 'rgb(20' in bg_color
            print(f"   Is dark background? {is_dark}")
            if not is_dark:
                print(f"   ⚠️  WARNING: Expected dark background but got {bg_color}")
        
        # Create output directory
        mode_dir = os.path.join(OUTPUT_DIR, mode)
        os.makedirs(mode_dir, exist_ok=True)
        
        # Capture initial view
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(mode_dir, f"01_initial_{timestamp}.png")
        await page.screenshot(path=screenshot_path, full_page=False)
        print(f"✅ Captured: {screenshot_path}")
        
        # Try to capture different tabs if they exist
        # Check for tab buttons
        print(f"🔍 Looking for tabs...")
        tabs = await page.query_selector_all('[role="tab"]')
        
        if tabs:
            print(f"   Found {len(tabs)} tabs")
            for i, tab in enumerate(tabs):
                tab_text = await tab.inner_text()
                print(f"   📑 Clicking tab {i+1}: {tab_text}")
                await tab.click()
                await asyncio.sleep(5)  # Wait for tab content to load
                
                tab_screenshot = os.path.join(mode_dir, f"02_tab_{i+1}_{tab_text.replace(' ', '_')}_{timestamp}.png")
                await page.screenshot(path=tab_screenshot, full_page=False)
                print(f"   ✅ Captured: {tab_screenshot}")
        else:
            print(f"   No tabs found (single-page app)")
        
        # Capture full page scroll
        print(f"📸 Capturing full page...")
        full_page_path = os.path.join(mode_dir, f"03_full_page_{timestamp}.png")
        await page.screenshot(path=full_page_path, full_page=True)
        print(f"✅ Captured: {full_page_path}")
        
        # Check for file uploader and other specific elements
        print(f"🔍 Checking for specific UI elements...")
        
        # File uploader
        uploader = await page.query_selector('[data-testid="stFileUploader"]')
        if uploader:
            print(f"   ✅ Found file uploader")
            await uploader.scroll_into_view_if_needed()
            await asyncio.sleep(2)
            uploader_path = os.path.join(mode_dir, f"04_file_uploader_{timestamp}.png")
            await page.screenshot(path=uploader_path, full_page=False)
            print(f"   📸 Captured: {uploader_path}")
        
        # Metrics/KPIs
        metrics = await page.query_selector_all('[data-testid="stMetric"]')
        if metrics:
            print(f"   ✅ Found {len(metrics)} metrics/KPIs")
            first_metric = metrics[0]
            await first_metric.scroll_into_view_if_needed()
            await asyncio.sleep(2)
            metrics_path = os.path.join(mode_dir, f"05_metrics_{timestamp}.png")
            await page.screenshot(path=metrics_path, full_page=False)
            print(f"   📸 Captured: {metrics_path}")
        
        # Buttons
        buttons = await page.query_selector_all('button')
        if buttons:
            print(f"   ✅ Found {len(buttons)} buttons")
        
        await browser.close()
        print(f"\n✅ {mode.upper()} MODE CAPTURE COMPLETE")

async def main():
    """Capture both light and dark modes"""
    print("\n" + "="*60)
    print("PROPER MODE SCREENSHOT CAPTURE")
    print("="*60)
    print(f"Production URL: {PRODUCTION_URL}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Capture LIGHT mode first
    await capture_mode('light')
    
    # Wait a bit between captures
    await asyncio.sleep(5)
    
    # Capture DARK mode
    await capture_mode('dark')
    
    print("\n" + "="*60)
    print("ALL CAPTURES COMPLETE")
    print("="*60)
    print(f"Check screenshots in: {OUTPUT_DIR}/")
    print(f"  - {OUTPUT_DIR}/light/")
    print(f"  - {OUTPUT_DIR}/dark/")
    print("\nNext: Analyze these screenshots to identify text visibility issues")

if __name__ == "__main__":
    asyncio.run(main())
