# User Acceptance Testing (UAT) Guide

## 🎯 Objective

Validate that **DataAnalytics Vietnam** meets real SME user needs and willingness to pay **199k VND/month**.

---

## 👥 **Test Participants (Target: 1-2 SME Users)**

### **Ideal User Profile**
- **Company Size**: 5-50 employees (SME)
- **Role**: Marketing Manager, E-commerce Manager, Business Owner
- **Industry**: Marketing, E-commerce, Sales
- **Pain Points**: 
  - Manually creating reports in Excel (time-consuming)
  - No professional dashboard tools (PowerBI/Tableau too expensive)
  - Need data-driven insights but lack analytics expertise
  - Want industry benchmarks to compare performance

### **Where to Find Test Users**
1. **Your Network**: Friends in marketing/e-commerce roles
2. **Facebook Groups**: 
   - "Marketing Vietnam"
   - "E-commerce Vietnam"
   - "SME Vietnam"
3. **LinkedIn**: Search "Marketing Manager Vietnam" or "E-commerce Manager"
4. **Local Business Communities**: Startup events, coworking spaces

---

## 📋 **UAT Preparation Checklist**

### **Before UAT Session**
- [ ] **App is deployed** and accessible (https://fast-dataanalytics.streamlit.app/)
- [ ] **Sample datasets prepared** (marketing, e-commerce)
- [ ] **User has their own data** (optional, if they're comfortable sharing)
- [ ] **UAT script printed/prepared** (see below)
- [ ] **Feedback form ready** (see below)
- [ ] **Screen recording tool** (Loom, Zoom) to capture session

### **Communication with User**
Send this message to potential UAT participants:

```
Subject: Giúp test công cụ phân tích dữ liệu AI miễn phí - 30 phút

Xin chào [Tên],

Mình đang phát triển công cụ phân tích dữ liệu AI cho SME Việt Nam (giống Bricks.ai nhưng tốt hơn và rẻ hơn).

Bạn có thể giúp mình test trong 30 phút không? Mình sẽ:
✅ Quan sát bạn dùng công cụ (không cần chuẩn bị gì)
✅ Nghe feedback thật lòng (càng chê càng tốt!)
✅ Tặng bạn 3 tháng Premium miễn phí khi ra mắt

Link: https://fast-dataanalytics.streamlit.app/
Lịch: [Đề xuất 2-3 khung giờ]

Bạn có rảnh không?

Thanks,
[Tên bạn]
```

---

## 🧪 **UAT Session Structure (30 minutes)**

### **Phase 1: Context Setting (5 minutes)**

**Script for Facilitator**:
```
"Cảm ơn bạn đã dành thời gian test!

Mình đang làm công cụ phân tích dữ liệu tự động bằng AI cho SME. 
Mục tiêu: Biến dữ liệu Excel thành dashboard chuyên nghiệp trong 1 phút.

Quy tắc UAT:
1. Nói ra suy nghĩ khi dùng (think aloud)
2. Chê thẳng, đừng khách sáo
3. Không có câu trả lời đúng/sai
4. Mình sẽ ghi chú nhưng không giúp (trừ khi bạn bí)

Sẵn sàng chưa?"
```

**Questions to Ask**:
1. "Hiện tại bạn phân tích dữ liệu như thế nào?" (Excel? PowerBI? Thủ công?)
2. "Mất bao nhiêu thời gian mỗi tuần cho công việc này?"
3. "Bạn có dùng dashboard tool nào không?" (Tableau, PowerBI, Google Data Studio?)

---

### **Phase 2: First Impressions (2 minutes)**

**Task**: Show them https://fast-dataanalytics.streamlit.app/ and observe

**What to Watch For**:
- [ ] Do they understand what the app does?
- [ ] Is the UI clear and inviting?
- [ ] Do they know where to start?

**Questions to Ask**:
- "Nhìn trang này, bạn nghĩ nó làm gì?"
- "Bạn sẽ click vào đâu đầu tiên?"
- "Có gì khó hiểu không?"

---

### **Phase 3: Guided Task - Marketing Data (10 minutes)**

**Task**: "Hãy upload file này và tạo dashboard" (provide `marketing_google_ads.csv`)

**Observe Silently**:
- [ ] Can they find the upload button?
- [ ] Do they add a description?
- [ ] Do they understand the progress indicators?
- [ ] Do they wait patiently during processing?

**After Pipeline Completes, Ask**:
1. "Bạn thấy dashboard này như thế nào?" (professional? useful?)
2. "Có insights nào bất ngờ/hữu ích không?"
3. "Benchmarks (ROAS 4:1, CTR 3.17%) có giúp gì không?"
4. "Bạn có tin tưởng các số liệu này không?" (accuracy perception)
5. "So với cách bạn làm hiện tại, nhanh hơn bao nhiêu?"

---

### **Phase 4: Independent Task - Own Data (8 minutes)**

**Task**: "Bây giờ thử với dữ liệu của bạn" (if they have data)

**Alternative** (if no own data): "Thử với file e-commerce này" (`ecommerce_shopify.csv`)

**Observe**:
- [ ] Can they complete the task without help?
- [ ] Do they encounter any errors?
- [ ] Do they understand the domain detection?
- [ ] Are the insights relevant to their business?

**Ask After**:
1. "Dashboard này có giúp bạn ra quyết định không?"
2. "Bạn muốn thêm feature gì?" (export PDF? scheduled reports?)
3. "Có gì khó chịu/chậm không?"

---

### **Phase 5: Pricing & Willingness to Pay (5 minutes)**

**Critical Questions**:

1. **Value Perception**:
   - "Nếu công cụ này giúp bạn tiết kiệm [X] giờ/tuần, nó đáng giá bao nhiêu?"
   - "So với Excel thủ công, dashboard này tốt hơn bao nhiêu?"

2. **Competitive Context**:
   - "Bạn có biết Tableau ($70/tháng), PowerBI ($10/tháng), Bricks.ai ($500k VND/tháng) không?"
   - "Nếu công cụ này giá 199k VND/tháng (60% rẻ hơn Bricks.ai), bạn sẽ mua không?"

3. **Willingness to Pay (Critical!)**:
   ```
   "Giả sử 3 gói giá:
   - FREE: 60 AI messages/tháng (5 dashboard)
   - PRO: 199k VND/tháng - 500 messages (unlimited dashboards)
   - ENTERPRISE: 1-2 triệu VND/tháng - Unlimited + support
   
   Bạn sẽ chọn gói nào?"
   ```

4. **Deal Breakers**:
   - "Cái gì sẽ khiến bạn KHÔNG mua?" (giá? features? trust?)
   - "Thiếu feature nào thì bạn không dùng?"

---

## 📝 **Feedback Form (Give to User After Session)**

### **Section 1: Overall Experience**
1. **Ease of Use** (1-5 stars): ⭐⭐⭐⭐⭐
   - 1 = Rất khó dùng, 5 = Rất dễ
   
2. **Speed** (1-5 stars): ⭐⭐⭐⭐⭐
   - 1 = Quá chậm, 5 = Rất nhanh
   
3. **Visual Quality** (1-5 stars): ⭐⭐⭐⭐⭐
   - 1 = Xấu/nghiệp dư, 5 = Đẹp/chuyên nghiệp
   
4. **Insights Usefulness** (1-5 stars): ⭐⭐⭐⭐⭐
   - 1 = Vô dụng, 5 = Rất hữu ích

### **Section 2: Feature Requests**
"3 features bạn muốn nhất?" (rank 1-3)
- [ ] Export PDF/PowerPoint
- [ ] Scheduled reports (email hàng tuần)
- [ ] More chart types (sankey, heatmap, etc.)
- [ ] Compare multiple time periods
- [ ] Team collaboration (share dashboards)
- [ ] Database connectors (MySQL, PostgreSQL)
- [ ] Mobile app
- [ ] Custom branding (logo, colors)
- [ ] Other: _________________

### **Section 3: Willingness to Pay (CRITICAL)**

**Q1: Nếu FREE tier có 60 AI messages/tháng (5 dashboards), bạn có dùng không?**
- [ ] Có, chắc chắn
- [ ] Có, nhưng cần thêm features
- [ ] Không, vì: _________________

**Q2: Bạn sẵn sàng trả 199k VND/tháng cho gói PRO không? (500 messages, unlimited dashboards)**
- [ ] Có, ngay lập tức
- [ ] Có, nhưng cần thấy thêm features
- [ ] Không, giá quá cao → Giá hợp lý: _______ VND
- [ ] Không, vì: _________________

**Q3: Bạn sẽ giới thiệu tool này cho đồng nghiệp không?**
- [ ] Có, chắc chắn
- [ ] Có, nếu họ cần
- [ ] Không

### **Section 4: Open Feedback**
1. **What did you LOVE?** (Top 3)
   - 
   - 
   - 

2. **What FRUSTRATED you?** (Top 3)
   - 
   - 
   - 

3. **What would make you pay 199k VND/month?**
   - 

4. **Any other comments?**
   - 

---

## 📊 **UAT Success Criteria**

### **Minimum Success Thresholds**
- [ ] **Task Completion Rate**: ≥80% (user completes both tasks without help)
- [ ] **Average Rating**: ≥4/5 stars (across all 4 dimensions)
- [ ] **Willingness to Pay (FREE)**: ≥70% say "Yes"
- [ ] **Willingness to Pay (PRO 199k)**: ≥40% say "Yes" or "Maybe with features"
- [ ] **Recommendation Rate**: ≥60% say "Yes, definitely"

### **Red Flags (Need to Fix)**
- ❌ User gets stuck and cannot complete task
- ❌ User says "This is too slow" (>60s pipeline)
- ❌ User says "I don't understand this" (unclear UI)
- ❌ User says "I don't trust these numbers" (accuracy doubt)
- ❌ All users say "No" to 199k VND/month pricing

---

## 🔍 **Post-UAT Analysis**

### **Step 1: Aggregate Feedback**
Create a spreadsheet with:
- User ID (User 1, User 2)
- Industry (Marketing, E-commerce, etc.)
- Current tool (Excel, PowerBI, etc.)
- Task completion (Yes/No)
- Ratings (1-5 for each dimension)
- WTP FREE (Yes/No)
- WTP PRO 199k (Yes/Maybe/No)
- Top features requested
- Top frustrations

### **Step 2: Prioritize Fixes**
**Critical (Fix Now)**:
- Bugs that block task completion
- UI confusion (>50% users mention it)
- Performance issues (>60s consistently)

**High Priority (Fix Soon)**:
- Features requested by 100% users
- Frustrations mentioned by ≥50% users
- Pricing concerns (if <40% WTP)

**Medium Priority (Roadmap)**:
- Nice-to-have features (requested by <50%)
- Minor UI improvements

**Low Priority (Ignore)**:
- One-off requests
- Edge cases
- Out-of-scope features

### **Step 3: Iterate**
1. Fix critical issues
2. Re-test with same users (if possible)
3. Validate fixes work
4. Deploy updates
5. Repeat UAT with new users

---

## 🎯 **UAT Outcomes**

### **Scenario 1: Strong Validation (≥4/5 stars, ≥40% WTP)**
✅ **Action**: Proceed to launch!
- Create marketing website
- Set up payment (Stripe, MoMo, etc.)
- Launch on Product Hunt Vietnam
- Share on Facebook groups

### **Scenario 2: Moderate Validation (3-4/5 stars, 20-40% WTP)**
⚠️ **Action**: Iterate before launch
- Fix top 3 frustrations
- Add top 2 requested features
- Re-test with new users
- Validate improvements

### **Scenario 3: Weak Validation (<3/5 stars, <20% WTP)**
❌ **Action**: Major pivot needed
- Re-evaluate value proposition
- Consider different target market
- Simplify or add killer features
- Conduct deeper user interviews

---

## 📞 **Support During UAT**

If users encounter errors during UAT:

1. **Don't panic** - bugs are normal
2. **Note the error** (screenshot, error message)
3. **Ask user to describe what they did** before error
4. **Have backup plan**: Switch to sample data if their data breaks the app
5. **Thank them for finding the bug** (this is valuable!)

After UAT, fix bugs and redeploy immediately.

---

## ✅ **UAT Completion Checklist**

- [ ] Recruited 1-2 SME users
- [ ] Conducted 30-min UAT sessions
- [ ] Recorded sessions (with permission)
- [ ] Collected feedback forms
- [ ] Analyzed results (spreadsheet)
- [ ] Identified critical issues
- [ ] Measured WTP (willingness to pay)
- [ ] Documented insights
- [ ] Created iteration plan
- [ ] Marked Task #17 as COMPLETED

---

**Last Updated**: 2025-10-21  
**Version**: 1.0.0  
**Status**: Ready for UAT
