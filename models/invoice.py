from datetime import datetime


class Invoice:
    def __init__(self, invoice_id, customer_name, pet, care_services):
        self.__invoice_id = invoice_id
        self.__customer_name = customer_name
        self.__pet = pet
        self.__care_services = care_services
        self.__created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__total = self.calculate_total()

    @property
    def invoice_id(self):
        return self.__invoice_id

    @property
    def total(self):
        return self.__total

    @property
    def service_names(self):
        return [service.name for service in self.__care_services]

    def calculate_total(self):
        total = 0
        for service in self.__care_services:
            total += service.calculate_price(self.__pet)
        return total

    def get_info(self):
        return (
            f"Invoice ID: {self.__invoice_id}\n"
            f"Customer: {self.__customer_name}\n"
            f"Pet: {self.__pet.name}\n"
            f"Services: {', '.join(self.service_names)}\n"
            f"Total: {self.__total:,.0f} VND\n"
            f"Date: {self.__created_at}"
        )

    def to_dict(self):
        return {
            "invoice_id": self.__invoice_id,
            "customer_name": self.__customer_name,
            "pet_name": self.__pet.name,
            "pet_breed": self.__pet.breed,
            "services": self.service_names,
            "total": self.__total,
            "created_at": self.__created_at
        }