# 🧪 PRODUCTION TEST MANUAL - Vietnam Benchmarks Integration

## Mục Đích
Test production app như **"người dùng khó tính nhất"** cho từng domain để validate Vietnam benchmark integration.

---

## Test Environment
- **Production URL**: https://fast-nicedashboard.streamlit.app/
- **Test Data**: 4 CSV files đã tạo sẵn
- **Testers**: 5 expert personas (HR, Marketing, E-commerce, Sales, Data Analyst)

---

## ✅ TEST 1: HR MANAGER - CHỊ LAN (35, HCMC, KHÓ TÍNH NHẤT)

### Persona:
- **Pain Point**: "Mất developer nào cũng đau đầu, không biết offer bao nhiêu"
- **Goal**: Xem salary của Developer 35M/tháng có competitive không so với Vietnam market
- **Success Criteria**: Phải thấy percentile, Vietnam context, benchmark source

### Test Steps:

#### Step 1: Access App
1. Mở browser: https://fast-nicedashboard.streamlit.app/
2. **CHECK**: App loads trong <3 seconds? ✅/❌
3. **CHECK**: Header hiển thị "DataAnalytics Vietnam - Bricks.ai"? ✅/❌
4. **CHECK**: Có 3 tabs: "Upload & Analyze", "Dashboard", "Insights"? ✅/❌

#### Step 2: Upload HR Data
1. Click tab "Upload & Analyze"
2. Click "Browse files" hoặc drag-drop `test_sample_hr_data.csv`
3. **CHECK**: File upload thành công? ✅/❌
4. **CHECK**: Hiển thị "✅ Đọc thành công: 15 dòng × 6 cột"? ✅/❌
5. **CHECK**: Button "🚀 Phân Tích Dữ Liệu" xuất hiện? ✅/❌

#### Step 3: Run Analysis
1. (Optional) Nhập description: "HR salary data Q1 2024"
2. Click "🚀 Phân Tích Dữ Liệu"
3. **CHECK**: Loading spinner xuất hiện? ✅/❌
4. **CHECK**: Progress messages hiển thị (Domain Detection, Data Cleaning, etc.)? ✅/❌
5. **CHECK**: Analysis hoàn thành trong <60 seconds? ✅/❌
6. **CHECK**: Success message: "✅ Hoàn thành! Pipeline chạy trong X giây"? ✅/❌

#### Step 4: View Dashboard
1. Click tab "Dashboard"
2. **CHECK**: Domain hiển thị: "HR / Nhân Sự" hoặc "General"? ✅/❌
3. **CHECK**: Có KPIs section với "📊 Key Performance Indicators"? ✅/❌

#### Step 5: Validate KPIs (CRITICAL!)
Tìm KPIs sau và check từng field:

**KPI: "Median Salary"** (hoặc "Average Salary"):
- **Value**: Hiển thị số VND (vd: 35,000,000)? ✅/❌
- **Benchmark**: Hiển thị số benchmark (vd: 32,500,000)? ✅/❌
- **Status**: Hiển thị "Above" hoặc "Below"? ✅/❌
- **🇻🇳 Vietnam Context**: Có dòng "🇻🇳 Tốt! Cao hơn X% thị trường Vietnam"? ✅/❌
- **📊 Benchmark Source**: Có dòng "📊 Michael Page Vietnam Salary Guide 2025"? ✅/❌
- **📈 Percentile**: Có dòng "📈 Percentile: 55th" (hoặc số khác)? ✅/❌

#### Step 6: Verify Insights
1. Click tab "Insights"
2. **CHECK**: "Executive Summary" có mention về salary? ✅/❌
3. **CHECK**: "Key Insights" có insights về compensation? ✅/❌
4. **CHECK**: "Recommendations" có actionable advice? ✅/❌

### Expected Result - Chị Lan's Reaction:
✅ **PASS (5/5 ⭐)**: "Perfect! Giờ tôi biết Developer 35M/tháng = 55th percentile Vietnam. Tôi tự tin giữ người!"

❌ **FAIL (2/5 ⭐)**: "App đẹp nhưng không có Vietnam benchmark. Tôi vẫn không biết competitive hay không."

---

## ✅ TEST 2: MARKETING MANAGER - ANH MINH (32, HCMC, KHÓ TÍNH NHẤT)

### Persona:
- **Pain Point**: "Facebook CPA ngày càng cao, sếp hỏi tại sao conversion rate thấp"
- **Goal**: So sánh Facebook Ads CPA với Vietnam benchmark
- **Success Criteria**: Phải thấy CPA benchmark cho Facebook Ads Vietnam

### Test Steps:

#### Step 1-3: Upload & Analyze
(Same as Test 1, but use `test_sample_marketing_data.csv`)
- **CHECK**: File uploaded: 10 dòng × 8 cột? ✅/❌
- **CHECK**: Domain detected: "Marketing / Quảng Cáo"? ✅/❌

#### Step 4: View Dashboard
1. Click tab "Dashboard"
2. **CHECK**: Domain: "Marketing / Quảng Cáo"? ✅/❌

#### Step 5: Validate KPIs (CRITICAL!)

**KPI: "Cost Per Acquisition (CPA)"**:
- **Value**: Hiển thị CPA tính được (vd: 95,000 VND)? ✅/❌
- **Benchmark**: Hiển thị benchmark (vd: 85,000 VND)? ✅/❌
- **Status**: "Above" (⚠️ High CPA) or "Below" (✅ Efficient)? ✅/❌
- **Insight**: Có text "Lower is better. Benchmark: 85,000 VND"? ✅/❌
- **🇻🇳 Vietnam Context**: Có message về CPA so với Vietnam market? ✅/❌
- **📊 Benchmark Source**: Có "Vietnam Digital Report 2024 (DataReportal)"? ✅/❌
- **📈 Percentile**: Có percentile ranking? ✅/❌

**Optional KPIs to check**:
- "ROAS" (Return on Ad Spend)
- "CTR (%)" (Click-Through Rate)
- "Conversion Rate (%)"

### Expected Result - Anh Minh's Reaction:
✅ **PASS (5/5 ⭐)**: "Amazing! CPA 95K cao hơn benchmark 85K. Tôi có proof để optimize budget!"

❌ **FAIL (2.5/5 ⭐)**: "Không có Vietnam benchmark. Tôi vẫn không biết CPA của tôi tốt hay xấu."

---

## ✅ TEST 3: E-COMMERCE OWNER - ANH TUẤN (38, HANOI, KHÓ TÍNH NHẤT)

### Persona:
- **Pain Point**: "COD fake orders 15%, cart abandonment 68% - cao hay bình thường?"
- **Goal**: So sánh metrics với Shopee Fashion Vietnam
- **Success Criteria**: Phải thấy platform-specific (Shopee) + category-specific (Fashion) benchmarks

### Test Steps:

#### Step 1-3: Upload & Analyze
(Use `test_sample_ecommerce_data.csv`)
- **CHECK**: File uploaded: 10 dòng × 10 cột? ✅/❌
- **CHECK**: Domain detected: "E-commerce / Bán Hàng Trực Tuyến"? ✅/❌

#### Step 4: View Dashboard
1. Click tab "Dashboard"
2. **CHECK**: Domain: "E-commerce"? ✅/❌

#### Step 5: Validate KPIs (CRITICAL!)

**KPI: "Conversion Rate (%)"**:
- **Value**: ~2.1% (calculated from test data)? ✅/❌
- **Benchmark**: ~2.3% (Vietnam average)? ✅/❌
- **Status**: "Below" or "Above"? ✅/❌
- **🇻🇳 Vietnam Context**: Mention về Shopee Fashion benchmark? ✅/❌
- **📊 Benchmark Source**: "VECOM EBI 2024"? ✅/❌
- **📈 Percentile**: Có percentile? ✅/❌

**KPI: "Cart Abandonment Rate (%)"**:
- **Value**: ~68% (calculated)? ✅/❌
- **Benchmark**: ~68% (Vietnam Fashion avg)? ✅/❌
- **Status**: "Normal" (not above/below)? ✅/❌
- **🇻🇳 Vietnam Context**: Có note về "voucher hunting behavior"? ✅/❌

**KPI: "Average Order Value (AOV)"**:
- **Value**: ~385,000 VND? ✅/❌
- **Benchmark**: Vietnam AOV benchmark? ✅/❌
- **🇻🇳 Vietnam Context**: Platform-specific context? ✅/❌

### Expected Result - Anh Tuấn's Reaction:
✅ **PASS (5/5 ⭐)**: "Tuyệt vời! 68% cart abandonment = NORMAL cho Fashion. Không stress nữa!"

❌ **FAIL (2/5 ⭐)**: "Không có Shopee benchmark. Tôi vẫn lo lắng về cart abandonment."

---

## ✅ TEST 4: SALES MANAGER - CHỊ HƯƠNG (34, HCMC, KHÓ TÍNH NHẤT)

### Persona:
- **Pain Point**: "Deal này 90 ngày rồi chưa close, sếp hỏi sao chậm thế"
- **Goal**: Defend sales cycle với Vietnam B2B benchmark
- **Success Criteria**: Phải thấy B2B SaaS sales cycle benchmark

### Test Steps:

#### Step 1-3: Upload & Analyze
(Use `test_sample_sales_b2b_data.csv`)
- **CHECK**: File uploaded: 13 dòng × 9 cột? ✅/❌
- **CHECK**: Domain detected: "Sales / Kinh Doanh"? ✅/❌

#### Step 4: View Dashboard
1. Click tab "Dashboard"
2. **CHECK**: Domain: "Sales / Kinh Doanh"? ✅/❌

#### Step 5: Validate KPIs (CRITICAL!)

**KPI: "Win Rate (%)"**:
- **Value**: ~25-30%? ✅/❌
- **Benchmark**: ~25% (Vietnam B2B avg)? ✅/❌
- **Status**: "Above" or "Below"? ✅/❌
- **🇻🇳 Vietnam Context**: Mention về B2B SaaS Vietnam? ✅/❌
- **📊 Benchmark Source**: "HubSpot Vietnam Data 2024"? ✅/❌
- **📈 Percentile**: Có percentile? ✅/❌

**KPI: "Sales Cycle (days)"**:
- **Value**: ~80-90 days? ✅/❌
- **Benchmark**: ~45-90 days (depending on segment)? ✅/❌
- **Status**: "Normal" for Enterprise? ✅/❌
- **🇻🇳 Vietnam Context**: Có note về "relationship-based selling"? ✅/❌
- **Insight**: "Bình thường cho Enterprise Vietnam"? ✅/❌

**KPI: "Average Deal Size"**:
- **Value**: ~50-60M VND for SME? ✅/❌
- **Benchmark**: Vietnam deal size benchmark? ✅/❌
- **🇻🇳 Vietnam Context**: Segment-specific (SME/Enterprise)? ✅/❌

### Expected Result - Chị Hương's Reaction:
✅ **PASS (5/5 ⭐)**: "Perfect! 90 days = NORMAL cho Enterprise. Defend được với sếp!"

❌ **FAIL (2.5/5 ⭐)**: "Không có Vietnam sales cycle data. Sếp vẫn complain."

---

## ✅ TEST 5: DATA ANALYST - ANH NAM (29, HCMC, KHÓ TÍNH NHẤT)

### Persona:
- **Pain Point**: "C-suite hỏi 'data này lấy từ đâu?' - cần source verification"
- **Goal**: Validate tất cả 4 domains có proper attribution
- **Success Criteria**: 100% KPIs phải có benchmark source

### Test Steps:

#### Step 1: Review All 4 Domain Tests
Run Tests 1-4 ở trên

#### Step 2: Data Quality Audit
For each domain, verify:

1. **Source Attribution**:
   - **CHECK**: Mỗi KPI có "📊 Benchmark Source" field? ✅/❌
   - **CHECK**: Sources credible (Michael Page, DataReportal, VECOM, HubSpot)? ✅/❌
   - **CHECK**: KHÔNG có "Unknown source" hay "Estimated"? ✅/❌

2. **Vietnam Context**:
   - **CHECK**: Mỗi KPI có "🇻🇳 Vietnam Context" message? ✅/❌
   - **CHECK**: Context sát thực tế (COD, mobile-first, relationship-based)? ✅/❌
   - **CHECK**: KHÔNG có generic global benchmarks? ✅/❌

3. **Percentile Ranking**:
   - **CHECK**: Main KPIs có "📈 Percentile" display? ✅/❌
   - **CHECK**: Percentile calculation hợp lý (25th-75th range)? ✅/❌

4. **Data Consistency**:
   - **CHECK**: Numbers make sense (no negative values, outliers)? ✅/❌
   - **CHECK**: Benchmarks realistic for Vietnam market? ✅/❌

#### Step 3: Coverage Audit

| Domain | CSV Data | Integration | Vietnam Context | Percentile | Source | Status |
|--------|----------|-------------|-----------------|------------|--------|--------|
| HR Salary | ✅ | ? | ? | ? | ? | ?/? |
| Marketing CPA | ✅ | ? | ? | ? | ? | ?/? |
| E-commerce | ✅ | ? | ? | ? | ? | ?/? |
| Sales | ✅ | ? | ? | ? | ? | ?/? |

Fill in the table based on testing results.

### Expected Result - Anh Nam's Reaction:
✅ **PASS (5/5 ⭐)**: "Perfect! C-suite presentation ready. Tất cả có sources verified!"

❌ **FAIL (3/5 ⭐)**: "Some domains missing Vietnam benchmarks. Cần complete integration."

---

## 📊 FINAL VALIDATION CHECKLIST

### Overall Score Calculation:

| Component | Weight | Score | Notes |
|-----------|--------|-------|-------|
| **HR Domain** | 25% | ?/10 | Salary benchmarks working? |
| **Marketing Domain** | 25% | ?/10 | CPA benchmarks working? |
| **E-commerce Domain** | 25% | ?/10 | Conversion/AOV benchmarks working? |
| **Sales Domain** | 25% | ?/10 | Win Rate/Cycle benchmarks working? |
| **TOTAL** | 100% | **?/10** | **Target: 10.0/10** |

### Pass Criteria:
- ✅ **10.0/10**: All 4 domains show Vietnam context + percentile + source
- ⚠️ **8.5/10**: 3/4 domains working, 1 missing
- ⚠️ **7.2/10**: 2/4 domains working (current before fix)
- ❌ **<7.0/10**: Major integration issues

---

## 🐛 COMMON ISSUES TO CHECK

### Issue 1: Vietnam Context Not Showing
**Symptom**: KPI hiển thị benchmark nhưng KHÔNG có "🇻🇳" message
**Root Cause**:
- Benchmark CSV files không load được
- Filter không match (e.g., role/city/channel not found)
**Fix**: Check browser console for errors

### Issue 2: Percentile Missing
**Symptom**: Có Vietnam context nhưng KHÔNG có "📈 Percentile"
**Root Cause**: Percentile calculation failed (missing Q1/Q3 data)
**Fix**: Review benchmark_loader.py logic

### Issue 3: Wrong Benchmark Source
**Symptom**: Source hiển thị "Calculated from Your Dataset" thay vì "Michael Page Vietnam"
**Root Cause**: Vietnam benchmark match failed, fallback to generic
**Fix**: Check if CSV file path correct in src/benchmark_loader.py

### Issue 4: App Crashes on Upload
**Symptom**: Error message after clicking "Phân Tích Dữ Liệu"
**Root Cause**:
- CSV format issue (encoding, delimiters)
- Missing required columns
**Fix**: Check file format matches expected schema

---

## 📝 TEST REPORT TEMPLATE

After completing all tests, fill out:

```
## PRODUCTION TEST REPORT - Vietnam Benchmarks Integration

**Test Date**: _________
**Tester**: _________
**Production URL**: https://fast-nicedashboard.streamlit.app/

### Test Results:

#### HR Domain (Chị Lan):
- Upload successful: ✅/❌
- KPIs displayed: ✅/❌
- Vietnam context shown: ✅/❌
- Percentile shown: ✅/❌
- Benchmark source shown: ✅/❌
- **Rating**: __/5 ⭐
- **Comments**: _________

#### Marketing Domain (Anh Minh):
- Upload successful: ✅/❌
- KPIs displayed: ✅/❌
- Vietnam context shown: ✅/❌
- Percentile shown: ✅/❌
- Benchmark source shown: ✅/❌
- **Rating**: __/5 ⭐
- **Comments**: _________

#### E-commerce Domain (Anh Tuấn):
- Upload successful: ✅/❌
- KPIs displayed: ✅/❌
- Vietnam context shown: ✅/❌
- Percentile shown: ✅/❌
- Benchmark source shown: ✅/❌
- **Rating**: __/5 ⭐
- **Comments**: _________

#### Sales Domain (Chị Hương):
- Upload successful: ✅/❌
- KPIs displayed: ✅/❌
- Vietnam context shown: ✅/❌
- Percentile shown: ✅/❌
- Benchmark source shown: ✅/❌
- **Rating**: __/5 ⭐
- **Comments**: _________

### Overall Assessment:

**Final Score**: __/10

**Production Ready**: ✅ YES / ❌ NO

**Critical Issues Found**:
1. _________
2. _________

**Recommendations**:
1. _________
2. _________

**Tester Signature**: _________
```

---

## 🎯 SUCCESS DEFINITION

**10.0/10 ACHIEVED** khi:
- ✅ Tất cả 4 domains show Vietnam benchmarks
- ✅ Mỗi KPI có 🇻🇳 context + 📈 percentile + 📊 source
- ✅ All 5 expert testers rate 5/5 ⭐
- ✅ Zero critical bugs
- ✅ Response time <60 seconds per analysis

**Ready to Ship** ✅

---

## 📎 Attachments

Test data files:
- `test_sample_hr_data.csv`
- `test_sample_marketing_data.csv`
- `test_sample_ecommerce_data.csv`
- `test_sample_sales_b2b_data.csv`

Test script:
- `test_production_integration.py` (for local validation)
