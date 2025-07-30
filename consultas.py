import psycopg2
import os

INSTANCE_CONNECTION_NAME    = os.environ.get("INSTANCE_CONNECTION_NAME")

def leer_secreto(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except Exception as e:
        print(f"Error al leer el secreto {path}: {e}")
        return None

# Lee los secretos montados por Secret Manager
DB_PASS = leer_secreto("/secrets/DB_PASS")
DB_USER = leer_secreto("/secrets/DB_USER")

print(DB_USER, DB_PASS)

# Parámetros de conexión
def connect():
    conn = psycopg2.connect(
        host        = f"/cloudsql/{INSTANCE_CONNECTION_NAME}",
        database    = 'panaderia',
        user        = DB_USER,
        password    = DB_PASS,
        port        = 5432
    )
    return conn, conn.cursor()


def getProductos():
    # Conectar a la base de datos
    conexion, cursor = connect()

    # Crear cursor
    cursor.execute("SELECT id, nombre, precio, descripcion FROM productos")

    # Obtener resultados
    productos = cursor.fetchall()

    prod = []
    for producto in productos:
        prod.append({'id'           : producto[0], 
                     'nombre'       : producto[1], 
                     'precio'       : producto[2], 
                     'descripcion'  : producto[3]})



    # Cerrar conexiones
    cursor.close()
    conexion.close()

    return prod

def insercion(items, now):
    conn, cursor = connect()
    
    # Paso 1: Calcular el total desde la base de datos
    producto_ids = [item["producto_id"] for item in items]
    cantidades = {item["producto_id"]: item["cantidad"] for item in items}

    query = """
        SELECT id, precio FROM productos WHERE id = ANY(%s);
    """
    cursor.execute(query, (producto_ids,))
    precios = cursor.fetchall()  # [(1, 1000), (2, 500), ...]

    total = sum(precio * cantidades[pid] for pid, precio in precios)

    # Paso 2: Insertar en la tabla pedidos
    cursor.execute(
        """
        INSERT INTO pedidos (total, fecha)
        VALUES (%s, %s)
        RETURNING id;
        """,
        (total, now)
    )
    pedido_id = cursor.fetchone()[0]

    # Paso 3: Insertar en tabla pedido_productos (debes tener esta tabla creada)
    detalle_values = [
        (pedido_id, item["producto_id"], item["cantidad"])
        for item in items
    ]
    cursor.executemany(
        """
        INSERT INTO pedido_productos (pedido_id, producto_id, cantidad)
        VALUES (%s, %s, %s);
        """,
        detalle_values
    )

    conn.commit()


    cursor.close()
    conn.close()