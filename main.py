from flask import Flask, render_template, url_for

app = Flask(__name__)

# テスト用、本番はスタートを指定する
@app.route('/')
def index():
    return render_template('test.html', test_str='test')
    #return app.send_static_file('index.html')

# py側での処理がないならまとめて書いても良い
# スタート画面
@app.route('/start')
def start():
    return render_template('start.html')

# ルール説明画面
@app.route('/rule')
def rule():
    return render_template('rule.html')

# ゲーム画面
@app.route('/game')
def game():
    # ゲームの初期化処理はここに書ける
    # ログインやスタート処理など
    return render_template('game.html')

# 終了画面
@app.route('/end')
def end():
    # 終了処理はここにかける
    return render_template('end.html')

# 中断画面
@app.route('/interrupt')
def interrupt():
    # 中断用の処理を書く
    # aタグを使っているため、戻るボタンでゲーム画面に戻れてしまう。戻ったとき用の処理を考えておく
    # もしくはaタグではなくbuttonを使う
    return render_template('interrupt.html')



# 以下はapi用、本当はフォルダを分けて整理したい


@app.route('/scripts/<script>')
def scripts(script):
    return app.send_static_file(f'scripts/{script}')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
