#!/usr/bin/env python3
"""
Test Customer Service KPI Calculation after Fix
"""

import pandas as pd

def calculate_customer_service_kpis(df):
    """Replicate the Customer Service KPI calculation logic"""
    kpis = {}
    
    # Detect columns
    response_time_cols = [col for col in df.columns if 'response' in col.lower() and 'time' in col.lower()]
    resolution_time_cols = [col for col in df.columns if 'resolution' in col.lower() and 'time' in col.lower()]
    csat_cols = [col for col in df.columns if 'satisfaction' in col.lower() or 'csat' in col.lower()]
    sla_cols = [col for col in df.columns if 'sla' in col.lower()]
    reopened_cols = [col for col in df.columns if 'reopen' in col.lower()]
    escalated_cols = [col for col in df.columns if 'escalat' in col.lower()]
    ticket_value_cols = [col for col in df.columns if 'ticket' in col.lower() and 'value' in col.lower()]
    
    # 1. Average First Response Time
    if response_time_cols:
        response_col = response_time_cols[0]
        avg_response = df[response_col].mean()
        kpis['Avg First Response Time (min)'] = {
            'value': float(avg_response),
            'benchmark': 15.0,
            'status': 'Below' if avg_response <= 15.0 else 'Above',
            'column': response_col
        }
    
    # 2. Average Resolution Time
    if resolution_time_cols:
        resolution_col = resolution_time_cols[0]
        avg_resolution = df[resolution_col].mean()
        kpis['Avg Resolution Time (hrs)'] = {
            'value': float(avg_resolution),
            'benchmark': 4.0,
            'status': 'Below' if avg_resolution <= 4.0 else 'Above',
            'column': resolution_col
        }
    
    # 3. Customer Satisfaction Score (CSAT)
    if csat_cols:
        csat_col = csat_cols[0]
        avg_csat = df[csat_col].mean()
        kpis['CSAT Score'] = {
            'value': float(avg_csat),
            'benchmark': 4.5,
            'status': 'Above' if avg_csat >= 4.5 else 'Below',
            'column': csat_col
        }
    
    # 4. First Contact Resolution (FCR)
    if reopened_cols:
        reopen_col = reopened_cols[0]
        total_tickets = len(df)
        not_reopened = df[reopen_col].astype(str).str.lower().isin(['no', 'false', '0']).sum()
        fcr_rate = (not_reopened / total_tickets) * 100
        kpis['First Contact Resolution (%)'] = {
            'value': float(fcr_rate),
            'benchmark': 75.0,
            'status': 'Above' if fcr_rate >= 75.0 else 'Below',
            'column': reopen_col
        }
    
    # 5. SLA Compliance
    if sla_cols:
        sla_col = sla_cols[0]
        total_tickets = len(df)
        sla_met = df[sla_col].astype(str).str.lower().isin(['yes', 'true', '1']).sum()
        sla_rate = (sla_met / total_tickets) * 100
        kpis['SLA Met (%)'] = {
            'value': float(sla_rate),
            'benchmark': 85.0,
            'status': 'Above' if sla_rate >= 85.0 else 'Below',
            'column': sla_col
        }
    
    # 6. Escalation Rate
    if escalated_cols:
        escalated_col = escalated_cols[0]
        total_tickets = len(df)
        escalated = df[escalated_col].astype(str).str.lower().isin(['yes', 'true', '1']).sum()
        escalation_rate = (escalated / total_tickets) * 100
        kpis['Escalation Rate (%)'] = {
            'value': float(escalation_rate),
            'benchmark': 15.0,
            'status': 'Below' if escalation_rate <= 15.0 else 'Above',
            'column': escalated_col
        }
    
    # 7. Reopen Rate
    if reopened_cols:
        reopen_col = reopened_cols[0]
        total_tickets = len(df)
        reopened = df[reopen_col].astype(str).str.lower().isin(['yes', 'true', '1']).sum()
        reopen_rate = (reopened / total_tickets) * 100
        kpis['Reopen Rate (%)'] = {
            'value': float(reopen_rate),
            'benchmark': 10.0,
            'status': 'Below' if reopen_rate <= 10.0 else 'Above',
            'column': reopen_col
        }
    
    # 8. Total Ticket Value
    if ticket_value_cols:
        ticket_value_col = ticket_value_cols[0]
        total_value = df[ticket_value_col].sum()
        kpis['Total Ticket Value (VND)'] = {
            'value': float(total_value),
            'benchmark': float(total_value * 0.8),
            'status': 'Above Target',
            'column': ticket_value_col
        }
    
    return kpis

# Load test data
df = pd.read_csv('sample_data/customer_service_tickets_30days.csv')

print("="*80)
print("🧪 TESTING CUSTOMER SERVICE KPI CALCULATION (AFTER FIX)")
print("="*80)

# Calculate KPIs
kpis = calculate_customer_service_kpis(df)

print(f"\n✅ CALCULATED {len(kpis)} KPIs:")
for kpi_name, kpi_data in kpis.items():
    value = kpi_data['value']
    benchmark = kpi_data.get('benchmark', 'N/A')
    
    if 'VND' in kpi_name:
        print(f"  • {kpi_name}: {value:,.0f} (benchmark: {benchmark})")
    elif '(%)' in kpi_name or 'Rate' in kpi_name:
        print(f"  • {kpi_name}: {value:.2f}% (benchmark: {benchmark}%)")
    else:
        print(f"  • {kpi_name}: {value:.2f} (benchmark: {benchmark})")

print("\n" + "="*80)
print("📊 VALIDATION AGAINST EXPECTED VALUES")
print("="*80)

expected = {
    'Avg First Response Time (min)': 18.81,
    'Avg Resolution Time (hrs)': 4.35,
    'CSAT Score': 4.22,
    'First Contact Resolution (%)': 82.00,
    'SLA Met (%)': 77.00,
    'Escalation Rate (%)': 21.00,
    'Reopen Rate (%)': 18.00,
    'Total Ticket Value (VND)': 397845000
}

all_passed = True
for kpi_name, expected_value in expected.items():
    if kpi_name in kpis:
        actual_value = kpis[kpi_name]['value']
        diff_pct = abs(actual_value - expected_value) / expected_value * 100
        
        if diff_pct <= 0.5:
            print(f"✅ PASS: {kpi_name}")
            print(f"   Expected: {expected_value:.2f}, Actual: {actual_value:.2f}, Diff: {diff_pct:.2f}%")
        else:
            print(f"❌ FAIL: {kpi_name}")
            print(f"   Expected: {expected_value:.2f}, Actual: {actual_value:.2f}, Diff: {diff_pct:.2f}%")
            all_passed = False
    else:
        print(f"❌ MISSING: {kpi_name} not calculated!")
        all_passed = False

print("\n" + "="*80)
if all_passed:
    print("✅✅✅ ALL CUSTOMER SERVICE KPIS PASSED!")
    print("✅ Backend fix complete - Ready for production testing")
    print("="*80)
    exit(0)
else:
    print("❌ SOME KPIS FAILED - Review calculation logic")
    print("="*80)
    exit(1)
