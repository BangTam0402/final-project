class Pet:
    def __init__(self, pet_id, name, breed, weight, price):
        self.__pet_id = pet_id
        self.name = name
        self.breed = breed
        self.weight = weight
        self.price = price

    @property
    def pet_id(self):
        return self.__pet_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self.__name = value

    @property
    def breed(self):
        return self.__breed

    @breed.setter
    def breed(self, value):
        if not value.strip():
            raise ValueError("Breed cannot be empty")
        self.__breed = value

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Weight must be greater than 0")
        self.__weight = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        value = float(value)
        if value < 0:
            raise ValueError("Price cannot be negative")
        self.__price = value

    def get_info(self):
        return f"{self.pet_id} | {self.name} | {self.breed} | {self.weight}kg | {self.price:,.0f} VND"

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "pet_id": self.pet_id,
            "name": self.name,
            "breed": self.breed,
            "weight": self.weight,
            "price": self.price
        }


class Dog(Pet):
    def get_info(self):
        return "[Dog] " + super().get_info()


class Cat(Pet):
    def get_info(self):
        return "[Cat] " + super().get_info()


class Bird(Pet):
    def get_info(self):
        return "[Bird] " + super().get_info()