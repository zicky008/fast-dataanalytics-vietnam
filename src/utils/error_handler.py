"""
Vietnamese Error Message Library
PMF Strategy Tactic #3 - Reduce error dropout from 30% to 5%
Zero-cost implementation with AI-generated friendly error messages
"""

import streamlit as st

# Error message library (Vietnamese + English)
ERROR_MESSAGES = {
    "password_protected": {
        "vi": {
            "title": "❌ Không thể mở file Excel",
            "problem": "File của bạn có mật khẩu bảo vệ",
            "why": "Excel cho phép đặt mật khẩu để bảo vệ dữ liệu. Hệ thống không thể đọc file có mật khẩu vì lý do bảo mật.",
            "fix_steps": [
                "Mở file trong Excel",
                "Chọn File → Info → Protect Workbook → Encrypt with Password",
                "Xóa mật khẩu (để trống) → Lưu file",
                "Upload lại file đã xóa mật khẩu"
            ],
            "support": "Vẫn gặp lỗi? Liên hệ support qua email hoặc Zalo"
        },
        "en": {
            "title": "❌ Cannot open Excel file",
            "problem": "Your file is password protected",
            "why": "Excel allows setting passwords to protect data. The system cannot read password-protected files for security reasons.",
            "fix_steps": [
                "Open file in Excel",
                "Select File → Info → Protect Workbook → Encrypt with Password",
                "Remove password (leave blank) → Save file",
                "Re-upload the file without password"
            ],
            "support": "Still having issues? Contact support via email or Zalo"
        }
    },

    "empty_file": {
        "vi": {
            "title": "❌ File rỗng (không có dữ liệu)",
            "problem": "File của bạn không chứa dữ liệu hoặc chỉ có tiêu đề",
            "why": "File CSV/Excel cần có ít nhất 2 dòng: 1 dòng tiêu đề và 1 dòng dữ liệu.",
            "fix_steps": [
                "Mở file và kiểm tra có dữ liệu không",
                "Đảm bảo dòng đầu tiên là tên cột (Header)",
                "Dòng thứ 2 trở đi phải có dữ liệu thực tế",
                "Lưu file và upload lại"
            ],
            "support": "Cần file mẫu? Thử các file mẫu trong app"
        },
        "en": {
            "title": "❌ Empty file (no data)",
            "problem": "Your file contains no data or only headers",
            "why": "CSV/Excel files need at least 2 rows: 1 header row and 1 data row.",
            "fix_steps": [
                "Open file and check if it contains data",
                "Ensure first row is column names (Header)",
                "Rows 2 onwards must have actual data",
                "Save file and re-upload"
            ],
            "support": "Need sample file? Try sample data in the app"
        }
    },

    "file_too_large": {
        "vi": {
            "title": "❌ File quá lớn (vượt quá 50,000 dòng)",
            "problem": "File của bạn có quá nhiều dữ liệu để xử lý",
            "why": "Để đảm bảo tốc độ xử lý nhanh (<60 giây), chúng tôi giới hạn 50,000 dòng.",
            "fix_steps": [
                "Lọc dữ liệu theo khoảng thời gian ngắn hơn (ví dụ: 3 tháng gần nhất thay vì cả năm)",
                "Hoặc tách file lớn thành nhiều file nhỏ",
                "Mỗi file nên có 10,000-50,000 dòng",
                "Upload từng file để phân tích riêng"
            ],
            "support": "Cần xử lý file lớn hơn? Liên hệ Enterprise plan"
        },
        "en": {
            "title": "❌ File too large (exceeds 50,000 rows)",
            "problem": "Your file has too much data to process",
            "why": "To ensure fast processing (<60 seconds), we limit to 50,000 rows.",
            "fix_steps": [
                "Filter data by shorter time period (e.g., last 3 months instead of whole year)",
                "Or split large file into smaller files",
                "Each file should have 10,000-50,000 rows",
                "Upload each file for separate analysis"
            ],
            "support": "Need to process larger files? Contact Enterprise plan"
        }
    },

    "corrupted_file": {
        "vi": {
            "title": "❌ File bị hỏng hoặc không đọc được",
            "problem": "File của bạn có thể bị hỏng hoặc định dạng không hợp lệ",
            "why": "File có thể bị hỏng khi download/transfer, hoặc được lưu với encoding không chuẩn.",
            "fix_steps": [
                "Thử mở file trong Excel/Google Sheets để kiểm tra",
                "Nếu mở được: File → Save As → Chọn 'CSV UTF-8' hoặc 'Excel Workbook (.xlsx)'",
                "Nếu không mở được: File có thể bị hỏng, cần export lại từ nguồn gốc",
                "Upload file mới"
            ],
            "support": "File export từ hệ thống nào? Chúng tôi có thể hướng dẫn cách export đúng"
        },
        "en": {
            "title": "❌ Corrupted or unreadable file",
            "problem": "Your file may be corrupted or in invalid format",
            "why": "Files can get corrupted during download/transfer, or saved with non-standard encoding.",
            "fix_steps": [
                "Try opening file in Excel/Google Sheets to verify",
                "If it opens: File → Save As → Choose 'CSV UTF-8' or 'Excel Workbook (.xlsx)'",
                "If it doesn't open: File may be corrupted, need to re-export from source",
                "Upload the new file"
            ],
            "support": "Which system exported this file? We can guide you on correct export method"
        }
    },

    "encoding_error": {
        "vi": {
            "title": "❌ Lỗi hiển thị ký tự tiếng Việt",
            "problem": "Ký tự tiếng Việt trong file hiển thị sai (dấu bị lỗi)",
            "why": "File CSV được lưu với encoding không phải UTF-8 (thường là Windows-1252).",
            "fix_steps": [
                "Mở file trong Excel",
                "File → Save As → 'CSV UTF-8 (Comma delimited) (*.csv)'",
                "Lưu file với tên mới",
                "Upload file UTF-8 này"
            ],
            "support": "Hoặc dùng Notepad++: Encoding → Convert to UTF-8"
        },
        "en": {
            "title": "❌ Vietnamese character encoding error",
            "problem": "Vietnamese characters in your file display incorrectly (broken accents)",
            "why": "CSV file was saved with encoding other than UTF-8 (often Windows-1252).",
            "fix_steps": [
                "Open file in Excel",
                "File → Save As → 'CSV UTF-8 (Comma delimited) (*.csv)'",
                "Save with new name",
                "Upload this UTF-8 file"
            ],
            "support": "Or use Notepad++: Encoding → Convert to UTF-8"
        }
    },

    "mixed_data_types": {
        "vi": {
            "title": "❌ Cột có dữ liệu hỗn hợp (số và chữ)",
            "problem": "Một cột chứa cả số lẫn chữ (ví dụ: 100, 200, 'N/A', 300)",
            "why": "Hệ thống không thể xác định cột là số hay chữ khi có dữ liệu hỗn hợp.",
            "fix_steps": [
                "Mở file, tìm cột bị lỗi (thường là cột số)",
                "Thay tất cả giá trị chữ (N/A, TBD, etc.) bằng: 0 hoặc để trống",
                "Hoặc tách thành 2 cột: 1 cột số, 1 cột ghi chú",
                "Lưu file và upload lại"
            ],
            "support": "Không chắc cột nào? Gửi file cho chúng tôi, sẽ check giúp"
        },
        "en": {
            "title": "❌ Column has mixed data types (numbers and text)",
            "problem": "A column contains both numbers and text (e.g., 100, 200, 'N/A', 300)",
            "why": "System cannot determine if column is numeric or text when data is mixed.",
            "fix_steps": [
                "Open file, find problematic column (usually numeric column)",
                "Replace all text values (N/A, TBD, etc.) with: 0 or leave blank",
                "Or split into 2 columns: 1 numeric, 1 notes column",
                "Save file and re-upload"
            ],
            "support": "Not sure which column? Send us the file, we'll check"
        }
    },

    "no_header": {
        "vi": {
            "title": "❌ File không có dòng tiêu đề (Header)",
            "problem": "Dòng đầu tiên không phải là tên cột",
            "why": "Hệ thống cần dòng đầu tiên để biết tên từng cột (Revenue, Date, Product, etc.).",
            "fix_steps": [
                "Mở file trong Excel",
                "Thêm dòng đầu tiên với tên cột (ngắn gọn, dễ hiểu)",
                "Ví dụ: Date, Product, Revenue, Quantity",
                "Lưu file và upload lại"
            ],
            "support": "Không biết đặt tên cột? Chúng tôi có thể gợi ý"
        },
        "en": {
            "title": "❌ File has no header row",
            "problem": "First row is not column names",
            "why": "System needs first row to identify column names (Revenue, Date, Product, etc.).",
            "fix_steps": [
                "Open file in Excel",
                "Add first row with column names (short, clear)",
                "Example: Date, Product, Revenue, Quantity",
                "Save file and re-upload"
            ],
            "support": "Not sure what to name columns? We can suggest"
        }
    },

    "all_columns_empty": {
        "vi": {
            "title": "❌ Tất cả các cột đều rỗng",
            "problem": "File có tiêu đề nhưng không có dữ liệu trong các cột",
            "why": "Có thể do filter Excel còn active, hoặc copy sai vùng dữ liệu.",
            "fix_steps": [
                "Mở file, bỏ filter nếu có (Data → Clear Filters)",
                "Kiểm tra dữ liệu có hiển thị không",
                "Nếu có dữ liệu: Lưu lại và upload",
                "Nếu không: Export lại từ nguồn gốc"
            ],
            "support": "File export từ đâu? Chúng tôi hướng dẫn cách export đúng"
        },
        "en": {
            "title": "❌ All columns are empty",
            "problem": "File has headers but no data in columns",
            "why": "Could be due to active Excel filter, or wrong data range copied.",
            "fix_steps": [
                "Open file, remove filters if any (Data → Clear Filters)",
                "Check if data is visible",
                "If data visible: Save and upload",
                "If not: Re-export from source"
            ],
            "support": "Where was file exported from? We can guide correct export method"
        }
    },

    "only_header_row": {
        "vi": {
            "title": "❌ Chỉ có dòng tiêu đề, không có dữ liệu",
            "problem": "File chỉ có 1 dòng (tên cột) mà không có dòng dữ liệu",
            "why": "Cần ít nhất 1 dòng dữ liệu để phân tích.",
            "fix_steps": [
                "Kiểm tra xem dữ liệu có bị filter ẩn không",
                "Hoặc export từ nguồn có chọn đúng khoảng thời gian",
                "Đảm bảo có ít nhất 10 dòng dữ liệu để phân tích có ý nghĩa",
                "Upload lại file có dữ liệu"
            ],
            "support": "Cần file mẫu để tham khảo format? Dùng sample data trong app"
        },
        "en": {
            "title": "❌ Only header row, no data",
            "problem": "File has only 1 row (column names) with no data rows",
            "why": "Need at least 1 data row for analysis.",
            "fix_steps": [
                "Check if data is hidden by filters",
                "Or re-export from source with correct date range",
                "Ensure at least 10 data rows for meaningful analysis",
                "Re-upload file with data"
            ],
            "support": "Need sample file for format reference? Use sample data in app"
        }
    },

    "date_format_error": {
        "vi": {
            "title": "❌ Định dạng ngày tháng không nhận diện được",
            "problem": "Cột ngày tháng không đúng format (ví dụ: '25-10-2025' thay vì '2025-10-25')",
            "why": "Hệ thống hỗ trợ các format: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY.",
            "fix_steps": [
                "Mở file trong Excel",
                "Chọn cột ngày tháng",
                "Format Cells → Date → Chọn format: 'YYYY-MM-DD' hoặc 'DD/MM/YYYY'",
                "Lưu file và upload lại"
            ],
            "support": "Các format được hỗ trợ: 2025-10-25, 25/10/2025, 10/25/2025"
        },
        "en": {
            "title": "❌ Date format not recognized",
            "problem": "Date column is not in correct format (e.g., '25-10-2025' instead of '2025-10-25')",
            "why": "System supports formats: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY.",
            "fix_steps": [
                "Open file in Excel",
                "Select date column",
                "Format Cells → Date → Choose format: 'YYYY-MM-DD' or 'DD/MM/YYYY'",
                "Save file and re-upload"
            ],
            "support": "Supported formats: 2025-10-25, 25/10/2025, 10/25/2025"
        }
    }
}


def show_error(error_type: str, lang: str = 'vi', additional_info: str = None):
    """
    Display friendly error message in Streamlit

    Args:
        error_type: One of the error types in ERROR_MESSAGES
        lang: Language ('vi' or 'en')
        additional_info: Optional additional context to display
    """
    if error_type not in ERROR_MESSAGES:
        # Fallback for unknown errors
        if lang == 'vi':
            st.error("❌ Đã xảy ra lỗi không xác định. Vui lòng liên hệ support.")
        else:
            st.error("❌ An unknown error occurred. Please contact support.")
        if additional_info:
            st.caption(f"Error details: {additional_info}")
        return

    error = ERROR_MESSAGES[error_type][lang]

    # Display error title
    st.error(f"### {error['title']}")

    # Display details in expander
    with st.expander("📋 Chi tiết & Cách khắc phục" if lang == 'vi' else "📋 Details & How to fix", expanded=True):
        st.markdown(f"**{'Vấn đề' if lang == 'vi' else 'Problem'}**: {error['problem']}")
        st.markdown(f"**{'Tại sao' if lang == 'vi' else 'Why'}**: {error['why']}")

        st.markdown(f"**✅ {'Cách khắc phục' if lang == 'vi' else 'How to fix'}**:")
        for i, step in enumerate(error['fix_steps'], 1):
            st.markdown(f"{i}. {step}")

        st.markdown(f"💬 {error['support']}")

        if additional_info:
            st.caption(f"Technical info: {additional_info}")


def detect_error_type(error_message: str, df=None) -> str:
    """
    Detect error type from error message or dataframe

    Args:
        error_message: Error message string
        df: Optional pandas DataFrame to inspect

    Returns:
        error_type: One of the ERROR_MESSAGES keys
    """
    error_lower = error_message.lower() if error_message else ""

    # Password protected
    if 'password' in error_lower or 'encrypted' in error_lower:
        return 'password_protected'

    # Empty file
    if df is not None and (len(df) == 0 or df.empty):
        return 'empty_file'

    if 'empty' in error_lower or 'no data' in error_lower:
        return 'empty_file'

    # File too large
    if df is not None and len(df) > 50000:
        return 'file_too_large'

    if 'too large' in error_lower or 'size limit' in error_lower:
        return 'file_too_large'

    # Corrupted
    if 'corrupt' in error_lower or 'invalid' in error_lower or 'cannot read' in error_lower:
        return 'corrupted_file'

    # Encoding
    if 'encoding' in error_lower or 'decode' in error_lower or 'utf' in error_lower:
        return 'encoding_error'

    # Mixed data types
    if 'dtype' in error_lower or 'type' in error_lower or 'convert' in error_lower:
        return 'mixed_data_types'

    # Date format
    if 'date' in error_lower or 'datetime' in error_lower:
        return 'date_format_error'

    # Default to corrupted file
    return 'corrupted_file'


# Quick access functions for common errors
def show_password_error(lang='vi'):
    show_error('password_protected', lang)

def show_empty_file_error(lang='vi'):
    show_error('empty_file', lang)

def show_file_too_large_error(lang='vi', row_count=None):
    additional = f"Your file has {row_count:,} rows" if row_count else None
    show_error('file_too_large', lang, additional)

def show_encoding_error(lang='vi'):
    show_error('encoding_error', lang)

def show_date_format_error(lang='vi'):
    show_error('date_format_error', lang)
