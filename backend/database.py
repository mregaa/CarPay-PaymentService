import sqlite3

def get_db():
    conn = sqlite3.connect("carpay.db")
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        payment_id TEXT PRIMARY KEY,
        order_id TEXT NOT NULL,
        user_id TEXT NOT NULL,
        amount REAL NOT NULL,
        payment_method TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'PENDING',
        paid_at TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    print("Database initialized successfully.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()