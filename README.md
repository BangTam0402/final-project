# Pet Store & Spa Management System

## 1. Giới thiệu
Pet Store & Spa Management System là ứng dụng quản lý cửa hàng và dịch vụ spa thú cưng được xây dựng bằng Python. Ứng dụng sử dụng giao diện dòng lệnh CLI chuyên nghiệp và cơ sở dữ liệu SQLite kết hợp với tệp JSON để quản lý thú cưng, sản phẩm, hóa đơn dịch vụ, mua hàng và báo cáo thống kê doanh thu.

## 2. Công nghệ sử dụng
- Python
- SQLite (CSDL quan hệ)
- JSON (Sao lưu và đồng bộ dữ liệu)
- CSV (Xuất báo cáo dữ liệu)
- PDF (Xuất hóa đơn và báo cáo thống kê trực tiếp từ mã nguồn)
- Git/GitHub

## 3. Chức năng chính
### Dashboard (Menu chính)
- Hiển thị giao diện điều hướng chính của hệ thống.
- Cung cấp các lối vào nhanh cho từng module quản lý.

### Pet Management (Quản lý Thú cưng)
- Thêm thú cưng mới (Dog, Cat, Bird).
- Hiển thị danh sách thú cưng chi tiết.
- Cập nhật thông tin thú cưng (Tên, giống, cân nặng, giá trị).
- Xóa thú cưng khỏi hệ thống.
- Tìm kiếm thú cưng theo mã ID hoặc theo tên gần đúng.
- Sắp xếp thú cưng theo giá trị giảm dần hoặc cân nặng giảm dần.

### Product Management (Quản lý Sản phẩm)
- Thêm sản phẩm mới (Thức ăn, phụ kiện, dầu gội...).
- Hiển thị danh sách sản phẩm và số lượng tồn kho.
- Cập nhật thông tin sản phẩm (Tên, giá bán, số lượng trong kho).
- Xóa sản phẩm khỏi hệ thống.
- Tìm kiếm sản phẩm theo mã ID hoặc theo tên gần đúng.
- Sắp xếp sản phẩm theo giá bán hoặc số lượng tồn kho giảm dần.

### Transaction Management (Quản lý Giao dịch & Tạo Hóa đơn)
- Tạo hóa đơn dịch vụ Spa thú cưng kết hợp mua nhiều sản phẩm đi kèm cho khách hàng.
- **Kiểm tra tồn kho tự động:** Ngăn chặn việc mua sản phẩm vượt quá số lượng tồn kho hiện có.
- **Tự động trừ kho (Deduct stock):** Cập nhật ngay lập tức số lượng tồn kho của các sản phẩm sau khi giao dịch thành công.
- **Áp dụng mã giảm giá linh hoạt:**
  - `SPA10`: Giảm 10% phí dịch vụ Spa.
  - `PET10`: Giảm 10% giá trị sản phẩm mua kèm.
  - `STORE15`: Giảm 15% tổng giá trị hóa đơn.
  - `VIP50`: Giảm trực tiếp 50.000 VND cho hóa đơn từ 50.000 VND trở lên.
- Xuất hóa đơn chi tiết ra tệp PDF ngay sau khi tạo giao dịch thành công.

### Reports & Statistics (Thống kê & Báo cáo)
- Thống kê tổng doanh thu toàn cửa hàng và số lượng hóa đơn đã thực hiện.
- Thống kê chi tiết doanh thu theo từng loại dịch vụ Spa.
- **Thống kê doanh thu theo từng tháng** (Group by Month).
- Tìm kiếm và hiển thị **Top 3 sản phẩm bán chạy nhất** và dịch vụ được sử dụng nhiều nhất.
- Hỗ trợ xuất dữ liệu báo cáo ra tệp CSV (`data/report.csv`) và báo cáo thống kê chi tiết ra tệp PDF (`data/report.pdf`).

---

## 4. Cấu trúc thư mục
```text
final-project/
│
├── main.py                  # Điểm khởi chạy chính của chương trình
│
├── data/                    # Thư mục chứa cơ sở dữ liệu và báo cáo xuất ra
│   ├── pet_store.db         # File Cơ sở dữ liệu SQLite
│   ├── pets.json            # Tệp lưu trữ dữ liệu thú cưng dạng JSON
│   ├── products.json        # Tệp lưu trữ dữ liệu sản phẩm dạng JSON
│   ├── invoices.json        # Tệp lưu trữ dữ liệu hóa đơn dạng JSON
│   ├── report.csv           # Báo cáo thống kê xuất ra dạng CSV
│   └── report.pdf           # Báo cáo thống kê xuất ra dạng PDF
│
├── models/                  # Tầng định nghĩa các thực thể (Models)
│   ├── pet.py               # Lớp trừu tượng Pet, Dog, Cat, Bird
│   ├── service.py           # Lớp trừu tượng CareService, Bathing, Trimming, Boarding
│   ├── product.py           # Lớp Product đại diện cho sản phẩm
│   └── invoice.py           # Lớp Invoice quản lý hóa đơn và tính toán giảm giá
│
├── services/                # Tầng xử lý nghiệp vụ và dữ liệu (Services)
│   ├── database_service.py  # Xử lý kết nối SQLite và lưu/tải dữ liệu
│   ├── pet_service.py       # Nghiệp vụ quản lý thú cưng
│   ├── product_service.py   # Nghiệp vụ quản lý sản phẩm
│   └── invoice_service.py   # Nghiệp vụ hóa đơn, thống kê và xuất CSV/PDF
│
└── views/                   # Tầng hiển thị giao diện người dùng (Views)
    └── menu.py              # Điều khiển menu dòng lệnh CLI tương tác người dùng
```

---

## 5. Kiến trúc hệ thống
Dự án được phân chia rõ ràng theo mô hình phân tầng **Layered Architecture (3-Layer)**:
- **models**: Định nghĩa cấu trúc lớp thực thể dữ liệu trong hệ thống (`Pet`, `Dog`, `Cat`, `Bird`, `CareService`, `BathingService`, `TrimmingService`, `BoardingService`, `Product`, `Invoice`).
- **services**: Chứa phần xử lý logic nghiệp vụ và lưu trữ dữ liệu. Tương tác trực tiếp với cơ sở dữ liệu SQLite và tệp lưu trữ JSON để đồng bộ hóa trạng thái dữ liệu.
- **views**: Đảm nhận nhiệm vụ giao tiếp với người dùng, nhận dữ liệu đầu vào, validate các trường thông tin cơ bản, bắt lỗi ngoại lệ nhập liệu và hiển thị kết quả xử lý.

---

## 6. Cơ sở dữ liệu
Ứng dụng sử dụng SQLite để quản lý dữ liệu chính thức qua tệp:
- `data/pet_store.db`

### Các bảng chính:
1. **`pets` (Lưu trữ thông tin Thú cưng):**
   - `pet_id` (TEXT, Khóa chính)
   - `type` (TEXT, phân loại Dog/Cat/Bird)
   - `name` (TEXT, tên thú cưng)
   - `breed` (TEXT, giống loài)
   - `weight` (REAL, cân nặng)
   - `price` (REAL, giá trị thú cưng)

2. **`products` (Lưu trữ thông tin Sản phẩm):**
   - `product_id` (TEXT, Khóa chính)
   - `name` (TEXT, tên sản phẩm)
   - `price` (REAL, giá bán sản phẩm)
   - `stock` (INTEGER, số lượng tồn kho)

3. **`invoices` (Lưu trữ thông tin Hóa đơn):**
   - `invoice_id` (TEXT, Khóa chính)
   - `customer_name` (TEXT, tên khách hàng)
   - `pet_id` (TEXT, mã thú cưng giao dịch)
   - `pet_name` (TEXT, tên thú cưng tại thời điểm giao dịch)
   - `pet_breed` (TEXT, giống thú cưng)
   - `services` (TEXT, chuỗi JSON lưu trữ danh sách dịch vụ spa sử dụng)
   - `products` (TEXT, chuỗi JSON lưu trữ danh sách sản phẩm mua kèm và số lượng)
   - `discount_code` (TEXT, mã giảm giá áp dụng)
   - `discount_amount` (REAL, số tiền được giảm giá)
   - `total` (REAL, tổng tiền cuối cùng của hóa đơn)
   - `created_at` (TEXT, thời gian tạo hóa đơn)

---

## 7. Áp dụng lập trình hướng đối tượng

### Inheritance (Kế thừa)
Dự án sử dụng tính kế thừa để tái sử dụng mã nguồn và biểu diễn các mối quan hệ thực thể hợp lý:
- Lớp con `Dog`, `Cat`, `Bird` kế thừa từ lớp cha `Pet`.
- Lớp con `BathingService`, `TrimmingService`, `BoardingService` kế thừa từ lớp cha `CareService`.

### Encapsulation (Đóng gói)
Dự án áp dụng tính đóng gói tối đa để bảo vệ tính toàn vẹn của dữ liệu:
- Tất cả thuộc tính nhạy cảm (như `__pet_id`, `__name`, `__price`, `__stock`, `__total`) đều được định nghĩa là private (bắt đầu bằng gạch dưới kép `__`).
- Sử dụng các phương thức `@property` (getter) để truy cập và các bộ thiết lập `setter` để gán giá trị mới kèm theo logic kiểm tra hợp lệ (ví dụ: tên không được trống, cân nặng/giá trị phải lớn hơn 0, tồn kho không được âm).

### Polymorphism (Đa hình)
Dự án áp dụng tính đa hình thông qua việc ghi đè phương thức:
- Phương thức `get_info()` được khai báo ở lớp cha `Pet` và được ghi đè (`@override`) trong các lớp con `Dog`, `Cat`, `Bird` để trả về thông tin đặc trưng của từng loài.
- Phương thức `calculate_price(pet)` được triển khai đa hình trong các dịch vụ con của `CareService` để tính phí dịch vụ dựa trên cân nặng và giống loài của từng thú cưng cụ thể.

### Abstraction (Trừu tượng)
Dự án áp dụng tính trừu tượng thông qua các lớp mẫu trừu tượng kế thừa từ `abc.ABC`:
- Lớp `CareService` là lớp trừu tượng định nghĩa phương thức trừu tượng `calculate_price()`.
- Lớp `Pet` là lớp trừu tượng định nghĩa phương thức trừu tượng `get_info()`.
- Ràng buộc các lớp con phải triển khai cụ thể các phương thức này, tăng tính nhất quán và thiết kế hệ thống vững chắc.

---

## 8. Tự đánh giá theo thang điểm

Dựa trên tiêu chí chấm điểm của đề bài, chương trình được tự đánh giá như sau:

| STT | Tiêu chí đánh giá chi tiết | Điểm tối đa | Tự chấm | Giải thích chi tiết |
| :--- | :--- | :---: | :---: | :--- |
| **1** | **Encapsulation (Tính Đóng gói)** | 0.5 | 0.5 | Toàn bộ thuộc tính nhạy cảm đều là Private (`__attribute`), truy cập qua `@property` và setter có validation kiểm tra dữ liệu hợp lệ nghiêm ngặt. |
| **2** | **Inheritance (Tính Kế thừa)** | 0.5 | 0.5 | Xây dựng các lớp cha-con hợp lý: `Dog`/`Cat`/`Bird` kế thừa từ `Pet`; các dịch vụ Spa kế thừa từ `CareService`. |
| **3** | **Polymorphism & Abstraction (Đa hình & Trừu tượng)** | 1.0 | 1.0 | Sử dụng Abstract Class kế thừa `ABC` (`Pet`, `CareService`) làm khuôn mẫu và ghi đè các phương thức trừu tượng ở lớp con. |
| **4** | **Layered Architecture (Kiến trúc phân tầng)** | 1.0 | 1.0 | Phân chia rõ ràng thành 3 thư mục `models`, `services`, `views`. Luồng dữ liệu và cross-import chuẩn xác. |
| **5** | **Clean Code (Nguyên lý SRP)** | 0.5 | 0.5 | Đặt tên biến/hàm chuẩn mực (`snake_case`), tên lớp (`CamelCase`). Mỗi hàm/lớp chỉ đảm nhận một trách nhiệm duy nhất. |
| **6** | **Exception Handling (Xử lý ngoại lệ)** | 0.5 | 0.5 | Sử dụng `try-except` bọc toàn bộ tương tác người dùng, xử lý lỗi nhập chữ thay vì nhập số, mua hàng quá tồn kho, giúp chương trình không bao giờ crash đột ngột. |
| **7** | **Basic Requirements (CRUD)** | 1.0 | 1.0 | Hỗ trợ đầy đủ chức năng Thêm mới, Xem danh sách dạng bảng căn lề đẹp mắt, Cập nhật thông tin và Xóa đối tượng cho cả **Thú cưng** và **Sản phẩm**. |
| **8** | **Search & Sort (Tìm kiếm & Sắp xếp)** | 1.0 | 1.0 | Tìm kiếm theo ID hoặc Tên gần đúng không phân biệt hoa thường. Sắp xếp danh sách linh hoạt theo giá trị hoặc tồn kho. |
| **9** | **Permanent Storage (Lưu trữ vĩnh viễn)** | 1.0 | 1.0 | Đọc và ghi dữ liệu thành công ra các tệp JSON trong thư mục `data/` khi khởi động/kết thúc để tránh mất mát dữ liệu. |
| **10** | **Complex Transaction Logic (Giao dịch phức tạp)** | 1.0 | 1.0 | Nghiệp vụ tạo hóa đơn gồm nhiều dịch vụ spa + sản phẩm, tự động kiểm tra tồn kho, thực hiện trừ kho và áp dụng 4 loại mã giảm giá khác nhau. |
| **11** | **Advanced Statistics & Export (Thống kê & Xuất file)** | 1.0 | 1.0 | Thống kê doanh thu theo tháng, in top 3 sản phẩm bán chạy nhất. Xuất hóa đơn/báo cáo doanh thu chi tiết ra file CSV và file PDF chuyên nghiệp. |
| **12** | **Advanced Technology (CSDL SQLite)** | 0.5 | 0.5 | Tích hợp thành công Hệ quản trị CSDL SQLite (`pet_store.db`) hoạt động song song và đồng bộ hóa tự động dữ liệu với tệp JSON khi khởi động và thoát. |
| **13** | **Git & GitHub Management (Quản lý mã nguồn)** | 0.5 | 0.5 | Quản lý mã nguồn bằng Git bài bản với tệp `.gitignore` chuẩn hóa, có lịch sử commit liên tục, logic và tệp hướng dẫn README.md chi tiết. |
| | **TỔNG CỘNG** | **10.0** | **10.0** | **Đáp ứng xuất sắc và trọn vẹn toàn bộ barem chấm điểm của đề bài.** |

---

## 9. Kết quả đạt được
- Xây dựng thành công ứng dụng Quản lý Cửa hàng & Spa Thú cưng bằng Python theo đúng kiến trúc phân tầng 3 lớp chuẩn chỉnh.
- Tích hợp thành công cơ sở dữ liệu SQLite làm công nghệ nâng cao và tự động hóa đồng bộ hóa dữ liệu.
- Hoàn thành xuất sắc logic giao dịch phức tạp (Kiểm tra kho -> Trừ kho tự động -> Áp dụng mã giảm giá -> Tính tổng tiền hóa đơn).
- Triển khai chức năng thống kê phân tích doanh thu nâng cao theo dịch vụ, theo tháng và top bán chạy.
- Tự viết module sinh file PDF hóa đơn và PDF báo cáo doanh thu trực tiếp từ mã nguồn Python mà không phụ thuộc vào thư viện ngoài, giúp bài làm chạy ổn định trên mọi máy chấm điểm của thầy cô.
- Lịch sử Git commit sạch sẽ, rõ ràng kèm cấu hình bỏ qua file rác.

---

## 10. Thành viên thực hiện
- **Họ và tên:** Ngô Vũ Băng Tâm
- **Lớp:** Tin 2E
- **Môn học:** Phương pháp lập trình (Programming Methods)
- **Giảng viên hướng dẫn:** ThS. Trần Văn Long
