from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
# --- 追加：画像の保存場所をアプリに教える ---
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# データベースに接続する関数（後で使います）
def get_db_connection():
    db_path = os.path.join('database', 'food_app.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    
    # ① 検索窓（name="q"）に入力された文字を読み取る
    query = request.args.get('q', '')

    if query:
        # ② 文字が入っている場合：名前にその文字を含む食材だけを探す（LIKE検索）
        ingredients = conn.execute("""
            SELECT * FROM ingredients 
            WHERE is_deleted = 0 AND name LIKE ?
            ORDER BY expiry_date
        """, ('%' + query + '%',)).fetchall()
    else:
        # ③ 文字が空の場合：今まで通り全部出す
        ingredients = conn.execute(
            "SELECT * FROM ingredients WHERE is_deleted = 0 ORDER BY expiry_date"
        ).fetchall()

    conn.close()

    # ④ 検索キーワード（query）も一緒にHTMLへ送る（検索窓に文字を残すため）
    return render_template("index.html", ingredients=ingredients, query=query)

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
    ingredient = conn.execute('SELECT * FROM ingredients WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        # --- ここから画像処理を追加 ---
        image = request.files.get('image')
        image_name = ingredient['photo_path']  # 基本は今の画像名（変えない）

        if image and image.filename != "":
            image_name = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
        # --- ここまで ---

        name = request.form['ingredientName']
        purchase_date = request.form['purchaseDate']
        expiry_date = request.form['expiryDate']
        quantity = request.form['quantity']
        unit = request.form['unit']
        category = request.form['category']
        memo = request.form['memo']

        # SQLの UPDATE 文に photo_path を追加
        conn.execute("""
            UPDATE ingredients
            SET name=?, purchase_date=?, expiry_date=?, quantity=?, unit=?, category=?, memo=?, photo_path=?
            WHERE id=?
        """, (name, purchase_date, expiry_date, quantity, unit, category, memo, image_name, id))
        
        conn.commit()
        conn.close()
        return redirect('/')

    conn.close()
    return render_template('edit.html', ingredient=ingredient)

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