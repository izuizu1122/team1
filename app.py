from flask import Flask, render_template, request, redirect
from datetime import datetime, date
import sqlite3
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_db_connection():
    db_path = os.path.join("database", "food_app.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():

    conn = get_db_connection()

    query = request.args.get("q", "").strip()
    active_filter = request.args.get("filter", "all")

    ingredients = conn.execute("""
        SELECT *
        FROM ingredients
        WHERE is_deleted = 0
        ORDER BY expiry_date
    """).fetchall()

    conn.close()

    today = date.today()
    ingredients_with_status = []

    for item in ingredients:

        row = dict(item)

        expiry = datetime.strptime(row["expiry_date"], "%Y-%m-%d").date()
        days_left = (expiry - today).days

        row["days_left"] = days_left

        if days_left < 0:
            row["expiry_status"] = "expired"
            row["progress"] = 0

        elif days_left <= 3:
            row["expiry_status"] = "warning"
            row["progress"] = 30

        else:
            row["expiry_status"] = "safe"
            row["progress"] = max(10, days_left * 10)
        if query and query.lower() not in row["name"].lower():
            continue

        ingredients_with_status.append(row)

    if active_filter == "expired":
        ingredients_with_status = [i for i in ingredients_with_status if i["expiry_status"] == "expired"]

    elif active_filter == "warning":
        ingredients_with_status = [i for i in ingredients_with_status if i["expiry_status"] == "warning"]

    elif active_filter != "all":
        ingredients_with_status = [i for i in ingredients_with_status if i["category"] == active_filter]

    priority = {"expired": 0, "warning": 1, "safe": 2}

    ingredients_with_status.sort(
        key=lambda x: (
            priority[x["expiry_status"]],
            x["days_left"]
        )
    )

    total_count = len(ingredients_with_status)

    warning_count = sum(1 for i in ingredients_with_status if i["expiry_status"] == "warning")
    expired_count = sum(1 for i in ingredients_with_status if i["expiry_status"] == "expired")

    return render_template(
        "index.html",
        ingredients=ingredients_with_status,
        query=query,
        active_filter=active_filter,
        total_count=total_count,
        warning_count=warning_count,
        expired_count=expired_count
    )


@app.route("/add", methods=["GET", "POST"])
def add_ingredient():

    if request.method == "POST":

        name = request.form["ingredientName"]
        purchase_date = request.form["purchaseDate"]
        expiry_date = request.form["expiryDate"]
        quantity = request.form["quantity"]
        unit = request.form["unit"]
        category = request.form["category"]
        memo = request.form["memo"]

        image = request.files.get("image")

        conn = get_db_connection()
        cursor = conn.cursor()

        upload_id = None

        if image and image.filename != "":

            image_name = image.filename

            image.save(os.path.join(app.config["UPLOAD_FOLDER"], image_name))

            cursor.execute("""
                INSERT INTO uploads (file_name, file_path)
                VALUES (?,?)
            """, (image_name, "static/uploads/" + image_name))

            upload_id = cursor.lastrowid

        conn.execute("""
            INSERT INTO ingredients
            (name, purchase_date, expiry_date, quantity, unit, category, memo, upload_id, is_deleted)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (
            name, purchase_date, expiry_date,
            quantity, unit, category, memo, upload_id
        ))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("edit.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_ingredient(id):

    conn = get_db_connection()

    ingredient = conn.execute("""
        SELECT ingredients.*, uploads.file_path
        FROM ingredients
        LEFT JOIN uploads
        ON ingredients.upload_id = uploads.id
        WHERE ingredients.id = ?
    """, (id,)).fetchone()

    if request.method == "POST":

        name = request.form["ingredientName"]
        purchase_date = request.form["purchaseDate"]
        expiry_date = request.form["expiryDate"]
        quantity = request.form["quantity"]
        unit = request.form["unit"]
        category = request.form["category"]
        memo = request.form["memo"]

        image = request.files.get("image")

        upload_id = ingredient["upload_id"]

        cursor = conn.cursor()

        if image and image.filename != "":

            image_name = image.filename
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], image_name))

            cursor.execute("""
                INSERT INTO uploads (file_name, file_path)
                VALUES (?,?)
            """, (image_name, "static/uploads/" + image_name))

            upload_id = cursor.lastrowid

        conn.execute("""
            UPDATE ingredients
            SET name=?, purchase_date=?, expiry_date=?, quantity=?,
                unit=?, category=?, memo=?, upload_id=?
            WHERE id=?
        """, (
            name, purchase_date, expiry_date, quantity,
            unit, category, memo, upload_id, id
        ))

        conn.commit()
        conn.close()

        return redirect("/")

    conn.close()
    return render_template("edit.html", ingredient=ingredient)


@app.route("/delete/<int:id>", methods=["POST"])
def delete_ingredient(id):

    conn = get_db_connection()

    conn.execute("""
        UPDATE ingredients
        SET is_deleted=1
        WHERE id=?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/test-db")
def test_db():

    conn = get_db_connection()

    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()

    conn.close()

    return str([row["name"] for row in tables])


if __name__ == "__main__":
    app.run(debug=True)
