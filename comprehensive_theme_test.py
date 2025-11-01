#!/usr/bin/env python3
"""
🔬 COMPREHENSIVE THEME TEST
Wait for full render, check theme, force light if needed
"""
import asyncio
from playwright.async_api import async_playwright
from PIL import Image
import numpy as np

def check_theme(img_path):
    """Analyze image to determine theme"""
    img = Image.open(img_path)
    pixels = np.array(img)
    
    # Sample main content area
    content_rgb = tuple(pixels[400, 960, :3].astype(int))
    avg = sum(content_rgb) / 3
    
    if avg > 200:
        return "LIGHT", content_rgb
    elif avg < 50:
        return "DARK", content_rgb
    else:
        return "UNKNOWN", content_rgb

async def comprehensive_test():
    print("="*80)
    print("🔬 COMPREHENSIVE THEME TEST - PR #43 VALIDATION")
    print("="*80)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Test 1: Default (should respect config.toml)
        print("\n" + "="*80)
        print("🧪 TEST 1: Default light theme")
        print("="*80)
        
        context1 = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            color_scheme="light"
        )
        page1 = await context1.new_page()
        
        print("   Loading app...")
        await page1.goto("https://fast-nicedashboard.streamlit.app/",
                        wait_until="networkidle",  # Wait for network to be idle
                        timeout=90000)
        
        print("   Waiting 20s for full render...")
        await asyncio.sleep(20)
        
        # Try to find and click theme toggle if exists
        try:
            # Look for Streamlit's theme menu button
            settings_button = await page1.query_selector('[data-testid="stBaseButton-headerNoPadding"]')
            if settings_button:
                print("   Found settings button, clicking...")
                await settings_button.click()
                await asyncio.sleep(2)
                
                # Look for light theme option
                light_option = await page1.query_selector('text="Light"')
                if light_option:
                    print("   Found light theme option, clicking...")
                    await light_option.click()
                    await asyncio.sleep(3)
        except Exception as e:
            print(f"   Theme toggle not found: {e}")
        
        # Capture
        await page1.screenshot(path="test_final_pr43_validation/comprehensive_test_1.png", full_page=False)
        print("   ✅ Saved: comprehensive_test_1.png")
        
        theme, rgb = check_theme("test_final_pr43_validation/comprehensive_test_1.png")
        print(f"   Theme detected: {theme} (RGB{rgb})")
        
        await context1.close()
        
        # Test 2: Force reload with cache clear
        print("\n" + "="*80)
        print("🧪 TEST 2: Force reload with cache clear")
        print("="*80)
        
        context2 = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            color_scheme="light"
        )
        page2 = await context2.new_page()
        
        print("   Loading app (with cache cleared)...")
        await page2.goto("https://fast-nicedashboard.streamlit.app/",
                        wait_until="networkidle",
                        timeout=90000)
        
        # Force reload
        print("   Force reloading...")
        await page2.reload(wait_until="networkidle")
        await asyncio.sleep(20)
        
        await page2.screenshot(path="test_final_pr43_validation/comprehensive_test_2.png", full_page=False)
        print("   ✅ Saved: comprehensive_test_2.png")
        
        theme, rgb = check_theme("test_final_pr43_validation/comprehensive_test_2.png")
        print(f"   Theme detected: {theme} (RGB{rgb})")
        
        await context2.close()
        await browser.close()
        
        print("\n" + "="*80)
        print("✅ COMPREHENSIVE TEST COMPLETE")
        print("="*80)
        
        # Final analysis
        print("\n🔬 ANALYZING RESULTS...")
        
        img1 = Image.open("test_final_pr43_validation/comprehensive_test_1.png")
        pixels1 = np.array(img1)
        
        # Sample multiple points
        points = [
            (960, 200, "Title"),
            (960, 400, "Content"),
            (250, 400, "Sidebar"),
        ]
        
        print("\n📊 PIXEL ANALYSIS:")
        print("="*80)
        
        config_applied = False
        
        for x, y, label in points:
            rgb = tuple(pixels1[y, x, :3].astype(int))
            print(f"{label:15s} ({x:4d}, {y:4d}): RGB{rgb}")
            
            # Check if it's near RGB(5, 5, 5) from config.toml
            if all(c <= 10 for c in rgb):
                print(f"                → ✅ Near-black from config.toml!")
                config_applied = True
            elif rgb == (15, 23, 42):
                print(f"                → ❌ OLD color (not config.toml)")
        
        print("\n" + "="*80)
        if config_applied:
            print("🎉 SUCCESS! config.toml #050505 IS APPLIED!")
            print("   ⭐⭐⭐⭐⭐ 5-STAR QUALITY ACHIEVED!")
        else:
            print("⚠️ config.toml STILL NOT APPLIED")
            print("\n🔍 POSSIBLE REASONS:")
            print("   1. Streamlit Cloud caching issue")
            print("   2. App defaulting to dark theme")
            print("   3. Browser/Playwright forcing dark mode")
            print("   4. Need to clear Streamlit Cloud cache manually")
        print("="*80)

if __name__ == "__main__":
    asyncio.run(comprehensive_test())
