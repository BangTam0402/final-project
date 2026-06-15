import sqlite3
import json


class DatabaseService:
    def __init__(self, db_name="data/pet_store.db"):
        self.db_name = db_name
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()

        # Create table for pets
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                pet_id TEXT PRIMARY KEY,
                type TEXT,
                name TEXT,
                breed TEXT,
                weight REAL,
                price REAL
            )
        """)

        # Create table for products
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                name TEXT,
                price REAL,
                stock INTEGER
            )
        """)

        # Check and handle table schema migration for invoices
        try:
            cursor.execute("PRAGMA table_info(invoices)")
            columns = cursor.fetchall()
            if columns and len(columns) < 11:
                # Dropping the old table to recreate with new schema
                cursor.execute("DROP TABLE IF EXISTS invoices")
        except sqlite3.OperationalError:
            pass

        # Create table for invoices with new schema
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                invoice_id TEXT PRIMARY KEY,
                customer_name TEXT,
                pet_id TEXT,
                pet_name TEXT,
                pet_breed TEXT,
                services TEXT,
                products TEXT,
                discount_code TEXT,
                discount_amount REAL,
                total REAL,
                created_at TEXT
            )
        """)

        conn.commit()
        conn.close()

    def load_pets(self):
        conn = self.connect()
        cursor = conn.cursor()
        pets = []
        try:
            cursor.execute("SELECT pet_id, type, name, breed, weight, price FROM pets")
            rows = cursor.fetchall()
            from models.pet import Dog, Cat, Bird
            for row in rows:
                pet_id, pet_type, name, breed, weight, price = row
                if pet_type == "Dog":
                    pet = Dog(pet_id, name, breed, weight, price)
                elif pet_type == "Cat":
                    pet = Cat(pet_id, name, breed, weight, price)
                else:
                    pet = Bird(pet_id, name, breed, weight, price)
                pets.append(pet)
        except sqlite3.OperationalError:
            pass
        conn.close()
        return pets

    def load_products(self):
        conn = self.connect()
        cursor = conn.cursor()
        products = []
        try:
            cursor.execute("SELECT product_id, name, price, stock FROM products")
            rows = cursor.fetchall()
            from models.product import Product
            for row in rows:
                product_id, name, price, stock = row
                product = Product(product_id, name, price, stock)
                products.append(product)
        except sqlite3.OperationalError:
            pass
        conn.close()
        return products

    def load_invoices(self, pet_service, product_service):
        conn = self.connect()
        cursor = conn.cursor()
        invoices = []
        try:
            cursor.execute("""
                SELECT invoice_id, customer_name, pet_id, pet_name, pet_breed, services, products, discount_code, discount_amount, total, created_at 
                FROM invoices
            """)
            rows = cursor.fetchall()
            from models.invoice import Invoice
            from models.service import BathingService, TrimmingService, BoardingService
            
            for row in rows:
                invoice_id, customer_name, pet_id, pet_name, pet_breed, services_json, products_json, discount_code, discount_amount, total, created_at = row
                
                # Find pet in pet service
                pet = pet_service.search_pet_by_id(pet_id)
                if not pet:
                    # Fallback to recreate a temporary pet object
                    from models.pet import Dog, Cat, Bird
                    if "dog" in pet_breed.lower():
                        pet = Dog(pet_id, pet_name, pet_breed, 5.0, 0.0)
                    elif "cat" in pet_breed.lower():
                        pet = Cat(pet_id, pet_name, pet_breed, 4.0, 0.0)
                    else:
                        pet = Bird(pet_id, pet_name, pet_breed, 0.5, 0.0)
                
                # Reconstruct care services from JSON string
                care_services = []
                if services_json:
                    try:
                        services_data = json.loads(services_json)
                        for s_item in services_data:
                            s_name = s_item.get("name")
                            if s_name == "Bathing":
                                care_services.append(BathingService())
                            elif s_name == "Trimming":
                                care_services.append(TrimmingService())
                            elif s_name == "Boarding":
                                days = s_item.get("days", 1)
                                care_services.append(BoardingService(days))
                    except Exception:
                        # Fallback for comma separated names
                        for s_name in services_json.split(","):
                            s_name = s_name.strip()
                            if s_name == "Bathing":
                                care_services.append(BathingService())
                            elif s_name == "Trimming":
                                care_services.append(TrimmingService())
                            elif s_name == "Boarding":
                                care_services.append(BoardingService(1))
                
                # Reconstruct purchased products from JSON string
                purchased_products = []
                if products_json:
                    try:
                        products_data = json.loads(products_json)
                        for p_item in products_data:
                            p_id = p_item.get("product_id")
                            qty = p_item.get("quantity", 1)
                            product = product_service.search_product_by_id(p_id)
                            if not product:
                                from models.product import Product
                                product = Product(p_id, p_item.get("name", "Unknown Product"), p_item.get("price", 0.0), 0)
                            purchased_products.append({"product": product, "quantity": qty})
                    except Exception:
                        pass

                invoice = Invoice(
                    invoice_id=invoice_id,
                    customer_name=customer_name,
                    pet=pet,
                    care_services=care_services,
                    purchased_products=purchased_products,
                    discount_code=discount_code,
                    created_at=created_at
                )
                invoices.append(invoice)
        except sqlite3.OperationalError:
            pass
        conn.close()
        return invoices

    def save_pets(self, pets):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pets")
        for pet in pets:
            cursor.execute("""
                INSERT INTO pets VALUES (?, ?, ?, ?, ?, ?)
            """, (
                pet.pet_id,
                pet.__class__.__name__,
                pet.name,
                pet.breed,
                pet.weight,
                pet.price
            ))
        conn.commit()
        conn.close()

    def save_products(self, products):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products")
        for product in products:
            cursor.execute("""
                INSERT INTO products VALUES (?, ?, ?, ?)
            """, (
                product.product_id,
                product.name,
                product.price,
                product.stock
            ))
        conn.commit()
        conn.close()

    def save_invoices(self, invoices):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM invoices")
        for invoice in invoices:
            # Services as JSON
            services_list = []
            for s in invoice.care_services:
                s_dict = {"name": s.name}
                if hasattr(s, "days"):
                    s_dict["days"] = s.days
                services_list.append(s_dict)
            services_json = json.dumps(services_list)

            # Products as JSON
            products_list = []
            for item in invoice.purchased_products:
                products_list.append({
                    "product_id": item["product"].product_id,
                    "name": item["product"].name,
                    "price": item["product"].price,
                    "quantity": item["quantity"]
                })
            products_json = json.dumps(products_list)

            cursor.execute("""
                INSERT INTO invoices VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                invoice.invoice_id,
                invoice.customer_name,
                invoice.pet.pet_id,
                invoice.pet.name,
                invoice.pet.breed,
                services_json,
                products_json,
                invoice.discount_code,
                invoice.discount_amount,
                invoice.total,
                invoice.created_at
            ))
        conn.commit()
        conn.close()