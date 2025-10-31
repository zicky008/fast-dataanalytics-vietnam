# 🚀 PHASE 1: DEPLOYMENT CHECKLIST (PATH C - HYBRID)

**Goal**: Deploy current version → Test with 3 domains → Identify highest demand → Deep dive

---

## ✅ PRE-DEPLOYMENT CHECKS

### 1. Code Integration Status
- [x] Visual Hierarchy CSS integrated (commit 0b4e622)
- [x] Progressive Disclosure integrated (commit 0b4e622)
- [x] Benchmarks research validated (commit b67bbfc)
- [x] Pipeline flows documented (commit b67bbfc)
- [ ] **Local testing passed** (THIS STEP)
- [ ] Microsoft Clarity enabled
- [ ] Production URL obtained

### 2. Sample Data Ready (3 Domains)
- [x] E-commerce: `sample_data/ecommerce_shopify_daily.csv`
  - Has: cart_abandonment_rate, channel, conversion_rate, aov
  - Perfect for: Channel comparison, cart abandonment alerts
- [x] Retail: `sample_data/manufacturing_production_30days.csv`
  - Has: production data
  - Need to verify: inventory, staff metrics
- [x] Services: `sample_data/customer_service_tickets_30days.csv`
  - Has: ticket data
  - Need to verify: resolution time, satisfaction metrics

### 3. User Testing Plan
- [ ] Recruit 3 users (1 per domain)
  - [ ] E-commerce: Shopee/Lazada seller
  - [ ] Retail: Physical store owner
  - [ ] Services: Spa/Salon/Clinic owner
- [ ] Prepare interview script (Vietnamese)
- [ ] Microsoft Clarity project setup

---

## 📋 DEPLOYMENT STEPS

### Step 1: Local Testing (15 minutes)
```bash
# Test current version locally
cd /home/user/webapp
streamlit run streamlit_app.py

# Manual tests:
1. Upload ecommerce_shopify_daily.csv
2. Verify progressive disclosure (3 KPIs default, "Xem thêm" button)
3. Check visual hierarchy (36px primary KPIs)
4. Test on mobile viewport (Chrome DevTools: 375x667)
5. Verify no errors in console
```

**Success Criteria**:
- [ ] App loads without errors
- [ ] Top 3 KPIs visible (36px font)
- [ ] "Xem thêm" button works
- [ ] Expansion shows remaining 9 KPIs
- [ ] Mobile responsive (no horizontal scroll)

---

### Step 2: Streamlit Cloud Deployment (10 minutes)
```bash
# Push to GitHub (if not already)
git push origin main

# Deploy to Streamlit Cloud:
1. Go to https://streamlit.io/cloud
2. Connect GitHub repo
3. Select main branch
4. Deploy streamlit_app.py
5. Get permanent URL: https://[your-app].streamlit.app
```

**Success Criteria**:
- [ ] Production URL obtained
- [ ] App accessible via URL
- [ ] No deployment errors
- [ ] CSV upload works in production

---

### Step 3: Microsoft Clarity Setup (5 minutes)
```yaml
Project: tybfgieemx (already created)
Dashboard: https://clarity.microsoft.com/projects/view/tybfgieemx

Enable tracking:
1. Verify Clarity script in streamlit_app.py (should be at line ~75)
2. Test: Visit production URL
3. Wait 2-4 hours for data processing
4. Check Clarity dashboard for sessions
```

**Success Criteria**:
- [ ] Clarity script present in code
- [ ] First session recorded (after 2-4h)
- [ ] Heatmaps available

---

## 🧪 TESTING PROTOCOL (PHASE 1)

### Test 1: E-Commerce Domain (Day 1)
**User Profile**: Shopee seller, 100-500 orders/month

**Test Steps**:
1. Share production URL via Zalo
2. Ask user to upload their Shopee CSV
3. Observe via Clarity (screen recording)
4. 30-minute interview (Vietnamese)

**Questions to Ask**:
```yaml
1. "Anh/chị thấy dashboard này dễ hiểu không?" (1-5 scale)
2. "Cái gì anh/chị chú ý đầu tiên?"
3. "Anh/chị có click 'Xem thêm 9 chỉ số' không? Tại sao?"
4. "Top 3 KPIs có phải là những gì anh/chị quan tâm nhất không?"
5. "Anh/chị muốn biết thêm gì về cart abandonment rate?"
6. "So với cách anh/chị đang dùng (Excel/Google Sheets), tool này khác gì?"
7. "Điểm nào anh/chị thích nhất?"
8. "Điểm nào anh/chị thấy khó hiểu/khó dùng?"
9. "Anh/chị có giới thiệu cho seller khác không?"
10. "Nếu có tính năng XYZ, anh/chị có trả tiền không?"
```

**Data to Collect**:
- [ ] Time to first insight (target: <30s)
- [ ] Bounce or complete session?
- [ ] Clicked "Xem thêm"? (yes/no)
- [ ] Which KPIs did user focus on? (from Clarity heatmap)
- [ ] User confusion points (from recording)
- [ ] Feature requests (write down)

---

### Test 2: Retail Domain (Day 2)
**User Profile**: Physical store owner (fashion, electronics, grocery)

**Same protocol as Test 1**, but focus on:
- Inventory questions (slow-moving products)
- Staff performance questions
- Peak hours questions

---

### Test 3: Services Domain (Day 3)
**User Profile**: Spa, salon, clinic, gym owner

**Same protocol**, focus on:
- No-show rate questions
- Package conversion questions
- Customer retention questions

---

## 📊 SUCCESS METRICS (PHASE 1)

### Baseline Metrics (Current - Unknown)
```yaml
To Measure:
- Actual bounce rate (vs predicted 40%)
- Actual time-to-insight (vs predicted 45s)
- Actual "Xem thêm" click rate (predict 50%+)
- Actual mobile usage % (predict 60%+)
- Actual domain demand (which domain has most interest?)
```

### Target Metrics (End of Phase 1 - 3 Days)
```yaml
Quantitative:
- [ ] 3 users tested (1 per domain)
- [ ] Clarity: 3+ full sessions recorded
- [ ] Average session duration: >2 minutes
- [ ] "Xem thêm" click rate: >40%
- [ ] Mobile usage: >50%

Qualitative:
- [ ] Identify top domain (most pain points + willingness to pay)
- [ ] Document top 3 feature requests per domain
- [ ] Identify top 3 UX friction points
- [ ] Get 3 testimonials (even if "needs improvement")
```

---

## 🎯 PHASE 1 DECISION POINT (Day 4)

After 3 days of testing, we decide:

### Scenario A: E-commerce has HIGHEST demand
```yaml
Signals:
- E-commerce user most excited
- Most feature requests from e-commerce
- E-commerce user asks "when can I use daily?"

Next Action: DEEP DIVE E-COMMERCE
- Create cart abandonment alert system
- Channel comparison detailed view
- Integration with Shopee API (future)
- Vietnamese e-commerce benchmarks (refined)
```

### Scenario B: Retail has HIGHEST demand
```yaml
Signals:
- Retail user has acute inventory pain
- Asks about staff performance tracking
- Willing to pay for solution

Next Action: DEEP DIVE RETAIL
- Inventory slow-moving alerts
- Staff performance dashboard
- Peak hours heatmap
- POS integration roadmap
```

### Scenario C: Services has HIGHEST demand
```yaml
Signals:
- Services user frustrated with no-shows
- Asks about package upsell tracking
- Needs customer retention features

Next Action: DEEP DIVE SERVICES
- No-show rate tracking + alerts
- Package conversion funnel
- Customer lifetime value calculator
- Booking system integration
```

### Scenario D: ALL 3 have demand (unlikely but possible)
```yaml
Next Action: PRIORITIZE by Revenue Potential
- Which domain willing to pay most?
- Which domain easiest to serve?
- Which domain fastest time-to-revenue?
```

---

## 📝 PHASE 1 DELIVERABLES

### End of Day 3:
1. **Testing Report** (this will be created after testing)
   - 3 user interview transcripts (Vietnamese)
   - Clarity session recordings (3+)
   - Heatmap analysis
   - Bounce rate, time-to-insight metrics
   
2. **Domain Priority Decision**
   - Which domain to deep dive FIRST
   - Why? (data-backed reasoning)
   - Top 3 feature requests for that domain
   
3. **Phase 2 Roadmap**
   - A-Z product details for chosen domain
   - Domain-specific features to build
   - Timeline: Week 2 implementation

---

## 🚨 CRITICAL REMINDERS

### During Testing:
- ❌ **DON'T**: Lead users ("Do you like this feature?")
- ✅ **DO**: Let users explore naturally
- ✅ **DO**: Ask "What are you thinking?" when they pause
- ✅ **DO**: Record exact quotes (for testimonials)
- ✅ **DO**: Note when they look confused
- ✅ **DO**: Ask "What would you do next?" at decision points

### After Testing:
- ❌ **DON'T**: Build features users didn't ask for
- ❌ **DON'T**: Assume all 3 domains need same features
- ✅ **DO**: Focus on ONE domain first (highest ROI)
- ✅ **DO**: Validate with "Would you pay ₫99K/month for this?"
- ✅ **DO**: Document everything (quotes, videos, metrics)

---

## ⏭️ NEXT IMMEDIATE ACTION

**RIGHT NOW**: Local testing before deployment

```bash
cd /home/user/webapp
streamlit run streamlit_app.py
```

**Manual Test Checklist**:
- [ ] Upload `sample_data/ecommerce_shopify_daily.csv`
- [ ] Top 3 KPIs visible (Revenue, Conversion Rate, AOV)?
- [ ] Font sizes correct (36px primary)?
- [ ] "Xem thêm 9 chỉ số" button present?
- [ ] Click button → 9 more KPIs appear?
- [ ] Mobile test (375x667 viewport)?
- [ ] No console errors?

**If ALL PASS → Deploy to Streamlit Cloud**
**If FAIL → Fix issues first, then deploy**

---

**Status**: ⏳ READY FOR LOCAL TESTING
**Next Step**: Run `streamlit run streamlit_app.py` and verify checklist above
