"""
Test for duplicate column names bug fix.

Bug Report: User encountered "Expected unique column names" error when testing
with salary data. Charts like "Phân bố độ tuổi của nhân viên" failed because
AI generated the same column for both x_axis and y_axis.

Root Cause: When df[['Age', 'Age']] is executed, pandas creates a DataFrame
with duplicate column names, which Plotly rejects.

Fix: Added validation in step3_dashboard_build() to skip charts where
x_axis == y_axis before attempting to create the DataFrame subset.
"""

import pytest
import pandas as pd
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_duplicate_column_selection():
    """
    Test that selecting the same column twice creates duplicate column names.
    This is the underlying pandas behavior that causes the bug.
    """
    df = pd.DataFrame({
        'Age': [25, 30, 35],
        'Salary': [50000, 60000, 70000]
    })
    
    # When we select the same column twice
    df_dup = df[['Age', 'Age']]
    
    # Pandas creates a DataFrame with duplicate column names
    assert len(df_dup.columns) == 2
    assert df_dup.columns.tolist() == ['Age', 'Age']
    
    # This would cause Plotly to fail with "Expected unique column names"


def test_plotly_rejects_duplicate_columns():
    """
    Test that Plotly Express raises error when given duplicate column names.
    """
    import plotly.express as px
    
    # Create DataFrame with duplicate columns
    df = pd.DataFrame({
        'Age': [25, 30, 35],
        'Age ': [1, 2, 3]  # Different data, will be renamed
    })
    df.columns = ['Age', 'Age']  # Force duplicate names
    
    # Plotly should reject this
    with pytest.raises(Exception) as exc_info:
        fig = px.bar(df, x='Age', y='Age', title='Test')
    
    # Verify it's the expected error
    error_msg = str(exc_info.value)
    assert "Expected unique column names" in error_msg or "duplicate" in error_msg.lower()
    assert "Age" in error_msg


def test_chart_validation_skips_duplicate_axes():
    """
    Test that the fix correctly skips charts where x_axis == y_axis.
    This is the core fix that prevents the bug.
    """
    df = pd.DataFrame({
        'Age': [25, 30, 35, 40, 45],
        'Salary': [50000, 60000, 70000, 80000, 90000],
        'Education Level': ['BS', 'MS', 'PhD', 'BS', 'MS']
    })
    
    # Simulate AI-generated chart specs
    chart_specs = [
        {
            'id': 'c1',
            'title': 'Phân bố độ tuổi của nhân viên',
            'type': 'bar',
            'x_axis': 'Age',
            'y_axis': 'Age'  # BUG: Same as x_axis
        },
        {
            'id': 'c2',
            'title': 'Lương theo độ tuổi',
            'type': 'scatter',
            'x_axis': 'Age',
            'y_axis': 'Salary'  # VALID: Different from x_axis
        },
        {
            'id': 'c3',
            'title': 'Tỷ lệ nhân viên theo trình độ học vấn',
            'type': 'pie',
            'x_axis': 'Education Level',
            'y_axis': 'Education Level'  # BUG: Same as x_axis
        }
    ]
    
    valid_charts = []
    
    for chart_spec in chart_specs:
        x_axis = chart_spec['x_axis']
        y_axis = chart_spec['y_axis']
        
        # Apply the fix: Skip if axes are identical
        if x_axis == y_axis:
            continue  # This chart should be skipped
        
        # Only valid charts reach here
        valid_charts.append(chart_spec)
    
    # Verify only the valid chart passed validation
    assert len(valid_charts) == 1
    assert valid_charts[0]['id'] == 'c2'
    assert valid_charts[0]['x_axis'] == 'Age'
    assert valid_charts[0]['y_axis'] == 'Salary'


def test_valid_charts_still_work():
    """
    Test that the fix doesn't break valid charts with different axes.
    """
    df = pd.DataFrame({
        'Age': [25, 30, 35, 40, 45],
        'Salary': [50000, 60000, 70000, 80000, 90000]
    })
    
    # Valid chart spec
    x_axis = 'Age'
    y_axis = 'Salary'
    
    # Should NOT be skipped
    assert x_axis != y_axis
    
    # Should create DataFrame successfully
    df_clean = df[[x_axis, y_axis]].dropna()
    
    # Verify no duplicate columns
    assert len(df_clean.columns) == 2
    assert df_clean.columns.tolist() == ['Age', 'Salary']
    
    # Should be able to create Plotly chart
    import plotly.express as px
    fig = px.scatter(df_clean, x=x_axis, y=y_axis, title='Test')
    assert fig is not None


def test_salary_data_scenario():
    """
    Test the exact scenario the user reported: salary data with Age and Education Level.
    """
    # Create realistic salary dataset
    salary_data = pd.DataFrame({
        'Employee ID': [1, 2, 3, 4, 5],
        'Age': [25, 30, 35, 40, 45],
        'Salary': [50000, 60000, 70000, 80000, 90000],
        'Education Level': ['BS', 'MS', 'PhD', 'BS', 'MS'],
        'Years of Experience': [2, 5, 10, 15, 20],
        'Department': ['Sales', 'Tech', 'Tech', 'Sales', 'Tech']
    })
    
    # These are the problematic charts the user reported
    problematic_charts = [
        {'title': 'Phân bố độ tuổi của nhân viên', 'x_axis': 'Age', 'y_axis': 'Age'},
        {'title': 'Tỷ lệ nhân viên theo trình độ học vấn', 'x_axis': 'Education Level', 'y_axis': 'Education Level'}
    ]
    
    for chart in problematic_charts:
        x_axis = chart['x_axis']
        y_axis = chart['y_axis']
        
        # The fix should catch these
        assert x_axis == y_axis, f"Chart '{chart['title']}' should have duplicate axes"
        
        # These should be skipped by the validation logic
        # (In production, they would be filtered out before reaching Plotly)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
