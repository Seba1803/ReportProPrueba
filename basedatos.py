import sqlite3
import bcrypt
import smtplib
import random
from email.mime.text import MIMEText
from datetime import datetime

def conectar():
    return sqlite3.connect('reportpro.db')

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    # Crear tablas si no existen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maquinaria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mantenimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            maquinaria_id INTEGER,
            fecha DATE,
            tipo_servicio TEXT,
            piezas_reemplazadas TEXT,
            observaciones TEXT,
            FOREIGN KEY(maquinaria_id) REFERENCES maquinaria(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            descripcion TEXT,
            stock INTEGER NOT NULL DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimientos_stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            fecha DATE,
            tipo_movimiento TEXT,
            cantidad INTEGER,
            FOREIGN KEY(producto_id) REFERENCES productos(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registro_actividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            actividad TEXT,
            fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS programacion_mantenimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            maquinaria_id INTEGER,
            fecha_programada DATE,
            tipo_servicio TEXT,
            observaciones TEXT,
            FOREIGN KEY(maquinaria_id) REFERENCES maquinaria(id)
        )
    ''')

    conn.commit()
    conn.close()

# Funciones de maquinaria

def agregar_maquinaria(nombre, descripcion):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO maquinaria (nombre, descripcion)
        VALUES (?, ?)
    ''', (nombre, descripcion))
    conn.commit()
    conn.close()

def obtener_maquinaria():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, descripcion FROM maquinaria')
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def eliminar_maquinaria(maquinaria_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM maquinaria WHERE id = ?', (maquinaria_id,))
    conn.commit()
    conn.close()

def obtener_maquinaria_por_nombre(nombre):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM maquinaria WHERE nombre = ?', (nombre,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

# Funciones de mantenimientos

def agregar_mantenimiento(maquinaria_id, fecha, tipo_servicio, piezas, observaciones):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO mantenimientos (maquinaria_id, fecha, tipo_servicio, piezas_reemplazadas, observaciones)
        VALUES (?, ?, ?, ?, ?)
    ''', (maquinaria_id, fecha, tipo_servicio, piezas, observaciones))
    conn.commit()
    conn.close()

def obtener_mantenimientos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.id, ma.nombre, m.fecha, m.tipo_servicio, m.piezas_reemplazadas, m.observaciones
        FROM mantenimientos m
        JOIN maquinaria ma ON m.maquinaria_id = ma.id
    ''')
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def obtener_mantenimientos_por_fecha(desde, hasta):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.id, ma.nombre, m.fecha, m.tipo_servicio, m.piezas_reemplazadas, m.observaciones
        FROM mantenimientos m
        JOIN maquinaria ma ON m.maquinaria_id = ma.id
        WHERE m.fecha BETWEEN ? AND ?
    ''', (desde, hasta))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def obtener_mantenimientos_proximos(desde, hasta):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT m.id, m.tipo_servicio, m.fecha, ma.nombre
        FROM mantenimientos m
        JOIN maquinaria ma ON m.maquinaria_id = ma.id
        WHERE m.fecha BETWEEN ? AND ?
    ''', (desde, hasta))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# Funciones de programación de mantenimientos

def programar_mantenimiento(maquinaria_id, fecha_programada, tipo_servicio, observaciones):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO programacion_mantenimientos (maquinaria_id, fecha_programada, tipo_servicio, observaciones)
        VALUES (?, ?, ?, ?)
    ''', (maquinaria_id, fecha_programada, tipo_servicio, observaciones))
    conn.commit()
    conn.close()

def obtener_programaciones():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT pm.id, ma.nombre, pm.fecha_programada, pm.tipo_servicio, pm.observaciones
        FROM programacion_mantenimientos pm
        JOIN maquinaria ma ON pm.maquinaria_id = ma.id
        ORDER BY pm.fecha_programada ASC
    ''')
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def eliminar_programacion(programacion_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM programacion_mantenimientos WHERE id = ?', (programacion_id,))
    conn.commit()
    conn.close()

# Funciones de inventario

def agregar_producto(nombre, descripcion, cantidad_inicial):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO productos (nombre, descripcion, stock)
            VALUES (?, ?, ?)
        ''', (nombre, descripcion, cantidad_inicial))
        conn.commit()
    except sqlite3.IntegrityError:
        return False  # El producto ya existe
    finally:
        conn.close()
    return True

def obtener_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, descripcion, stock FROM productos')
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def actualizar_stock(producto_id, cantidad, tipo_movimiento):
    conn = conectar()
    cursor = conn.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    # Registrar el movimiento
    cursor.execute('''
        INSERT INTO movimientos_stock (producto_id, fecha, tipo_movimiento, cantidad)
        VALUES (?, ?, ?, ?)
    ''', (producto_id, fecha_actual, tipo_movimiento, cantidad))
    # Actualizar el stock del producto
    if tipo_movimiento == 'Entrada':
        cursor.execute('UPDATE productos SET stock = stock + ? WHERE id = ?', (cantidad, producto_id))
    elif tipo_movimiento == 'Salida':
        cursor.execute('UPDATE productos SET stock = stock - ? WHERE id = ?', (cantidad, producto_id))
    conn.commit()
    conn.close()

def obtener_producto_por_nombre(nombre):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT id, stock FROM productos WHERE nombre = ?', (nombre,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def obtener_movimientos_stock():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT ms.id, p.nombre, ms.fecha, ms.tipo_movimiento, ms.cantidad
        FROM movimientos_stock ms
        JOIN productos p ON ms.producto_id = p.id
        ORDER BY ms.fecha DESC
    ''')
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# Funciones de registro de actividades

def registrar_actividad(usuario, actividad):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO registro_actividades (usuario, actividad)
        VALUES (?, ?)
    ''', (usuario, actividad))
    conn.commit()
    conn.close()

def obtener_registro_actividades():
    conn = conectar()
    cursor # type: ignore