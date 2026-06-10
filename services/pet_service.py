import json
from models.pet import Dog, Cat, Bird


class PetService:
    def __init__(self):
        self.__pets = []

    @property
    def pets(self):
        return self.__pets

    def add_pet(self, pet):
        if self.search_pet_by_id(pet.pet_id):
            raise ValueError("Pet ID already exists")
        self.__pets.append(pet)

    def display_pets(self):
        if not self.__pets:
            print("No pets available.")
            return

        for pet in self.__pets:
            print(pet.get_info())

    def search_pet_by_id(self, pet_id):
        for pet in self.__pets:
            if pet.pet_id.lower() == pet_id.lower():
                return pet
        return None

    def search_pet_by_name(self, name):
        return [pet for pet in self.__pets if name.lower() in pet.name.lower()]

    def update_pet(self, pet_id, name=None, breed=None, weight=None, price=None):
        pet = self.search_pet_by_id(pet_id)
        if not pet:
            return False

        if name:
            pet.name = name
        if breed:
            pet.breed = breed
        if weight is not None:
            pet.weight = weight
        if price is not None:
            pet.price = price

        return True

    def delete_pet(self, pet_id):
        pet = self.search_pet_by_id(pet_id)
        if pet:
            self.__pets.remove(pet)
            return True
        return False

    def sort_by_price(self):
        self.__pets.sort(key=lambda pet: pet.price, reverse=True)

    def sort_by_weight(self):
        self.__pets.sort(key=lambda pet: pet.weight, reverse=True)

    def save_to_file(self, filename="data/pets.json"):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump([pet.to_dict() for pet in self.__pets], file, indent=4, ensure_ascii=False)

    def load_from_file(self, filename="data/pets.json"):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.__pets.clear()

            for item in data:
                pet_type = item["type"]

                if pet_type == "Dog":
                    pet = Dog(item["pet_id"], item["name"], item["breed"], item["weight"], item["price"])
                elif pet_type == "Cat":
                    pet = Cat(item["pet_id"], item["name"], item["breed"], item["weight"], item["price"])
                else:
                    pet = Bird(item["pet_id"], item["name"], item["breed"], item["weight"], item["price"])

                self.__pets.append(pet)

        except (FileNotFoundError, json.JSONDecodeError):
            self.__pets = []