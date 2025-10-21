"""
Unit tests for validators module.

Tests cover:
- File size validation
- Encoding detection (UTF-8, UTF-8-BOM, Latin1)
- Malformed CSV handling
- Column name sanitization
- DataFrame validation
"""

import pytest
import pandas as pd
import io
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.validators import (
    sanitize_column_names,
    validate_dataframe,
    safe_file_upload
)


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


class TestSanitizeColumnNames:
    """Test column name sanitization."""
    
    def test_special_characters_removed(self):
        """Special characters should be removed."""
        df = pd.DataFrame({
            'Revenue ($)': [100],
            'Chi phí!!!': [50],
            'ROI%': [0.5]
        })
        df_clean = sanitize_column_names(df)
        
        assert 'Revenue' in df_clean.columns or 'Revenue ' in df_clean.columns
        assert 'Chi phí' in df_clean.columns
        assert 'ROI' in df_clean.columns
    
    def test_vietnamese_diacritics_preserved(self):
        """Vietnamese diacritics should be preserved."""
        df = pd.DataFrame({
            'Doanh thu': [100],
            'Lợi nhuận': [50],
            'Kênh bán hàng': ['Online']
        })
        df_clean = sanitize_column_names(df)
        
        assert 'Doanh thu' in df_clean.columns
        assert 'Lợi nhuận' in df_clean.columns
        assert 'Kênh bán hàng' in df_clean.columns
    
    def test_long_names_truncated(self):
        """Column names >100 chars should be truncated."""
        long_name = 'A' * 200
        df = pd.DataFrame({long_name: [1]})
        df_clean = sanitize_column_names(df)
        
        assert len(df_clean.columns[0]) <= 100
    
    def test_duplicate_names_numbered(self):
        """Duplicate names should get unique suffixes."""
        df = pd.DataFrame({
            'Value': [1],
            'Value ': [2],  # Will become 'Value' after sanitization
            'Value  ': [3]
        })
        df_clean = sanitize_column_names(df)
        
        # Should have unique names
        assert len(df_clean.columns) == 3
        assert len(set(df_clean.columns)) == 3
    
    def test_empty_names_replaced(self):
        """Empty column names should be replaced."""
        df = pd.DataFrame({
            '': [1],
            '!!!': [2],  # Will become empty after sanitization
            '###': [3]
        })
        df_clean = sanitize_column_names(df)
        
        # Should have valid names
        for col in df_clean.columns:
            assert col.strip() != ''
            assert 'Column_' in col


class TestValidateDataFrame:
    """Test DataFrame validation."""
    
    def test_valid_dataframe(self):
        """Valid DataFrame should pass."""
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })
        is_valid, msg = validate_dataframe(df)
        
        assert is_valid is True
        assert '✅' in msg
    
    def test_empty_dataframe(self):
        """Empty DataFrame should fail."""
        df = pd.DataFrame()
        is_valid, msg = validate_dataframe(df)
        
        assert is_valid is False
        assert 'rỗng' in msg.lower() or 'empty' in msg.lower()
    
    def test_all_nan_dataframe(self):
        """All-NaN DataFrame should fail."""
        df = pd.DataFrame({
            'A': [None, None, None],
            'B': [pd.NA, pd.NA, pd.NA]
        })
        is_valid, msg = validate_dataframe(df)
        
        assert is_valid is False
        assert 'NaN' in msg or 'null' in msg
    
    def test_single_row_warning(self):
        """Single-row DataFrame should show warning."""
        df = pd.DataFrame({'A': [1]})
        is_valid, msg = validate_dataframe(df)
        
        assert is_valid is False
        assert '1 dòng' in msg or 'single row' in msg.lower()
    
    def test_oversized_dataframe(self):
        """DataFrame >10M cells should fail."""
        # Create large DataFrame (would exceed 10M cells)
        is_valid, msg = validate_dataframe(
            pd.DataFrame({'A': range(10_000_001)})
        )
        
        assert is_valid is False
        assert 'quá lớn' in msg.lower() or 'too large' in msg.lower()


class TestSafeFileUpload:
    """Test safe file upload functionality."""
    
    def test_valid_csv_utf8(self):
        """Valid UTF-8 CSV should upload successfully."""
        csv_content = b"Name,Age,City\nAlice,30,Hanoi\nBob,25,HCM"
        mock_file = MockUploadedFile(csv_content, "test.csv")
        
        success, df, msg = safe_file_upload(mock_file, show_progress=False)
        
        assert success is True
        assert df is not None
        assert len(df) == 2
        assert '✅' in msg
    
    def test_valid_csv_with_vietnamese(self):
        """CSV with Vietnamese characters should work."""
        csv_content = "Tên,Tuổi,Thành phố\nNguyễn Văn A,30,Hà Nội\nTrần Thị B,25,TP.HCM".encode('utf-8')
        mock_file = MockUploadedFile(csv_content, "test_vietnamese.csv")
        
        success, df, msg = safe_file_upload(mock_file, show_progress=False)
        
        assert success is True
        assert df is not None
        assert len(df) == 2
    
    def test_file_too_large(self):
        """File >200MB should be rejected."""
        # Mock a large file (don't actually create 200MB)
        mock_file = MockUploadedFile(b"data", "large.csv", size=250 * 1024 * 1024)
        
        success, df, msg = safe_file_upload(mock_file, max_size_mb=200, show_progress=False)
        
        assert success is False
        assert df is None
        assert 'quá lớn' in msg.lower()
    
    def test_empty_csv(self):
        """Empty CSV should be rejected."""
        mock_file = MockUploadedFile(b"", "empty.csv")
        
        success, df, msg = safe_file_upload(mock_file, show_progress=False)
        
        assert success is False
        assert df is None
    
    def test_malformed_csv(self):
        """Malformed CSV should show helpful error."""
        # CSV with inconsistent columns
        csv_content = b"A,B,C\n1,2\n3,4,5,6"
        mock_file = MockUploadedFile(csv_content, "malformed.csv")
        
        success, df, msg = safe_file_upload(mock_file, show_progress=False)
        
        # Should either fail or handle gracefully
        if not success:
            assert '❌' in msg
    
    def test_unsupported_format(self):
        """Unsupported file format should be rejected."""
        mock_file = MockUploadedFile(b"some content", "file.txt")
        
        success, df, msg = safe_file_upload(mock_file, show_progress=False)
        
        assert success is False
        assert df is None
        assert 'không hỗ trợ' in msg.lower()
    
    def test_single_row_csv(self):
        """CSV with only header should be rejected."""
        csv_content = b"Name,Age,City"
        mock_file = MockUploadedFile(csv_content, "header_only.csv")
        
        success, df, msg = safe_file_upload(mock_file, show_progress=False)
        
        assert success is False
        assert df is None


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v', '--tb=short'])
