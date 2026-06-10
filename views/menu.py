from models.pet import Dog, Cat, Bird
from models.service import BathingService, TrimmingService, BoardingService
from services.database_service import DatabaseService


class Menu:
    def __init__(self, pet_service, invoice_service):
        self.pet_service = pet_service
        self.invoice_service = invoice_service
        self.database_service = DatabaseService()

    def run(self):
        self.pet_service.load_from_file()

        while True:
            print("\n===== PET STORE & SPA MANAGEMENT =====")
            print("1. Add pet")
            print("2. Display pets")
            print("3. Update pet")
            print("4. Delete pet")
            print("5. Search pet")
            print("6. Sort pets")
            print("7. Create spa invoice")
            print("8. Display invoices")
            print("9. Statistics")
            print("10. Export report CSV")
            print("0. Exit")

            choice = input("Choose: ")

            try:
                if choice == "1":
                    self.add_pet_menu()
                elif choice == "2":
                    self.pet_service.display_pets()
                elif choice == "3":
                    self.update_pet_menu()
                elif choice == "4":
                    pet_id = input("Enter pet ID: ")
                    print("Deleted." if self.pet_service.delete_pet(pet_id) else "Pet not found.")
                elif choice == "5":
                    self.search_pet_menu()
                elif choice == "6":
                    self.sort_pet_menu()
                elif choice == "7":
                    self.create_invoice_menu()
                elif choice == "8":
                    self.invoice_service.display_invoices()
                elif choice == "9":
                    self.statistics_menu()
                elif choice == "10":
                    self.invoice_service.export_csv()
                    print("Exported to data/report.csv")
                elif choice == "0":
                    self.pet_service.save_to_file()
                    self.invoice_service.save_to_file()
                    self.database_service.save_pets(self.pet_service.pets)
                    self.database_service.save_invoices(self.invoice_service.invoices)
                    print("Data saved to JSON and SQLite. Goodbye!")
                    break
                else:
                    print("Invalid choice.")
            except Exception as e:
                print("Error:", e)

    def add_pet_menu(self):
        pet_type = input("Type Dog/Cat/Bird: ")
        pet_id = input("Pet ID: ")
        name = input("Name: ")
        breed = input("Breed: ")
        weight = float(input("Weight: "))
        price = float(input("Price: "))

        if pet_type.lower() == "dog":
            pet = Dog(pet_id, name, breed, weight, price)
        elif pet_type.lower() == "cat":
            pet = Cat(pet_id, name, breed, weight, price)
        elif pet_type.lower() == "bird":
            pet = Bird(pet_id, name, breed, weight, price)
        else:
            print("Invalid pet type.")
            return

        self.pet_service.add_pet(pet)
        print("Pet added successfully.")

    def update_pet_menu(self):
        pet_id = input("Pet ID to update: ")
        name = input("New name, leave blank to skip: ")
        breed = input("New breed, leave blank to skip: ")
        weight = input("New weight, leave blank to skip: ")
        price = input("New price, leave blank to skip: ")

        result = self.pet_service.update_pet(
            pet_id,
            name if name else None,
            breed if breed else None,
            float(weight) if weight else None,
            float(price) if price else None
        )

        print("Updated." if result else "Pet not found.")

    def search_pet_menu(self):
        keyword = input("Enter ID or name: ")
        pet = self.pet_service.search_pet_by_id(keyword)

        if pet:
            print(pet.get_info())
        else:
            results = self.pet_service.search_pet_by_name(keyword)
            if results:
                for item in results:
                    print(item.get_info())
            else:
                print("Pet not found.")

    def sort_pet_menu(self):
        print("1. Sort by price")
        print("2. Sort by weight")
        choice = input("Choose: ")

        if choice == "1":
            self.pet_service.sort_by_price()
        elif choice == "2":
            self.pet_service.sort_by_weight()
        else:
            print("Invalid choice.")
            return

        self.pet_service.display_pets()

    def create_invoice_menu(self):
        customer_name = input("Customer name: ")
        pet_id = input("Pet ID: ")
        pet = self.pet_service.search_pet_by_id(pet_id)

        if not pet:
            print("Pet not found.")
            return

        care_services = []

        while True:
            print("\nChoose service:")
            print("1. Bathing")
            print("2. Trimming")
            print("3. Boarding")
            print("0. Finish selecting services")

            choice = input("Choose: ")

            if choice == "1":
                care_services.append(BathingService())
                print("Added Bathing.")
            elif choice == "2":
                care_services.append(TrimmingService())
                print("Added Trimming.")
            elif choice == "3":
                days = int(input("Number of boarding days: "))
                care_services.append(BoardingService(days))
                print("Added Boarding.")
            elif choice == "0":
                break
            else:
                print("Invalid service.")

        if not care_services:
            print("No service selected. Invoice cancelled.")
            return

        invoice = self.invoice_service.create_invoice(customer_name, pet, care_services)
        print("Invoice created:")
        print(invoice.get_info())

    def statistics_menu(self):
        print("Total invoices:", len(self.invoice_service.invoices))
        print(f"Total revenue: {self.invoice_service.total_revenue():,.0f} VND")
        print("Most used service:", self.invoice_service.most_used_service())

        print("\nRevenue by service:")
        revenue_data = self.invoice_service.revenue_by_service()

        if not revenue_data:
            print("No data")
        else:
            for service, revenue in revenue_data.items():
                print(f"{service}: {revenue:,.0f} VND")

        dog_count = sum(1 for pet in self.pet_service.pets if pet.__class__.__name__ == "Dog")
        cat_count = sum(1 for pet in self.pet_service.pets if pet.__class__.__name__ == "Cat")
        bird_count = sum(1 for pet in self.pet_service.pets if pet.__class__.__name__ == "Bird")

        print("\nPets by type:")
        print("Dogs:", dog_count)
        print("Cats:", cat_count)
        print("Birds:", bird_count)