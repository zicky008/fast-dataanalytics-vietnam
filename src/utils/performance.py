"""
Performance monitoring utilities for tracking execution time and resource usage.

This module provides:
- Function execution time logging
- Performance monitoring with detailed metrics
- Benchmarking utilities
"""

import time
import functools
import logging
from typing import Callable, Any, Dict
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def log_performance(func_name: str = None):
    """
    Decorator to log function execution time and performance metrics.
    
    Args:
        func_name: Optional custom name for logging (default: use function name)
    
    Returns:
        Decorated function with performance logging
    
    Example:
        >>> @log_performance("AI Insight Generation")
        >>> def generate_ai_insight(client, prompt):
        >>>     response = client.models.generate_content(...)
        >>>     return (True, response.text)
        
        Output:
        [2024-01-15 10:30:45] AI Insight Generation completed in 2.34s
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            name = func_name or func.__name__
            start_time = time.time()
            
            try:
                logger.info(f"🚀 {name} started")
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                logger.info(f"✅ {name} completed in {duration:.2f}s")
                return result
            
            except Exception as e:
                duration = time.time() - start_time
                logger.error(f"❌ {name} failed after {duration:.2f}s: {str(e)[:100]}")
                raise e
        
        return wrapper
    return decorator


class PerformanceMonitor:
    """
    Context manager for monitoring performance of code blocks.
    
    Tracks:
    - Execution time
    - Start/end timestamps
    - Custom metrics
    
    Example:
        >>> with PerformanceMonitor("Dashboard Generation") as monitor:
        >>>     # Generate dashboard
        >>>     create_charts()
        >>>     monitor.add_metric("charts_created", 4)
        >>> 
        >>> print(f"Duration: {monitor.duration:.2f}s")
        >>> print(f"Metrics: {monitor.metrics}")
    """
    
    def __init__(self, operation_name: str):
        """
        Initialize performance monitor.
        
        Args:
            operation_name: Name of the operation being monitored
        """
        self.operation_name = operation_name
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.metrics: Dict[str, Any] = {}
        self.success = False
    
    def __enter__(self):
        """Start monitoring."""
        self.start_time = time.time()
        logger.info(f"🚀 {self.operation_name} started at {datetime.now().strftime('%H:%M:%S')}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """End monitoring and log results."""
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        
        if exc_type is None:
            self.success = True
            logger.info(
                f"✅ {self.operation_name} completed in {self.duration:.2f}s | "
                f"Metrics: {self.metrics}"
            )
        else:
            self.success = False
            logger.error(
                f"❌ {self.operation_name} failed after {self.duration:.2f}s | "
                f"Error: {exc_val}"
            )
        
        return False  # Don't suppress exceptions
    
    def add_metric(self, key: str, value: Any):
        """
        Add a custom metric to track.
        
        Args:
            key: Metric name
            value: Metric value
        
        Example:
            >>> monitor.add_metric("rows_processed", 1000)
            >>> monitor.add_metric("charts_created", 4)
        """
        self.metrics[key] = value
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get performance summary.
        
        Returns:
            Dictionary with operation name, duration, success status, and metrics
        """
        return {
            'operation': self.operation_name,
            'duration': self.duration,
            'success': self.success,
            'start_time': datetime.fromtimestamp(self.start_time).isoformat() if self.start_time else None,
            'end_time': datetime.fromtimestamp(self.end_time).isoformat() if self.end_time else None,
            'metrics': self.metrics
        }


def benchmark(iterations: int = 3):
    """
    Decorator to benchmark a function over multiple iterations.
    
    Args:
        iterations: Number of times to run the function (default: 3)
    
    Returns:
        Decorated function with benchmarking
    
    Example:
        >>> @benchmark(iterations=5)
        >>> def expensive_operation():
        >>>     time.sleep(0.1)
        >>>     return "Done"
        
        Output:
        Benchmark: expensive_operation
        - Iteration 1: 0.10s
        - Iteration 2: 0.10s
        - Iteration 3: 0.10s
        - Average: 0.10s
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            durations = []
            result = None
            
            logger.info(f"📊 Benchmarking {func.__name__} over {iterations} iterations...")
            
            for i in range(iterations):
                start = time.time()
                result = func(*args, **kwargs)
                duration = time.time() - start
                durations.append(duration)
                logger.info(f"  Iteration {i+1}: {duration:.2f}s")
            
            avg_duration = sum(durations) / len(durations)
            min_duration = min(durations)
            max_duration = max(durations)
            
            logger.info(
                f"📈 Benchmark Summary for {func.__name__}:\n"
                f"  Average: {avg_duration:.2f}s\n"
                f"  Min: {min_duration:.2f}s\n"
                f"  Max: {max_duration:.2f}s"
            )
            
            return result
        
        return wrapper
    return decorator


def measure_time(func: Callable) -> float:
    """
    Simple utility to measure execution time of a function.
    
    Args:
        func: Function to measure (should be callable with no args)
    
    Returns:
        Execution time in seconds
    
    Example:
        >>> def slow_function():
        >>>     time.sleep(1)
        >>> 
        >>> duration = measure_time(slow_function)
        >>> print(f"Took {duration:.2f}s")
    """
    start = time.time()
    func()
    return time.time() - start
