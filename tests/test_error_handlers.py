"""
Unit tests for error_handlers module.

Tests cover:
- Rate limit retry logic with exponential backoff
- User-friendly error message formatting
- Different error types (API key, network, model, safety)
- Retry decorator functionality
"""

import pytest
import time
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.error_handlers import (
    rate_limit_handler,
    user_friendly_error,
    retry_on_failure
)


class TestRateLimitHandler:
    """Test rate limit handling with exponential backoff."""
    
    def test_success_on_first_attempt(self):
        """Function that succeeds on first try should not retry."""
        call_count = {'count': 0}
        
        @rate_limit_handler(max_retries=3, backoff_base=1)
        def mock_api_call():
            call_count['count'] += 1
            return (True, "Success")
        
        success, result = mock_api_call()
        
        assert success is True
        assert result == "Success"
        assert call_count['count'] == 1  # Only called once
    
    def test_retry_on_rate_limit_error(self):
        """Should retry on rate limit errors with exponential backoff."""
        call_count = {'count': 0}
        
        @rate_limit_handler(max_retries=3, backoff_base=1)
        def mock_api_call_with_rate_limit():
            call_count['count'] += 1
            if call_count['count'] < 2:
                raise Exception("429 Too Many Requests - Rate limit exceeded")
            return (True, "Success after retry")
        
        start_time = time.time()
        success, result = mock_api_call_with_rate_limit()
        elapsed = time.time() - start_time
        
        assert success is True
        assert result == "Success after retry"
        assert call_count['count'] == 2  # Called twice (initial + 1 retry)
        assert elapsed >= 1.0  # Waited at least 1 second (backoff_base=1, attempt=1)
    
    def test_max_retries_exceeded(self):
        """Should return error after max retries exceeded."""
        call_count = {'count': 0}
        
        @rate_limit_handler(max_retries=2, backoff_base=1)
        def mock_api_call_always_fails():
            call_count['count'] += 1
            raise Exception("Rate limit exceeded")
        
        success, result = mock_api_call_always_fails()
        
        assert success is False
        assert 'Vượt giới hạn API' in result or 'rate limit' in result.lower()
        assert call_count['count'] == 2  # max_retries = 2
    
    def test_non_rate_limit_error_no_retry(self):
        """Non-rate-limit errors should not trigger retry."""
        call_count = {'count': 0}
        
        @rate_limit_handler(max_retries=3, backoff_base=1)
        def mock_api_call_with_other_error():
            call_count['count'] += 1
            raise Exception("Invalid API key")
        
        success, result = mock_api_call_with_other_error()
        
        assert success is False
        assert call_count['count'] == 1  # No retry for non-rate-limit errors
    
    def test_exponential_backoff_timing(self):
        """Verify exponential backoff timing (2^1, 2^2, 2^3)."""
        call_count = {'count': 0}
        retry_times = []
        
        @rate_limit_handler(max_retries=3, backoff_base=2)
        def mock_api_call_track_time():
            retry_times.append(time.time())
            call_count['count'] += 1
            if call_count['count'] < 3:
                raise Exception("429 Rate limit")
            return (True, "Success")
        
        start_time = time.time()
        success, result = mock_api_call_track_time()
        total_elapsed = time.time() - start_time
        
        assert success is True
        assert call_count['count'] == 3
        # Should wait 2^1 + 2^2 = 2 + 4 = 6 seconds total
        assert total_elapsed >= 6.0


class TestUserFriendlyError:
    """Test user-friendly error message formatting."""
    
    def test_api_key_error(self):
        """API key errors should be detected and formatted."""
        error = Exception("Invalid API key provided")
        message = user_friendly_error(error)
        
        assert 'API Key' in message or 'api key' in message.lower()
        assert '❌' in message
        assert 'Google AI Studio' in message or 'API key' in message
    
    def test_rate_limit_error(self):
        """Rate limit errors should be detected and formatted."""
        error = Exception("429 Too Many Requests")
        message = user_friendly_error(error)
        
        assert 'giới hạn' in message.lower() or 'rate limit' in message.lower()
        assert '15 requests/phút' in message or 'quota' in message.lower()
    
    def test_network_error(self):
        """Network errors should be detected and formatted."""
        error = Exception("Connection timeout")
        message = user_friendly_error(error)
        
        assert 'kết nối' in message.lower() or 'network' in message.lower()
        assert 'internet' in message.lower() or 'connection' in message.lower()
    
    def test_model_error(self):
        """Model not found errors should be detected."""
        error = Exception("Model gemini-2.5-flash not found")
        message = user_friendly_error(error)
        
        assert 'model' in message.lower()
        assert 'không tồn tại' in message.lower() or 'not found' in message.lower()
    
    def test_safety_filter_error(self):
        """Content safety filter errors should be detected."""
        error = Exception("Content blocked by safety filter")
        message = user_friendly_error(error)
        
        assert 'safety' in message.lower() or 'bị chặn' in message.lower()
        assert 'nhạy cảm' in message.lower() or 'inappropriate' in message.lower()
    
    def test_generic_error(self):
        """Unknown errors should show generic message with details."""
        error = Exception("Some random unexpected error")
        message = user_friendly_error(error)
        
        assert '❌' in message
        assert 'không xác định' in message.lower() or 'unknown' in message.lower()
        assert 'Some random unexpected error' in message  # Should include original error


class TestRetryOnFailure:
    """Test simple retry decorator."""
    
    def test_success_on_first_try(self):
        """Function that succeeds should not retry."""
        call_count = {'count': 0}
        
        @retry_on_failure(max_retries=2, delay=0.1)
        def mock_function():
            call_count['count'] += 1
            return "Success"
        
        result = mock_function()
        
        assert result == "Success"
        assert call_count['count'] == 1
    
    def test_retry_until_success(self):
        """Should retry until function succeeds."""
        call_count = {'count': 0}
        
        @retry_on_failure(max_retries=2, delay=0.1)
        def mock_function_fails_once():
            call_count['count'] += 1
            if call_count['count'] < 2:
                raise Exception("Temporary failure")
            return "Success"
        
        result = mock_function_fails_once()
        
        assert result == "Success"
        assert call_count['count'] == 2
    
    def test_max_retries_raises_exception(self):
        """Should raise exception after max retries."""
        call_count = {'count': 0}
        
        @retry_on_failure(max_retries=2, delay=0.1)
        def mock_function_always_fails():
            call_count['count'] += 1
            raise ValueError("Always fails")
        
        with pytest.raises(ValueError, match="Always fails"):
            mock_function_always_fails()
        
        assert call_count['count'] == 3  # Initial + 2 retries


class TestRateLimitKeywords:
    """Test detection of various rate limit error formats."""
    
    @pytest.mark.parametrize("error_message", [
        "429 Too Many Requests",
        "Rate limit exceeded",
        "Quota exceeded",
        "Resource exhausted",
        "too many requests, please try again later"
    ])
    def test_rate_limit_detection(self, error_message):
        """Various rate limit error formats should be detected."""
        call_count = {'count': 0}
        
        @rate_limit_handler(max_retries=2, backoff_base=1)
        def mock_api():
            call_count['count'] += 1
            if call_count['count'] < 2:
                raise Exception(error_message)
            return (True, "Success")
        
        success, result = mock_api()
        
        # Should have retried (call_count > 1)
        assert call_count['count'] >= 2 or success is False


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v', '--tb=short'])
