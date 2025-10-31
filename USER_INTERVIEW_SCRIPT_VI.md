# 🎤 KỊCH BẢN PHỎNG VẤN NGƯỜI DÙNG (3 DOMAINS)

**Mục đích**: Thu thập phản hồi thật từ real users để quyết định domain nào cần deep dive FIRST

**Thời gian**: 30 phút/người dùng  
**Phương thức**: Zalo call + Screen share (hoặc gặp mặt)  
**Ghi chép**: Record (xin phép trước) + Take notes

---

## 📋 CHUẨN BỊ TRƯỚC KHI PHỎNG VẤN

### Thông tin cần có sẵn:
- [ ] Production URL của app
- [ ] Microsoft Clarity đã setup (để record session)
- [ ] Máy record sẵn sàng (Zoom/OBS)
- [ ] Notebook ghi chú sẵn sàng
- [ ] Sample CSV file (nếu user không có data)

### Kịch bản mở đầu (1 phút):
```
"Chào anh/chị, cảm ơn anh/chị đã dành thời gian. 

Tôi đang phát triển tool phân tích dữ liệu cho SME Việt Nam, 
hoàn toàn MIỄN PHÍ, để giúp chủ shop/cửa hàng hiểu rõ hơn về 
doanh số, khách hàng của mình.

Hôm nay tôi muốn anh/chị trải nghiệm tool và cho tôi biết:
- Cái gì tốt, cái gì chưa tốt
- Anh/chị có thực sự dùng nó không
- Cần thêm tính năng gì

Không có câu trả lời đúng hay sai, tôi muốn nghe ý kiến THẬT của anh/chị.

Tôi có thể record lại không? (chỉ để ghi chú, không share ra ngoài)"

[Chờ đồng ý]

"Ok, bắt đầu nhé!"
```

---

## 🛒 DOMAIN 1: E-COMMERCE (Shopee/Lazada/Tiki Seller)

### PHẦN 1: HIỂU CONTEXT (5 phút)

**Câu hỏi khởi động**:
1. "Anh/chị bán gì trên Shopee/Lazada?"
2. "Bao nhiêu đơn hàng/tháng?"
3. "Hiện tại anh/chị dùng gì để xem doanh số?" (Excel? Shopee report?)
4. "Anh/chị thường xem những chỉ số nào?" (doanh thu, đơn hàng, conversion?)

**Ghi chú quan trọng**:
- Pain point hiện tại của họ (Excel phức tạp? Shopee report không đủ?)
- Metric nào họ THỰC SỰ care (revenue? conversion? AOV?)

---

### PHẦN 2: TRẢI NGHIỆM TOOL (15 phút)

**Hướng dẫn**:
```
"Giờ tôi gửi link tool cho anh/chị qua Zalo.

[Gửi production URL]

Anh/chị thử upload file CSV dữ liệu Shopee lên xem sao.
(Nếu không có file, tôi có file mẫu đây)

[Share sample CSV nếu cần]

Anh/chị cứ làm như bình thường, tôi quan sát thôi.
Nếu thắc mắc gì, cứ nói to ra!"
```

**Quan sát (GHI CHÚ TỪNG HÀNH ĐỘNG)**:
- [ ] Upload file có gặp khó khăn không?
- [ ] Nhìn vào đâu đầu tiên? (Status banner? Top 3 KPIs? Charts?)
- [ ] Đọc được Top 3 KPIs không? (hiểu nghĩa không?)
- [ ] Có click "Xem thêm 9 chỉ số" không? Tự nhiên hay phải gợi ý?
- [ ] Khi xem hết 12 KPIs, họ focus vào KPI nào? (ghi lại!)
- [ ] Có scroll xuống xem charts không?
- [ ] Biểu hiện: Confused? Excited? Bored? (ghi lại biểu cảm)

**Câu hỏi khi họ đang dùng**:
- "Anh/chị đang nghĩ gì?" (khi họ dừng lại)
- "Cái này có ý nghĩa gì với anh/chị?" (khi họ nhìn 1 KPI)
- "Anh/chị muốn làm gì tiếp theo?" (sau khi xem xong)

---

### PHẦN 3: FEEDBACK SÂU (8 phút)

**Block 1: Overall Impression**
1. **"Nhìn chung, anh/chị cảm thấy tool này thế nào?" (1-5 scale)**
   - 1 = Rất tệ
   - 2 = Tệ
   - 3 = Bình thường
   - 4 = Tốt
   - 5 = Rất tốt
   
   [GHI ĐIỂM + LÝ DO]

2. **"Cái gì anh/chị THÍCH NHẤT?"**
   - Ghi verbatim (nguyên văn câu nói)
   - Nếu họ nói "Dễ dùng" → Hỏi tiếp: "Dễ ở chỗ nào cụ thể?"

3. **"Cái gì anh/chị KHÓ HIỂU/KHÓ DÙNG NHẤT?"**
   - Ghi verbatim
   - Nếu họ nói "Không có" → Hỏi tiếp: "Có điểm nào anh/chị phải suy nghĩ lâu không?"

---

**Block 2: Feature-Specific (E-commerce)**

4. **"Anh/chị có để ý chỉ số 'Cart Abandonment Rate' (Tỷ lệ rời bỏ giỏ hàng) không?"**
   - Yes → "Anh/chị hiểu nghĩa không? Có hữu ích không?"
   - No → "Tại sao không chú ý?"
   
   **CRITICAL**: Nếu họ thấy hữu ích, hỏi:
   - "Nếu tool tự động BÁO ĐỘNG khi cart abandonment tăng đột ngột, anh/chị có dùng không?"
   - "Nếu có GỢI Ý cách giảm cart abandonment (giảm bước checkout, thêm COD...), anh/chị có làm theo không?"

5. **"Anh/chị có thấy phần so sánh channels (Facebook vs Organic vs TikTok) không?"**
   - Yes → "Hữu ích không? Muốn xem chi tiết gì thêm?"
   - No → "Nếu tool show chi tiết kênh nào bán tốt nhất, anh/chị có muốn không?"

6. **"Top 3 KPIs (Doanh thu, Conversion, AOV) có PHẢI là những gì anh/chị quan tâm nhất không?"**
   - Yes → Good!
   - No → "Vậy anh/chị muốn thấy KPI nào ở top 3?" [GHI LẠI!]

---

**Block 3: Comparison & Value**

7. **"So với cách anh/chị đang dùng (Excel/Shopee report), tool này khác gì?"**
   - Tốt hơn ở đâu?
   - Tệ hơn ở đâu?
   - Nhanh hơn? Dễ hiểu hơn?

8. **"Nếu tool này có thêm tính năng [XYZ], anh/chị có dùng thường xuyên không?"**
   
   **Test 3 features** (đọc lần lượt, ghi reaction):
   - Feature A: "Cảnh báo tự động khi chỉ số quan trọng giảm" (push Zalo)
   - Feature B: "So sánh với shop cùng ngành (benchmark)" (anonymous)
   - Feature C: "Gợi ý hành động cụ thể để tăng doanh thu" (AI-powered)
   
   Hỏi mỗi feature:
   - "Có hữu ích không?" (1-5 scale)
   - "Anh/chị có dùng không?" (Yes/No)

---

**Block 4: Willingness to Pay (CRITICAL)**

9. **"Nếu tool này hoàn toàn MIỄN PHÍ, anh/chị có dùng hàng ngày/hàng tuần không?"**
   - Yes → "Bao lâu 1 lần?"
   - No → "Tại sao?" [Pain point không đủ lớn?]

10. **"Nếu tool này giúp anh/chị TĂNG 5-10% doanh thu/tháng, anh/chị có SẴN SÀNG TRẢ TIỀN không?"**
    - Yes → "Bao nhiêu anh/chị thấy hợp lý?"
      - ₫50K/tháng?
      - ₫99K/tháng?
      - ₫199K/tháng?
      - Khác?
    - No → "Tại sao?" [Trust issue? Budget issue?]

11. **"Anh/chị có GIỚI THIỆU cho seller khác không?"**
    - Yes → "Anh/chị sẽ nói gì về tool này?"
    - No → "Tại sao?" [Tool chưa đủ tốt? Hay ngại giới thiệu?]

---

### PHẦN 4: CLOSING (2 phút)

**Wrap up**:
```
"Cảm ơn anh/chị rất nhiều!

Feedback của anh/chị rất giá trị với tôi.
Tôi sẽ cải thiện tool dựa trên ý kiến này.

Khi tool có version mới (trong 1-2 tuần),
tôi có thể gửi lại cho anh/chị test không?

[Nếu đồng ý] Tuyệt vời! Tôi sẽ giữ liên lạc qua Zalo.

Cuối cùng, nếu tôi quote lại câu nói của anh/chị
(ẩn danh) để làm testimonial, anh/chị ok không?

[Ví dụ: 'Tool này giúp tôi tiết kiệm 30 phút mỗi ngày' - Seller Shopee]"
```

**Ghi chú cuối**:
- [ ] User đồng ý follow-up
- [ ] User đồng ý testimonial
- [ ] Zalo contact saved
- [ ] Best quote for testimonial (ghi lại)

---

## 🏬 DOMAIN 2: RETAIL (Physical Store Owner)

**Cùng structure như E-commerce**, nhưng thay đổi:

### Feature-Specific Questions (thay thế câu 4-6):

4. **"Anh/chị có để ý phần inventory (hàng tồn kho) không?"**
   - "Nếu tool BÁO ĐỘNG sản phẩm nào tồn kho lâu >90 ngày, anh/chị có muốn không?"
   - "Nếu có GỢI Ý: 'Giảm giá 30% để clear stock', anh/chị có làm theo không?"

5. **"Anh/chị có quan tâm đến hiệu suất từng nhân viên không?"**
   - "Nếu tool show: Lan bán ₫180K/giờ, Minh bán ₫90K/giờ, anh/chị thấy hữu ích không?"
   - "Có lo ngại gì không?" (nhân viên phản ứng? privacy?)

6. **"Anh/chị có muốn biết giờ nào khách đông nhất không?"**
   - "Để làm gì?" (schedule nhân viên? order hàng?)
   - "Nếu có heatmap giờ cao điểm, anh/chị có dùng không?"

---

## 💆 DOMAIN 3: SERVICES (Spa/Salon/Clinic/Gym)

**Cùng structure**, thay đổi:

### Feature-Specific Questions:

4. **"Anh/chị có vấn đề khách book mà không đến (no-show) không?"**
   - "Bao nhiêu % khách no-show?" (ghi lại)
   - "Nếu tool TRACK no-show rate + GỢI Ý: 'Yêu cầu deposit ₫50K', anh/chị có làm không?"

5. **"Anh/chị có bán gói (package) không?"**
   - "Bao nhiêu % khách mua gói vs lẻ?"
   - "Nếu tool show: 'Chỉ 15% khách mua gói, chuẩn là 30%', anh/chị có muốn cải thiện không?"
   - "Nếu có GỢI Ý upsell script, anh/chị có train nhân viên dùng không?"

6. **"Anh/chị có track khách quay lại không?"**
   - "Bao nhiêu % khách quay lại trong 30 ngày?"
   - "Nếu tool tính Customer Lifetime Value, anh/chị có muốn không?"

---

## 📊 SCORING MATRIX (Sau Mỗi Interview)

### Quantitative Scores (1-5 scale):
```yaml
User ID: [E-commerce-1 / Retail-1 / Services-1]
Date: [YYYY-MM-DD]
Duration: [XX minutes]

Scores:
1. Overall Satisfaction: [1-5]
2. Ease of Use: [1-5]
3. Usefulness: [1-5]
4. Would Use Regularly: [1-5]
5. Would Recommend: [1-5]
6. Willingness to Pay: [1-5]
   (1=Never, 3=Maybe ₫50K, 5=Yes ₫199K+)

TOTAL SCORE: [/30]
```

### Qualitative Notes:
```yaml
Top 3 Likes:
1. [Quote]
2. [Quote]
3. [Quote]

Top 3 Dislikes/Confusions:
1. [Quote]
2. [Quote]
3. [Quote]

Feature Requests:
1. [Specific feature]
2. [Specific feature]
3. [Specific feature]

Best Testimonial Quote:
"[Exact quote từ user]"

Willingness to Pay:
- Amount: ₫[XX]K/month
- Condition: [If XYZ feature exists]

Follow-up:
- OK to contact again? [Yes/No]
- Zalo: [Phone number]
```

---

## 🎯 DECISION CRITERIA (After 3 Interviews)

### High Priority Domain (Deep Dive First) if:
```yaml
Criteria:
✅ Average satisfaction score >4.0/5.0
✅ >2/3 users would use regularly
✅ >2/3 users willing to pay ≥₫99K/month
✅ Clear, specific feature requests (not vague)
✅ Users have ACUTE pain (not nice-to-have)
✅ Users excited (not just polite)

Red Flags (Skip Domain):
❌ Satisfaction score <3.5/5.0
❌ Users say "I'll stick to Excel for now"
❌ Can't articulate what they'd use it for
❌ No willingness to pay (even if free value is high)
❌ Feature requests too complex (need enterprise features)
```

### Ranking Formula:
```python
Domain_Score = (
    (Satisfaction * 2) +      # Weight 2x
    (Usefulness * 2) +         # Weight 2x
    (Would_Use_Regularly * 1.5) +
    (Willingness_to_Pay * 3) + # Weight 3x (revenue potential)
    (Would_Recommend * 1)
) / 9.5

# Range: 1-5
# >4.0 = High Priority
# 3.5-4.0 = Medium Priority
# <3.5 = Low Priority
```

---

## 📝 REPORTING TEMPLATE (End of Phase 1)

### File: `USER_TESTING_REPORT_PHASE1.md`

```markdown
# USER TESTING REPORT - PHASE 1

**Testing Period**: [Start Date] - [End Date]
**Users Tested**: 3 (1 E-commerce, 1 Retail, 1 Services)

---

## EXECUTIVE SUMMARY

**Highest Priority Domain**: [E-commerce / Retail / Services]

**Why**:
- Highest Domain_Score: [X.XX / 5.0]
- Most acute pain point: [Describe]
- Willingness to pay: [X/3 users @ ₫XXK/month]
- Clear feature requests: [List top 3]

**Recommendation**: Deep dive [Domain] in Phase 2

---

## DETAILED FINDINGS

### E-commerce Domain
- User: [Anonymous ID]
- Score: [X.XX / 5.0]
- Key Quote: "[Testimonial]"
- Pain Point: [Describe]
- Feature Requests: [List]
- WTP: ₫[XX]K/month

### Retail Domain
[Same structure]

### Services Domain
[Same structure]

---

## PRIORITY RANKING

1. [Domain A]: [Score] - [Reason]
2. [Domain B]: [Score] - [Reason]
3. [Domain C]: [Score] - [Reason]

---

## NEXT STEPS (Phase 2)

Focus on [Winning Domain]:
1. Build feature [A] (from user request #1)
2. Build feature [B] (from user request #2)
3. Build feature [C] (from user request #3)
4. Re-test with 5 users from same domain
5. Iterate based on feedback

Timeline: Week 2 (7 days)
Budget: ₫170K (20 hours)
```

---

## ✅ CHECKLIST SUMMARY

Before each interview:
- [ ] Production URL ready
- [ ] Clarity recording enabled
- [ ] Recording tool ready
- [ ] Notebook ready
- [ ] Sample CSV prepared (if needed)

During interview:
- [ ] Record session (with permission)
- [ ] Take verbatim notes
- [ ] Observe natural behavior
- [ ] Ask follow-up questions
- [ ] Don't lead user

After interview:
- [ ] Fill scoring matrix immediately
- [ ] Extract best testimonial quote
- [ ] Save Zalo contact (if follow-up OK)
- [ ] Update comparison table

After 3 interviews:
- [ ] Calculate Domain_Score for each
- [ ] Write USER_TESTING_REPORT_PHASE1.md
- [ ] Decide which domain to deep dive
- [ ] Plan Phase 2 features

---

**Status**: ✅ SCRIPT READY
**Next**: Run interviews with 3 real users (1 per domain)
