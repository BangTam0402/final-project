import sqlite3


class DatabaseService:
    def __init__(self, db_name="data/pet_store.db"):
        self.db_name = db_name
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                pet_id TEXT PRIMARY KEY,
                type TEXT,
                name TEXT,
                breed TEXT,
                weight REAL,
                price REAL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                invoice_id TEXT PRIMARY KEY,
                customer_name TEXT,
                pet_name TEXT,
                pet_breed TEXT,
                services TEXT,
                total REAL,
                created_at TEXT
            )
        """)

        conn.commit()
        conn.close()

    def save_pets(self, pets):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM pets")

        for pet in pets:
            cursor.execute("""
                INSERT INTO pets VALUES (?, ?, ?, ?, ?, ?)
            """, (
                pet.pet_id,
                pet.__class__.__name__,
                pet.name,
                pet.breed,
                pet.weight,
                pet.price
            ))

        conn.commit()
        conn.close()

    def save_invoices(self, invoices):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM invoices")

        for invoice in invoices:
            data = invoice.to_dict()
            cursor.execute("""
                INSERT INTO invoices VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data["invoice_id"],
                data["customer_name"],
                data["pet_name"],
                data["pet_breed"],
                ", ".join(data["services"]),
                data["total"],
                data["created_at"]
            ))

        conn.commit()
        conn.close()