class Product:
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Product name cannot be empty")
        self.__name = value.strip()

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        value = float(value)
        if value < 0:
            raise ValueError("Product price cannot be negative")
        self.__price = value

    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, value):
        value = int(value)
        if value < 0:
            raise ValueError("Product stock cannot be negative")
        self.__stock = value

    def get_info(self):
        return f"{self.product_id} | {self.name} | Price: {self.price:,.0f} VND | Stock: {self.stock}"

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }
