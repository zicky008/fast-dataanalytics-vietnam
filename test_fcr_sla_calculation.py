#!/usr/bin/env python3
"""
Direct test of the FCR and SLA calculation logic from premium_lean_pipeline.py
"""

import pandas as pd

# Load data
df = pd.read_csv('sample_data/customer_service_tickets_30days.csv')

print("=" * 80)
print("TESTING ACTUAL CODE LOGIC FROM premium_lean_pipeline.py")
print("=" * 80)

# Detect columns (same as in pipeline)
reopened_cols = [col for col in df.columns if 'reopen' in col.lower()]
sla_cols = [col for col in df.columns if 'sla' in col.lower()]

print(f"\nDetected columns:")
print(f"  reopened_cols: {reopened_cols}")
print(f"  sla_cols: {sla_cols}")

# FCR Calculation (lines 1065-1078)
if reopened_cols:
    reopen_col = reopened_cols[0]
    total_tickets = len(df)
    # Assuming 'No' or False means not reopened (first contact resolution)
    not_reopened = df[reopen_col].astype(str).str.lower().isin(['no', 'false', '0']).sum()
    fcr_rate = (not_reopened / total_tickets) * 100
    
    print(f"\nFCR Calculation (using column '{reopen_col}'):")
    print(f"  not_reopened count: {not_reopened}")
    print(f"  total_tickets: {total_tickets}")
    print(f"  fcr_rate: {fcr_rate:.2f}%")
    
    # Show what values are in the column
    print(f"  Column value distribution: {df[reopen_col].value_counts().to_dict()}")

# SLA Calculation (lines 1080-1093)
if sla_cols:
    sla_col = sla_cols[0]
    total_tickets = len(df)
    # Assuming 'Yes' or True means SLA met
    sla_met = df[sla_col].astype(str).str.lower().isin(['yes', 'true', '1']).sum()
    sla_rate = (sla_met / total_tickets) * 100
    
    print(f"\nSLA Calculation (using column '{sla_col}'):")
    print(f"  sla_met count: {sla_met}")
    print(f"  total_tickets: {total_tickets}")
    print(f"  sla_rate: {sla_rate:.2f}%")
    
    # Show what values are in the column
    print(f"  Column value distribution: {df[sla_col].value_counts().to_dict()}")

print(f"\n{'=' * 80}")
print(f"EXPECTED vs CALCULATED:")
print(f"{'=' * 80}")
print(f"  Expected FCR: 82.00% | Calculated: {fcr_rate:.2f}%")
print(f"  Expected SLA: 77.00% | Calculated: {sla_rate:.2f}%")
print(f"\n  Match? FCR: {abs(fcr_rate - 82.0) < 0.1} | SLA: {abs(sla_rate - 77.0) < 0.1}")
print(f"{'=' * 80}\n")
