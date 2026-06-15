import json
import csv
from collections import Counter
from models.invoice import Invoice


class InvoiceService:
    def __init__(self):
        self.__invoices = []

    @property
    def invoices(self):
        return self.__invoices

    def create_invoice(self, customer_name, pet, care_services, purchased_products=None, discount_code=None):
        purchased_products = purchased_products if purchased_products else []
        
        # Validate and deduct stock (Complex Transaction Logic)
        for item in purchased_products:
            product = item["product"]
            quantity = item["quantity"]
            if quantity <= 0:
                raise ValueError(f"Quantity for product {product.name} must be greater than 0")
            if product.stock < quantity:
                raise ValueError(f"Product '{product.name}' is out of stock. Available: {product.stock}, Requested: {quantity}")

        # Deduct stock
        for item in purchased_products:
            product = item["product"]
            quantity = item["quantity"]
            product.stock -= quantity

        # Generate invoice ID
        invoice_id = f"I{len(self.__invoices) + 1:03d}"
        
        # Create invoice object
        invoice = Invoice(
            invoice_id=invoice_id,
            customer_name=customer_name,
            pet=pet,
            care_services=care_services,
            purchased_products=purchased_products,
            discount_code=discount_code
        )
        self.__invoices.append(invoice)
        return invoice

    def display_invoices(self):
        if not self.__invoices:
            print("No invoices available.")
            return

        for invoice in self.__invoices:
            print("-" * 50)
            print(invoice.get_info())
        print("-" * 50)

    def total_revenue(self):
        return sum(invoice.total for invoice in self.__invoices)

    def most_used_service(self):
        if not self.__invoices:
            return "No data"

        service_names = []
        for invoice in self.__invoices:
            service_names.extend(invoice.service_names)

        if not service_names:
            return "None"

        counter = Counter(service_names)
        return counter.most_common(1)[0][0]

    def revenue_by_service(self):
        rev = {"Bathing": 0.0, "Trimming": 0.0, "Boarding": 0.0}
        for invoice in self.__invoices:
            for service in invoice.care_services:
                rev[service.name] = rev.get(service.name, 0.0) + service.calculate_price(invoice.pet)
        return rev

    def revenue_by_month(self):
        rev = {}
        for invoice in self.__invoices:
            try:
                month = invoice.created_at[:7]  # YYYY-MM
            except Exception:
                month = "Unknown"
            rev[month] = rev.get(month, 0.0) + invoice.total
        return rev

    def top_products(self, limit=3):
        product_counts = {}
        for invoice in self.__invoices:
            for item in invoice.purchased_products:
                name = item["product"].name
                qty = item["quantity"]
                product_counts[name] = product_counts.get(name, 0) + qty
        sorted_products = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_products[:limit]

    def save_to_file(self, filename="data/invoices.json"):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump([invoice.to_dict() for invoice in self.__invoices], file, indent=4, ensure_ascii=False)

    def load_from_file(self, pet_service, product_service, filename="data/invoices.json"):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.__invoices.clear()
            from models.invoice import Invoice
            from models.service import BathingService, TrimmingService, BoardingService

            for item in data:
                # Find pet
                pet_id = item["pet_id"]
                pet = pet_service.search_pet_by_id(pet_id)
                if not pet:
                    from models.pet import Dog, Cat, Bird
                    pet_breed = item["pet_breed"]
                    pet_name = item["pet_name"]
                    if "dog" in pet_breed.lower():
                        pet = Dog(pet_id, pet_name, pet_breed, 5.0, 0.0)
                    elif "cat" in pet_breed.lower():
                        pet = Cat(pet_id, pet_name, pet_breed, 4.0, 0.0)
                    else:
                        pet = Bird(pet_id, pet_name, pet_breed, 0.5, 0.0)

                # Reconstruct services
                care_services = []
                # Check for detailed service representation if exists
                if "services_detail" in item:
                    for s_item in item["services_detail"]:
                        s_name = s_item["name"]
                        if s_name == "Bathing":
                            care_services.append(BathingService())
                        elif s_name == "Trimming":
                            care_services.append(TrimmingService())
                        elif s_name == "Boarding":
                            days = s_item.get("days", 1)
                            care_services.append(BoardingService(days))
                else:
                    for s_name in item.get("services", []):
                        if s_name == "Bathing":
                            care_services.append(BathingService())
                        elif s_name == "Trimming":
                            care_services.append(TrimmingService())
                        elif s_name == "Boarding":
                            care_services.append(BoardingService(1))

                # Reconstruct purchased products
                purchased_products = []
                for p_item in item.get("products", []):
                    p_id = p_item["product_id"]
                    qty = p_item["quantity"]
                    product = product_service.search_product_by_id(p_id)
                    if not product:
                        from models.product import Product
                        product = Product(p_id, p_item["name"], p_item["price"], 0)
                    purchased_products.append({"product": product, "quantity": qty})

                invoice = Invoice(
                    invoice_id=item["invoice_id"],
                    customer_name=item["customer_name"],
                    pet=pet,
                    care_services=care_services,
                    purchased_products=purchased_products,
                    discount_code=item.get("discount_code", ""),
                    created_at=item["created_at"]
                )
                self.__invoices.append(invoice)
        except (FileNotFoundError, json.JSONDecodeError):
            self.__invoices = []

    def export_csv(self, filename="data/report.csv"):
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Invoice ID", "Customer Name", "Pet ID", "Pet Name", "Pet Breed", "Services", "Products", "Discount Code", "Discount Amount (VND)", "Total (VND)", "Date"])

            for invoice in self.__invoices:
                data = invoice.to_dict()
                services_str = ", ".join(data["services"])
                products_list = [f"{p['name']} (x{p['quantity']})" for p in data["products"]]
                products_str = ", ".join(products_list)
                writer.writerow([
                    data["invoice_id"],
                    data["customer_name"],
                    data["pet_id"],
                    data["pet_name"],
                    data["pet_breed"],
                    services_str,
                    products_str,
                    data["discount_code"],
                    f"{data['discount_amount']:.0f}",
                    f"{data['total']:.0f}",
                    data["created_at"]
                ])

    def _create_pdf(self, filename, title, lines):
        # A simple, robust, dependency-free PDF writer
        def remove_accents(input_str):
            s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỶỷỸỹỴỵ'
            s0 = u'AAAAEEEIIOOOUUYaaaaeeeiiooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
            s = ''
            for c in input_str:
                if c in s1:
                    s += s0[s1.index(c)]
                else:
                    s += c
            return s

        clean_title = remove_accents(title)
        clean_lines = [remove_accents(line) for line in lines]

        # Draw content stream
        stream = []
        stream.append("BT")
        stream.append("/F1 16 Tf")
        stream.append("50 780 Td")
        stream.append("22 TL")
        stream.append(f"({clean_title}) Tj T*")
        stream.append("/F1 10 Tf")
        stream.append("14 TL")
        stream.append("T*")  # spacing
        
        for line in clean_lines:
            escaped = line.replace("(", "\\(").replace(")", "\\)")
            stream.append(f"({escaped}) Tj T*")
            
        stream.append("ET")
        
        stream_str = "\n".join(stream)
        stream_bytes = stream_str.encode('ascii', errors='ignore')
        
        # Build PDF structure
        objects = {}
        objects[1] = b"<< /Type /Catalog /Pages 2 0 R >>"
        objects[2] = b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>"
        objects[3] = b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
        objects[4] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
        objects[5] = f"<< /Length {len(stream_bytes)} >>\nstream\n".encode('ascii') + stream_bytes + b"\nendstream"
        
        with open(filename, "wb") as f:
            f.write(b"%PDF-1.4\n")
            offsets = {}
            for i in range(1, 6):
                offsets[i] = f.tell()
                f.write(f"{i} 0 obj\n".encode('ascii'))
                f.write(objects[i])
                f.write(b"\nendobj\n")
                
            xref_offset = f.tell()
            f.write(b"xref\n")
            f.write(b"0 6\n")
            f.write(b"0000000000 65535 f \n")
            for i in range(1, 6):
                f.write(f"{offsets[i]:010d} 00000 n \n".encode('ascii'))
                
            f.write(b"trailer\n")
            f.write(b"<< /Size 6 /Root 1 0 R >>\n")
            f.write(b"startxref\n")
            f.write(f"{xref_offset}\n".encode('ascii'))
            f.write(b"%%EOF\n")

    def export_invoice_pdf(self, invoice, filename):
        lines = []
        lines.append("=" * 60)
        lines.append(f"Customer Name: {invoice.customer_name}")
        lines.append(f"Pet: {invoice.pet.name} ({invoice.pet.__class__.__name__} - {invoice.pet.breed})")
        lines.append("-" * 60)
        lines.append("SPA SERVICES:")
        if invoice.care_services:
            for s in invoice.care_services:
                price = s.calculate_price(invoice.pet)
                lines.append(f" - {s.name:<20}: {price:,.0f} VND")
        else:
            lines.append(" - None")
            
        lines.append("-" * 60)
        lines.append("PURCHASED PRODUCTS:")
        if invoice.purchased_products:
            for item in invoice.purchased_products:
                p = item["product"]
                qty = item["quantity"]
                cost = p.price * qty
                lines.append(f" - {p.name:<20} (x{qty:<2}): {cost:,.0f} VND  (Unit: {p.price:,.0f} VND)")
        else:
            lines.append(" - None")
            
        lines.append("-" * 60)
        if invoice.discount_code:
            lines.append(f"Discount Code       : {invoice.discount_code}")
            lines.append(f"Discount Amount     : -{invoice.discount_amount:,.0f} VND")
        lines.append(f"TOTAL AMOUNT        : {invoice.total:,.0f} VND")
        lines.append("=" * 60)
        lines.append(f"Date: {invoice.created_at}")
        
        self._create_pdf(filename, f"INVOICE SUMMARY {invoice.invoice_id}", lines)

    def export_report_pdf(self, filename="data/report.pdf"):
        lines = []
        lines.append("=" * 60)
        lines.append(f"Total Invoices      : {len(self.__invoices)}")
        lines.append(f"Total Revenue       : {self.total_revenue():,.0f} VND")
        lines.append(f"Most Used Service   : {self.most_used_service()}")
        lines.append("-" * 60)
        lines.append("REVENUE BY SERVICE:")
        for s, rev in self.revenue_by_service().items():
            lines.append(f" - {s:<20}: {rev:,.0f} VND")
            
        lines.append("-" * 60)
        lines.append("REVENUE BY MONTH:")
        for month, rev in sorted(self.revenue_by_month().items()):
            lines.append(f" - {month:<20}: {rev:,.0f} VND")
            
        lines.append("-" * 60)
        lines.append("TOP 3 BEST SELLING PRODUCTS:")
        top_p = self.top_products()
        if top_p:
            for p_name, qty in top_p:
                lines.append(f" - {p_name:<20}: {qty} units")
        else:
            lines.append(" - No product sales yet")
            
        lines.append("-" * 60)
        lines.append("LIST OF TRANSACTIONS:")
        for invoice in self.__invoices:
            lines.append(f" {invoice.invoice_id} | {invoice.customer_name:<15} | {invoice.total:>10,.0f} VND | {invoice.created_at}")
        lines.append("=" * 60)
        
        self._create_pdf(filename, "PET SPA & STORE SALES REPORT", lines)