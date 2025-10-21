"""
Error handling utilities for API rate limits and user-friendly error messages.

This module provides:
- Rate limit handling with exponential backoff
- User-friendly error message formatting
- Retry logic for transient failures
"""

import time
import functools
import streamlit as st
from typing import Callable, Any, Tuple


def rate_limit_handler(max_retries: int = 3, backoff_base: int = 2):
    """
    Decorator to handle API rate limits with exponential backoff retry.
    
    Gemini API free tier: 15 requests/minute (1 request every 4 seconds)
    
    Args:
        max_retries: Maximum number of retry attempts (default: 3)
        backoff_base: Base for exponential backoff in seconds (default: 2)
                     Retry delays: 2s, 4s, 8s
    
    Returns:
        Decorated function that handles rate limit errors
    
    Example:
        >>> @rate_limit_handler(max_retries=3, backoff_base=2)
        >>> def generate_ai_insight(client, prompt):
        >>>     response = client.models.generate_content(...)
        >>>     return (True, response.text)
    
    Behavior:
        - On rate limit error (429): Wait and retry with exponential backoff
        - On other errors: Raise immediately (no retry)
        - After max_retries: Return (False, error_message)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Tuple[bool, Any]:
            last_error = None
            
            for attempt in range(max_retries):
                try:
                    # Call the original function
                    return func(*args, **kwargs)
                
                except Exception as e:
                    error_str = str(e).lower()
                    last_error = e
                    
                    # Check if it's a rate limit error
                    is_rate_limit = any(keyword in error_str for keyword in [
                        'rate limit',
                        '429',
                        'quota',
                        'too many requests',
                        'resource exhausted'
                    ])
                    
                    if is_rate_limit and attempt < max_retries - 1:
                        # Calculate wait time with exponential backoff
                        wait_time = backoff_base ** (attempt + 1)
                        
                        # Show user-friendly warning
                        st.warning(
                            f"⏳ **Gemini API đang bận** (rate limit).\n\n"
                            f"Đang chờ {wait_time}s trước khi thử lại... "
                            f"(Lần thử {attempt + 1}/{max_retries})"
                        )
                        
                        # Wait before retry
                        time.sleep(wait_time)
                        continue
                    
                    elif is_rate_limit:
                        # Max retries exceeded
                        return (
                            False,
                            "❌ **Vượt giới hạn API Gemini** (15 requests/phút).\n\n"
                            "**Giải pháp:**\n"
                            "- Chờ 1 phút rồi thử lại\n"
                            "- Giảm số lượng chart cần phân tích\n"
                            "- Nâng cấp lên Gemini API Pro (60 req/min)"
                        )
                    
                    else:
                        # Not a rate limit error - don't retry
                        return (False, user_friendly_error(e))
            
            # Should not reach here, but just in case
            return (False, user_friendly_error(last_error))
        
        return wrapper
    return decorator


def user_friendly_error(error: Exception) -> str:
    """
    Convert technical error messages to user-friendly Vietnamese messages.
    
    Args:
        error: Exception object
    
    Returns:
        User-friendly error message in Vietnamese
    
    Example:
        >>> try:
        >>>     response = client.generate_content(...)
        >>> except Exception as e:
        >>>     st.error(user_friendly_error(e))
    """
    error_str = str(error).lower()
    
    # API Key errors
    if any(keyword in error_str for keyword in ['api key', 'authentication', 'unauthorized', '401']):
        return (
            "❌ **Lỗi API Key không hợp lệ**\n\n"
            "**Nguyên nhân:** GEMINI_API_KEY chưa được cấu hình hoặc không đúng.\n\n"
            "**Giải pháp:**\n"
            "1. Vào [Google AI Studio](https://makersuite.google.com/app/apikey)\n"
            "2. Tạo API key mới\n"
            "3. Thêm vào Streamlit Secrets (Settings → Secrets)\n"
            "4. Khởi động lại app"
        )
    
    # Rate limit errors
    if any(keyword in error_str for keyword in ['rate limit', '429', 'quota', 'too many requests']):
        return (
            "❌ **Vượt giới hạn API**\n\n"
            "Gemini API free tier: 15 requests/phút\n\n"
            "**Giải pháp:** Chờ 1 phút rồi thử lại."
        )
    
    # Network errors
    if any(keyword in error_str for keyword in ['connection', 'network', 'timeout', 'unreachable']):
        return (
            "❌ **Lỗi kết nối mạng**\n\n"
            "**Nguyên nhân:** Không thể kết nối đến Gemini API.\n\n"
            "**Giải pháp:**\n"
            "- Kiểm tra kết nối internet\n"
            "- Thử lại sau vài giây\n"
            "- Kiểm tra firewall/proxy"
        )
    
    # Model errors
    if any(keyword in error_str for keyword in ['model', 'not found', '404']):
        return (
            "❌ **Lỗi model không tồn tại**\n\n"
            "**Nguyên nhân:** Model 'gemini-2.5-flash' không khả dụng.\n\n"
            "**Giải pháp:** Kiểm tra tên model hoặc nâng cấp google-genai package."
        )
    
    # Content filtering
    if any(keyword in error_str for keyword in ['safety', 'blocked', 'filtered', 'inappropriate']):
        return (
            "⚠️ **Nội dung bị chặn bởi AI safety filter**\n\n"
            "**Nguyên nhân:** Dữ liệu hoặc câu hỏi chứa nội dung nhạy cảm.\n\n"
            "**Giải pháp:** Thử với dữ liệu hoặc câu hỏi khác."
        )
    
    # Generic error
    return (
        f"❌ **Lỗi không xác định**\n\n"
        f"**Chi tiết kỹ thuật:**\n"
        f"```\n{str(error)[:500]}\n```\n\n"
        f"**Gợi ý:** Chụp màn hình lỗi này và liên hệ support."
    )


def retry_on_failure(max_retries: int = 2, delay: float = 1.0):
    """
    Simple retry decorator for non-API operations.
    
    Args:
        max_retries: Number of retry attempts (default: 2)
        delay: Delay between retries in seconds (default: 1.0)
    
    Example:
        >>> @retry_on_failure(max_retries=2, delay=1.0)
        >>> def load_data():
        >>>     return pd.read_csv('data.csv')
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        raise e
                    time.sleep(delay)
            return None
        return wrapper
    return decorator
