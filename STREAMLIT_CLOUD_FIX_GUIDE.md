# 🚨 STREAMLIT CLOUD DEPLOYMENT FIX GUIDE

## VẤN ĐỀ HIỆN TẠI

Production app (https://fast-dashboard.streamlit.app/) vẫn báo lỗi:
```
Model 'gemini-2.5-flash' không khả dụng
```

Trong khi local app đã chạy tốt với `gemini-2.0-flash`.

---

## NGUYÊN NHÂN

1. **Streamlit Cloud chưa pull code mới** từ GitHub
2. Hoặc **cache issue** - vẫn chạy code cũ
3. Hoặc **main file path sai** - đang chạy file cũ thay vì `streamlit_app.py`

---

## GIẢI PHÁP KHẨN CẤP (LÀM NGAY)

### **Option 1: Force Reboot App** (Nhanh nhất - 30 giây)

1. Truy cập: https://share.streamlit.io/
2. Đăng nhập với GitHub account
3. Tìm app: **fast-dashboard**
4. Click **⋮ (3 dots)** → **Settings**
5. Scroll xuống → Click **"Reboot app"**
6. ✅ Chờ 30 giây → Test lại app

### **Option 2: Clear Cache + Rebuild** (Toàn diện - 2-3 phút)

1. Vào Settings của app
2. Click **"Clear cache"**
3. Chờ cache clear xong
4. Click **"Reboot app"**
5. ✅ Chờ 2-3 phút → Test lại app

### **Option 3: Verify Main File Path** (Nếu vẫn lỗi)

1. Vào Settings → **General**
2. Check **"Main file path"**: 
   - ✅ ĐÚNG: `streamlit_app.py`
   - ❌ SAI: `streamlit_app.py` (file cũ)
   - ❌ SAI: `streamlit_app.py` (file cũ)
3. Nếu sai → Đổi thành `streamlit_app.py`
4. Click **Save**
5. App sẽ auto-rebuild
6. ✅ Chờ 2-3 phút → Test lại app

### **Option 4: Check Branch** (Nếu vẫn lỗi)

1. Vào Settings → **General**
2. Check **"Branch"**: Phải là `main`
3. Nếu sai → Đổi thành `main`
4. Save → Auto-rebuild
5. ✅ Test lại app

---

## VERIFY GITHUB CODE (Đã OK)

Tôi đã push 4 commits lên GitHub `main` branch:

```bash
5b4efbd - Fix hardcoded model name in error message
973da24 - FORCE DEPLOY: Trigger rebuild
a582b69 - Use stable model: gemini-2.0-flash
4e25021 - Fix genai module vs model object
```

Code trên GitHub đã ĐÚNG:
- ✅ `src/premium_lean_pipeline.py` line 2354: `gemini-2.0-flash`
- ✅ `streamlit_app.py` imports `premium_lean_pipeline`
- ✅ Error messages đã fix

---

## SAU KHI REBOOT/REBUILD

### Test Checklist:

1. **Upload manufacturing data**
   - File: `sample_data/manufacturing_production_30days.xlsx`
   - Hoặc download: https://github.com/zicky008/fast-dataanalytics-vietnam/tree/main/sample_data

2. **Verify KPIs hiển thị**
   - Should see **9 KPIs** with numeric values
   - NOT empty boxes

3. **Verify error messages**
   - Không còn mention `gemini-2.5-flash`
   - Nếu có lỗi → Generic message về API key

---

## NẾU VẪN KHÔNG HOẠT ĐỘNG

### Debug Steps:

1. **Check app logs**:
   - Trong Streamlit Cloud → Logs tab
   - Look for errors about model loading
   - Screenshot và gửi cho tôi

2. **Verify environment variables**:
   - Settings → Secrets
   - Check `GEMINI_API_KEY` có đúng không
   - Format: `GEMINI_API_KEY = "your-key-here"`

3. **Check Python version**:
   - Settings → Python version
   - Should be: **Python 3.9+** (3.10 recommended)

4. **Check requirements.txt**:
   - Verify `google-generativeai` version
   - Should be: `google-generativeai>=0.3.0`

---

## TIMELINE EXPECTED

| Action | Time | Result Check |
|--------|------|--------------|
| Reboot app | 30s | Immediate - check app URL |
| Clear cache + rebuild | 2-3 min | Check after 3 min |
| Change main file | 2-3 min | Auto-rebuild → check logs |

---

## CONTACT ME IF STUCK

Nếu sau tất cả steps trên vẫn không hoạt động:

1. **Screenshot** Streamlit Cloud settings page
2. **Copy** full error message from app
3. **Check** app logs tab
4. Gửi cho tôi → Tôi sẽ investigate deeper

---

## EXPECTED FINAL STATE

✅ **Production app**: https://fast-dashboard.streamlit.app/
✅ **Local app**: https://8501-il3t21q4q4u3y4euhfp08-de59bda9.sandbox.novita.ai

Both should show:
- 9 Manufacturing KPIs with numeric values
- 8 Interactive charts
- Domain expert insights
- No errors about model names

---

**Last Updated**: 2025-10-22 13:15 UTC
**Git Commit**: `5b4efbd`
