from flask import Flask, render_template, request

from datetime import datetime

import insercion

productos = [
    { 'id': 1, 'nombre': 'Baguette', 'precio': 1200, 'descripcion': 'un tipo de pan largo'},
    { 'id': 2, 'nombre': 'Croissant', 'precio': 1000, 'descripcion': 'pan frances' },
]

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route('/productos')
def list():
    print('productos')
    return productos

@app.route('/pedido', methods=['POST'])
def pedido():
    now = datetime.now().date()
    print(now)
    cliente = request.args.get('cliente')
    datos = request.get_json()
    insercion.insercion(cliente, datos['items'], now)
        
    return {'ok': 'ok'}

if __name__ == "__main__":
    app.run()