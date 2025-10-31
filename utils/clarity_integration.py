#!/usr/bin/env python3
"""
Microsoft Clarity Integration
FREE forever, UNLIMITED sessions (better than Hotjar)

Why Clarity > Hotjar:
- FREE with unlimited sessions (vs Hotjar's 35/day limit)
- AI-powered insights
- Better performance (faster loading)
- Microsoft trust & reliability
- More advanced filters

Setup time: 5 minutes
"""

def generate_clarity_code(project_id: str) -> str:
    """
    Generate Microsoft Clarity tracking code
    
    Args:
        project_id: Your Clarity project ID (from dashboard)
        
    Returns:
        HTML tracking code to inject into Streamlit
    """
    return f"""
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){{
        c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "{project_id}");
</script>
"""


CLARITY_SETUP_GUIDE = """
================================================================================
🔍 MICROSOFT CLARITY SETUP - FREE UNLIMITED USER TESTING
================================================================================

WHY CLARITY IS BETTER THAN HOTJAR:
-----------------------------------
✅ Unlimited sessions (vs Hotjar's 35/day)
✅ 100% FREE forever (no credit card needed)
✅ AI-powered insights (automatic issue detection)
✅ Better performance (faster than Hotjar)
✅ Microsoft trust & security
✅ More advanced filtering
✅ Better mobile support
✅ No session limits, no page view limits

STEP 1: SIGN UP (2 minutes)
----------------------------
1. Go to https://clarity.microsoft.com
2. Click "Sign up" (use Microsoft, Google, or GitHub account)
3. No credit card needed!
4. Email verification

STEP 2: CREATE PROJECT (1 minute)
----------------------------------
1. Click "New Project"
2. Enter project name: "Fast Data Analytics Vietnam"
3. Enter website URL: your-app.streamlit.app
4. Click "Create"
5. Copy your Project ID (shown immediately)

STEP 3: GET TRACKING CODE (30 seconds)
---------------------------------------
1. After creating project, you'll see tracking code
2. Copy the entire <script> tag
3. Or use: clarity_integration.py to generate it

STEP 4: ADD TO STREAMLIT (2 minutes)
-------------------------------------
Option A: Direct code (quick)
```python
# Add to streamlit_app.py, right after st.set_page_config()

import streamlit as st

st.set_page_config(...)

# Microsoft Clarity tracking
clarity_code = '''
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "YOUR_PROJECT_ID");
</script>
'''
st.markdown(clarity_code, unsafe_allow_html=True)
```

Option B: Using helper function
```python
from utils.clarity_integration import generate_clarity_code

clarity_code = generate_clarity_code("YOUR_PROJECT_ID")
st.markdown(clarity_code, unsafe_allow_html=True)
```

5. Replace YOUR_PROJECT_ID with actual ID (e.g., "k9x5m2p8q1")
6. Commit & deploy to production

STEP 5: VERIFY (1 minute)
--------------------------
1. Visit your production app
2. Perform a few actions (click, scroll, navigate)
3. Go back to Clarity dashboard
4. Wait 2-3 minutes (processing time)
5. Check "Dashboard" → Should see "Sessions: 1+"
6. If yes → ✅ Working perfectly!

================================================================================
📊 WHAT YOU GET (100% FREE FOREVER)
================================================================================

✅ SESSION RECORDINGS (UNLIMITED):
   • Watch every user session
   • See exact mouse movements
   • Identify click patterns
   • Spot confusion points
   • Filter by device, country, duration

✅ HEATMAPS (UNLIMITED):
   • Click heatmap (where users click most)
   • Scroll heatmap (how far they scroll)
   • Area heatmap (attention zones)
   • Aggregated data over time

✅ AI-POWERED INSIGHTS:
   • Rage clicks (frustrated users) 🔴
   • Dead clicks (clicking non-interactive elements) 🟠
   • Excessive scrolling (confusion) 🟡
   • Quick backs (immediate exits) 🔵
   • JavaScript errors (bugs) 🐛

✅ ADVANCED FILTERING:
   • By device (mobile, tablet, desktop)
   • By browser (Chrome, Safari, Firefox)
   • By country (Vietnam, US, etc.)
   • By duration (>1 min, >2 min, etc.)
   • By page URL
   • Custom segments

✅ CONVERSION FUNNELS:
   • Track multi-step processes
   • Identify drop-off points
   • Optimize conversion paths

================================================================================
🎯 DAILY ANALYSIS ROUTINE (10 minutes)
================================================================================

MORNING CHECK (5 min):
1. Open Clarity dashboard
2. Check "Insights" tab
3. Review:
   • Rage clicks: Target 0 🎯
   • Dead clicks: Target <5 🎯
   • JavaScript errors: Target 0 🎯
   • Quick backs: Target <10% 🎯

4. If issues found → Note them
5. Priority: Fix rage clicks first (highest frustration)

EVENING REVIEW (5 min):
1. Go to "Recordings" tab
2. Filter:
   • Country: Vietnam
   • Duration: >1 minute
   • Date: Today

3. Watch 2-3 sessions (2x speed)
4. Note:
   • Where users hesitate
   • What they click repeatedly
   • Where they give up
   • Navigation patterns

5. Tag important sessions for team review

================================================================================
📈 KEY METRICS TO TRACK
================================================================================

ENGAGEMENT METRICS:
1. Session Duration
   • Excellent: >3 minutes 🟢
   • Good: 1-3 minutes 🟡
   • Poor: <1 minute 🔴
   • Target: >2 minutes ✅

2. Pages per Session
   • Excellent: 4+ pages 🟢
   • Good: 2-3 pages 🟡
   • Poor: 1 page 🔴
   • Target: 3+ pages ✅

3. Scroll Depth
   • Excellent: 75%+ 🟢
   • Good: 50-75% 🟡
   • Poor: <50% 🔴
   • Target: 60%+ ✅

FRUSTRATION METRICS:
1. Rage Clicks (user frustration)
   • Excellent: 0 🟢
   • Acceptable: 1-2 🟡
   • Problem: 3+ 🔴
   • Target: 0 ✅

2. Dead Clicks (confusion)
   • Excellent: 0 🟢
   • Acceptable: 1-3 🟡
   • Problem: 4+ 🔴
   • Target: <2 ✅

3. Excessive Scrolling
   • Excellent: 0 🟢
   • Acceptable: 1-2 🟡
   • Problem: 3+ 🔴
   • Target: 0 ✅

4. Quick Backs (<10s)
   • Excellent: <5% 🟢
   • Acceptable: 5-15% 🟡
   • Problem: >15% 🔴
   • Target: <10% ✅

TECHNICAL METRICS:
1. JavaScript Errors
   • Target: 0 errors ✅
   • If >0 → Fix immediately 🚨

2. Page Load Time
   • Excellent: <2s 🟢
   • Good: 2-4s 🟡
   • Poor: >4s 🔴
   • Target: <3s ✅

================================================================================
🔍 HOW TO USE INSIGHTS
================================================================================

RAGE CLICKS ANALYSIS:
1. Dashboard → "Insights" → "Rage clicks"
2. Click on any session
3. Watch the recording
4. Identify the element causing frustration
5. Common causes:
   • Button not working (disabled state)
   • Slow response (no loading indicator)
   • Confusing label (unclear action)
   • Hidden element (user expects interaction)

6. Fix:
   • Add loading spinners
   • Make buttons more obvious
   • Improve labeling
   • Show feedback on click

DEAD CLICKS ANALYSIS:
1. Dashboard → "Insights" → "Dead clicks"
2. See which non-interactive elements users click
3. Common examples:
   • Text that looks like a link (but isn't)
   • Disabled buttons (user doesn't know why)
   • Images (user expects them clickable)

4. Fix:
   • Make real links blue + underlined
   • Show tooltips on disabled buttons
   • Make images clickable if relevant

EXCESSIVE SCROLLING:
1. Dashboard → "Insights" → "Excessive scrolling"
2. Watch sessions
3. Identify why:
   • Looking for specific content (not found)
   • Navigation unclear
   • Content buried too deep

4. Fix:
   • Add search functionality
   • Improve navigation
   • Use progressive disclosure (our Day 3-4 task!)

QUICK BACKS:
1. Dashboard → "Insights" → "Quick backs"
2. See users who leave <10 seconds
3. Identify first page they see
4. Common causes:
   • Slow loading
   • Confusing landing page
   • Wrong expectations

5. Fix:
   • Optimize performance
   • Improve hero section
   • Clear value proposition

================================================================================
💡 PRO TIPS
================================================================================

1. FOCUS ON VIETNAMESE USERS:
   Filter → Country → Vietnam
   This ensures you're seeing relevant behavior

2. WATCH FULL SESSIONS (not just problem ones):
   • 70% normal sessions: Understand typical usage
   • 30% problem sessions: Fix issues

3. USE SEGMENTS:
   Create custom segments:
   • "Engaged users" (>2 min, 3+ pages)
   • "Frustrated users" (rage clicks + quick back)
   • "Mobile users" (device = mobile)
   • "First-time visitors" (new users)

4. TAG IMPORTANT SESSIONS:
   • Add tags like "bug", "ux-issue", "good-flow"
   • Share with team
   • Track improvements

5. COMBINE WITH LIGHTHOUSE:
   • Clarity: Shows WHAT users do (behavior)
   • Lighthouse: Shows WHY it's slow (technical)
   • Together: Complete picture!

6. WEEKLY HEATMAP REVIEW:
   • Monday: Generate heatmap for last 7 days
   • Identify:
     - Hot zones (high engagement) ✅
     - Cold zones (ignored content) ⚠️
     - Unexpected clicks (confusion) 🔴
   • Adjust layout based on data

7. A/B TEST WITH CLARITY:
   • Make change (e.g., button color)
   • Watch 10 sessions
   • Compare metrics before/after
   • Data-driven decisions!

================================================================================
⚠️  PRIVACY & COMPLIANCE
================================================================================

✅ GDPR Compliant:
   - Clarity is GDPR compliant
   - No PII collected
   - Users can opt-out

✅ Add Privacy Notice:
   "We use Microsoft Clarity to analyze anonymous user behavior
    and improve your experience. No personal information is collected."

✅ Update Privacy Policy:
   "Analytics: We use Microsoft Clarity (clarity.microsoft.com)
    to collect anonymous usage data for UX improvement purposes."

================================================================================
🎯 EXPECTED INSIGHTS (Week 1)
================================================================================

After 1 week with Clarity, you'll discover:

✅ Top 3 UX issues (based on rage clicks)
✅ Most confusing page sections (based on dead clicks)
✅ Mobile vs desktop behavior differences
✅ Which features users love (high engagement)
✅ Which features users ignore (cold zones)
✅ Optimal navigation patterns
✅ Vietnamese-specific UX preferences

This data = GOLD for 5-star UX! 🌟

================================================================================
🚀 NEXT STEPS
================================================================================

1. Sign up now: https://clarity.microsoft.com (2 min)
2. Create project (1 min)
3. Add tracking code to streamlit_app.py (2 min)
4. Deploy (5 min)
5. Wait 24 hours for data
6. Start analyzing! (10 min/day)

TOTAL SETUP: <10 MINUTES
DAILY MAINTENANCE: 10 MINUTES
COST: ₫0 FOREVER

🎉 UNLIMITED FREE USER TESTING FOR LIFE!

================================================================================
"""


def print_clarity_guide():
    """Print Microsoft Clarity setup guide"""
    print(CLARITY_SETUP_GUIDE)


if __name__ == "__main__":
    print_clarity_guide()
