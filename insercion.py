import psycopg2

def insercion(cliente, items, fecha):
# Conexión a la base de datos
    conn = psycopg2.connect(
        host        = "localhost",
        database    = "tu_base_de_datos",
        user        = "tu_usuario",
        password    = "tu_contraseña"
    )

    try:
        with conn:
            with conn.cursor() as cur:
                # Obtener precios desde la tabla productos
                producto_ids = [item["producto_id"] for item in items]
                cur.execute(
                    "SELECT id, precio FROM productos WHERE id = ANY(%s)",
                    (producto_ids,)
                )
                precios_db = dict(cur.fetchall())  # {1: 1200, 3: 1500, ...}

                # Calcular total del pedido
                total = 0
                for item in items:
                    pid = item["producto_id"]
                    if pid not in precios_db:
                        raise ValueError(f"Producto con ID {pid} no existe.")
                    total += precios_db[pid] * item["cantidad"]

                # Insertar el pedido
                cur.execute(
                    """
                    INSERT INTO pedidos (cliente, fecha, total)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (cliente, fecha, total)
                )
                pedido_id = cur.fetchone()[0]

                # Insertar los ítems del pedido
                for item in items:
                    cur.execute(
                        """
                        INSERT INTO pedido_items (pedido_id, producto_id, cantidad)
                        VALUES (%s, %s, %s)
                        """,
                        (pedido_id, item["producto_id"], item["cantidad"])
                    )

        print(f"Pedido insertado con ID: {pedido_id}, total: ${total}")

    except Exception as e:
        print("Ocurrió un error:", e)
        conn.rollback()
    finally:
        conn.close()
