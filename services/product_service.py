import json
from models.product import Product


class ProductService:
    def __init__(self):
        self.__products = []

    @property
    def products(self):
        return self.__products

    def add_product(self, product):
        if self.search_product_by_id(product.product_id):
            raise ValueError("Product ID already exists")
        self.__products.append(product)

    def display_products(self):
        if not self.__products:
            print("No products available.")
            return

        print("-" * 60)
        print(f"{'Product ID':<12} | {'Name':<20} | {'Price (VND)':<12} | {'Stock':<6}")
        print("-" * 60)
        for product in self.__products:
            print(f"{product.product_id:<12} | {product.name:<20} | {product.price:<12,.0f} | {product.stock:<6}")
        print("-" * 60)

    def search_product_by_id(self, product_id):
        for product in self.__products:
            if product.product_id.lower() == product_id.lower().strip():
                return product
        return None

    def search_product_by_name(self, name):
        name_lower = name.lower().strip()
        return [p for p in self.__products if name_lower in p.name.lower()]

    def update_product(self, product_id, name=None, price=None, stock=None):
        product = self.search_product_by_id(product_id)
        if not product:
            return False

        if name:
            product.name = name
        if price is not None:
            product.price = price
        if stock is not None:
            product.stock = stock

        return True

    def delete_product(self, product_id):
        product = self.search_product_by_id(product_id)
        if product:
            self.__products.remove(product)
            return True
        return False

    def sort_by_price(self, reverse=True):
        self.__products.sort(key=lambda p: p.price, reverse=reverse)

    def sort_by_stock(self, reverse=True):
        self.__products.sort(key=lambda p: p.stock, reverse=reverse)

    def save_to_file(self, filename="data/products.json"):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump([product.to_dict() for product in self.__products], file, indent=4, ensure_ascii=False)

    def load_from_file(self, filename="data/products.json"):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.__products.clear()
            for item in data:
                product = Product(item["product_id"], item["name"], item["price"], item["stock"])
                self.__products.append(product)
        except (FileNotFoundError, json.JSONDecodeError):
            self.__products = []
