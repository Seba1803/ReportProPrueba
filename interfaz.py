import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import basedatos
import notificaciones
import reportes

def iniciar_interfaz():
    print("Iniciando interfaz gráfica...")
    ventana = tk.Tk()
    ventana.title("ReportPro - Sistema de Gestión de Talleres")
    ventana.geometry("1024x768")
    ventana.state('zoomed')
    ventana.resizable(True, True)

    # Estilos para la interfaz
    estilo = ttk.Style()
    estilo.theme_use('clam')
    estilo.configure('TLabel', font=('Segoe UI', 12))
    estilo.configure('TButton', font=('Segoe UI', 11))
    estilo.configure('TEntry', font=('Segoe UI', 12))
    estilo.configure('TCombobox', font=('Segoe UI', 12))

    # Menú principal
    menu_bar = tk.Menu(ventana)
    ventana.config(menu=menu_bar)

    # Menú Archivo
    menu_archivo = tk.Menu(menu_bar, tearoff=0)
    menu_archivo.add_command(label="Salir", command=ventana.quit)
    menu_bar.add_cascade(label="Archivo", menu=menu_archivo)

    # Menú Gestión
    menu_gestion = tk.Menu(menu_bar, tearoff=0)
    menu_gestion.add_command(label="Maquinaria", command=ventana_maquinaria)
    menu_gestion.add_command(label="Mantenimientos", command=ventana_mantenimientos)
    menu_bar.add_cascade(label="Gestión", menu=menu_gestion)

    # Menú Inventario
    menu_inventario = tk.Menu(menu_bar, tearoff=0)
    menu_inventario.add_command(label="Productos", command=ventana_productos)
    menu_inventario.add_command(label="Movimientos de Stock", command=ventana_movimientos_stock)
    menu_bar.add_cascade(label="Inventario", menu=menu_inventario)

    # Menú Reportes
    menu_reportes = tk.Menu(menu_bar, tearoff=0)
    menu_reportes.add_command(label="Reporte de Mantenimientos", command=ventana_reportes_mantenimientos)
    menu_reportes.add_command(label="Reporte de Inventario", command=ventana_reportes_inventario)
    menu_bar.add_cascade(label="Reportes", menu=menu_reportes)

    # Menú Ayuda
    menu_ayuda = tk.Menu(menu_bar, tearoff=0)
    menu_ayuda.add_command(label="Acerca de", command=mostrar_acerca_de)
    menu_bar.add_cascade(label="Ayuda", menu=menu_ayuda)

    # Mensaje de bienvenida
    lbl_bienvenida = ttk.Label(ventana, text="¡Bienvenido a ReportPro!", font=('Segoe UI', 20))
    lbl_bienvenida.pack(pady=30)

    # Botones de acceso rápido sin imágenes
    marco_botones = ttk.Frame(ventana)
    marco_botones.pack(pady=20)

    btn_maquinaria = ttk.Button(marco_botones, text="Maquinaria", command=ventana_maquinaria, width=20)
    btn_maquinaria.grid(row=0, column=0, padx=10, pady=10)

    btn_mantenimientos = ttk.Button(marco_botones, text="Mantenimientos", command=ventana_mantenimientos, width=20)
    btn_mantenimientos.grid(row=0, column=1, padx=10, pady=10)

    btn_inventario = ttk.Button(marco_botones, text="Inventario", command=ventana_productos, width=20)
    btn_inventario.grid(row=0, column=2, padx=10, pady=10)

    btn_reportes = ttk.Button(marco_botones, text="Reportes", command=ventana_reportes_mantenimientos, width=20)
    btn_reportes.grid(row=0, column=3, padx=10, pady=10)

    # Verificar mantenimientos pendientes
    mantenimientos_pendientes, programados = notificaciones.verificar_mantenimientos_pendientes()
    if mantenimientos_pendientes or programados:
        mensaje = ""
        if mantenimientos_pendientes:
            mensaje += "Mantenimientos próximos:\n"
            for m in mantenimientos_pendientes:
                mensaje += f"{m[2]} - {m[1]} ({m[3]})\n"
        if programados:
            mensaje += "\nMantenimientos programados:\n"
            for p in programados:
                mensaje += f"{p[2]} - {p[1]} ({p[3]})\n"
        messagebox.showinfo("Notificaciones", mensaje)

    ventana.mainloop()
    print("Interfaz gráfica cerrada.")

# Función para mostrar la ventana "Acerca de"
def mostrar_acerca_de():
    messagebox.showinfo("Acerca de ReportPro", "ReportPro v1.0\nSistema de Gestión de Talleres Mecánicos\nDesarrollado por [Tu Nombre]")

# Función para gestionar la maquinaria
def ventana_maquinaria():
    ventana_m = tk.Toplevel()
    ventana_m.title("Gestión de Maquinaria - ReportPro")
    ventana_m.geometry("800x600")
    ventana_m.resizable(False, False)

    # Estilos
    estilo = ttk.Style()
    estilo.theme_use('clam')

    # Marco para el formulario
    marco_formulario = ttk.Frame(ventana_m)
    marco_formulario.pack(pady=10)

    ttk.Label(marco_formulario, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    entrada_nombre = ttk.Entry(marco_formulario, width=50)
    entrada_nombre.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(marco_formulario, text="Descripción:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    entrada_descripcion = ttk.Entry(marco_formulario, width=50)
    entrada_descripcion.grid(row=1, column=1, padx=5, pady=5)

    def agregar_maquinaria():
        nombre = entrada_nombre.get()
        descripcion = entrada_descripcion.get()
        if nombre:
            basedatos.agregar_maquinaria(nombre, descripcion)
            messagebox.showinfo("Éxito", "Maquinaria agregada correctamente.")
            actualizar_lista()
            entrada_nombre.delete(0, tk.END)
            entrada_descripcion.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "El nombre es obligatorio.")

    ttk.Button(marco_formulario, text="Agregar", command=agregar_maquinaria).grid(row=2, column=1, pady=10, sticky='e')

    # Lista de maquinaria
    columnas = ("ID", "Nombre", "Descripción")
    tabla = ttk.Treeview(ventana_m, columns=columnas, show="headings", height=15)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=200)
    tabla.pack(pady=10)

    # Barra de desplazamiento vertical
    scroll_vertical = ttk.Scrollbar(ventana_m, orient='vertical', command=tabla.yview)
    tabla.configure(yscroll=scroll_vertical.set)
    scroll_vertical.pack(side='right', fill='y')

    def actualizar_lista():
        for fila in tabla.get_children():
            tabla.delete(fila)
        maquinaria = basedatos.obtener_maquinaria()
        for m in maquinaria:
            tabla.insert("", tk.END, values=m)

    def eliminar_maquinaria():
        item_seleccionado = tabla.selection()
        if item_seleccionado:
            maquinaria_id = tabla.item(item_seleccionado)["values"][0]
            nombre_maquinaria = tabla.item(item_seleccionado)["values"][1]
            respuesta = messagebox.askyesno("Confirmación", f"¿Estás seguro de eliminar la maquinaria '{nombre_maquinaria}'?")
            if respuesta:
                basedatos.eliminar_maquinaria(maquinaria_id)
                messagebox.showinfo("Éxito", "Maquinaria eliminada correctamente.")
                actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Selecciona un registro para eliminar.")

    ttk.Button(ventana_m, text="Eliminar", command=eliminar_maquinaria).pack(pady=5)

    actualizar_lista()

# Función para gestionar los mantenimientos
def ventana_mantenimientos():
    ventana_mtto = tk.Toplevel()
    ventana_mtto.title("Gestión de Mantenimientos - ReportPro")
    ventana_mtto.geometry("900x700")
    ventana_mtto.resizable(False, False)

    # Estilos
    estilo = ttk.Style()
    estilo.theme_use('clam')

    # Marco para el formulario
    marco_formulario = ttk.Frame(ventana_mtto)
    marco_formulario.pack(pady=10)

    ttk.Label(marco_formulario, text="Maquinaria:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    maquinaria_lista = [m[1] for m in basedatos.obtener_maquinaria()]
    maquinaria_var = tk.StringVar()
    combo_maquinaria = ttk.Combobox(marco_formulario, textvariable=maquinaria_var, values=maquinaria_lista, width=47)
    combo_maquinaria.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(marco_formulario, text="Fecha (AAAA-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    entrada_fecha = ttk.Entry(marco_formulario, width=50)
    entrada_fecha.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(marco_formulario, text="Tipo de Servicio:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
    entrada_servicio = ttk.Entry(marco_formulario, width=50)
    entrada_servicio.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(marco_formulario, text="Piezas Reemplazadas:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
    entrada_piezas = ttk.Entry(marco_formulario, width=50)
    entrada_piezas.grid(row=3, column=1, padx=5, pady=5)
    ttk.Label(marco_formulario, text="(Separe las piezas por comas)").grid(row=3, column=2, padx=5, pady=5, sticky='w')

    ttk.Label(marco_formulario, text="Observaciones:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
    entrada_observaciones = scrolledtext.ScrolledText(marco_formulario, width=37, height=5)
    entrada_observaciones.grid(row=4, column=1, padx=5, pady=5)

    def agregar_mantenimiento():
        maquinaria_nombre = maquinaria_var.get()
        fecha = entrada_fecha.get()
        tipo_servicio = entrada_servicio.get()
        piezas = entrada_piezas.get()
        observaciones = entrada_observaciones.get('1.0', tk.END).strip()

        if maquinaria_nombre and fecha and tipo_servicio:
            maquinaria = basedatos.obtener_maquinaria_por_nombre(maquinaria_nombre)
            if maquinaria:
                maquinaria_id = maquinaria[0]
                basedatos.agregar_mantenimiento(maquinaria_id, fecha, tipo_servicio, piezas, observaciones)
                # Descontar piezas del inventario
                if piezas:
                    lista_piezas = piezas.split(',')
                    for pieza in lista_piezas:
                        pieza = pieza.strip()
                        producto = basedatos.obtener_producto_por_nombre(pieza)
                        if producto:
                            producto_id, stock_actual = producto
                            if stock_actual > 0:
                                basedatos.actualizar_stock(producto_id, 1, 'Salida')
                            else:
                                messagebox.showwarning("Stock insuficiente", f"No hay stock disponible para {pieza}")
                        else:
                            messagebox.showwarning("Producto no encontrado", f"La pieza '{pieza}' no está registrada en el inventario.")
                messagebox.showinfo("Éxito", "Mantenimiento registrado correctamente.")
                actualizar_lista()
                # Limpiar campos
                maquinaria_var.set('')
                entrada_fecha.delete(0, tk.END)
                entrada_servicio.delete(0, tk.END)
                entrada_piezas.delete(0, tk.END)
                entrada_observaciones.delete('1.0', tk.END)
            else:
                messagebox.showerror("Error", "Maquinaria no encontrada.")
        else:
            messagebox.showwarning("Advertencia", "Completa los campos obligatorios.")

    ttk.Button(marco_formulario, text="Registrar Mantenimiento", command=agregar_mantenimiento).grid(row=5, column=1, pady=20, sticky='e')

    # Lista de mantenimientos
    columnas = ("ID", "Maquinaria", "Fecha", "Servicio", "Piezas", "Observaciones")
    tabla = ttk.Treeview(ventana_mtto, columns=columnas, show="headings", height=20)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=130)
    tabla.pack(pady=10)

    # Barra de desplazamiento vertical
    scroll_vertical = ttk.Scrollbar(ventana_mtto, orient='vertical', command=tabla.yview)
    tabla.configure(yscroll=scroll_vertical.set)
    scroll_vertical.pack(side='right', fill='y')

    def actualizar_lista():
        for fila in tabla.get_children():
            tabla.delete(fila)
        mantenimientos = basedatos.obtener_mantenimientos()
        for m in mantenimientos:
            tabla.insert("", tk.END, values=m)

    actualizar_lista()

# Función para gestionar los productos del inventario
def ventana_productos():
    ventana_p = tk.Toplevel()
    ventana_p.title("Gestión de Productos - ReportPro")
    ventana_p.geometry("800x600")
    ventana_p.resizable(False, False)

    # Estilos
    estilo = ttk.Style()
    estilo.theme_use('clam')

    # Marco para el formulario
    marco_formulario = ttk.Frame(ventana_p)
    marco_formulario.pack(pady=10)

    ttk.Label(marco_formulario, text="Nombre del Producto:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    entrada_nombre = ttk.Entry(marco_formulario, width=50)
    entrada_nombre.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(marco_formulario, text="Descripción:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    entrada_descripcion = ttk.Entry(marco_formulario, width=50)
    entrada_descripcion.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(marco_formulario, text="Cantidad Inicial:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
    entrada_cantidad = ttk.Entry(marco_formulario, width=50)
    entrada_cantidad.grid(row=2, column=1, padx=5, pady=5)

    def agregar_producto():
        nombre = entrada_nombre.get()
        descripcion = entrada_descripcion.get()
        cantidad = entrada_cantidad.get()
        if nombre and cantidad.isdigit():
            exito = basedatos.agregar_producto(nombre, descripcion, int(cantidad))
            if exito:
                messagebox.showinfo("Éxito", "Producto agregado correctamente.")
                actualizar_lista()
                entrada_nombre.delete(0, tk.END)
                entrada_descripcion.delete(0, tk.END)
                entrada_cantidad.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "El producto ya existe.")
        else:
            messagebox.showwarning("Advertencia", "Completa los campos obligatorios con valores válidos.")

    ttk.Button(marco_formulario, text="Agregar Producto", command=agregar_producto).grid(row=3, column=1, pady=20, sticky='e')

    # Lista de productos
    columnas = ("ID", "Nombre", "Descripción", "Stock")
    tabla = ttk.Treeview(ventana_p, columns=columnas, show="headings", height=20)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=200)
    tabla.pack(pady=10)

    # Barra de desplazamiento vertical
    scroll_vertical = ttk.Scrollbar(ventana_p, orient='vertical', command=tabla.yview)
    tabla.configure(yscroll=scroll_vertical.set)
    scroll_vertical.pack(side='right', fill='y')

    def actualizar_lista():
        for fila in tabla.get_children():
            tabla.delete(fila)
        productos = basedatos.obtener_productos()
        for p in productos:
            tabla.insert("", tk.END, values=p)

    actualizar_lista()

# Función para registrar movimientos de stock
def ventana_movimientos_stock():
    ventana_ms = tk.Toplevel()
    ventana_ms.title("Movimientos de Stock - ReportPro")
    ventana_ms.geometry("800x600")
    ventana_ms.resizable(False, False)

    # Estilos
    estilo = ttk.Style()
    estilo.theme_use('clam')

    # Marco para el formulario
    marco_formulario = ttk.Frame(ventana_ms)
    marco_formulario.pack(pady=10)

    ttk.Label(marco_formulario, text="Producto:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    productos_lista = [p[1] for p in basedatos.obtener_productos()]
    producto_var = tk.StringVar()
    combo_producto = ttk.Combobox(marco_formulario, textvariable=producto_var, values=productos_lista, width=47)
    combo_producto.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(marco_formulario, text="Tipo de Movimiento:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    tipo_var = tk.StringVar(value='Entrada')
    opciones_tipo = ['Entrada', 'Salida']
    combo_tipo = ttk.Combobox(marco_formulario, textvariable=tipo_var, values=opciones_tipo, state='readonly', width=47)
    combo_tipo.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(marco_formulario, text="Cantidad:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
    entrada_cantidad = ttk.Entry(marco_formulario, width=50)
    entrada_cantidad.grid(row=2, column=1, padx=5, pady=5)

    def registrar_movimiento():
        producto_nombre = producto_var.get()
        tipo_movimiento = tipo_var.get()
        cantidad = entrada_cantidad.get()
        if producto_nombre and cantidad.isdigit():
            producto = basedatos.obtener_producto_por_nombre(producto_nombre)
            if producto:
                producto_id = producto[0]
                basedatos.actualizar_stock(producto_id, int(cantidad), tipo_movimiento)
                messagebox.showinfo("Éxito", "Movimiento registrado correctamente.")
                entrada_cantidad.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Producto no encontrado.")
        else:
            messagebox.showwarning("Advertencia", "Completa los campos obligatorios con valores válidos.")

    ttk.Button(marco_formulario, text="Registrar Movimiento", command=registrar_movimiento).grid(row=3, column=1, pady=20, sticky='e')

# Función para generar reportes de mantenimientos
def ventana_reportes_mantenimientos():
    ventana_r = tk.Toplevel()
    ventana_r.title("Reporte de Mantenimientos - ReportPro")
    ventana_r.geometry("500x300")
    ventana_r.resizable(False, False)

    ttk.Label(ventana_r, text="Generar Reporte de Mantenimientos").pack(pady=20)

    ttk.Label(ventana_r, text="Desde (AAAA-MM-DD):").pack()
    entrada_desde = ttk.Entry(ventana_r, width=30)
    entrada_desde.pack()

    ttk.Label(ventana_r, text="Hasta (AAAA-MM-DD):").pack()
    entrada_hasta = ttk.Entry(ventana_r, width=30)
    entrada_hasta.pack()

    def generar_reporte():
        desde = entrada_desde.get()
        hasta = entrada_hasta.get()
        mantenimientos = basedatos.obtener_mantenimientos_por_fecha(desde, hasta)
        if mantenimientos:
            reportes.generar_reporte_mantenimientos(mantenimientos, desde, hasta)
            messagebox.showinfo("Éxito", "Reporte generado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "No hay datos para el rango de fechas seleccionado.")

    ttk.Button(ventana_r, text="Generar Reporte", command=generar_reporte).pack(pady=20)

# Función para generar reportes de inventario
def ventana_reportes_inventario():
    ventana_ri = tk.Toplevel()
    ventana_ri.title("Reporte de Inventario - ReportPro")
    ventana_ri.geometry("500x200")
    ventana_ri.resizable(False, False)

    ttk.Label(ventana_ri, text="Generar Reporte de Inventario Actual").pack(pady=20)

    def generar_reporte():
        productos = basedatos.obtener_productos()
        if productos:
            reportes.generar_reporte_inventario(productos)
            messagebox.showinfo("Éxito", "Reporte de inventario generado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "No hay productos en el inventario.")

    ttk.Button(ventana_ri, text="Generar Reporte", command=generar_reporte).pack(pady=20)
