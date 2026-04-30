import sqlite3

# テーブル作成
conn = sqlite3.connect('database/food_app.db')
with open('database/schema.sql', 'r', encoding='utf-8') as f:
    schema = f.read()
conn.executescript(schema)
conn.close()

# 確認
conn = sqlite3.connect('database/food_app.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print('テーブル:', [t[0] for t in tables])
conn.close()
