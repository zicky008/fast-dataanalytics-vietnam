"""
Comprehensive Manufacturing KPIs Test Suite
Zero tolerance validation - Same rigor as Finance domain

Author: QA Engineer (20 years manufacturing testing experience)
Standard: Six Sigma quality (99.99966% accuracy)
"""

import pytest
import pandas as pd
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from premium_lean_pipeline import PremiumLeanPipeline


class TestManufacturingKPIsAccuracy:
    """Test Manufacturing KPI calculations with 10 decimal precision"""
    
    @pytest.fixture
    def manufacturing_data(self):
        """Load manufacturing production dataset"""
        csv_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'sample_data', 
            'manufacturing_production_30days.csv'
        )
        return pd.read_csv(csv_path)
    
    @pytest.fixture
    def pipeline(self):
        """Create pipeline instance with mock client"""
        class MockClient:
            pass
        return PremiumLeanPipeline(MockClient())
    
    @pytest.fixture
    def ground_truth(self, manufacturing_data):
        """Calculate ground truth values with high precision"""
        df = manufacturing_data
        
        total_units = df['units_produced'].sum()
        total_good = df['good_units'].sum()
        total_defective = df['defective_units'].sum()
        total_available = df['available_hours'].sum()
        total_downtime = df['downtime_hours'].sum()
        total_actual_run = df['actual_run_hours'].sum()
        total_theoretical = df['theoretical_max_output'].sum()
        total_cost = df['total_cost_vnd'].sum()
        num_shifts = len(df)
        
        # Calculate all KPIs
        fpy = (total_good / total_units) * 100
        defect_rate = (total_defective / total_units) * 100
        avg_output = total_units / num_shifts
        cycle_time = (total_available * 60) / total_units
        utilization = (total_actual_run / total_available) * 100
        avg_downtime = total_downtime / num_shifts
        cost_per_unit = total_cost / total_units
        
        # OEE components
        availability = (total_available - total_downtime) / total_available
        performance = total_units / total_theoretical
        quality = total_good / total_units
        oee = availability * performance * quality * 100
        
        return {
            'First Pass Yield (%)': fpy,
            'Defect Rate (%)': defect_rate,
            'Avg Production Output (units/shift)': avg_output,
            'Cycle Time (min/unit)': cycle_time,
            'Machine Utilization (%)': utilization,
            'Total Downtime (hours)': total_downtime,
            'Avg Downtime (hours/shift)': avg_downtime,
            'Cost per Unit (VND)': cost_per_unit,
            'OEE - Overall Equipment Effectiveness (%)': oee,
            'OEE_Availability': availability * 100,
            'OEE_Performance': performance * 100,
            'OEE_Quality': quality * 100
        }
    
    def test_all_kpis_extracted(self, pipeline, manufacturing_data):
        """Test that all 9 Manufacturing KPIs are extracted"""
        kpis = pipeline._calculate_real_kpis(
            manufacturing_data, 
            {'domain': 'manufacturing'}
        )
        
        assert len(kpis) >= 9, f"Expected at least 9 KPIs, got {len(kpis)}"
        
        required_kpis = [
            'First Pass Yield (%)',
            'Defect Rate (%)',
            'Avg Production Output (units/shift)',
            'Cycle Time (min/unit)',
            'Machine Utilization (%)',
            'Total Downtime (hours)',
            'Avg Downtime (hours/shift)',
            'Cost per Unit (VND)',
            'OEE - Overall Equipment Effectiveness (%)'
        ]
        
        for required_kpi in required_kpis:
            found = any(required_kpi in kpi_name for kpi_name in kpis.keys())
            assert found, f"Missing required KPI: {required_kpi}"
    
    def test_fpy_accuracy(self, pipeline, manufacturing_data, ground_truth):
        """Test First Pass Yield (FPY) calculation accuracy"""
        kpis = pipeline._calculate_real_kpis(
            manufacturing_data, 
            {'domain': 'manufacturing'}
        )
        
        fpy_kpi = [kpi for kpi in kpis.keys() if 'First Pass Yield' in kpi][0]
        pipeline_value = kpis[fpy_kpi]['value']
        expected_value = ground_truth['First Pass Yield (%)']
        
        diff = abs(pipeline_value - expected_value)
        
        assert diff < 1e-10, (
            f"FPY accuracy failed!\n"
            f"Expected: {expected_value:.10f}\n"
            f"Got:      {pipeline_value:.10f}\n"
            f"Diff:     {diff:.15e}"
        )
    
    def test_defect_rate_accuracy(self, pipeline, manufacturing_data, ground_truth):
        """Test Defect Rate calculation accuracy"""
        kpis = pipeline._calculate_real_kpis(
            manufacturing_data, 
            {'domain': 'manufacturing'}
        )
        
        defect_kpi = [kpi for kpi in kpis.keys() if 'Defect Rate' in kpi][0]
        pipeline_value = kpis[defect_kpi]['value']
        expected_value = ground_truth['Defect Rate (%)']
        
        diff = abs(pipeline_value - expected_value)
        
        assert diff < 1e-10, (
            f"Defect Rate accuracy failed!\n"
            f"Expected: {expected_value:.10f}\n"
            f"Got:      {pipeline_value:.10f}\n"
            f"Diff:     {diff:.15e}"
        )
    
    def test_oee_accuracy(self, pipeline, manufacturing_data, ground_truth):
        """Test OEE (Overall Equipment Effectiveness) accuracy"""
        kpis = pipeline._calculate_real_kpis(
            manufacturing_data, 
            {'domain': 'manufacturing'}
        )
        
        oee_kpi = [kpi for kpi in kpis.keys() if 'OEE' in kpi][0]
        pipeline_value = kpis[oee_kpi]['value']
        expected_value = ground_truth['OEE - Overall Equipment Effectiveness (%)']
        
        diff = abs(pipeline_value - expected_value)
        
        assert diff < 1e-10, (
            f"OEE accuracy failed!\n"
            f"Expected: {expected_value:.10f}\n"
            f"Got:      {pipeline_value:.10f}\n"
            f"Diff:     {diff:.15e}"
        )
        
        # Validate OEE components
        if 'components' in kpis[oee_kpi]:
            components = kpis[oee_kpi]['components']
            
            avail_diff = abs(components['Availability'] - ground_truth['OEE_Availability'])
            perf_diff = abs(components['Performance'] - ground_truth['OEE_Performance'])
            qual_diff = abs(components['Quality'] - ground_truth['OEE_Quality'])
            
            assert avail_diff < 1e-10, f"OEE Availability component off by {avail_diff:.15e}"
            assert perf_diff < 1e-10, f"OEE Performance component off by {perf_diff:.15e}"
            assert qual_diff < 1e-10, f"OEE Quality component off by {qual_diff:.15e}"
    
    def test_all_kpis_10_decimal_accuracy(self, pipeline, manufacturing_data, ground_truth):
        """CRITICAL TEST: Validate ALL KPIs at 10 decimal places precision"""
        kpis = pipeline._calculate_real_kpis(
            manufacturing_data, 
            {'domain': 'manufacturing'}
        )
        
        tolerance = 1e-10
        failures = []
        
        for expected_name, expected_value in ground_truth.items():
            if expected_name.startswith('OEE_'):
                continue  # Skip OEE components (tested separately)
            
            # Find matching KPI
            matched_kpi = None
            for kpi_name in kpis.keys():
                if expected_name in kpi_name or kpi_name in expected_name:
                    matched_kpi = kpi_name
                    break
            
            if matched_kpi is None:
                failures.append(f"KPI '{expected_name}' not found in pipeline output")
                continue
            
            pipeline_value = kpis[matched_kpi]['value']
            diff = abs(pipeline_value - expected_value)
            
            if diff >= tolerance:
                failures.append(
                    f"{expected_name}:\n"
                    f"  Expected: {expected_value:.10f}\n"
                    f"  Got:      {pipeline_value:.10f}\n"
                    f"  Diff:     {diff:.15e}"
                )
        
        assert len(failures) == 0, (
            f"\n{'='*80}\n"
            f"❌ VALIDATION FAILED - {len(failures)} KPI(s) failed accuracy test:\n"
            f"{'='*80}\n" +
            "\n\n".join(failures)
        )
    
    def test_kpi_business_logic(self, pipeline, manufacturing_data):
        """Test business logic constraints and relationships"""
        kpis = pipeline._calculate_real_kpis(
            manufacturing_data, 
            {'domain': 'manufacturing'}
        )
        
        # FPY + Defect Rate should equal 100%
        fpy_kpi = [kpi for kpi in kpis.keys() if 'First Pass Yield' in kpi][0]
        defect_kpi = [kpi for kpi in kpis.keys() if 'Defect Rate' in kpi][0]
        
        fpy_value = kpis[fpy_kpi]['value']
        defect_value = kpis[defect_kpi]['value']
        
        sum_value = fpy_value + defect_value
        assert abs(sum_value - 100.0) < 1e-10, (
            f"FPY + Defect Rate should equal 100%\n"
            f"FPY: {fpy_value:.10f}%\n"
            f"Defect Rate: {defect_value:.10f}%\n"
            f"Sum: {sum_value:.10f}%"
        )
        
        # OEE should be between 0 and 100
        oee_kpi = [kpi for kpi in kpis.keys() if 'OEE' in kpi][0]
        oee_value = kpis[oee_kpi]['value']
        
        assert 0 <= oee_value <= 100, f"OEE must be 0-100%, got {oee_value:.2f}%"
        
        # Machine Utilization should be between 0 and 100
        util_kpi = [kpi for kpi in kpis.keys() if 'Machine Utilization' in kpi][0]
        util_value = kpis[util_kpi]['value']
        
        assert 0 <= util_value <= 100, f"Utilization must be 0-100%, got {util_value:.2f}%"
    
    def test_kpi_metadata_completeness(self, pipeline, manufacturing_data):
        """Test that all KPIs have required metadata"""
        kpis = pipeline._calculate_real_kpis(
            manufacturing_data, 
            {'domain': 'manufacturing'}
        )
        
        for kpi_name, kpi_data in kpis.items():
            assert 'value' in kpi_data, f"{kpi_name} missing 'value'"
            assert 'benchmark' in kpi_data, f"{kpi_name} missing 'benchmark'"
            assert 'status' in kpi_data, f"{kpi_name} missing 'status'"
            assert 'column' in kpi_data, f"{kpi_name} missing 'column'"
            assert 'insight' in kpi_data, f"{kpi_name} missing 'insight'"
            
            # Validate status values
            assert kpi_data['status'] in ['Above', 'Below', 'At Target'], (
                f"{kpi_name} has invalid status: {kpi_data['status']}"
            )


class TestManufacturingEdgeCases:
    """Test edge cases and error handling"""
    
    @pytest.fixture
    def pipeline(self):
        """Create pipeline instance"""
        class MockClient:
            pass
        return PremiumLeanPipeline(MockClient())
    
    def test_empty_dataframe(self, pipeline):
        """Test handling of empty dataframe"""
        df = pd.DataFrame(columns=[
            'units_produced', 'good_units', 'defective_units',
            'downtime_hours', 'available_hours', 'actual_run_hours',
            'theoretical_max_output', 'total_cost_vnd'
        ])
        
        kpis = pipeline._calculate_real_kpis(df, {'domain': 'manufacturing'})
        
        # Should return empty or handle gracefully (no crash)
        assert isinstance(kpis, dict)
    
    def test_single_row(self, pipeline):
        """Test with single production record"""
        df = pd.DataFrame({
            'units_produced': [950],
            'good_units': [920],
            'defective_units': [30],
            'downtime_hours': [0.5],
            'available_hours': [8],
            'actual_run_hours': [7.5],
            'theoretical_max_output': [1000],
            'total_cost_vnd': [28500000]
        })
        
        kpis = pipeline._calculate_real_kpis(df, {'domain': 'manufacturing'})
        
        # Should calculate KPIs correctly
        assert len(kpis) > 0
        
        # Verify FPY = 920/950 = 96.84%
        fpy_kpi = [kpi for kpi in kpis.keys() if 'First Pass Yield' in kpi][0]
        expected_fpy = (920 / 950) * 100
        actual_fpy = kpis[fpy_kpi]['value']
        
        assert abs(actual_fpy - expected_fpy) < 1e-10


if __name__ == '__main__':
    # Run tests with verbose output
    pytest.main([__file__, '-v', '--tb=short'])
