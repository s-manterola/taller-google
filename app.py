from flask import Flask, render_template, request

from datetime import datetime

import consultas

app = Flask(__name__)

@app.route("/")
def main():
    #return render_template("index.html")
    return render_template("index_chatgpt.html")

@app.route('/productos')
def productos():
    return consultas.getProductos()


@app.route('/pedido', methods=['POST'])
def pedido():
    now = datetime.now().date()
    datos = request.get_json()
    consultas.insercion(datos['items'], now)
        
    return {'ok': 'ok'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)