# Deployment Verification Checklist

## 🎯 App URL
**Production**: https://fast-dataanalytics.streamlit.app/

---

## ✅ Deployment Verification (Task #16)

### **1. Basic Functionality**
- [ ] **Page loads successfully** (no 500 errors)
- [ ] **UI renders correctly** (title, header, upload section visible)
- [ ] **No JavaScript errors** in browser console (F12)
- [ ] **Gemini API key configured** (check Streamlit Cloud secrets)

### **2. File Upload**
- [ ] **CSV upload works** (try `sample_data/marketing_google_ads.csv`)
- [ ] **Excel upload works** (if you have .xlsx files)
- [ ] **File validation works** (correct error messages for invalid files)
- [ ] **Encoding detection works** (UTF-8, Latin-1, etc.)

### **3. Pipeline Execution**
- [ ] **Step 0: Domain Detection** completes
  - Domain name displayed correctly (e.g., "Marketing / Quảng Cáo")
  - Confidence % shown
  - Expert role displayed
  
- [ ] **Step 1: Data Cleaning** completes
  - Quality score displayed (should be 90-100/100)
  - Cleaning summary shown
  - No errors about missing data

- [ ] **Step 2: Smart Blueprint** completes
  - KPIs calculated (ROAS, CTR, etc. for Marketing)
  - 8-9 charts planned
  - Blueprint quality score shown

- [ ] **Step 3: Dashboard Build** completes
  - 8-9 charts render correctly
  - All charts have titles, axes labels
  - No "undefined" or error messages

- [ ] **Step 4: Domain Insights** completes
  - Executive summary in Vietnamese
  - 3-5 recommendations shown
  - Risk alerts (if any)

### **4. Performance**
- [ ] **Total pipeline time < 60s** (target: 13-23s based on local tests)
- [ ] **No timeout errors**
- [ ] **Progress indicators work** (Steps 0/4, 1/4, etc.)
- [ ] **UI remains responsive** during processing

### **5. Visual Quality**
- [ ] **Charts are interactive** (hover shows data points)
- [ ] **Colors are professional** (not default ugly colors)
- [ ] **Text is readable** (Vietnamese characters display correctly)
- [ ] **Layout is clean** (no overlapping elements)
- [ ] **Mobile responsive** (check on phone if possible)

### **6. Error Handling**
- [ ] **Rate limit handled gracefully** (if you hit 15 req/min limit)
- [ ] **Invalid data handled** (upload a broken CSV, should show clear error)
- [ ] **API errors handled** (what happens if Gemini API is down?)
- [ ] **User-friendly error messages** (in Vietnamese)

### **7. Data Privacy**
- [ ] **No data stored permanently** (refresh page = data gone)
- [ ] **No PII sent to logs** (check Streamlit Cloud logs)
- [ ] **API key not exposed** (check page source, should not see key)

---

## 🧪 **Test Scenarios**

### **Test 1: Marketing Data (Google Ads)**
```
File: sample_data/marketing_google_ads.csv
Expected Domain: Marketing / Quảng Cáo
Expected KPIs: ROAS, CTR, CPC, CPA, Conversion Rate
Expected Charts: 8-9 (bar, line charts)
Expected Time: 13-15s
```

**Steps**:
1. Upload `marketing_google_ads.csv`
2. Add description: "Google Ads campaign data - January 2024"
3. Click "Phân Tích Dữ Liệu"
4. Wait for pipeline to complete
5. Verify all 4 steps complete successfully
6. Check quality score = 100/100
7. Review charts and insights

**Expected Result**: ✅ All steps pass, quality 100/100, 8-9 charts, Vietnamese insights

---

### **Test 2: E-commerce Data (Shopify)**
```
File: sample_data/ecommerce_shopify.csv
Expected Domain: E-commerce / Bán Hàng Trực Tuyến
Expected KPIs: AOV, CLV, Conversion Rate, Cart Abandonment
Expected Charts: 8-9 charts
Expected Time: 20-25s
```

**Steps**:
1. Upload `ecommerce_shopify.csv`
2. Add description: "Shopify e-commerce orders - January 2024"
3. Click "Phân Tích Dữ Liệu"
4. Wait for pipeline to complete
5. Verify all 4 steps complete successfully
6. Check quality score = 100/100
7. Review AOV and CLV calculations

**Expected Result**: ✅ All steps pass, quality 100/100, 8 charts, E-commerce insights

---

### **Test 3: Error Handling**
```
File: Create a CSV with invalid data (missing columns, bad encoding, etc.)
Expected: Clear error message, no crash
```

**Steps**:
1. Create a CSV with only 2 columns (not enough for analysis)
2. Upload to app
3. Try to analyze
4. Check error message

**Expected Result**: ✅ Clear error message in Vietnamese, app doesn't crash

---

### **Test 4: Rate Limiting**
```
Goal: Test if app handles Gemini API rate limits (15 req/min)
```

**Steps**:
1. Upload and analyze 5 datasets rapidly (within 1 minute)
2. Watch for rate limit errors
3. Check if app retries automatically

**Expected Result**: ✅ App retries with exponential backoff (2s, 4s, 8s delays)

---

## 🐛 **Common Issues & Solutions**

### **Issue 1: App Shows "Error: Invalid API Key"**

**Symptom**: Pipeline fails at Step 1 with API key error

**Solution**:
1. Go to Streamlit Cloud dashboard
2. Click your app → Settings → Secrets
3. Verify `GEMINI_API_KEY` is set correctly
4. Format should be:
   ```toml
   GEMINI_API_KEY = "AIzaSyBue04J1-g35_OVtBshhE9Bieym7IAEx64"
   ```
5. Save and wait for app to restart (1-2 minutes)

---

### **Issue 2: App Loads Very Slowly (>30s)**

**Symptom**: White screen for 30+ seconds before UI appears

**Cause**: Cold start (Streamlit Cloud spins down idle apps)

**Expected Behavior**: 
- First load after idle: 10-30s (cold start)
- Subsequent loads: <5s (warm)

**Solution**: No action needed, this is normal for free tier

---

### **Issue 3: Charts Not Rendering**

**Symptom**: Dashboard shows "Loading..." but charts never appear

**Possible Causes**:
1. NumPy metadata issue (should be fixed in deployment)
2. Plotly import error
3. Data format issue

**Solution**:
1. Check Streamlit Cloud logs (Manage app → Logs)
2. Look for errors mentioning "plotly" or "numpy"
3. If NumPy error: Check that `requirements.txt` has `numpy>=1.24.0` (not `--no-deps`)

---

### **Issue 4: Vietnamese Text Shows as "??????"**

**Symptom**: Vietnamese characters display as question marks

**Cause**: UTF-8 encoding issue

**Solution**:
1. Ensure CSV file is saved as UTF-8 (not ANSI or Windows-1252)
2. App should auto-detect encoding using `chardet`
3. If issue persists, check browser character encoding settings

---

### **Issue 5: Pipeline Timeout (>60s)**

**Symptom**: Pipeline fails with "Execution time exceeded"

**Cause**: 
1. Very large dataset (>10,000 rows)
2. Gemini API slow response
3. Rate limiting delays

**Solution**:
1. Reduce dataset size (sample first 1000-5000 rows)
2. Wait a few minutes (rate limit cooldown)
3. Check Gemini API status: https://status.cloud.google.com/

---

## 📊 **Performance Benchmarks (Expected)**

Based on local testing, here are expected performance metrics:

| Metric | Expected Value | Acceptable Range |
|--------|----------------|------------------|
| **Total Pipeline Time** | 13-23s | <60s |
| **Domain Detection** | 0.5s | <3s |
| **Data Cleaning** | 1-8s | <15s |
| **Smart Blueprint** | 7-9s | <20s |
| **Dashboard Build** | 0.2-0.4s | <10s |
| **Domain Insights** | 4-6s | <20s |
| **Quality Score** | 100/100 | ≥80/100 |
| **Charts Generated** | 8-9 | ≥5 |
| **Success Rate** | 100% | ≥95% |

**Note**: Cloud performance may vary from local tests due to:
- Cold start delays (first load)
- Network latency
- Gemini API response time variations
- Streamlit Cloud resource allocation

---

## ✅ **Verification Complete**

When all checkboxes above are checked, mark Task #16 as **COMPLETED** and proceed to **Task #17: User Acceptance Testing**.

---

## 📝 **Deployment Info**

**App URL**: https://fast-dataanalytics.streamlit.app/  
**Repository**: YOUR_GITHUB_USERNAME/dataanalytics-vietnam  
**Branch**: main  
**Main File**: src/app.py  
**Python Version**: 3.11  
**Dependencies**: See requirements.txt  
**Secrets**: GEMINI_API_KEY (configured in Streamlit Cloud)

---

**Last Updated**: 2025-10-21  
**Version**: 1.0.0  
**Status**: 🚀 DEPLOYED
