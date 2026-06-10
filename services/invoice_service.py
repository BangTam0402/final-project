import json
import csv
from collections import Counter
from models.invoice import Invoice


class InvoiceService:
    def __init__(self):
        self.__invoices = []

    @property
    def invoices(self):
        return self.__invoices

    def create_invoice(self, customer_name, pet, care_services):
        invoice_id = f"I{len(self.__invoices) + 1:03d}"
        invoice = Invoice(invoice_id, customer_name, pet, care_services)
        self.__invoices.append(invoice)
        return invoice

    def display_invoices(self):
        if not self.__invoices:
            print("No invoices available.")
            return

        for invoice in self.__invoices:
            print("-" * 40)
            print(invoice.get_info())

    def total_revenue(self):
        return sum(invoice.total for invoice in self.__invoices)

    def most_used_service(self):
        if not self.__invoices:
            return "No data"

        service_names = []
        for invoice in self.__invoices:
            service_names.extend(invoice.service_names)

        counter = Counter(service_names)
        return counter.most_common(1)[0][0]

    def save_to_file(self, filename="data/invoices.json"):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump([invoice.to_dict() for invoice in self.__invoices], file, indent=4, ensure_ascii=False)

    def export_csv(self, filename="data/report.csv"):
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Invoice ID", "Customer", "Pet", "Breed", "Services", "Total", "Date"])

            for invoice in self.__invoices:
                data = invoice.to_dict()
                writer.writerow([
                    data["invoice_id"],
                    data["customer_name"],
                    data["pet_name"],
                    data["pet_breed"],
                    ", ".join(data["services"]),
                    data["total"],
                    data["created_at"]
                ])