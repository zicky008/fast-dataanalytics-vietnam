#!/usr/bin/env python3
"""
Test NEW PDF improvements:
1. Unicode symbols (NO emoji)
2. Bold key metrics in insights
3. Professional recommendations formatting
4. Callout boxes validation
"""

# Mock result for testing PDF export directly
mock_result = {
    'domain_info': {
        'domain': 'Restaurant & Food',
        'domain_name': 'Nhà hàng & Ẩm thực',
        'expert_role': 'Chuyên gia Phân tích Dữ liệu Ngành F&B - Ẩm thực Việt Nam'
    },
    'insights': {
        'executive_summary': 'Phân tích dữ liệu bán hàng cho các sản phẩm ẩm thực Việt Nam. Kết quả cho thấy Phở bò có doanh số cao nhất (₫75,000) với đánh giá tích cực (4.8/5). Khu vực TP.HCM và Hà Nội là thị trường chính.',
        'key_insights': [
            {
                'title': 'Phở bò dẫn đầu về doanh số',
                'description': 'Sản phẩm Phở bò đạt doanh số cao nhất ₫75,000 với 85 đơn hàng và đánh giá 4.8/5 sao.',
                'impact': 'high'
            },
            {
                'title': 'Cà phê sữa đá có lượng bán cao nhất',
                'description': 'Mặc dù giá thấp (₫30,000), sản phẩm này có 200 đơn bán - cao nhất trong danh sách.',
                'impact': 'medium'
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
                'timeline': '1-2 tháng',
                'priority': 'high'
            },
            {
                'action': 'Mở rộng phân phối Cà phê sữa đá - sản phẩm bán chạy',
                'expected_impact': 'Tăng 40% lượng bán, tăng 20% doanh thu',
                'timeline': '2-3 tuần',
                'priority': 'high'
            },
            {
                'action': 'Khảo sát thị trường tỉnh lẻ để mở rộng',
                'expected_impact': 'Tiềm năng tăng 50% thị trường',
                'timeline': '3-6 tháng',
                'priority': 'medium'
            }
        ]
    },
    'dashboard': {
        'kpis': {
            'Tổng doanh số': {
                'value': 225000.0,
                'status': 'Good',
                'benchmark': 200000,
                'benchmark_source': 'HubSpot Marketing Benchmarks'
            },
            'Trung bình đánh giá': {
                'value': 4.4,
                'status': 'Excellent',
                'benchmark': 4.0,
                'benchmark_source': 'Zendesk Support Benchmarks'
            },
            'Tổng đơn hàng': {
                'value': 560.0,
                'status': 'Good',
                'benchmark': 500,
                'benchmark_source': 'Gartner IT Benchmarks'
            },
            'Doanh số/Đơn': {
                'value': 401.8,
                'status': 'Good',
                'benchmark': 400,
                'benchmark_source': 'McKinsey Manufacturing Report'
            }
        },
        'charts': []  # No charts for this test
    },
    'performance': {
        'total': 2.5
    },
    'quality_scores': {
        'overall': 95
    }
}

# Mock DataFrame
class MockDataFrame:
    def __init__(self, data):
        self.data = data
        self.columns = list(data.keys())
        self._rows = len(list(data.values())[0])

    def __len__(self):
        return self._rows

    def select_dtypes(self, include=None):
        # Return mock with numeric columns
        numeric_cols = ['Doanh số', 'Đơn hàng', 'Đánh giá']

        class MockSubset:
            def __init__(self, cols):
                self.columns = cols
        return MockSubset(numeric_cols)

    def isnull(self):
        class MockNull:
            def sum(self):
                class MockSum:
                    def sum(self):
                        return 0
                return MockSum()
        return MockNull()

# Create mock df
df_data = {
    'Sản phẩm': ['Phở bò', 'Cà phê sữa đá', 'Bánh mì', 'Bún chả', 'Chè'],
    'Doanh số': [75000, 30000, 45000, 60000, 35000],
    'Đơn hàng': [85, 200, 120, 95, 110],
    'Đánh giá': [4.8, 4.2, 4.5, 4.6, 4.3],
    'Khu vực': ['TP.HCM', 'Hà Nội', 'Đà Nẵng', 'Hà Nội', 'TP.HCM']
}

df = MockDataFrame(df_data)

print("=" * 80)
print("🧪 TESTING NEW PDF IMPROVEMENTS")
print("=" * 80)
print("")
print("✅ Expected improvements:")
print("  1. Unicode symbols (» ■ ◆ ▶ ▪) instead of emoji")
print("  2. Auto-bold key metrics (₫75,000, 4.8/5, 85 đơn)")
print("  3. Professional recommendations with symbols (▲ ● ▼)")
print("  4. Callout boxes for Executive Summary")
print("  5. Clickable benchmark sources")
print("")
print("=" * 80)
print("📄 Generating PDF...")
print("=" * 80)
print("")

# Import and generate
from src.utils.export_utils import export_to_pdf

try:
    pdf_bytes = export_to_pdf(mock_result, df, lang='vi')

    # Save to file
    output_file = 'test_output_NEW_IMPROVED.pdf'
    with open(output_file, 'wb') as f:
        f.write(pdf_bytes)

    print(f"✅ SUCCESS: PDF generated!")
    print(f"   File: {output_file}")
    print(f"   Size: {len(pdf_bytes):,} bytes")
    print("")
    print("=" * 80)
    print("🔍 VALIDATION CHECKLIST")
    print("=" * 80)
    print("")
    print("Open the PDF and verify:")
    print("  [ ] Section titles use Unicode symbols (» ■ ◆ ▶ ▪) NOT emoji")
    print("  [ ] Executive Summary has callout box (bordered, light background)")
    print("  [ ] KPI table has 'Nguồn' (Source) column")
    print("  [ ] Benchmark sources are blue underlined links (clickable)")
    print("  [ ] Status indicators use ▲▼● symbols with colors")
    print("  [ ] Insights: Key metrics are BOLDED (₫75,000, 4.8/5, etc.)")
    print("  [ ] Insights: Impact labels are colored ([HIGH IMPACT] in red)")
    print("  [ ] Recommendations: Priority symbols (▲ ● ▼) visible")
    print("  [ ] Recommendations: Clear structure with bold labels")
    print("  [ ] Responsible party shown for each recommendation")
    print("")
    print("=" * 80)
    print("📊 COMPARISON INSTRUCTIONS")
    print("=" * 80)
    print("")
    print("Compare these files:")
    print(f"  OLD: test_output_vietnamese.pdf")
    print(f"  NEW: {output_file}")
    print("")
    print("Expected differences:")
    print("  • Icons: 📋📊 → » ■ (more professional, reliable rendering)")
    print("  • Insights: Plain text → Bold metrics + colored labels")
    print("  • Recommendations: Basic list → Structured with symbols")
    print("  • Executive Summary: Plain paragraph → Callout box")
    print("")

except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
