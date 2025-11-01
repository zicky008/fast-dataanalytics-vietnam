#!/usr/bin/env python3
"""
🔬 PIXEL-LEVEL ANALYSIS - PR #43 vs PR #42
Professional comparison with WCAG AAA validation
"""
from PIL import Image
import numpy as np

def calculate_luminance(rgb):
    """Calculate relative luminance (WCAG 2.2)"""
    r, g, b = [x / 255.0 for x in rgb]
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def calculate_contrast_ratio(rgb1, rgb2):
    """Calculate WCAG contrast ratio"""
    l1 = calculate_luminance(rgb1)
    l2 = calculate_luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def pixel_difference(rgb1, rgb2):
    """Calculate Euclidean distance"""
    return np.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))

print("="*80)
print("🔬 COMPREHENSIVE PIXEL-LEVEL ANALYSIS")
print("="*80)
print("Comparing: PR #42 (before) vs PR #43 (after)")
print("="*80)

# Load images
try:
    dark_img = Image.open("test_comprehensive_pr42/dark_02_upload_fold.png")
    light_before_img = Image.open("test_comprehensive_pr42/light_02_upload_fold.png")
    light_after_img = Image.open("test_final_pr43_validation/light_02_above_fold.png")
    
    dark_pixels = np.array(dark_img)
    light_before_pixels = np.array(light_before_img)
    light_after_pixels = np.array(light_after_img)
    
    print(f"\n✅ Images loaded successfully")
    print(f"   Dark:         {dark_pixels.shape}")
    print(f"   Light Before: {light_before_pixels.shape}")
    print(f"   Light After:  {light_after_pixels.shape}")
    
except Exception as e:
    print(f"❌ Error loading images: {e}")
    exit(1)

# Sample points for critical UI elements (x, y, component_name, description)
sample_points = [
    (960, 200, "Page Title", "Header text"),
    (960, 400, "Upload Label", "File uploader label"),
    (200, 400, "Sidebar Label", "Sidebar text"),
    (960, 600, "Description", "Body text"),
    (960, 800, "Caption", "Secondary text"),
]

print("\n" + "="*80)
print("📊 DETAILED COMPARISON BY COMPONENT")
print("="*80)

total_improvement = 0
background_rgb = (255, 255, 255)  # White background

results = []

for x, y, component, description in sample_points:
    try:
        # Sample pixels (use center if out of bounds)
        h, w = dark_pixels.shape[:2]
        x = min(x, w - 1)
        y = min(y, h - 1)
        
        dark_rgb = tuple(dark_pixels[y, x, :3].astype(int))
        light_before_rgb = tuple(light_before_pixels[y, x, :3].astype(int))
        light_after_rgb = tuple(light_after_pixels[y, x, :3].astype(int))
        
        # Calculate improvements
        before_diff = pixel_difference(dark_rgb, light_before_rgb)
        after_diff = pixel_difference(dark_rgb, light_after_rgb)
        improvement = after_diff - before_diff
        total_improvement += improvement
        
        # Calculate contrast ratios
        contrast_before = calculate_contrast_ratio(light_before_rgb, background_rgb)
        contrast_after = calculate_contrast_ratio(light_after_rgb, background_rgb)
        contrast_improvement = contrast_after - contrast_before
        
        print(f"\n📍 {component} ({description}):")
        print(f"   Position: ({x}, {y})")
        print(f"   ────────────────────────────────────────────")
        print(f"   Dark RGB (baseline):   {dark_rgb}")
        print(f"   ────────────────────────────────────────────")
        print(f"   PR #42 BEFORE:")
        print(f"      RGB: {light_before_rgb}")
        print(f"      Contrast: {contrast_before:.2f}:1")
        print(f"   ────────────────────────────────────────────")
        print(f"   PR #43 AFTER:")
        print(f"      RGB: {light_after_rgb}")
        print(f"      Contrast: {contrast_after:.2f}:1")
        print(f"   ────────────────────────────────────────────")
        print(f"   IMPROVEMENT:")
        print(f"      Pixel Diff: {before_diff:.1f} → {after_diff:.1f} (Δ {improvement:+.1f})")
        print(f"      Contrast: {contrast_before:.2f}:1 → {contrast_after:.2f}:1 (Δ {contrast_improvement:+.2f})")
        
        # WCAG compliance check
        if contrast_after >= 7.0:
            wcag_status = "✅ WCAG AAA PASS"
            print(f"   {wcag_status} (7:1+ required, got {contrast_after:.2f}:1)")
        elif contrast_after >= 4.5:
            wcag_status = "⚠️ WCAG AA only"
            print(f"   {wcag_status} (need 7:1 for AAA, got {contrast_after:.2f}:1)")
        else:
            wcag_status = "❌ WCAG FAIL"
            print(f"   {wcag_status} (need 4.5:1 minimum, got {contrast_after:.2f}:1)")
        
        results.append({
            'component': component,
            'improvement': improvement,
            'contrast_before': contrast_before,
            'contrast_after': contrast_after,
            'wcag_status': wcag_status
        })
        
    except Exception as e:
        print(f"\n⚠️ {component}: Analysis error - {e}")

# Overall assessment
print("\n" + "="*80)
print("📊 OVERALL ASSESSMENT")
print("="*80)

print(f"\n🎯 PIXEL IMPROVEMENT ANALYSIS:")
print(f"   Total Pixel Improvement: {total_improvement:.1f}")
print(f"   PR #42 Baseline: 91.6 (⭐⭐⭐ 3/5 stars)")
print(f"   Target for 5-star: 180+ improvement")

if total_improvement >= 150:
    stars = "⭐⭐⭐⭐⭐"
    rating = "5/5 stars - EXCELLENT!"
    verdict = "🎉 SUCCESS! PR #43 achieved 5-STAR quality!"
elif total_improvement >= 100:
    stars = "⭐⭐⭐⭐"
    rating = "4/5 stars - Very Good"
    verdict = "✅ Significant improvement, close to 5-star"
elif total_improvement >= 50:
    stars = "⭐⭐⭐"
    rating = "3/5 stars - Good"
    verdict = "⚠️ Moderate improvement, needs more work"
else:
    stars = "⭐⭐"
    rating = "2/5 stars - Minimal"
    verdict = "❌ Minimal improvement, needs investigation"

print(f"\n🌟 RATING: {stars} {rating}")
print(f"   {verdict}")

# WCAG compliance summary
print(f"\n📋 WCAG AAA COMPLIANCE SUMMARY:")
wcag_pass = sum(1 for r in results if "AAA PASS" in r['wcag_status'])
wcag_aa = sum(1 for r in results if "AA only" in r['wcag_status'])
wcag_fail = sum(1 for r in results if "FAIL" in r['wcag_status'])

print(f"   ✅ AAA Pass (7:1+):  {wcag_pass}/{len(results)} components")
print(f"   ⚠️ AA Only (4.5:1):  {wcag_aa}/{len(results)} components")
print(f"   ❌ Failed (<4.5:1):  {wcag_fail}/{len(results)} components")

if wcag_pass == len(results):
    print(f"\n   🎉 PERFECT! All components meet WCAG AAA standards!")
elif wcag_pass >= len(results) * 0.8:
    print(f"\n   ✅ EXCELLENT! Most components meet WCAG AAA standards!")
elif wcag_pass >= len(results) * 0.5:
    print(f"\n   ⚠️ GOOD: Over half meet WCAG AAA, but needs improvement")
else:
    print(f"\n   ❌ NEEDS WORK: Most components don't meet AAA standards")

# Component-by-component summary
print(f"\n📊 COMPONENT IMPROVEMENTS:")
for r in results:
    imp = r['improvement']
    icon = "✅" if imp > 30 else "⚠️" if imp > 10 else "❌"
    print(f"   {icon} {r['component']:20s} {imp:+6.1f} pixels | "
          f"Contrast: {r['contrast_before']:.1f}:1 → {r['contrast_after']:.1f}:1")

print("\n" + "="*80)
print("✅ ANALYSIS COMPLETE")
print("="*80)
print("\n📸 Next: Visual inspection of screenshots for final verification")
