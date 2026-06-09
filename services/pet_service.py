class PetService:
    def __init__(self):
        self.__pets = []

    def add_pet(self, pet):
        self.__pets.append(pet)

    def show_pets(self):
        if not self.__pets:
            print("No pets available.")
            return

        for pet in self.__pets:
            print(pet.get_info())

    def search_pet_by_name(self, name):
        for pet in self.__pets:
            if pet.name.lower() == name.lower():
                return pet
        return None

    def search_pet_by_id(self, pet_id):
        for pet in self.__pets:
            if pet.pet_id.lower() == pet_id.lower():
                return pet
        return None

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

    @property
    def pets(self):
        return self.__pets