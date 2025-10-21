# 🚀 DataAnalytics Vietnam - Hướng Dẫn Setup

## 📋 Yêu Cầu Hệ Thống

- **Python:** 3.11 trở lên
- **RAM:** Tối thiểu 2GB (khuyến nghị 4GB)
- **Disk:** 500MB trống
- **Internet:** Kết nối ổn định (cho Gemini API)

---

## 🔑 Bước 1: Lấy Gemini API Key (MIỄN PHÍ)

1. Truy cập: https://aistudio.google.com/app/apikey
2. Đăng nhập bằng Google Account
3. Click **"Create API Key"**
4. Copy API key (dạng: `AIzaSy...`)

**Giới hạn Free Tier:**
- ✅ 15 requests/phút
- ✅ 1,500 requests/ngày
- ✅ Không cần thẻ tín dụng

---

## 🛠️ Bước 2: Cài Đặt Local

### 2.1. Clone Repository (hoặc download ZIP)

```bash
# Nếu có git
git clone https://github.com/yourusername/dataanalytics-vietnam.git
cd dataanalytics-vietnam

# Hoặc download ZIP và giải nén
```

### 2.2. Tạo Virtual Environment

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 2.3. Cài Dependencies

```bash
pip install -r requirements.txt
```

**Thời gian:** 2-3 phút (tùy tốc độ internet)

### 2.4. Cấu Hình API Key

```bash
# Copy template
cp .env.template .env

# Mở .env bằng text editor
# Thay "your_gemini_api_key_here" bằng API key thực
```

**File `.env` sau khi sửa:**
```bash
GEMINI_API_KEY=AIzaSyAbc123YourRealKeyHere
```

---

## ▶️ Bước 3: Chạy Ứng Dụng

```bash
streamlit run streamlit_app.py
```

**Kết quả:**
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

Mở trình duyệt và truy cập: **http://localhost:8501**

---

## 📊 Bước 4: Test với Sample Data

### 4.1. Chuẩn bị file CSV/Excel

**Marketing Sample (Google Ads):**
```csv
campaign_name,clicks,impressions,cost,conversions
Brand Campaign,1250,25000,3500,45
Search Ads,890,18000,2800,32
Display Ads,560,45000,1500,18
```

**E-commerce Sample (Shopify):**
```csv
order_id,order_date,product_name,quantity,revenue
ORD001,2024-01-15,Product A,2,5000
ORD002,2024-01-16,Product B,1,3500
ORD003,2024-01-17,Product A,3,7500
```

### 4.2. Upload và Phân Tích

1. Click **"📁 Tải lên file CSV/Excel"**
2. Chọn file sample
3. (Tùy chọn) Thêm mô tả: "Dữ liệu Google Ads tháng 1/2024"
4. Click **"🚀 Phân Tích Ngay"**
5. Đợi 50-60 giây ⏱️

**Kết quả mong đợi:**
- ✅ Quality Score: 85-95/100
- ✅ 8-10 biểu đồ tương tác
- ✅ 5-7 insights chuyên sâu
- ✅ Benchmarks so sánh ngành

---

## 🐛 Khắc Phục Sự Cố

### Lỗi: "Invalid API Key"

```
❌ GEMINI_API_KEY không hợp lệ hoặc chưa được cấu hình
```

**Giải pháp:**
1. Kiểm tra file `.env` có tồn tại không
2. Kiểm tra API key đúng format (bắt đầu bằng `AIza`)
3. Thử tạo API key mới tại https://aistudio.google.com/app/apikey

---

### Lỗi: "Rate Limit Exceeded"

```
⏳ Gemini API đang bận, chờ 4s...
```

**Nguyên nhân:** Vượt quá 15 requests/phút

**Giải pháp:**
- ✅ Hệ thống tự động retry (chờ 2s → 4s → 8s)
- ✅ Nếu lỗi tiếp tục, đợi 1 phút và thử lại

---

### Lỗi: "File quá lớn"

```
❌ File quá lớn: 250.5MB. Giới hạn: 200MB
```

**Giải pháp:**
1. Lọc dữ liệu (chỉ lấy cột cần thiết)
2. Giới hạn số dòng (VD: 100,000 dòng gần nhất)
3. Nén file Excel → CSV (thường nhẹ hơn 50%)

---

### Lỗi: "Encoding Error"

```
❌ Không thể đọc file. Encoding không được hỗ trợ.
```

**Giải pháp:**
1. Mở file bằng Excel
2. "Save As" → chọn encoding **UTF-8** hoặc **CSV (Comma delimited)**
3. Upload file mới

---

## 🎯 Performance Benchmarks

| Dataset Size | Expected Time | Quality Score |
|--------------|---------------|---------------|
| 1,000 rows   | 45-50s        | 90-95/100     |
| 10,000 rows  | 50-55s        | 85-90/100     |
| 100,000 rows | 55-60s        | 80-85/100     |

**Nếu quá 60 giây:** Kiểm tra kết nối internet hoặc Gemini API status

---

## 🚀 Deploy lên Streamlit Cloud (MIỄN PHÍ)

### Bước 1: Tạo tài khoản Streamlit Cloud

1. Truy cập: https://streamlit.io/cloud
2. Sign up bằng GitHub
3. Free tier: Unlimited public apps, 1GB RAM

### Bước 2: Deploy App

1. Push code lên GitHub repository (public hoặc private)
2. Vào Streamlit Cloud dashboard
3. Click **"New app"**
4. Chọn repository: `yourusername/dataanalytics-vietnam`
5. Main file: `streamlit_app.py`
6. Click **"Deploy"**

### Bước 3: Thêm Secrets

1. Vào **"App settings"** → **"Secrets"**
2. Thêm nội dung:
   ```toml
   GEMINI_API_KEY = "AIzaSyAbc123YourRealKeyHere"
   ```
3. Click **"Save"**

**Thời gian deploy:** 5-10 phút

**URL công khai:** `https://your-app.streamlit.app`

---

## 📚 Tài Liệu Tham Khảo

- **Streamlit Docs:** https://docs.streamlit.io
- **Gemini API Docs:** https://ai.google.dev/docs
- **Plotly Charts:** https://plotly.com/python/

---

## 🆘 Hỗ Trợ

- **GitHub Issues:** https://github.com/yourusername/dataanalytics-vietnam/issues
- **Email:** support@dataanalytics.vn
- **Zalo/Telegram:** [Your contact]

---

## 📝 Checklist Setup Thành Công

- [ ] Python 3.11+ đã cài đặt
- [ ] Virtual environment đã tạo và kích hoạt
- [ ] Dependencies đã cài (`pip install -r requirements.txt`)
- [ ] File `.env` đã tạo với API key hợp lệ
- [ ] Chạy `streamlit run streamlit_app.py` không lỗi
- [ ] Truy cập http://localhost:8501 thành công
- [ ] Test với sample data hoàn thành
- [ ] Quality Score ≥ 80/100
- [ ] Dashboard hiển thị 8-10 charts
- [ ] Insights có ý nghĩa và liên quan

**Nếu tất cả checklist đều ✅ → Setup thành công! 🎉**

---

## ⏭️ Next Steps

1. ✅ Test với dữ liệu thực của bạn
2. ✅ Khám phá 7 domains (Marketing, E-commerce, Sales, Finance, Operations, Customer Service, HR)
3. ✅ Đọc [User Guide](USER_GUIDE.md) để tối ưu kết quả
4. ✅ Deploy lên Streamlit Cloud để chia sẻ với team
5. ✅ Cung cấp feedback để cải thiện sản phẩm

**Chúc bạn phân tích dữ liệu thành công! 🚀📊**
