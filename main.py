from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/scripts/<script>')
def scripts(script):
    return app.send_static_file(f'scripts/{script}')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
