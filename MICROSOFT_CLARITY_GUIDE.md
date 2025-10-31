# 📊 Microsoft Clarity - Hướng Dẫn Sử Dụng

> **Mục đích**: Theo dõi hành vi người dùng thực để cải thiện UX lên 5 sao  
> **Chi phí**: ₫0 mãi mãi (unlimited sessions)  
> **Project ID**: `tybfgieemx`  
> **Dashboard**: https://clarity.microsoft.com/projects/view/tybfgieemx

---

## ✅ TÍCH HỢP HOÀN TẤT

### Tracking Code Đã Được Thêm Vào
- **File**: `streamlit_app.py` (dòng 151-166)
- **Vị trí**: Ngay sau viewport fix, trước WCAG fixes
- **Status**: ✅ ACTIVE
- **Performance Impact**: ~50ms (negligible)

### Dữ Liệu Được Thu Thập
1. **Session Recordings** (Video ghi lại cách người dùng thao tác)
   - Mouse movements
   - Clicks and taps
   - Scrolling behavior
   - Form interactions
   - Page navigation

2. **Heatmaps** (Bản đồ nhiệt - nơi người dùng click nhiều nhất)
   - Click heatmaps
   - Scroll heatmaps
   - Area of interest

3. **Analytics** (Phân tích định lượng)
   - Pages per session
   - Session duration
   - Bounce rate
   - Rage clicks (người dùng click nhiều lần vì frustrated)
   - Dead clicks (click vào element không hoạt động)
   - Excessive scrolling

4. **AI Insights** (Clarity tự động phát hiện vấn đề)
   - Broken interactions
   - Confusing UX patterns
   - Mobile usability issues
   - Performance problems

---

## 🚀 CÁCH SỬ DỤNG CLARITY DASHBOARD

### 1. Truy Cập Dashboard
```
URL: https://clarity.microsoft.com/projects/view/tybfgieemx
Login: Dùng tài khoản Microsoft/GitHub/Google bạn đã đăng ký
```

### 2. Xem Session Recordings (Quan Trọng Nhất!)

**Bước 1**: Click vào tab **"Recordings"** ở menu bên trái

**Bước 2**: Chọn một session để xem (ví dụ: session 5 phút)

**Bước 3**: Xem video người dùng thao tác trên app của bạn:
- Họ click vào đâu?
- Họ cuộn đến đâu?
- Họ bỏ qua phần nào?
- Họ gặp khó khăn ở đâu?

**Lọc Sessions Theo**:
- Device type (Mobile vs Desktop)
- Country (Vietnam)
- Session duration (>30s = engaged users)
- Rage clicks (frustrated users)
- Dead clicks (confused users)

### 3. Xem Heatmaps

**Click Heatmap**:
- Xem phần nào được click nhiều nhất
- Phát hiện: Người dùng click vào đâu khi họ muốn làm gì?

**Scroll Heatmap**:
- Xem người dùng cuộn đến đâu
- Phát hiện: Bao nhiêu % người dùng thấy nội dung bên dưới?

**Ứng dụng cho Phase P0**:
```yaml
Progressive Disclosure Test:
  - Xem: Bao nhiêu % người dùng click "Xem thêm"?
  - Nếu <20% → Nội dung mặc định chưa đủ hấp dẫn
  - Nếu >50% → Người dùng muốn xem chi tiết (good!)

At-a-Glance Dashboard Test:
  - Xem: Người dùng dừng lại ở KPI nào?
  - Xem: Họ cuộn nhanh qua phần nào? (boring)
  - Xem: Họ click vào chart nào? (interesting)
```

### 4. Xem Dashboard Analytics

**Key Metrics để Theo Dõi**:

| Metric | Current | Target (Week 2) | How to Measure |
|--------|---------|-----------------|----------------|
| Bounce Rate | ??? | 20% | % sessions <10s |
| Avg Session Duration | ??? | 2-3 min | Time spent on app |
| Pages per Session | ??? | 3+ | Multi-page exploration |
| Rage Clicks | ??? | <5% | Frustrated interactions |
| Dead Clicks | ??? | <3% | Clicks on non-interactive elements |

### 5. Phân Tích AI Insights

Clarity tự động phát hiện:
- ❌ **Dead Clicks**: "Users clicked here but nothing happened"
- 😡 **Rage Clicks**: "Users clicked 5+ times rapidly (frustrated)"
- 📜 **Excessive Scrolling**: "Users scrolled up/down multiple times (confused)"
- 📱 **Mobile Issues**: "Touch targets too small (<44px)"

**Action Items từ Insights**:
```
Dead Click on "Doanh Thu" label
→ Người dùng nghĩ label có thể click được
→ Fix: Thêm tooltip hoặc làm rõ đây chỉ là label

Rage Click on "Upload CSV" button
→ Button không respond nhanh
→ Fix: Thêm loading spinner

Excessive Scrolling on dashboard
→ Người dùng không tìm thấy thông tin họ cần
→ Fix: Cải thiện Visual Hierarchy (đang làm Day 1!)
```

---

## 📊 WEEK 1 TESTING PLAN

### Day 1-2: Baseline Measurement
**Sau khi deploy app với Clarity**:
- [ ] Đợi 24 giờ để có dữ liệu
- [ ] Xem 10 session recordings đầu tiên
- [ ] Note down 3 vấn đề UX lớn nhất
- [ ] Screenshot bounce rate baseline

### Day 3-4: Progressive Disclosure Impact
**Sau khi implement "Xem thêm" button**:
- [ ] So sánh bounce rate trước/sau
- [ ] Xem: Bao nhiêu % click "Xem thêm"?
- [ ] Xem: Session duration có tăng không?
- [ ] Target: Bounce rate giảm từ 40% → 30%

### Day 5-7: At-a-Glance Dashboard Impact
**Sau khi implement status banner + top 3 KPIs**:
- [ ] Xem heatmap: Người dùng focus vào KPI nào?
- [ ] Xem: Time to first interaction có giảm không?
- [ ] Target: Bounce rate giảm từ 30% → 20%

### Day 8-10: User Testing Validation
**Tổng hợp insights từ Clarity + 5 SME owners**:
- [ ] So sánh: Clarity data vs User interview findings
- [ ] Confirm: UX rating 2.2 → 3.8?
- [ ] Identify: Top 3 remaining issues
- [ ] Plan: Week 2 improvements

---

## 🎯 SUCCESS CRITERIA (SMART Goals)

### Week 1 Targets
```yaml
Bounce Rate:
  Baseline: 40% (Day 1)
  Week 1 Target: 20% (Day 10)
  Measurement: Clarity Dashboard > Analytics > Bounce Rate

Session Duration:
  Baseline: ??? (Day 1)
  Week 1 Target: 2-3 minutes
  Measurement: Clarity Dashboard > Analytics > Avg Duration

Rage Clicks:
  Baseline: ??? (Day 1)
  Week 1 Target: <5%
  Measurement: Clarity Dashboard > Insights > Rage Clicks

Dead Clicks:
  Baseline: ??? (Day 1)
  Week 1 Target: <3%
  Measurement: Clarity Dashboard > Insights > Dead Clicks
```

### Month 1 Targets
```yaml
Mobile Usability:
  Current: 2.1/5.0
  Target: 4.3/5.0
  Measurement: Manual testing + Clarity mobile sessions

User Satisfaction:
  Current: 2.2/5.0 (estimated)
  Target: 3.8/5.0
  Measurement: 5 SME owner interviews + SUS score
```

---

## 🔧 TROUBLESHOOTING

### Không Thấy Dữ Liệu Trên Clarity?

**Nguyên nhân 1: Chưa đủ thời gian**
- Clarity cần 2-4 giờ để xử lý dữ liệu đầu tiên
- Giải pháp: Đợi thêm, refresh dashboard

**Nguyên nhân 2: App chưa được truy cập**
- Chưa ai visit app sau khi deploy
- Giải pháp: Tự test app (mở trên mobile + desktop)

**Nguyên nhân 3: Ad blocker chặn Clarity**
- Browser extension block tracking script
- Giải pháp: Tắt ad blocker hoặc test trên Incognito mode

**Nguyên nhân 4: Tracking code chưa chạy**
- Kiểm tra console log trong browser (F12)
- Tìm: Clarity script error
- Giải pháp: Xem phần "Verify Installation" bên dưới

### Verify Installation

**Cách 1: Check Browser Console**
```
1. Mở app: http://localhost:8501 (hoặc production URL)
2. Press F12 (mở Developer Tools)
3. Click tab "Console"
4. Tìm: "⏱️ PERF [0.XXs] COMPLETE: Microsoft Clarity tracking initialized"
5. Nếu thấy → Clarity đã load ✅
```

**Cách 2: Check Network Tab**
```
1. Mở app
2. Press F12 → Tab "Network"
3. Filter: "clarity.ms"
4. Nếu thấy request tới clarity.ms → Tracking đang gửi data ✅
```

**Cách 3: Check Clarity Dashboard**
```
1. Truy cập: https://clarity.microsoft.com/projects/view/tybfgieemx
2. Click "Setup" → "Tracking Status"
3. Nếu thấy "Receiving data" → ✅ Success!
```

---

## 📱 MOBILE TESTING CHECKLIST

### Test Trên Mobile Device Thật
- [ ] Mở app trên điện thoại của bạn
- [ ] Thao tác 2-3 phút (upload CSV, xem dashboard)
- [ ] Đợi 4 giờ
- [ ] Vào Clarity → Filter "Mobile" → Xem recording

### Phát Hiện Mobile Issues
```yaml
Touch Target Too Small:
  Issue: Button <44x44px (WCAG guideline)
  Detection: Clarity shows "missed clicks"
  Fix: Increase button size to 44x44px minimum

Text Too Small:
  Issue: Font size <16px on mobile
  Detection: Excessive zooming in recordings
  Fix: Use 36px/28px/20px hierarchy (Week 1 Day 1)

Horizontal Scrolling:
  Issue: Content wider than screen
  Detection: Users scrolling left-right
  Fix: Responsive CSS (max-width: 100%)
```

---

## 🎓 LEARNING RESOURCES

### Official Docs
- Clarity Help Center: https://learn.microsoft.com/en-us/clarity/
- Getting Started Guide: https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-setup

### Video Tutorials
- Clarity Overview (5 min): https://www.youtube.com/watch?v=ORnFRPXDCDw
- Session Recordings Deep Dive (10 min): https://www.youtube.com/watch?v=DvAXU7RbYSQ
- Heatmaps Analysis (8 min): https://www.youtube.com/watch?v=ij7vV5zGl7c

### Best Practices
- How to Analyze Session Recordings: https://clarity.microsoft.com/blog/analyze-recordings/
- Heatmap Interpretation Guide: https://clarity.microsoft.com/blog/heatmaps-guide/
- Mobile UX Insights: https://clarity.microsoft.com/blog/mobile-ux/

---

## 💡 PRO TIPS

### 1. Focus on Vietnamese Mobile Users
```
Filter Setup:
  Device: Mobile
  Country: Vietnam
  Session Duration: >30 seconds (engaged users)
```

### 2. Watch "Rage Click" Sessions First
```
These are frustrated users → High-priority issues!
Filter: Rage Clicks > 0
Sort by: Most rage clicks first
```

### 3. Compare Before/After Each Change
```
Week 1 Day 1: Take screenshots of all metrics
Week 1 Day 10: Compare screenshots
Improvement: UX 2.2 → 3.8? Bounce 40% → 20%?
```

### 4. Share Insights với Team (Nếu Có)
```
Clarity has "Share" feature:
  - Share session recording URL
  - Share heatmap
  - Export metrics to Excel
```

### 5. Set Up Custom Dashboards
```
Create dashboard for:
  - Mobile UX (mobile sessions only)
  - Key User Flows (CSV upload → Dashboard view)
  - Error Tracking (dead clicks, rage clicks)
```

---

## 🚀 NEXT STEPS

### Ngay Sau Khi Deploy App
1. ✅ Clarity tracking code đã được add vào `streamlit_app.py`
2. ⏳ Deploy app lên production (Streamlit Cloud hoặc server)
3. ⏳ Đợi 24 giờ để có dữ liệu
4. ⏳ Truy cập Clarity dashboard
5. ⏳ Xem 10 session recordings đầu tiên
6. ⏳ Note down top 3 UX issues
7. ⏳ Plan fixes cho Week 1 Day 3-4

### Weekly Review (Every Friday)
- [ ] Export metrics (bounce rate, session duration, etc.)
- [ ] Watch 5 most interesting sessions
- [ ] List top 3 issues discovered
- [ ] Plan next week improvements
- [ ] Update SESSION_CHECKPOINT.json with findings

---

## 📞 SUPPORT

### Nếu Cần Hỗ Trợ
- **Clarity Support**: https://learn.microsoft.com/en-us/clarity/support
- **Community Forum**: https://github.com/microsoft/clarity/discussions
- **Twitter**: @MSFTClarity

### Nếu Cần Hỗ Trợ Tích Hợp
- File này: `MICROSOFT_CLARITY_GUIDE.md`
- Integration code: `streamlit_app.py` (dòng 151-166)
- Helper functions: `utils/clarity_integration.py`

---

## ✅ CHECKLIST - ĐÃ HOÀN THÀNH

- [x] Microsoft Clarity account created
- [x] Project ID obtained: `tybfgieemx`
- [x] Tracking code added to `streamlit_app.py`
- [x] Performance logging added
- [x] Documentation created (this file)
- [ ] App deployed to production
- [ ] First 24 hours of data collected
- [ ] Baseline metrics recorded
- [ ] Week 1 testing plan started

---

**🎯 Mục Tiêu**: UX 2.2 → 3.8 stars (+73%) trong 10 ngày!

**🔥 Let's track real user behavior and build 5-star experience! 🇻🇳**
