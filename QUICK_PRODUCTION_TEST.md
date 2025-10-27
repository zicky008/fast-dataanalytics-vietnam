# 🚀 QUICK PRODUCTION TEST - 5 Minutes

## THE TWO CRITICAL TESTS ⭐⭐⭐⭐⭐

**Goal**: Verify Vietnamese fonts + Charts in PDF export

---

## ⚡ SUPER QUICK TEST (5 minutes)

### Step 1: Prepare (30 seconds)
1. Download file: `sample_data/test_vietnamese_restaurant.csv`
2. Open browser: https://fast-nicedashboard.streamlit.app/

### Step 2: Upload & Analyze (2 minutes)
1. Click "Browse files"
2. Select `test_vietnamese_restaurant.csv`
3. Click "Analyze" or "Phân tích"
4. Wait ~60 seconds

✅ **CHECK**: Vietnamese text shows correctly (not □□□)

### Step 3: Export PDF (2 minutes)
1. Find "Export to PDF" button
2. Click it
3. Wait ~60 seconds
4. Download PDF

### Step 4: Verify PDF (30 seconds)
Open PDF and check:

**CRITICAL CHECK #1: Vietnamese Fonts**
Look for: "BÁO CÁO PHÂN TÍCH DỮ LIỆU"
- ✅ PASS: Shows correctly → ⭐⭐⭐⭐⭐
- ❌ FAIL: Shows □□□ → Report bug

**CRITICAL CHECK #2: Charts**
Scroll PDF, count charts:
- ✅ PASS: 3+ charts visible → ⭐⭐⭐⭐⭐
- ⚠️ PARTIAL: 1-2 charts → ⭐⭐⭐⭐
- ❌ FAIL: No charts → Report bug

---

## 📊 INSTANT REPORT

**Vietnamese Fonts**: [ ] ✅ Perfect / [ ] ❌ Broken
**Charts in PDF**: [ ] ✅ Yes (___ charts) / [ ] ❌ No

**Overall Rating**: ⭐⭐⭐⭐⭐ / ⭐⭐⭐⭐ / ⭐⭐⭐ / ⭐⭐ / ⭐

**Screenshot PDF Page 1**: (attach here)
**Screenshot PDF Charts**: (attach here)

---

## 🎯 Decision

- **5⭐ or 4⭐** → ✅ SUCCESS! Ready for users
- **3⭐ or below** → ⚠️ Issues found, see PRODUCTION_TEST_PLAN.md for details

---

**Time needed**: 5 minutes
**Test file**: `sample_data/test_vietnamese_restaurant.csv`
**Production URL**: https://fast-nicedashboard.streamlit.app/
