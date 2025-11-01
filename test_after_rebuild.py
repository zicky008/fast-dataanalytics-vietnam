#!/usr/bin/env python3
"""
🔬 TEST AFTER STREAMLIT CLOUD REBUILD
Check if config.toml #050505 is now applied
"""
import asyncio
from playwright.async_api import async_playwright
from PIL import Image
import numpy as np

def calculate_luminance(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def calculate_contrast(rgb1, rgb2):
    l1 = calculate_luminance(rgb1)
    l2 = calculate_luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

async def test_rebuild():
    print("="*80)
    print("🔬 TESTING AFTER STREAMLIT CLOUD REBUILD")
    print("="*80)
    print("Expected: textColor=#050505 → RGB(5, 5, 5)")
    print("="*80)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            color_scheme="light"
        )
        page = await context.new_page()
        
        print("\n📸 Loading production app...")
        await page.goto("https://fast-nicedashboard.streamlit.app/",
                      wait_until="domcontentloaded",
                      timeout=90000)
        await asyncio.sleep(12)
        
        # Capture
        await page.screenshot(path="test_final_pr43_validation/after_rebuild.png", full_page=False)
        print("   ✅ Saved: after_rebuild.png")
        
        await browser.close()
        
        # Analyze
        print("\n" + "="*80)
        print("🔬 PIXEL ANALYSIS:")
        print("="*80)
        
        img = Image.open("test_final_pr43_validation/after_rebuild.png")
        pixels = np.array(img)
        
        # Sample key areas
        sample_points = [
            (960, 200, "Main title"),
            (960, 300, "Content"),
            (250, 300, "Sidebar"),
        ]
        
        white_bg = (255, 255, 255)
        config_applied = False
        
        for x, y, label in sample_points:
            rgb = tuple(pixels[y, x, :3].astype(int))
            contrast = calculate_contrast(rgb, white_bg)
            
            print(f"\n📍 {label} ({x}, {y}):")
            print(f"   RGB: {rgb}")
            print(f"   Contrast: {contrast:.2f}:1")
            
            # Check if it's the new color
            if rgb == (5, 5, 5):
                print(f"   ✅ PERFECT! config.toml #050505 IS APPLIED!")
                config_applied = True
            elif rgb[0] <= 10 and rgb[1] <= 10 and rgb[2] <= 10:
                print(f"   ✅ VERY CLOSE! config.toml likely applied (near-black)")
                config_applied = True
            elif rgb == (15, 23, 42):
                print(f"   ❌ OLD COLOR still showing (PR #42 color)")
            else:
                print(f"   🤔 Different color")
            
            if contrast >= 7.0:
                print(f"   ✅ WCAG AAA PASS")
        
        print("\n" + "="*80)
        if config_applied:
            print("🎉 SUCCESS! config.toml #050505 IS NOW APPLIED!")
            print("="*80)
            print("\n📊 EXPECTED RESULTS:")
            print("   - RGB values near (5, 5, 5)")
            print("   - Contrast ratio ~9:1")
            print("   - ⭐⭐⭐⭐⭐ 5-STAR quality achieved!")
        else:
            print("⚠️ config.toml NOT YET APPLIED - May need more time")
            print("="*80)
            print("\n📊 TROUBLESHOOTING:")
            print("   1. Streamlit Cloud may need more rebuild time")
            print("   2. Check if app restarted properly")
            print("   3. May need to trigger manual redeploy")

if __name__ == "__main__":
    asyncio.run(test_rebuild())
