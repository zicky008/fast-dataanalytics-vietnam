# 🎯 PRODUCTION APP TESTING PLAN
## Role: Demanding Vietnamese Real Users across 5 Domains

**App URL:** https://8501-imbpbeetz4iocl2ra4swe-5634da27.sandbox.novita.ai  
**Test Date:** 2024-10-29  
**Tester:** AI as Real Vietnamese Users (demanding, detail-oriented)

---

## 👥 TEST PERSONAS (5 Real Vietnam User Types)

### 1. **Chị Mai - HR Manager (Vinamilk)**
**Profile:**
- 35 tuổi, 10 năm kinh nghiệm HR
- Công ty 500+ nhân viên
- Khó tính về data accuracy (salary, turnover rate)
- Cần benchmark với VietnamWorks data
- Quan tâm: Churn risk, salary competitiveness

**Expectations:**
- ✅ Salary data KHÔNG được fake (legal liability)
- ✅ Benchmark với VietnamWorks phải click được
- ✅ Insights phải có evidence cụ thể
- ✅ Tiếng Việt interface (ho_ten, luong_thang)
- ✅ Charts dễ đọc (CEO presentation)

---

### 2. **Anh Tuấn - E-commerce Owner (Shopee Seller)**
**Profile:**
- 28 tuổi, owner shop electronics trên Shopee
- Doanh thu 500M-1B VND/tháng
- Rất khó tính về order accuracy
- Cần phân tích COD vs Bank Transfer
- Quan tâm: Conversion rate, customer retention

**Expectations:**
- ✅ Order ID KHÔNG được impute (fraud risk)
- ✅ Province data phải chính xác (shipping cost)
- ✅ Payment method breakdown rõ ràng
- ✅ Benchmark với Shopee/Lazada data
- ✅ Product categories Tiếng Việt

---

### 3. **Chị Lan - Marketing Manager (FPT)**
**Profile:**
- 32 tuổi, lead digital marketing team
- Budget 100M-200M VND/tháng
- Cực kỳ khó tính về ROAS accuracy
- Cần so sánh với Google/Facebook benchmarks
- Quan tâm: CTR, CPC, conversion rate

**Expectations:**
- ✅ Campaign revenue KHÔNG được guess
- ✅ ROAS calculation phải đúng
- ✅ Benchmark Vietnam digital market (DataReportal)
- ✅ Channel performance comparison
- ✅ Insights có data evidence

---

### 4. **Anh Hùng - Sales Director (Viettel Enterprise)**
**Profile:**
- 40 tuổi, 15 năm kinh nghiệm B2B sales
- Deal size 500M-5B VND
- Không chấp nhận deal value bị fake
- Cần forecast accuracy cao
- Quan tâm: Win rate, pipeline value

**Expectations:**
- ✅ Deal value KHÔNG được impute
- ✅ Company names phải chính xác
- ✅ Benchmark với Salesforce/HubSpot
- ✅ Pipeline stage accuracy
- ✅ Next steps actionable

---

### 5. **Chị Ngọc - Customer Service Manager (Lazada VN)**
**Profile:**
- 30 tuổi, quản lý team CS 50 người
- Handle 500+ tickets/ngày
- Cần giảm resolution time
- Quan tâm: SLA, CSAT, FCR
- Khó tính về missing data

**Expectations:**
- ✅ Ticket ID KHÔNG được fake
- ✅ Resolution time phải accurate
- ✅ Customer name privacy (không show full)
- ✅ Issue categories Tiếng Việt
- ✅ CSAT score không được impute

---

## 🧪 TEST SCENARIOS (End-to-End for Each Persona)

### Scenario 1: Chị Mai (HR) - Test with vietnam_hr_data.csv

**Step 1: Upload File**
- [ ] Upload vietnam_hr_data.csv (50 employees)
- [ ] Check file upload success message
- [ ] Verify file size shown correctly

**Step 2: Data Quality Check**
- [ ] Quality score displayed (expect 85-95%)
- [ ] Missing data warning for 7 fields
- [ ] Check: luong_thang, position có missing → KHÔNG được impute
- [ ] Verify "calculated" benchmark source có URL GitHub

**Step 3: Domain Detection**
- [ ] Auto-detect as HR domain
- [ ] Show relevant KPIs: Average salary, Turnover risk
- [ ] Vietnamese labels: "Lương trung bình", "Nguy cơ nghỉ việc"

**Step 4: Dashboard**
- [ ] Salary distribution chart (by department)
- [ ] Experience vs Salary correlation
- [ ] Resignation risk breakdown
- [ ] Charts có labels Tiếng Việt

**Step 5: Insights**
- [ ] Check insight: "Technology department lương cao nhất"
- [ ] Verify data_evidence field có:
  - Column: luong_thang, department
  - Rows: specific employee IDs
  - Numbers: 32.5M vs 24M VND
- [ ] Click VietnamWorks benchmark URL → verify opens

**Step 6: Benchmark Verification**
- [ ] VietnamWorks URL: https://www.vietnamworks.com/salary-report
- [ ] Click → page loads với salary data
- [ ] Metrics preview matches: "IT: 15-25M VND/month"

**Expected Results:**
- ✅ NO salary data imputed (critical!)
- ✅ Insights have specific evidence
- ✅ Benchmark URLs work
- ✅ Vietnamese interface
- ✅ Charts professional quality

---

### Scenario 2: Anh Tuấn (E-commerce) - Test with vietnam_ecommerce_data.csv

**Step 1: Upload File**
- [ ] Upload vietnam_ecommerce_data.csv (29 orders)
- [ ] Check upload success
- [ ] File size ~3KB

**Step 2: Data Quality**
- [ ] Missing customer_id (2 records) → KHÔNG impute
- [ ] Missing discount (some records) → keep NULL
- [ ] Order_id integrity check

**Step 3: Domain Detection**
- [ ] Auto-detect as E-commerce
- [ ] KPIs: AOV, Conversion rate, Repeat purchase
- [ ] Vietnamese: "Giá trị đơn hàng", "Tỷ lệ chuyển đổi"

**Step 4: Dashboard**
- [ ] Revenue by province (HCM, Hanoi, Da Nang)
- [ ] Payment method breakdown (COD, Bank, E-wallet)
- [ ] Product category performance
- [ ] Order status funnel

**Step 5: Insights**
- [ ] "COD chiếm 40% orders" → verify data_evidence
- [ ] "HCM orders có AOV cao nhất" → specific numbers
- [ ] Province distribution accurate

**Step 6: Benchmark**
- [ ] iPrice Vietnam URL: https://iprice.vn/insights/mapofecommerce/
- [ ] Click → verify có Vietnam e-commerce data
- [ ] VECOM EBI 2024 PDF: https://esc.vn/wp-content/uploads/2025/07/Bao-cao-EBI-2024-ENG.pdf
- [ ] Click → PDF downloads

**Expected Results:**
- ✅ Order IDs not imputed
- ✅ Province names accurate
- ✅ Payment methods correct
- ✅ Benchmark URLs work
- ✅ Product names Tiếng Việt preserved

---

### Scenario 3: Chị Lan (Marketing) - Test with vietnam_marketing_campaign_data.csv

**Step 1: Upload**
- [ ] Upload vietnam_marketing_campaign_data.csv (20 campaigns)
- [ ] Success message

**Step 2: Data Quality**
- [ ] Missing budget (some campaigns) → KHÔNG impute
- [ ] Missing ROAS → keep NULL
- [ ] Campaign names Tiếng Việt preserved

**Step 3: Domain Detection**
- [ ] Auto-detect as Marketing
- [ ] KPIs: ROAS, CTR, CPC
- [ ] Labels: "Tỷ suất hoàn vốn", "Tỷ lệ click"

**Step 4: Dashboard**
- [ ] ROAS by channel (Facebook, TikTok, Zalo, Google)
- [ ] Budget vs Revenue scatter plot
- [ ] Campaign performance ranking
- [ ] Tết campaign highlighted (highest ROAS)

**Step 5: Insights**
- [ ] "TikTok Ads hiệu quả cho gen Z" → evidence
- [ ] "Zalo Ads phù hợp B2C Vietnam" → specific metrics
- [ ] Budget allocation recommendations

**Step 6: Benchmark**
- [ ] DataReportal Vietnam: https://datareportal.com/reports/digital-2024-vietnam
- [ ] Click → verify 76.9M users data
- [ ] VECOM EBI PDF → download works

**Expected Results:**
- ✅ Budget not imputed
- ✅ ROAS calculations accurate
- ✅ Channel names correct
- ✅ Vietnam benchmarks clickable
- ✅ Campaign names Tiếng Việt

---

### Scenario 4: Anh Hùng (Sales) - Test with vietnam_sales_pipeline_data.csv

**Step 1: Upload**
- [ ] Upload vietnam_sales_pipeline_data.csv (20 deals)
- [ ] Success

**Step 2: Data Quality**
- [ ] Missing deal_value → KHÔNG impute (legal!)
- [ ] Missing deal_name → keep NULL
- [ ] Company names intact (Vinamilk, FPT, Viettel)

**Step 3: Domain Detection**
- [ ] Auto-detect as Sales
- [ ] KPIs: Win rate, Pipeline value, Average deal size
- [ ] Labels Tiếng Việt

**Step 4: Dashboard**
- [ ] Pipeline by stage (Discovery, Proposal, Negotiation)
- [ ] Deal value by industry
- [ ] Days in stage analysis
- [ ] Top companies (Vinamilk, FPT visible)

**Step 5: Insights**
- [ ] "Banking sector highest deal value" → evidence
- [ ] "Negotiation stage 75% win rate" → specific numbers
- [ ] Next steps recommendations

**Step 6: Benchmark**
- [ ] HubSpot Sales: https://www.hubspot.com/sales/statistics
- [ ] Salesforce State of Sales working
- [ ] VECOM B2B PDF accessible

**Expected Results:**
- ✅ Deal values not imputed
- ✅ Company names accurate
- ✅ Pipeline stages correct
- ✅ Win rate calculations right
- ✅ Benchmarks work

---

### Scenario 5: Chị Ngọc (Customer Service) - Test with vietnam_customer_service_data.csv

**Step 1: Upload**
- [ ] Upload vietnam_customer_service_data.csv (20 tickets)
- [ ] Success

**Step 2: Data Quality**
- [ ] Missing satisfaction_score → KHÔNG impute
- [ ] Missing customer_id → keep NULL
- [ ] Ticket IDs intact

**Step 3: Domain Detection**
- [ ] Auto-detect as Customer Service
- [ ] KPIs: Resolution time, CSAT, FCR
- [ ] Labels: "Thời gian giải quyết", "Độ hài lòng"

**Step 4: Dashboard**
- [ ] Resolution time by issue category
- [ ] CSAT score distribution
- [ ] Channel performance (Phone, Email, Chat)
- [ ] Issue categories Tiếng Việt

**Step 5: Insights**
- [ ] "Delivery delay issues common" → evidence
- [ ] "Chat channel fastest resolution" → specific hours
- [ ] Recommendations to reduce time

**Step 6: Benchmark**
- [ ] Zendesk benchmarks accessible
- [ ] Industry standards visible

**Expected Results:**
- ✅ Ticket IDs not fake
- ✅ CSAT not imputed
- ✅ Customer privacy preserved
- ✅ Issue descriptions Tiếng Việt
- ✅ Resolution times accurate

---

## ✅ CRITICAL CHECKS (Apply to ALL Scenarios)

### Data Integrity
- [ ] NO critical fields imputed (revenue, salary, order_id, etc.)
- [ ] NULL values preserved where appropriate
- [ ] Vietnamese text not corrupted (dấu intact)
- [ ] Numbers formatted correctly (VND, percentages)

### Benchmark URLs
- [ ] ALL URLs clickable
- [ ] URLs lead to specific data (not homepage)
- [ ] DataReportal works: https://datareportal.com/reports/digital-2024-vietnam
- [ ] VECOM PDF works: https://esc.vn/wp-content/uploads/2025/07/Bao-cao-EBI-2024-ENG.pdf
- [ ] VietnamWorks works: https://www.vietnamworks.com/salary-report
- [ ] Anphabe works: https://www.anphabe.com/research/best-places-to-work

### Insights Quality
- [ ] Every insight has data_evidence field
- [ ] Evidence includes column names
- [ ] Evidence includes row references
- [ ] Evidence includes specific numbers
- [ ] Evidence shows calculations

### UX/UI Quality
- [ ] Interface loads < 3 seconds
- [ ] Charts render correctly
- [ ] No broken images
- [ ] Labels readable (not cut off)
- [ ] Colors professional (not garish)
- [ ] Vietnamese text displays correctly
- [ ] Mobile responsive (if applicable)

### Trust & Credibility
- [ ] Quality score visible
- [ ] Missing data warnings shown
- [ ] Benchmark sources credited
- [ ] Data sources disclosed
- [ ] Methodology transparent

---

## 📊 SCORING RUBRIC

### For Each Scenario (0-10 scale):

**Data Accuracy (3 points)**
- 3.0: Zero fake data, all preserved correctly
- 2.0: Minor imputation issues
- 1.0: Major imputation issues
- 0.0: Critical fake data

**Benchmark URLs (2 points)**
- 2.0: All URLs work perfectly
- 1.0: Some URLs broken
- 0.0: Most URLs broken

**Insights Quality (2 points)**
- 2.0: All insights have evidence
- 1.0: Some insights lack evidence
- 0.0: No evidence provided

**UX/UI (2 points)**
- 2.0: Professional, 5-star experience
- 1.0: Acceptable but issues
- 0.0: Poor UX

**Trust/Credibility (1 point)**
- 1.0: High trust, transparent
- 0.5: Moderate trust
- 0.0: Low trust

### Overall Score
- **9.5-10.0:** ⭐⭐⭐⭐⭐ OUTSTANDING - Production ready
- **9.0-9.4:** ⭐⭐⭐⭐⭐ EXCELLENT - Minor polish
- **8.0-8.9:** ⭐⭐⭐⭐ GOOD - Some improvements
- **7.0-7.9:** ⭐⭐⭐ ACCEPTABLE - Significant work needed
- **<7.0:** ⭐⭐ NEEDS WORK - Not ready

---

## 🎯 SUCCESS CRITERIA

**For 5-Star "Happy Customer" Validation:**

✅ **ALL 5 personas satisfied** (each scores 9.0+/10)  
✅ **Zero critical data imputation** (revenue, salary, IDs preserved)  
✅ **All benchmark URLs work** (100% clickable)  
✅ **All insights have evidence** (column, row, numbers)  
✅ **Vietnamese text perfect** (no corruption)  
✅ **Professional UX** (charts, labels, colors)  
✅ **Fast loading** (<5 seconds)  
✅ **Transparent methodology** (quality score, warnings)

**If ANY criteria fails → NOT 5-star ready**

---

**Next Step:** Execute tests for all 5 scenarios on production app and document results.
