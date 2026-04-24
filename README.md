# 🥬 食材管理アプリ

食材の賞味期限を管理し、アラート通知で無駄を削減するアプリです。

## 📋 プロジェクト概要

このアプリは、家庭や飲食店で購入した食材の情報を登録し、賞味期限が近づくと通知を受け取ることができます。また、食材の写真を登録することで、冷蔵庫の中身を一目で把握できます。

## 🎯 機能一覧

### ✅ 完成済み機能

- **トップページ**
  - 登録済み食材の一覧表示
  - 検索機能（食材名で検索）
  - 削除機能
  - 編集ページへのリンク

- **マイページ**
  - ユーザープロフィール表示
  - 統計情報（登録済み食材数、期限が近い数など）
  - 設定機能（通知日数、テーマ選択）
  - アカウント管理（パスワード変更、アカウント削除）

- **編集ページ**
  - 食材の新規追加
  - 既存食材の編集
  - 食材の削除
  - 写真アップロード機能
  - フォーム入力値の検証

### ⏳ 実装予定機能

- REST API との連携
- データベースへの実際のデータ保存
- 賞味期限切れアラート通知
- ハンバーガーメニュー（スマートフォン対応）
- ダークモード対応

## 📁 ファイル構成

\`\`\`
team1/
├── index.html
├── mypage.html
├── edit.html
├── css/
│   ├── styles.css
│   ├── mypage-styles.css
│   └── edit-styles.css
├── js/
│   ├── index.js
│   ├── mypage.js
│   ├── edit.js
│   └── menu.js
└── README.md
\`\`\`

## 🚀 使い方

### 1. ローカルサーバー起動

\`\`\`powershell
python -m http.server 8000
\`\`\`

### 2. ブラウザでアクセス

- トップページ：http://localhost:8000/index.html
- マイページ：http://localhost:8000/mypage.html
- 編集ページ：http://localhost:8000/edit.html

## 📊 進捗状況

| タスク | 進捗度 |
|--------|--------|
| トップページ | ✅ 100% |
| マイページ | ✅ 100% |
| 編集ページ | ✅ 100% |
| 写真アップロード | ✅ 100% |
| REST API | ⏳ 実装中 |
| データベース連携 | ⏳ 実装中 |

## 👥 チーム
- フロントエンド担当
- バックエンド担当（Python/Flask/SQLite）

## 🗄 データベース設計（追加実装）

本プロジェクトでは SQLite + Flask によるデータベース連携を追加実装しています。

### 実装済みDB機能
- 食材データ登録（Create）
- 一覧表示（Read）
- 編集更新（Update）
- 論理削除（Delete）
- Flask と SQLite 接続
- schema.sql によるテーブル管理

### 採用している設計
#### ingredients テーブル
主な管理項目：

- id (PK)
- name
- purchase_date
- expiry_date
- quantity
- unit
- category
- memo
- is_deleted（論理削除）

#### uploads テーブル
画像管理用テーブル（食材と分離）

- id (PK)
- ingredient_id (FK)
- image_path

### 設計上のポイント
- **論理削除（is_deleted）採用**
  - 誤削除防止
  - データ保全

- **画像テーブル分離**
  - 正規化
  - 将来拡張しやすい構成

- **SQLインジェクション対策**
  - Parameterized Query（`?` プレースホルダ）で実装

---

## 🧩 バックエンド構成（追加）
使用技術：

- Python
- Flask
- SQLite
- DB Browser for SQLite
- Git / GitHub
- Render（デプロイ予定）

### Flaskルーティング
```python
/              # 一覧表示
/add           # 新規追加
/edit/<id>     # 編集
/delete/<id>   # 論理削除
/test-db       # DB接続確認
```

---

## 📌 バックエンド進捗（追加）
| 機能 | 状況 |
|------|------|
| DB設計 | ✅ 完了 |
| CRUD実装 | ✅ 完了 |
| 論理削除 | ✅ 完了 |
| Flask-DB接続 | ✅ 完了 |
| 画像DB連携 | ⏳ 今後対応 |

最終更新日：2026/04/24
