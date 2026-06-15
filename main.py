from services.pet_service import PetService
from services.product_service import ProductService
from services.invoice_service import InvoiceService
from views.menu import Menu


def main():
    pet_service = PetService()
    product_service = ProductService()
    invoice_service = InvoiceService()
    
    # Khởi tạo Menu với cả 3 Services
    menu = Menu(pet_service, product_service, invoice_service)
    menu.run()


if __name__ == "__main__":
    main()