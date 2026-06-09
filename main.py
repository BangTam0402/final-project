from models.pet import Dog, Cat, Bird
from models.service import BathingService, TrimmingService, BoardingService
from models.invoice import Invoice


pets = [
    Dog("D01", "Lucky", "Poodle", 5, 3000000),
    Cat("C01", "Mimi", "British Shorthair", 3, 2500000),
    Bird("B01", "Rio", "Parrot", 1, 800000)
]

print("=== PET LIST ===")
for pet in pets:
    print(pet.get_info())

print("\n=== SPA SERVICE TEST ===")
service = BathingService()
pet = pets[0]
total = service.calculate_price(pet)

invoice = Invoice("I01", "Nguyen Van A", pet, service, total)
print(invoice.get_info())