from datetime import datetime


class Invoice:
    def __init__(self, invoice_id, customer_name, pet, service, total):
        self.__invoice_id = invoice_id
        self.__customer_name = customer_name
        self.__pet = pet
        self.__service = service
        self.__total = total
        self.__created_at = datetime.now().strftime("%d/%m/%Y %H:%M")

    @property
    def total(self):
        return self.__total

    def get_info(self):
        return (
            f"Invoice: {self.__invoice_id}\n"
            f"Customer: {self.__customer_name}\n"
            f"Pet: {self.__pet.name}\n"
            f"Service: {self.__service.name}\n"
            f"Total: {self.__total} VND\n"
            f"Date: {self.__created_at}"
        )