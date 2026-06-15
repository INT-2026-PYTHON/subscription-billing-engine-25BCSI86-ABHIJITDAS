"""
Repositories — the ONLY place SQL lives.

Each repository wraps the Database connection and exposes methods that
take/return domain dataclasses (defined in billing_engine/models/).

⚠️ YOU IMPLEMENT every method body marked TODO.
   The signatures, docstrings, and the LedgerRepository's append-only
   guarantee are already in place — do not change them.

Conventions:
  - Always use parameterized queries (`?` placeholders) — NEVER f-string SQL.
  - Money values are persisted as TEXT using `money.to_storage()`.
  - Dates are persisted as ISO strings (`date.isoformat()`).
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from billing_engine.db.database import Database
from billing_engine.money import Money
from billing_engine.models import (
    Customer,
    Plan, PricingType, BillingPeriod,
    Subscription, SubscriptionStatus,
    Invoice, InvoiceStatus, InvoiceLineItem, LineItemKind,
    LedgerEntry, LedgerDirection,
)


# ============================================================
# CUSTOMERS
# ============================================================
class CustomerRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def add(self, customer: Customer) -> Customer:
        with self.db.connect() as conn:
            cur = conn.execute(
                """
                INSERT INTO customers
                (name, email, country_code, state_code)
                VALUES (?, ?, ?, ?)
                """,
                (
                    customer.name,
                    customer.email,
                    customer.country_code,
                    customer.state_code,
                ),
            )
            conn.commit()

            return Customer(
                id=cur.lastrowid,
                name=customer.name,
                email=customer.email,
                country_code=customer.country_code,
                state_code=customer.state_code,
            )

    def get(self, customer_id: int) -> Optional[Customer]:
        with self.db.connect() as conn:
            row = conn.execute(
                "SELECT * FROM customers WHERE id = ?",
                (customer_id,),
            ).fetchone()

            if row is None:
                return None

            return Customer(
                id=row["id"],
                name=row["name"],
                email=row["email"],
                country_code=row["country_code"],
                state_code=row["state_code"],
                created_at=datetime.fromisoformat(row["created_at"]),
            )

    def find_by_email(self, email: str) -> Optional[Customer]:
        with self.db.connect() as conn:
            row = conn.execute(
                "SELECT * FROM customers WHERE email = ?",
                (email,),
            ).fetchone()

            if row is None:
                return None

            return Customer(
                id=row["id"],
                name=row["name"],
                email=row["email"],
                country_code=row["country_code"],
                state_code=row["state_code"],
                created_at=datetime.fromisoformat(row["created_at"]),
            )

    def list_all(self) -> list[Customer]:
        with self.db.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM customers ORDER BY id"
            ).fetchall()

            return [
                Customer(
                    id=row["id"],
                    name=row["name"],
                    email=row["email"],
                    country_code=row["country_code"],
                    state_code=row["state_code"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                )
                for row in rows
            ]