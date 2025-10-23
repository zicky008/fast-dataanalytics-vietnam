# 🚀 START NEW SESSION - Quick Guide

**For User**: Copy-paste này vào chat đầu session mới để AI load context nhanh nhất

📁 **File Location**: All files ở `/home/user/webapp/`

---

## 📋 TEMPLATE FOR USER

```
Chào AI! Session mới bắt đầu.

Trước khi làm việc, hãy đọc theo thứ tự:
(All files ở /home/user/webapp/)

1. SESSION_HANDOVER_PROTOCOL.md (workflow guide)
2. PRODUCTION_INFO.md (current state)
3. LESSONS_LEARNED.md (past mistakes & rules)
4. COMPLETION_SUMMARY_2025-10-22.md (recent work)

Sau khi đọc xong, confirm context bằng cách trả lời:
- Production URL là gì?
- 3 lessons quan trọng nhất?
- Current status như thế nào?
- Pending tasks gì?

Hôm nay tôi cần: [MÔ TẢ TASK]
```

---

## ⚡ ULTRA-FAST VERSION (1 dòng)

```
Đọc SESSION_HANDOVER_PROTOCOL.md, PRODUCTION_INFO.md, LESSONS_LEARNED.md rồi [TASK]
```

---

## 🎯 AI RESPONSE TEMPLATE

After reading, AI should respond:

```
✅ Context loaded!

📍 Production: https://fast-nicedashboard.streamlit.app/
🔧 Tech: Streamlit + Google Gemini AI
📊 Status: 5-star quality, all critical bugs fixed

📚 Key Lessons Reviewed:
1. Debug code must be removed before commit
2. Verify production URLs in all docs
3. Careful screenshot validation

🎯 Current State:
- All 9 KPIs displaying correctly
- Badge colors working (higher/lower logic)
- No debug code visible to users
- Professional UI maintained

⏳ Pending Tasks:
- Bug #2: OEE Chart Y-Axis (medium priority)
- Bug #4: Domain-specific benchmarks (low priority)

Tôi đã sẵn sàng [TASK]. Có gì cần clarify không?
```

---

## 🔄 WORKFLOW REMINDER

### AI Should Follow:
1. ✅ Read mandatory files (5-10 min)
2. ✅ Confirm context loaded
3. ✅ Execute task with context
4. ✅ Apply prevention rules
5. ✅ Document new lessons if any

### User Should:
1. ✅ Provide clear task description
2. ✅ Give feedback on AI understanding
3. ✅ Point out missed context
4. ✅ Verify quality maintained

---

## 📚 FILE HIERARCHY (Quick Ref)

```
Must Read (Tier 1):
├── SESSION_HANDOVER_PROTOCOL.md   ← Master workflow
├── PRODUCTION_INFO.md             ← Current state
├── LESSONS_LEARNED.md             ← Past mistakes
└── COMPLETION_SUMMARY_*.md        ← Recent work

Should Read (Tier 2):
├── README.md                      ← Project overview
└── BUG_FIX_*.md                  ← Specific fixes

Read When Coding (Tier 3):
├── streamlit_app.py              ← Main UI
├── src/premium_lean_pipeline.py  ← Core logic
└── requirements.txt               ← Dependencies
```

---

## ⚠️ CRITICAL RULES (Always Apply)

```bash
# 1. Check debug code before commit
grep -rn "🐛\|DEBUG" . --include="*.py"

# 2. Use correct production URL
https://fast-nicedashboard.streamlit.app/

# 3. Maintain quality standards
- Data accuracy: 100%
- User experience: 5-star
- No debug visible to users

# 4. Git workflow
git add . && git commit -m "Clear message" && git push origin main

# 5. User feedback = Priority #1
```

---

## 💡 TIPS

### For Faster Start:
- Keep this file open in browser
- Copy template at session start
- AI will load context automatically

### For Better Results:
- Be specific about task
- Mention if it's related to previous work
- Point out relevant lessons if you know

### For Quality:
- Verify AI confirms context
- Check AI applies lessons
- Provide feedback on outputs

---

**Created**: 2025-10-22  
**Purpose**: Fastest way to start new sessions with full context  
**Saves**: ~5 minutes of explanation every session  
**Result**: Zero context loss, consistent quality
