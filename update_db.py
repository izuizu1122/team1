import sqlite3
import os

# スクショから判明した正しいパスを指定
# databaseフォルダの中の food_app.db
db_path = os.path.join('database', 'food_app.db')

def update():
    if not os.path.exists(db_path):
        print(f"❌ まだファイルが見つかりません。現在の場所からの相対パス: {db_path}")
        return

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # photo_path 列を追加
        cursor.execute("ALTER TABLE ingredients ADD COLUMN photo_path TEXT")
        
        conn.commit()
        print("✅ 成功！データベースに photo_path 列を追加しました。")

    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("ℹ️ すでに photo_path 列は存在しています。そのまま進んでOKです！")
        else:
            print(f"❌ エラーが発生しました: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    update()