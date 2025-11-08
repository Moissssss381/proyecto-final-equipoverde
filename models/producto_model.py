from database.db_connection import get_db_connection
class ProductModel:
    @staticmethod
    def agregar_producto(nombre, descripcion, categoria, precio_compra, precio_venta, stock, stock_minimo, unidad, proveedor_id):
        conn=get_db_connection()
        cursor=conn.cursor()

        cursor.execute('''INSERT TO productos (nombre, descripcion, categoria, precio_compra, stock, stock_minimo, unidad, proveedor_id) 
                       VALUES(?,?,?,?,?,?,?,?,?)''',(nombre, descripcion,categoria, precio_compra, stock, stock_minimo, unidad,proveedor_id))
        producto_id=cursor.lastrowid
        conn.commit()
        conn.close()
        return producto_id
    @staticmethod
    def obtener_productos():
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.executer('''SELECT p.*, pr.nombre AS proveedor_nombre
            FROM productos p
            LEFT JOIN proveedores pr ON p.proveedor_id = pr.id
            ORDER BY p.nombre''')
        productos=cursor.fetchall()
        conn.close()
        return productos
    @staticmethod
    def obtener_producto_por_id(producto_id):
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.executer(''' SELECT p.*, pr. nombre AS proveedor_nombre FROM productos p LEFT JOIN proveedores pr ON p.proveedor_id=pr.id WHERE p.id=?''', (producto_id,))
        producto=cursor.fetchone()
        conn.close()
        return producto
    @staticmethod
    def actualizar_producto(producto_id, nombre, descripcion, categoria, precio_compra, precio_venta, stock, stock_minimo, unidad, proveedor_id, activo):
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute('''UPDATE productos SET nombre = ?, descripcion = ?, categoria = ?, 
                precio_compra = ?, precio_venta = ?, stock = ?, 
                stock_minimo = ?, unidad = ?, proveedor_id = ?, activo = ?
            WHERE id = ?
        ''', (nombre, descripcion, categoria, precio_compra, precio_venta, stock,
              stock_minimo, unidad, proveedor_id, activo, producto_id))
        conn.commit()
        conn.close()
        return True
    @staticmethod
    def eliminar_producto(producto_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM detalle_ventas WHERE producto_id = ?', (producto_id,))
        ventas_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM detalle_compras WHERE producto_id = ?', (producto_id,))
        compras_count = cursor.fetchone()[0]
        if ventas_count > 0 or compras_count > 0:
            raise Exception("No se puede eliminar el producto porque tiene movimientos asociados")
        cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
        conn.commit()
        conn.close()
        return True