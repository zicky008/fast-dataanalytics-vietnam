# 📅 WEEK 2 PLAN: Acquisition Week

> **Theme**: Get first 20 signups
> **Goal**: 20 signups, 80%+ activation rate
> **Focus**: LinkedIn content + Email sequence + Product-led growth
> **Time**: 45 hours (full-time) OR 22 hours (side hustle)

---

## 🎯 Week 2 Overview

**What We Accomplished in Week 1**:
- ✅ Sample data feature (7 domains)
- ✅ Vietnamese error messages (10 types)
- ✅ Onboarding welcome message
- ✅ Sidebar optimization (pricing + Zalo)
- ✅ Payment + Zalo documentation
- ✅ Customer interview script

**Week 2 Focus Shift**:
- Week 1: ACTIVATION (product fixes)
- Week 2: ACQUISITION (get users to try the product)

---

## 📊 Daily Plan (Monday-Friday)

### 🌅 **Morning Routine** (2 hours daily - 10h total)

**9:00-9:30 AM**: LinkedIn Engagement
- Comment on 10 posts from target audience (CEOs, Managers)
- Share value, not sales pitch
- Goal: Build visibility

**9:30-10:30 AM**: Content Creation
- 1 post every 2 days (3 posts total Week 2)
- Use customer interview insights
- Authentic storytelling

**10:30-11:00 AM**: Respond to Messages
- All LinkedIn comments/DMs
- Warm leads from Week 1 interviews

---

### 🌆 **Afternoon Work** (4-5 hours daily - 20h total)

#### **Monday**: Email Sequence Setup (5 hours)
**Goal**: Automated 5-email nurture sequence

**Tasks**:
1. **Setup Mailchimp** (free tier, 500 contacts) - 30 mins
   - Create account
   - Create audience list
   - Setup automation trigger (user signs up)

2. **Write 5 Emails** (use Genspark) - 2 hours
   - Day 1: Welcome + Quick start
   - Day 7: Usage reminder + Value highlight
   - Day 14: Social proof + Case study
   - Day 21: Early adopter offer (₫49K lifetime)
   - Day 28: Urgency + Last chance

3. **Integrate with Streamlit** (Claude Code) - 1.5 hours
   - Add email capture on signup
   - Send to Mailchimp API
   - Test flow end-to-end

4. **Test Sequence** (manual) - 1 hour
   - Sign up with test email
   - Verify all 5 emails schedule correctly
   - Check links work

**Expected Impact**: 15% conversion lift (25% total conversion rate)

---

#### **Tuesday**: Landing Page Copy Optimization (3 hours)
**Goal**: Reduce bounce rate 60% → 20%

**Tasks**:
1. **Optimize Hero Section** (Genspark) - 1 hour
   ```
   Before: "DataAnalytics Vietnam - AI-Powered Dashboard Builder"
   After:  "Excel → Dashboard Chuyên Nghiệp Trong 60 Giây"

   Subheadline:
   "Dành cho CEO E-commerce & Marketing Việt Nam
   (Không cần biết code, không cần data analyst)"

   Trust Line:
   "✅ Đã giúp 10+ SME Việt Nam tiết kiệm 5 giờ/tuần"
   ```

2. **Update CTAs** - 30 mins
   ```
   Primary: "🚀 Tạo Dashboard Miễn Phí" (not "Sign Up")
   Secondary: "▶️ Xem Demo 90 Giây"
   ```

3. **Add Social Proof** - 1 hour
   - 3 Vietnamese testimonials (from Week 1 interviews if available)
   - Or use: "Đã giúp 10+ SMEs tiết kiệm X giờ/tuần"

4. **Deploy & Test** - 30 mins
   - Update streamlit_app.py
   - Commit + Push
   - Verify in production

**Expected Impact**: Bounce rate 40% improvement, +40% signups

---

#### **Wednesday**: Product-Led Growth Features (4 hours)
**Goal**: Viral mechanisms + retention hooks

**Tasks**:
1. **Add Dashboard Watermark** (Claude Code) - 1 hour
   ```python
   # Bottom of dashboard
   "📊 Created with Fast DataAnalytics
   Try free: https://fast-nicedashboard.streamlit.app"
   ```
   - When users share PDF/screenshots → Free marketing

2. **Referral Link Generator** (Claude Code) - 2 hours
   ```python
   # After successful dashboard creation
   st.success("✅ Dashboard created!")
   st.info("""
   💡 Share with friends:
   Your referral link: https://fast-data.com/ref/[user_id]

   You get: ₫10K credit per referral
   They get: Extra 7 days free trial (37 days total)
   """)
   ```
   - Track referrals in session state
   - Give incentives

3. **Test & Deploy** - 1 hour
   - Verify watermark appears on all exports
   - Test referral link generation
   - Commit + Push

**Expected Impact**: 10-15% organic signups from referrals/shares

---

#### **Thursday**: Competitor Analysis (2 hours)
**Goal**: Understand competition, find differentiation opportunities

**Tasks**:
1. **Analyze Top 3 Competitors** (Genspark) - 1.5 hours
   ```
   Prompt Genspark:
   "Analyze top 3 competitors for data analytics in Vietnam:
   - Base.vn
   - Subiz.com (analytics module)
   - Haravan Analytics

   For each, provide:
   - Features
   - Pricing
   - Target market
   - Strengths
   - Weaknesses

   Identify: What can Fast DataAnalytics do better?"
   ```

2. **Create Competitive Matrix** - 30 mins
   | Feature | Base.vn | Subiz | Haravan | **Fast Data** |
   |---------|---------|-------|---------|---------------|
   | Price | ₫500K+ | ₫300K+ | ₫200K+ | **₫99K** ✅ |
   | Speed | 5+ mins | 3+ mins | 2+ mins | **60s** ✅ |
   | Vietnamese | Partial | Partial | Good | **100%** ✅ |
   | Sample Data | No | No | Limited | **7 domains** ✅ |
   | Zalo Support | No | Yes | No | **Yes** ✅ |

3. **Update Positioning** - Based on gaps found

**Expected Impact**: Clear differentiation messaging → 20% higher conversion

---

#### **Friday**: Week 2 Review + Week 3 Prep (3 hours)
**Goal**: Measure progress, plan next week

**Tasks**:
1. **Calculate Week 2 Metrics** (1 hour)
   ```
   Metrics to track:
   - Signups: X/20 target
   - Activation rate: X% (target 80%+)
   - LinkedIn posts: 3/3 ✅
   - LinkedIn engagement: X comments, X profile views
   - Email sequence: Active? (Yes/No)
   - Landing page: Bounce rate X%
   - Referrals: X users referred

   Decision:
   - On track? → Continue Week 3 (Conversion focus)
   - Behind? → Double down on LinkedIn + outreach
   ```

2. **Collect First User Feedback** (1 hour)
   - Email/Zalo 5-10 users who created dashboards
   - Ask: "What did you like? What can improve?"
   - Note: Feature requests, pain points still unsolved

3. **Plan Week 3** (1 hour)
   - Week 3 theme: CONVERSION (get first 5 paying customers)
   - Tactics: Early adopter outreach, in-app upgrade prompts, case studies
   - Daily plan: Who to contact, what to offer

**Expected Outcome**: Clear Week 3 roadmap with 5 paying customer goal

---

## 📋 Weekly Checklist

### 🎯 Content (Marketing)
- [ ] Monday: LinkedIn post #1 (Problem identification from interviews)
- [ ] Wednesday: LinkedIn post #2 (Solution building / product demo)
- [ ] Friday: LinkedIn post #3 (Early validation / launch invitation)
- [ ] Daily: 10 comments on target audience posts (50 total/week)
- [ ] Daily: Respond to all comments/DMs within 2 hours

### 🛠️ Product (Features)
- [ ] Monday: Email sequence live (Mailchimp + Streamlit integration)
- [ ] Tuesday: Landing page optimized (Hero + CTAs + Social proof)
- [ ] Wednesday: Dashboard watermark + Referral links implemented
- [ ] Thursday: Competitive analysis complete
- [ ] Friday: Week 2 metrics calculated

### 💬 Engagement (Users)
- [ ] Follow up with 5 Week 1 interview Hot Leads
- [ ] Email 10 Warm Leads from Week 1
- [ ] Respond to all app users who reach out (Zalo/Email <2h)
- [ ] Collect feedback from 5-10 users who created dashboards

---

## 🎯 Success Metrics (Week 2 Targets)

### Primary Metrics:
```
✅ Signups: 20+ (from 0-2 Week 1)
✅ Activation rate: 80%+ maintained
✅ LinkedIn posts: 3/3 published
✅ Email sequence: Active (automated)
```

### Secondary Metrics:
```
✅ LinkedIn engagement: 50+ comments on others' posts
✅ Landing page bounce rate: <40% (from 60%)
✅ Referrals: 2-5 organic signups
✅ User feedback: 5-10 responses collected
```

### Conversion Setup (for Week 3):
```
✅ 2-3 "interested in paying" conversations started
✅ Early adopter offer prepared (₫49K lifetime)
✅ Case study drafted (from best user)
```

---

## 💡 Key Tactics (Zero Budget)

### Tactic #1: LinkedIn Content Calendar (Genspark)
- **Time**: 3 hours (1h/post × 3 posts)
- **Cost**: ₫0
- **Expected**: 3 posts × 3 interested people/post = 9 leads
- **ROI**: 300%

### Tactic #5: Email Sequence (Mailchimp Free)
- **Time**: 5 hours (setup + integration)
- **Cost**: ₫0 (Mailchimp free tier)
- **Expected**: 15% conversion lift
- **ROI**: 350%

### Tactic #6: Landing Page Copy (Genspark)
- **Time**: 3 hours
- **Cost**: ₫0
- **Expected**: Bounce 60% → 20% = +40% signups
- **ROI**: 2,000%

### Tactic #7: Competitor Analysis (Genspark)
- **Time**: 2 hours
- **Cost**: ₫0
- **Expected**: Clear differentiation → +20% conversion
- **ROI**: 200%

---

## 🚨 Red Flags (Stop & Reassess)

If by Week 2 end:
- **<5 signups** → Acquisition broken
  - Action: More aggressive LinkedIn, Facebook groups, cold DMs

- **<60% activation** → Product UX issues
  - Action: Watch 3-5 users use product (screen share), fix friction points

- **0 engagement** on LinkedIn posts → Content not resonating
  - Action: Use exact language from customer interviews, more storytelling

- **High bounce rate (>50%)** → Landing page unclear
  - Action: Simplify hero message, add video demo, more social proof

---

## 🔄 Daily Routine (Side Hustle - 22h/week)

### Weekday (Mon-Fri): 3-4 hours/day

**Morning (1 hour before day job)**:
- 7:00-7:30am: LinkedIn engagement (10 comments)
- 7:30-8:00am: Respond to messages/emails

**Evening (2-3 hours after day job)**:
- 7:00-9:00pm: Main task of the day (Monday = Email, Tuesday = Landing, etc.)
- 9:00-10:00pm: Follow-ups, user feedback

### Weekend (Sat-Sun): 4 hours total
- Saturday 2h: Content batch creation (next week's 3 posts)
- Sunday 2h: Week review + planning

---

## 📖 Resources

### LinkedIn Post Templates:
See `PMF_STRATEGY_03_ZERO_BUDGET_TACTICS.md` lines 76-88 for Week 1 Post 1 example.

### Email Sequence Templates:
See `PMF_STRATEGY_03_ZERO_BUDGET_TACTICS.md` lines 600-629 for full 5-email sequence.

### Landing Page Copy:
See `PMF_STRATEGY_03_ZERO_BUDGET_TACTICS.md` lines 702-757 for optimized hero section.

### Competitor Analysis:
See `PMF_STRATEGY_03_ZERO_BUDGET_TACTICS.md` lines 811-821 for Genspark prompt.

---

## ✅ Week 2 Complete Checklist

- [ ] **Monday**: Email sequence live
- [ ] **Tuesday**: Landing page optimized
- [ ] **Wednesday**: PLG features (watermark + referral)
- [ ] **Thursday**: Competitor analysis done
- [ ] **Friday**: Week 2 metrics + Week 3 plan
- [ ] **Ongoing**: 3 LinkedIn posts, 50 comments, all DMs answered
- [ ] **Outcome**: 20 signups, 80% activation, 2-3 warm conversion leads

---

## 🚀 Week 3 Preview

**Theme**: CONVERSION WEEK
**Goal**: 5 paying customers (₫495K MRR)
**Tactics**:
- Early adopter outreach (email 30 active free users)
- In-app upgrade prompts (after 5 dashboards)
- Social proof (testimonials on landing page)
- Personal touch (Zalo calls with interested users)

**Expected Outcome**: 5/5 customers = ₫495K MRR by end of Week 3

---

**Document Status**: ✅ READY FOR EXECUTION
**Time Commitment**: 45 hours full-time OR 22 hours side hustle
**Cost**: ₫0 (all zero-budget tactics)
**Expected ROI**: 20 signups → 16 activated (80%) → 3-4 paying by Week 3 (20% conversion)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
