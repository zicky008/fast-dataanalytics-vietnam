# ✅ MANUAL TESTING CHECKLIST - Production App

**App URL**: https://fast-nicedashboard.streamlit.app/  
**Date**: 2025-10-31  
**Status**: ⏳ PENDING USER TESTING  
**Time Required**: 30 minutes

---

## 🎯 PURPOSE

Verify production app works correctly before user interviews.  
Fix any critical issues that could waste users' time.

**Remember**: "TRÁCH NHIỆM" (Responsibility) - Test before showing to real users!

---

## 📋 TEST 1: DESKTOP BASIC FUNCTIONALITY (10 min)

### 1.1 App Loading
- [ ] Open: https://fast-nicedashboard.streamlit.app/
- [ ] Page loads without errors (<30s acceptable for cold start)
- [ ] Title visible: "DataAnalytics Vietnam - AI-Powered Business Intelligence"
- [ ] Sidebar visible with language options

**Expected**: ✅ Clean load, no red error messages

---

### 1.2 Sample Data Upload (E-commerce)
- [ ] Click "📊 Tải file mẫu: E-commerce"
- [ ] Preview table appears (50 rows, 19 columns)
- [ ] Data shows: date, channel, revenue, transactions, etc.
- [ ] No missing data in preview

**Expected**: ✅ Data loads in <5 seconds

---

### 1.3 Analysis Execution
- [ ] Click "🚀 Phân tích dữ liệu" button
- [ ] Loading spinner appears
- [ ] Analysis completes (<55s target, expect 15-25s)
- [ ] Dashboard appears with charts + KPIs

**Expected**: ✅ Analysis completes successfully, no errors

---

### 1.4 Dashboard Content Verification
- [ ] Top 3 KPIs visible (Revenue, Conversion Rate, AOV or similar)
- [ ] Font sizes appropriate (primary KPIs larger)
- [ ] At least 2 charts rendered (trend, breakdown, etc.)
- [ ] Vietnamese text displays correctly (no ???)
- [ ] No red error messages

**Expected**: ✅ Professional dashboard with clear hierarchy

---

### 1.5 Progressive Disclosure (if implemented)
- [ ] Check for "Xem thêm" or expand button
- [ ] If present: Click to expand additional KPIs
- [ ] Additional content appears smoothly
- [ ] Can collapse back

**Expected**: ⚠️ May not be fully visible yet, note observations

---

## 📋 TEST 2: MOBILE RESPONSIVENESS (5 min)

### 2.1 Mobile Viewport Test
- [ ] Press F12 (DevTools)
- [ ] Click "Toggle device toolbar" (Ctrl+Shift+M)
- [ ] Select: iPhone SE (375x667)

---

### 2.2 Mobile Layout Check
- [ ] KPIs stack vertically (not horizontal overflow)
- [ ] Text readable without zooming
- [ ] Buttons tap-able (target size adequate)
- [ ] Charts display (may be simplified)
- [ ] No horizontal scrolling required

**Expected**: ✅ Layout adapts to mobile, usable on small screen

---

### 2.3 Mobile Interaction
- [ ] Try scrolling up/down
- [ ] Try tapping "Phân tích" button
- [ ] Try uploading sample data
- [ ] All interactions work on touch

**Expected**: ✅ Touch-friendly, no broken interactions

---

## 📋 TEST 3: BROWSER CONSOLE CHECK (5 min)

### 3.1 Open DevTools Console
- [ ] Press F12
- [ ] Go to "Console" tab
- [ ] Look for red errors

---

### 3.2 Error Classification
**Critical Errors** (red, breaks functionality):
- [ ] List any critical errors here: _______________

**Warnings** (yellow, cosmetic):
- [ ] Count warnings: _____ (acceptable if <20)

**Expected**: ✅ No critical errors, warnings acceptable

---

## 📋 TEST 4: PERFORMANCE BENCHMARKING (5 min)

### 4.1 Cold Start (First Load)
- [ ] Clear browser cache (Ctrl+Shift+Delete)
- [ ] Reload page
- [ ] Time from click to fully loaded: _____ seconds

**Target**: <30s acceptable for cold start  
**Expected**: 10-20s typical for Streamlit Cloud

---

### 4.2 Analysis Time
- [ ] Upload e-commerce sample data
- [ ] Start timer when clicking "Phân tích"
- [ ] Stop when dashboard appears
- [ ] Time: _____ seconds

**Target**: <55s (expected: 15-25s)  
**Expected**: ✅ Under target

---

### 4.3 Subsequent Loads (Cached)
- [ ] Reload page (F5)
- [ ] Time: _____ seconds

**Expected**: <10s with cache

---

## 📋 TEST 5: DATA QUALITY VALIDATION (5 min)

### 5.1 Verify Sample Data
- [ ] Check e-commerce sample: revenue numbers make sense?
- [ ] Check dates: all in August 2024?
- [ ] Check channels: Organic, Facebook, Google, Direct, Email?
- [ ] No null/missing values in key columns?

**Expected**: ✅ Data looks realistic and complete

---

### 5.2 KPI Calculations Spot Check
Pick 1-2 KPIs and manually verify:

**Revenue**:
- [ ] Dashboard shows: ₫___________
- [ ] Matches sum in preview table?

**Conversion Rate**:
- [ ] Dashboard shows: _____%
- [ ] Formula: transactions / sessions * 100
- [ ] Calculation correct?

**Expected**: ✅ Calculations accurate (100% requirement)

---

## 📋 TEST 6: MICROSOFT CLARITY VERIFICATION (Post-Test)

### 6.1 Immediate Check
- [ ] View page source (Ctrl+U)
- [ ] Search for "clarity.ms"
- [ ] Clarity script found?
- [ ] Project ID present: tybfgieemx

**Expected**: ✅ Script injected in HTML

---

### 6.2 Dashboard Check (After 2-4 Hours)
- [ ] Visit: https://clarity.microsoft.com/projects/view/tybfgieemx/dashboard
- [ ] Sign in if needed
- [ ] Check for today's sessions
- [ ] Session recordings visible?
- [ ] Heatmaps generated?

**Expected**: ⏳ Data appears after 2-4 hour processing delay

---

## 📊 TEST RESULTS SUMMARY

### ✅ PASSED TESTS (Check all that apply)
- [ ] App loads successfully
- [ ] Sample data uploads correctly
- [ ] Analysis completes without errors
- [ ] Dashboard renders with charts + KPIs
- [ ] Mobile responsive (no horizontal scroll)
- [ ] No critical errors in console
- [ ] Performance within targets
- [ ] Data quality accurate
- [ ] Microsoft Clarity script present

### ❌ FAILED TESTS (Note issues)
1. __________________________________________________
2. __________________________________________________
3. __________________________________________________

### ⚠️ OBSERVATIONS (Non-critical notes)
1. __________________________________________________
2. __________________________________________________
3. __________________________________________________

---

## 🚦 GO/NO-GO DECISION

**PASS CRITERIA**: 8/9 tests passed, no critical errors

**Result**: 
- [ ] ✅ **PASS** - Ready for user interviews
- [ ] ⚠️ **CONDITIONAL PASS** - Minor issues, document for future fix
- [ ] ❌ **FAIL** - Critical issues, must fix before user testing

---

## 📝 NEXT ACTIONS

### If PASS ✅:
1. Proceed to user recruitment
2. Schedule 3 interviews (1 per domain)
3. Use USER_INTERVIEW_SCRIPT_VI.md
4. Follow DEPLOYMENT_CHECKLIST_PHASE1.md

### If CONDITIONAL PASS ⚠️:
1. Document issues in GitHub Issues
2. Assess impact on user testing
3. Proceed with user interviews (inform users of known issues)
4. Fix after Phase 1 if time permits

### If FAIL ❌:
1. Identify critical blockers
2. Fix immediately before proceeding
3. Re-test all failed items
4. Only proceed when all critical issues resolved

---

## 🔍 COMMON ISSUES & QUICK FIXES

### Issue 1: "App stuck on Loading..."
**Cause**: Cold start or server timeout  
**Fix**: Wait 2-3 minutes, refresh page  
**Prevention**: Streamlit Cloud free tier has cold starts

### Issue 2: "Analysis fails with error"
**Cause**: Gemini API key issue or quota  
**Fix**: Check Streamlit Cloud → Settings → Secrets  
**Verify**: GEMINI_API_KEY is set correctly

### Issue 3: "Charts not rendering"
**Cause**: Plotly library or data issue  
**Fix**: Check browser console for specific error  
**Workaround**: Try different browser (Chrome recommended)

### Issue 4: "Mobile layout broken"
**Cause**: CSS conflict or Streamlit update  
**Fix**: Check CSS in streamlit_app.py line ~75-150  
**Workaround**: Advise users to use desktop for now

### Issue 5: "Microsoft Clarity not tracking"
**Cause**: Script blocked by ad-blocker or not yet processed  
**Fix**: Disable ad-blocker, wait 2-4 hours  
**Verify**: Check page source for script presence

---

## ✅ SIGN-OFF

**Tested by**: ____________________  
**Date**: ____________________  
**Result**: ✅ PASS / ⚠️ CONDITIONAL / ❌ FAIL  
**Comments**: ____________________

**Ready for User Testing**: [ ] YES / [ ] NO

---

**Next Document**: `USER_INTERVIEW_SCRIPT_VI.md` (if PASS)  
**Escalation**: Create GitHub Issue if critical failures found

**Remember**: Happy Customers → Trust → Revenue 🇻🇳
