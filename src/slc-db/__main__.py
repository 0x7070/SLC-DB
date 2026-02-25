import sqlite3
from datetime import datetime

DB_NAME = "slc_test_db.db"


# -------------------------
# DATABASE SCHEMA
# -------------------------

INITIAL_DB = """
CREATE TABLE IF NOT EXISTS films (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    barcode TEXT UNIQUE,
    name TEXT,
    brand TEXT,
    film_type TEXT,
    weight REAL,
    date_received TEXT,
    notes TEXT
)
"""


# -------------------------
# DATABASE INIT
# -------------------------

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(INITIAL_DB)

    conn.commit()
    conn.close()


# -------------------------
# ADD FILM
# -------------------------

def add_film():

    print("\n-- Add Film Roll --")

    barcode = input("Scan or enter barcode: ")
    name = input("Film name: ")
    brand = input("Brand: ")
    film_type = input("Film type (security, decorative, etc): ")

    try:
        weight = float(input("Weight (lbs): "))
    except ValueError:
        print("Invalid weight.")
        return

    notes = input("Notes: ")

    date_received = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    insert_cmd = """
    INSERT INTO films (
        barcode,
        name,
        brand,
        film_type,
        weight,
        date_received,
        notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    try:

        cur.execute(
            insert_cmd,
            (barcode, name, brand, film_type, weight, date_received, notes)
        )

        conn.commit()

        print("\nFilm saved.\n")

    except sqlite3.IntegrityError:
        print("\nERROR: Barcode already exists.\n")

    conn.close()


# -------------------------
# SCAN FILM
# -------------------------

def scan_film():

    print("\nScan film barcode:")
    barcode = input("> ")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "SELECT barcode, name, brand, film_type, weight, date_received, notes FROM films WHERE barcode = ?",
        (barcode,)
    )

    film = cur.fetchone()

    conn.close()

    if film:

        print("\n--- Film Info ---")

        print(f"Barcode: {film[0]}")
        print(f"Name: {film[1]}")
        print(f"Brand: {film[2]}")
        print(f"Type: {film[3]}")
        print(f"Weight: {film[4]} lbs")
        print(f"Received: {film[5]}")
        print(f"Notes: {film[6]}")

        print()

    else:
        print("Film not found.\n")


# -------------------------
# SEARCH FILMS
# -------------------------

def search_films():

    term = input("\nSearch term: ")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT barcode, name, brand, film_type, weight
        FROM films
        WHERE name LIKE ?
        OR brand LIKE ?
        OR film_type LIKE ?
        OR notes LIKE ?
        """,
        (f"%{term}%", f"%{term}%", f"%{term}%", f"%{term}%")
    )

    results = cur.fetchall()

    conn.close()

    if not results:
        print("\nNo results found.\n")
        return

    print("\nResults:\n")

    for r in results:

        barcode, name, brand, film_type, weight = r

        print(
            f"{barcode} | {name} | {brand} | {film_type} | {weight} lbs"
        )

    print()


# -------------------------
# LIST ALL FILMS
# -------------------------

def list_films():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "SELECT barcode, name, brand, film_type, weight FROM films"
    )

    results = cur.fetchall()

    conn.close()

    if not results:
        print("\nInventory empty.\n")
        return

    print("\n--- Inventory ---\n")

    for r in results:
        print(
            f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} lbs"
        )

    print()


# -------------------------
# MAIN CLI LOOP
# -------------------------

def main():

    init_db()

    while True:

        print("Inventory Management")
        print("1) Add Film")
        print("2) Scan Film")
        print("3) Search")
        print("4) List All")
        print("0) Exit")

        choice = input("> ")

        if choice == "1":
            add_film()

        elif choice == "2":
            scan_film()

        elif choice == "3":
            search_films()

        elif choice == "4":
            list_films()

        elif choice == "0":
            print("Exiting...")
            break

        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main()