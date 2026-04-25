from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# データベースに接続する関数（後で使います）
def get_db_connection():
    db_path = os.path.join('database', 'food_app.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()

    ingredients = conn.execute("""
        SELECT * 
        FROM ingredients 
        WHERE is_deleted = 0 
        ORDER BY expiry_date
    """).fetchall()

    conn.close()

    return render_template(
        'index.html',
        ingredients=ingredients
    )

# 食材追加（Create：「新規追加」ボタンを本当に動かす
@app.route('/add', methods=['GET', 'POST'])
def add_ingredient():

    if request.method == 'POST':

        name = request.form['ingredientName']
        purchase_date = request.form['purchaseDate']
        expiry_date = request.form['expiryDate']
        quantity = request.form['quantity']
        unit = request.form['unit']
        category = request.form['category']
        memo = request.form['memo']

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO ingredients
            (name, purchase_date, expiry_date,
             quantity, unit, category, memo, is_deleted)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0)
        """, (
            name,
            purchase_date,
            expiry_date,
            quantity,
            unit,
            category,
            memo
        ))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('edit.html')

#編集ボタンを本当に動かす
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_ingredient(id):

    conn = get_db_connection()

    if request.method == 'POST':

        conn.execute("""
            UPDATE ingredients
            SET
                name=?,
                purchase_date=?,
                expiry_date=?,
                quantity=?,
                unit=?,
                category=?,
                memo=?
            WHERE id=?
        """,(
            request.form['ingredientName'],
            request.form['purchaseDate'],
            request.form['expiryDate'],
            request.form['quantity'],
            request.form['unit'],
            request.form['category'],
            request.form['memo'],
            id
        ))

        conn.commit()
        conn.close()

        return redirect('/')


    ingredient = conn.execute(
        "SELECT * FROM ingredients WHERE id=? AND is_deleted=0",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        'edit.html',
        ingredient=ingredient
    )

#削除ルート
@app.route('/delete/<int:id>', methods=['POST'])
def delete_ingredient(id):

    conn = get_db_connection()

    conn.execute("""
        UPDATE ingredients
        SET is_deleted = 1
        WHERE id = ?
    """,(id,))

    conn.commit()
    conn.close()

    return redirect('/')

# DB接続テスト
@app.route('/test-db')
def test_db():
    conn = get_db_connection()

    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()

    conn.close()

    return str([row["name"] for row in tables])

if __name__ == '__main__':
    app.run(debug=True)