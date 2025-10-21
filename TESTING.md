# 🧪 Testing Guide - DataAnalytics Vietnam

## 📋 Overview

Tài liệu này hướng dẫn test **Premium Lean Pipeline** với **Real Gemini API**.

---

## 🚀 Quick Test (3 phút)

### Bước 1: Setup API Key

```bash
# Copy template
cp .env.template .env

# Edit .env và thêm API key
nano .env  # hoặc dùng editor bất kỳ
```

**File `.env` sau khi sửa:**
```bash
GEMINI_API_KEY=AIzaSyAbc123YourActualKeyHere
```

**Lấy API key miễn phí:**
👉 https://aistudio.google.com/app/apikey

---

### Bước 2: Cài Dependencies

```bash
# Activate virtual environment (nếu chưa)
source venv/bin/activate  # Mac/Linux
# hoặc: venv\Scripts\activate  # Windows

# Cài dependencies
pip install -r requirements.txt
```

---

### Bước 3: Run Tests

```bash
# Run comprehensive test suite
python test_real_api.py
```

**Kết quả mong đợi:**

```
🧪 DataAnalytics Vietnam - Real API Testing
============================================================

TEST 1: Gemini API Connection
============================================================
✅ API Key found: AIzaSyAbc123...xyz
✅ API Response: OK
✅ PASSED: Gemini API connection successful

TEST 2: Marketing Pipeline (Google Ads)
============================================================
📁 Loading: marketing_google_ads.csv
✅ Data loaded: 21 rows × 7 columns

⏱️  Starting pipeline...

✅ Pipeline completed in 52.3 seconds

📊 Validation Results:
------------------------------------------------------------
✅ Status: success
✅ Domain: Marketing / Quảng Cáo
✅ Quality Score: 87.5/100
✅ Charts Generated: 9
✅ Insights Generated: 6
✅ KPIs Calculated: 4
   - ROAS: 5.14 (Above)
   - CTR: 3.89% (Above)
   - CPC: 2.51 (Below)
   - CPA: 77.14 (Below)

⏱️  Performance:
   - Total Time: 52.3s
   - Target: <60s
   ✅ Within target (7.7s buffer)

✅ PASSED: Marketing Pipeline Test

[... more tests ...]

📊 TEST SUMMARY
============================================================
✅ PASSED: Gemini Connection
✅ PASSED: Marketing Pipeline
✅ PASSED: E-commerce Pipeline
✅ PASSED: Rate Limiting

Total: 4/4 tests passed

🎉 ALL TESTS PASSED! Pipeline is ready for deployment.
```

---

## 📊 Test Suite Details

### Test 1: Gemini API Connection

**Kiểm tra:**
- ✅ API key format (phải bắt đầu với `AIza`)
- ✅ API key valid (call thử)
- ✅ Response structure đúng

**Expected Time:** <5 giây

---

### Test 2: Marketing Pipeline

**Sample Data:** `sample_data/marketing_google_ads.csv`
- 21 rows × 7 columns
- Google Ads campaigns (Brand, Search, Display, Retargeting, Video, Social, Email)

**Kiểm tra:**
- ✅ Domain detection: "Marketing / Quảng Cáo"
- ✅ Quality Score: ≥80/100
- ✅ Charts: 8-10 biểu đồ
- ✅ Insights: 5-7 insights
- ✅ KPIs: ROAS, CTR, CPC, CPA, CLV
- ✅ Benchmarks: So sánh với chuẩn 2024

**Expected Time:** 50-60 giây

---

### Test 3: E-commerce Pipeline

**Sample Data:** `sample_data/ecommerce_shopify.csv`
- 20 rows × 10 columns
- Shopify orders (Products, Categories, Revenue, Discounts)

**Kiểm tra:**
- ✅ Domain detection: "E-commerce"
- ✅ Quality Score: ≥80/100
- ✅ KPIs: AOV, Conversion Rate, CLV, Cart Abandonment
- ✅ Benchmarks: AOV $81.49, CR 2-3%

**Expected Time:** 50-60 giây

---

### Test 4: Rate Limiting

**Kiểm tra:**
- ✅ Free tier limit: 15 requests/minute
- ✅ Exponential backoff: 2s → 4s → 8s
- ✅ Automatic retry on 429 errors

**Expected Behavior:**
- Rapid requests → some may be rate limited
- System auto-retries với delay
- Vietnamese messages: "⏳ Gemini API đang bận, chờ Xs..."

---

## 🐛 Troubleshooting

### Error: "GEMINI_API_KEY not found in .env"

```bash
# Check .env file exists
ls -la .env

# If not, copy template
cp .env.template .env

# Edit and add API key
nano .env
```

---

### Error: "Invalid API key format"

API key phải:
- ✅ Bắt đầu với `AIza`
- ✅ Dài ~39 ký tự
- ✅ Không có khoảng trắng

**Fix:**
```bash
# Get new key from
https://aistudio.google.com/app/apikey

# Copy EXACTLY (no spaces, quotes)
GEMINI_API_KEY=AIzaSyAbc123...
```

---

### Error: "429 Rate Limit Exceeded"

**Nguyên nhân:** Vượt quá 15 requests/minute (free tier)

**Fix:**
1. Đợi 1 phút
2. Chạy lại test
3. Hệ thống tự retry với backoff

---

### Error: "JSON parsing failed"

**Nguyên nhân:** Gemini API response không phải JSON hợp lệ

**Debug:**
```python
# Check raw response
print(response.text)

# Validate JSON
import json
json.loads(response.text)
```

**Possible causes:**
- API trả về markdown thay vì JSON
- Response bị truncate (quá dài)
- Model không follow prompt format

**Fix:**
- Cải thiện prompt với JSON schema
- Thêm validation/retry logic
- Giảm output size

---

### Performance: Pipeline quá 60 giây

**Nguyên nhân:**
- Internet chậm
- Gemini API overloaded
- Dataset quá lớn (>100k rows)

**Fix:**
1. **Kiểm tra internet:**
   ```bash
   curl -w "@curl-format.txt" -o /dev/null -s https://generativelanguage.googleapis.com/
   ```

2. **Giảm dataset size:**
   ```python
   df = df.sample(n=1000)  # Random 1000 rows
   ```

3. **Optimize prompts:**
   - Giảm context trong prompts
   - Combine thêm steps
   - Cache frequent queries

---

## 📈 Performance Benchmarks

### Expected Results

| Dataset Size | Domain | Time (s) | Quality | Charts | Insights |
|--------------|--------|----------|---------|--------|----------|
| 21 rows | Marketing | 50-55 | 85-90 | 8-10 | 5-7 |
| 20 rows | E-commerce | 50-55 | 80-85 | 8-10 | 5-7 |
| 15 rows | Sales | 50-55 | 80-85 | 8-10 | 5-7 |
| 1,000 rows | Marketing | 52-58 | 85-90 | 8-10 | 5-7 |
| 10,000 rows | E-commerce | 55-60 | 80-85 | 8-10 | 5-7 |

### Bottlenecks

Nếu pipeline chậm, check từng step:

```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run pipeline
result = pipeline.run_pipeline(df, description)

# Check logs
# Step 0 (Domain): Should be <5s (3s if cached)
# Step 1 (Cleaning): Should be <15s
# Step 2 (Blueprint): Should be <15s (combined EDA + Blueprint)
# Step 3 (Insights): Should be <15s
```

**Typical breakdown:**
- Step 0: 3s (cached) or 5s (uncached)
- Step 1: 12-15s
- Step 2: 12-15s
- Step 3: 12-15s
- **Total:** 50-55s ✅

---

## 🔬 Advanced Testing

### Test với Custom Data

```python
import pandas as pd
from src.premium_lean_pipeline import PremiumLeanPipeline
import google.generativeai as genai

# Load your data
df = pd.read_csv('your_data.csv')

# Initialize
genai.configure(api_key='your_key')
client = genai.GenerativeModel('gemini-2.0-flash-exp')
pipeline = PremiumLeanPipeline(client)

# Run
result = pipeline.run_pipeline(
    df=df,
    dataset_description="Your description here"
)

# Check results
print(f"Domain: {result['domain_info']['name']}")
print(f"Quality: {result['quality_score']:.1f}/100")
print(f"Charts: {len(result['dashboard']['charts'])}")
print(f"Insights: {len(result['insights']['key_insights'])}")
```

---

### Test Rate Limiting Behavior

```python
import time
import google.generativeai as genai

genai.configure(api_key='your_key')
client = genai.GenerativeModel('gemini-2.0-flash-exp')

# Send 20 rapid requests (exceed 15/min limit)
for i in range(20):
    try:
        response = client.generate_content(f"Test {i}")
        print(f"✅ Request {i}: Success")
    except Exception as e:
        if '429' in str(e):
            print(f"⏳ Request {i}: Rate limited (expected)")
            time.sleep(4)  # Wait and retry
        else:
            raise
```

---

### Load Testing (Stress Test)

```python
import concurrent.futures
import time

def run_pipeline_test(test_id):
    """Run pipeline in parallel"""
    result = pipeline.run_pipeline(df, f"Test {test_id}")
    return result['quality_score']

# Run 5 pipelines concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(run_pipeline_test, i) for i in range(5)]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]

print(f"Average Quality: {sum(results)/len(results):.1f}")
```

**Expected:**
- Most will hit rate limits
- Automatic retry với backoff
- All eventually succeed

---

## ✅ Success Criteria

Pipeline được coi là **production-ready** nếu:

- [x] ✅ Gemini API connection successful
- [x] ✅ Marketing pipeline: <60s, quality ≥80
- [x] ✅ E-commerce pipeline: <60s, quality ≥80
- [x] ✅ Rate limiting handled gracefully
- [x] ✅ JSON parsing 100% successful
- [x] ✅ Domain detection accuracy ≥90%
- [x] ✅ KPIs calculated correctly
- [x] ✅ Benchmarks comparison accurate
- [x] ✅ Charts render without errors
- [x] ✅ Insights meaningful and actionable

---

## 🎯 Next Steps After Testing

Nếu tất cả tests PASSED:

1. ✅ **Task #6 completed** → Mark as done
2. ⏭️  **Task #7: Performance Optimization** (nếu cần)
   - Profile bottlenecks
   - Optimize prompts
   - Add caching layers
3. ⏭️  **Task #8: Deploy to Streamlit Cloud**
   - Push to GitHub
   - Configure Streamlit Cloud
   - Add secrets (GEMINI_API_KEY)
4. ⏭️  **Task #9: User Acceptance Testing**
   - Recruit 1-2 friendly users
   - Observe usage
   - Collect feedback

---

## 📞 Need Help?

**Issues:**
- GitHub Issues: [Link]
- Email: support@dataanalytics.vn

**Questions:**
- Discord/Slack: [Link]
- Zalo/Telegram: [Contact]

---

**Happy Testing! 🧪🚀**
