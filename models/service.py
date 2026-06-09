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
        return 50000 + pet.weight * 10000


class TrimmingService(CareService):
    def __init__(self):
        super().__init__("S02", "Trimming")

    def calculate_price(self, pet):
        return 80000 + pet.weight * 15000


class BoardingService(CareService):
    def __init__(self, days):
        super().__init__("S03", "Boarding")
        self.__days = days

    def calculate_price(self, pet):
        return self.__days * 100000 + pet.weight * 5000