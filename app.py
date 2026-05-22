from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import database as db

app = Flask(__name__)
app.secret_key = "student-expense-tracker-secret-2024"

db.init_db()


def current_month():
    return datetime.now().strftime("%Y-%m")


def month_label(ym: str) -> str:
    """'2024-03' → 'March 2024'"""
    try:
        return datetime.strptime(ym, "%Y-%m").strftime("%B %Y")
    except Exception:
        return ym


@app.context_processor
def inject_globals():
    return {
        "categories": db.CATEGORIES,
        "category_colors": db.CATEGORY_COLORS,
        "now": datetime.now(),
    }


@app.route("/")
def index():
    month = request.args.get("month", current_month())
    available_months = db.get_available_months()

    total = db.get_monthly_total(month)
    cat_totals = db.get_category_totals(month)
    recent = db.get_recent_expenses(8)
    trend = db.get_monthly_trend(6)
    budgets = db.get_budgets()

    alerts = []
    for ct in cat_totals:
        limit = budgets.get(ct["category"])
        if limit and ct["total"] > limit * 0.8:
            pct = int(ct["total"] / limit * 100)
            alerts.append({
                "category": ct["category"],
                "spent": ct["total"],
                "limit": limit,
                "pct": pct,
                "over": ct["total"] > limit,
            })

    return render_template(
        "index.html",
        month=month,
        month_label=month_label(month),
        available_months=available_months,
        total=total,
        cat_totals=cat_totals,
        recent=recent,
        trend=trend,
        budgets=budgets,
        alerts=alerts,
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            flash("Please enter a valid amount.", "error")
            return redirect(url_for("add"))

        category = request.form.get("category", "Miscellaneous")
        note = request.form.get("note", "").strip()
        date = request.form.get("date") or datetime.now().strftime("%Y-%m-%d")

        db.add_expense(amount, category, note, date)
        flash(f"✅ ${amount:.2f} added to {category}!", "success")
        return redirect(url_for("index"))

    return render_template("add.html", today=datetime.now().strftime("%Y-%m-%d"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    db.delete_expense(expense_id)
    flash("🗑️ Expense deleted.", "info")
    return redirect(request.referrer or url_for("index"))


@app.route("/history")
def history():
    month = request.args.get("month", "")
    available_months = db.get_available_months()
    expenses = db.get_all_expenses(month if month else None)
    total = sum(e["amount"] for e in expenses)
    return render_template(
        "history.html",
        expenses=expenses,
        available_months=available_months,
        selected_month=month,
        month_label=month_label(month) if month else "All Time",
        total=total,
    )


@app.route("/budgets", methods=["GET", "POST"])
def budgets():
    if request.method == "POST":
        for cat_icon, cat_name in db.CATEGORIES:
            val = request.form.get(f"budget_{cat_name}", "").strip()
            if val:
                try:
                    db.set_budget(cat_name, float(val))
                except ValueError:
                    pass
        flash("✅ Budgets saved!", "success")
        return redirect(url_for("budgets"))

    month = current_month()
    cat_totals = {ct["category"]: ct["total"] for ct in db.get_category_totals(month)}
    budgets_data = db.get_budgets()
    return render_template(
        "budgets.html",
        budgets=budgets_data,
        cat_totals=cat_totals,
        month_label=month_label(month),
    )


@app.route("/api/trend")
def api_trend():
    return jsonify(db.get_monthly_trend(6))


if __name__ == "__main__":
    app.run(debug=True, port=5000)