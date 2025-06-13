from database import get_db, init_db
import uuid
from datetime import datetime

# Initialize DB and table
init_db()

# Seed data
seed_payments = [
    {
        "payment_id": str(uuid.uuid4()),
        "order_id": "ORD001",
        "user_id": "USR001",
        "amount": 150000.0,
        "payment_method": "credit_card",
        "status": "SUCCESS",
        "paid_at": datetime.utcnow().strftime("%H:%M:%S $d-%m-%Y"),
        "created_at": datetime.utcnow().strftime("%H:%M:%S $d-%m-%Y"),
        "updated_at": datetime.utcnow().strftime("%H:%M:%S $d-%m-%Y")
    },
    {
        "payment_id": str(uuid.uuid4()),
        "order_id": "ORD002",
        "user_id": "USR002",
        "amount": 250000.0,
        "payment_method": "bank_transfer",
        "status": "PENDING",
        "paid_at": None,
        "created_at": datetime.utcnow().strftime("%H:%M:%S $d-%m-%Y"),
        "updated_at": datetime.utcnow().strftime("%H:%M:%S $d-%m-%Y")
    },
    {
        "payment_id": str(uuid.uuid4()),
        "order_id": "ORD003",
        "user_id": "USR003",
        "amount": 100000.0,
        "payment_method": "credit_card",
        "status": "FAILED",
        "paid_at": None,
        "created_at": datetime.utcnow().strftime("%H:%M:%S $d-%m-%Y"),
        "updated_at": datetime.utcnow().strftime("%H:%M:%S $d-%m-%Y")
    }
]

conn = get_db()
cur = conn.cursor()

for payment in seed_payments:
    cur.execute("""
        INSERT INTO payments (payment_id, order_id, user_id, amount, payment_method, status, paid_at, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        payment["payment_id"],
        payment["order_id"],
        payment["user_id"],
        payment["amount"],
        payment["payment_method"],
        payment["status"],
        payment["paid_at"],
        payment["created_at"],
        payment["updated_at"]
    ))

conn.commit()
conn.close()

print("Database seeded with sample payments.")