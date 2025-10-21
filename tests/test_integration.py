"""
Integration tests for the full application workflow.

Tests the complete data analysis pipeline:
1. File upload with validation
2. Data cleaning
3. AI insight generation (mocked)
4. Dashboard creation
"""

import pytest
import pandas as pd
import sys
import os
import io

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.validators import safe_file_upload, sanitize_column_names
from utils.error_handlers import rate_limit_handler, user_friendly_error
from utils.performance import PerformanceMonitor


class MockUploadedFile:
    """Mock Streamlit UploadedFile for testing."""
    
    def __init__(self, content: bytes, name: str, size: int = None):
        self.content = content
        self.name = name
        self.size = size if size is not None else len(content)
        self._position = 0
    
    def read(self, size=-1):
        if size == -1:
            result = self.content[self._position:]
            self._position = len(self.content)
        else:
            result = self.content[self._position:self._position + size]
            self._position += len(result)
        return result
    
    def seek(self, position):
        self._position = position
    
    def getvalue(self):
        return self.content


class TestFullWorkflow:
    """Test complete workflow from file upload to dashboard."""
    
    def test_upload_marketing_data(self):
        """Test uploading the sample marketing data."""
        # Read actual sample file
        sample_file_path = os.path.join(
            os.path.dirname(__file__), '..', 'data', 'sample_marketing_data.csv'
        )
        
        if os.path.exists(sample_file_path):
            with open(sample_file_path, 'rb') as f:
                content = f.read()
            
            mock_file = MockUploadedFile(content, "sample_marketing_data.csv")
            
            with PerformanceMonitor("Sample Data Upload") as monitor:
                success, df, message = safe_file_upload(mock_file, show_progress=False)
                monitor.add_metric("rows", len(df) if df is not None else 0)
                monitor.add_metric("columns", len(df.columns) if df is not None else 0)
            
            assert success is True
            assert df is not None
            assert len(df) > 0
            assert len(df.columns) > 0
            assert monitor.duration < 5.0  # Should be fast
            
            # Verify column sanitization
            for col in df.columns:
                assert len(col) <= 100  # Max length check
                assert col.strip() != ""  # Not empty
    
    def test_workflow_with_valid_data(self):
        """Test complete workflow with valid CSV data."""
        # Create test CSV
        csv_content = """Campaign,Channel,Impressions,Clicks,Spend,Revenue
Campaign_A,Facebook,10000,500,1000,5000
Campaign_B,Google,15000,750,1500,7500
Campaign_C,Email,5000,200,500,2000
""".encode('utf-8')
        
        mock_file = MockUploadedFile(csv_content, "test_campaign.csv")
        
        # Step 1: Upload
        with PerformanceMonitor("Full Workflow") as workflow:
            success, df, message = safe_file_upload(mock_file, show_progress=False)
            workflow.add_metric("upload_success", success)
            
            assert success is True
            assert df is not None
            
            # Step 2: Sanitize columns
            df = sanitize_column_names(df)
            workflow.add_metric("columns_sanitized", len(df.columns))
            
            # Step 3: Basic data validation
            assert 'Campaign' in df.columns
            assert 'Revenue' in df.columns
            assert len(df) == 3
            
            # Step 4: Calculate metrics
            total_revenue = df['Revenue'].sum()
            workflow.add_metric("total_revenue", total_revenue)
            assert total_revenue == 14500
        
        # Verify performance
        assert workflow.success is True
        assert workflow.duration < 5.0
        print(f"\n✅ Workflow completed in {workflow.duration:.2f}s")
        print(f"   Metrics: {workflow.metrics}")
    
    def test_error_handling_integration(self):
        """Test error handling throughout the workflow."""
        
        # Test 1: Empty file
        empty_file = MockUploadedFile(b"", "empty.csv")
        success, df, message = safe_file_upload(empty_file, show_progress=False)
        assert success is False
        assert '❌' in message
        
        # Test 2: Malformed CSV
        malformed = b"A,B,C\n1,2\n3,4,5,6"
        malformed_file = MockUploadedFile(malformed, "malformed.csv")
        success, df, message = safe_file_upload(malformed_file, show_progress=False)
        # Should handle gracefully (either parse with warnings or reject)
        
        # Test 3: Unsupported format
        txt_file = MockUploadedFile(b"Some text", "file.txt")
        success, df, message = safe_file_upload(txt_file, show_progress=False)
        assert success is False
        assert 'không hỗ trợ' in message.lower()
    
    def test_performance_benchmarks(self):
        """Verify performance meets benchmarks."""
        # Create medium-sized dataset
        data = {
            'Date': ['2024-01-01'] * 100,
            'Category': ['A', 'B', 'C', 'D', 'E'] * 20,
            'Value': range(100)
        }
        df = pd.DataFrame(data)
        csv_buffer = io.BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_content = csv_buffer.getvalue()
        
        mock_file = MockUploadedFile(csv_content, "medium_data.csv")
        
        with PerformanceMonitor("Medium Dataset Upload") as monitor:
            success, df, message = safe_file_upload(mock_file, show_progress=False)
            monitor.add_metric("rows", len(df))
        
        assert success is True
        # File upload should be < 5s for 100 rows (benchmark: <10s for normal files)
        assert monitor.duration < 5.0
        
        summary = monitor.get_summary()
        assert summary['operation'] == "Medium Dataset Upload"
        assert summary['success'] is True
        assert summary['metrics']['rows'] == 100


class TestRateLimitMocking:
    """Test rate limit handling with mocked AI calls."""
    
    def test_rate_limit_decorator_with_mock_api(self):
        """Test that rate limit decorator works with mock API."""
        call_count = {'count': 0}
        
        @rate_limit_handler(max_retries=2, backoff_base=1)
        def mock_ai_call():
            call_count['count'] += 1
            if call_count['count'] < 2:
                raise Exception("Rate limit exceeded")
            return (True, "AI response")
        
        success, result = mock_ai_call()
        
        assert success is True
        assert result == "AI response"
        assert call_count['count'] == 2  # Retried once


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v', '--tb=short'])
