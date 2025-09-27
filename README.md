# VnStock Pro - Nền tảng Phân tích Chứng khoán Chuyên nghiệp 📊

**VnStock Pro** là một ứng dụng web được xây dựng bằng Python và Streamlit bởi nhóm 5 sinh viên lớp K23414A, cho môn học Gói phần mềm ứng dụng cho tài chính 1, cung cấp một giao diện hiện đại và chuyên nghiệp để phân tích và trực quan hóa dữ liệu chứng khoán Việt Nam. Ứng dụng tự động tải dữ liệu mới nhất từ nguồn CafeF, cho phép người dùng theo dõi biểu đồ giá, áp dụng các chỉ báo kỹ thuật phổ biến và xem các thống kê quan trọng một cách trực quan.

**Danh sách sinh viên thực hiện:**
Phan Đặng Anh Kiệt - K234141653
Ngô Cao Nguyên - K234141661
Trần Thị Hoài Nhân - K234141662
Huỳnh Bảo Nhi - K234141663
Cao Huỳnh Tuyết Trân - K234141684

## ✨ Tính năng nổi bật

* ** Giao diện hiện đại & chuyên nghiệp**:
    * Thiết kế theo phong cách "Glassmorphism" và "Hologram" sang trọng.
    * Hỗ trợ 2 giao diện **Sáng (Light) ☀️** và **Tối (Dark) 🌙**.
    * Bố cục responsive, tối ưu cho trải nghiệm trên nhiều kích thước màn hình.

* ** Dữ liệu tự động & tin cậy**:
    * Tự động tải và cập nhật dữ liệu giao dịch hàng ngày từ **CafeF**.
    * Cơ chế tìm kiếm thông minh để lấy dữ liệu của ngày gần nhất có thể.
    * Dữ liệu được cache để tối ưu hiệu suất và tốc độ tải trang.

* ** Biểu đồ tương tác nâng cao**:
    * Biểu đồ nến (Candlestick) được tùy chỉnh theo phong cách của FireAnt.
    * Hỗ trợ **Zoom** (lăn chuột), **Pan** (kéo thả) và **Reset** (double click).
    * Thanh công cụ cho phép vẽ các đường xu hướng, hình chữ nhật, vòng tròn... trực tiếp trên biểu đồ.

* ** Phân tích kỹ thuật đa dạng**:
    * **Đường trung bình động (MA)**: Hỗ trợ chọn nhiều kỳ hạn cùng lúc (5, 10, 20, 50, 100, 200).
    * **Khối lượng giao dịch (Volume)**: Hiển thị theo màu sắc tương ứng với nến tăng/giảm.
    * **Chỉ số sức mạnh tương đối (RSI)**: Với các vùng quá mua/quá bán (70/30).
    * **Hội tụ phân kỳ trung bình động (MACD)**: Bao gồm đường MACD, đường Signal và Histogram.

* ** Thống kê & Phân tích**:
    * Bảng điều khiển (Dashboard) hiển thị các thông tin tổng quan: biên độ giá, thống kê khối lượng, và phân tích xu hướng.
    * Cho phép xem và kiểm tra dữ liệu gốc trực tiếp trên ứng dụng.

## 🚀 Cài đặt & Chạy dự án

Để chạy dự án này trên máy của bạn, hãy làm theo các bước sau.

### **Yêu cầu**

* Python 3.8+
* Pip (trình quản lý gói của Python)

### **Các bước cài đặt**

1.  **Clone repository (hoặc tải mã nguồn):**
    ```bash
    git clone https://github.com/preutbao/vnstock-pro.git
    cd your-project-directory
    ```

2.  **Tạo môi trường ảo (khuyến khích):**
    Điều này giúp cô lập các thư viện của dự án và tránh xung đột.
    ```bash
    python -m venv venv
    ```
    * Trên Windows: `venv\Scripts\activate`
    * Trên macOS/Linux: `source venv/bin/activate`

3.  **Cài đặt các thư viện cần thiết:**
    Tạo một file tên là `requirements.txt` với nội dung sau:
    ```txt
    streamlit
    pandas
    numpy
    requests
    plotly
    ```
    Sau đó chạy lệnh:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Chạy ứng dụng:**
    Sử dụng Streamlit để khởi chạy file `app.py`.
    ```bash
    streamlit run app.py
    ```
    Ứng dụng sẽ tự động mở trên trình duyệt của bạn tại địa chỉ `http://localhost:8501`.

## 📂 Cấu trúc thư mục

```
.
├── 📜 app.py           # File mã nguồn chính của ứng dụng Streamlit
├── 📜 requirements.txt  # Danh sách các thư viện Python cần thiết
└── 📜 README.md         # File hướng dẫn và mô tả dự án
```

## 🛠️ Công nghệ sử dụng

* **Ngôn ngữ:** Python
* **Giao diện Web:** Streamlit
* **Thao tác dữ liệu:** Pandas, NumPy
* **Trực quan hóa:** Plotly
* **Tải dữ liệu:** Requests

## 📄 Giấy phép

Dự án này được cấp phép theo Giấy phép MIT. Xem file `LICENSE` để biết thêm chi tiết.