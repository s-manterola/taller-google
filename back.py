from flask import Flask, render_template

productos = [
    { 'id': 1, 'nombre': 'Baguette', 'precio': 1200 },
    { 'id': 2, 'nombre': 'Croissant', 'precio': 1000 },
]

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route('/productos')
def list():
    print('productos')
    return productos

@app.route('/pedidos', methods=['POST'])
def pedidos():
    print('pedidos')
    return {'ok': 'ok'}

if __name__ == "__main__":
    app.run()