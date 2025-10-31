#!/usr/bin/env python3
"""
Automated Lighthouse Testing
Tests Performance, Accessibility, Best Practices, SEO
100% free, built into Chrome
"""

import subprocess
import json
import os
from datetime import datetime
from pathlib import Path

class LighthouseTest:
    """
    Automate Google Lighthouse testing
    
    Tests:
    - Performance (target: 90+)
    - Accessibility (target: 95+)
    - Best Practices (target: 95+)
    - SEO (target: 90+)
    """
    
    def __init__(self, url: str, output_dir: str = "lighthouse_reports"):
        self.url = url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def run_lighthouse(self, device: str = "desktop") -> dict:
        """
        Run Lighthouse test
        
        Args:
            device: "desktop" or "mobile"
            
        Returns:
            Test results dict
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"lighthouse_{device}_{timestamp}.json"
        
        # Lighthouse CLI command
        cmd = [
            "lighthouse",
            self.url,
            "--output=json",
            f"--output-path={output_file}",
            "--chrome-flags='--headless'",
            "--quiet"
        ]
        
        if device == "mobile":
            cmd.append("--preset=mobile")
        else:
            cmd.append("--preset=desktop")
        
        print(f"🔍 Running Lighthouse test ({device})...")
        print(f"   URL: {self.url}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                with open(output_file, 'r') as f:
                    data = json.load(f)
                
                return self._parse_results(data, device)
            else:
                print(f"❌ Lighthouse failed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("❌ Lighthouse timed out (>120s)")
            return None
        except FileNotFoundError:
            print("❌ Lighthouse not installed. Install with: npm install -g lighthouse")
            return None
    
    def _parse_results(self, data: dict, device: str) -> dict:
        """Parse Lighthouse results"""
        categories = data.get('categories', {})
        
        results = {
            'device': device,
            'url': self.url,
            'timestamp': datetime.now().isoformat(),
            'scores': {
                'performance': categories.get('performance', {}).get('score', 0) * 100,
                'accessibility': categories.get('accessibility', {}).get('score', 0) * 100,
                'best_practices': categories.get('best-practices', {}).get('score', 0) * 100,
                'seo': categories.get('seo', {}).get('score', 0) * 100,
            },
            'metrics': {
                'first_contentful_paint': data.get('audits', {}).get('first-contentful-paint', {}).get('displayValue', 'N/A'),
                'speed_index': data.get('audits', {}).get('speed-index', {}).get('displayValue', 'N/A'),
                'largest_contentful_paint': data.get('audits', {}).get('largest-contentful-paint', {}).get('displayValue', 'N/A'),
                'time_to_interactive': data.get('audits', {}).get('interactive', {}).get('displayValue', 'N/A'),
                'total_blocking_time': data.get('audits', {}).get('total-blocking-time', {}).get('displayValue', 'N/A'),
                'cumulative_layout_shift': data.get('audits', {}).get('cumulative-layout-shift', {}).get('displayValue', 'N/A'),
            }
        }
        
        return results
    
    def display_results(self, results: dict):
        """Display test results"""
        if not results:
            return
        
        print("\n" + "=" * 80)
        print(f"📊 LIGHTHOUSE TEST RESULTS - {results['device'].upper()}")
        print("=" * 80)
        
        scores = results['scores']
        print("\n🎯 SCORES:")
        for category, score in scores.items():
            icon = "✅" if score >= 90 else "⚠️" if score >= 70 else "❌"
            print(f"  {icon} {category.replace('_', ' ').title()}: {score:.0f}/100")
        
        print("\n⚡ PERFORMANCE METRICS:")
        for metric, value in results['metrics'].items():
            print(f"  • {metric.replace('_', ' ').title()}: {value}")
        
        # Overall assessment
        avg_score = sum(scores.values()) / len(scores)
        print("\n" + "=" * 80)
        if avg_score >= 90:
            print("🎉 EXCELLENT! All metrics meet 5-star standards")
        elif avg_score >= 80:
            print("✅ GOOD! Minor improvements needed")
        elif avg_score >= 70:
            print("⚠️  ACCEPTABLE! Needs optimization")
        else:
            print("❌ NEEDS WORK! Major improvements required")
        print("=" * 80)


if __name__ == "__main__":
    # Example usage (replace with your production URL)
    url = "https://your-app.streamlit.app"
    
    tester = LighthouseTest(url)
    
    # Test desktop
    desktop_results = tester.run_lighthouse("desktop")
    if desktop_results:
        tester.display_results(desktop_results)
    
    # Test mobile
    mobile_results = tester.run_lighthouse("mobile")
    if mobile_results:
        tester.display_results(mobile_results)
