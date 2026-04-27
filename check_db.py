import sqlite3

conn = sqlite3.connect('database/food_app.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print('テーブル一覧:')
for table in tables:
    print(f'  - {table[0]}')
conn.close()
