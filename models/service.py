from abc import ABC, abstractmethod


class CareService(ABC):
    def __init__(self, service_id, name):
        self.__service_id = service_id
        self.__name = name

    @property
    def service_id(self):
        return self.__service_id

    @property
    def name(self):
        return self.__name

    @abstractmethod
    def calculate_price(self, pet):
        pass


class BathingService(CareService):
    def __init__(self):
        super().__init__("S01", "Bathing")

    def calculate_price(self, pet):
        breed_fee = 30000 if pet.breed.lower() in ["poodle", "persian", "british shorthair"] else 0
        return 50000 + pet.weight * 10000 + breed_fee


class TrimmingService(CareService):
    def __init__(self):
        super().__init__("S02", "Trimming")

    def calculate_price(self, pet):
        breed_fee = 50000 if pet.breed.lower() in ["poodle", "persian"] else 0
        return 80000 + pet.weight * 15000 + breed_fee


class BoardingService(CareService):
    def __init__(self, days=1):
        super().__init__("S03", "Boarding")
        self.__days = int(days)

    @property
    def days(self):
        return self.__days

    def calculate_price(self, pet):
        return self.days * 100000 + pet.weight * 5000