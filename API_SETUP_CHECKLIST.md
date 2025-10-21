# ✅ API Setup Checklist - Gemini API Key

## 🎯 Mục Đích

Để test **Premium Lean Pipeline** với **Real Gemini API**, bạn cần:
1. ✅ Gemini API Key (miễn phí)
2. ✅ Setup trong file `.env`
3. ✅ Run test script

---

## 📋 Step-by-Step Checklist

### ☐ Step 1: Get Gemini API Key (2 phút)

1. Truy cập: https://aistudio.google.com/app/apikey
2. Đăng nhập bằng Google Account
3. Click **"Create API Key"**
4. Click **"Create API key in new project"** (hoặc chọn project có sẵn)
5. Copy API key (dạng: `AIzaSyAbc123...`)

**Screenshot:**
```
┌─────────────────────────────────────────┐
│ Google AI Studio                        │
├─────────────────────────────────────────┤
│                                         │
│  [Create API Key in New Project]       │
│                                         │
│  Your API Key:                          │
│  AIzaSyAbc123def456ghi789...           │
│  [Copy] [Regenerate]                   │
│                                         │
│  ⚠️  Keep your API key secure          │
│                                         │
└─────────────────────────────────────────┘
```

**Free Tier Limits:**
- ✅ 15 requests/minute
- ✅ 1,500 requests/day
- ✅ Không cần thẻ tín dụng

---

### ☐ Step 2: Create .env File (1 phút)

```bash
# Trong thư mục webapp/
cd webapp

# Copy template
cp .env.template .env

# Edit file .env
nano .env
# hoặc dùng editor bất kỳ (VS Code, Sublime, etc.)
```

**File `.env` sau khi sửa:**
```bash
# DataAnalytics Vietnam - Environment Variables Template
# Copy this file to .env and fill in your actual values

# ============================================
# GOOGLE GEMINI API KEY (REQUIRED)
# ============================================
GEMINI_API_KEY=AIzaSyAbc123def456ghi789jkl...  # <-- Paste API key ở đây

# ============================================
# OPTIONAL SETTINGS
# ============================================
APP_TITLE="DataAnalytics Vietnam"
APP_VERSION="1.0.0"
APP_ENV="development"
```

**⚠️  Lưu ý:**
- Không có khoảng trắng trước/sau `=`
- Không có dấu ngoặc kép quanh API key
- Không commit file `.env` lên Git (đã có trong .gitignore)

---

### ☐ Step 3: Verify Setup (30 giây)

```bash
# Check file .env tồn tại
ls -la .env

# Check nội dung (KHÔNG share output này!)
cat .env | grep GEMINI_API_KEY

# Kết quả mong đợi:
# GEMINI_API_KEY=AIzaSy...
```

---

### ☐ Step 4: Run Test Script (3 phút)

```bash
# Activate virtual environment (nếu chưa)
source venv/bin/activate  # Mac/Linux
# hoặc: venv\Scripts\activate  # Windows

# Run test
python test_real_api.py
```

**Expected Output:**
```
🧪 DataAnalytics Vietnam - Real API Testing
============================================================

TEST 1: Gemini API Connection
============================================================
✅ API Key found: AIzaSyAbc123...xyz
✅ API Response: OK
✅ PASSED: Gemini API connection successful

TEST 2: Marketing Pipeline (Google Ads)
============================================================
📁 Loading: marketing_google_ads.csv
✅ Data loaded: 21 rows × 7 columns

⏱️  Starting pipeline...
✅ Pipeline completed in 52.3 seconds

📊 Validation Results:
------------------------------------------------------------
✅ Status: success
✅ Domain: Marketing / Quảng Cáo
✅ Quality Score: 87.5/100
✅ Charts Generated: 9
✅ Insights Generated: 6

⏱️  Performance:
   - Total Time: 52.3s
   - Target: <60s
   ✅ Within target (7.7s buffer)

✅ PASSED: Marketing Pipeline Test

[... more tests ...]

📊 TEST SUMMARY
============================================================
✅ PASSED: Gemini Connection
✅ PASSED: Marketing Pipeline
✅ PASSED: E-commerce Pipeline
✅ PASSED: Rate Limiting

Total: 4/4 tests passed

🎉 ALL TESTS PASSED! Pipeline is ready for deployment.
```

---

## ❌ Common Errors & Fixes

### Error 1: "GEMINI_API_KEY not found in .env"

**Nguyên nhân:** File `.env` chưa được tạo

**Fix:**
```bash
# Copy template
cp .env.template .env

# Edit và thêm API key
nano .env
```

---

### Error 2: "Invalid API key format"

**Output:**
```
❌ FAILED: Invalid API key format (should start with 'AIza')
Current: your_gemini_api_key_here...
```

**Nguyên nhân:** Chưa thay placeholder bằng API key thật

**Fix:**
1. Lấy API key mới từ: https://aistudio.google.com/app/apikey
2. Copy EXACTLY (không có khoảng trắng)
3. Paste vào `.env`:
   ```bash
   GEMINI_API_KEY=AIzaSyAbc123...
   ```

---

### Error 3: "API_KEY_INVALID"

**Output:**
```
❌ FAILED: google.api_core.exceptions.PermissionDenied: 403 API_KEY_INVALID
```

**Nguyên nhân:** 
- API key đã bị revoke
- API key bị typo khi paste
- API key từ wrong project

**Fix:**
1. Vào https://aistudio.google.com/app/apikey
2. Check API key còn active không
3. Nếu không, regenerate key mới
4. Update trong `.env`

---

### Error 4: "429 Rate Limit Exceeded"

**Output:**
```
⏳ Gemini API đang bận, chờ 4s...
```

**Nguyên nhân:** Vượt quá 15 requests/minute

**Fix:**
- ✅ Hệ thống tự retry (2s → 4s → 8s)
- ✅ Nếu liên tục, đợi 1 phút
- ✅ Monitor usage: https://aistudio.google.com/app/apikey

---

### Error 5: "ModuleNotFoundError"

**Output:**
```
ModuleNotFoundError: No module named 'google.generativeai'
```

**Nguyên nhân:** Dependencies chưa được cài

**Fix:**
```bash
# Check virtual env activated
which python  # Should be venv/bin/python

# Install dependencies
pip install -r requirements.txt

# Verify
pip list | grep google-generativeai
```

---

## 🎯 Success Criteria

Sau khi complete checklist, bạn sẽ có:

- [x] ✅ Gemini API Key (miễn phí)
- [x] ✅ File `.env` với valid API key
- [x] ✅ Test script chạy thành công (4/4 tests passed)
- [x] ✅ Pipeline performance <60s
- [x] ✅ Quality Score ≥80/100
- [x] ✅ Ready for deployment

---

## 📞 Cần Hỗ Trợ?

**Nếu gặp vấn đề:**
1. Đọc [TESTING.md](TESTING.md) để troubleshooting chi tiết
2. Check GitHub Issues: [Link]
3. Email: support@dataanalytics.vn

**Nếu thành công:**
1. ✅ Mark Task #6 as completed
2. ⏭️  Tiếp tục Task #7: Performance Optimization
3. 🚀 Deploy to Streamlit Cloud (Task #8)

---

## 🔐 Security Reminders

**⚠️  QUAN TRỌNG:**
- ❌ KHÔNG commit file `.env` lên Git
- ❌ KHÔNG share API key trong screenshots/logs
- ❌ KHÔNG paste API key vào public chat/forum
- ✅ Regenerate API key nếu bị leak
- ✅ Monitor usage regularly

**File `.gitignore` đã bảo vệ:**
```bash
# File .gitignore
.env           # <-- Protected
.env.local
*.key
secrets.toml
```

---

**Ready to test? Let's go! 🚀**

## 📝 Testing Notes (For Your Records)

**Date Tested:** _______________

**Test Results:**
- [ ] Test 1: Gemini Connection - PASSED / FAILED
- [ ] Test 2: Marketing Pipeline - PASSED / FAILED
- [ ] Test 3: E-commerce Pipeline - PASSED / FAILED
- [ ] Test 4: Rate Limiting - PASSED / FAILED

**Performance:**
- Marketing Pipeline Time: _______ seconds
- E-commerce Pipeline Time: _______ seconds
- Quality Score: _______ / 100

**Issues Encountered:**
_________________________________________________
_________________________________________________
_________________________________________________

**Notes:**
_________________________________________________
_________________________________________________
_________________________________________________
