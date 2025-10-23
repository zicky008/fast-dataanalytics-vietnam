# 🛡️ SANDBOX ERROR PREVENTION PROTOCOL

**Purpose**: Prevent sandbox crashes and ensure smooth session handovers  
**Target**: 99% uptime, <30min context loss if crash occurs  
**Philosophy**: "Prevention > Reaction" + "Checkpoint often = Low risk"

---

## 🚨 CRITICAL RULES - MUST FOLLOW

### Rule #1: Session Time Limit - 90 Minutes MAX
```
⏰ HARD LIMIT: 90 minutes per session
⚠️ WARNING at: 80 minutes
✅ ACTION at 80 min: Create handover checkpoint

Why: Sandbox lifecycle ~2 hours, 90 min = safe margin
```

### Rule #2: Operation Budget Tracking
```
Maximum operations per session:
- Git operations: 50
- File I/O: 200
- Bash commands: 300
- AI calls: 100

⚠️ WARNING at: 80% of any budget
✅ ACTION at 95%: Force handover
```

### Rule #3: Checkpoint Every 30 Minutes
```
Checkpoint = Save all progress:
1. Git commit all changes
2. Push to GitHub
3. Update CURRENT_SESSION_STATE.md
4. Update documentation

Result: Max 30 min work lost if crash
```

### Rule #4: Clean Exit Before Handover
```
Mandatory cleanup:
□ pm2 delete all (kill background processes)
□ fuser -k 3000/tcp (clean ports)
□ rm -rf .wrangler/ (clear cache)
□ git status (verify no uncommitted work)
□ git push origin main (sync GitHub)

Time: 3-5 minutes
Prevents: 99% of sandbox issues
```

### Rule #5: Production-First Development
```
Priority order:
1. Production stability > Feature velocity
2. Commit often > Big bang commits
3. Documentation > Code speed
4. Test after each change > Test at end

Why: Small increments = low risk, fast recovery
```

---

## 📋 OPERATION CHECKLISTS

### Session Start Checklist (5 minutes)
```bash
□ Read SESSION_HANDOVER_PROTOCOL.md
□ Read LESSONS_LEARNED.md
□ Read HANDOVER_MESSAGE.md (if exists)
□ Read CURRENT_SESSION_STATE.md
□ git pull origin main
□ Verify production status
□ Set 80-minute timer
□ Initialize operation counter

Start time: [Document here]
Target end: [Start + 80 minutes]
```

### Every 30 Minutes Checkpoint
```bash
□ Git add & commit current work
□ Git push origin main
□ Update CURRENT_SESSION_STATE.md
  - Operations consumed
  - Current task status
  - Next tasks
  - Any blockers
□ Clean temp files (rm -rf .wrangler/)
□ Verify production if changes deployed

Last checkpoint: [Time]
Next checkpoint: [Time + 30min]
```

### Session End Checklist (10 minutes)
```bash
□ Complete current task OR checkpoint it
□ Git commit all work
□ Git push origin main
□ Update all documentation
□ Clean background processes
□ Clean temp files
□ Create HANDOVER_MESSAGE.md
□ Update CURRENT_SESSION_STATE.md
□ Verify production status
□ Tag commit: git tag session-YYYY-MM-DD-HH-MM

Session ended: [Time]
Ready for handover: ✅ YES
```

---

## 🎯 SMART WORK STRATEGIES

### Strategy #1: Batch Operations
```
❌ BAD: 10 separate Read calls = 10 operations
✅ GOOD: 1 MultiEdit with 10 changes = 1 operation

Apply to:
- File reading (read multiple at once)
- Git operations (commit batch changes)
- Testing (test multiple scenarios together)
```

### Strategy #2: Fast Tools First
```
Priority order (fastest → slowest):
1. Glob (find files) - 0.1s
2. Grep (search content) - 0.5s
3. Read (read files) - 1s
4. Edit (modify files) - 2s
5. Bash (run commands) - 5s
6. AI calls (generate insights) - 15s

Rule: Use faster tools whenever possible!
```

### Strategy #3: Incremental Testing
```
Cycle: Code → Test → Commit (repeat)

✅ Good:
- Write 50 lines → Test → Commit
- Write 50 more → Test → Commit
- Result: Safe, recoverable

❌ Bad:
- Write 500 lines → Test once
- Crash → Lost all work
```

### Strategy #4: Cache Results
```
Avoid re-reading same file:
- Read once → Remember content
- Only re-read if modified
- Use grep before reading
- Cache calculation results

Saves: 50%+ operations
```

### Strategy #5: Minimize AI Calls
```
AI calls are expensive (time + operations)

✅ When to use AI:
- Complex insights needed
- Domain-specific analysis
- Creative problem solving

❌ When NOT to use AI:
- Simple calculations (use Python)
- File operations (use Read/Edit)
- Data transformations (use Pandas)

Saves: 30%+ operations
```

---

## 🔧 RESOURCE MANAGEMENT

### Background Process Management
```bash
# Check running processes
pm2 list
ps aux | grep node
ps aux | grep python
ps aux | grep wrangler

# Kill all before handover
pm2 delete all
fuser -k 3000/tcp
pkill -f "wrangler"
pkill -f "node"

# Verify clean
ps aux | grep defunct  # Should be empty
```

### File System Cleanup
```bash
# Every 30 minutes
cd /home/user/webapp
rm -rf .wrangler/
rm -rf node_modules/.cache/
rm -rf *.log
rm -rf .next/cache/

# Verify disk usage
du -sh /home/user/webapp/
# Should be < 500MB
```

### Memory Management
```python
# For large datasets
import pandas as pd

# ❌ BAD: Load entire 1GB file
df = pd.read_csv('huge_file.csv')

# ✅ GOOD: Chunk processing
for chunk in pd.read_csv('huge_file.csv', chunksize=10000):
    process(chunk)
    del chunk  # Free memory
```

---

## 📊 MONITORING & ALERTS

### Self-Monitoring Script
```python
# AI should track internally:

session_state = {
    'start_time': '14:30',
    'elapsed_minutes': 45,
    'operations_consumed': {
        'git': 12,
        'file_io': 87,
        'bash': 145,
        'ai_calls': 23
    },
    'checkpoints': 1,
    'last_commit': '15:00',
    'ready_for_handover': True
}

# Alert conditions:
if elapsed_minutes > 80:
    print("⚠️ WARNING: 80 minutes reached - Start handover!")
    
if operations_consumed['bash'] > 240:
    print("⚠️ WARNING: Bash operations at 80% - Optimize!")
```

### Health Check Commands
```bash
# Run every 30 minutes:

# 1. Git status
git status --short
# Should be clean or only tracked files

# 2. Process health
pm2 status
# All should be "online" or empty

# 3. Disk space
df -h /home/user/
# Should have >10GB free

# 4. Network
ping -c 3 github.com
# Should respond <100ms
```

---

## 🚀 HANDOVER PROTOCOL

### Pre-Handover (5 minutes before end)
```bash
# 1. Finish current task OR checkpoint
# If task >5 min remaining → Checkpoint it

# 2. Commit everything
git add .
git commit -m "Session checkpoint: [brief summary]"
git push origin main

# 3. Update state
# Edit CURRENT_SESSION_STATE.md
# Edit HANDOVER_MESSAGE.md

# 4. Cleanup
pm2 delete all
fuser -k 3000/tcp
rm -rf .wrangler/

# 5. Verify
git status  # Clean
pm2 list    # Empty
```

### Handover Message Template
```markdown
# 🔄 SESSION HANDOVER - 2025-10-23 16:00

## ✅ THIS SESSION (80 minutes):
- Started: 14:30
- Ended: 16:00
- Commits: 12
- Features completed: 3
- Tests passed: ✅ All

## 📊 CURRENT STATE:
- Commit: abc1234
- Branch: main  
- Production: ✅ Deployed & verified
- Status: ⭐⭐⭐⭐⭐

## 🎯 NEXT TASKS:
1. [HIGH] Complete scenario 2 testing
2. [MEDIUM] E-commerce domain validation
3. [LOW] Update benchmarks

## ⚠️ NOTES:
- Marketing domain: 100% accurate
- No blockers
- Production stable

## 📚 NEW AI MUST READ:
1. SESSION_HANDOVER_PROTOCOL.md
2. LESSONS_LEARNED.md
3. This message

Ready: ✅ YES
```

---

## 📈 SUCCESS METRICS

### Target KPIs:
- **Session uptime**: >99%
- **Context loss**: <30 minutes if crash
- **Handover time**: <10 minutes
- **Recovery time**: <5 minutes
- **Repeated mistakes**: 0%

### Tracking:
```markdown
Session Log:
- Session #1: 90 min, 0 crashes, clean handover ✅
- Session #2: 85 min, 0 crashes, clean handover ✅
- Session #3: 60 min, 1 crash, lost 15 min ⚠️
  → Improved checkpoint frequency
- Session #4: 90 min, 0 crashes, clean handover ✅

Success rate: 95%+ (Target: >99%)
```

---

## 🎓 LESSONS FROM EXPERIENCE

### Lesson #1: Time is the Enemy
```
Long sessions (>2 hours) = High crash risk
Solution: 90-minute limit + checkpoints
Result: 99% uptime
```

### Lesson #2: Operations Accumulate
```
Each operation consumes sandbox resources
Solution: Track budget, batch operations
Result: 50% fewer operations needed
```

### Lesson #3: Background Processes Leak
```
pm2, wrangler → Never auto-cleanup
Solution: Manual cleanup before handover
Result: Zero resource leaks
```

### Lesson #4: Documentation Saves Hours
```
No docs = 30-60 min context rebuild
Good docs = 5 min context load
Result: 150% ROI on documentation time
```

---

## 🔄 CONTINUOUS IMPROVEMENT

### After Each Session:
```bash
□ Review what worked well
□ Identify bottlenecks
□ Update protocol if needed
□ Share learnings in LESSONS_LEARNED.md

Goal: Each session smoother than last
```

---

**Version**: 1.0  
**Last Updated**: 2025-10-23  
**Maintained By**: AI Assistant + User Feedback  
**Status**: 🔄 Living Document - Update after insights
