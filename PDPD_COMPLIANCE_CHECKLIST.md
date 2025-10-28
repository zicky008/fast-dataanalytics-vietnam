# ✅ PDPD COMPLIANCE CHECKLIST - Vietnam Decree 13/2023/NĐ-CP
## For Startup Founders & Solo Entrepreneurs

**Version:** 1.0 (Legally Validated)
**Effective Date:** July 1, 2023
**Last Updated:** October 28, 2025
**Legal Basis:** Nghị định 13/2023/NĐ-CP về Bảo vệ Dữ liệu Cá nhân

---

## 🎯 MỤC TIÊU / OBJECTIVE

**VN:** Hướng dẫn tuân thủ Nghị định 13/2023/NĐ-CP cho startup/founder solo xử lý dữ liệu người dùng (upload file, phân tích, xuất báo cáo).

**EN:** Guide for startups/solo founders to comply with Decree 13/2023/ND-CP when processing user data (file upload, analysis, report generation).

---

## 📋 CHECKLIST - STAGE 1: BEFORE LAUNCH (BẮT BUỘC)

### ☑️ 1. Xác định loại dữ liệu & yêu cầu DPO

**VN:**
- [ ] Kiểm tra xem có xử lý **dữ liệu cá nhân nhạy cảm** không:
  - ✅ Dữ liệu tài chính (thu nhập, chi tiêu, tài khoản)
  - ✅ Dữ liệu sinh trắc học (vân tay, khuôn mặt)
  - ✅ Dữ liệu sức khỏe
  - ✅ Dữ liệu vị trí địa lý
  - ✅ Thông tin trẻ em dưới 16 tuổi
  - ❌ Chỉ dữ liệu doanh nghiệp (không có PII)

- [ ] **Nếu CÓ dữ liệu nhạy cảm** → Bổ nhiệm DPO (Data Protection Officer):
  - Yêu cầu: 3+ năm kinh nghiệm bảo vệ dữ liệu/an ninh mạng
  - Phải hoàn thành chương trình đào tạo của Bộ Công an
  - Có thể thuê ngoài (outsource) hoặc kiêm nhiệm (part-time)

- [ ] **Nếu KHÔNG có dữ liệu nhạy cảm** + đăng ký startup/SME + chưa 2 năm thành lập:
  - ✅ Được miễn DPO trong 2 năm đầu
  - ⚠️ Sau 2 năm → phải bổ nhiệm DPO

**EN:**
- [ ] Check if processing **sensitive personal data**:
  - ✅ Financial data (income, expenses, accounts)
  - ✅ Biometric data (fingerprints, facial recognition)
  - ✅ Health data
  - ✅ Location data
  - ✅ Children's data (under 16)
  - ❌ Business data only (no PII)

- [ ] **If processing sensitive data** → Appoint DPO:
  - Requirement: 3+ years experience in data protection/cybersecurity
  - Must complete training by Ministry of Public Security
  - Can outsource or part-time internal

- [ ] **If NO sensitive data** + registered startup/SME + less than 2 years old:
  - ✅ 2-year DPO exemption
  - ⚠️ After 2 years → must appoint DPO

**Action:**
```
□ Sensitive data: YES / NO
□ DPO required: YES / NO / EXEMPTED (2 years)
□ DPO appointed: __________ (name)
□ DPO training completed: YES / NO
```

---

### ☑️ 2. Tạo Hồ sơ Đánh giá Tác động (Impact Assessment) - BẮT BUỘC

**VN:**
- [ ] Chuẩn bị **Hồ sơ Đánh giá Tác động** xử lý dữ liệu cá nhân (DPIA - Data Protection Impact Assessment)
- [ ] **NỘP HỒ SƠ đến Bộ Công an trong vòng 60 ngày** kể từ khi bắt đầu xử lý dữ liệu
- [ ] Nộp đến: Cục An ninh mạng và Phòng chống tội phạm sử dụng công nghệ cao, Bộ Công an
- [ ] Luôn sẵn sàng để phục vụ thanh tra của Bộ Công an

**Nội dung hồ sơ phải có:**
1. ✅ Thông tin Bên kiểm soát dữ liệu (Data Controller) và Bên xử lý dữ liệu (Data Processor)
2. ✅ Thông tin DPO nội bộ
3. ✅ Danh sách người nhận dữ liệu cá nhân + quốc tịch
4. ✅ Loại và mục đích xử lý dữ liệu cá nhân
5. ✅ Thời gian lưu trữ dữ liệu
6. ✅ Biện pháp bảo vệ dữ liệu (technical & organizational measures)
7. ✅ Đánh giá rủi ro và biện pháp giảm thiểu

**EN:**
- [ ] Prepare **Data Protection Impact Assessment (DPIA)** dossier
- [ ] **SUBMIT to Ministry of Public Security within 60 days** of starting data processing
- [ ] Submit to: Department of Cybersecurity and High-Tech Crime Prevention, MPS
- [ ] Keep available for MPS inspection at all times

**Required Content:**
1. ✅ Data Controller & Data Processor information
2. ✅ Internal DPO information
3. ✅ Recipients of personal data + nationality
4. ✅ Types and purposes of personal data processing
5. ✅ Data retention period
6. ✅ Data protection measures (technical & organizational)
7. ✅ Risk assessment and mitigation measures

**Action:**
```
□ DPIA completed: YES / NO
□ DPIA submitted to MPS: YES / NO
□ Submission date: __________
□ DPIA available for inspection: YES / NO
```

---

### ☑️ 3. Đánh giá Chuyển dữ liệu ra nước ngoài (nếu có)

**VN:**
- [ ] Kiểm tra xem có **chuyển dữ liệu cá nhân ra nước ngoài** không:
  - ✅ Sử dụng server quốc tế (AWS Singapore, Google Cloud, Azure)
  - ✅ Lưu trữ backup ở nước ngoài
  - ✅ Sử dụng dịch vụ cloud của bên thứ ba nước ngoài
  - ❌ Chỉ lưu trữ tại Việt Nam

- [ ] **Nếu CÓ chuyển ra nước ngoài** → Tạo **Hồ sơ Đánh giá Tác động riêng** cho việc chuyển dữ liệu xuyên biên giới:
  - Nộp đến Bộ Công an trong vòng **60 ngày** kể từ khi bắt đầu chuyển dữ liệu
  - Phải có **đồng ý của chủ thể dữ liệu** cho việc chuyển ra nước ngoài
  - Xác minh **biện pháp bảo vệ dữ liệu** ở nước nhận
  - Hợp đồng chuyển dữ liệu phải ghi rõ: vị trí lưu trữ, thời gian lưu trữ, xử lý sau khi hết hạn

- [ ] **Quyền thanh tra của Bộ Công an:**
  - Bộ Công an có quyền thanh tra 1 lần/năm
  - Có thể ra lệnh dừng chuyển dữ liệu nếu vi phạm an ninh quốc gia hoặc rò rỉ dữ liệu

**EN:**
- [ ] Check if **transferring personal data outside Vietnam**:
  - ✅ Using international servers (AWS Singapore, Google Cloud, Azure)
  - ✅ Storing backups abroad
  - ✅ Using third-party cloud services abroad
  - ❌ Only storing in Vietnam

- [ ] **If transferring abroad** → Create **separate Cross-Border Transfer Impact Assessment**:
  - Submit to MPS within **60 days** of transfer commencement
  - Must obtain **data subject consent** for international transfer
  - Verify **data protection measures** in receiving country
  - Transfer agreement must specify: storage location, duration, post-expiration handling

- [ ] **MPS Inspection Rights:**
  - MPS can inspect once per year
  - Can order cessation if national security violation or data breach

**Action:**
```
□ Cross-border transfer: YES / NO
□ If YES, server location: __________
□ Cross-border DPIA completed: YES / NO
□ Cross-border DPIA submitted: YES / NO
□ Data subject consent obtained: YES / NO
□ Transfer agreement signed: YES / NO
```

---

## 📋 CHECKLIST - STAGE 2: DURING OPERATION

### ☑️ 4. Xin đồng ý rõ ràng, chủ động trước khi xử lý

**VN:**
- [ ] Hiển thị **Chính sách Bảo mật** rõ ràng (Privacy Policy) trước khi thu thập dữ liệu
- [ ] Checkbox **"Tôi đồng ý"** KHÔNG được tick sẵn (must be unticked by default)
- [ ] Đồng ý phải **rõ ràng, cụ thể, dễ rút lại**
- [ ] **Riêng biệt cho từng mục đích** (không gộp chung nhiều mục đích vào 1 checkbox)
- [ ] Lưu **audit log** về thời điểm đồng ý, IP address, session ID

**Nội dung phải thông báo:**
1. ✅ **Mục đích** xử lý dữ liệu (VD: phân tích dữ liệu, tạo báo cáo)
2. ✅ **Phạm vi** dữ liệu thu thập (VD: file CSV/Excel, không thu thập email/số điện thoại)
3. ✅ **Thời gian lưu trữ** (VD: xóa ngay sau khi xuất PDF, hoặc 24 giờ)
4. ✅ **Nơi lưu trữ** (VD: server tại Việt Nam, hoặc AWS Singapore)
5. ✅ **Quyền rút lại đồng ý** (cách thức + thời hạn phản hồi 72 giờ)
6. ✅ **Quyền của chủ thể dữ liệu** (truy cập, xóa, hạn chế xử lý, phản đối)

**EN:**
- [ ] Display clear **Privacy Policy** before collecting data
- [ ] **"I consent" checkbox** must be unticked by default
- [ ] Consent must be **explicit, specific, easily retractable**
- [ ] **Separate consent for each purpose** (cannot bundle multiple purposes)
- [ ] Save **audit log** with consent timestamp, IP address, session ID

**Must disclose:**
1. ✅ **Purpose** of data processing (e.g., data analysis, report generation)
2. ✅ **Scope** of data collected (e.g., CSV/Excel file, no email/phone collected)
3. ✅ **Retention period** (e.g., delete immediately after PDF export, or 24 hours)
4. ✅ **Storage location** (e.g., servers in Vietnam, or AWS Singapore)
5. ✅ **Right to withdraw consent** (method + 72-hour response deadline)
6. ✅ **Data subject rights** (access, delete, restrict, object)

**Action:**
```
□ Privacy Policy created: YES / NO
□ Consent checkbox implemented: YES / NO
□ Checkbox default: UNTICKED ✅
□ Audit log system: ACTIVE / INACTIVE
□ Purpose-specific consent: YES / NO
```

---

### ☑️ 5. Giới hạn mục đích & Xóa dữ liệu kịp thời

**VN:**
- [ ] Dữ liệu **chỉ được xử lý cho mục đích đã thông báo**
- [ ] **KHÔNG được** sử dụng cho mục đích khác (VD: marketing, bán dữ liệu)
- [ ] **Xóa dữ liệu ngay** khi hoàn thành mục đích (VD: sau khi xuất PDF)
- [ ] Nếu người dùng chọn lưu → ghi rõ thời gian lưu tối đa
- [ ] **Audit log** về thời điểm xóa dữ liệu

**Best Practice:**
- ✅ Xóa file upload **ngay lập tức** sau khi tạo báo cáo (trừ khi user chọn lưu)
- ✅ Nếu lưu tạm → tối đa 24-48 giờ, sau đó tự động xóa
- ✅ Không lưu dữ liệu "just in case" - chỉ lưu khi cần thiết

**EN:**
- [ ] Data shall be used **only for stated purpose**
- [ ] **SHALL NOT** use for other purposes (e.g., marketing, selling data)
- [ ] **Delete data immediately** when purpose is fulfilled (e.g., after PDF export)
- [ ] If user opts to save → clearly state maximum retention period
- [ ] **Audit log** of data deletion timestamps

**Best Practice:**
- ✅ Delete uploaded file **immediately** after report generation (unless user saves)
- ✅ If temporary storage → max 24-48 hours, then auto-delete
- ✅ Don't store data "just in case" - only when necessary

**Action:**
```
□ Purpose limitation enforced: YES / NO
□ Auto-deletion after processing: ACTIVE / INACTIVE
□ Max retention period defined: __________ hours
□ Deletion audit log: ACTIVE / INACTIVE
```

---

### ☑️ 6. Phản hồi yêu cầu của chủ thể dữ liệu trong 72 giờ

**VN:**
- [ ] Cung cấp cơ chế để người dùng thực hiện các quyền:
  1. ✅ **Quyền truy cập** - Xem dữ liệu cá nhân đang được lưu trữ
  2. ✅ **Quyền rút lại đồng ý** - Hủy quyền xử lý dữ liệu
  3. ✅ **Quyền xóa dữ liệu** - Yêu cầu xóa toàn bộ dữ liệu
  4. ✅ **Quyền hạn chế xử lý** - Yêu cầu tạm dừng xử lý
  5. ✅ **Quyền phản đối** - Phản đối việc xử lý dữ liệu

- [ ] **Phản hồi trong vòng 72 giờ** (bắt buộc theo luật)
- [ ] Tạo hệ thống tracking để đảm bảo không quá hạn
- [ ] Cung cấp email/form liên hệ: support@DataAnalytics.vn

**EN:**
- [ ] Provide mechanism for users to exercise rights:
  1. ✅ **Right to access** - View personal data being stored
  2. ✅ **Right to withdraw consent** - Revoke data processing permission
  3. ✅ **Right to delete** - Request deletion of all data
  4. ✅ **Right to restrict** - Request processing pause
  5. ✅ **Right to object** - Object to data processing

- [ ] **Respond within 72 hours** (legally required)
- [ ] Create tracking system to ensure deadline compliance
- [ ] Provide contact email/form: support@DataAnalytics.vn

**Action:**
```
□ Data subject request form: CREATED / NOT CREATED
□ 72-hour response system: ACTIVE / INACTIVE
□ Tracking system: IMPLEMENTED / NOT IMPLEMENTED
□ Contact email published: YES / NO
```

---

### ☑️ 7. Bảo mật & Báo cáo sự cố trong 72 giờ

**VN:**
- [ ] Áp dụng **biện pháp bảo mật kỹ thuật**:
  - ✅ HTTPS/TLS cho truyền tải dữ liệu
  - ✅ Mã hóa dữ liệu lưu trữ (encryption at rest)
  - ✅ Access control (chỉ người có quyền mới truy cập)
  - ✅ Audit logs (ghi nhận mọi truy cập dữ liệu)
  - ✅ Regular security updates (cập nhật bảo mật định kỳ)

- [ ] **Nếu có sự cố rò rỉ dữ liệu:**
  - ⚠️ **Báo cáo Bộ Công an trong vòng 72 giờ** (bắt buộc)
  - Chuẩn bị sẵn **Incident Response Plan**
  - Chuẩn bị sẵn **mẫu thông báo cho Bộ Công an**

**EN:**
- [ ] Implement **technical security measures**:
  - ✅ HTTPS/TLS for data transmission
  - ✅ Encryption at rest for stored data
  - ✅ Access control (only authorized personnel)
  - ✅ Audit logs (record all data access)
  - ✅ Regular security updates

- [ ] **If data breach occurs:**
  - ⚠️ **Report to MPS within 72 hours** (mandatory)
  - Prepare **Incident Response Plan**
  - Prepare **MPS notification template**

**Action:**
```
□ HTTPS/TLS enabled: YES / NO
□ Encryption at rest: YES / NO
□ Access control implemented: YES / NO
□ Audit logs active: YES / NO
□ Incident Response Plan: PREPARED / NOT PREPARED
□ MPS notification template: READY / NOT READY
```

---

## 📋 CHECKLIST - STAGE 3: ONGOING COMPLIANCE

### ☑️ 8. Rà soát & cập nhật định kỳ

**VN:**
- [ ] **Rà soát Chính sách Bảo mật** mỗi 6 tháng
- [ ] **Cập nhật Impact Assessment** khi có thay đổi về xử lý dữ liệu
- [ ] **Theo dõi thay đổi pháp lý** (Draft PDPL đang được soạn thảo)
- [ ] **Đào tạo nhân viên** (nếu có) về bảo vệ dữ liệu cá nhân
- [ ] **Kiểm tra audit logs** định kỳ để phát hiện bất thường

**EN:**
- [ ] **Review Privacy Policy** every 6 months
- [ ] **Update Impact Assessment** when data processing changes
- [ ] **Monitor regulatory changes** (Draft PDPL being drafted)
- [ ] **Train staff** (if any) on personal data protection
- [ ] **Check audit logs** regularly for anomalies

**Schedule:**
```
□ Next Privacy Policy review: __________
□ Next Impact Assessment update: __________
□ Regulatory monitoring: ACTIVE / INACTIVE
□ Staff training: COMPLETED / NOT APPLICABLE
□ Last audit log review: __________
```

---

### ☑️ 9. Chuẩn bị cho thanh tra của Bộ Công an

**VN:**
- [ ] Lưu trữ đầy đủ hồ sơ:
  - ✅ Impact Assessment Dossier (original)
  - ✅ Cross-Border Transfer Assessment (if applicable)
  - ✅ Consent records (audit logs)
  - ✅ Data deletion records
  - ✅ DPO appointment letter & training certificate
  - ✅ Privacy Policy (current + historical versions)
  - ✅ Data Processing Agreements (with third parties)

- [ ] **Sẵn sàng cung cấp cho Bộ Công an bất cứ lúc nào**
- [ ] Bộ Công an có thể thanh tra:
  - ✅ Bất cứ lúc nào (không cần báo trước)
  - ✅ 1 lần/năm cho cross-border transfers
  - ✅ Khi có khiếu nại hoặc nghi ngờ vi phạm

**EN:**
- [ ] Maintain complete records:
  - ✅ Impact Assessment Dossier (original)
  - ✅ Cross-Border Transfer Assessment (if applicable)
  - ✅ Consent records (audit logs)
  - ✅ Data deletion records
  - ✅ DPO appointment letter & training certificate
  - ✅ Privacy Policy (current + historical versions)
  - ✅ Data Processing Agreements (with third parties)

- [ ] **Ready to provide to MPS at any time**
- [ ] MPS can inspect:
  - ✅ At any time (no advance notice required)
  - ✅ Once per year for cross-border transfers
  - ✅ When complaints or suspected violations occur

**Action:**
```
□ All records maintained: YES / NO
□ Records accessible for inspection: YES / NO
□ Record retention period: __________ years
□ Backup of records: YES / NO
```

---

### ☑️ 10. ISO/IEC 27701 Alignment (Tùy chọn - Nâng cao uy tín)

**VN:**
- [ ] (Tùy chọn) Tuân thủ **ISO/IEC 27701:2019** - Privacy Information Management
- [ ] Lợi ích:
  - ✅ Tăng uy tín quốc tế
  - ✅ Dễ hợp tác với đối tác nước ngoài
  - ✅ Chứng minh "best practice" khi thanh tra
  - ✅ Giảm rủi ro pháp lý

- [ ] Chi phí: $3,000-8,000 cho certification (tùy chọn)
- [ ] Có thể tự áp dụng nguyên tắc ISO 27701 mà không cần certification

**EN:**
- [ ] (Optional) Align with **ISO/IEC 27701:2019** - Privacy Information Management
- [ ] Benefits:
  - ✅ Increase international credibility
  - ✅ Easier collaboration with foreign partners
  - ✅ Demonstrate "best practice" during inspection
  - ✅ Reduce legal risk

- [ ] Cost: $3,000-8,000 for certification (optional)
- [ ] Can self-implement ISO 27701 principles without certification

**Action:**
```
□ ISO 27701 alignment: YES / NO / PLANNED
□ Certification obtained: YES / NO / NOT PLANNED
□ Internal audit: COMPLETED / NOT APPLICABLE
```

---

## 💰 CHI PHÍ TUÂN THỦ / COMPLIANCE COSTS

### Phương án LEAN (Solo Founder)

**Chi phí 1 lần (One-Time):**
- Tư vấn pháp lý cơ bản: $300-500 ✅
- Đào tạo DPO (nếu tự làm): $300-600 ✅
- Template & implementation (I'll create): $0 ✅✅✅
- **Tổng:** $600-1,100

**Chi phí hàng năm (Ongoing):**
- DPO part-time (tự làm): $0 ✅✅✅
- Rà soát 6 tháng/lần (tự làm): $0 ✅✅✅
- Cập nhật MPS submissions: $200-400
- **Tổng:** $200-400/năm

### Phương án PROFESSIONAL (Khi scale)

**Chi phí 1 lần:**
- Tư vấn pháp lý toàn diện: $800-1,500
- Impact Assessment (thuê viết): $800-1,500
- DPO training: $300-600
- Technical implementation: $500-1,000
- **Tổng:** $2,400-4,600

**Chi phí hàng năm:**
- DPO outsource: $3,600-9,600 ($300-800/month)
- Compliance review: $500-1,000
- MPS submissions: $200-400
- **Tổng:** $4,300-11,000/năm

---

## ⚖️ HÌNH PHẠT VI PHẠM / PENALTIES

**Hành chính (Administrative):**
- Phạt tiền (chưa có mức cụ thể - chờ Nghị định xử phạt)
- Tạm ngừng xử lý dữ liệu
- Thu hồi giấy phép kinh doanh

**Hình sự (Criminal):**
- Khởi tố khi gây thiệt hại nghiêm trọng
- Vi phạm an ninh quốc gia

**Uy tín (Reputational):**
- **"Một lần bất tin, vạn lần bất tín"**
- Mất niềm tin khách hàng
- Khó khăn trong hợp tác quốc tế

---

## ✅ NGUỒN THAM KHẢO / SOURCES

1. **Nghị định 13/2023/NĐ-CP** (Official Government Decree)
2. **Bộ Công an** - Ministry of Public Security (Enforcement Authority)
3. **KPMG Vietnam** - Legal Alert April 2023
4. **Watson Farley & Williams** - International Law Firm Analysis
5. **Lexology** - Legal Compliance Database
6. **Viet An Law** - Vietnamese Law Firm

**Độ tin cậy / Reliability:** ⭐⭐⭐⭐⭐

---

## 📞 LIÊN HỆ / CONTACT

**Để được hỗ trợ tuân thủ:**
- Email: support@DataAnalytics.vn
- Legal consultation: (Partner with Vietnamese law firm)

**Cơ quan chức năng:**
- Bộ Công an - Cục An ninh mạng và Phòng chống tội phạm sử dụng công nghệ cao
- Website: https://www.mps.gov.vn
- Hotline: (024) 3942 8526

---

**DISCLAIMER:** Đây là hướng dẫn giáo dục, không phải tư vấn pháp lý. Vui lòng tham khảo luật sư Việt Nam có giấy phép cho tình huống cụ thể của bạn.

**DISCLAIMER:** This is educational guidance, not legal advice. Please consult a licensed Vietnamese lawyer for your specific situation.

---

**Version History:**
- v1.0 (2025-10-28): Initial release based on Decree 13/2023/ND-CP + deep research validation
- Next review: 2026-04-28 (6 months)
