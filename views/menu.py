from models.pet import Dog, Cat, Bird
from models.product import Product
from models.service import BathingService, TrimmingService, BoardingService
from services.database_service import DatabaseService


class Menu:
    def __init__(self, pet_service, product_service, invoice_service):
        self.pet_service = pet_service
        self.product_service = product_service
        self.invoice_service = invoice_service
        self.database_service = DatabaseService()

    def load_data(self):
        # 1. Tải dữ liệu Thú cưng
        pets = self.database_service.load_pets()
        if pets:
            self.pet_service.pets.clear()
            for p in pets:
                try:
                    self.pet_service.add_pet(p)
                except ValueError:
                    pass
            print("[CSDL] Đã tải danh sách thú cưng từ SQLite.")
        else:
            self.pet_service.load_from_file()
            print("[JSON] Đã tải danh sách thú cưng từ JSON.")

        # 2. Tải dữ liệu Sản phẩm
        products = self.database_service.load_products()
        if products:
            self.product_service.products.clear()
            for pr in products:
                try:
                    self.product_service.add_product(pr)
                except ValueError:
                    pass
            print("[CSDL] Đã tải danh sách sản phẩm từ SQLite.")
        else:
            self.product_service.load_from_file()
            print("[JSON] Đã tải danh sách sản phẩm từ JSON.")

        # 3. Tải dữ liệu Hóa đơn
        invoices = self.database_service.load_invoices(self.pet_service, self.product_service)
        if invoices:
            self.invoice_service.invoices.clear()
            for inv in invoices:
                self.invoice_service.invoices.append(inv)
            print("[CSDL] Đã tải danh sách hóa đơn từ SQLite.")
        else:
            self.invoice_service.load_from_file(self.pet_service, self.product_service)
            print("[JSON] Đã tải danh sách hóa đơn từ JSON.")

    def run(self):
        # Tải dữ liệu khi khởi động chương trình
        self.load_data()

        while True:
            print("\n=============================================")
            print("      HỆ THỐNG QUẢN LÝ CỬA HÀNG & SPA PET    ")
            print("=============================================")
            print("1. Quản lý Thú cưng (Pets)")
            print("2. Quản lý Sản phẩm (Products)")
            print("3. Tạo Hóa đơn dịch vụ & mua hàng (Transaction)")
            print("4. Hiển thị danh sách Hóa đơn")
            print("5. Thống kê & Báo cáo (Statistics)")
            print("6. Xuất báo cáo CSV")
            print("0. Lưu dữ liệu & Thoát")
            print("=============================================")
            
            choice = input("Nhập lựa chọn của bạn: ").strip()

            try:
                if choice == "1":
                    self.pet_menu()
                elif choice == "2":
                    self.product_menu()
                elif choice == "3":
                    self.create_invoice_menu()
                elif choice == "4":
                    print("\n--- DANH SÁCH HÓA ĐƠN ---")
                    self.invoice_service.display_invoices()
                elif choice == "5":
                    self.statistics_menu()
                elif choice == "6":
                    self.invoice_service.export_csv()
                    print("\n[Thành công] Đã xuất báo cáo ra file 'data/report.csv'")
                elif choice == "0":
                    print("\nĐang lưu dữ liệu...")
                    # Ghi ra JSON
                    self.pet_service.save_to_file()
                    self.product_service.save_to_file()
                    self.invoice_service.save_to_file()
                    
                    # Ghi ra SQLite
                    self.database_service.save_pets(self.pet_service.pets)
                    self.database_service.save_products(self.product_service.products)
                    self.database_service.save_invoices(self.invoice_service.invoices)
                    
                    print("[Thành công] Toàn bộ dữ liệu đã được lưu vào file JSON và CSDL SQLite.")
                    print("Cảm ơn bạn đã sử dụng dịch vụ. Tạm biệt!")
                    break
                else:
                    print("[Lỗi] Lựa chọn không hợp lệ. Vui lòng nhập lại.")
            except Exception as e:
                print(f"[Lỗi Hệ thống] Đã xảy ra lỗi: {e}")

    # ================= QUẢN LÝ THÚ CƯNG (CRUD PET) =================
    def pet_menu(self):
        while True:
            print("\n--- QUẢN LÝ THÚ CƯNG ---")
            print("1. Thêm thú cưng mới (Create)")
            print("2. Hiển thị danh sách thú cưng (Read)")
            print("3. Cập nhật thông tin thú cưng (Update)")
            print("4. Xóa thú cưng (Delete)")
            print("5. Tìm kiếm thú cưng (Search)")
            print("6. Sắp xếp danh sách thú cưng (Sort)")
            print("0. Quay lại Menu chính")
            print("------------------------")
            choice = input("Nhập lựa chọn: ").strip()

            try:
                if choice == "1":
                    self.add_pet_menu()
                elif choice == "2":
                    print("\n--- DANH SÁCH THÚ CƯNG ---")
                    self.pet_service.display_pets()
                elif choice == "3":
                    self.update_pet_menu()
                elif choice == "4":
                    pet_id = input("Nhập ID thú cưng muốn xóa: ").strip()
                    if self.pet_service.delete_pet(pet_id):
                        print("[Thành công] Đã xóa thú cưng.")
                    else:
                        print("[Lỗi] Không tìm thấy thú cưng có ID này.")
                elif choice == "5":
                    self.search_pet_menu()
                elif choice == "6":
                    self.sort_pet_menu()
                elif choice == "0":
                    break
                else:
                    print("[Lỗi] Lựa chọn không hợp lệ.")
            except Exception as e:
                print(f"[Lỗi] {e}")

    def add_pet_menu(self):
        pet_type = input("Nhập loại thú cưng (Dog/Cat/Bird): ").strip()
        if pet_type.lower() not in ["dog", "cat", "bird"]:
            print("[Lỗi] Loại thú cưng không hợp lệ. Chỉ chấp nhận Dog, Cat hoặc Bird.")
            return

        pet_id = input("Nhập ID thú cưng: ").strip()
        if not pet_id:
            print("[Lỗi] ID không được để trống.")
            return
            
        name = input("Nhập tên thú cưng: ").strip()
        breed = input("Nhập giống loài: ").strip()
        
        try:
            weight = float(input("Nhập cân nặng (kg): "))
            price = float(input("Nhập giá mua/giá trị (VND): "))
        except ValueError:
            print("[Lỗi] Cân nặng và Giá trị phải là số.")
            return

        if pet_type.lower() == "dog":
            pet = Dog(pet_id, name, breed, weight, price)
        elif pet_type.lower() == "cat":
            pet = Cat(pet_id, name, breed, weight, price)
        else:
            pet = Bird(pet_id, name, breed, weight, price)

        self.pet_service.add_pet(pet)
        print("[Thành công] Đã thêm thú cưng mới.")

    def update_pet_menu(self):
        pet_id = input("Nhập ID thú cưng cần cập nhật: ").strip()
        pet = self.pet_service.search_pet_by_id(pet_id)
        if not pet:
            print("[Lỗi] Không tìm thấy thú cưng.")
            return

        print(f"Thông tin hiện tại: {pet.get_info()}")
        name = input("Nhập tên mới (để trống nếu không sửa): ").strip()
        breed = input("Nhập giống mới (để trống nếu không sửa): ").strip()
        
        weight_input = input("Nhập cân nặng mới (để trống nếu không sửa): ").strip()
        weight = float(weight_input) if weight_input else None
        
        price_input = input("Nhập giá mới (để trống nếu không sửa): ").strip()
        price = float(price_input) if price_input else None

        if self.pet_service.update_pet(pet_id, name if name else None, breed if breed else None, weight, price):
            print("[Thành công] Đã cập nhật thông tin thú cưng.")
        else:
            print("[Lỗi] Cập nhật thất bại.")

    def search_pet_menu(self):
        keyword = input("Nhập ID hoặc Tên thú cưng cần tìm: ").strip()
        # Tìm theo ID trước
        pet = self.pet_service.search_pet_by_id(keyword)
        if pet:
            print(f"\n[Kết quả] Tìm thấy theo ID:\n{pet.get_info()}")
        else:
            # Tìm theo tên
            results = self.pet_service.search_pet_by_name(keyword)
            if results:
                print(f"\n[Kết quả] Tìm thấy {len(results)} thú cưng có tên chứa '{keyword}':")
                for idx, p in enumerate(results, 1):
                    print(f"{idx}. {p.get_info()}")
            else:
                print("[Thông báo] Không tìm thấy thú cưng nào phù hợp.")

    def sort_pet_menu(self):
        print("Sắp xếp danh sách thú cưng theo:")
        print("1. Giá trị giảm dần")
        print("2. Cân nặng giảm dần")
        choice = input("Lựa chọn: ").strip()

        if choice == "1":
            self.pet_service.sort_by_price()
            print("[Thành công] Đã sắp xếp theo giá giảm dần.")
        elif choice == "2":
            self.pet_service.sort_by_weight()
            print("[Thành công] Đã sắp xếp theo cân nặng giảm dần.")
        else:
            print("[Lỗi] Lựa chọn không hợp lệ.")
            return

        self.pet_service.display_pets()

    # ================= QUẢN LÝ SẢN PHẨM (CRUD PRODUCT) =================
    def product_menu(self):
        while True:
            print("\n--- QUẢN LÝ SẢN PHẨM ---")
            print("1. Thêm sản phẩm mới (Create)")
            print("2. Hiển thị danh sách sản phẩm (Read)")
            print("3. Cập nhật thông tin sản phẩm (Update)")
            print("4. Xóa sản phẩm (Delete)")
            print("5. Tìm kiếm sản phẩm (Search)")
            print("6. Sắp xếp danh sách sản phẩm (Sort)")
            print("0. Quay lại Menu chính")
            print("------------------------")
            choice = input("Nhập lựa chọn: ").strip()

            try:
                if choice == "1":
                    self.add_product_menu()
                elif choice == "2":
                    print("\n--- DANH SÁCH SẢN PHẨM ---")
                    self.product_service.display_products()
                elif choice == "3":
                    self.update_product_menu()
                elif choice == "4":
                    prod_id = input("Nhập ID sản phẩm muốn xóa: ").strip()
                    if self.product_service.delete_product(prod_id):
                        print("[Thành công] Đã xóa sản phẩm.")
                    else:
                        print("[Lỗi] Không tìm thấy sản phẩm.")
                elif choice == "5":
                    self.search_product_menu()
                elif choice == "6":
                    self.sort_product_menu()
                elif choice == "0":
                    break
                else:
                    print("[Lỗi] Lựa chọn không hợp lệ.")
            except Exception as e:
                print(f"[Lỗi] {e}")

    def add_product_menu(self):
        product_id = input("Nhập ID sản phẩm (ví dụ: P01): ").strip()
        if not product_id:
            print("[Lỗi] ID không được để trống.")
            return
            
        name = input("Nhập tên sản phẩm: ").strip()
        
        try:
            price = float(input("Nhập giá bán (VND): "))
            stock = int(input("Nhập số lượng tồn kho ban đầu: "))
        except ValueError:
            print("[Lỗi] Giá bán và số lượng tồn kho phải là số.")
            return

        prod = Product(product_id, name, price, stock)
        self.product_service.add_product(prod)
        print("[Thành công] Đã thêm sản phẩm mới.")

    def update_product_menu(self):
        product_id = input("Nhập ID sản phẩm cần cập nhật: ").strip()
        prod = self.product_service.search_product_by_id(product_id)
        if not prod:
            print("[Lỗi] Không tìm thấy sản phẩm.")
            return

        print(f"Thông tin hiện tại: {prod.get_info()}")
        name = input("Nhập tên mới (để trống nếu không sửa): ").strip()
        
        price_input = input("Nhập giá bán mới (để trống nếu không sửa): ").strip()
        price = float(price_input) if price_input else None
        
        stock_input = input("Nhập số lượng tồn kho mới (để trống nếu không sửa): ").strip()
        stock = int(stock_input) if stock_input else None

        if self.product_service.update_product(product_id, name if name else None, price, stock):
            print("[Thành công] Đã cập nhật thông tin sản phẩm.")
        else:
            print("[Lỗi] Cập nhật thất bại.")

    def search_product_menu(self):
        keyword = input("Nhập ID hoặc Tên sản phẩm cần tìm: ").strip()
        prod = self.product_service.search_product_by_id(keyword)
        if prod:
            print(f"\n[Kết quả] Tìm thấy theo ID:\n{prod.get_info()}")
        else:
            results = self.product_service.search_product_by_name(keyword)
            if results:
                print(f"\n[Kết quả] Tìm thấy {len(results)} sản phẩm có tên chứa '{keyword}':")
                for idx, p in enumerate(results, 1):
                    print(f"{idx}. {p.get_info()}")
            else:
                print("[Thông báo] Không tìm thấy sản phẩm nào phù hợp.")

    def sort_product_menu(self):
        print("Sắp xếp danh sách sản phẩm theo:")
        print("1. Giá bán giảm dần")
        print("2. Số lượng tồn kho giảm dần")
        choice = input("Lựa chọn: ").strip()

        if choice == "1":
            self.product_service.sort_by_price(reverse=True)
            print("[Thành công] Đã sắp xếp theo giá bán giảm dần.")
        elif choice == "2":
            self.product_service.sort_by_stock(reverse=True)
            print("[Thành công] Đã sắp xếp theo số lượng tồn kho giảm dần.")
        else:
            print("[Lỗi] Lựa chọn không hợp lệ.")
            return

        self.product_service.display_products()

    # ================= TẠO GIAO DỊCH HÓA ĐƠN (SPA SERVICE & PRODUCTS SHOPPING) =================
    def create_invoice_menu(self):
        print("\n--- BẮT ĐẦU GIAO DỊCH TẠO HÓA ĐƠN ---")
        customer_name = input("Nhập tên khách hàng: ").strip()
        if not customer_name:
            print("[Lỗi] Tên khách hàng không được để trống.")
            return

        # 1. Chọn thú cưng
        pet_id = input("Nhập ID thú cưng của khách hàng: ").strip()
        pet = self.pet_service.search_pet_by_id(pet_id)
        if not pet:
            print("[Lỗi] Không tìm thấy thú cưng này trong hệ thống. Vui lòng thêm thú cưng trước.")
            return

        # 2. Chọn dịch vụ chăm sóc Spa
        care_services = []
        while True:
            print("\n--- Chọn dịch vụ chăm sóc Spa ---")
            print("1. Tắm rửa (Bathing)")
            print("2. Cắt tỉa lông (Trimming)")
            print("3. Gửi nội trú qua đêm (Boarding)")
            print("0. Hoàn thành việc chọn dịch vụ")
            choice = input("Lựa chọn dịch vụ: ").strip()

            if choice == "1":
                # Tránh trùng lặp dịch vụ tắm trong 1 lần giao dịch
                if any(isinstance(s, BathingService) for s in care_services):
                    print("[Thông báo] Dịch vụ Tắm rửa đã được thêm trước đó.")
                else:
                    care_services.append(BathingService())
                    print("[Thành công] Đã thêm dịch vụ Tắm rửa.")
            elif choice == "2":
                if any(isinstance(s, TrimmingService) for s in care_services):
                    print("[Thông báo] Dịch vụ Cắt tỉa lông đã được thêm trước đó.")
                else:
                    care_services.append(TrimmingService())
                    print("[Thành công] Đã thêm dịch vụ Cắt tỉa lông.")
            elif choice == "3":
                if any(isinstance(s, BoardingService) for s in care_services):
                    print("[Thông báo] Dịch vụ Nội trú đã được thêm trước đó.")
                else:
                    try:
                        days = int(input("Nhập số ngày muốn gửi nội trú: "))
                        if days <= 0:
                            raise ValueError()
                    except ValueError:
                        print("[Lỗi] Số ngày gửi phải là số nguyên dương lớn hơn 0.")
                        continue
                    care_services.append(BoardingService(days))
                    print(f"[Thành công] Đã thêm dịch vụ Nội trú ({days} ngày).")
            elif choice == "0":
                break
            else:
                print("[Lỗi] Lựa chọn không hợp lệ.")

        # 3. Chọn mua sản phẩm đi kèm (Thức ăn, cát vệ sinh, dầu tắm...)
        purchased_products = []
        buy_product = input("\nKhách hàng có muốn mua thêm sản phẩm đi kèm không? (y/n): ").strip().lower()
        
        if buy_product == "y":
            while True:
                print("\n--- DANH SÁCH SẢN PHẨM CÓ SẴN ---")
                self.product_service.display_products()
                
                prod_id = input("Nhập ID sản phẩm muốn mua (hoặc gõ '0' để kết thúc): ").strip()
                if prod_id == "0":
                    break

                prod = self.product_service.search_product_by_id(prod_id)
                if not prod:
                    print("[Lỗi] Không tìm thấy sản phẩm.")
                    continue

                try:
                    qty = int(input(f"Nhập số lượng mua cho '{prod.name}' (Tồn: {prod.stock}): "))
                    if qty <= 0:
                        print("[Lỗi] Số lượng mua phải lớn hơn 0.")
                        continue
                except ValueError:
                    print("[Lỗi] Số lượng phải là số nguyên.")
                    continue

                # Kiểm tra tồn kho tạm thời (hoặc để InvoiceService xử lý)
                if prod.stock < qty:
                    print(f"[Lỗi] Không đủ hàng trong kho. Hiện tại chỉ còn {prod.stock} sản phẩm.")
                    continue

                # Kiểm tra xem sản phẩm đã có trong giỏ hàng tạm chưa
                found_in_cart = False
                for item in purchased_products:
                    if item["product"].product_id == prod.product_id:
                        if prod.stock < (item["quantity"] + qty):
                            print(f"[Lỗi] Tổng số lượng yêu cầu vượt quá tồn kho hiện có.")
                        else:
                            item["quantity"] += qty
                            print(f"[Thành công] Đã cập nhật số lượng mua cho {prod.name}.")
                        found_in_cart = True
                        break

                if not found_in_cart:
                    purchased_products.append({"product": prod, "quantity": qty})
                    print(f"[Thành công] Đã thêm {qty} sản phẩm '{prod.name}' vào giỏ hàng.")

                more = input("Tiếp tục mua sản phẩm khác? (y/n): ").strip().lower()
                if more != "y":
                    break

        if not care_services and not purchased_products:
            print("[Hủy] Bạn chưa chọn dịch vụ hoặc sản phẩm nào. Hóa đơn bị hủy.")
            return

        # 4. Áp dụng mã giảm giá
        print("\nCác mã giảm giá khả dụng:")
        print("- SPA10   : Giảm 10% phí dịch vụ Spa")
        print("- PET10   : Giảm 10% giá trị sản phẩm mua kèm")
        print("- STORE15 : Giảm 15% tổng giá trị hóa đơn (Spa + Sản phẩm)")
        print("- VIP50   : Giảm thẳng 50.000 VND trên hóa đơn (cho đơn từ 50.000 VND trở lên)")
        discount_code = input("Nhập mã giảm giá (nếu có, nhấn Enter để bỏ qua): ").strip().upper()

        # 5. Thực hiện tạo hóa đơn & trừ kho (Logic giao dịch trong Try-Except)
        try:
            invoice = self.invoice_service.create_invoice(
                customer_name, pet, care_services, purchased_products, discount_code
            )
            print("\n=============================================")
            print("          HÓA ĐƠN THANH TOÁN THÀNH CÔNG       ")
            print("=============================================")
            print(invoice.get_info())
            print("=============================================")
            
            # Hỏi người dùng muốn xuất file PDF không
            pdf_choice = input("Bạn có muốn xuất hóa đơn này ra file PDF không? (y/n): ").strip().lower()
            if pdf_choice == "y":
                filename = f"data/invoice_{invoice.invoice_id}.pdf"
                self.invoice_service.export_invoice_pdf(invoice, filename)
                print(f"[Thành công] Đã xuất hóa đơn ra file '{filename}'")
                
        except ValueError as err:
            print(f"\n[Giao dịch thất bại] {err}")

    # ================= THỐNG KÊ & BÁO CÁO =================
    def statistics_menu(self):
        print("\n================ BÁO CÁO THỐNG KÊ DOANH THU ================")
        total_inv = len(self.invoice_service.invoices)
        print(f"Tổng số hóa đơn đã thực hiện : {total_inv}")
        print(f"Tổng doanh thu toàn cửa hàng  : {self.invoice_service.total_revenue():,.0f} VND")
        print(f"Dịch vụ Spa được dùng nhiều nhất: {self.invoice_service.most_used_service()}")
        
        # 1. Thống kê theo dịch vụ
        print("\n1. Doanh thu phân tích theo dịch vụ Spa:")
        rev_by_s = self.invoice_service.revenue_by_service()
        for service, rev in rev_by_s.items():
            print(f" - Dịch vụ {service:<12}: {rev:,.0f} VND")

        # 2. Thống kê theo tháng
        print("\n2. Doanh thu thống kê theo từng tháng:")
        rev_by_m = self.invoice_service.revenue_by_month()
        if not rev_by_m:
            print(" - Chưa có dữ liệu doanh thu tháng nào.")
        else:
            for month, rev in sorted(rev_by_m.items()):
                print(f" - Tháng {month:<12}: {rev:,.0f} VND")

        # 3. Top sản phẩm bán chạy nhất
        print("\n3. Top 3 sản phẩm bán chạy nhất:")
        top_p = self.invoice_service.top_products(limit=3)
        if not top_p:
            print(" - Chưa bán được sản phẩm nào.")
        else:
            for idx, (p_name, qty) in enumerate(top_p, 1):
                print(f" Top {idx}. Sản phẩm '{p_name}': Đã bán {qty} chiếc")

        # 4. Số lượng thú cưng trong hệ thống
        dog_count = sum(1 for pet in self.pet_service.pets if isinstance(pet, Dog))
        cat_count = sum(1 for pet in self.pet_service.pets if isinstance(pet, Cat))
        bird_count = sum(1 for pet in self.pet_service.pets if isinstance(pet, Bird))
        print(f"\n4. Số lượng thú cưng đang chăm sóc: {dog_count + cat_count + bird_count} con")
        print(f" - Chó: {dog_count} con | Mèo: {cat_count} con | Chim: {bird_count} con")
        print("==========================================================")

        export_pdf_choice = input("Bạn có muốn xuất toàn bộ báo cáo này ra tệp PDF không? (y/n): ").strip().lower()
        if export_pdf_choice == "y":
            filename = "data/report.pdf"
            self.invoice_service.export_report_pdf(filename)
            print(f"[Thành công] Đã xuất báo cáo thống kê ra tệp '{filename}'")