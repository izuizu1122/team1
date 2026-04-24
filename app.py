from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

# データベースに接続する関数（後で使います）
def get_db_connection():
    db_path = os.path.join('datebase', 'food_app.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    # templates/index.html を表示させる
    return render_template('index.html')

# 接続テスト
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