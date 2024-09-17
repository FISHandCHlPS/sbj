# Firebase を利用したプロジェクト作成

## 準備
- firebase の project 作成
  - anonymous auth を on に
  - firestore を on に
    - 権限なしでの read / write を許可する

## 共通ファイル
- static/index.html
- static/scripts/init.js
- static/scripts/auth.js
- static/scripts/main.js

### init.js
init_template.js に必要情報を記入して rename

## Firebase の hosting

サーバサイドが要らない場合のみ

### 必要ファイル
- firebase.json

### テスト環境で実行
```
firebase emulators:start
```

#### ブラウズ
local の 8080 ポートにアクセス

### デプロイ
```
firebase deploy --only hosting
```

## App Engine

### 必要ファイル
- app.yaml
- requirements.txt
- main.py

### テスト環境で実行
```
dev_appserver.py app.yaml
```

#### ブラウズ
local の 8080 ポートにアクセス

### デプロイ
```
gcloud app deploy
```

## Cloud Run

### 必要ファイル
- requirements.txt
- main.py

### デプロイ
```
gcloud run deploy
```