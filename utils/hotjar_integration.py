#!/usr/bin/env python3
"""
Hotjar Integration for Real User Testing
Free plan: 35 daily sessions, heatmaps, recordings

Setup:
1. Sign up at https://www.hotjar.com (FREE)
2. Get tracking code
3. Add to Streamlit app
4. Analyze user behavior

Features (Free):
- Session recordings (35/day)
- Heatmaps (unlimited)
- Conversion funnels
- Form analysis
- Feedback polls
"""

HOTJAR_INTEGRATION_CODE = """
<!-- Hotjar Tracking Code -->
<script>
    (function(h,o,t,j,a,r){
        h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
        h._hjSettings={hjid:YOUR_HOTJAR_ID,hjsv:6};
        a=o.getElementsByTagName('head')[0];
        r=o.createElement('script');r.async=1;
        r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
        a.appendChild(r);
    })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
</script>
"""

def generate_hotjar_code(site_id: str) -> str:
    """
    Generate Hotjar tracking code
    
    Args:
        site_id: Your Hotjar site ID (from dashboard)
        
    Returns:
        HTML tracking code to inject
    """
    return f"""
<script>
    (function(h,o,t,j,a,r){{
        h.hj=h.hj||function(){{(h.hj.q=h.hj.q||[]).push(arguments)}};
        h._hjSettings={{hjid:{site_id},hjsv:6}};
        a=o.getElementsByTagName('head')[0];
        r=o.createElement('script');r.async=1;
        r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
        a.appendChild(r);
    }})(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
</script>
"""


HOTJAR_SETUP_GUIDE = """
================================================================================
🔥 HOTJAR SETUP GUIDE - FREE REAL USER TESTING
================================================================================

STEP 1: SIGN UP (2 minutes)
----------------------------
1. Go to https://www.hotjar.com
2. Click "Sign up for free"
3. Choose "Basic" plan (₫0 - FREE forever)
4. Enter email + password
5. Verify email

STEP 2: CREATE SITE (1 minute)
-------------------------------
1. Click "Add new site"
2. Enter your Streamlit app URL
3. Copy your Site ID (e.g., 1234567)

STEP 3: GET TRACKING CODE (30 seconds)
---------------------------------------
1. Dashboard → Settings → Sites & Organizations
2. Click your site
3. Copy tracking code

STEP 4: ADD TO STREAMLIT (2 minutes)
-------------------------------------
1. Open streamlit_app.py
2. Add after st.set_page_config():

   ```python
   # Hotjar tracking
   hotjar_code = '''
   <script>
       (function(h,o,t,j,a,r){
           h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
           h._hjSettings={hjid:YOUR_SITE_ID,hjsv:6};
           a=o.getElementsByTagName('head')[0];
           r=o.createElement('script');r.async=1;
           r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
           a.appendChild(r);
       })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
   </script>
   '''
   st.markdown(hotjar_code, unsafe_allow_html=True)
   ```

3. Replace YOUR_SITE_ID with actual ID
4. Deploy to production

STEP 5: VERIFY (1 minute)
--------------------------
1. Visit your production app
2. Go to Hotjar dashboard
3. Wait 2-3 minutes
4. Check "Recordings" → Should see "1 recording available"
5. If yes → ✅ Working!

================================================================================
📊 WHAT YOU GET (FREE PLAN)
================================================================================

✅ Session Recordings (35/day):
   • Watch real users navigate your app
   • See exactly where they click
   • Identify confusion points
   • Spot UI/UX issues

✅ Heatmaps (Unlimited):
   • Click heatmap (where users click most)
   • Move heatmap (where mouse moves)
   • Scroll heatmap (how far users scroll)
   • Visual representation of engagement

✅ Conversion Funnels:
   • Track user journey step-by-step
   • Identify drop-off points
   • Optimize conversion path

✅ Feedback Polls:
   • Ask users questions on-page
   • NPS surveys
   • Quick feedback widgets

✅ Form Analysis:
   • See which fields users struggle with
   • Identify abandoned forms
   • Optimize form UX

================================================================================
🎯 HOW TO ANALYZE (10 minutes/day)
================================================================================

DAILY ROUTINE:
1. Check Recordings (5 min):
   • Watch 2-3 sessions
   • Note confusion points
   • Look for rage clicks (repeated clicks)
   • Identify navigation issues

2. Review Heatmaps (3 min):
   • Check click concentration
   • Verify important CTAs get clicks
   • Identify dead zones

3. Check Funnels (2 min):
   • Monitor drop-off rates
   • Identify bottlenecks
   • Track improvements

WEEKLY ANALYSIS:
• Aggregate insights
• Prioritize fixes
• Implement improvements
• Measure impact

================================================================================
🔍 KEY METRICS TO TRACK
================================================================================

1. Session Duration:
   • Target: >2 minutes (engaged users)
   • Red flag: <30 seconds (bouncing)

2. Pages per Session:
   • Target: 3+ pages (exploring)
   • Red flag: 1 page (immediate exit)

3. Rage Clicks:
   • Target: 0
   • Red flag: Multiple (user frustrated)

4. Dead Clicks:
   • Target: 0
   • Red flag: Users clicking non-interactive elements

5. Error Clicks:
   • Target: 0
   • Red flag: Users clicking error messages repeatedly

6. Form Abandonment:
   • Target: <20%
   • Red flag: >50% (form too complex)

================================================================================
💡 PRO TIPS (Free Plan Optimization)
================================================================================

1. FOCUS ON CRITICAL PAGES:
   • Set up recordings on key pages only
   • Don't waste 35 sessions on every page

2. USE FILTERS:
   • Filter by device (mobile vs desktop)
   • Filter by country (Vietnam only)
   • Filter by duration (>1 minute only)

3. TAG IMPORTANT SESSIONS:
   • Tag sessions with issues
   • Add notes for follow-up
   • Share with team

4. COMBINE WITH LIGHTHOUSE:
   • Hotjar shows WHAT users do
   • Lighthouse shows WHY it's slow
   • Together = complete picture

5. SCHEDULE WEEKLY REVIEWS:
   • Monday: Review last week
   • Wednesday: Check progress
   • Friday: Plan next week

================================================================================
⚠️  PRIVACY & GDPR COMPLIANCE
================================================================================

✅ Hotjar is GDPR compliant
✅ No personal data collected (unless in forms)
✅ Users can opt-out
✅ Add privacy notice to your app:

   "We use Hotjar to understand how you use our app and improve your experience.
    Hotjar may record your session. No personal data is collected."

Add to Privacy Policy:
   "Analytics: We use Hotjar (hotjar.com) to collect anonymous usage data."

================================================================================
🎯 EXPECTED INSIGHTS (Within 1 week)
================================================================================

You'll discover:
✅ Where users get confused (watch them struggle)
✅ Which features are never used (dead zones)
✅ What causes users to leave (drop-off points)
✅ Mobile vs desktop behavior differences
✅ Vietnamese-specific UX issues

This data is GOLD for reaching 5-star UX! 🌟

================================================================================
"""


def print_hotjar_guide():
    """Print Hotjar setup guide"""
    print(HOTJAR_SETUP_GUIDE)


if __name__ == "__main__":
    print_hotjar_guide()
