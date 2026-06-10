from services.pet_service import PetService
from services.invoice_service import InvoiceService
from views.menu import Menu


def main():
    pet_service = PetService()
    invoice_service = InvoiceService()
    menu = Menu(pet_service, invoice_service)
    menu.run()


if __name__ == "__main__":
    main()