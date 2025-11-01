#!/usr/bin/env python3
"""
🔬 GRID INSPECTION - Sample many points to find light areas
"""
from PIL import Image
import numpy as np

img = Image.open("test_final_pr43_validation/light_test_approach_2_light.png")
pixels = np.array(img)
h, w = pixels.shape[:2]

print(f"Image size: {w}x{h}")
print("\n" + "="*80)
print("🔬 GRID SAMPLING (Every 200px)")
print("="*80)

# Sample a grid
light_pixels = []
dark_pixels = []

for y in range(0, h, 200):
    for x in range(0, w, 200):
        rgb = tuple(pixels[y, x, :3].astype(int))
        avg = sum(rgb) / 3
        
        if avg > 200:  # Likely white/light area
            light_pixels.append((x, y, rgb))
        elif avg < 50:  # Likely dark area
            dark_pixels.append((x, y, rgb))

print(f"\n📊 Found {len(light_pixels)} LIGHT pixels (avg > 200)")
print(f"📊 Found {len(dark_pixels)} DARK pixels (avg < 50)")

if light_pixels:
    print("\n✅ LIGHT AREAS FOUND:")
    for x, y, rgb in light_pixels[:10]:
        print(f"   ({x:4d}, {y:4d}): RGB{rgb}")

if dark_pixels:
    print("\n🌙 DARK AREAS FOUND:")
    for x, y, rgb in dark_pixels[:10]:
        print(f"   ({x:4d}, {y:4d}): RGB{rgb}")

# Sample center of main content area (should be background)
center_points = [
    (960, 300, "Center top"),
    (960, 540, "Exact center"),
    (1200, 540, "Right of center"),
    (600, 540, "Left of center"),
]

print("\n" + "="*80)
print("🎯 KEY AREA SAMPLES:")
print("="*80)

for x, y, label in center_points:
    rgb = tuple(pixels[y, x, :3].astype(int))
    avg = sum(rgb) / 3
    print(f"{label:20s} ({x:4d}, {y:4d}): RGB{rgb} avg={avg:.1f}")

# Check edges (sidebar should be there)
print("\n" + "="*80)
print("📏 EDGE SAMPLES:")
print("="*80)

edge_points = [
    (50, 300, "Far left (sidebar?)"),
    (250, 300, "Left edge (sidebar?)"),
    (1850, 300, "Far right"),
    (960, 50, "Top center"),
    (960, 1050, "Bottom center (if exists)"),
]

for x, y, label in edge_points:
    if y < h and x < w:
        rgb = tuple(pixels[y, x, :3].astype(int))
        avg = sum(rgb) / 3
        print(f"{label:25s} ({x:4d}, {y:4d}): RGB{rgb} avg={avg:.1f}")
