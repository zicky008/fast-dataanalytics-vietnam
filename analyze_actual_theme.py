#!/usr/bin/env python3
"""
🔬 PROPER THEME ANALYSIS
Check background AND text colors to determine theme
"""
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

print("="*80)
print("🔬 PROPER THEME ANALYSIS - BACKGROUND + TEXT")
print("="*80)

img = Image.open("test_final_pr43_validation/light_test_approach_2_light.png")
pixels = np.array(img)

# Sample points
points = [
    (960, 100, "Background (center top)"),
    (960, 200, "Title text"),
    (960, 400, "Body text"),
    (200, 400, "Sidebar area"),
]

print("\n📊 PIXEL ANALYSIS:")
print("="*80)

for x, y, description in points:
    rgb = tuple(pixels[y, x, :3].astype(int))
    lum = calculate_luminance(rgb)
    print(f"\n📍 {description}")
    print(f"   Position: ({x}, {y})")
    print(f"   RGB: {rgb}")
    print(f"   Luminance: {lum:.4f}")
    if lum > 0.5:
        print(f"   → LIGHT color (background candidate)")
    else:
        print(f"   → DARK color (text candidate)")

# Check contrast between background and text
bg_rgb = tuple(pixels[100, 960, :3].astype(int))
text_rgb = tuple(pixels[200, 960, :3].astype(int))

contrast = calculate_contrast(bg_rgb, text_rgb)

print("\n" + "="*80)
print("🎯 THEME DETERMINATION:")
print("="*80)
print(f"Background RGB: {bg_rgb}")
print(f"Text RGB: {text_rgb}")
print(f"Contrast Ratio: {contrast:.2f}:1")

if bg_rgb[0] > 240 and bg_rgb[1] > 240 and bg_rgb[2] > 240:
    print("\n✅ THEME: LIGHT MODE (white background)")
    if text_rgb[0] < 20 and text_rgb[1] < 30 and text_rgb[2] < 50:
        print("✅ TEXT: Dark colors (expected for light mode)")
        print(f"✅ ACCESSIBILITY: {contrast:.2f}:1 contrast")
        if contrast >= 7.0:
            print("✅ WCAG AAA PASS (7:1+ required)")
        elif contrast >= 4.5:
            print("⚠️ WCAG AA (need 7:1 for AAA)")
    else:
        print("❌ TEXT: Not dark enough!")
elif bg_rgb[0] < 30 and bg_rgb[1] < 30 and bg_rgb[2] < 30:
    print("\n🌙 THEME: DARK MODE (dark background)")
else:
    print("\n🤔 THEME: UNKNOWN")

print("="*80)
