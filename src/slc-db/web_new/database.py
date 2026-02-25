import sqlite3
from datetime import datetime
import os

DB_NAME = "slc_test_db.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, DB_NAME)

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

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(INITIAL_DB)
    conn.commit()
    conn.close()


def get_all_films():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    films = conn.execute("SELECT * FROM films").fetchall()
    conn.close()
    return films


def get_film_by_barcode(barcode):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    film = conn.execute("SELECT * FROM films WHERE barcode = ?", (barcode,)).fetchone()
    conn.close()
    return film


def insert_film(barcode, name, brand, film_type, weight, notes):
    date_received = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            """
            INSERT INTO films
            (barcode, name, brand, film_type, weight, date_received, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (barcode, name, brand, film_type, weight, date_received, notes)
        )
        conn.commit()
        return True, None
    except sqlite3.IntegrityError:
        duplicate = get_film_by_barcode(barcode)
        return False, dict(duplicate) if duplicate else None
    finally:
        conn.close()