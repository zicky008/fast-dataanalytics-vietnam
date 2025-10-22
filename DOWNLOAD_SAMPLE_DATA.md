# 📥 DOWNLOAD SAMPLE DATA - MANUFACTURING DOMAIN

## 🎯 Files Available for Testing

### **Manufacturing Production Data (30 Days)**
- **180 rows** (30 days × 6 shifts)
- **14 columns** (production metrics)
- **100% validated** data quality

---

## 📊 OPTION 1: DOWNLOAD EXCEL FILE (Recommended)

**File**: `manufacturing_production_30days.xlsx`
**Size**: 16 KB
**Format**: Microsoft Excel (.xlsx)

### **Direct Download Links**:

🔗 **GitHub Direct Download**:
```
https://github.com/zicky008/fast-dataanalytics-vietnam/raw/main/sample_data/manufacturing_production_30days.xlsx
```

**Cách tải**:
1. Click vào link trên
2. File sẽ tự động download về máy
3. Hoặc: Right-click → "Save link as..."

---

## 📄 OPTION 2: DOWNLOAD CSV FILE

**File**: `manufacturing_production_30days.csv`
**Size**: 15 KB
**Format**: CSV (Comma-Separated Values)

### **Direct Download Links**:

🔗 **GitHub Direct Download**:
```
https://github.com/zicky008/fast-dataanalytics-vietnam/raw/main/sample_data/manufacturing_production_30days.csv
```

**Cách tải**:
1. Click vào link trên
2. File sẽ tự động download về máy
3. Hoặc: Right-click → "Save link as..."

---

## 📋 DATA STRUCTURE

### **Columns** (14 total):
1. `production_date` - Ngày sản xuất (YYYY-MM-DD)
2. `shift` - Ca làm việc (Morning/Afternoon/Night)
3. `production_line` - Dây chuyền (Line A/B)
4. `machine_id` - Mã máy (M001, M002)
5. `units_produced` - Số lượng sản xuất
6. `good_units` - Số lượng đạt chất lượng
7. `defective_units` - Số lượng lỗi
8. `downtime_hours` - Giờ ngừng máy
9. `available_hours` - Giờ làm việc khả dụng
10. `actual_run_hours` - Giờ máy chạy thực tế
11. `theoretical_max_output` - Công suất tối đa lý thuyết
12. `total_cost_vnd` - Tổng chi phí (VND)
13. `material_cost_vnd` - Chi phí nguyên vật liệu (VND)
14. `labor_cost_vnd` - Chi phí nhân công (VND)

### **Sample Preview** (first 3 rows):
```
production_date | shift     | production_line | machine_id | units_produced | good_units | defective_units
2024-01-01      | Morning   | Line A          | M001       | 950            | 920        | 30
2024-01-01      | Afternoon | Line A          | M001       | 930            | 905        | 25
2024-01-01      | Night     | Line A          | M001       | 880            | 850        | 30
```

---

## ✅ EXPECTED KPIs (Ground Truth)

Sau khi upload file này lên app, bạn sẽ thấy **9 KPIs** với giá trị chính xác:

1. **OEE (Overall Equipment Effectiveness)**: 83.28%
2. **First Pass Yield (FPY)**: 97.45%
3. **Defect Rate**: 2.55%
4. **Machine Utilization**: 94.26%
5. **Cycle Time**: 0.62 min/unit
6. **Downtime %**: 5.74%
7. **Cost per Unit**: 162,920 VND
8. **Scrap Rate**: 2.55%
9. **Throughput**: 13,032 units

---

## 🧪 TESTING CHECKLIST

### **Step 1: Download File**
- [ ] Download Excel hoặc CSV file từ links trên
- [ ] Verify file size (~15-16 KB)

### **Step 2: Open Production App**
- [ ] Navigate to: https://fast-nicedashboard.streamlit.app/
- [ ] Wait for app to load (should be <5 seconds)

### **Step 3: Upload File**
- [ ] Click "Browse files" hoặc drag & drop
- [ ] Select downloaded file
- [ ] Wait for processing (~10-30 seconds)

### **Step 4: Verify Results**
- [ ] Domain detected: "Manufacturing/Operations"
- [ ] All 9 KPIs displayed
- [ ] Charts rendered correctly
- [ ] Expert insights displayed

### **Step 5: Report Back**
- [ ] Take screenshots of results
- [ ] Note any errors or issues
- [ ] Compare KPI values with ground truth above

---

## 🆘 TROUBLESHOOTING

### **Problem**: File won't download
**Solution**: 
- Try different browser
- Right-click → "Save link as..."
- Or use wget/curl:
  ```bash
  wget https://github.com/zicky008/fast-dataanalytics-vietnam/raw/main/sample_data/manufacturing_production_30days.xlsx
  ```

### **Problem**: App shows error after upload
**Solution**:
- Check file format (must be .xlsx or .csv)
- Verify file not corrupted (open in Excel first)
- Try refreshing the page and re-upload

### **Problem**: KPIs not displaying
**Solution**:
- Wait 30 seconds for processing
- Check browser console for errors (F12)
- Try different file format (CSV vs Excel)

---

## 📞 SUPPORT

Nếu gặp bất kỳ vấn đề nào, vui lòng:
1. Chụp screenshot error message
2. Mô tả chi tiết vấn đề
3. Report lại để debug

---

**Created**: 2025-10-22
**Updated**: 2025-10-22
**Status**: ✅ Ready for Testing
