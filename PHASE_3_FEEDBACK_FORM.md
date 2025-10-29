# Phase 3: User Feedback Form Structure (Google Forms)

**Purpose**: Collect structured feedback from 5-10 Vietnam users to achieve 10/10 score
**Platform**: Google Forms (free, easy to use, automatic data collection)
**Target**: 15 minutes completion time per user

---

## How to Create This Form

### Step 1: Go to Google Forms
1. Open https://forms.google.com
2. Click "+ Blank form" or use a template
3. Set form title: "Benchmark URL Validation - User Testing Feedback"

### Step 2: Copy Questions Below
Copy each section below into your Google Form, following the format instructions.

### Step 3: Configure Settings
- ✅ Collect email addresses: Optional (for follow-up)
- ✅ Limit to 1 response: No (allow multiple if needed)
- ✅ Response receipts: Yes (send copy to respondent)
- ✅ Response editing: Yes (allow users to edit after submission)

### Step 4: Share Form
- Get shareable link
- Include in recruitment email
- Track responses in Google Sheets (automatic)

---

## Form Structure

---

### SECTION 1: Welcome & Instructions

**Title**: Benchmark URL Validation - User Testing Feedback

**Description**:
```
Thank you for helping us achieve 10/10 data quality! 🎯

This feedback form takes 10-15 minutes to complete. Your honest feedback helps us:
- ✅ Verify all benchmark URLs work for real users
- ✅ Ensure data is useful and credible
- ✅ Achieve perfect 10/10 credibility score

Please answer all questions honestly. Critical feedback is more valuable than overly positive feedback!

Your responses will be used to:
1. Fix any broken/fake URLs
2. Improve benchmark quality
3. Document user validation in our Phase 3 report

Privacy: Your responses will be kept confidential unless you give permission to quote you.
```

---

### SECTION 2: Your Profile (Optional but Helpful)

#### Question 1: What's your name? (Optional)
- **Type**: Short answer
- **Required**: No
- **Placeholder**: "First Last or 'Anonymous'"

#### Question 2: What's your email? (Optional)
- **Type**: Short answer
- **Required**: No
- **Placeholder**: "your.email@example.com"
- **Note**: "Only if you want to receive final results summary"

#### Question 3: What's your role/title?
- **Type**: Short answer
- **Required**: Yes
- **Placeholder**: "e.g., HR Manager, Marketing Director, E-commerce Owner, Data Analyst"

#### Question 4: What industry do you work in?
- **Type**: Multiple choice
- **Required**: Yes
- **Options**:
  - HR / Human Resources / Talent Acquisition
  - Marketing / Advertising / Digital Marketing
  - E-commerce / Retail / Online Sales
  - Data Analytics / Business Intelligence
  - Consulting / Professional Services
  - Technology / Software
  - Finance / Banking
  - Other: ___________

#### Question 5: How many years of professional experience do you have?
- **Type**: Multiple choice
- **Required**: Yes
- **Options**:
  - 0-2 years
  - 3-5 years
  - 6-10 years
  - 11+ years

---

### SECTION 3: URL Testing Results

**Section Title**: URL Validation Results

**Section Description**:
```
Please answer the following questions for EACH URL you tested.

If you tested multiple URLs, you'll see repeated questions for each one. Just fill out what applies to the URLs you actually tested.

Reminder: You only need to test 5-10 URLs from your chosen domain (HR, Marketing, E-commerce, or General).
```

---

#### Question 6: Which domain did you test?
- **Type**: Multiple choice
- **Required**: Yes
- **Options**:
  - Option A: HR / Salary Benchmarks
  - Option B: Marketing / Advertising Benchmarks
  - Option C: E-commerce / Conversion Benchmarks
  - Option D: General / All Benchmarks (mix)

---

#### Question 7: How many URLs did you test total?
- **Type**: Multiple choice
- **Required**: Yes
- **Options**:
  - 1-3 URLs
  - 4-6 URLs
  - 7-10 URLs
  - 10+ URLs

---

### URL Testing Template (Repeat for Each URL)

**Instructions for Google Forms**:
Create a "URL Testing" section that repeats for each URL. You can either:
1. Create 10 separate sections (one per URL)
2. Create 1 section with repeating question groups
3. Ask users to test 5 URLs and provide 5 sets of questions

**Recommended**: Create 5 URL testing blocks (most users will test 5 URLs)

---

#### For Each URL (URL #1, URL #2, URL #3, URL #4, URL #5):

**Section Title**: URL #[X] Testing

##### Q[X].1: Which URL did you test? (URL #[X])
- **Type**: Dropdown or Short answer
- **Required**: Yes (for URL #1-5), No (for URL #6-10)
- **Options** (Dropdown - all 26 URLs):
  - Michael Page Vietnam Salary Guide 2025
  - Talentnet-Mercer Total Remuneration Report 2024
  - Robert Walters Salary Survey Vietnam 2025
  - ITviec Vietnam IT Salary Report 2024-2025
  - Adecco Vietnam Salary Guide 2024
  - VietnamWorks Salary Report 2024
  - LinkedIn Workforce Report
  - Gallup State of the Global Workplace
  - Anphabe Best Places to Work 2024
  - Vietnam Digital Report 2024 (DataReportal)
  - Google Vietnam Mobile Commerce Insights
  - HubSpot Sales Strategy & Trends Report
  - WordStream PPC Benchmarks 2024
  - Mailchimp Email Marketing Benchmarks
  - Unbounce Conversion Benchmark Report
  - LinkedIn State of Sales Report
  - Vietnam E-Business Index 2024 (VECOM)
  - Baymard Institute Cart Abandonment Statistics
  - Adobe Digital Economy Index
  - Statista E-commerce Conversion Rates
  - Zendesk Customer Experience Trends
  - Bain & Company NPS Benchmarks
  - Calculated from Your Dataset Statistics
  - Other (specify in comments)

##### Q[X].2: Did the URL work? (URL #[X])
- **Type**: Multiple choice
- **Required**: Yes
- **Options**:
  - ✅ Yes - Loaded perfectly
  - ⚠️ Partial - Loaded but with issues (specify below)
  - ❌ No - Broken/404/403/Error
  - 🔒 Paywall - Requires payment to access
  - 📝 Registration - Requires free signup to access
  - Not tested (skipped this URL)

##### Q[X].3: How fast did the page load? (URL #[X])
- **Type**: Multiple choice
- **Required**: No
- **Options**:
  - ⚡ Fast (< 3 seconds)
  - ⏱️ Medium (3-10 seconds)
  - 🐢 Slow (> 10 seconds)
  - ❌ Didn't load
  - Not tested

##### Q[X].4: Was the benchmark data visible on the page? (URL #[X])
- **Type**: Multiple choice
- **Required**: No
- **Options**:
  - ✅ Yes - Clear and visible
  - ⚠️ Partial - Some data visible, some hidden
  - ❌ No - No data visible
  - 📄 PDF Download - Data in downloadable file
  - 🔒 Behind paywall/login
  - Not tested

##### Q[X].5: How useful was the benchmark data? (URL #[X])
- **Type**: Linear scale (1-5 stars)
- **Required**: No
- **Scale**: 1 (Not useful) to 5 (Very useful)
- **Labels**:
  - 1 = Not useful at all / Generic / Vague
  - 2 = Slightly useful / Limited data
  - 3 = Moderately useful / Some good data
  - 4 = Very useful / Detailed and actionable
  - 5 = Extremely useful / Perfect for my needs

##### Q[X].6: Rate the credibility/trustworthiness of this source (URL #[X])
- **Type**: Linear scale (1-5 stars)
- **Required**: No
- **Scale**: 1 (Don't trust) to 5 (Completely trust)
- **Labels**:
  - 1 = Don't trust / Looks fake / No authority
  - 2 = Low trust / Questionable source
  - 3 = Neutral / Somewhat credible
  - 4 = High trust / Credible source
  - 5 = Complete trust / Authoritative / Industry leader

##### Q[X].7: Any specific issues or comments about this URL? (URL #[X])
- **Type**: Long answer
- **Required**: No
- **Placeholder**: "e.g., '403 error but tried incognito and it worked', 'Data is outdated (2022)', 'Perfect - exactly what I needed', etc."

---

**NOTE**: Repeat the above 7 questions for URLs #2, #3, #4, #5 (minimum).

Optionally create URLs #6-10 for users who test more than 5 URLs.

---

### SECTION 4: Overall Assessment

**Section Title**: Overall Feedback

**Section Description**:
```
Now that you've tested several URLs, please give us your overall assessment of the benchmark quality.
```

---

#### Question 20: Overall, how would you rate the benchmark URL quality?
- **Type**: Linear scale (1-5 stars)
- **Required**: Yes
- **Scale**: 1 (Very poor) to 5 (Excellent)
- **Labels**:
  - 1 = Very poor quality / Many broken URLs / Not useful
  - 2 = Below average / Several issues / Limited usefulness
  - 3 = Average / Some good, some issues / Moderately useful
  - 4 = Good quality / Few issues / Mostly useful
  - 5 = Excellent quality / All URLs work / Very useful

#### Question 21: How would you rate the Vietnam-specific sources?
- **Type**: Linear scale (1-5 stars)
- **Required**: Yes (if tested Vietnam sources), No (otherwise)
- **Scale**: 1 (Poor) to 5 (Excellent)
- **Labels**:
  - 1 = Poor / Not Vietnam-specific / Not credible
  - 2 = Below average / Questionable authority
  - 3 = Average / Decent but could be better
  - 4 = Good / Credible Vietnam sources
  - 5 = Excellent / Authoritative / Perfect for Vietnam market
  - N/A (didn't test Vietnam sources)

#### Question 22: How much do you trust the data quality?
- **Type**: Linear scale (1-5 stars)
- **Required**: Yes
- **Scale**: 1 (Don't trust) to 5 (Completely trust)
- **Labels**:
  - 1 = Don't trust at all / Seems fake / Not credible
  - 2 = Low trust / Questionable quality
  - 3 = Neutral / Some trust but skeptical
  - 4 = High trust / Seems credible and accurate
  - 5 = Complete trust / Would use for important decisions

#### Question 23: Would you use this tool for your work?
- **Type**: Multiple choice
- **Required**: Yes
- **Options**:
  - ✅ Yes, definitely - Would use regularly
  - 👍 Yes, probably - Would use occasionally
  - 🤔 Maybe - Depends on improvements
  - 👎 Probably not - Needs significant work
  - ❌ No - Not useful for me
  - Not applicable to my work

#### Question 24: What impressed you MOST about the benchmarks?
- **Type**: Long answer
- **Required**: No
- **Placeholder**: "e.g., 'Vietnam-specific sources are excellent', 'All URLs actually worked!', 'Data is very detailed and actionable', 'Mix of local and global sources is perfect', etc."

#### Question 25: What needs IMPROVEMENT?
- **Type**: Long answer
- **Required**: No
- **Placeholder**: "e.g., 'Some URLs were slow', 'Need more Vietnam sources for X domain', 'Data from Y source seems outdated', 'Would like to see Z benchmark added', etc."

#### Question 26: Any other comments or suggestions?
- **Type**: Long answer
- **Required**: No
- **Placeholder**: "Any additional feedback, ideas, or observations..."

---

### SECTION 5: Testimonial (Optional)

**Section Title**: Testimonial (Optional but Appreciated!)

**Section Description**:
```
If you found this testing valuable and the benchmarks useful, we'd love a testimonial!

Your testimonial helps us:
- Show social proof of quality
- Build trust with other users
- Document real user validation

You can choose to be quoted by name, title only, or anonymously.
```

---

#### Question 27: Would you recommend this tool to colleagues?
- **Type**: Multiple choice
- **Required**: No
- **Options**:
  - ✅ Yes, highly recommend
  - 👍 Yes, probably recommend
  - 🤔 Maybe, with some improvements
  - 👎 Probably not
  - ❌ No, would not recommend

#### Question 28: What would you tell a colleague about this tool?
- **Type**: Long answer
- **Required**: No
- **Placeholder**: "In 1-3 sentences, what would you say to a colleague asking about this tool?"

#### Question 29: Can we quote you in our documentation?
- **Type**: Multiple choice
- **Required**: No
- **Options**:
  - ✅ Yes, with my name and title
  - 👤 Yes, with title only (no name)
  - 🎭 Yes, but anonymously (no name or title)
  - ❌ No, please don't quote me

#### Question 30: Your testimonial (if you agree to be quoted)
- **Type**: Long answer
- **Required**: No
- **Placeholder**: "Write your testimonial here (1-3 sentences). Example: 'As an HR manager in Vietnam, I'm impressed by the quality and credibility of these salary benchmarks. All the URLs I tested actually worked, and the Vietnam-specific sources are spot-on. This is exactly what we need!'"

---

### SECTION 6: Thank You!

**Section Title**: Thank You! 🙏

**Final Message**:
```
Thank you for completing this feedback form!

Your honest feedback is incredibly valuable and helps us achieve perfect 10/10 quality.

** WHAT HAPPENS NEXT? **

1. We'll analyze feedback from all testers (targeting 5-10 total)
2. We'll fix any issues you and others discovered
3. You'll receive:
   - Aggregated findings summary
   - How your feedback improved the tool
   - Final 10/10 achievement announcement

** ESTIMATED TIMELINE **

- Your feedback: Received ✅
- Analysis: Within 24 hours
- Fixes: Within 48 hours
- Results summary: Within 72 hours

** WANT TO STAY CONNECTED? **

If you want to receive the final results or be part of our Vietnam user community, make sure you provided your email in Question 2.

** QUESTIONS? **

If you have any follow-up questions or want to discuss your feedback:
Email: [your_email@example.com]
LinkedIn: [Your LinkedIn profile]

Once again, **THANK YOU** for your time! Your 15 minutes = Our 10/10 quality! 🎯

---

Feel free to share this testing opportunity with other HR/Marketing/E-commerce professionals who might be interested!
```

---

## Form Configuration Tips

### Design Settings (Appearance)
- **Theme color**: Use brand colors or professional blue/green
- **Header image**: Optional - add your logo or project banner
- **Font**: Use clean, readable font (e.g., "Basic", "Formal", or "Playful")

### Response Settings
- ✅ **Collect email addresses**: Optional (set to "Off" for anonymity, "On" for follow-up)
- ✅ **Limit to 1 response**: No (allow users to edit if needed)
- ✅ **Allow response editing**: Yes (users can correct mistakes)
- ✅ **Response receipts**: Yes (send copy to respondent)
- ✅ **Show progress bar**: Yes (helps users see how much is left)

### Response Notifications
- ✅ **Email notifications**: Yes (get notified when someone submits)
- ✅ **Daily summary**: Optional (daily digest of responses)

### Response Validation
- Add validation for email field (must be valid email format)
- Add validation for short answer fields (minimum characters if needed)
- Make critical questions required (e.g., Q20-23)

---

## Analyzing Responses (Google Sheets Integration)

### Step 1: Link Form to Google Sheets
1. In Google Forms, click "Responses" tab
2. Click green Sheets icon "View responses in Sheets"
3. Create new spreadsheet or link to existing
4. All responses will automatically populate in real-time

### Step 2: Create Summary Tab
Create a separate tab in the spreadsheet with:

**Summary Statistics**:
- Total responses received
- Average rating per question (Q20-23)
- URL success rate (% of URLs that worked)
- Vietnam sources rating average
- Trust score average
- Would-use-tool breakdown (% Yes / Maybe / No)

**URL-Specific Stats**:
- For each benchmark URL:
  - Number of times tested
  - Success rate (% worked)
  - Average usefulness rating
  - Average credibility rating
  - Issues reported

**Testimonials Collection**:
- Extract all testimonials (Q30)
- Categorize by attribution (name, anonymous, etc.)
- Highlight best quotes for documentation

### Step 3: Visualizations
Create charts in Google Sheets:
- Bar chart: Overall quality rating distribution (Q20)
- Bar chart: Vietnam sources rating (Q21)
- Bar chart: Trust score distribution (Q22)
- Pie chart: Would-use-tool breakdown (Q23)
- Table: URL success rates (all 26 URLs)

---

## Success Criteria (from Responses)

### Minimum Requirements for 10/10 Score:

| Metric | Target | Formula |
|--------|--------|---------|
| **Total Responses** | 5+ | Count of submitted forms |
| **URL Success Rate** | 95%+ | (URLs that worked / Total URLs tested) × 100 |
| **Overall Quality** | 4.0+ / 5.0 | Average of Q20 responses |
| **Vietnam Sources** | 4.0+ / 5.0 | Average of Q21 responses |
| **Trust Score** | 4.5+ / 5.0 | Average of Q22 responses |
| **Would Use Tool** | 80%+ "Yes" | (Yes responses / Total) × 100 |
| **Testimonials** | 3+ | Count of Q30 responses with permission |

### Scoring Calculation:

**Current Score**: 9.85/10 (after Phase 2)

**Phase 3 Additions** (based on feedback):
- URL success rate 95%+: +0.05
- Overall quality 4.0+: +0.05
- Trust score 4.5+: +0.05

**Final Score**: 9.85 + 0.15 = **10.00/10** ✅

---

## Sample Data Analysis (Example)

### Example Results (5 Testers):

**Response Summary**:
- Total responses: 5
- Total URLs tested: 28 (average 5.6 URLs per tester)
- URLs with 100% success: 25/28 (89.3%)
- URLs with issues: 3/28 (10.7%)

**Rating Averages**:
- Overall quality (Q20): 4.2 / 5.0 ✅
- Vietnam sources (Q21): 4.6 / 5.0 ✅
- Trust score (Q22): 4.4 / 5.0 ⚠️ (just below target)
- Would use tool: 80% "Yes" ✅

**Issues Found**:
- 2 URLs had slow loading times (but worked)
- 1 URL had 403 error (but user verified it works in incognito)
- 0 URLs completely broken ✅

**Testimonials**: 4 testers provided testimonials (3 with names, 1 anonymous)

**Conclusion**: Achieved 9.95/10 (minor trust score issue to address, but overall excellent)

---

## Troubleshooting

### Issue: Low Response Rate
**Solution**:
- Send reminder email after 12 hours
- Extend deadline by 24 hours
- Offer incentive (if budget allows)
- Post on social media for broader reach

### Issue: Negative Feedback
**Solution**:
- Thank user for honesty
- Investigate reported issues immediately
- Fix broken URLs or replace with alternatives
- Follow up with user to verify fix

### Issue: Incomplete Responses
**Solution**:
- Follow up with user to complete
- Accept partial responses if they tested 3+ URLs
- Use "Not required" for optional questions

### Issue: Conflicting Feedback
**Solution**:
- Investigate discrepancies (e.g., URL works for some, broken for others)
- Test URLs yourself to verify
- Consider geographic/network differences (Vietnam vs international)
- Document both perspectives in report

---

## Next Steps

1. ✅ Create Google Form using structure above
2. ✅ Test the form yourself (fill it out to ensure it works)
3. ✅ Get shareable link
4. ✅ Include link in recruitment email
5. ✅ Monitor responses in real-time
6. ✅ Analyze data after 5+ responses received
7. ✅ Fix any issues discovered
8. ✅ Document results in Phase 3 Validation Report

**Ready to collect feedback and achieve 10/10!** 📊

---

**Generated**: 2025-10-29
**Phase**: 3 (User Validation)
**Tool**: Google Forms (free, easy, automatic data collection)
