from models.pet import Dog, Cat, Bird
from models.service import BathingService
from models.invoice import Invoice
from services.pet_service import PetService


pet_service = PetService()

pet_service.add_pet(Dog("D01", "Lucky", "Poodle", 5, 3000000))
pet_service.add_pet(Cat("C01", "Mimi", "British Shorthair", 3, 2500000))
pet_service.add_pet(Bird("B01", "Rio", "Parrot", 1, 800000))

print("=== PET LIST ===")
pet_service.show_pets()

print("\n=== SEARCH PET ===")
pet = pet_service.search_pet_by_name("Lucky")
if pet:
    print("Found:", pet.get_info())
else:
    print("Pet not found.")

print("\n=== SORT BY PRICE ===")
pet_service.sort_by_price()
pet_service.show_pets()

print("\n=== SPA INVOICE ===")
service = BathingService()
pet = pet_service.search_pet_by_id("D01")
total = service.calculate_price(pet)

invoice = Invoice("I01", "Nguyen Van A", pet, service, total)
print(invoice.get_info())