#!/usr/bin/env python3
"""
🔬 CHECK BACKGROUND COLOR
Determine if app is in dark or light theme by sampling background
"""
from PIL import Image
import numpy as np

img = Image.open("test_final_pr43_validation/after_rebuild.png")
pixels = np.array(img)

print("="*80)
print("🔬 BACKGROUND COLOR ANALYSIS")
print("="*80)

# Sample various background areas
bg_points = [
    (960, 50, "Top center background"),
    (960, 100, "Header background"),
    (1500, 400, "Right side background"),
    (500, 800, "Lower background"),
]

print("\n📊 BACKGROUND SAMPLES:")
print("="*80)

light_count = 0
dark_count = 0

for x, y, label in bg_points:
    rgb = tuple(pixels[y, x, :3].astype(int))
    avg = sum(rgb) / 3
    
    print(f"\n📍 {label}")
    print(f"   Position: ({x}, {y})")
    print(f"   RGB: {rgb}")
    print(f"   Average: {avg:.1f}")
    
    if avg > 200:
        print(f"   → LIGHT background")
        light_count += 1
    elif avg < 50:
        print(f"   → DARK background")
        dark_count += 1
    else:
        print(f"   → MEDIUM")

print("\n" + "="*80)
print("🎯 THEME DETERMINATION:")
print("="*80)
print(f"Light background areas: {light_count}")
print(f"Dark background areas: {dark_count}")

if light_count > dark_count:
    print("\n✅ THEME: LIGHT MODE")
    print("   config.toml backgroundColor=#FFFFFF should show white")
elif dark_count > light_count:
    print("\n🌙 THEME: DARK MODE")
    print("   App is rendering in dark theme despite our request")
else:
    print("\n🤔 THEME: MIXED/UNKNOWN")

# Check a specific known white area from our grid analysis
top_center = tuple(pixels[50, 960, :3].astype(int))
print(f"\n📍 Known white area (960, 50): RGB{top_center}")
if top_center == (255, 255, 255):
    print("   ✅ This area IS white! Light mode confirmed.")
elif top_center[0] < 50:
    print("   ❌ This area is DARK! Dark mode active.")

print("="*80)
