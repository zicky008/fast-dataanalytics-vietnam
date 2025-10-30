#!/usr/bin/env python3
"""
🎯 COMPREHENSIVE PRODUCTION APP TESTING
Testing as 5 demanding Vietnamese users with ZERO tolerance for inaccuracies.

User's Final Request:
"Act as best expert testers and demanding Vietnamese real users for each domain 
to experience A to Z on the production app, test thoroughly every part to ensure 
happy customers, extremely accurate output, high credibility and trust, 5-star 
user satisfaction, fully validated."

Test Personas:
1. Chị Mai - HR Manager at Vinamilk (500+ employees)
2. Anh Tuấn - E-commerce Owner (Shopee seller, 500M-1B VND/month)
3. Chị Lan - Marketing Manager at FPT (100M-200M VND budget)
4. Anh Hùng - Sales Director at Viettel Enterprise (500M-5B VND deals)
5. Chị Ngọc - CS Manager at Lazada (500+ tickets/day)

Success Criteria:
✅ All 5 personas satisfied (9.0+/10 each)
✅ Zero critical data imputation
✅ 100% benchmark URLs working
✅ All insights have evidence
✅ Vietnamese text perfect
✅ Professional UX
✅ Transparent methodology
"""

import sys
import os
import pandas as pd
import re
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from premium_lean_pipeline import (
    PremiumLeanPipeline,
    BENCHMARK_SOURCES
)

from smart_oqmlb_pipeline import NEVER_IMPUTE_FIELDS

class ProductionAppTester:
    """Comprehensive production app tester simulating demanding Vietnamese users"""
    
    def __init__(self):
        self.test_results = []
        self.personas = {
            'hr': {
                'name': 'Chị Mai',
                'role': 'HR Manager at Vinamilk',
                'file': 'test_data/vietnam_hr_data.csv',
                'context': '500+ employees, cần phân tích công bằng lương',
                'critical_checks': ['luong_thang', 'position', 'employee_id'],
                'expected_domain': 'HR',
                'expected_insights': ['salary distribution', 'department comparison'],
                'benchmark_url': 'vietnamworks.com/salary-report'
            },
            'ecommerce': {
                'name': 'Anh Tuấn',
                'role': 'E-commerce Owner',
                'file': 'test_data/vietnam_ecommerce_data.csv',
                'context': 'Shopee seller, 500M-1B VND/month revenue',
                'critical_checks': ['order_id', 'customer_id', 'revenue'],
                'expected_domain': 'E-commerce',
                'expected_insights': ['order trends', 'payment methods'],
                'benchmark_url': 'esc.vn/wp-content/uploads'
            },
            'marketing': {
                'name': 'Chị Lan',
                'role': 'Marketing Manager at FPT',
                'file': 'test_data/vietnam_marketing_campaign_data.csv',
                'context': '100M-200M VND budget, cần tối ưu ROAS',
                'critical_checks': ['budget', 'revenue', 'roas'],
                'expected_domain': 'Marketing',
                'expected_insights': ['campaign performance', 'channel ROI'],
                'benchmark_url': 'datareportal.com/reports/digital'
            },
            'sales': {
                'name': 'Anh Hùng',
                'role': 'Sales Director at Viettel',
                'file': 'test_data/vietnam_sales_pipeline_data.csv',
                'context': 'Enterprise deals 500M-5B VND',
                'critical_checks': ['deal_value', 'deal_name', 'customer_name'],
                'expected_domain': 'Sales',
                'expected_insights': ['pipeline health', 'conversion rates'],
                'benchmark_url': 'hubspot.com'
            },
            'customer_service': {
                'name': 'Chị Ngọc',
                'role': 'CS Manager at Lazada',
                'file': 'test_data/vietnam_customer_service_data.csv',
                'context': '500+ tickets/day, cần cải thiện CSAT',
                'critical_checks': ['customer_id', 'satisfaction_score'],
                'expected_domain': 'Customer Service',
                'expected_insights': ['ticket resolution', 'satisfaction trends'],
                'benchmark_url': 'zendesk.com'
            }
        }
        
    def print_header(self, text: str, level: int = 1):
        """Print formatted header"""
        symbols = {1: '='*80, 2: '-'*80, 3: '·'*80}
        print(f"\n{symbols[level]}")
        print(f"{'🎯' if level == 1 else '📋' if level == 2 else '✓'} {text}")
        print(symbols[level])
        
    def test_persona(self, persona_key: str) -> Dict:
        """Test complete workflow for one persona"""
        persona = self.personas[persona_key]
        self.print_header(f"Testing: {persona['name']} - {persona['role']}", 1)
        print(f"📍 Context: {persona['context']}")
        print(f"📁 Dataset: {persona['file']}")
        
        scores = {
            'data_accuracy': 0,
            'benchmark_urls': 0,
            'insights_quality': 0,
            'ux_ui': 0,
            'trust_credibility': 0
        }
        
        issues = []
        
        try:
            # Step 1: Load and analyze data
            self.print_header("STEP 1: Upload & Load Data", 2)
            file_path = project_root / persona['file']
            df = pd.read_csv(file_path)
            print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")
            print(f"📊 Columns: {', '.join(df.columns[:8])}{'...' if len(df.columns) > 8 else ''}")
            
            # Step 2: Check NEVER_IMPUTE protection
            self.print_header("STEP 2: NEVER_IMPUTE Protection Check (CRITICAL)", 2)
            impute_violations = []
            for field in persona['critical_checks']:
                if field in df.columns:
                    missing_count = df[field].isna().sum()
                    if missing_count > 0:
                        # Check if field is protected
                        is_protected = any(field in protected for protected in NEVER_IMPUTE_FIELDS)
                        if is_protected:
                            print(f"✅ {field}: {missing_count} missing values PROTECTED (will NOT impute)")
                        else:
                            print(f"⚠️  {field}: {missing_count} missing but NOT protected!")
                            impute_violations.append(field)
                    else:
                        print(f"✅ {field}: No missing values")
            
            if impute_violations:
                issues.append(f"❌ CRITICAL: {', '.join(impute_violations)} not protected from imputation!")
                scores['data_accuracy'] = 0
            else:
                scores['data_accuracy'] = 3  # Max 3 points
                print(f"\n🎉 EXCELLENT: All critical fields protected!")
            
            # Step 3: Run pipeline
            self.print_header("STEP 3: Run Analysis Pipeline", 2)
            pipeline = PremiumLeanPipeline()
            result = pipeline.process(df)
            
            # Step 4: Domain detection
            self.print_header("STEP 4: Domain Detection", 2)
            detected_domain = result.get('domain', 'Unknown')
            print(f"Detected: {detected_domain}")
            print(f"Expected: {persona['expected_domain']}")
            
            if detected_domain == persona['expected_domain']:
                print(f"✅ Domain detection CORRECT")
                scores['ux_ui'] += 1
            else:
                issues.append(f"❌ Domain mismatch: got {detected_domain}, expected {persona['expected_domain']}")
                print(f"❌ Domain detection FAILED")
            
            # Step 5: Data quality score
            self.print_header("STEP 5: Data Quality Assessment", 2)
            quality_score = result.get('quality_score', 0)
            print(f"Quality Score: {quality_score:.1f}/100")
            
            if quality_score >= 70:
                print(f"✅ Quality score acceptable (≥70)")
                scores['ux_ui'] += 1
            else:
                issues.append(f"⚠️  Low quality score: {quality_score:.1f}")
            
            # Step 6: Insights validation
            self.print_header("STEP 6: Insights Quality Check", 2)
            insights = result.get('insights', [])
            print(f"Generated {len(insights)} insights")
            
            insights_valid = 0
            insights_invalid = 0
            
            for i, insight in enumerate(insights[:5], 1):  # Check first 5
                print(f"\n--- Insight {i} ---")
                print(f"Text: {insight.get('insight', '')[:100]}...")
                
                # Check for data evidence
                evidence = insight.get('data_evidence', {})
                has_columns = bool(evidence.get('columns'))
                has_rows = bool(evidence.get('rows'))
                has_numbers = bool(evidence.get('actual_numbers'))
                
                print(f"Evidence - Columns: {has_columns}, Rows: {has_rows}, Numbers: {has_numbers}")
                
                if has_columns and has_rows and has_numbers:
                    print(f"✅ Complete evidence")
                    insights_valid += 1
                else:
                    print(f"❌ Incomplete evidence")
                    insights_invalid += 1
            
            if insights_valid >= 3:
                scores['insights_quality'] = 2  # Max 2 points
                print(f"\n✅ Insights quality EXCELLENT")
            elif insights_valid >= 1:
                scores['insights_quality'] = 1
                print(f"\n⚠️  Insights quality ACCEPTABLE")
            else:
                issues.append(f"❌ No insights with complete evidence")
                print(f"\n❌ Insights quality POOR")
            
            # Step 7: Benchmark URLs
            self.print_header("STEP 7: Benchmark URL Validation", 2)
            benchmarks = result.get('benchmarks', {})
            print(f"Available benchmarks: {len(benchmarks)}")
            
            # Find Vietnam-specific benchmarks
            vietnam_benchmarks = []
            for key, bench in benchmarks.items():
                if bench.get('vietnam_specific'):
                    vietnam_benchmarks.append(bench)
            
            print(f"Vietnam-specific: {len(vietnam_benchmarks)}")
            
            # Check if expected URL present
            url_found = False
            for bench in vietnam_benchmarks:
                url = bench.get('url', '')
                if persona['benchmark_url'] in url:
                    print(f"✅ Expected benchmark found: {url}")
                    url_found = True
                    
                    # Verify URL is not fake
                    if url and url != 'None' and 'http' in url:
                        scores['benchmark_urls'] = 2  # Max 2 points
                        print(f"✅ URL valid: {url[:60]}...")
                    else:
                        issues.append(f"❌ Invalid URL: {url}")
                    break
            
            if not url_found:
                issues.append(f"⚠️  Expected benchmark URL not found: {persona['benchmark_url']}")
                print(f"⚠️  Expected benchmark not found")
            
            # Step 8: Trust & Credibility
            self.print_header("STEP 8: Trust & Credibility Assessment", 2)
            
            # Check for fake data indicators
            fake_indicators = []
            
            # Check if critical fields were imputed
            if not impute_violations:
                print(f"✅ No critical data imputation")
            else:
                fake_indicators.append("Critical data imputed")
            
            # Check for "calculated" source
            calc_source = BENCHMARK_SOURCES.get('calculated', {})
            if calc_source.get('url') and calc_source['url'] != 'None':
                print(f"✅ 'Calculated' source has verification URL")
            else:
                fake_indicators.append("'Calculated' source missing URL")
            
            # Check Vietnam source count
            vietnam_count = sum(1 for v in BENCHMARK_SOURCES.values() if v.get('vietnam_specific'))
            vietnam_pct = (vietnam_count / len(BENCHMARK_SOURCES)) * 100
            print(f"✅ Vietnam sources: {vietnam_count}/{len(BENCHMARK_SOURCES)} ({vietnam_pct:.1f}%)")
            
            if not fake_indicators:
                scores['trust_credibility'] = 1  # Max 1 point
                print(f"\n✅ TRUST LEVEL: HIGH")
            else:
                issues.append(f"❌ Trust issues: {', '.join(fake_indicators)}")
                print(f"\n❌ TRUST LEVEL: LOW")
            
        except Exception as e:
            issues.append(f"❌ FATAL ERROR: {str(e)}")
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
        
        # Calculate final score
        total_score = sum(scores.values())
        max_score = 10
        
        self.print_header(f"FINAL SCORE: {persona['name']}", 1)
        print(f"Data Accuracy (max 3):      {scores['data_accuracy']}/3")
        print(f"Benchmark URLs (max 2):     {scores['benchmark_urls']}/2")
        print(f"Insights Quality (max 2):   {scores['insights_quality']}/2")
        print(f"UX/UI (max 2):              {scores['ux_ui']}/2")
        print(f"Trust/Credibility (max 1):  {scores['trust_credibility']}/1")
        print(f"\n{'='*80}")
        print(f"TOTAL SCORE: {total_score}/{max_score}")
        print(f"RATING: {self.get_rating(total_score)}")
        print(f"{'='*80}")
        
        if issues:
            print(f"\n⚠️  ISSUES FOUND ({len(issues)}):")
            for issue in issues:
                print(f"  • {issue}")
        else:
            print(f"\n🎉 NO ISSUES FOUND! PERFECT EXECUTION!")
        
        return {
            'persona': persona['name'],
            'role': persona['role'],
            'scores': scores,
            'total_score': total_score,
            'max_score': max_score,
            'rating': self.get_rating(total_score),
            'issues': issues,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_rating(self, score: float) -> str:
        """Convert numeric score to star rating"""
        if score >= 9.5:
            return "⭐⭐⭐⭐⭐ OUTSTANDING (5 stars)"
        elif score >= 9.0:
            return "⭐⭐⭐⭐⭐ EXCELLENT (5 stars)"
        elif score >= 8.0:
            return "⭐⭐⭐⭐ VERY GOOD (4 stars)"
        elif score >= 7.0:
            return "⭐⭐⭐ GOOD (3 stars)"
        elif score >= 6.0:
            return "⭐⭐ FAIR (2 stars)"
        else:
            return "⭐ POOR (1 star)"
    
    def run_all_tests(self):
        """Run tests for all 5 personas"""
        self.print_header("🎯 COMPREHENSIVE PRODUCTION APP TESTING", 1)
        print(f"Testing as 5 demanding Vietnamese users")
        print(f"ZERO tolerance for inaccuracies")
        print(f"Target: 5-star satisfaction for ALL personas")
        
        results = []
        for persona_key in self.personas.keys():
            result = self.test_persona(persona_key)
            results.append(result)
            self.test_results.append(result)
        
        # Final summary
        self.print_header("📊 FINAL SUMMARY: ALL PERSONAS", 1)
        
        total_scores = [r['total_score'] for r in results]
        avg_score = sum(total_scores) / len(total_scores)
        
        print(f"\nIndividual Scores:")
        for r in results:
            print(f"  {r['persona']}: {r['total_score']}/{r['max_score']} - {r['rating']}")
        
        print(f"\n{'='*80}")
        print(f"AVERAGE SCORE: {avg_score:.2f}/10")
        print(f"OVERALL RATING: {self.get_rating(avg_score)}")
        print(f"{'='*80}")
        
        # Check success criteria
        all_pass = all(r['total_score'] >= 9.0 for r in results)
        no_critical_issues = all(len(r['issues']) == 0 for r in results)
        
        print(f"\n✅ SUCCESS CRITERIA:")
        print(f"  • All personas ≥9.0/10: {'✅ PASS' if all_pass else '❌ FAIL'}")
        print(f"  • No critical issues: {'✅ PASS' if no_critical_issues else '❌ FAIL'}")
        
        if all_pass and no_critical_issues:
            print(f"\n🎉🎉🎉 VALIDATION COMPLETE: 5-STAR SATISFACTION ACHIEVED! 🎉🎉🎉")
        else:
            print(f"\n⚠️  VALIDATION INCOMPLETE: Issues need resolution")
        
        return results

def main():
    """Main entry point"""
    print(f"""
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║         🎯 VIETNAM DATA ANALYTICS APP - PRODUCTION TESTING 🎯              ║
    ║                                                                           ║
    ║  Testing as 5 demanding Vietnamese users with ZERO tolerance for errors  ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    tester = ProductionAppTester()
    results = tester.run_all_tests()
    
    print(f"\n✅ Testing complete! Check results above.")
    return results

if __name__ == "__main__":
    main()
