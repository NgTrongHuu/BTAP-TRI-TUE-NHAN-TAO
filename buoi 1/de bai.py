"""
BÀI TẬP
23.1. Sử dụng thư viện Folium, bạn hãy xây dựng một bản đồ tương tác hiển thị vị trí của UEH hoặc trường Đại học đang theo học hoặc một địa điểm trung tâm được lựa chọn. Trên bản đồ cần thể hiện tối thiểu năm địa điểm công cộng lân cận như bệnh viện, trung tâm thương mại, bến xe hoặc cơ quan hành chính. Mỗi địa điểm phải được gắn marker có popup mô tả ngắn gọn thông tin. Bản đồ cần có khả năng phóng to, thu nhỏ và bật/tắt các lớp dữ liệu
.
23.2. Sử dụng GeoPy, bạn hãy thu thập hoặc giả lập danh sách tối thiểu mười địa chỉ cụ thể. Thực hiện chuyển đổi các địa chỉ này sang tọa độ địa lý (vĩ độ, kinh độ) và tính khoảng cách từ mỗi địa chỉ đến một điểm trung tâm xác định trước. Kết quả cần được trực quan hóa trên bản đồ bằng Folium, trong đó thể hiện rõ vị trí, khoảng cách và mối quan hệ không gian giữa các điểm
.
23.3. Bạn hãy tạo một bản đồ nhiệt (heatmap) thể hiện mật độ phân bổ của một hiện tượng không gian như khách hàng, đơn hàng, dân cư hoặc điểm giao dịch (dữ liệu có thể giả lập). Bản đồ cho phép người xem nhận biết trực quan các khu vực có mật độ cao và thấp, đồng thời giải thích ý nghĩa quản trị của các vùng nóng trên bản đồ
.
23.4. Sử dụng GeoPandas, hãy đọc dữ liệu ranh giới hành chính (tỉnh, thành phố hoặc phường/xã) và kết hợp với một tập dữ liệu số tương ứng như dân số, doanh thu, số lượng đơn hàng hoặc mức độ tiêu thụ. Kết quả cần được thể hiện dưới dạng bản đồ choropleth, phản ánh sự khác biệt không gian giữa các khu vực và đưa ra nhận xét ngắn về ý nghĩa quản trị
.
23.5. Bạn hãy xây dựng mô hình phân tích vùng phục vụ (service area) cho một trung tâm phân phối, kho hàng hoặc trạm dịch vụ. Sử dụng dữ liệu tọa độ để vẽ các vòng bán kính phục vụ khác nhau (ví dụ: 3 km, 5 km và 10 km) và trực quan hóa trên bản đồ. Bài làm cần đánh giá khả năng tiếp cận khách hàng của từng vùng và đề xuất phạm vi hoạt động tối ưu
.
23.6. Sử dụng OSMnx, bạn hãy tải dữ liệu mạng lưới giao thông đường bộ của một khu vực đô thị cụ thể. Trực quan hóa mạng đường trên bản đồ và thực hiện một số phân tích cơ bản như số lượng nút giao, chiều dài đường trung bình hoặc mật độ mạng. Trình bày vai trò của dữ liệu mạng giao thông trong các hệ thống AI đô thị thông minh
.
23.7. Kết hợp OSMnx và NetworkX, bạn hãy xây dựng chương trình tìm đường đi ngắn nhất giữa hai địa điểm bất kỳ trong khu vực nghiên cứu. So sánh kết quả giữa ít nhất hai thuật toán khác nhau (ví dụ: Dijkstra và A*). Tuyến đường tìm được cần được hiển thị trực quan trên bản đồ và phân tích ưu – nhược điểm của từng phương pháp
.
23.8. Bạn hãy mô phỏng một hệ thống gọi xe công nghệ đơn giản. Trong đó, vị trí khách hàng và xe được biểu diễn bằng tọa độ trên bản đồ. Áp dụng một phương pháp AI hoặc heuristic để gán xe phù hợp nhất cho từng khách hàng dựa trên khoảng cách hoặc thời gian di chuyển. Toàn bộ quá trình ghép xe và khách cần được trực quan hóa trên bản đồ
.
23.9. Sử dụng thuật toán phân cụm trong học máy, bạn hãy phân cụm dữ liệu vị trí khách hàng hoặc đơn hàng. Trên cơ sở kết quả phân cụm, đề xuất vị trí đặt trạm xe, kho hàng hoặc điểm trung chuyển tối ưu. Kết quả phân tích phải được trình bày dưới dạng bản đồ và có giải thích logic quản trị đi kèm
.
23.10. Bạn hãy xây dựng bản đồ phân tích nguy cơ tắc nghẽn giao thông dựa trên dữ liệu giả lập hoặc dữ liệu mở. Áp dụng mô hình AI đơn giản hoặc logic mờ để xác định các khu vực có nguy cơ cao, đồng thời đề xuất tuyến đường thay thế. Bản đồ cần thể hiện rõ các vùng rủi ro và tuyến đề xuất
.
23.11. Xây dựng một mô hình dự đoán nhu cầu dịch vụ (ví dụ: nhu cầu gọi xe, giao hàng) theo khu vực và thời gian. Sử dụng một mô hình học máy cơ bản để dự đoán và trực quan hóa kết quả trên bản đồ. Bạn cần phân tích sự khác biệt nhu cầu giữa các khu vực và thảo luận ý nghĩa trong điều phối nguồn lực
.
23.12. Bạn hãy mô phỏng một bài toán tối ưu hóa tuyến giao hàng với nhiều kho và nhiều điểm giao nhận. Sử dụng thuật toán mạng hoặc heuristic để tìm tuyến đường hiệu quả cho từng xe. Kết quả phải được thể hiện trên bản đồ và đánh giá hiệu quả so với phương án không tối ưu
.
23.13. Hãy thiết kế một dashboard bản đồ kết hợp nhiều lớp dữ liệu không gian, bao gồm điểm, vùng và tuyến đường. Dashboard phải hỗ trợ tương tác cơ bản và phục vụ mục đích báo cáo quản trị hoặc ra quyết định chiến lược
.
23.14. Bạn hãy xây dựng mô hình mô phỏng hệ thống điều phối xe theo thời gian, trong đó xe di chuyển trên mạng đường và trạng thái xe được cập nhật liên tục. Quá trình mô phỏng cần được trực quan hóa trên bản đồ theo từng bước thời gian
.
23.15. Bạn tự đề xuất và xây dựng một ứng dụng AI dựa trên bản đồ liên quan đến quản trị hoặc công nghệ, chẳng hạn như gọi xe, logistics, quản lý đô thị hoặc phân tích thị trường. Bài làm cần trình bày rõ bài toán, dữ liệu, phương pháp AI, cách trực quan hóa bản đồ và giá trị ứng dụng thực tiễn
"""