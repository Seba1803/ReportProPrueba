from datetime import datetime, timedelta
import basedatos

def verificar_mantenimientos_pendientes():
    desde = datetime.now().date()
    hasta = desde + timedelta(days=7)
    mantenimientos = basedatos.obtener_mantenimientos_proximos(desde.isoformat(), hasta.isoformat())
    programados = obtener_programaciones_pendientes(desde.isoformat(), hasta.isoformat())
    return mantenimientos, programados

def obtener_programaciones_pendientes(desde, hasta):
    conn = basedatos.conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT pm.id, ma.nombre, pm.fecha_programada, pm.tipo_servicio, pm.observaciones
        FROM programacion_mantenimientos pm
        JOIN maquinaria ma ON pm.maquinaria_id = ma.id
        WHERE pm.fecha_programada BETWEEN ? AND ?
        ORDER BY pm.fecha_programada ASC
    ''', (desde, hasta))
    resultados = cursor.fetchall()
    conn.close()
    return resultados
