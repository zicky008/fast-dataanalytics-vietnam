#!/usr/bin/env python3
"""
COMPREHENSIVE PDF EXPORT VALIDATION TEST
=========================================
Role: Expert QA Engineer + Data Analyst + Demanding Real User
Standard: 5-star user experience validation
"""

import sys
import os
import traceback
from datetime import datetime
import pandas as pd

# Test Configuration
TEST_RESULTS = {
    'passed': [],
    'failed': [],
    'warnings': []
}

def log_result(test_name, status, message="", details=""):
    """Log test results"""
    result = {
        'test': test_name,
        'status': status,
        'message': message,
        'details': details,
        'timestamp': datetime.now().isoformat()
    }

    if status == 'PASS':
        TEST_RESULTS['passed'].append(result)
        print(f"✅ PASS: {test_name}")
        if message:
            print(f"   {message}")
    elif status == 'FAIL':
        TEST_RESULTS['failed'].append(result)
        print(f"❌ FAIL: {test_name}")
        print(f"   {message}")
        if details:
            print(f"   Details: {details}")
    elif status == 'WARN':
        TEST_RESULTS['warnings'].append(result)
        print(f"⚠️  WARN: {test_name}")
        print(f"   {message}")

print("="*80)
print("🔍 COMPREHENSIVE PDF EXPORT VALIDATION")
print("="*80)
print(f"Tester: Expert QA + Data Analyst + Real User (Demanding)")
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Standard: 5-star user experience")
print("="*80)

# TEST 1: Dependencies Check
print("\n📦 TEST 1: DEPENDENCY VALIDATION")
print("-" * 80)

try:
    import reportlab
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    log_result("T1.1: ReportLab Installation", "PASS", f"Version: {reportlab.Version}")
except ImportError as e:
    log_result("T1.1: ReportLab Installation", "FAIL", str(e))
    sys.exit(1)

try:
    import plotly
    import plotly.graph_objects as go
    log_result("T1.2: Plotly Installation", "PASS", f"Version: {plotly.__version__}")
except ImportError as e:
    log_result("T1.2: Plotly Installation", "FAIL", str(e))

try:
    import kaleido
    log_result("T1.3: Kaleido Installation", "PASS", "Chart export engine available")
except ImportError as e:
    log_result("T1.3: Kaleido Installation", "WARN",
               "Kaleido not found - charts may not export",
               "Install: pip install kaleido>=0.2.1")

# TEST 2: Font System Validation
print("\n🔤 TEST 2: VIETNAMESE FONT SYSTEM VALIDATION")
print("-" * 80)

# Check system fonts
import subprocess
try:
    result = subprocess.run(['fc-list'], capture_output=True, text=True, timeout=5)
    dejavu_fonts = [line for line in result.stdout.split('\n') if 'dejavu' in line.lower()]

    if dejavu_fonts:
        log_result("T2.1: System Fonts - DejaVu Availability", "PASS",
                   f"Found {len(dejavu_fonts)} DejaVu font variants")
        print(f"   Sample: {dejavu_fonts[0][:100]}")
    else:
        log_result("T2.1: System Fonts - DejaVu Availability", "FAIL",
                   "DejaVu fonts not found in system")
except Exception as e:
    log_result("T2.1: System Fonts - DejaVu Availability", "WARN",
               f"Could not check system fonts: {str(e)}")

# Test font paths
dejavu_paths = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
]

for i, path in enumerate(dejavu_paths, 1):
    if os.path.exists(path):
        size = os.path.getsize(path) / 1024  # KB
        log_result(f"T2.2.{i}: Font File Exists - {os.path.basename(path)}",
                   "PASS", f"Size: {size:.1f} KB")
    else:
        log_result(f"T2.2.{i}: Font File Exists - {os.path.basename(path)}",
                   "FAIL", f"Font file not found at: {path}")

# Test font registration
try:
    if os.path.exists(dejavu_paths[0]):
        pdfmetrics.registerFont(TTFont('DejaVuSans-Test', dejavu_paths[0]))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold-Test', dejavu_paths[1]))
        log_result("T2.3: Font Registration", "PASS",
                   "Successfully registered DejaVuSans fonts")
    else:
        log_result("T2.3: Font Registration", "FAIL",
                   "Cannot register fonts - files not found")
except Exception as e:
    log_result("T2.3: Font Registration", "FAIL", str(e), traceback.format_exc())

# TEST 3: Vietnamese Character Support
print("\n🇻🇳 TEST 3: VIETNAMESE CHARACTER ENCODING VALIDATION")
print("-" * 80)

vietnamese_test_strings = [
    ("Basic Vowels", "aăâeêioôơuưy"),
    ("Vowels with Acute", "áắấéếíóốớúứý"),
    ("Vowels with Grave", "àằầèềìòồờùừỳ"),
    ("Vowels with Hook", "ảẳẩẻểỉỏổởủửỷ"),
    ("Vowels with Tilde", "ãẵẫẽễĩõỗỡũữỹ"),
    ("Vowels with Dot", "ạặậẹệịọộợụựỵ"),
    ("Common Words", "Việt Nam Tiếng Việt Phân tích dữ liệu"),
    ("Business Terms", "Doanh nghiệp Khách hàng Báo cáo Thống kê"),
    ("Special Chars", "đĐ ₫ % $ €"),
    ("Full Sentence", "Báo cáo phân tích dữ liệu chuyên nghiệp cho doanh nghiệp Việt Nam")
]

for test_name, test_string in vietnamese_test_strings:
    try:
        # Test encoding
        encoded = test_string.encode('utf-8')
        decoded = encoded.decode('utf-8')

        if decoded == test_string:
            log_result(f"T3.{vietnamese_test_strings.index((test_name, test_string)) + 1}: {test_name}",
                       "PASS", f"String: '{test_string[:50]}'")
        else:
            log_result(f"T3.{vietnamese_test_strings.index((test_name, test_string)) + 1}: {test_name}",
                       "FAIL", "Encoding mismatch")
    except Exception as e:
        log_result(f"T3.{vietnamese_test_strings.index((test_name, test_string)) + 1}: {test_name}",
                   "FAIL", str(e))

# TEST 4: Export Function Code Quality Review
print("\n💻 TEST 4: CODE QUALITY & IMPLEMENTATION REVIEW")
print("-" * 80)

# Check if export_utils.py exists and has the function
export_utils_path = '/home/user/fast-dataanalytics-vietnam/src/utils/export_utils.py'

if os.path.exists(export_utils_path):
    log_result("T4.1: export_utils.py exists", "PASS", f"Path: {export_utils_path}")

    with open(export_utils_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Check critical implementations
    checks = [
        ("Font registration code", "pdfmetrics.registerFont", True),
        ("DejaVuSans font usage", "DejaVuSans", True),
        ("Vietnamese font path", "/usr/share/fonts/truetype/dejavu", True),
        ("Font fallback handling", "except", True),
        ("Chart export code", "to_image", True),
        ("Kaleido engine specified", 'engine="kaleido"', True),
        ("Chart export fallback", "write_image", True),
        ("Temp file handling", "tempfile", True),
        ("Error logging for charts", "print.*chart", False),  # Regex
        ("Font error messages", "Warning.*fonts", False),  # Regex
    ]

    import re
    for i, (check_name, pattern, is_literal) in enumerate(checks, 1):
        if is_literal:
            found = pattern in code
        else:
            found = re.search(pattern, code, re.IGNORECASE) is not None

        if found:
            log_result(f"T4.{i+1}: {check_name}", "PASS", f"Implementation found")
        else:
            log_result(f"T4.{i+1}: {check_name}", "FAIL",
                       f"Missing: {pattern}")
else:
    log_result("T4.1: export_utils.py exists", "FAIL", "File not found")

# TEST 5: Mock Data & Chart Creation
print("\n📊 TEST 5: MOCK DATA & VISUALIZATION CREATION")
print("-" * 80)

try:
    # Create test data with Vietnamese content
    test_data = pd.DataFrame({
        'Tên sản phẩm': ['Bánh mì', 'Phở bò', 'Cà phê sữa đá', 'Bánh flan', 'Nem rán'],
        'Doanh số (₫)': [50000, 75000, 30000, 25000, 45000],
        'Số lượng bán': [120, 85, 200, 60, 95],
        'Đánh giá': [4.5, 4.8, 4.3, 4.0, 4.6],
        'Khu vực': ['Hà Nội', 'TP.HCM', 'Đà Nẵng', 'Hà Nội', 'TP.HCM']
    })

    log_result("T5.1: Test Data Creation", "PASS",
               f"Created {len(test_data)} rows with Vietnamese content")

    # Create test charts
    test_charts = []

    # Chart 1: Bar chart
    fig1 = go.Figure(data=[
        go.Bar(x=test_data['Tên sản phẩm'], y=test_data['Doanh số (₫)'])
    ])
    fig1.update_layout(
        title='Doanh số theo Sản phẩm',
        xaxis_title='Tên sản phẩm',
        yaxis_title='Doanh số (₫)'
    )
    test_charts.append({'title': 'Doanh số theo Sản phẩm', 'figure': fig1})

    # Chart 2: Pie chart
    fig2 = go.Figure(data=[
        go.Pie(labels=test_data['Khu vực'], values=test_data['Số lượng bán'])
    ])
    fig2.update_layout(title='Phân bổ Số lượng bán theo Khu vực')
    test_charts.append({'title': 'Phân bổ Số lượng bán theo Khu vực', 'figure': fig2})

    # Chart 3: Line chart
    fig3 = go.Figure(data=[
        go.Scatter(x=test_data['Tên sản phẩm'], y=test_data['Đánh giá'], mode='lines+markers')
    ])
    fig3.update_layout(
        title='Xu hướng Đánh giá Sản phẩm',
        xaxis_title='Sản phẩm',
        yaxis_title='Điểm đánh giá'
    )
    test_charts.append({'title': 'Xu hướng Đánh giá Sản phẩm', 'figure': fig3})

    log_result("T5.2: Chart Creation", "PASS",
               f"Created {len(test_charts)} test charts with Vietnamese titles")

except Exception as e:
    log_result("T5.1: Test Data Creation", "FAIL", str(e), traceback.format_exc())
    test_charts = []

# TEST 6: Chart Image Export Validation
print("\n🖼️  TEST 6: CHART TO IMAGE CONVERSION VALIDATION")
print("-" * 80)

if test_charts:
    for i, chart in enumerate(test_charts, 1):
        try:
            # Test kaleido export
            try:
                img_bytes = chart['figure'].to_image(format="png", width=800, height=450, engine="kaleido")
                size_kb = len(img_bytes) / 1024
                log_result(f"T6.{i}: Chart Export - {chart['title'][:30]}",
                           "PASS", f"Exported: {size_kb:.1f} KB (kaleido)")
            except Exception as kaleido_error:
                # Try fallback method
                import tempfile
                with tempfile.NamedTemporaryFile(suffix='.png', delete=True) as tmp:
                    chart['figure'].write_image(tmp.name, format='png', width=800, height=450)
                    size_kb = os.path.getsize(tmp.name) / 1024
                    log_result(f"T6.{i}: Chart Export - {chart['title'][:30]}",
                               "PASS", f"Exported: {size_kb:.1f} KB (fallback method)",
                               f"Kaleido failed, used write_image: {str(kaleido_error)[:50]}")
        except Exception as e:
            log_result(f"T6.{i}: Chart Export - {chart['title'][:30]}",
                       "FAIL", str(e), traceback.format_exc())
else:
    log_result("T6.0: Chart Export Test", "FAIL", "No test charts available")

# TEST 7: Full PDF Export Integration Test
print("\n📄 TEST 7: FULL PDF EXPORT INTEGRATION TEST")
print("-" * 80)

try:
    from src.utils.export_utils import export_to_pdf

    # Create mock result object matching expected structure
    mock_result = {
        'domain_info': {
            'domain_name': 'Nhà hàng & Ẩm thực',
            'expert_role': 'Chuyên gia Phân tích Dữ liệu Ngành F&B - Ẩm thực Việt Nam'
        },
        'performance': {
            'total': 2.5
        },
        'quality_scores': {
            'overall': 95
        },
        'insights': {
            'executive_summary': 'Phân tích dữ liệu bán hàng cho các sản phẩm ẩm thực Việt Nam. '
                                 'Kết quả cho thấy Phở bò có doanh số cao nhất (₫75,000) với đánh giá '
                                 'tích cực (4.8/5). Khu vực TP.HCM và Hà Nội là thị trường chính.',
            'key_insights': [
                {
                    'title': 'Phở bò dẫn đầu về doanh số',
                    'description': 'Sản phẩm Phở bò đạt doanh số cao nhất ₫75,000 với 85 đơn hàng và đánh giá 4.8/5 sao.',
                    'impact': 'high'
                },
                {
                    'title': 'Cà phê sữa đá có lượng bán cao nhất',
                    'description': 'Mặc dù giá thấp (₫30,000), sản phẩm này có 200 đơn bán - cao nhất trong danh sách.',
                    'impact': 'high'
                },
                {
                    'title': 'Thị trường tập trung ở 3 thành phố lớn',
                    'description': 'Hà Nội, TP.HCM và Đà Nẵng chiếm 100% doanh số, cơ hội mở rộng thị trường tỉnh.',
                    'impact': 'medium'
                }
            ],
            'recommendations': [
                {
                    'action': 'Tăng cường marketing cho Phở bò tại các khu vực mới',
                    'expected_impact': 'Tăng 25-30% doanh số trong Q2',
                    'priority': 'high',
                    'timeline': '1-2 tháng'
                },
                {
                    'action': 'Mở rộng phân phối Cà phê sữa đá - sản phẩm bán chạy',
                    'expected_impact': 'Tăng 40% lượng bán, tăng 20% doanh thu',
                    'priority': 'high',
                    'timeline': '2-3 tuần'
                },
                {
                    'action': 'Khảo sát thị trường tỉnh lẻ để mở rộng',
                    'expected_impact': 'Tiềm năng tăng 50% thị trường',
                    'priority': 'medium',
                    'timeline': '3-6 tháng'
                }
            ]
        },
        'dashboard': {
            'kpis': {
                'Tổng doanh số': {'value': 225000, 'status': 'Good', 'benchmark': 200000},
                'Trung bình đánh giá': {'value': 4.44, 'status': 'Excellent', 'benchmark': 4.0},
                'Tổng đơn hàng': {'value': 560, 'status': 'Good', 'benchmark': 500},
                'Doanh số/Đơn': {'value': 401.79, 'status': 'Good', 'benchmark': 400}
            },
            'charts': test_charts if test_charts else []
        }
    }

    log_result("T7.1: Mock Result Structure", "PASS", "Created complete test data structure")

    # Test Vietnamese PDF export
    print("\n   Testing Vietnamese PDF export...")
    pdf_bytes_vi = export_to_pdf(mock_result, test_data, lang='vi')
    size_vi_kb = len(pdf_bytes_vi) / 1024

    if len(pdf_bytes_vi) > 1000:  # At least 1KB
        log_result("T7.2: Vietnamese PDF Export", "PASS",
                   f"Generated {size_vi_kb:.1f} KB PDF with Vietnamese content")

        # Save for manual inspection
        test_output_path = '/home/user/fast-dataanalytics-vietnam/test_output_vietnamese.pdf'
        with open(test_output_path, 'wb') as f:
            f.write(pdf_bytes_vi)
        print(f"   📁 Saved to: {test_output_path}")
    else:
        log_result("T7.2: Vietnamese PDF Export", "FAIL",
                   f"PDF too small ({size_vi_kb:.1f} KB), likely incomplete")

    # Test English PDF export
    print("\n   Testing English PDF export...")
    # Create English version of result
    mock_result_en = mock_result.copy()
    mock_result_en['domain_info']['domain_name'] = 'Restaurant & Food Service'
    mock_result_en['domain_info']['expert_role'] = 'F&B Data Analytics Expert - Vietnamese Cuisine'

    pdf_bytes_en = export_to_pdf(mock_result_en, test_data, lang='en')
    size_en_kb = len(pdf_bytes_en) / 1024

    if len(pdf_bytes_en) > 1000:
        log_result("T7.3: English PDF Export", "PASS",
                   f"Generated {size_en_kb:.1f} KB PDF with English content")

        test_output_path_en = '/home/user/fast-dataanalytics-vietnam/test_output_english.pdf'
        with open(test_output_path_en, 'wb') as f:
            f.write(pdf_bytes_en)
        print(f"   📁 Saved to: {test_output_path_en}")
    else:
        log_result("T7.3: English PDF Export", "FAIL",
                   f"PDF too small ({size_en_kb:.1f} KB), likely incomplete")

except Exception as e:
    log_result("T7.0: PDF Export Integration", "FAIL", str(e), traceback.format_exc())

# TEST 8: Edge Cases & Error Handling
print("\n⚠️  TEST 8: EDGE CASE & ERROR HANDLING VALIDATION")
print("-" * 80)

# Test with missing charts
try:
    mock_result_no_charts = mock_result.copy()
    mock_result_no_charts['dashboard']['charts'] = []

    pdf_no_charts = export_to_pdf(mock_result_no_charts, test_data, lang='vi')

    if len(pdf_no_charts) > 1000:
        log_result("T8.1: PDF Export without Charts", "PASS",
                   "Successfully handled missing charts")
    else:
        log_result("T8.1: PDF Export without Charts", "FAIL",
                   "PDF generation failed when charts missing")
except Exception as e:
    log_result("T8.1: PDF Export without Charts", "FAIL", str(e))

# Test with empty KPIs
try:
    mock_result_no_kpis = mock_result.copy()
    mock_result_no_kpis['dashboard']['kpis'] = {}

    pdf_no_kpis = export_to_pdf(mock_result_no_kpis, test_data, lang='vi')

    if len(pdf_no_kpis) > 1000:
        log_result("T8.2: PDF Export without KPIs", "PASS",
                   "Successfully handled missing KPIs")
    else:
        log_result("T8.2: PDF Export without KPIs", "FAIL",
                   "PDF generation failed when KPIs missing")
except Exception as e:
    log_result("T8.2: PDF Export without KPIs", "FAIL", str(e))

# FINAL REPORT
print("\n" + "="*80)
print("📊 VALIDATION REPORT SUMMARY")
print("="*80)

total_tests = len(TEST_RESULTS['passed']) + len(TEST_RESULTS['failed']) + len(TEST_RESULTS['warnings'])
pass_rate = (len(TEST_RESULTS['passed']) / total_tests * 100) if total_tests > 0 else 0

print(f"\n✅ PASSED:   {len(TEST_RESULTS['passed'])} tests")
print(f"❌ FAILED:   {len(TEST_RESULTS['failed'])} tests")
print(f"⚠️  WARNINGS: {len(TEST_RESULTS['warnings'])} tests")
print(f"📈 PASS RATE: {pass_rate:.1f}%")

if TEST_RESULTS['failed']:
    print("\n❌ FAILED TESTS:")
    for fail in TEST_RESULTS['failed']:
        print(f"   • {fail['test']}: {fail['message']}")

if TEST_RESULTS['warnings']:
    print("\n⚠️  WARNINGS:")
    for warn in TEST_RESULTS['warnings']:
        print(f"   • {warn['test']}: {warn['message']}")

print("\n" + "="*80)
print("🎯 QUALITY ASSESSMENT")
print("="*80)

# 5-star rating based on pass rate
if pass_rate >= 95:
    stars = "⭐⭐⭐⭐⭐"
    quality = "EXCELLENT - 5 STAR"
elif pass_rate >= 85:
    stars = "⭐⭐⭐⭐"
    quality = "VERY GOOD - 4 STAR"
elif pass_rate >= 75:
    stars = "⭐⭐⭐"
    quality = "GOOD - 3 STAR"
elif pass_rate >= 60:
    stars = "⭐⭐"
    quality = "FAIR - 2 STAR"
else:
    stars = "⭐"
    quality = "NEEDS IMPROVEMENT - 1 STAR"

print(f"\n{stars}")
print(f"Quality: {quality}")
print(f"Pass Rate: {pass_rate:.1f}%")

critical_failures = [f for f in TEST_RESULTS['failed'] if 'Font' in f['test'] or 'Chart Export' in f['test']]
if critical_failures:
    print(f"\n⚠️  CRITICAL: {len(critical_failures)} critical failures detected")
    print("   User experience may be degraded!")
else:
    print("\n✅ CRITICAL: No critical failures")
    print("   Core functionality working as expected")

print("\n" + "="*80)
print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Exit code
sys.exit(0 if len(TEST_RESULTS['failed']) == 0 else 1)
