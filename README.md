# SBJ by Firebase

## ファイル構成
main.py  Flaskコード。現在はルーティングもこのファイル
- static
  - css
  - js   各画面に対応したjsファイル。aタグで遷移するだけならgame.js以外いらない
    - start.js
    - rule.js
    - game.js
    - interrupt.js
    - end.js
- templates
  - start.html   実験開始画面
  - rule.html    ルール説明画面
  - game.html    ゲーム画面
  - interrupt.html  中断画面
  - end.html     実験終了画面

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

## Cloud Run

### 必要ファイル
- requirements.txt
- main.py

### デプロイ
```
gcloud run deploy
```
