# 🔧 STREAMLIT CLOUD - CHANGE MAIN FILE PATH

**Problem**: App đang chạy `src/app.py` thay vì `streamlit_app.py`

**Solution**: 2 phương pháp dưới đây

---

## ✅ METHOD A: Edit Existing App (RECOMMENDED)

### Step 1: Access App Settings

1. Đăng nhập: https://share.streamlit.io/ (hoặc https://app.streamlit.io/)
2. Vào **"Your apps"**
3. Tìm app: **fast-dashboard**
4. Click vào app để mở

### Step 2: Open Edit/Manage Dialog

Click vào **một trong các nút sau** (tùy UI version):
- **⋯ (3 dots)** → **"Settings"** hoặc **"Manage app"**
- Hoặc nút **"⚙️ Settings"** ở góc phải
- Hoặc nút **"✏️ Edit"** / **"Edit app"**

### Step 3: Find Main File Setting

Trong dialog Settings/Edit, tìm một trong các fields sau:
- **"Main file"**
- **"Main file path"**  
- **"App file"**
- Hoặc field có placeholder: `app.py` hoặc `streamlit_app.py`

### Step 4: Change the Path

**Current value**: `src/app.py` ❌

**Change to**: `streamlit_app.py` ✅

**Important notes**:
- Dùng forward slashes `/` (không phải `\`)
- Path relative to repo root
- Phải include `.py` extension
- File phải tồn tại trên GitHub `main` branch

### Step 5: Save & Deploy

Click:
- **"Save"**
- Hoặc **"Save & deploy"**
- Hoặc **"Update"**

App sẽ **auto-redeploy** (~2-3 phút)

### Step 6: Verify

- Wait 2-3 minutes
- Refresh: https://fast-nicedashboard.streamlit.app/
- Test upload manufacturing data
- ✅ Should see 9 KPIs with values

---

## 🔄 METHOD B: Re-create App (If Method A Doesn't Work)

### When to use:
- Nếu không tìm thấy "Main file" setting trong Edit dialog
- Hoặc field bị disabled/locked
- Hoặc bạn muốn URL mới

### Steps:

1. **Delete old app** (optional - nếu muốn giữ URL):
   - Vào app settings → Scroll xuống
   - Click **"Delete app"** (màu đỏ)
   - Confirm deletion

2. **Create new app**:
   - Click **"New app"** hoặc **"Deploy a new app"**
   - Chọn GitHub repo: `zicky008/fast-dataanalytics-vietnam`
   - Chọn branch: `main`
   - **Main file path**: `streamlit_app.py` ✅
   - (Optional) Advanced: Set Python version to 3.10+
   - Click **"Deploy"**

3. **Wait for deployment**: ~3-5 minutes

4. **Update bookmarks**: URL có thể thay đổi

---

## 📸 WHAT TO LOOK FOR (Screenshots Help)

### Common UI Variations:

**Option 1**: App dashboard view
```
Your app: fast-dashboard
├── ⚙️ Settings (button)
└── When clicked:
    └── Main file: [src/app.py] ← Edit this
```

**Option 2**: Three-dot menu
```
fast-dashboard          ⋯
                        ├── Manage app
                        ├── View logs
                        └── Settings
                            └── Main file path: [____]
```

**Option 3**: App card view
```
[fast-dashboard card]
└── ✏️ Edit
    └── Dialog opens:
        └── Main file: [src/app.py]
```

---

## 🔍 IF YOU CAN'T FIND THE SETTING

### Troubleshooting:

1. **Check different tabs**: 
   - General
   - Advanced
   - App settings

2. **Look for these keywords**:
   - "Main file"
   - "Entry point"
   - "App file"
   - "Python file"
   - "Streamlit file"

3. **Try refreshing the page**: Sometimes UI doesn't load fully

4. **Check your role**: 
   - Are you app owner?
   - Or just collaborator? (might not have edit permissions)

5. **Take screenshot**: 
   - Screenshot the Settings/Edit page
   - Show me what options you see
   - I can guide you based on actual UI

---

## 📋 VERIFICATION AFTER CHANGE

### Check deployment:

1. **Go to app logs**:
   - Settings → Logs (or Manage app → Logs)
   - Look for: `streamlit run streamlit_app.py`
   - Should NOT see: `streamlit run src/app.py`

2. **Test functionality**:
   - Upload: `manufacturing_production_30days.xlsx`
   - Click "Analyze Data"
   - Wait ~20-30 seconds
   - Check Dashboard tab
   - ✅ Should see **9 KPIs** with numbers

3. **Compare with local**:
   - Local: https://8501-il3t21q4q4u3y4euhfp08-de59bda9.sandbox.novita.ai
   - Production: https://fast-nicedashboard.streamlit.app/
   - Should be IDENTICAL

---

## 🆘 IF STILL STUCK

### Send me:

1. **Screenshot** of Streamlit Cloud app page (the one with your app listed)
2. **Screenshot** of Settings/Edit dialog (all tabs if multiple)
3. **Tell me**:
   - What buttons do you see?
   - What fields are available?
   - Any error messages?

I'll guide you through the exact clicks for your specific UI.

---

## ⚡ QUICK ALTERNATIVE (If All Else Fails)

### Rename file on GitHub (hacky but works):

1. Go to: https://github.com/zicky008/fast-dataanalytics-vietnam
2. Rename `streamlit_app.py` → `src/app.py`
3. Commit change
4. Wait for Streamlit Cloud auto-deploy
5. Test app
6. (Later can rename back if needed)

**Note**: This is NOT ideal because:
- Breaks local development
- Makes docs inconsistent
- But it WILL work if you can't change main file path

---

## 📊 EXPECTED TIMELINE

| Action | Time |
|--------|------|
| Find settings page | 30 seconds |
| Change main file | 10 seconds |
| Save & trigger redeploy | Click |
| Wait for deployment | 2-3 minutes |
| Test & verify | 1 minute |
| **Total** | **~4 minutes** |

---

**Current Status**: ⏳ Waiting for you to find and change Main file setting

**Next Step**: Screenshot what you see in Streamlit Cloud settings, I'll guide you precisely!
