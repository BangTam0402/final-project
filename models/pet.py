class Pet:
    def __init__(self, pet_id, name, breed, weight, price):
        self.__pet_id = pet_id
        self.__name = name
        self.__breed = breed
        self.__weight = weight
        self.__price = price

    @property
    def pet_id(self):
        return self.__pet_id

    @property
    def name(self):
        return self.__name

    @property
    def breed(self):
        return self.__breed

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        if value <= 0:
            raise ValueError("Weight must be greater than 0")
        self.__weight = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self.__price = value

    def get_info(self):
        return f"{self.pet_id} | {self.name} | {self.breed} | {self.weight}kg | {self.price} VND"


class Dog(Pet):
    def get_info(self):
        return "[Dog] " + super().get_info()


class Cat(Pet):
    def get_info(self):
        return "[Cat] " + super().get_info()


class Bird(Pet):
    def get_info(self):
        return "[Bird] " + super().get_info()