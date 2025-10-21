# ⚡ Quick Start - DataAnalytics Vietnam

## 🚀 Chạy Local trong 2 Phút

### Bước 1: Setup Environment

```bash
# Clone repo (hoặc download ZIP)
cd webapp

# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
# hoặc: venv\Scripts\activate  # Windows

# Cài dependencies
pip install -r requirements.txt
```

### Bước 2: Cấu Hình API Key

```bash
# Copy template
cp .env.template .env

# Mở .env và thay API key
# GEMINI_API_KEY=your_actual_key_here
```

**Lấy API Key miễn phí:**
👉 https://aistudio.google.com/app/apikey

### Bước 3: Chạy App

```bash
streamlit run streamlit_app.py
```

Mở trình duyệt: **http://localhost:8501** 🎉

---

## 📊 Test với Sample Data

### Marketing Sample (Google Ads)

Tạo file `sample_marketing.csv`:

```csv
campaign_name,date,clicks,impressions,cost,conversions,revenue
Brand Campaign,2024-01-15,1250,25000,3500,45,18000
Search Ads,2024-01-16,890,18000,2800,32,12500
Display Ads,2024-01-17,560,45000,1500,18,7200
Retargeting,2024-01-18,420,8000,1200,28,11000
Video Ads,2024-01-19,680,35000,2100,22,8800
```

**Kết quả mong đợi:**
- ✅ Domain: Marketing / Quảng Cáo
- ✅ KPIs: ROAS, CTR, CPC, CPA
- ✅ Benchmarks: CTR 3.17%, ROAS 4:1
- ✅ Insights từ CMO expert

---

### E-commerce Sample (Shopify)

Tạo file `sample_ecommerce.csv`:

```csv
order_id,order_date,customer_id,product_name,category,quantity,revenue,cost
ORD001,2024-01-15,CUST123,Product A,Electronics,2,5000,3000
ORD002,2024-01-16,CUST456,Product B,Fashion,1,3500,2000
ORD003,2024-01-17,CUST123,Product C,Electronics,3,7500,4500
ORD004,2024-01-18,CUST789,Product A,Electronics,1,2500,1500
ORD005,2024-01-19,CUST456,Product D,Home,2,4000,2400
```

**Kết quả mong đợi:**
- ✅ Domain: E-commerce
- ✅ KPIs: AOV, Conversion Rate, CLV
- ✅ Benchmarks: AOV $81.49, CR 2-3%
- ✅ Insights từ Chief E-commerce Officer

---

## 🔍 Xác Nhận Setup Thành Công

### Checklist:

- [ ] Virtual environment activated (`(venv)` trong terminal)
- [ ] Dependencies installed (no errors từ `pip install`)
- [ ] `.env` file created với valid API key
- [ ] Streamlit app running (http://localhost:8501)
- [ ] Sample file uploaded thành công
- [ ] Analysis completed trong 50-60 giây
- [ ] Quality Score ≥ 80/100
- [ ] Dashboard có 8-10 charts
- [ ] Insights tab có 5-7 recommendations

**Nếu tất cả ✅ → Setup hoàn tất! 🎉**

---

## 🐛 Troubleshooting Nhanh

### Lỗi: ModuleNotFoundError

```bash
# Kiểm tra virtual env đã activate chưa
which python  # Should point to venv/bin/python

# Cài lại dependencies
pip install -r requirements.txt --force-reinstall
```

---

### Lỗi: Invalid API Key

```bash
# Kiểm tra .env file
cat .env  # Should show GEMINI_API_KEY=AIza...

# Kiểm tra API key có valid không
# Vào: https://aistudio.google.com/app/apikey
# Tạo key mới nếu cần
```

---

### Lỗi: Rate Limit

```
⏳ Gemini API đang bận, chờ 4s...
```

**Bình thường:** Hệ thống tự retry (2s → 4s → 8s)  
**Nếu liên tục:** Đợi 1 phút (free tier: 15 requests/minute)

---

## 📖 Đọc Thêm

- **Setup đầy đủ:** [SETUP.md](SETUP.md)
- **Hướng dẫn sử dụng:** [USER_GUIDE.md](USER_GUIDE.md)
- **Tài liệu kỹ thuật:** [README.md](README.md)

---

## 🎯 Next Steps

1. ✅ Test với sample data (Marketing + E-commerce)
2. ✅ Test với dữ liệu thực của bạn
3. ✅ Đọc USER_GUIDE.md để hiểu 7 domains
4. ✅ Deploy lên Streamlit Cloud (miễn phí)
5. ✅ Share với team và collect feedback

**Chúc bạn phân tích dữ liệu thành công! 🚀**

---

**Gặp vấn đề?**  
📧 Email: support@dataanalytics.vn  
💬 GitHub Issues: [Link to issues]
