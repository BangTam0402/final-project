from datetime import datetime


class Invoice:
    def __init__(self, invoice_id, customer_name, pet, care_services, purchased_products=None, discount_code=None, created_at=None):
        self.__invoice_id = invoice_id
        self.__customer_name = customer_name
        self.__pet = pet
        self.__care_services = care_services if care_services else []
        self.__purchased_products = purchased_products if purchased_products else []
        self.__discount_code = discount_code if discount_code else ""
        self.__created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__discount_amount = 0.0
        self.__total = 0.0
        self.calculate_total()

    @property
    def invoice_id(self):
        return self.__invoice_id

    @property
    def customer_name(self):
        return self.__customer_name

    @property
    def pet(self):
        return self.__pet

    @property
    def care_services(self):
        return self.__care_services

    @property
    def purchased_products(self):
        return self.__purchased_products

    @property
    def discount_code(self):
        return self.__discount_code

    @property
    def discount_amount(self):
        return self.__discount_amount

    @property
    def total(self):
        return self.__total

    @property
    def created_at(self):
        return self.__created_at

    @property
    def service_names(self):
        return [service.name for service in self.__care_services]

    def calculate_total(self):
        total_services = sum(service.calculate_price(self.__pet) for service in self.__care_services)
        total_products = sum(item["product"].price * item["quantity"] for item in self.__purchased_products)
        subtotal = total_services + total_products

        discount_amount = 0.0
        code = self.__discount_code.upper().strip()
        if code == "SPA10":
            discount_amount = total_services * 0.10
        elif code == "PET10":
            discount_amount = total_products * 0.10
        elif code == "STORE15":
            discount_amount = subtotal * 0.15
        elif code == "VIP50":
            if subtotal >= 50000:
                discount_amount = 50000.0
            else:
                discount_amount = subtotal

        self.__discount_amount = discount_amount
        self.__total = max(0.0, subtotal - discount_amount)

    def get_info(self):
        services_str = ", ".join(self.service_names) if self.__care_services else "None"
        
        products_list = []
        for item in self.__purchased_products:
            products_list.append(f"{item['product'].name} (x{item['quantity']})")
        products_str = ", ".join(products_list) if products_list else "None"
        
        info = (
            f"Invoice ID: {self.invoice_id}\n"
            f"Customer: {self.customer_name}\n"
            f"Pet: {self.pet.name} ({self.pet.__class__.__name__} - {self.pet.breed})\n"
            f"Services: {services_str}\n"
            f"Products: {products_str}\n"
        )
        if self.discount_code:
            info += f"Discount Code: {self.discount_code} (-{self.discount_amount:,.0f} VND)\n"
        info += (
            f"Total Price: {self.total:,.0f} VND\n"
            f"Date: {self.created_at}"
        )
        return info

    def to_dict(self):
        return {
            "invoice_id": self.invoice_id,
            "customer_name": self.customer_name,
            "pet_id": self.pet.pet_id,
            "pet_name": self.pet.name,
            "pet_breed": self.pet.breed,
            "services": self.service_names,
            "services_detail": [
                {"name": s.name, "days": s.days if hasattr(s, "days") else 0}
                for s in self.care_services
            ],
            "products": [
                {
                    "product_id": item["product"].product_id,
                    "name": item["product"].name,
                    "price": item["product"].price,
                    "quantity": item["quantity"]
                }
                for item in self.purchased_products
            ],
            "discount_code": self.discount_code,
            "discount_amount": self.discount_amount,
            "total": self.total,
            "created_at": self.created_at
        }