"""
Utility modules for Data Analytics Vietnam application.
"""

# Lazy imports to avoid circular dependencies and streamlit requirement
__all__ = [
    'safe_file_upload',
    'sanitize_column_names', 
    'validate_dataframe',
    'rate_limit_handler',
    'user_friendly_error',
    'log_performance',
    'PerformanceMonitor',
    'get_text',
    'format_number',
    'format_currency',
    'convert_vnd_to_usd',
    'get_logo_svg',
    'get_brand_colors'
]

def __getattr__(name):
    """Lazy loading of modules"""
    if name in ['safe_file_upload', 'sanitize_column_names', 'validate_dataframe']:
        from .validators import safe_file_upload, sanitize_column_names, validate_dataframe
        return locals()[name]
    elif name in ['rate_limit_handler', 'user_friendly_error']:
        from .error_handlers import rate_limit_handler, user_friendly_error
        return locals()[name]
    elif name in ['log_performance', 'PerformanceMonitor']:
        from .performance import log_performance, PerformanceMonitor
        return locals()[name]
    elif name in ['get_text', 'format_number', 'format_currency', 'convert_vnd_to_usd']:
        from .i18n import get_text, format_number, format_currency, convert_vnd_to_usd
        return locals()[name]
    elif name in ['get_logo_svg', 'get_brand_colors']:
        from .branding import get_logo_svg, get_brand_colors
        return locals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
