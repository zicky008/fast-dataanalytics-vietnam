"""
Branding utilities for DataAnalytics Vietnam
Generates professional logo and brand assets
"""

def get_logo_svg(variant="light"):
    """
    Generate professional SVG logo for DataAnalytics Vietnam
    
    Args:
        variant: 'light' or 'dark' theme
    
    Returns:
        SVG markup as string
    """
    if variant == "dark":
        primary_color = "#60A5FA"  # Light blue for dark theme
        text_color = "#F1F5F9"
        accent_color = "#3B82F6"
    else:
        primary_color = "#1E40AF"  # Dark blue for light theme
        text_color = "#1E293B"
        accent_color = "#3B82F6"
    
    svg = f'''<svg width="300" height="80" viewBox="0 0 300 80" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="300" height="80" fill="transparent"/>
  
  <!-- Icon: Data Analytics Symbol -->
  <g transform="translate(10, 15)">
    <!-- Chart bars -->
    <rect x="0" y="30" width="8" height="20" fill="{accent_color}" rx="2"/>
    <rect x="12" y="20" width="8" height="30" fill="{primary_color}" rx="2"/>
    <rect x="24" y="10" width="8" height="40" fill="{accent_color}" rx="2"/>
    <rect x="36" y="25" width="8" height="25" fill="{primary_color}" rx="2"/>
    
    <!-- Sparkline overlay -->
    <path d="M 2 35 L 16 25 L 28 15 L 40 30" 
          stroke="{primary_color}" 
          stroke-width="2" 
          fill="none" 
          stroke-linecap="round"/>
    
    <!-- Circle highlight -->
    <circle cx="28" cy="15" r="3" fill="{accent_color}"/>
  </g>
  
  <!-- Text: DataAnalytics -->
  <text x="65" y="35" 
        font-family="'Inter', 'SF Pro Display', -apple-system, sans-serif" 
        font-size="24" 
        font-weight="700" 
        fill="{text_color}">
    DataAnalytics
  </text>
  
  <!-- Text: Vietnam -->
  <text x="65" y="55" 
        font-family="'Inter', 'SF Pro Display', -apple-system, sans-serif" 
        font-size="14" 
        font-weight="500" 
        fill="{accent_color}">
    Vietnam
  </text>
  
  <!-- Tagline -->
  <text x="220" y="55" 
        font-family="'Inter', 'SF Pro Display', -apple-system, sans-serif" 
        font-size="10" 
        font-weight="400" 
        fill="{text_color}" 
        opacity="0.6">
    AI-Powered BI
  </text>
</svg>'''
    
    return svg


def get_favicon_svg():
    """
    Generate favicon SVG (simplified icon only)
    """
    svg = '''<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <!-- Background circle -->
  <circle cx="32" cy="32" r="30" fill="#1E40AF"/>
  
  <!-- Chart bars (white) -->
  <g transform="translate(16, 24)">
    <rect x="0" y="12" width="5" height="10" fill="white" opacity="0.8" rx="1"/>
    <rect x="8" y="8" width="5" height="14" fill="white" rx="1"/>
    <rect x="16" y="4" width="5" height="18" fill="white" opacity="0.8" rx="1"/>
    <rect x="24" y="10" width="5" height="12" fill="white" rx="1"/>
  </g>
  
  <!-- Sparkline overlay -->
  <path d="M 18 36 L 26 32 L 34 28 L 42 34" 
        stroke="white" 
        stroke-width="2" 
        fill="none" 
        stroke-linecap="round"
        opacity="0.9"/>
  
  <!-- Circle highlight -->
  <circle cx="34" cy="28" r="2.5" fill="#60A5FA"/>
</svg>'''
    
    return svg


def get_brand_colors():
    """
    Get brand color palette
    """
    return {
        "light_theme": {
            "primary": "#1E40AF",  # Dark blue
            "secondary": "#3B82F6",  # Medium blue
            "accent": "#60A5FA",  # Light blue
            "success": "#22C55E",  # Green
            "warning": "#F59E0B",  # Amber
            "danger": "#EF4444",  # Red
            "text_primary": "#1E293B",  # Slate 800
            "text_secondary": "#64748B",  # Slate 500
            "background": "#FFFFFF",
            "surface": "#F8FAFC",  # Slate 50
            "border": "#E2E8F0"  # Slate 200
        },
        "dark_theme": {
            "primary": "#60A5FA",  # Light blue
            "secondary": "#3B82F6",  # Medium blue
            "accent": "#93C5FD",  # Very light blue
            "success": "#4ADE80",  # Light green
            "warning": "#FBBF24",  # Light amber
            "danger": "#F87171",  # Light red
            "text_primary": "#F1F5F9",  # Slate 100
            "text_secondary": "#94A3B8",  # Slate 400
            "background": "#0F172A",  # Slate 900
            "surface": "#1E293B",  # Slate 800
            "border": "#334155"  # Slate 700
        }
    }


def get_brand_typography():
    """
    Get brand typography guidelines
    """
    return {
        "font_family_primary": "'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif",
        "font_family_mono": "'JetBrains Mono', 'Fira Code', 'Consolas', monospace",
        "font_sizes": {
            "h1": "2.5rem",  # 40px
            "h2": "2rem",    # 32px
            "h3": "1.5rem",  # 24px
            "h4": "1.25rem", # 20px
            "body": "1rem",  # 16px
            "small": "0.875rem",  # 14px
            "caption": "0.75rem"  # 12px
        },
        "font_weights": {
            "light": 300,
            "regular": 400,
            "medium": 500,
            "semibold": 600,
            "bold": 700
        }
    }


def save_logo_files():
    """
    Save logo files to assets directory
    """
    import os
    
    # Create assets directories
    assets_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
    logos_dir = os.path.join(assets_dir, 'logos')
    
    os.makedirs(logos_dir, exist_ok=True)
    
    # Save light theme logo
    with open(os.path.join(logos_dir, 'logo_light.svg'), 'w', encoding='utf-8') as f:
        f.write(get_logo_svg('light'))
    
    # Save dark theme logo
    with open(os.path.join(logos_dir, 'logo_dark.svg'), 'w', encoding='utf-8') as f:
        f.write(get_logo_svg('dark'))
    
    # Save favicon
    with open(os.path.join(logos_dir, 'favicon.svg'), 'w', encoding='utf-8') as f:
        f.write(get_favicon_svg())
    
    print("✅ Logo files saved to assets/logos/")
    print("   - logo_light.svg")
    print("   - logo_dark.svg")
    print("   - favicon.svg")


if __name__ == "__main__":
    save_logo_files()
