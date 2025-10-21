"""
Data validation utilities for file uploads and data quality checks.

This module provides robust validation for:
- File size limits
- Encoding detection
- Column name sanitization
- DataFrame quality checks
"""

import re
import pandas as pd
import streamlit as st
from typing import Tuple, Optional
import chardet


def safe_file_upload(
    uploaded_file,
    max_size_mb: int = 200,
    show_progress: bool = True
) -> Tuple[bool, Optional[pd.DataFrame], str]:
    """
    Safely upload and parse CSV/Excel files with comprehensive error handling.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        max_size_mb: Maximum file size in MB (default: 200)
        show_progress: Show progress bar during upload (default: True)
    
    Returns:
        Tuple of (success: bool, dataframe: pd.DataFrame or None, message: str)
    
    Example:
        >>> success, df, msg = safe_file_upload(uploaded_file)
        >>> if success:
        >>>     st.success(msg)
        >>>     st.dataframe(df)
        >>> else:
        >>>     st.error(msg)
    """
    try:
        # Check file size
        file_size_mb = uploaded_file.size / (1024 * 1024)
        
        if file_size_mb > max_size_mb:
            return (
                False,
                None,
                f"❌ File quá lớn: {file_size_mb:.1f}MB (giới hạn: {max_size_mb}MB). "
                f"Vui lòng giảm kích thước file hoặc chia nhỏ dữ liệu."
            )
        
        # Show progress for large files
        if show_progress and file_size_mb > 5:
            progress_bar = st.progress(0)
            st.info(f"⏳ Đang tải file {file_size_mb:.1f}MB...")
        
        # Determine file type
        file_name = uploaded_file.name.lower()
        
        # Parse based on file extension
        if file_name.endswith('.csv'):
            # Try UTF-8 first
            try:
                if show_progress and file_size_mb > 5:
                    progress_bar.progress(30)
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                # Fallback: Detect encoding
                uploaded_file.seek(0)
                raw_data = uploaded_file.read(10000)  # Read first 10KB
                detected = chardet.detect(raw_data)
                detected_encoding = detected.get('encoding', 'latin1')
                
                uploaded_file.seek(0)
                try:
                    df = pd.read_csv(uploaded_file, encoding=detected_encoding)
                    st.warning(f"⚠️ File được đọc với encoding: {detected_encoding}")
                except Exception:
                    # Last resort: latin1 always works
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding='latin1')
                    st.warning("⚠️ File được đọc với encoding: latin1 (có thể có lỗi tiếng Việt)")
        
        elif file_name.endswith(('.xlsx', '.xls')):
            if show_progress and file_size_mb > 5:
                progress_bar.progress(30)
            
            engine = 'openpyxl' if file_name.endswith('.xlsx') else 'xlrd'
            df = pd.read_excel(uploaded_file, engine=engine)
        
        else:
            return (
                False,
                None,
                f"❌ Định dạng file không hỗ trợ: {file_name}. "
                f"Chỉ chấp nhận: .csv, .xlsx, .xls"
            )
        
        if show_progress and file_size_mb > 5:
            progress_bar.progress(60)
        
        # Validate dataframe
        is_valid, validation_msg = validate_dataframe(df)
        if not is_valid:
            return (False, None, validation_msg)
        
        # Sanitize column names
        df = sanitize_column_names(df)
        
        if show_progress and file_size_mb > 5:
            progress_bar.progress(100)
            st.success(f"✅ Upload thành công: {len(df):,} dòng × {len(df.columns)} cột")
        
        return (
            True,
            df,
            f"✅ File đã được tải thành công: {len(df):,} dòng, {len(df.columns)} cột"
        )
    
    except pd.errors.EmptyDataError:
        return (False, None, "❌ File rỗng. Vui lòng kiểm tra lại file CSV/Excel.")
    
    except pd.errors.ParserError as e:
        return (
            False,
            None,
            f"❌ Lỗi parse file CSV. File có thể bị lỗi format:\n{str(e)[:200]}"
        )
    
    except Exception as e:
        return (
            False,
            None,
            f"❌ Lỗi không xác định khi đọc file:\n{str(e)[:200]}\n\n"
            f"Gợi ý: Kiểm tra file có đúng format CSV/Excel không?"
        )


def sanitize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sanitize column names to prevent SQL injection and XSS attacks.
    
    - Remove special characters (keep Vietnamese, alphanumeric, spaces, hyphens)
    - Trim whitespace
    - Limit to 100 characters
    - Ensure uniqueness
    
    Args:
        df: Input DataFrame
    
    Returns:
        DataFrame with sanitized column names
    
    Example:
        >>> df.columns = ['Revenue ($)', 'Chi phí!!!', 'ROI%', 'A' * 200]
        >>> df = sanitize_column_names(df)
        >>> df.columns
        ['Revenue', 'Chi phí', 'ROI', 'AAA...A']  # Max 100 chars
    """
    new_cols = {}
    seen_names = {}
    
    for col in df.columns:
        # Remove special characters, keep Vietnamese diacritics
        # Allow: a-z, A-Z, 0-9, Vietnamese (À-ỹ), spaces, hyphens, underscores
        safe_name = re.sub(r'[^\w\sÀ-ỹ\-]', '', str(col))
        
        # Trim and limit length
        safe_name = safe_name.strip()[:100]
        
        # Handle empty names
        if not safe_name:
            safe_name = f"Column_{len(new_cols) + 1}"
        
        # Ensure uniqueness
        if safe_name in seen_names:
            seen_names[safe_name] += 1
            safe_name = f"{safe_name}_{seen_names[safe_name]}"
        else:
            seen_names[safe_name] = 0
        
        new_cols[col] = safe_name
    
    return df.rename(columns=new_cols)


def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate DataFrame quality and structure.
    
    Checks:
    - Not empty
    - Has at least 1 row and 1 column
    - Not all NaN
    - Reasonable size (<10M cells)
    
    Args:
        df: DataFrame to validate
    
    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    # Check empty
    if df is None or df.empty:
        return (False, "❌ DataFrame rỗng. Không có dữ liệu để phân tích.")
    
    # Check dimensions
    rows, cols = df.shape
    if rows == 0:
        return (False, "❌ DataFrame không có dòng dữ liệu nào.")
    
    if cols == 0:
        return (False, "❌ DataFrame không có cột nào.")
    
    # Check if all NaN
    if df.isna().all().all():
        return (False, "❌ Tất cả giá trị trong DataFrame đều là NaN/null.")
    
    # Check size (prevent memory issues)
    total_cells = rows * cols
    if total_cells > 10_000_000:  # 10M cells
        return (
            False,
            f"❌ DataFrame quá lớn: {rows:,} dòng × {cols} cột = {total_cells:,} cells.\n"
            f"Giới hạn: 10,000,000 cells. Vui lòng giảm kích thước dữ liệu."
        )
    
    # Check for single row (might be header issue)
    if rows == 1:
        return (
            False,
            "⚠️ DataFrame chỉ có 1 dòng. Có thể file CSV thiếu dữ liệu hoặc header không đúng?"
        )
    
    return (True, f"✅ DataFrame hợp lệ: {rows:,} dòng × {cols} cột")


def detect_encoding(file_path: str, sample_size: int = 10000) -> str:
    """
    Detect file encoding using chardet library.
    
    Args:
        file_path: Path to file
        sample_size: Number of bytes to sample (default: 10KB)
    
    Returns:
        Detected encoding (e.g., 'utf-8', 'latin1', 'windows-1252')
    """
    with open(file_path, 'rb') as f:
        raw_data = f.read(sample_size)
        result = chardet.detect(raw_data)
        return result.get('encoding', 'utf-8')
