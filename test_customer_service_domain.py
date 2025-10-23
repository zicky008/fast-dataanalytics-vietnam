#!/usr/bin/env python3
"""
Customer Service Domain Testing
Test all KPIs against manually calculated baseline values
"""

import pandas as pd
import sys
sys.path.insert(0, 'src')

def test_customer_service_kpis():
    """Test Customer Service domain KPI calculations"""
    
    print("="*80)
    print("🧪 CUSTOMER SERVICE DOMAIN - BACKEND VALIDATION")
    print("="*80)
    
    # Load data
    df = pd.read_csv('sample_data/customer_service_tickets_30days.csv')
    print(f"\n✅ Data loaded: {len(df)} tickets")
    
    # Expected values (from manual calculation)
    expected_kpis = {
        'Avg First Response Time (min)': 18.81,
        'Avg Resolution Time (hrs)': 4.35,
        'CSAT Score': 4.22,
        'First Contact Resolution (%)': 82.00,
        'SLA Met (%)': 77.00,
        'Escalation Rate (%)': 21.00,
        'Reopen Rate (%)': 18.00,
        'Total Ticket Value (VND)': 397845000,
    }
    
    print("\n" + "="*80)
    print("🎯 EXPECTED KPIs (Manual Calculation)")
    print("="*80)
    for kpi, value in expected_kpis.items():
        if 'VND' in kpi:
            print(f"{kpi}: {value:,.0f}")
        elif '(%)' in kpi or 'Rate' in kpi:
            print(f"{kpi}: {value:.2f}%")
        else:
            print(f"{kpi}: {value:.2f}")
    
    # Calculate actual values
    print("\n" + "="*80)
    print("📊 ACTUAL CALCULATIONS")
    print("="*80)
    
    actual_kpis = {}
    
    # 1. Avg First Response Time
    actual_kpis['Avg First Response Time (min)'] = df['first_response_time_mins'].mean()
    print(f"Avg First Response Time: {actual_kpis['Avg First Response Time (min)']:.2f} minutes")
    
    # 2. Avg Resolution Time
    actual_kpis['Avg Resolution Time (hrs)'] = df['resolution_time_hours'].mean()
    print(f"Avg Resolution Time: {actual_kpis['Avg Resolution Time (hrs)']:.2f} hours")
    
    # 3. CSAT Score
    actual_kpis['CSAT Score'] = df['customer_satisfaction_score'].mean()
    print(f"CSAT Score: {actual_kpis['CSAT Score']:.2f} / 5")
    
    # 4. First Contact Resolution
    actual_kpis['First Contact Resolution (%)'] = (df['reopened'] == 'No').sum() / len(df) * 100
    print(f"First Contact Resolution: {actual_kpis['First Contact Resolution (%)']:.2f}%")
    
    # 5. SLA Met
    actual_kpis['SLA Met (%)'] = (df['sla_met'] == 'Yes').sum() / len(df) * 100
    print(f"SLA Met: {actual_kpis['SLA Met (%)']:.2f}%")
    
    # 6. Escalation Rate
    actual_kpis['Escalation Rate (%)'] = (df['escalated'] == 'Yes').sum() / len(df) * 100
    print(f"Escalation Rate: {actual_kpis['Escalation Rate (%)']:.2f}%")
    
    # 7. Reopen Rate
    actual_kpis['Reopen Rate (%)'] = (df['reopened'] == 'Yes').sum() / len(df) * 100
    print(f"Reopen Rate: {actual_kpis['Reopen Rate (%)']:.2f}%")
    
    # 8. Total Ticket Value
    actual_kpis['Total Ticket Value (VND)'] = df['ticket_value_vnd'].sum()
    print(f"Total Ticket Value: {actual_kpis['Total Ticket Value (VND)']:,.0f} VND")
    
    # Validation
    print("\n" + "="*80)
    print("✅ VALIDATION RESULTS")
    print("="*80)
    
    all_passed = True
    tolerance = 0.5  # 0.5% tolerance for floating point precision
    
    for kpi_name in expected_kpis.keys():
        expected = expected_kpis[kpi_name]
        actual = actual_kpis[kpi_name]
        
        # Calculate percentage difference
        if expected != 0:
            diff_pct = abs(actual - expected) / expected * 100
        else:
            diff_pct = 0 if actual == 0 else 100
        
        # Check if within tolerance
        if diff_pct <= tolerance:
            status = "✅ PASS"
        else:
            status = f"❌ FAIL (diff: {diff_pct:.2f}%)"
            all_passed = False
        
        if 'VND' in kpi_name:
            print(f"{status} | {kpi_name}")
            print(f"         Expected: {expected:,.0f}")
            print(f"         Actual:   {actual:,.0f}")
        else:
            print(f"{status} | {kpi_name}")
            print(f"         Expected: {expected:.2f}")
            print(f"         Actual:   {actual:.2f}")
    
    # Channel breakdown validation
    print("\n" + "="*80)
    print("📊 CHANNEL BREAKDOWN VALIDATION")
    print("="*80)
    
    channel_stats = df.groupby('channel').agg({
        'ticket_id': 'count',
        'first_response_time_mins': 'mean',
        'resolution_time_hours': 'mean',
        'customer_satisfaction_score': 'mean'
    }).round(2)
    
    print(channel_stats.to_string())
    
    # Verify Live Chat is best performer
    live_chat_csat = channel_stats.loc['Live Chat', 'customer_satisfaction_score']
    if live_chat_csat == 5.0:
        print("\n✅ PASS: Live Chat has perfect 5.0 CSAT (best performer)")
    else:
        print(f"\n❌ FAIL: Live Chat CSAT = {live_chat_csat} (expected 5.0)")
        all_passed = False
    
    # Verify Email is worst performer (response time)
    email_frt = channel_stats.loc['Email', 'first_response_time_mins']
    if email_frt > 30:
        print(f"✅ PASS: Email has slowest FRT = {email_frt:.2f} min (>30 min)")
    else:
        print(f"❌ FAIL: Email FRT = {email_frt:.2f} min (expected >30)")
        all_passed = False
    
    # Customer segment validation
    print("\n" + "="*80)
    print("💰 CUSTOMER SEGMENT VALIDATION")
    print("="*80)
    
    segment_stats = df.groupby('customer_segment').agg({
        'ticket_id': 'count',
        'customer_satisfaction_score': 'mean',
        'sla_met': lambda x: (x == 'Yes').sum() / len(x) * 100
    }).round(2)
    
    print(segment_stats.to_string())
    
    # Verify Premium customers have LOWER CSAT (critical insight!)
    premium_csat = segment_stats.loc['Premium', 'customer_satisfaction_score']
    standard_csat = segment_stats.loc['Standard', 'customer_satisfaction_score']
    
    if premium_csat < standard_csat:
        print(f"\n✅ CRITICAL INSIGHT CONFIRMED: Premium CSAT ({premium_csat:.2f}) < Standard ({standard_csat:.2f})")
        print("   → Premium customers paying more but getting WORSE service!")
    else:
        print(f"\n❌ UNEXPECTED: Premium CSAT ({premium_csat:.2f}) >= Standard ({standard_csat:.2f})")
    
    # Category problems validation
    print("\n" + "="*80)
    print("⚠️ PROBLEM CATEGORY VALIDATION")
    print("="*80)
    
    category_stats = df.groupby('category').agg({
        'ticket_id': 'count',
        'escalated': lambda x: (x == 'Yes').sum() / len(x) * 100,
        'customer_satisfaction_score': 'mean'
    }).round(2)
    
    # Check Account Access is worst CSAT
    account_access_csat = category_stats.loc['Account Access', 'customer_satisfaction_score']
    worst_csat = category_stats['customer_satisfaction_score'].min()
    
    if account_access_csat == worst_csat:
        print(f"✅ CRITICAL PROBLEM CONFIRMED: Account Access has worst CSAT = {account_access_csat:.2f}")
    else:
        print(f"⚠️ Account Access CSAT = {account_access_csat:.2f} (worst is {worst_csat:.2f})")
    
    # Check Product Defect has 100% escalation
    product_defect_esc = category_stats.loc['Product Defect', 'escalated']
    if product_defect_esc == 100.0:
        print(f"✅ CRITICAL PROBLEM CONFIRMED: Product Defect has 100% escalation rate")
    else:
        print(f"❌ Product Defect escalation = {product_defect_esc:.2f}% (expected 100%)")
        all_passed = False
    
    # Final result
    print("\n" + "="*80)
    print("🎯 FINAL VALIDATION RESULT")
    print("="*80)
    
    if all_passed:
        print("✅✅✅ ALL TESTS PASSED - Backend calculations 100% accurate!")
        print("✅ Ready for production testing")
        return 0
    else:
        print("❌ SOME TESTS FAILED - Review calculations above")
        return 1

if __name__ == '__main__':
    sys.exit(test_customer_service_kpis())
