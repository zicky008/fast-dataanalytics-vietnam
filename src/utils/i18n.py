"""
Internationalization (i18n) module for DataAnalytics Vietnam
Supports: Vietnamese (vi) and English (en)
"""

TRANSLATIONS = {
    "en": {
        # App Title & Branding
        "app_title": "DataAnalytics Vietnam - AI-Powered Business Intelligence",
        "app_subtitle": "Professional dashboards in 60 seconds - Built for Vietnamese SMEs",
        "app_tagline": "Built with ❤️ for Vietnamese SMEs",
        
        # Sidebar
        "premium_features": "🚀 Premium Features",
        "iso_compliance": "**ISO 8000 Compliance** - International data standards",
        "domain_expertise": "**Domain Expertise** - Insights from CMO/CFO/COO",
        "data_lineage": "**Data Lineage** - 100% transparency",
        "industry_benchmarks": "**Industry Benchmarks** - 2024 standards",
        "vietnamese_native": "**Vietnamese Native** - Local language support",
        "pricing": "💰 Pricing",
        "free_plan": "**FREE**: 60 AI messages/month",
        "pro_plan": "**PRO**: 199k VND/month",
        "pro_features": "- 500 AI messages\n- Priority support\n- Unlimited dashboards",
        
        # Tabs
        "tab_upload": "📤 Upload & Analyze",
        "tab_dashboard": "📊 Dashboard",
        "tab_insights": "💡 Insights",
        
        # Upload Tab
        "upload_title": "📤 Upload Data",
        "instructions_title": "📖 User Guide",
        "instructions_content": """
**Step 1**: Upload CSV/Excel file (max 200MB)

**Step 2**: (Optional) Describe your data to help AI understand better

**Step 3**: Click "🚀 Analyze Now" and wait ~60 seconds

**Result**: Professional dashboard + Expert insights

**Note**: 
- Your data is processed securely, not stored
- Results comply with ISO 8000 standards
- Export to PDF/PowerPoint available after completion
""",
        "choose_file": "Choose CSV or Excel file",
        "file_help": "Max 200MB. Supports UTF-8 and Latin1 encoding",
        "dataset_description": "Dataset description (optional)",
        "dataset_placeholder": "Example: Marketing campaign data from Facebook Ads in January 2024...",
        "dataset_help": "Description helps AI understand your data better",
        "analyze_button": "🚀 Analyze Now",
        "time_estimate": "⏱️ Estimated ~60 seconds | ✅ ISO 8000 Compliant | 🔒 Secure",
        "loading_file": "📁 Loading file...",
        "processing": "⚙️ Processing...",
        "preview_data": "👀 Data Preview",
        "shape_info": "📊 Shape: {rows:,} rows × {cols} columns",
        
        # Success Messages
        "success_title": "✅ Complete!",
        "success_time": "⏱️ **Time**: {time:.1f} seconds",
        "success_quality": "⭐ **Quality Score**: {score:.1f}/100 (ISO 8000 Compliant)",
        "success_charts": "📊 **Charts**: {count} charts created",
        "success_insights": "💡 **Insights**: {count} insights from {expert}...",
        "success_next": "👉 Switch to **Dashboard** and **Insights** tabs to view results!",
        
        # Dashboard Tab
        "dashboard_title": "📊 Professional Dashboard",
        "upload_prompt": "👈 Upload data in **Upload & Analyze** tab to start",
        "industry": "**Industry**: {domain} | **Expert**: {expert}...",
        "kpis_title": "📈 Key Performance Indicators",
        "data_quality_warnings": "⚠️ Data Quality Warnings",
        "benchmark": "Benchmark: {value}",
        "charts_title": "📊 Interactive Charts",
        "no_charts": "No charts created. Please check input data.",
        "export_title": "📥 Export Options",
        "export_pdf": "📄 Export PDF",
        "export_ppt": "📊 Export PowerPoint",
        "export_data": "📊 Download Data",
        "download_csv": "💾 Download CSV",
        "feature_coming": "🚧 Feature in development",
        
        # Insights Tab
        "insights_title": "💡 Expert Insights",
        "perspective": "**Perspective from**: {expert}",
        "industry_label": "**Industry**: {domain}",
        "executive_summary": "📋 Executive Summary",
        "no_summary": "No summary available",
        "key_insights": "🎯 Key Insights",
        "recommendations": "🚀 Actionable Recommendations",
        "risk_alerts": "⚠️ Risk Alerts",
        "quality_assurance": "✅ Quality Assurance",
        "quality_score": "Quality Score",
        "iso_compliant": "ISO 8000 Compliant",
        "data_cleaning": "Data Cleaning",
        "cleaning_note": "Missing <2%, Duplicates = 0",
        "blueprint_quality": "Blueprint Quality",
        "blueprint_note": "5 criteria ≥80%",
        
        # Insight Details
        "impact": "Impact: **{level}**",
        "expected_impact": "📊 Expected Impact: {impact}",
        "timeline": "⏱️ Timeline: {time}",
        "severity": "Severity: {level}",
        
        # Settings
        "settings": "⚙️ Settings",
        "language": "🌐 Language",
        "theme": "🎨 Theme",
        "light_mode": "☀️ Light Mode",
        "dark_mode": "🌙 Dark Mode",
        "currency_display": "💱 Currency Display",
        "vnd": "Vietnamese Dong (₫)",
        "usd": "US Dollar ($)",
        
        # Data Quality Guide
        "data_guide_title": "📘 Data Quality Guide",
        "data_guide_content": """
### ✅ How to Prepare Clean Data

**1. File Format**
- ✅ Use CSV or Excel (.xlsx, .xls)
- ✅ First row should be column headers
- ✅ UTF-8 encoding preferred

**2. Column Structure**
- ✅ Clear, descriptive column names (e.g., "Revenue", "Order_Date")
- ✅ No special characters in headers (avoid: @#$%^&*)
- ✅ Consistent data types per column

**3. Data Quality**
- ✅ Remove duplicate rows
- ✅ Fill missing values or use "N/A"
- ✅ Use consistent date formats (YYYY-MM-DD recommended)
- ✅ Use consistent number formats (no mixed commas/periods)

**4. Common Issues to Avoid**
- ❌ Merged cells in Excel
- ❌ Multiple tables in one sheet
- ❌ Formulas without values
- ❌ Hidden rows/columns with data
- ❌ Inconsistent units (mixing VND/USD without labels)

**5. Examples of Good Data**

| Order_Date | Product | Revenue_VND | Units_Sold |
|------------|---------|-------------|------------|
| 2024-01-15 | ProductA | 1500000 | 10 |
| 2024-01-16 | ProductB | 2300000 | 15 |

**Need help?** Contact support@dataanalytics.vn
"""
    },
    
    "vi": {
        # App Title & Branding
        "app_title": "DataAnalytics Vietnam - Phân Tích Kinh Doanh Thông Minh",
        "app_subtitle": "Dashboard chuyên nghiệp trong 60 giây - Được xây dựng cho SMEs Việt Nam",
        "app_tagline": "Được xây dựng với ❤️ cho SMEs Việt Nam",
        
        # Sidebar
        "premium_features": "🚀 Tính Năng Premium",
        "iso_compliance": "**ISO 8000 Compliance** - Dữ liệu chuẩn quốc tế",
        "domain_expertise": "**Domain Expertise** - Insights từ CMO/CFO/COO",
        "data_lineage": "**Data Lineage** - Minh bạch 100%",
        "industry_benchmarks": "**Industry Benchmarks** - Chuẩn 2024",
        "vietnamese_native": "**Vietnamese Native** - Ngôn ngữ bản địa",
        "pricing": "💰 Bảng Giá",
        "free_plan": "**MIỄN PHÍ**: 60 tin nhắn AI/tháng",
        "pro_plan": "**PRO**: 199k VND/tháng",
        "pro_features": "- 500 tin nhắn AI\n- Hỗ trợ ưu tiên\n- Không giới hạn dashboards",
        
        # Tabs
        "tab_upload": "📤 Upload & Phân Tích",
        "tab_dashboard": "📊 Dashboard",
        "tab_insights": "💡 Insights",
        
        # Upload Tab
        "upload_title": "📤 Upload Dữ Liệu",
        "instructions_title": "📖 Hướng Dẫn Sử Dụng",
        "instructions_content": """
**Bước 1**: Upload file CSV/Excel (tối đa 200MB)

**Bước 2**: (Tùy chọn) Mô tả dữ liệu để AI hiểu rõ hơn

**Bước 3**: Nhấn "🚀 Phân Tích Ngay" và chờ ~60 giây

**Kết quả**: Dashboard chuyên nghiệp + Insights từ chuyên gia

**Lưu ý**: 
- Dữ liệu của bạn được xử lý an toàn, không lưu trữ
- Kết quả tuân thủ chuẩn ISO 8000
- Có thể export PDF/PowerPoint sau khi hoàn thành
""",
        "choose_file": "Chọn file CSV hoặc Excel",
        "file_help": "File tối đa 200MB. Hỗ trợ UTF-8 và Latin1 encoding",
        "dataset_description": "Mô tả dữ liệu (tùy chọn)",
        "dataset_placeholder": "Ví dụ: Dữ liệu marketing campaign từ Facebook Ads tháng 1/2024...",
        "dataset_help": "Mô tả giúp AI hiểu rõ hơn về dữ liệu của bạn",
        "analyze_button": "🚀 Phân Tích Ngay",
        "time_estimate": "⏱️ Dự kiến ~60 giây | ✅ ISO 8000 Compliant | 🔒 Bảo mật",
        "loading_file": "📁 Đang tải file...",
        "processing": "⚙️ Đang Xử Lý...",
        "preview_data": "👀 Xem Trước Dữ Liệu",
        "shape_info": "📊 Shape: {rows:,} rows × {cols} columns",
        
        # Success Messages
        "success_title": "✅ Hoàn Thành!",
        "success_time": "⏱️ **Thời gian**: {time:.1f} giây",
        "success_quality": "⭐ **Quality Score**: {score:.1f}/100 (ISO 8000 Compliant)",
        "success_charts": "📊 **Charts**: {count} biểu đồ được tạo",
        "success_insights": "💡 **Insights**: {count} insights từ {expert}...",
        "success_next": "👉 Chuyển sang tab **Dashboard** và **Insights** để xem kết quả!",
        
        # Dashboard Tab
        "dashboard_title": "📊 Dashboard Chuyên Nghiệp",
        "upload_prompt": "👈 Upload dữ liệu ở tab **Upload & Phân Tích** để bắt đầu",
        "industry": "**Ngành nghề**: {domain} | **Expert**: {expert}...",
        "kpis_title": "📈 Chỉ Số Hiệu Suất Chính",
        "data_quality_warnings": "⚠️ Cảnh Báo Chất Lượng Dữ Liệu",
        "benchmark": "Chuẩn: {value}",
        "charts_title": "📊 Biểu Đồ Tương Tác",
        "no_charts": "Không có biểu đồ nào được tạo. Vui lòng kiểm tra dữ liệu đầu vào.",
        "export_title": "📥 Tùy Chọn Export",
        "export_pdf": "📄 Export PDF",
        "export_ppt": "📊 Export PowerPoint",
        "export_data": "📊 Tải Dữ Liệu",
        "download_csv": "💾 Tải CSV",
        "feature_coming": "🚧 Tính năng đang phát triển",
        
        # Insights Tab
        "insights_title": "💡 Insights Chuyên Gia",
        "perspective": "**Perspective từ**: {expert}",
        "industry_label": "**Ngành nghề**: {domain}",
        "executive_summary": "📋 Tóm Tắt Điều Hành",
        "no_summary": "Chưa có tóm tắt",
        "key_insights": "🎯 Insights Chính",
        "recommendations": "🚀 Khuyến Nghị Hành Động",
        "risk_alerts": "⚠️ Cảnh Báo Rủi Ro",
        "quality_assurance": "✅ Đảm Bảo Chất Lượng",
        "quality_score": "Điểm Chất Lượng",
        "iso_compliant": "ISO 8000 Compliant",
        "data_cleaning": "Làm Sạch Dữ Liệu",
        "cleaning_note": "Missing <2%, Duplicates = 0",
        "blueprint_quality": "Chất Lượng Blueprint",
        "blueprint_note": "5 tiêu chí ≥80%",
        
        # Insight Details
        "impact": "Tác động: **{level}**",
        "expected_impact": "📊 Tác Động Dự Kiến: {impact}",
        "timeline": "⏱️ Thời Gian: {time}",
        "severity": "Mức độ nghiêm trọng: {level}",
        
        # Settings
        "settings": "⚙️ Cài Đặt",
        "language": "🌐 Ngôn Ngữ",
        "theme": "🎨 Giao Diện",
        "light_mode": "☀️ Sáng",
        "dark_mode": "🌙 Tối",
        "currency_display": "💱 Hiển Thị Tiền Tệ",
        "vnd": "Việt Nam Đồng (₫)",
        "usd": "Đô La Mỹ ($)",
        
        # Data Quality Guide
        "data_guide_title": "📘 Hướng Dẫn Chất Lượng Dữ Liệu",
        "data_guide_content": """
### ✅ Cách Chuẩn Bị Dữ Liệu Sạch

**1. Định Dạng File**
- ✅ Sử dụng CSV hoặc Excel (.xlsx, .xls)
- ✅ Dòng đầu tiên là tên cột
- ✅ Ưu tiên encoding UTF-8

**2. Cấu Trúc Cột**
- ✅ Tên cột rõ ràng, mô tả (ví dụ: "Doanh_Thu", "Ngay_Don_Hang")
- ✅ Không có ký tự đặc biệt trong tên cột (tránh: @#$%^&*)
- ✅ Kiểu dữ liệu nhất quán trong mỗi cột

**3. Chất Lượng Dữ Liệu**
- ✅ Xóa các dòng trùng lặp
- ✅ Điền giá trị thiếu hoặc dùng "N/A"
- ✅ Sử dụng format ngày nhất quán (khuyến nghị YYYY-MM-DD)
- ✅ Sử dụng format số nhất quán (không trộn dấu phẩy/chấm)

**4. Các Vấn Đề Thường Gặp Cần Tránh**
- ❌ Ô merge trong Excel
- ❌ Nhiều bảng trong một sheet
- ❌ Công thức không có giá trị
- ❌ Dòng/cột ẩn có dữ liệu
- ❌ Đơn vị không nhất quán (trộn VND/USD không có nhãn)

**5. Ví Dụ Dữ Liệu Tốt**

| Ngay_Don_Hang | San_Pham | Doanh_Thu_VND | So_Luong |
|---------------|----------|---------------|----------|
| 2024-01-15    | SP_A     | 1500000       | 10       |
| 2024-01-16    | SP_B     | 2300000       | 15       |

**Cần hỗ trợ?** Liên hệ support@dataanalytics.vn
"""
    }
}


def get_text(key: str, lang: str = "vi", **kwargs) -> str:
    """
    Get translated text by key
    
    Args:
        key: Translation key
        lang: Language code ('vi' or 'en')
        **kwargs: Format arguments for string interpolation
    
    Returns:
        Translated text with formatting applied
    """
    text = TRANSLATIONS.get(lang, TRANSLATIONS["vi"]).get(key, key)
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    
    return text


def format_number(value: float, lang: str = "vi", decimals: int = 1) -> str:
    """
    Format number with thousand separators based on language
    
    Args:
        value: Number to format
        lang: Language code ('vi' or 'en')
        decimals: Number of decimal places
    
    Returns:
        Formatted number string
    
    Examples:
        >>> format_number(1234567.89, 'vi', 1)
        '1.234.567,9'
        >>> format_number(1234567.89, 'en', 1)
        '1,234,567.9'
    """
    if lang == "vi":
        # Vietnamese: 1.234.567,89 (dot for thousands, comma for decimal)
        formatted = f"{value:,.{decimals}f}"
        formatted = formatted.replace(",", "TEMP").replace(".", ",").replace("TEMP", ".")
    else:
        # English: 1,234,567.89 (comma for thousands, dot for decimal)
        formatted = f"{value:,.{decimals}f}"
    
    return formatted


def convert_vnd_to_usd(value: float, exchange_rate: float = 24000) -> float:
    """
    Convert VND to USD using standard exchange rate
    
    Args:
        value: Value in VND
        exchange_rate: VND to USD rate (default: 24,000 VND = 1 USD as of 2024)
    
    Returns:
        Value in USD
    """
    return value / exchange_rate


def format_currency(value: float, currency: str = "VND", lang: str = "vi", decimals: int = 0) -> str:
    """
    Format currency with proper symbol and formatting
    
    Args:
        value: Currency value
        currency: Currency code ('VND' or 'USD')
        lang: Language code
        decimals: Decimal places (default 0 for VND, 2 for USD)
    
    Returns:
        Formatted currency string
    
    Examples:
        >>> format_currency(1234567, 'VND', 'vi')
        '1.234.567₫'
        >>> format_currency(51.44, 'USD', 'en')
        '$51.44'
    """
    if currency == "VND":
        decimals = 0  # VND doesn't use decimals
        symbol = "₫"
        formatted_value = format_number(value, lang, decimals)
        return f"{formatted_value}{symbol}"
    else:  # USD
        decimals = 2
        symbol = "$"
        formatted_value = format_number(value, lang, decimals)
        return f"{symbol}{formatted_value}"
