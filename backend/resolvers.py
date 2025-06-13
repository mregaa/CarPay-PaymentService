import sqlite3
from datetime import datetime
import uuid
from ariadne import QueryType, gql


ORDER_SERVICE_URL = "https://orderservice-cloud.fly.dev/graphql"  # ganti dengan URL asli

def get_db():
    conn = sqlite3.connect("carpay.db")
    conn.row_factory = sqlite3.Row
    return conn

def resolve_get_payment_by_id(_, info, paymentId):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM payments WHERE payment_id = ?", (paymentId,))
    rows = cur.fetchall()
    result = []
    for row in rows:
        # mapping manual untuk memastikan nama key sesuai schema
        result.append({
            "paymentId": row["payment_id"],
            "orderId": row["order_id"],
            "userId": row["user_id"],
            "amount": row["amount"],
            "paymentMethod": row["payment_method"],
            "status": row["status"],
            "createdAt": row["created_at"],
            "paidAt": row["paid_at"]
        })
    return result

def resolve_get_payment_status(_, info, orderId):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT status FROM payments WHERE order_id = ?", (orderId,))
    row = cur.fetchone()
    return row["status"] if row else "not_found"

def resolve_create_payment(_, info, orderId, userId, amount, method):
    payment_id = str(uuid.uuid4())
    paid_at = datetime.utcnow().isoformat()
    status = "success"  # bisa logic dynamic kalau perlu

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO payments (payment_id, order_id, user_id, amount, payment_method, status, paid_at, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (payment_id, orderId, userId, amount, method, status, paid_at, paid_at, paid_at))
    conn.commit()

    return {
        "paymentId": payment_id,
        "orderId": orderId,
        "userId": userId,
        "amount": amount,
        "paymentMethod": method,
        "status": status,
        "paidAt": paid_at
    }

def resolve_get_payments_by_user(_, info, userId):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM payments WHERE user_id = ?", (userId,))
    rows = cur.fetchall()
    result = []
    for row in rows:
        # mapping manual untuk memastikan nama key sesuai schema
        result.append({
            "paymentId": row["payment_id"],
            "orderId": row["order_id"],
            "userId": row["user_id"],
            "amount": row["amount"],
            "paymentMethod": row["payment_method"],
            "status": row["status"],
            "createdAt": row["created_at"],
            "paidAt": row["paid_at"]
        })
    return result

def resolve_update_payment_status(_, info, paymentId, status):
    conn = get_db()
    cur = conn.cursor()

    updated_at = datetime.utcnow().isoformat()
    cur.execute("""
        UPDATE payments SET status = ?, updated_at = ? WHERE payment_id = ?
    """, (status, updated_at, paymentId))
    conn.commit()

    cur.execute("SELECT * FROM payments WHERE payment_id = ?", (paymentId,))
    rows = cur.fetchall()
    result = []
    for row in rows:
        # mapping manual untuk memastikan nama key sesuai schema
        result.append({
            "paymentId": row["payment_id"],
            "orderId": row["order_id"],
            "userId": row["user_id"],
            "amount": row["amount"],
            "paymentMethod": row["payment_method"],
            "status": row["status"],
            "createdAt": row["created_at"],
            "paidAt": row["paid_at"]
        })
    return result

def resolve_delete_payment(_, info, paymentId):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM payments WHERE payment_id = ?", (paymentId,))
    row = cur.fetchone()
    if not row:
        return {"success": False, "message": "Payment not found."}

    cur.execute("DELETE FROM payments WHERE payment_id = ?", (paymentId,))
    conn.commit()

    return {"success": True, "message": "Payment deleted successfully."}

def get_all_payments(_, info):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM payments")
    rows = cur.fetchall()
    result = []
    for row in rows:
        # mapping manual untuk memastikan nama key sesuai schema
        result.append({
            "paymentId": row["payment_id"],
            "orderId": row["order_id"],
            "userId": row["user_id"],
            "amount": row["amount"],
            "paymentMethod": row["payment_method"],
            "status": row["status"],
            "createdAt": row["created_at"],
            "paidAt": row["paid_at"]
        })
    return result

