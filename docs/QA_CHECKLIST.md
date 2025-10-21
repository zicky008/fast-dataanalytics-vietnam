# 🧪 Quality Assurance Checklist - DataAnalytics Vietnam

> 5-Star Quality Standards - Expert Tester + DA + Người dùng khó tính nhất

## 📋 Pre-Development QA

### ✅ Code Audit
- [ ] Review existing codebase for bugs
- [ ] Check dependencies security (pyproject.toml)
- [ ] Validate Python version compatibility (>=3.11)
- [ ] Code style consistency (PEP 8)
- [ ] Performance bottlenecks identification

### ✅ Architecture Review
- [ ] Session state management correctness
- [ ] Gemini API usage optimization
- [ ] Memory leak prevention
- [ ] Scalability considerations

---

## 🚀 Quick Dashboard Mode - QA Checklist

### Functional Testing

#### ✅ File Upload
- [ ] **CSV upload**: UTF-8, UTF-8-BOM, ISO-8859-1
- [ ] **Excel upload**: .xlsx, .xls
- [ ] **File size limits**: 1KB to 200MB
- [ ] **Edge cases**: 
  - Empty file
  - Single row
  - Single column
  - 10,000+ rows
  - Special characters in column names (spaces, Vietnamese, emojis)
  - Malformed CSV (missing commas, inconsistent columns)

#### ✅ Column Detection
- [ ] **Categorical**: Text, low cardinality (<20 unique)
- [ ] **Numerical**: Integer, float, currency
- [ ] **Date/Time**: Multiple formats (dd/mm/yyyy, yyyy-mm-dd, timestamps)
- [ ] **Mixed types**: Handle gracefully (e.g., "100" as text vs 100 as number)
- [ ] **Missing values**: NaN, NULL, empty strings, "-"

#### ✅ Chart Generation
- [ ] **Auto-select 4-6 charts**: Appropriate chart types for data
- [ ] **Chart types**:
  - Bar chart (categorical vs numerical)
  - Line chart (time series)
  - Scatter plot (numerical vs numerical)
  - Heatmap (correlations)
  - Pie chart (categorical distribution)
  - Histogram (numerical distribution)
- [ ] **Chart quality**:
  - Axes labels in Vietnamese
  - Legends clear
  - Colors accessible (colorblind-friendly)
  - Tooltips informative
  - No overlapping text

#### ✅ Performance
- [ ] **Generation speed**: <30s for 95% of files
- [ ] **Show progress**: Loading bar, status messages
- [ ] **Timeout handling**: Graceful failure after 60s
- [ ] **Memory management**: No crashes on large files

#### ✅ Error Handling
- [ ] **Invalid file format**: Clear error message
- [ ] **Corrupted file**: Handled gracefully
- [ ] **API failure**: Retry logic + fallback
- [ ] **Network issues**: Offline mode or error notification
- [ ] **User guidance**: "What went wrong" + "How to fix"

---

## 🤖 Natural Language Editing - QA Checklist

### Functional Testing

#### ✅ Intent Recognition
- [ ] **Add chart**: "Thêm biểu đồ cột", "Add bar chart"
- [ ] **Remove chart**: "Xóa chart 1", "Delete correlation heatmap"
- [ ] **Modify chart**: "Đổi màu chart 2 sang xanh", "Change title to 'Sales Report'"
- [ ] **Filter data**: "Chỉ hiện Region = HCM", "Show only Fashion segment"
- [ ] **Rearrange**: "Đổi vị trí chart 1 và 2"

#### ✅ Vietnamese Language Support
- [ ] **Diacritics**: ă, â, đ, ê, ô, ơ, ư (đầy đủ)
- [ ] **Common phrases**: "so sánh", "phân tích", "xu hướng"
- [ ] **Business terms**: doanh thu, chi phí, lợi nhuận, ROI
- [ ] **Mixed Vietnamese-English**: "Add biểu đồ", "Chart doanh thu"

#### ✅ Edge Cases
- [ ] **Vague prompt**: "Làm cái gì đó cho đẹp hơn"
- [ ] **Ambiguous**: "Chart mới" (which chart?)
- [ ] **Conflicting**: "Xóa tất cả chart" (confirm first)
- [ ] **Typos**: "Thêm bíu đồ cột" (fuzzy match)
- [ ] **Long prompt**: 200+ words (truncate or summarize)

#### ✅ Response Quality
- [ ] **Execution**: Action performed correctly
- [ ] **Feedback**: "Đã thêm biểu đồ cột so sánh doanh thu theo Region"
- [ ] **Undo**: Ability to revert changes
- [ ] **Suggestions**: If unclear, ask clarifying question

---

## 🎨 UI/UX Testing

### ✅ Visual Design
- [ ] **Typography**: Readable fonts (16px minimum)
- [ ] **Colors**: High contrast (WCAG AA compliant)
- [ ] **Layout**: No element overlap, proper spacing
- [ ] **Responsive**: Desktop (1920x1080 to 1366x768), Tablet, Mobile
- [ ] **Loading states**: Spinners, progress bars, skeleton screens

### ✅ User Flow
- [ ] **Onboarding**: First-time user sees guide
- [ ] **Tooltips**: Every button has helpful tooltip
- [ ] **Empty states**: Clear instructions when no data
- [ ] **Success states**: Confetti 🎉 after dashboard creation
- [ ] **Error states**: Friendly messages, no jargon

### ✅ Accessibility
- [ ] **Keyboard navigation**: Tab, Enter, Escape work
- [ ] **Screen reader**: Alt text on images, ARIA labels
- [ ] **Color contrast**: 4.5:1 ratio minimum
- [ ] **Focus indicators**: Visible outline on focused elements

---

## 📊 Data Validation Testing

### ✅ Input Validation
- [ ] **File types**: Reject .exe, .sh, .zip
- [ ] **File size**: 200MB hard limit, warning at 100MB
- [ ] **Column names**: Max 100 characters, no special SQL chars
- [ ] **Data types**: Validate before processing
- [ ] **Missing data**: Handle >50% missing gracefully

### ✅ Output Validation
- [ ] **Charts**: No empty charts, no NaN in axes
- [ ] **Insights**: Always actionable, never generic
- [ ] **Exports**: PDF/PPT renders correctly
- [ ] **Templates**: Save/load without data loss

---

## ⚡ Performance Testing

### ✅ Load Testing
- [ ] **1 user**: <2s response time
- [ ] **10 concurrent users**: <5s response time
- [ ] **50 concurrent users**: <10s response time (Streamlit Cloud limit)

### ✅ Stress Testing
- [ ] **Large files**: 200MB CSV (500k rows)
- [ ] **Complex dashboards**: 20+ charts
- [ ] **Rapid actions**: 10 NL edits in 30s
- [ ] **Memory leaks**: No crashes after 1 hour usage

### ✅ API Rate Limits
- [ ] **Gemini Free tier**: 15 requests/min
- [ ] **Retry logic**: Exponential backoff
- [ ] **Caching**: Avoid duplicate API calls
- [ ] **Fallback**: Manual mode if API fails

---

## 🔒 Security Testing

### ✅ Data Privacy
- [ ] **API keys**: Never exposed in frontend
- [ ] **User data**: Not stored permanently
- [ ] **Session data**: Cleared after 24 hours
- [ ] **Exports**: No sensitive data in filenames

### ✅ Input Sanitization
- [ ] **SQL injection**: N/A (no SQL database)
- [ ] **XSS**: Streamlit auto-escapes HTML
- [ ] **File upload**: Scan for malware (future)
- [ ] **API abuse**: Rate limiting per session

---

## 📱 Cross-Browser Testing

### ✅ Desktop Browsers
- [ ] **Chrome** (v120+): Full functionality
- [ ] **Firefox** (v120+): Full functionality
- [ ] **Safari** (v17+): Full functionality
- [ ] **Edge** (v120+): Full functionality

### ✅ Mobile Browsers
- [ ] **Chrome Mobile**: Basic functionality (view-only)
- [ ] **Safari iOS**: Basic functionality
- [ ] **Responsive**: Tables scroll horizontally

---

## 🧪 Integration Testing

### ✅ End-to-End Flows
1. **Happy Path**:
   - Upload CSV → Quick Mode → Generate → NL Edit → Export PDF
   - Expected: Success in <2 minutes

2. **OQMLB Expert Path**:
   - Upload → Step 1-5 → Generate Blueprint → Build Dashboard
   - Expected: Success in 5-10 minutes

3. **Template Reuse**:
   - Create dashboard → Save template → Upload new data → Apply template
   - Expected: Dashboard regenerated with new data

### ✅ Error Recovery
- [ ] **API timeout**: Retry 3x, then fallback
- [ ] **Invalid data**: Show error + guide user
- [ ] **Session expired**: Auto-save draft + restore

---

## ✅ User Acceptance Testing (UAT)

### Test Datasets (5 Real Scenarios)
1. **Marketing Campaign Data** (sample_marketing_data.csv)
   - 20 rows, 13 columns
   - Expected: Bar charts, line trends, insights about ROI

2. **Sales Report** (mock data)
   - 500 rows, 8 columns
   - Expected: Time series, regional comparison, top products

3. **Finance P&L** (mock data)
   - 100 rows, 15 columns
   - Expected: Waterfall chart, category breakdown, YoY comparison

4. **HR Analytics** (mock data)
   - 200 rows, 10 columns
   - Expected: Demographics, attrition analysis, salary distribution

5. **E-commerce Orders** (mock data)
   - 1000 rows, 12 columns
   - Expected: Funnel analysis, customer segments, order trends

### Success Criteria
- [ ] **80% users** create successful dashboard on first try
- [ ] **<5 clicks** to generate dashboard (Quick Mode)
- [ ] **<3 minutes** total time (upload to export)
- [ ] **4.5+ rating** on ease of use (1-5 scale)
- [ ] **0 critical bugs** in production

---

## 📊 Performance Benchmarks

| Metric | Target | Acceptable | Unacceptable |
|--------|--------|------------|--------------|
| **Dashboard generation** | <30s | <60s | >60s |
| **NL edit response** | <3s | <5s | >10s |
| **File upload** | <5s | <10s | >15s |
| **API calls/session** | <20 | <50 | >100 |
| **Memory usage** | <500MB | <1GB | >2GB |
| **Error rate** | <0.1% | <1% | >5% |

---

## 🎯 Final QA Sign-Off

Before deployment, ALL items must be ✅:

- [ ] **Code Review**: Peer reviewed by 1+ developer
- [ ] **Security Audit**: No critical vulnerabilities
- [ ] **Performance Tests**: All benchmarks met
- [ ] **UAT**: 5/5 test datasets successful
- [ ] **Documentation**: README + User Guide complete
- [ ] **Deployment**: Streamlit Cloud tested
- [ ] **Monitoring**: Error tracking setup (Sentry/LogRocket)
- [ ] **Rollback Plan**: Can revert to previous version in <5 min

---

## 📝 Test Execution Log

| Test Category | Pass Rate | Critical Issues | Status |
|--------------|-----------|-----------------|--------|
| Functional Testing | _/_ | _ | ⏳ |
| UI/UX Testing | _/_ | _ | ⏳ |
| Performance Testing | _/_ | _ | ⏳ |
| Security Testing | _/_ | _ | ⏳ |
| Integration Testing | _/_ | _ | ⏳ |
| UAT | _/_ | _ | ⏳ |

**QA Tester**: [Your Name]
**Date**: [Test Date]
**Version**: v1.0.0-mvp

---

**Sign-Off**: ✅ APPROVED for Production | ⚠️ NEEDS FIXES | ❌ REJECTED
