from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
# --- 霑ｽ蜉・夂判蜒上・菫晏ｭ伜ｴ謇繧偵い繝励Μ縺ｫ謨吶∴繧・---
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 繝・・繧ｿ繝吶・繧ｹ縺ｫ謗･邯壹☆繧矩未謨ｰ・亥ｾ後〒菴ｿ縺・∪縺呻ｼ・
def get_db_connection():
    db_path = os.path.join('database', 'food_app.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    
    # 竭 讀懃ｴ｢遯難ｼ・ame="q"・峨↓蜈･蜉帙＆繧後◆譁・ｭ励ｒ隱ｭ縺ｿ蜿悶ｋ
    query = request.args.get('q', '')

    if query:
        # 竭｡ 譁・ｭ励′蜈･縺｣縺ｦ縺・ｋ蝣ｴ蜷茨ｼ壼錐蜑阪↓縺昴・譁・ｭ励ｒ蜷ｫ繧鬟滓攝縺縺代ｒ謗｢縺呻ｼ・IKE讀懃ｴ｢・・
        ingredients = conn.execute("""
            SELECT * FROM ingredients 
            WHERE is_deleted = 0 AND name LIKE ?
            ORDER BY expiry_date
        """, ('%' + query + '%',)).fetchall()
    else:
        # 竭｢ 譁・ｭ励′遨ｺ縺ｮ蝣ｴ蜷茨ｼ壻ｻ翫∪縺ｧ騾壹ｊ蜈ｨ驛ｨ蜃ｺ縺・
        ingredients = conn.execute(
            "SELECT * FROM ingredients WHERE is_deleted = 0 ORDER BY expiry_date"
        ).fetchall()

    conn.close()

    # 竭｣ 讀懃ｴ｢繧ｭ繝ｼ繝ｯ繝ｼ繝会ｼ・uery・峨ｂ荳邱偵↓HTML縺ｸ騾√ｋ・域､懃ｴ｢遯薙↓譁・ｭ励ｒ谿九☆縺溘ａ・・
    return render_template("index.html", ingredients=ingredients, query=query)

# 鬟滓攝霑ｽ蜉・・reate・壹梧眠隕剰ｿｽ蜉縲阪・繧ｿ繝ｳ繧呈悽蠖薙↓蜍輔°縺・
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

        image = request.files.get('image')

        conn = get_db_connection()
        cursor = conn.cursor()

        image_name = None
        
        if image and image.filename != "":
            image_name = image.filename
            image.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    image_name
                )
            )

            cursor.execute("""
                INSERT INTO uploads
                (file_name, file_path)
                VALUES (?, ?)
            """, (
                image_name,
                'static/uploads/' + image_name
            ))

            upload_id = cursor.lastrowid            

        conn.execute("""
            INSERT INTO ingredients
            (name, purchase_date, expiry_date,
             quantity, unit, category, memo, upload_id, is_deleted)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (
            name,
            purchase_date,
            expiry_date,
            quantity,
            unit,
            category,
            memo,
            upload_id
        ))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('edit.html')

#邱ｨ髮・・繧ｿ繝ｳ繧呈悽蠖薙↓蜍輔°縺・
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_ingredient(id):
    conn = get_db_connection()
    ingredient = conn.execute("""
        SELECT
        ingredients.*,
        uploads.file_path
        FROM ingredients
        LEFT JOIN uploads
        ON ingredients.upload_id = uploads.id
        WHERE ingredients.id = ?
        """, (id,)).fetchone()

    if request.method == 'POST':

        name = request.form['ingredientName']
        purchase_date = request.form['purchaseDate']
        expiry_date = request.form['expiryDate']
        quantity = request.form['quantity']
        unit = request.form['unit']
        category = request.form['category']
        memo = request.form['memo']

        image = request.files.get('image')

        cursor = conn.cursor()

        upload_id = ingredient['upload_id']

        if image and image.filename != "":
            image_name = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))

            cursor.execute("""
                INSERT INTO uploads
                (file_name, file_path)
                VALUES (?, ?)
            """, (
                image_name,
                'static/uploads/' + image_name
            ))

            upload_id = cursor.lastrowid

        # SQL縺ｮ UPDATE 譁・↓ photo_path 繧定ｿｽ蜉
        conn.execute("""
            UPDATE ingredients
            SET name=?, purchase_date=?, expiry_date=?, quantity=?, unit=?, category=?, memo=?, upload_id=?
            WHERE id=?
        """, (name, purchase_date, expiry_date, quantity, unit, category, memo, upload_id, id))
        
        conn.commit()
        conn.close()
        return redirect('/')

    conn.close()
    return render_template('edit.html', ingredient=ingredient)

#蜑企勁繝ｫ繝ｼ繝・
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

# DB謗･邯壹ユ繧ｹ繝・
@app.route('/test-db')
def test_db():
    conn = get_db_connection()

    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()

    conn.close()

    return str([row["name"] for row in tables])


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
