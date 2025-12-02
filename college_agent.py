
import sqlite3
import csv
import os

DB_PATH = "career.db"
CSV_PATH = "database.csv"  # your file name

def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create table exactly matching your CSV
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS colleges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        university_name TEXT,
        college_name TEXT,
        college_type TEXT,
        state_name TEXT,
        district_name TEXT
    )
    """)
    conn.commit()

    # # 2. Check if already imported
    # cursor.execute("SELECT COUNT(*) FROM colleges")
    # if cursor.fetchone()[0] > 0:
    #     print("✔ Colleges already imported.")
    #     conn.close()
    #     return

    # 3. Import CSV
    # if not os.path.exists(CSV_PATH):
    #     print(f"❌ CSV not found: {CSV_PATH}")
    #     conn.close()
    #     return

    with open(CSV_PATH, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # skip header

        for row in reader:
            # row = [S. No, University Name, College Name, College Type, State Name, District Name]
            cursor.execute("""
            INSERT INTO colleges (university_name, college_name, college_type, state_name, district_name)
            VALUES (?, ?, ?, ?, ?)
            """, (row[1], row[2], row[3], row[4], row[5]))

    conn.commit()
    conn.close()
    

def find_colleges(query):
    init_database()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT university_name, college_name, college_type, state_name, district_name
        FROM colleges
        WHERE 
            college_name LIKE ? OR
            university_name LIKE ? OR
            district_name LIKE ? OR
            state_name LIKE ?
    """, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))

    rows = cursor.fetchall()
    conn.close()
    return rows
