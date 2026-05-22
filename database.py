import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

CATEGORIES = [
    ("🏠", "Rent"),
    ("🛒", "Groceries"),
    ("🚌", "Transport"),
    ("🍔", "Food & Dining"),
    ("🎉", "Party"),
    ("📚", "Text Books & Supplies"),
    ("💊", "Health"),
    ("📱", "Subscriptions"),
    ("👗", "Shopping"),
    ("☕", "Cafe & Drinks"),
    ("🎮", "Entertainment"),
    ("✈️", "Travel"),
    ("💡", "Utilities"),
    ("🎁", "Gifts"),
    ("🔧", "Miscellaneous"),
]

CATEGORY_COLORS = {
    "Rent":            "#FF6B6B",
    "Groceries":       "#4ECDC4",
    "Transport":       "#45B7D1",
    "Food & Dining":   "#FFA07A",
    "Party":           "#DA70D6",
    "Text Books & Supplies":   "#98D8C8",
    "Health":          "#90EE90",
    "Subscriptions":   "#DDA0DD",
    "Shopping":        "#F0E68C",
    "Cafe & Drinks":   "#D2691E",
    "Entertainment":   "#9370DB",
    "Travel":          "#20B2AA",
    "Utilities":       "#708090",
    "Gifts":           "#FF69B4",
    "Miscellaneous":   "#A9A9A9",
}


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            amount    REAL    NOT NULL,
            category  TEXT    NOT NULL,
            description      TEXT,
            date      TEXT    NOT NULL,
            created   TEXT    NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            category      TEXT PRIMARY KEY,
            monthly_limit REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_expense(amount: float, category: str, note: str, date: str):
    conn = get_connection()
    conn.execute(
        "INSERT INTO expenses (amount, category, note, date) VALUES (?, ?, ?, ?)",
        (amount, category, note or "", date),
    )
    conn.commit()
    conn.close()


def delete_expense(expense_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()


def get_all_expenses(month: str | None = None):
    conn = get_connection()
    if month:
        rows = conn.execute(
            "SELECT * FROM expenses WHERE strftime('%Y-%m', date) = ? ORDER BY date DESC",
            (month,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM expenses ORDER BY date DESC"
        ).fetchall()
    conn.close()
    return rows


def get_recent_expenses(limit: int = 8):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM expenses ORDER BY date DESC, created DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return rows


def get_monthly_total(month: str) -> float:
    conn = get_connection()
    result = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE strftime('%Y-%m', date) = ?",
        (month,),
    ).fetchone()[0]
    conn.close()
    return result


def get_category_totals(month: str) -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        """SELECT category, SUM(amount) as total
           FROM expenses
           WHERE strftime('%Y-%m', date) = ?
           GROUP BY category
           ORDER BY total DESC""",
        (month,),
    ).fetchall()
    conn.close()
    return [{"category": r["category"], "total": r["total"]} for r in rows]


def get_monthly_trend(months: int = 6) -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        """SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
           FROM expenses
           GROUP BY month
           ORDER BY month DESC
           LIMIT ?""",
        (months,),
    ).fetchall()
    conn.close()
    return [{"month": r["month"], "total": r["total"]} for r in reversed(rows)]


def get_available_months() -> list[str]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT DISTINCT strftime('%Y-%m', date) as month FROM expenses ORDER BY month DESC"
    ).fetchall()
    conn.close()
    return [r["month"] for r in rows]


def set_budget(category: str, limit: float):
    conn = get_connection()
    conn.execute(
        "INSERT OR REPLACE INTO budgets (category, monthly_limit) VALUES (?, ?)",
        (category, limit),
    )
    conn.commit()
    conn.close()


def get_budgets() -> dict:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM budgets").fetchall()
    conn.close()
    return {r["category"]: r["monthly_limit"] for r in rows}