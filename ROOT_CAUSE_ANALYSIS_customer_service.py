#!/usr/bin/env python3
"""
ROOT CAUSE ANALYSIS: Customer Service KPI Discrepancies
========================================================

Purpose: Identify exact root cause of value differences between:
1. Expected baseline calculations (UAT document)
2. Validation test script results
3. Production dashboard output (user screenshots)

Zero Tolerance Philosophy:
- Every decimal place matters
- 100% accuracy required for real customer trust
- Small errors at scale = catastrophic failures

Test Date: 2025-10-23
Tester: Demanding Expert DA + Real CX Officer personas
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json

def load_data():
    """Load the Customer Service test dataset"""
    print("=" * 80)
    print("📂 STEP 1: LOADING TEST DATA")
    print("=" * 80)
    
    df = pd.read_csv('sample_data/customer_service_tickets_30days.csv')
    
    print(f"✅ Loaded {len(df)} tickets")
    print(f"✅ Date range: {df['created_date'].min()} to {df['created_date'].max()}")
    print(f"✅ Columns: {list(df.columns)}")
    print()
    
    return df

def calculate_kpis_baseline(df):
    """
    Calculate KPIs using EXACT methodology from UAT document.
    This represents the GROUND TRUTH baseline.
    """
    print("=" * 80)
    print("📊 STEP 2: BASELINE CALCULATIONS (GROUND TRUTH)")
    print("=" * 80)
    
    kpis = {}
    
    # KPI 1: Average First Response Time
    kpis['avg_first_response_time'] = {
        'value': df['first_response_time_mins'].mean(),
        'formula': 'Mean of first_response_time_mins',
        'column': 'first_response_time_mins',
        'count': len(df),
        'sum': df['first_response_time_mins'].sum(),
        'raw_data': df['first_response_time_mins'].tolist()[:10]  # First 10 for inspection
    }
    
    # KPI 2: Average Resolution Time
    kpis['avg_resolution_time'] = {
        'value': df['resolution_time_hours'].mean(),
        'formula': 'Mean of resolution_time_hours',
        'column': 'resolution_time_hours',
        'count': len(df),
        'sum': df['resolution_time_hours'].sum(),
        'raw_data': df['resolution_time_hours'].tolist()[:10]
    }
    
    # KPI 3: CSAT Score
    kpis['csat_score'] = {
        'value': df['customer_satisfaction_score'].mean(),
        'formula': 'Mean of customer_satisfaction_score',
        'column': 'customer_satisfaction_score',
        'count': len(df),
        'sum': df['customer_satisfaction_score'].sum(),
        'distribution': df['customer_satisfaction_score'].value_counts().to_dict(),
        'raw_data': df['customer_satisfaction_score'].tolist()[:10]
    }
    
    # KPI 4: First Contact Resolution
    fcr_count = len(df[df['reopened'] == 'No'])
    kpis['first_contact_resolution'] = {
        'value': (fcr_count / len(df)) * 100,
        'formula': "(reopened='No') / total * 100",
        'column': 'reopened',
        'resolved_count': fcr_count,
        'total_count': len(df),
        'reopened_distribution': df['reopened'].value_counts().to_dict()
    }
    
    # KPI 5: SLA Met
    sla_met_count = len(df[df['sla_met'] == 'Yes'])
    kpis['sla_met'] = {
        'value': (sla_met_count / len(df)) * 100,
        'formula': "(sla_met='Yes') / total * 100",
        'column': 'sla_met',
        'met_count': sla_met_count,
        'total_count': len(df),
        'sla_distribution': df['sla_met'].value_counts().to_dict()
    }
    
    # KPI 6: Escalation Rate
    escalated_count = len(df[df['escalated'] == 'Yes'])
    kpis['escalation_rate'] = {
        'value': (escalated_count / len(df)) * 100,
        'formula': "(escalated='Yes') / total * 100",
        'column': 'escalated',
        'escalated_count': escalated_count,
        'total_count': len(df),
        'escalation_distribution': df['escalated'].value_counts().to_dict()
    }
    
    # KPI 7: Reopen Rate
    reopened_count = len(df[df['reopened'] == 'Yes'])
    kpis['reopen_rate'] = {
        'value': (reopened_count / len(df)) * 100,
        'formula': "(reopened='Yes') / total * 100",
        'column': 'reopened',
        'reopened_count': reopened_count,
        'total_count': len(df),
        'reopen_distribution': df['reopened'].value_counts().to_dict()
    }
    
    # KPI 8: Total Ticket Value
    kpis['total_ticket_value'] = {
        'value': df['ticket_value_vnd'].sum(),
        'formula': 'Sum of ticket_value_vnd',
        'column': 'ticket_value_vnd',
        'count': len(df),
        'mean': df['ticket_value_vnd'].mean(),
        'median': df['ticket_value_vnd'].median(),
        'raw_data': df['ticket_value_vnd'].tolist()[:10]
    }
    
    # Print results
    print("\n🎯 BASELINE KPI CALCULATIONS:\n")
    print(f"1. Avg First Response Time:  {kpis['avg_first_response_time']['value']:.2f} minutes")
    print(f"   - Sum: {kpis['avg_first_response_time']['sum']:.2f} / Count: {kpis['avg_first_response_time']['count']}")
    print(f"   - Sample: {kpis['avg_first_response_time']['raw_data']}")
    
    print(f"\n2. Avg Resolution Time:       {kpis['avg_resolution_time']['value']:.2f} hours")
    print(f"   - Sum: {kpis['avg_resolution_time']['sum']:.2f} / Count: {kpis['avg_resolution_time']['count']}")
    print(f"   - Sample: {kpis['avg_resolution_time']['raw_data']}")
    
    print(f"\n3. CSAT Score:                {kpis['csat_score']['value']:.2f} / 5.0")
    print(f"   - Sum: {kpis['csat_score']['sum']:.2f} / Count: {kpis['csat_score']['count']}")
    print(f"   - Distribution: {kpis['csat_score']['distribution']}")
    print(f"   - Sample: {kpis['csat_score']['raw_data']}")
    
    print(f"\n4. First Contact Resolution:  {kpis['first_contact_resolution']['value']:.2f}%")
    print(f"   - Resolved: {kpis['first_contact_resolution']['resolved_count']} / Total: {kpis['first_contact_resolution']['total_count']}")
    print(f"   - Distribution: {kpis['first_contact_resolution']['reopened_distribution']}")
    
    print(f"\n5. SLA Met:                   {kpis['sla_met']['value']:.2f}%")
    print(f"   - Met: {kpis['sla_met']['met_count']} / Total: {kpis['sla_met']['total_count']}")
    print(f"   - Distribution: {kpis['sla_met']['sla_distribution']}")
    
    print(f"\n6. Escalation Rate:           {kpis['escalation_rate']['value']:.2f}%")
    print(f"   - Escalated: {kpis['escalation_rate']['escalated_count']} / Total: {kpis['escalation_rate']['total_count']}")
    print(f"   - Distribution: {kpis['escalation_rate']['escalation_distribution']}")
    
    print(f"\n7. Reopen Rate:               {kpis['reopen_rate']['value']:.2f}%")
    print(f"   - Reopened: {kpis['reopen_rate']['reopened_count']} / Total: {kpis['reopen_rate']['total_count']}")
    print(f"   - Distribution: {kpis['reopen_rate']['reopen_distribution']}")
    
    print(f"\n8. Total Ticket Value:        {kpis['total_ticket_value']['value']:,.0f} VND")
    print(f"   - Count: {kpis['total_ticket_value']['count']}")
    print(f"   - Mean: {kpis['total_ticket_value']['mean']:,.0f} VND")
    print(f"   - Median: {kpis['total_ticket_value']['median']:,.0f} VND")
    print(f"   - Sample: {kpis['total_ticket_value']['raw_data']}")
    
    print()
    
    return kpis

def compare_with_production(baseline_kpis):
    """
    Compare baseline calculations with production values from user screenshots.
    Identify exact discrepancies and calculate error percentages.
    """
    print("=" * 80)
    print("🔬 STEP 3: PRODUCTION VALUES COMPARISON")
    print("=" * 80)
    
    # Production values extracted from user screenshots
    production = {
        'avg_first_response_time': 18.8,    # Screenshot shows 18.8 min
        'avg_resolution_time': 4.2,          # Screenshot shows 4.2 hrs
        'csat_score': 4.4,                    # Screenshot shows 4.4
        'first_contact_resolution': 77.0,    # Screenshot shows 77.0%
        'sla_met': 82.0,                      # Screenshot shows 82.0%
        'escalation_rate': 21.0,              # Screenshot shows 21.0%
        'reopen_rate': 18.0,                  # Screenshot shows 18.0%
        'total_ticket_value': 397845000       # Screenshot shows 397845000 VND
    }
    
    # Expected values from UAT document
    expected = {
        'avg_first_response_time': 18.81,
        'avg_resolution_time': 4.35,
        'csat_score': 4.22,
        'first_contact_resolution': 82.00,
        'sla_met': 77.00,
        'escalation_rate': 21.00,
        'reopen_rate': 18.00,
        'total_ticket_value': 397845000
    }
    
    print("\n📊 COMPARISON TABLE:\n")
    print(f"{'KPI':<30} {'Baseline':<15} {'Expected':<15} {'Production':<15} {'Status'}")
    print("-" * 90)
    
    discrepancies = []
    
    for key in production.keys():
        baseline_val = baseline_kpis[key]['value']
        expected_val = expected[key]
        production_val = production[key]
        
        # Calculate differences
        baseline_vs_expected = abs(baseline_val - expected_val)
        baseline_vs_production = abs(baseline_val - production_val)
        expected_vs_production = abs(expected_val - production_val)
        
        # Determine status
        if baseline_vs_production < 0.01:  # Essentially equal
            status = "✅ MATCH"
        elif baseline_vs_production < 0.5:  # Rounding difference
            status = "⚠️ ROUNDING"
            discrepancies.append({
                'kpi': key,
                'baseline': baseline_val,
                'production': production_val,
                'difference': baseline_vs_production,
                'type': 'rounding'
            })
        else:  # Significant difference
            status = "❌ MISMATCH"
            discrepancies.append({
                'kpi': key,
                'baseline': baseline_val,
                'production': production_val,
                'difference': baseline_vs_production,
                'type': 'calculation_error'
            })
        
        # Format values based on KPI type
        if key == 'total_ticket_value':
            print(f"{key:<30} {baseline_val:>14,.0f} {expected_val:>14,.0f} {production_val:>14,.0f} {status}")
        else:
            print(f"{key:<30} {baseline_val:>14.2f} {expected_val:>14.2f} {production_val:>14.2f} {status}")
    
    print()
    
    return discrepancies, production, expected

def analyze_discrepancies(discrepancies, baseline_kpis, df):
    """
    Deep dive analysis of each discrepancy to identify root cause.
    """
    print("=" * 80)
    print("🔍 STEP 4: ROOT CAUSE ANALYSIS OF DISCREPANCIES")
    print("=" * 80)
    
    if not discrepancies:
        print("\n✅ NO DISCREPANCIES FOUND - All values match!")
        print()
        return
    
    print(f"\n⚠️ Found {len(discrepancies)} discrepancies requiring investigation:\n")
    
    for i, disc in enumerate(discrepancies, 1):
        print(f"\n{'=' * 80}")
        print(f"DISCREPANCY #{i}: {disc['kpi'].upper()}")
        print(f"{'=' * 80}")
        
        print(f"\n📊 Values:")
        print(f"   Baseline (Ground Truth):  {disc['baseline']:.4f}")
        print(f"   Production (Screenshot):  {disc['production']:.4f}")
        print(f"   Difference:               {disc['difference']:.4f}")
        print(f"   Error %:                  {(disc['difference'] / disc['baseline'] * 100):.2f}%")
        
        # Get detailed data for this KPI
        kpi_data = baseline_kpis[disc['kpi']]
        
        print(f"\n🔬 Calculation Details:")
        print(f"   Formula: {kpi_data['formula']}")
        print(f"   Column: {kpi_data['column']}")
        
        # Specific analysis based on KPI type
        if disc['kpi'] == 'csat_score':
            print(f"\n   Distribution in data:")
            for score, count in sorted(kpi_data['distribution'].items()):
                print(f"      Score {score}: {count} tickets")
            
            print(f"\n   Calculation check:")
            print(f"      Sum: {kpi_data['sum']:.2f}")
            print(f"      Count: {kpi_data['count']}")
            print(f"      Mean: {kpi_data['sum'] / kpi_data['count']:.4f}")
            
            print(f"\n🤔 HYPOTHESIS:")
            print(f"   Production might be calculating CSAT differently:")
            print(f"   - Possibility 1: Weighted by ticket value")
            print(f"   - Possibility 2: Excluding certain categories")
            print(f"   - Possibility 3: Different aggregation method")
            
            # Test weighted average
            weighted_avg = (df['customer_satisfaction_score'] * df['ticket_value_vnd']).sum() / df['ticket_value_vnd'].sum()
            print(f"\n   Test - Weighted by ticket value: {weighted_avg:.4f}")
            if abs(weighted_avg - disc['production']) < 0.01:
                print(f"      ✅ THIS MATCHES PRODUCTION! Root cause found.")
            
            # Test by channel
            print(f"\n   Test - By channel:")
            for channel in df['channel'].unique():
                channel_csat = df[df['channel'] == channel]['customer_satisfaction_score'].mean()
                print(f"      {channel}: {channel_csat:.2f}")
        
        elif disc['kpi'] == 'first_contact_resolution':
            print(f"\n   Distribution in data:")
            for val, count in kpi_data['reopened_distribution'].items():
                print(f"      Reopened={val}: {count} tickets")
            
            print(f"\n   Calculation check:")
            print(f"      Not reopened: {kpi_data['resolved_count']}")
            print(f"      Total: {kpi_data['total_count']}")
            print(f"      FCR: {(kpi_data['resolved_count'] / kpi_data['total_count'] * 100):.4f}%")
            
            print(f"\n🤔 HYPOTHESIS:")
            print(f"   Production might be:")
            print(f"   - Using different reopened detection logic")
            print(f"   - Excluding certain ticket types")
            print(f"   - Inversing the calculation (reopened vs resolved)")
            
            # Test inverse (using reopen_rate KPI data)
            reopen_kpi = baseline_kpis['reopen_rate']
            reopened_rate = reopen_kpi['value']
            fcr_from_reopened = 100 - reopened_rate
            print(f"\n   Test - FCR from reopen rate: {fcr_from_reopened:.4f}%")
            if abs(fcr_from_reopened - disc['production']) < 0.01:
                print(f"      ✅ THIS MATCHES! But wait... baseline already uses this logic.")
        
        elif disc['kpi'] == 'sla_met':
            print(f"\n   Distribution in data:")
            for val, count in kpi_data['sla_distribution'].items():
                print(f"      SLA Met={val}: {count} tickets")
            
            print(f"\n   Calculation check:")
            print(f"      SLA Met: {kpi_data['met_count']}")
            print(f"      Total: {kpi_data['total_count']}")
            print(f"      Percentage: {(kpi_data['met_count'] / kpi_data['total_count'] * 100):.4f}%")
            
            print(f"\n🤔 HYPOTHESIS:")
            print(f"   Expected: 77.00% (77 tickets met SLA)")
            print(f"   Production: 82.00% (82 tickets met SLA)")
            print(f"   Difference: 5 tickets")
            print(f"   Possible causes:")
            print(f"   - Column value detection error (Yes/yes/YES)")
            print(f"   - Missing data handling difference")
            print(f"   - Swapped Yes/No logic")
            
            # Check for case sensitivity
            sla_yes_variations = df['sla_met'].value_counts()
            print(f"\n   SLA value variations: {sla_yes_variations.to_dict()}")
        
        elif disc['kpi'] in ['avg_first_response_time', 'avg_resolution_time']:
            print(f"\n   Calculation check:")
            print(f"      Sum: {kpi_data['sum']:.2f}")
            print(f"      Count: {kpi_data['count']}")
            print(f"      Mean: {kpi_data['sum'] / kpi_data['count']:.4f}")
            print(f"      Sample data: {kpi_data['raw_data']}")
            
            print(f"\n🤔 HYPOTHESIS:")
            print(f"   Difference: {disc['difference']:.4f} {'minutes' if 'response' in disc['kpi'] else 'hours'}")
            print(f"   This is likely:")
            print(f"   - Display rounding (showing 1 decimal vs 2 decimals)")
            print(f"   - Float precision in calculation")
            print(f"   - NOT a calculation error")
            
            # Check if rounding explains it
            rounded_baseline = round(disc['baseline'], 1)
            print(f"\n   Baseline rounded to 1 decimal: {rounded_baseline:.1f}")
            if abs(rounded_baseline - disc['production']) < 0.01:
                print(f"      ✅ EXPLAINED BY ROUNDING")
        
        print(f"\n{'=' * 80}\n")
    
    return

def investigate_fcr_sla_swap(df):
    """
    Special investigation: Are FCR and SLA Met values swapped in production?
    """
    print("=" * 80)
    print("🔍 STEP 5: SPECIAL INVESTIGATION - FCR vs SLA SWAP HYPOTHESIS")
    print("=" * 80)
    
    # Calculate both ways
    fcr_correct = len(df[df['reopened'] == 'No']) / len(df) * 100
    sla_correct = len(df[df['sla_met'] == 'Yes']) / len(df) * 100
    
    # Check if production values match the OPPOSITE metrics
    production_fcr = 77.0
    production_sla = 82.0
    
    print(f"\n📊 CORRECT CALCULATIONS:")
    print(f"   FCR (reopened='No'):  {fcr_correct:.2f}%")
    print(f"   SLA Met (sla_met='Yes'): {sla_correct:.2f}%")
    
    print(f"\n📱 PRODUCTION VALUES:")
    print(f"   Production FCR:  {production_fcr:.2f}%")
    print(f"   Production SLA:  {production_sla:.2f}%")
    
    print(f"\n🔬 SWAP DETECTION:")
    if abs(fcr_correct - production_sla) < 0.1 and abs(sla_correct - production_fcr) < 0.1:
        print(f"   ❌ CRITICAL BUG DETECTED!")
        print(f"   Production has SWAPPED FCR and SLA values!")
        print(f"   - Production FCR {production_fcr}% = Actual SLA {sla_correct:.2f}%")
        print(f"   - Production SLA {production_sla}% = Actual FCR {fcr_correct:.2f}%")
        print(f"\n   🚨 ROOT CAUSE: Code bug swapping these two metrics in display/calculation")
        return True
    else:
        print(f"   ✅ No swap detected. Values are correctly assigned.")
        print(f"   FCR difference: {abs(fcr_correct - production_fcr):.2f}%")
        print(f"   SLA difference: {abs(sla_correct - production_sla):.2f}%")
        return False
    
def generate_fix_recommendations(discrepancies, swap_detected):
    """
    Generate actionable fix recommendations based on root cause analysis.
    """
    print("=" * 80)
    print("🔧 STEP 6: FIX RECOMMENDATIONS")
    print("=" * 80)
    
    print("\n📋 REQUIRED FIXES:\n")
    
    fix_count = 0
    
    if swap_detected:
        fix_count += 1
        print(f"{fix_count}. ❌ CRITICAL: Fix FCR/SLA Swap Bug")
        print(f"   Location: src/premium_lean_pipeline.py, Customer Service KPI section")
        print(f"   Issue: FCR and SLA Met percentages are swapped in display")
        print(f"   Fix: Verify calculation logic and variable assignments")
        print(f"   Code to check:")
        print(f"      - kpis['First Contact Resolution (%)'] should use 'reopened'")
        print(f"      - kpis['SLA Met (%)'] should use 'sla_met'")
        print(f"   Impact: HIGH - Misleads users about actual performance")
        print()
    
    for disc in discrepancies:
        if disc['type'] == 'calculation_error' and disc['kpi'] == 'csat_score':
            fix_count += 1
            print(f"{fix_count}. ⚠️ MEDIUM: Investigate CSAT Calculation Method")
            print(f"   Location: src/premium_lean_pipeline.py, Customer Service CSAT calculation")
            print(f"   Issue: CSAT shows {disc['production']:.2f} vs expected {disc['baseline']:.2f}")
            print(f"   Possible causes:")
            print(f"      - Using weighted average by ticket value")
            print(f"      - Excluding certain categories")
            print(f"      - Different aggregation logic")
            print(f"   Fix: Verify CSAT is simple mean of customer_satisfaction_score")
            print(f"   Impact: MEDIUM - Affects satisfaction metric accuracy")
            print()
    
    rounding_issues = [d for d in discrepancies if d['type'] == 'rounding']
    if rounding_issues:
        fix_count += 1
        print(f"{fix_count}. ℹ️ LOW: Standardize Display Rounding")
        print(f"   Location: Dashboard display formatting")
        print(f"   Issue: Inconsistent decimal places in display")
        print(f"   Affected KPIs: {', '.join([d['kpi'] for d in rounding_issues])}")
        print(f"   Fix: Use consistent rounding (2 decimal places recommended)")
        print(f"   Impact: LOW - Display consistency for professional appearance")
        print()
    
    if fix_count == 0:
        print("✅ NO FIXES REQUIRED - All values accurate!\n")
    else:
        print(f"{'=' * 80}")
        print(f"SUMMARY: {fix_count} fix(es) required")
        print(f"{'=' * 80}\n")
    
    return fix_count

def main():
    """
    Main execution flow for root cause analysis.
    """
    print("\n")
    print("=" * 80)
    print("🔬 ROOT CAUSE ANALYSIS: CUSTOMER SERVICE KPI DISCREPANCIES")
    print("=" * 80)
    print("Date: 2025-10-23")
    print("Purpose: Identify exact cause of value differences")
    print("Philosophy: Zero tolerance - 100% accuracy required")
    print("=" * 80)
    print("\n")
    
    # Step 1: Load data
    df = load_data()
    
    # Step 2: Calculate baseline (ground truth)
    baseline_kpis = calculate_kpis_baseline(df)
    
    # Step 3: Compare with production
    discrepancies, production, expected = compare_with_production(baseline_kpis)
    
    # Step 4: Analyze discrepancies
    analyze_discrepancies(discrepancies, baseline_kpis, df)
    
    # Step 5: Special investigation - FCR/SLA swap
    swap_detected = investigate_fcr_sla_swap(df)
    
    # Step 6: Generate fix recommendations
    fix_count = generate_fix_recommendations(discrepancies, swap_detected)
    
    # Final summary
    print("=" * 80)
    print("🎯 FINAL SUMMARY")
    print("=" * 80)
    print(f"\n✅ Analysis complete!")
    print(f"   - Discrepancies found: {len(discrepancies)}")
    print(f"   - FCR/SLA swap detected: {'YES ❌' if swap_detected else 'NO ✅'}")
    print(f"   - Fixes required: {fix_count}")
    
    if swap_detected or len(discrepancies) > 0:
        print(f"\n⚠️ RECOMMENDATION: Fix issues before proceeding to Domain #7")
        print(f"   Zero tolerance philosophy: Must achieve 100% accuracy")
        print(f"   Small errors at scale = catastrophic user trust loss")
    else:
        print(f"\n✅ PRODUCTION VALIDATED: Ready for Domain #7 testing!")
    
    print(f"\n{'=' * 80}\n")

if __name__ == "__main__":
    main()
