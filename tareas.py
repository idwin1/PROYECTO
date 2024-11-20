from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # Importamos Pillow
from funcionalidad import seleccionar_opcion
import mysql.connector
import tkinter as tk
from tkinter import ttk

"""
def abrir_tareas(rol):
    # Crear la ventana principal
    root = tk.Tk()
    root.title('Tareas')
    root.geometry('950x500+300+200')
    root.configure(bg="#f4f4f9")
    root.resizable(False, False)

    menu_lateral = tk.Frame(root, bg="#333", width=150)
    menu_lateral.pack(side="left", fill="y")
    frame_central = Frame(root, bg="#fff")
    frame_central.pack(side="right", expand=True, fill="both")


    # Crear las opciones del menú
    if rol == "A":
            opciones_menu = [
            {"texto": "Recompensas", "icono": "★"},
            {"texto": "Usuarios", "icono": "👤"},
            {"texto": "Tareas", "icono": "📝"},
            {"texto": "Inventario", "icono": "📦"},
            {"texto": "Recetas", "icono": "🗒️"},
            {"texto": "Punto ventas", "icono": "🗒️"},
            {"texto": "Cerrar sesión", "icono": "🗒️"}
            ]
    else:
        opciones_menu = [
        {"texto": "Recompensas", "icono": "★"},
        {"texto": "Tareas", "icono": "📝"},
        {"texto": "Inventario", "icono": "📦"},
        {"texto": "Recetas", "icono": "🗒️"},
        {"texto": "Punto ventas", "icono": "🗒️"},
        {"texto": "Cerrar sesión", "icono": "🗒️"}
        ]

    # Crear los botones en el menú lateral
    for opcion in opciones_menu:
        frame_opcion = tk.Frame(menu_lateral, bg="#333")
        frame_opcion.pack(fill="x", pady=1)

        etiqueta = tk.Label(frame_opcion, text=f"{opcion['icono']} {opcion['texto']}", anchor="w", padx=10, bg="#333", fg="#fff", font=('Helvetica', 10, 'bold'))
        etiqueta.pack(fill="x")

        if opcion.get("notificacion"):
            notificacion = tk.Label(frame_opcion, text="●", fg="red", bg="#333", anchor="e")
            notificacion.pack(side="right", padx=5)

        ventana = root
        etiqueta.bind("<Button-1>", lambda e, texto=opcion['texto']: destruir(texto, ventana,rol))
    root.mainloop()

def destruir(texto,root,rol) :
    root.destroy()
    seleccionar_opcion(texto,rol)
    print("se elimino")
    
# Ejecutar el bucle principal de la aplicación

abrir_tareas("A")
"""
import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox



def cargar_tareas(tabla):
    from conexion_bd import conexion
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, acciones, fecha_limite, encargado FROM tarea")

    tabla.delete(*tabla.get_children())
    
    for (id, nombre, acciones, fecha_limite, encargado) in cursor:
        tabla.insert("", "end", values=(id, nombre, acciones, fecha_limite, encargado))

    cursor.close()
    conn.close()

def abrir_tareas(rol):
    root = tk.Tk()
    root.iconbitmap("tareas.ico")
    root.title('Tareas')
    root.geometry('950x500+300+200')
    root.configure(bg="#f4f4f9")
    root.resizable(False, False)

    menu_lateral = tk.Frame(root, bg="#333", width=150)
    menu_lateral.pack(side="left", fill="y")
    frame_central = tk.Frame(root, bg="#fff")
    frame_central.pack(side="right", expand=True, fill="both")

    # Crear las opciones del menú
    if rol == "A":
            opciones_menu = [
            {"texto": "Recompensas", "icono": "★"},
            {"texto": "Usuarios", "icono": "👤"},
            {"texto": "Tareas", "icono": "📝"},
            {"texto": "Inventario", "icono": "📦"},
            {"texto": "Recetas", "icono": "🗒️"},
            {"texto": "Punto ventas", "icono": "🗒️"},
            {"texto": "Cerrar sesión", "icono": "🗒️"}
            ]
    else:
        opciones_menu = [
        {"texto": "Recompensas", "icono": "★"},
        {"texto": "Tareas", "icono": "📝"},
        {"texto": "Inventario", "icono": "📦"},
        {"texto": "Recetas", "icono": "🗒️"},
        {"texto": "Punto ventas", "icono": "🗒️"},
        {"texto": "Cerrar sesión", "icono": "🗒️"}
        ]
    for opcion in opciones_menu:
        frame_opcion = tk.Frame(menu_lateral, bg="#333")
        frame_opcion.pack(fill="x", pady=1)

        etiqueta = tk.Label(frame_opcion, text=f"{opcion['icono']} {opcion['texto']}", anchor="w", padx=10, bg="#333", fg="#fff", font=('Helvetica', 10, 'bold'))
        etiqueta.pack(fill="x")

        if opcion.get("notificacion"):
            notificacion = tk.Label(frame_opcion, text="●", fg="red", bg="#333", anchor="e")
            notificacion.pack(side="right", padx=5)

        ventana = root
        etiqueta.bind("<Button-1>", lambda e, texto=opcion['texto']: destruir(texto, ventana,rol))

    headers = ["ID", "Nombre", "Acciones", "Fecha Límite", "Encargado"]
    tabla = ttk.Treeview(frame_central, columns=headers, show="headings")
    for header in headers:
        tabla.heading(header, text=header)
        tabla.column(header, anchor="center", width=100)
    tabla.pack(pady=20, padx=10, fill="both", expand=True)

    cargar_tareas(tabla)

    botones_frame = tk.Frame(frame_central, bg="#fff")
    botones_frame.pack(pady=10)

    btn_agregar = tk.Button(botones_frame, text="Agregar Tarea", command=lambda: agregar_tarea(tabla))
    btn_agregar.grid(row=0, column=0, padx=5)

    btn_modificar = tk.Button(botones_frame, text="Modificar Tarea", command=lambda: modificar_tarea(tabla))
    btn_modificar.grid(row=0, column=1, padx=5)

    btn_eliminar = tk.Button(botones_frame, text="Eliminar Tarea", command=lambda: eliminar_tarea(tabla))
    btn_eliminar.grid(row=0, column=2, padx=5)

    root.mainloop()

def agregar_tarea(tabla):
    """
    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Modificar Tarea")
    ventana_agregar.geometry("400x300")
    campos = [ "Nombre", "Acciones", "Fecha Límite", "Encargado"]
    entradas = {}
    for idx, campo in enumerate(campos):
        lbl = tk.Label(ventana_agregar, text=campo)
        lbl.grid(row=idx, column=0, padx=10, pady=5, sticky="e")
        entrada = tk.Entry(ventana_agregar, width=30)
        entrada.grid(row=idx, column=1, padx=10, pady=5)
        entradas[campo] = entrada


    btn_confirmar = tk.Button(ventana_agregar, text="AGREGAR", command=lambda: confirmar_agregar( entradas, tabla,ventana_agregar))
    btn_confirmar.grid(row=len(campos), columnspan=2, pady=10)"""
    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Agregar Tarea")
    ventana_agregar.geometry("350x250")
    ventana_agregar.configure(bg="#f7f2f2")  # Fondo claro
    
    # Colores y estilo
    color_fondo = "#f7f2f2"  # Fondo de la ventana
    color_label = "#333"  # Azul para los labels
    color_boton = "#e06666"  # Rojo para el botón
    color_borde = "#ffd966"  # Amarillo para el borde del marco

    # Marco para organización estética
    marco = tk.Frame(ventana_agregar, bg=color_fondo, bd=2, relief="groove", padx=10, pady=10)
    marco.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Crear etiquetas y entradas
    campos = ["Nombre", "Acciones", "Fecha Límite", "Encargado"]
    entradas = {}
    for idx, campo in enumerate(campos):
        lbl = tk.Label(marco, text=campo, bg=color_fondo, fg=color_label, font=("Arial", 10, "bold"))
        lbl.grid(row=idx, column=0, padx=10, pady=5, sticky="e")
        entrada = tk.Entry(marco, width=30)
        entrada.grid(row=idx, column=1, padx=10, pady=5)
        entradas[campo] = entrada

    # Botón de confirmación
    btn_confirmar = tk.Button(
        marco, text="AGREGAR", bg=color_boton, fg="white", font=("Arial", 12, "bold"),
        command=lambda: confirmar_agregar(entradas, tabla, ventana_agregar)
    )
    btn_confirmar.grid(row=len(campos), columnspan=2, pady=10)


def modificar_tarea(tabla):
    """
    selected_item = tabla.selection()
    if not selected_item:
        messagebox.showwarning("Selección vacía", "Selecciona una tarea para modificar")
        return

    item_values = tabla.item(selected_item)['values']
    if not item_values:
        messagebox.showwarning("Datos vacíos", "No se encontraron datos para modificar.")
        return

    ventana_editar = tk.Toplevel()
    ventana_editar.title("Modificar Tarea")
    ventana_editar.geometry("400x300")

    campos = ["ID", "Nombre", "Acciones", "Fecha Límite", "Encargado"]
    entradas = {}

    for idx, campo in enumerate(campos):
        lbl = tk.Label(ventana_editar, text=campo)
        lbl.grid(row=idx, column=0, padx=10, pady=5, sticky="e")
        entrada = tk.Entry(ventana_editar, width=30)
        entrada.grid(row=idx, column=1, padx=10, pady=5)
        entradas[campo] = entrada
        if campo == "ID":
            entrada.insert(0, item_values[0])
            entrada.config(state='readonly')
        else:
            entrada.insert(0, item_values[idx])

    btn_confirmar = tk.Button(ventana_editar, text="Modificar", command=lambda: confirmar_modificacion(entradas, tabla,ventana_editar))
    btn_confirmar.grid(row=len(campos), columnspan=2, pady=10)"""
    selected_item = tabla.selection()
    if not selected_item:
        messagebox.showwarning("Selección vacía", "Selecciona una tarea para modificar")
        return

    item_values = tabla.item(selected_item)['values']
    if not item_values:
        messagebox.showwarning("Datos vacíos", "No se encontraron datos para modificar.")
        return

    # Configuración de la ventana de edición
    ventana_editar = tk.Toplevel()
    ventana_editar.title("Modificar Tarea")
    ventana_editar.geometry("350x250")
    ventana_editar.configure(bg="#f7f2f2")  # Fondo claro

    # Colores y estilo
    color_fondo = "#f7f2f2"
    color_label = "#333"  # Azul para los labels
    color_boton = "#e06666"  # Rojo para el botón
    color_borde = "#ffd966"  # Amarillo para el borde del marco

    # Marco para organización estética
    marco = tk.Frame(ventana_editar, bg=color_fondo, bd=2, relief="groove", padx=10, pady=10)
    marco.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Crear etiquetas y entradas
    campos = ["ID", "Nombre", "Acciones", "Fecha Límite", "Encargado"]
    entradas = {}

    for idx, campo in enumerate(campos):
        lbl = tk.Label(marco, text=campo, bg=color_fondo, fg=color_label, font=("Arial", 10, "bold"))
        lbl.grid(row=idx, column=0, padx=10, pady=5, sticky="e")
        
        entrada = tk.Entry(marco, width=30)
        entrada.grid(row=idx, column=1, padx=10, pady=5)
        entradas[campo] = entrada
        
        # Llenar los campos con valores existentes y hacer el campo ID de solo lectura
        if campo == "ID":
            entrada.insert(0, item_values[0])
            entrada.config(state='readonly')
        else:
            entrada.insert(0, item_values[idx])

    # Botón de confirmación
    btn_confirmar = tk.Button(
        marco, text="Modificar", bg=color_boton, fg="white", font=("Arial", 12, "bold"),
        command=lambda: confirmar_modificacion(item_values[0],entradas, tabla, ventana_editar)
    )
    btn_confirmar.grid(row=len(campos), columnspan=2, pady=10)
    
def confirmar_agregar(entradas,tabla,ventana):
    from conexion_bd import conexion
    datos = {campo: entradas[campo].get() for campo in entradas}
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tarea (nombre,acciones,fecha_limite,encargado) VALUES(%s,%s,%s,%s)
    """, (datos['Nombre'], datos['Acciones'], datos['Fecha Límite'], datos['Encargado']))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Éxito", "Tarea agregada correctamente")
    ventana.destroy()
    cargar_tareas(tabla)

def confirmar_modificacion( tarea_id,entradas, tabla,ventana):
    from conexion_bd import conexion
    datos = {campo: entradas[campo].get() for campo in entradas}
    print(f"Modificando tarea {tarea_id} con datos:", datos)

    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tarea
        SET nombre = %s, acciones = %s, fecha_limite = %s, encargado = %s
        WHERE id = %s
    """, (datos['Nombre'], datos['Acciones'], datos['Fecha Límite'], datos['Encargado'], tarea_id))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Éxito", "Tarea modificada correctamente")
    ventana.destroy()
    cargar_tareas(tabla)

def eliminar_tarea(tabla):
    from conexion_bd import conexion
    selected_item = tabla.selection()
    if not selected_item:
        messagebox.showwarning("Selección vacía", "Selecciona una tarea para eliminar")
        return

    item_values = tabla.item(selected_item)['values']
    if not item_values:
        messagebox.showwarning("Datos vacíos", "No se encontraron datos para eliminar.")
        return

    confirmar = messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de que deseas eliminar la tarea '{item_values[1]}'?")
    if confirmar:
        conn = conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tarea WHERE id = %s", (item_values[0],))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Éxito", "Tarea eliminada correctamente")
        cargar_tareas(tabla)

def destruir(texto,root,rol) :
    from funcionalidad import seleccionar_opcion
    root.destroy()
    seleccionar_opcion(texto,rol)
    print("se elimino")
# Ejecuta la función de abrir_tareas con un rol de ejemplo

