#!/usr/bin/env python3
"""
🔬 FORCE LIGHT THEME TEST
Test if Streamlit app respects light theme request
"""
import asyncio
from playwright.async_api import async_playwright
from PIL import Image
import numpy as np

async def test_light_theme():
    print("="*80)
    print("🔬 TESTING LIGHT THEME - FORCING LIGHT MODE")
    print("="*80)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Try multiple approaches to force light theme
        approaches = [
            ("no-preference", "color_scheme='no-preference'"),
            ("light", "color_scheme='light'"),
            ("null", "color_scheme=null (system default)"),
        ]
        
        for i, (scheme, description) in enumerate(approaches):
            print(f"\n{'='*80}")
            print(f"🧪 Approach {i+1}: {description}")
            print(f"{'='*80}")
            
            context_args = {
                "viewport": {"width": 1920, "height": 1080},
            }
            
            if scheme != "null":
                context_args["color_scheme"] = scheme
            
            context = await browser.new_context(**context_args)
            page = await context.new_page()
            
            # Navigate and wait
            print("   Loading page...")
            await page.goto("https://fast-nicedashboard.streamlit.app/",
                          wait_until="domcontentloaded",
                          timeout=90000)
            await asyncio.sleep(12)
            
            # Capture
            filename = f"test_final_pr43_validation/light_test_approach_{i+1}_{scheme}.png"
            await page.screenshot(path=filename, full_page=False)
            print(f"   ✅ Saved: {filename}")
            
            # Sample a pixel to check theme
            img = Image.open(filename)
            pixels = np.array(img)
            # Sample center title area
            sample_rgb = tuple(pixels[200, 960, :3].astype(int))
            print(f"   📊 Sample RGB at (960, 200): {sample_rgb}")
            
            # Determine if dark or light
            if sample_rgb[0] < 50 and sample_rgb[1] < 50 and sample_rgb[2] < 50:
                theme_detected = "🌙 DARK THEME detected (text is dark on likely dark bg)"
            elif sample_rgb[0] > 200 and sample_rgb[1] > 200 and sample_rgb[2] > 200:
                theme_detected = "☀️ LIGHT THEME detected (text is light on likely light bg)"
            else:
                theme_detected = f"🤔 UNKNOWN (RGB {sample_rgb})"
            
            print(f"   {theme_detected}")
            
            await context.close()
        
        await browser.close()
        
        print("\n" + "="*80)
        print("✅ TEST COMPLETE - Check screenshots manually")
        print("="*80)

if __name__ == "__main__":
    asyncio.run(test_light_theme())
