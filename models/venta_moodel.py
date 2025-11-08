from database.db_connection import get_db_connection
class VentaModel:
    @staticmethod
    def agregar_venta(cliente_id, usuario_id, productos):
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute('''INSERT INTO ventas (cliente_id, usuario_id, productos) VALUES (?,?,?)''', (cliente_id, usuario_id, productos))
        venta_id=cursor.lastrowid
        conn.commit()
        conn.close()
        return venta_id
    @staticmethod
    def obtener_ventas(fecha_inicio=None, fecha_fin=None):
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute('''''')
    @staticmethod
    def obtener_detalle_venta(venta_id):pass
    @staticmethod
    def eliminar_venta(venta_id):pass