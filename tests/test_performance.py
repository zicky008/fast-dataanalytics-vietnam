"""
Unit tests for performance monitoring module.

Tests cover:
- Function execution time logging
- Performance monitoring context manager
- Benchmarking utilities
- Custom metrics tracking
"""

import pytest
import time
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.performance import (
    log_performance,
    PerformanceMonitor,
    benchmark,
    measure_time
)


class TestLogPerformance:
    """Test performance logging decorator."""
    
    def test_successful_execution(self):
        """Should log execution time for successful function."""
        
        @log_performance("Test Function")
        def test_func():
            time.sleep(0.1)
            return "Success"
        
        result = test_func()
        
        assert result == "Success"
        # Check that function executed (no exceptions)
    
    def test_failed_execution(self):
        """Should log execution time and re-raise exception."""
        
        @log_performance("Test Function That Fails")
        def test_func_fails():
            time.sleep(0.1)
            raise ValueError("Test error")
        
        with pytest.raises(ValueError, match="Test error"):
            test_func_fails()
    
    def test_default_function_name(self):
        """Should use function name if custom name not provided."""
        
        @log_performance()
        def my_custom_function():
            return "Done"
        
        result = my_custom_function()
        
        assert result == "Done"


class TestPerformanceMonitor:
    """Test PerformanceMonitor context manager."""
    
    def test_successful_monitoring(self):
        """Should track duration and metrics for successful operation."""
        
        with PerformanceMonitor("Test Operation") as monitor:
            time.sleep(0.1)
            monitor.add_metric("items_processed", 100)
            monitor.add_metric("success_rate", 0.95)
        
        assert monitor.success is True
        assert monitor.duration >= 0.1
        assert monitor.metrics['items_processed'] == 100
        assert monitor.metrics['success_rate'] == 0.95
        assert monitor.start_time is not None
        assert monitor.end_time is not None
    
    def test_failed_monitoring(self):
        """Should track duration even when operation fails."""
        
        with pytest.raises(ValueError):
            with PerformanceMonitor("Test Operation That Fails") as monitor:
                time.sleep(0.05)
                monitor.add_metric("items_processed", 50)
                raise ValueError("Test error")
        
        assert monitor.success is False
        assert monitor.duration >= 0.05
        assert monitor.metrics['items_processed'] == 50
    
    def test_get_summary(self):
        """Should return complete performance summary."""
        
        with PerformanceMonitor("Test Operation") as monitor:
            monitor.add_metric("charts_created", 4)
            monitor.add_metric("api_calls", 2)
        
        summary = monitor.get_summary()
        
        assert summary['operation'] == "Test Operation"
        assert summary['success'] is True
        assert summary['duration'] is not None
        assert summary['start_time'] is not None
        assert summary['end_time'] is not None
        assert summary['metrics']['charts_created'] == 4
        assert summary['metrics']['api_calls'] == 2
    
    def test_multiple_metrics(self):
        """Should handle multiple custom metrics."""
        
        with PerformanceMonitor("Multi Metric Test") as monitor:
            for i in range(5):
                monitor.add_metric(f"metric_{i}", i * 10)
        
        assert len(monitor.metrics) == 5
        assert monitor.metrics['metric_0'] == 0
        assert monitor.metrics['metric_4'] == 40


class TestBenchmark:
    """Test benchmark decorator."""
    
    def test_benchmark_iterations(self):
        """Should run function multiple times and log statistics."""
        
        call_count = {'count': 0}
        
        @benchmark(iterations=3)
        def test_func():
            call_count['count'] += 1
            time.sleep(0.05)
            return "Done"
        
        result = test_func()
        
        assert result == "Done"
        assert call_count['count'] == 3  # Should run 3 times
    
    def test_benchmark_consistency(self):
        """Benchmark should return last iteration result."""
        
        iteration_results = []
        
        @benchmark(iterations=3)
        def test_func_with_state():
            result = len(iteration_results) + 1
            iteration_results.append(result)
            return result
        
        final_result = test_func_with_state()
        
        assert final_result == 3  # Last iteration
        assert len(iteration_results) == 3


class TestMeasureTime:
    """Test measure_time utility."""
    
    def test_measure_time_accuracy(self):
        """Should measure execution time accurately."""
        
        def sleep_func():
            time.sleep(0.1)
        
        duration = measure_time(sleep_func)
        
        assert duration >= 0.1
        assert duration < 0.2  # Should not take too long
    
    def test_measure_time_fast_function(self):
        """Should measure even very fast functions."""
        
        def fast_func():
            x = 1 + 1
        
        duration = measure_time(fast_func)
        
        assert duration >= 0
        assert duration < 0.01  # Should be very fast


class TestIntegration:
    """Test integration of performance monitoring tools."""
    
    def test_nested_monitoring(self):
        """Should handle nested performance monitors."""
        
        with PerformanceMonitor("Outer Operation") as outer:
            time.sleep(0.05)
            outer.add_metric("outer_metric", 100)
            
            with PerformanceMonitor("Inner Operation") as inner:
                time.sleep(0.05)
                inner.add_metric("inner_metric", 50)
        
        assert outer.success is True
        assert inner.success is True
        assert outer.duration >= 0.1  # Both sleeps
        assert inner.duration >= 0.05  # Inner sleep only
    
    def test_monitor_with_decorated_function(self):
        """Should work with performance-logged functions."""
        
        @log_performance("Decorated Function")
        def decorated_func():
            time.sleep(0.05)
            return "Done"
        
        with PerformanceMonitor("Monitor Context") as monitor:
            result = decorated_func()
            monitor.add_metric("result", result)
        
        assert monitor.success is True
        assert monitor.metrics['result'] == "Done"


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v', '--tb=short'])
