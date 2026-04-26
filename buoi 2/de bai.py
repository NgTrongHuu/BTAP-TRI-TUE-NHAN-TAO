"""
## 2.11. TÌNH HUỐNG 1: HỆ THỐNG GIÁ TIỀN GRAB-BIKE

Hệ thống giá và tiền thưởng thay đổi của Grab cho các chuyến đi GrabBike dựa trên nhiều yếu tố ngoài khoảng cách. Có các lý do tại sao hai chuyến đi cùng khoảng cách có thể có giá khác nhau và điểm thưởng cho các tài xế là khác nhau. GrabBike sử dụng mô hình định giá động, điều chỉnh giá cước dựa trên các yếu tố thời gian thực. Bên cạnh đó, nếu nhiều người đặt GrabBike cùng lúc, giá cước sẽ tăng do nhu cầu cao và tài xế có hạn, ngoài giờ cao điểm, giá cước sẽ thấp hơn.

Ngoài ra điều kiện giao thông ở Việt Nam cũng ảnh hưởng tới giá cước đưa ra của hệ thống, giao thông đông đúc làm tăng thời gian di chuyển và mức tiêu thụ nhiên liệu. Grab có thể tính giá cước cao hơn ở những khu vực đông đúc. Nếu tuyến đường thông thoáng, giá cước có thể thấp hơn. Đôi khi, giá cước được điều chỉnh dựa trên mức độ khó khăn khi đón khách (ví dụ: bên trong trung tâm thương mại, sân bay hoặc khu vực có lưu lượng giao thông cao). Nếu địa điểm trả khách ở khu vực hẻo lánh, Grab có thể tăng giá cước vì tài xế khó có thể gọi thêm chuyến nữa. Giờ cao điểm buổi sáng (7 giờ sáng - 9 giờ sáng) và giờ cao điểm buổi tối (5 giờ chiều - 8 giờ tối) thường có giá vận chuyển cao hơn do nhu cầu tăng cao. Khi đêm muộn (nửa đêm - 5 giờ sáng) cũng có giá vận chuyển có thể thấp hơn. Ngoài ra có thể sử dụng voucher để Grab giảm giá tiền các chuyến vận chuyển. Bên cạnh đó, GrabBike tặng điểm thưởng để khích lệ và thưởng cho tài xế dựa trên hiệu suất. Điểm thưởng có thể được quy đổi thành tiền mặt hoặc các phần thưởng khác. Sau đây là lý do tại sao tài xế nhận được điểm thưởng:

* **Hoàn thành một số chuyến đi nhất định:** Grab cung cấp các ưu đãi khi hoàn thành X chuyến đi mỗi ngày hoặc mỗi tuần (ví dụ: hoàn thành 10 chuyến đi = điểm thưởng).
* **Chấp nhận chuyến đi trong giờ cao điểm:** Nếu tài xế làm việc trong giờ cao điểm, Grab có thể tặng tài xế thêm điểm để họ luôn chủ động khi nhu cầu cao.
* **Xếp hạng khách hàng cao:** Nếu tài xế liên tục nhận được xếp hạng tốt (4,5 sao trở lên), họ sẽ nhận được điểm thưởng như một phần thưởng cho dịch vụ tốt.
* **Hoàn thành các chuyến đi đường dài:** Một số chuyến đi đường dài giúp tài xế kiếm thêm điểm vì mất nhiều thời gian và công sức hơn.
* **Lái xe trong thời tiết xấu:** Nếu tài xế nhận chuyến đi trong thời tiết mưa lớn, Grab có thể tặng họ thêm điểm để khuyến khích nhiều tài xế trực tuyến hơn.
* **Duy trì tỷ lệ chấp nhận cao:** Những tài xế chấp nhận hầu hết các chuyến đi (thay vì hủy chuyến) sẽ nhận được nhiều điểm thưởng hơn như một phần thưởng.

Hệ thống giá và tiền thưởng của GrabBike được thiết kế để cân bằng cung và cầu, thưởng cho những tài xế tốt và điều chỉnh giá về dựa trên các điều kiện thực tế. Đối với hành khách: Giá vận chuyển thay đổi tùy theo nhu cầu, giao thông, địa điểm, thời tiết và chương trình khuyến mãi. Đối với tài xế thì điểm thưởng khuyến khích họ làm việc ở những khu vực có nhu cầu cao, nhận thêm nhiều chuyến xe hơn và cung cấp dịch vụ tốt.

### 1. Biến vào
* **Quãng đường/Ride Distance (km):** Short/Ngắn (0 - 3 km); Trung bình/Medium (2 - 8 km); Dài/Long (6 - 20 km); Rất xa/Very Long (15 - 50 km)
* **Tình trạng giao thông (lưu lượng)/Traffic Condition:** Thấp/Low (Tắc nghẽn 0 - 30%); Trung bình/Medium (20 - 70%); Cao/High (60 - 100%)
* **Mức cầu/Demand Level (Có bao nhiêu người đặt xe tại thời điểm đó):** Thấp/Low (0 - 30%); Trung bình/Medium (20 - 70%); Cao/High (60 - 100%)
* **Điều kiện khí hậu/Weather Condition:** Tốt/Good (Thời tiết quang đãng/Clear weather); Trung bình/Moderate (Mưa nhẹ/Light rain); Xấu/Bad (Mưa to, bão/Heavy rain, storm)
* **Customer Rating/Đánh giá của khách hàng:** Kém/Poor (1.0 - 2.5); Trung bình/Average (2.0 - 4.0); Tốt/Good (3.5 - 5.0)
* **Đúng giờ/Ride Punctuality:** Trễ/Late (0 - 50%); Đúng giờ/On Time (40 - 80%); Sớm/Early (70 - 100%)

### 2. Biến đầu ra
* **Giá đi xe:** Thấp/Low; Trung bình/Medium; Cao/High; Rất cao/Very High
* **Điểm thưởng cho khách hàng:** Không có/None; Ít/Few; Trung bình/Moderate; Cao/High

### LUẬT MỜ ĐỀ XUẤT
1.  Nếu (Khoảng cách ngắn) VÀ (Lưu lượng thấp) VÀ (Nhu cầu thấp), THÌ Giá thấp.
2.  Nếu (Khoảng cách ngắn) VÀ (Lưu lượng trung bình) VÀ (Nhu cầu cao), THÌ Giá trung bình.
3.  Nếu (Khoảng cách trung bình) VÀ (Lưu lượng cao) VÀ (Nhu cầu cao), THÌ Giá cao.
4.  Nếu (Khoảng cách xa) VÀ (Lưu lượng trung bình) VÀ (Thời tiết tốt), THÌ Giá trung bình.
5.  Nếu (Khoảng cách xa) VÀ (Lưu lượng cao) VÀ (Thời tiết xấu), THÌ Giá rất cao.
6.  Nếu (Khoảng cách rất xa) VÀ (Lưu lượng cao) VÀ (Nhu cầu cao), THÌ Giá rất cao.
7.  Nếu (Khoảng cách trung bình) VÀ (Lưu lượng thấp) VÀ (Nhu cầu thấp), THÌ Giá trung bình.
8.  Nếu (Khoảng cách ngắn) VÀ (Lưu lượng giao thông cao) VÀ (Thời tiết xấu), THÌ Giá cao.
9.  Nếu (Khoảng cách rất xa) VÀ (Thời tiết xấu), THÌ Giá rất cao.
10. Nếu (Khoảng cách trung bình) VÀ (Lưu lượng giao thông trung bình) VÀ (Thời tiết vừa phải), THÌ Giá trung bình.
11. Nếu (Đánh giá của khách hàng tốt) VÀ (Đúng giờ sớm), THÌ Điểm thưởng cao.
12. Nếu (Đánh giá của khách hàng trung bình) VÀ (Đúng giờ đúng giờ), THÌ Điểm thưởng trung bình.
13. Nếu (Đánh giá của khách hàng kém) VÀ (Đúng giờ muộn), THÌ Điểm thưởng không có.
14. Nếu (Khoảng cách dài) VÀ (Lưu lượng giao thông cao) VÀ (Đi xe đúng giờ đúng giờ), THÌ Điểm thưởng cao.
15. Nếu (Khoảng cách là Trung bình) VÀ (Giao thông là Trung bình) VÀ (Xếp hạng của Khách hàng là Tốt), THÌ Điểm thưởng là Trung bình.
16. Nếu (Xếp hạng của Khách hàng là Kém) VÀ (Đúng giờ là Trễ), THÌ Điểm thưởng là Không có.
17. Nếu (Khoảng cách là Rất xa) VÀ (Thời tiết xấu) VÀ (Xếp hạng của Khách hàng là Tốt), THÌ Điểm thưởng là Cao.
18. Nếu (Khoảng cách là Ngắn) VÀ (Xếp hạng của Khách hàng là Trung bình) VÀ (Đúng giờ là Đúng giờ), THÌ Điểm thưởng là Ít.
19. Nếu (Khoảng cách là Dài) VÀ (Giao thông là Cao) VÀ (Đúng giờ là Trễ), THÌ Điểm thưởng là Ít.
20. Nếu (Khoảng cách là Trung bình) VÀ (Thời tiết là Trung bình) VÀ (Xếp hạng của Khách hàng là Tốt), THÌ Điểm thưởng là Trung bình.

---

## 2.12. TÌNH HUỐNG 2: CHIẾN LƯỢC CHIẾT KHẤU CHO KHÁCH HÀNG Ở CÁC CỬA HÀNG SHOPEE

Trên Shopee, các cửa hàng sử dụng chiết khấu để thu hút khách hàng, tăng doanh số và duy trì khả năng cạnh tranh. Tuy nhiên, việc cung cấp chiết khấu đi kèm với một sự đánh đổi đó là quá nhiều chiết khấu có thể làm giảm lợi nhuận, trong khi quá ít có thể làm khách hàng nản lòng. Một chiến lược chiết khấu thông minh giúp cân bằng các yếu tố này. Các cửa hàng lại giảm giá trên Shopee nhằm:

* **Thu hút nhiều khách hàng hơn:** Giảm giá giúp tăng khả năng hiển thị trên kết quả tìm kiếm của Shopee. Khách hàng thích giá thấp hơn và có nhiều khả năng mua hàng hơn. Các cửa hàng mới sử dụng giảm giá để thu hút khách hàng sớm.
* **Cạnh tranh với những người bán khác:** Đối với người tiêu dùng mua hàng trên Shopee rất nhạy cảm với giá cả; khách hàng so sánh các giao dịch do đó nếu đối thủ cạnh tranh giảm giá tốt hơn, cửa hàng có thể mất doanh số.
* **Tăng khối lượng đơn hàng và thứ hạng:** Doanh số cao hơn có thể cải thiện thứ hạng của cửa hàng, dẫn đến khả năng hiển thị trên giao diện dành cho người tiêu dùng cao hơn. Ngoài ra, khi khối lượng đơn hàng tăng giúp giảm chi phí lưu kho.
* **Khuyến khích mua hàng số lượng lớn:** Giảm giá cho các giá trị giỏ hàng cao hơn làm tăng kích thước đơn hàng trung bình. Đóng gói sản phẩm với các khoản giảm giá khuyến khích chi tiêu nhiều hơn.

Nhưng bên cạnh đó khi giảm giá dẫn đến việc đánh đổi biên lợi nhuận:
* **Rủi ro giảm giá quá mức:** Quá nhiều khoản giảm giá làm giảm lợi nhuận trên mỗi mặt hàng. Khi một số người mua chờ giảm giá, khiến việc bán với giá đầy đủ trở nên khó khăn. Nếu một cửa hàng phụ thuộc quá nhiều vào chiết khấu, họ có thể gặp khó khăn trong việc duy trì lợi nhuận.
* **Cân bằng lợi nhuận và chiết khấu:** Các cửa hàng phải phân tích chi phí và biên lợi nhuận trước khi đưa ra chiết khấu như đặt biên lợi nhuận tối thiểu (sau khi chiết khấu) và sử dụng chiết khấu theo từng bậc như chiết khấu cao hơn cho các đơn hàng số lượng lớn. Đưa ra chiết khấu cho các sản phẩm có biên lợi nhuận cao để bảo vệ lợi nhuận. Ngoài ra, sử dụng các ưu đãi có thời hạn để tạo sự cấp bách mà không phải giảm giá dài hạn.

Từ những yếu tố trên có các chiến lược chiết khấu phổ biến trên Shopee như:
* **Khuyến mãi chớp nhoáng (Flash Sale):** Giảm giá ngắn hạn để tăng tính cấp bách và thúc đẩy doanh số. Phổ biến trong các chiến dịch lớn của Shopee như các sự kiện (9.9, 11.11, 12.12, Black Friday).
* **Chiết khấu phiếu giảm giá:** Phiếu giảm giá cho toàn cửa hàng hoặc theo danh mục cụ thể (ví dụ: giảm 5.000 đồng cho các đơn hàng trên 50.000 đồng). Khuyến khích khách hàng chi tiêu nhiều hơn để mở khóa các khoản tiết kiệm.
* **Khuyến mãi theo gói:** Như các chiến dịch "Mua 2, giảm 10%" hoặc "Mua 1 tặng 1". Khuyến khích mua hàng số lượng lớn, tăng giá trị đơn hàng.
* **Hoàn tiền bằng Shopee voucher:** Khách hàng được hoàn lại % số tiền dưới dạng Shopee voucher. Khuyến khích mua hàng nhiều lần thay vì giảm giá trực tiếp.
* **Giảm giá miễn phí vận chuyển:** Shopee thường trợ cấp một phần phí vận chuyển. Khách hàng thích ưu đãi miễn phí vận chuyển hơn là giảm giá.

**Ví dụ: Tính toán chiến lược giảm giá với tình huống:**
Một cửa hàng bán một sản phẩm với giá 100.000 đồng. Giá thành (bao gồm phí) là 70.000 đồng. Với các tình huống có thể xảy ra như sau:
* **Không có giảm giá thì:**
    Giá bán = 100.000 đồng
    Chi phí = 70.000 đồng
    Lợi nhuận = 30.000 đồng (30%)
* **Có Giảm giá 20% (Giá 80.000 đồng):**
    Giá bán = 80.000 đồng
    Chi phí = 70.000 đồng
    Lợi nhuận = 10.000 đồng (10%)

**Giải pháp:** Cửa hàng có thể giảm giá khi mua số lượng lớn thay vì bán lẻ. Có thể áp dụng mức giảm giá 10% thay vì 20%, đảm bảo biên lợi nhuận ít nhất là 20%. Như vậy: Giảm giá thông minh để thành công trên Shopee nhằm giảm giá để thu hút khách hàng nhưng cần được quản lý cẩn thận. Các cửa hàng phải phân tích biên lợi nhuận trước khi thiết lập mức giảm giá. Các chiến lược năng động (giảm giá chớp nhoáng, phiếu giảm giá, gói sản phẩm) giúp duy trì lợi nhuận trong khi tăng doanh số.

Tại Shopee, các cửa hàng cung cấp các chương trình giảm giá để thu hút khách hàng trong khi vẫn cần cân bằng được biên lợi nhuận. Phương pháp logic mờ giúp xác định động mức giảm giá tốt nhất dựa trên các yếu tố chính.

### Biến đầu vào: Những đầu vào này ảnh hưởng đến quyết định giảm giá.
* **Đánh giá cửa hàng/Store Rating (Thấp/Low, Trung bình/Medium, Cao/High):** Thấp -> Dưới 4,0 sao; Trung bình -> 4,0 - 4,5 sao; Cao -> Trên 4,5 sao
* **Khối lượng bán hàng/Sales Volume (Thấp/Low, Trung bình/Medium, Cao/High):** Thấp -> Ít đơn hàng mỗi tháng; Trung bình -> Doanh số ổn định; Cao -> Số lượng đơn hàng lớn mỗi tháng
* **Biên lợi nhuận/Profit Margin (Thấp/Low, Trung bình/Medium, Cao/High):** Thấp -> Lợi nhuận nhỏ trên mỗi lần bán; Trung bình -> Lợi nhuận vừa phải; Cao -> Biên lợi nhuận lớn
* **Sự kiện theo mùa/Seasonal Event (Không có/None, Trung bình/Moderate, Cao/High):** Không có -> Thời gian mua sắm bình thường; Trung bình -> Sự kiện bán hàng nhỏ; Cao -> Sự kiện lớn như Shopee 9/9, 1/1, 12/12, Black Friday
* **Giảm giá của đối thủ cạnh tranh/Competitor Discounts (Thấp/Low, Trung bình/Medium, Cao/High):** Thấp -> Ít chương trình khuyến mãi của đối thủ; Trung bình -> Ưu đãi của đối thủ vừa phải; Cao -> Nhiều chiết khấu mạnh của đối thủ

### Biến đầu ra: Tỷ lệ phần trăm chiết khấu (%)
* Rất thấp (0-5%)
* Thấp (5-10%)
* Trung bình (10-20%)
* Cao (20-40%)
* Rất cao (40-70%)

### LUẬT MỜ
Những quy tắc này xác định cách phân bổ chiết khấu.
1. Nếu (Xếp hạng cửa hàng cao) VÀ (Khối lượng bán hàng cao) VÀ (Biên lợi nhuận cao) Thì Chiết khấu rất thấp (Không cần chiết khấu mạnh).
2. Nếu (Xếp hạng cửa hàng thấp) VÀ (Khối lượng bán hàng thấp) VÀ (Biên lợi nhuận cao) Thì Chiết khấu cao (Tăng doanh số với biên lợi nhuận tốt).
3. Nếu (Sự kiện theo mùa cao) VÀ (Chiết khấu của đối thủ cao) Thì Chiết khấu rất cao (Duy trì tính cạnh tranh trong các đợt bán hàng lớn).
4. Nếu (Xếp hạng cửa hàng là Trung bình) VÀ (Khối lượng bán hàng là Trung bình) VÀ (Biên lợi nhuận là Trung bình) Thì Chiết khấu là Trung bình (Khuyến khích mua nhiều hơn).
5. Nếu (Chiết khấu của đối thủ cạnh tranh là Thấp) VÀ (Biên lợi nhuận là Thấp) VÀ (Khối lượng bán hàng là Cao) Thì Chiết khấu là Rất thấp (Tối đa hóa lợi nhuận).
6. Nếu (Xếp hạng cửa hàng là Thấp) VÀ (Sự kiện theo mùa là Không có) Thì Chiết khấu là Trung bình (Thu hút khách hàng).
7. Nếu (Khối lượng bán hàng là Thấp) VÀ (Biên lợi nhuận là Thấp) Thì Chiết khấu là Rất cao (Khuyến khích bán hàng).

**Từ trên chúng ta xem xét một cửa hàng có:**
* Xếp hạng = 4,3 (Trung bình)
* Khối lượng bán hàng = Trung bình
* Biên lợi nhuận = Thấp
* Sự kiện theo mùa = Cao
* Giảm giá của đối thủ cạnh tranh = Cao

Với các luật đưa ra thì giảm giá = Cao (30-40%) do sự kiện theo mùa & Giảm giá của đối thủ cạnh tranh cao. Mô hình logic mờ này tối ưu hóa các khoản giảm giá của Shopee dựa trên các điều kiện thị trường thực tế, đảm bảo các cửa hàng thu hút được người mua mà không mất quá nhiều lợi nhuận.

---

## 2.13. TÌNH HUỐNG 3: KẾ HOẠCH CHIẾN LƯỢC BÁN HÀNG CỦA SHOPEE DÀNH CHO CÁC CỬA HÀNG

Đối với các cửa hàng bán mặt hàng đặc biệt (ví dụ: hàng thủ công, đồ sưu tầm hiếm, đồ điện tử cao cấp, thời trang đặc biệt) trên Shopee, các chiến lược giảm giá phải được quản lý cẩn thận. Các mặt hàng đặc biệt thường có biên lợi nhuận cao hơn nhưng số lượng bán thấp hơn, đòi hỏi phải có cách tiếp cận thông minh về giá cả và khuyến mãi.

**Đây là những yếu tố chính ảnh hưởng đến quyết định giảm giá:**
* **Nhu cầu sản phẩm/Product Demand (Thấp, Trung bình, Cao):** Thấp (Sản phẩm ngách có mức độ quan tâm chung thấp); Trung bình (Nhu cầu vừa phải, nhưng không phải là chính thống); Cao (Mặt hàng đặc sản phổ biến có nhu cầu cao).
* **Áp lực định giá của đối thủ cạnh tranh/Competitor Pricing Pressure (Thấp, Trung bình, Cao):** Thấp (Ít hoặc không có đối thủ cạnh tranh bán cùng một mặt hàng); Trung bình (Một số đối thủ cạnh tranh với mức giá khác nhau); Cao (Nhiều đối thủ cạnh tranh với mức giá cạnh tranh).
* **Uy tín của cửa hàng/Store Reputation (Thấp, Trung bình, Cao):** Thấp (Cửa hàng mới hoặc được đánh giá thấp dưới 4,0 sao); Trung bình (Cửa hàng đã thành lập với xếp hạng từ 4,0 - 4,5 sao); Cao (Cửa hàng nổi tiếng với xếp hạng cao trên 4,5 sao).
* **Biên lợi nhuận/Profit Margin (Thấp, Trung bình, Cao):** Thấp (Mức tăng giá nhỏ, không có nhiều cơ hội giảm giá); Trung bình (Mức tăng giá vừa phải, có thể cung cấp một số giảm giá); Cao (Tăng giá mạnh, có thể giảm giá nhiều hơn).
* **Nhu cầu theo mùa/Seasonal Demand (Không có, Trung bình, Cao):** Không có (Thời gian bán hàng thường xuyên, không có sự kiện lớn); Trung bình (Một số đợt tăng theo mùa như mùa sắm vào ngày lễ); Cao (Sự kiện mua sắm cao điểm như Shopee 9.9, 11.11, 12.12).

**Xác định mức giảm giá/Discount Percentage áp dụng cho sản phẩm đó là:**
* Rất thấp (0-5%)
* Thấp (5-10%)
* Trung bình (10-20%)
* Cao (20-40%)
* Rất cao (40-70%)

**LUẬT MỜ:**
1. Nếu (Nhu cầu sản phẩm cao) VÀ (Áp lực định giá đối thủ cạnh tranh thấp) VÀ (Biên lợi nhuận thấp) Thì Giảm giá rất thấp (Không cần giảm giá các mặt hàng ngách có nhu cầu cao).
2. Nếu (Nhu cầu sản phẩm thấp) VÀ (Áp lực định giá của đối thủ cạnh tranh cao) VÀ (Biên lợi nhuận cao) Thì Chiết khấu cao (Khuyến khích bán hàng cho một mặt hàng ngách có sự cạnh tranh mạnh).
3. Nếu (Uy tín cửa hàng cao) VÀ (Biên lợi nhuận trung bình) VÀ (Nhu cầu theo mùa cao) Thì Chiết khấu trung bình (Tận dụng uy tín trong khi vẫn giữ được biên lợi nhuận tốt).
4. Nếu (Áp lực định giá của đối thủ cạnh tranh cao) VÀ (Nhu cầu theo mùa cao) VÀ (Biên lợi nhuận cao) Thì Chiết khấu rất cao (Cạnh tranh quyết liệt trong thời gian bán hàng cao điểm).
5. Nếu (Uy tín cửa hàng thấp) VÀ (Nhu cầu sản phẩm trung bình) VÀ (Biên lợi nhuận thấp) Thì Chiết khấu trung bình (Thu hút người mua ban đầu mà không bị lỗ nặng).
6. Nếu (Nhu cầu sản phẩm cao) VÀ (Nhu cầu theo mùa không có) VÀ (Áp lực định giá của đối thủ cạnh tranh thấp) Thì Chiết khấu rất thấp (Nhu cầu mạnh, không cần giảm giá).
7. Nếu (Biên lợi nhuận cao) VÀ (Áp lực định giá của đối thủ cạnh tranh là Trung bình) VÀ (Cầu theo mùa là Trung bình) Thì Chiết khấu là Trung bình (Cân bằng doanh số và lợi nhuận).

**Quá trình tính toán:**
Mờ hóa: Chuyển đổi các giá trị rõ như Biên lợi nhuận = 40% thành các tập mờ (Trung bình, Cao); Chiết khấu cao thành một tỷ lệ phần trăm chính xác như 30%.

**Tình huống:**
Sản phẩm: Đồng hồ xa xỉ thủ công
Nhu cầu sản phẩm: Cao
Áp lực định giá của đối thủ cạnh tranh: Trung bình
Uy tín của cửa hàng: Trung bình (4,2 sao)
Biên lợi nhuận: Cao
Nhu cầu theo mùa: Cao (Khuyến mãi Shopee 11.11)
Phù hợp với luật: Khi biên lợi nhuận cao và nhu cầu theo mùa cao và áp lực của đối thủ cạnh tranh mức trung bình, từ đó chiến lược giảm giá = Trung bình (15-25%).

---

## 2.14. TÌNH HUỐNG 4: TỐI ƯU HÓA THỜI GIAN GIAO HÀNG VÀ TĂNG THU NHẬP CHO TÀI XẾ

Trong logistics, việc kết hợp giao hàng hiệu quả có thể giảm thời gian di chuyển, chi phí nhiên liệu và thời gian nhàn rỗi đồng thời tăng thu nhập cho tài xế. Hệ thống logic mờ có thể tối ưu hóa việc lập kế hoạch tuyến đường, phân công giao hàng và phân lô đơn hàng dựa trên các yếu tố thời gian thực.

**Các biến ảnh hưởng đến cách kết hợp các lần giao hàng:**
* **Mật độ đơn hàng/Order Density (Thấp, Trung bình, Cao):** Thấp (Ít đơn hàng trong cùng một khu vực); Trung bình (Một số đơn hàng gần nhau); Cao (Nhiều đơn hàng gần nhau).
* **Giao hàng khẩn cấp/Delivery Urgency (Thấp, Trung bình, Cao):** Thấp (Thời gian giao hàng linh hoạt); Trung bình (Cần giao hàng sớm); Cao (Giao hàng khẩn cấp yêu cầu nhanh/trong ngày).
* **Tải trọng hiện tại của tài xế/Driver's Current Load (Thấp, Trung bình, Cao):** Thấp (Tài xế có ít hoặc không có đơn hàng); Trung bình (Số lượng đơn hàng được giao vừa phải); Cao (Tài xế gần hết công suất).
* **Tình trạng giao thông/Traffic Conditions (Thấp, Trung bình, Cao):** Thấp (Giao thông thông thoáng, có tuyến đường nhanh); Trung bình (Tắc nghẽn vừa phải); Cao (Giao thông đông đúc, di chuyển chậm hơn).
* **Lợi nhuận trên mỗi lần giao hàng/Profit Per Delivery (Thấp, Trung bình, Cao):** Thấp (Trọng lượng thấp giao hàng); Trung bình (Thu nhập công bằng cho mỗi chuyến đi); Cao (Đơn hàng giá trị cao).

**Biến đầu ra:**
* **Số lượng đơn hàng cần kết hợp/Number of Orders to Combine (Ít, Một số, Nhiều):** Xác định số lượng đơn hàng cần nhóm lại với nhau cho một tài xế.
* **Ưu tiên giao hàng/Delivery Priority (Thấp, Trung bình, Cao):** Xác định xem đơn hàng có nên được giao sớm hơn hay muộn hơn trên tuyến đường không.

### LUẬT
**Luật kết hợp đơn hàng:**
1. Nếu (Mật độ đơn hàng cao) VÀ (Tải trọng hiện tại của tài xế thấp) VÀ (Tình trạng giao thông thấp) Thì hãy kết hợp nhiều đơn hàng (Tối đa hóa hiệu quả).
2. Nếu (Mật độ đơn hàng trung bình) VÀ (Tình trạng giao thông cao) VÀ (Mức độ khẩn cấp giao hàng trung bình) Thì kết hợp một vài đơn hàng (Tránh chậm trễ).
3. Nếu (Tải trọng hiện tại của tài xế cao) VÀ (Mật độ đơn hàng cao) VÀ (Lợi nhuận trên mỗi lần giao hàng trung bình) Thì kết hợp một số đơn hàng (Tránh quá tải).
4. Nếu (Mật độ đơn hàng thấp) VÀ (Mức độ khẩn cấp của giao hàng cao) VÀ (Điều kiện giao thông trung bình) Thì kết hợp một vài đơn hàng (Ưu tiên tốc độ hơn hiệu quả).
5. Nếu (Lợi nhuận trên mỗi lần giao hàng cao) VÀ (Mức độ khẩn cấp của giao hàng cao) VÀ (Điều kiện giao thông cao) Thì kết hợp một vài đơn hàng (Đảm bảo giao hàng đúng hạn có giá trị cao).

**Luật ưu tiên giao hàng:**
6. Nếu (Mức độ khẩn cấp của giao hàng cao) VÀ (Lợi nhuận trên mỗi lần giao hàng cao) Thì mức độ ưu tiên giao hàng cao (Giao hàng trước).
7. Nếu (Mức độ khẩn cấp của giao hàng trung bình) VÀ (Điều kiện giao thông trung bình) Thì mức độ ưu tiên giao hàng trung bình.
8. Nếu (Mức độ khẩn cấp của giao hàng thấp) VÀ (Mật độ đơn hàng cao) VÀ (Lợi nhuận trên mỗi lần giao hàng thấp) Thì mức độ ưu tiên giao hàng thấp (Giao hàng sau).

**Chú ý:**
Ví dụ: tốc độ giao thông = 30 km/h, mờ hóa thành: Giao thông trung bình thành các giá trị mờ.

**Dữ liệu đầu vào:**
* Mật độ đơn hàng: Cao
* Mức độ khẩn cấp giao hàng: Trung bình
* Tải trọng hiện tại của tài xế: Thấp
* Điều kiện giao thông: Trung bình
* Lợi nhuận trên mỗi lần giao hàng: Trung bình

**Từ đó:**
* Nên kết hợp nhiều đơn hàng vì mật độ cao và tải trọng của tài xế thấp.
* Mức độ ưu tiên trung bình vì mức độ khẩn cấp ở mức trung bình.

**Kết quả:** Hệ thống chỉ định 5 lần giao hàng cho tài xế, tối ưu hóa cả thời gian và thu nhập. Sử dụng Logic mờ để giao hàng thông minh hơn nhằm kết hợp các đơn hàng hiệu quả giúp tiết kiệm thời gian và nhiên liệu. Bên cạnh đó tài xế kiếm được nhiều tiền hơn bằng cách giảm các chuyến đi không có khách. Các chuyến giao hàng khẩn cấp và có lợi nhuận cao được ưu tiên đúng cách. Các yếu tố giao thông và thời gian thực đảm bảo lịch trình giao hàng suôn sẻ.
"""
