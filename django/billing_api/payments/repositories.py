# payments/repositories.py
from bson import ObjectId
from datetime import datetime, timezone
from .mongo import get_mongo_db

def _now():
    return datetime.now(timezone.utc)

def ensure_indexes():
    db = get_mongo_db()
    db.payment_plans.create_index([("invoice_id", 1), ("created_at", -1)])
    db.payment_transactions.create_index([("plan_id", 1), ("paid_at", 1)])
    db.payment_transactions.create_index([("invoice_id", 1), ("paid_at", 1)])
    db.payment_transactions.create_index([("reference", 1)], unique=True, sparse=True)

def create_payment_plan(invoice_id: int, customer_id: int, total: float, installments: int, currency: str = "USD"):
    db = get_mongo_db()
    doc = {
        "invoice_id": int(invoice_id),
        "customer_id": int(customer_id),
        "status": "ACTIVE",
        "currency": currency,
        "total": float(total),
        "installments": int(installments),
        "created_at": _now(),
    }
    res = db.payment_plans.insert_one(doc)
    doc["_id"] = res.inserted_id
    return doc

def add_payment_transaction(plan_id: str, invoice_id: int, amount: float, method: str, reference: str = "", meta: dict | None = None):
    db = get_mongo_db()
    pid = ObjectId(plan_id)
    doc = {
        "plan_id": pid,
        "invoice_id": int(invoice_id),
        "type": "PAYMENT",
        "amount": float(amount),
        "method": method,
        "reference": reference or None,
        "paid_at": _now(),
        "meta": meta or {},
    }
    res = db.payment_transactions.insert_one(doc)
    doc["_id"] = res.inserted_id
    return doc

def get_plan_with_transactions(invoice_id: int):
    db = get_mongo_db()
    plan = db.payment_plans.find_one({"invoice_id": int(invoice_id)}, sort=[("created_at", -1)])
    if not plan:
        return None
    txs = list(db.payment_transactions.find({"plan_id": plan["_id"]}).sort("paid_at", 1))

    def normalize(d):
        d = dict(d)
        if "_id" in d:
            d["_id"] = str(d["_id"])
        if "plan_id" in d:
            d["plan_id"] = str(d["plan_id"])
        for k in ("created_at", "paid_at"):
            if k in d and d[k]:
                d[k] = d[k].isoformat()
        return d

    return {
        "plan": normalize(plan),
        "transactions": [normalize(t) for t in txs],
    }