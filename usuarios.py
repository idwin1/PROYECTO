"""import time
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # Importamos Pillow
from funcionalidad import seleccionar_opcion

import tkinter as tk
from tkinter import ttk
def cargarDatos():
    from conexion_bd import conexion
    conn = conexion()
    cursor = conn.cursor()
    
    # Consulta para obtener los datos
    cursor.execute("SELECT id, usuario, contrasena, rol FROM usuarios")
    resultados = cursor.fetchall()

    # Limpiar la tabla antes de insertar nuevos datos
    for row in tree.get_children():
        tree.delete(row)

    # Insertar cada fila en el Treeview
    for fila in resultados:
        tree.insert("", "end", values=fila)

    # Cerrar la conexión
    cursor.close()
    conn.close()

def abrir_usuarios():   
    global tree 
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Usuarios")
    root.geometry("800x600")

    # Crear el marco para el menú lateral
    menu_frame = tk.Frame(root, bg="#333333", width=150)
    menu_frame.pack(side="left", fill="y")

    # Opciones del menú lateral
    menu_options = ["Recompensas", "Reportes", "Estadísticas", "Usuarios", "Tareas", "Inventario", "Recetas"]
    for option in menu_options:
        button = tk.Button(menu_frame, text=option, bg="#333333", fg="white", bd=0, font=("Arial", 10), anchor="w")
        button.pack(fill="x", padx=10, pady=5)

        ventana = root
        # El truco es capturar el valor actual de 'option' usando un parámetro por defecto en el lambda
        button.bind("<Button-1>", lambda e, texto=option: destruir(texto,ventana))


    # Crear el marco principal para la tabla y los botones
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(side="right", fill="both", expand=True)

    # Título
    title_label = tk.Label(main_frame, text="usuarios", bg="white", font=("Arial", 14))
    title_label.pack(pady=10)

    # Buscar receta
    search_frame = tk.Frame(main_frame, bg="white")
    search_frame.pack(pady=5)

    search_label = tk.Label(search_frame, text="Buscar Receta:", bg="white", font=("Arial", 10))
    search_label.grid(row=0, column=0)

    search_entry = tk.Entry(search_frame, width=30)
    search_entry.grid(row=0, column=1, padx=5)

    search_button = tk.Button(search_frame, text="Buscar", bg="#4BA3C7", fg="white")
    search_button.grid(row=0, column=2, padx=5)

    # Crear una tabla usando Treeview
    columns = ("ID", "Usuario", "Contraseña", "Rol")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=8)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    
    tree.pack(pady=20)

    # Crear botones de acción
    button_frame = tk.Frame(main_frame, bg="white")
    button_frame.pack(pady=10)

    add_button = tk.Button(button_frame, text="AGREGAR USUARIO", bg="#28A745", fg="white", font=("Arial", 10), width=20)
    add_button.grid(row=0, column=0, padx=5)

    update_button = tk.Button(button_frame, text="ACTUALIZAR USUARIO", bg="#FFC107", fg="black", font=("Arial", 10), width=20)
    update_button.grid(row=0, column=1, padx=5)

    delete_button = tk.Button(button_frame, text="ELIMINAR USUARIO", bg="#DC3545", fg="white", font=("Arial", 10), width=20)
    delete_button.grid(row=0, column=2, padx=5)
    cargarDatos()

    # Ejecutar la aplicación
    root.mainloop()

def destruir(texto,root) :
    from funcionalidad import seleccionar_opcion
    root.destroy()
    # Añadir más opciones según el menú
    print("texto") 
    time.sleep(1)
    seleccionar_opcion(texto)
"""

import time
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # Importamos Pillow
from funcionalidad import seleccionar_opcion
import tkinter as tk
from tkinter import ttk

def cargarDatos():
    from conexion_bd import conexion
    conn = conexion()
    cursor = conn.cursor()
    
    # Consulta para obtener los datos
    cursor.execute("SELECT id, usuario, contrasena, rol FROM usuarios")
    resultados = cursor.fetchall()

    # Limpiar la tabla antes de insertar nuevos datos
    for row in tree.get_children():
        tree.delete(row)

    # Insertar cada fila en el Treeview
    for fila in resultados:
        tree.insert("", "end", values=fila)

    # Cerrar la conexión
    cursor.close()
    conn.close()

def abrir_ventana_edicion(accion):
    # Obtener el usuario seleccionado
    selected_item = tree.focus()
    if not selected_item and accion != "Agregar":
        messagebox.showwarning("Advertencia", "Selecciona un usuario para " + accion.lower())
        return

    # Crear una nueva ventana
    ventana_edicion = tk.Toplevel()
    ventana_edicion.title(f"{accion} Usuario")
    ventana_edicion.geometry("400x300")

    # Crear los campos de entrada
    Label(ventana_edicion, text="ID:").grid(row=0, column=0, padx=10, pady=10)
    id_entry = Entry(ventana_edicion)
    id_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(ventana_edicion, text="Usuario:").grid(row=1, column=0, padx=10, pady=10)
    usuario_entry = Entry(ventana_edicion)
    usuario_entry.grid(row=1, column=1, padx=10, pady=10)

    Label(ventana_edicion, text="Contraseña:").grid(row=2, column=0, padx=10, pady=10)
    contrasena_entry = Entry(ventana_edicion)
    contrasena_entry.grid(row=2, column=1, padx=10, pady=10)

    Label(ventana_edicion, text="Rol:").grid(row=3, column=0, padx=10, pady=10)
    rol_entry = Entry(ventana_edicion)
    rol_entry.grid(row=3, column=1, padx=10, pady=10)
    
    # Si no es "Agregar", cargar los datos del usuario seleccionado
    if accion != "Agregar":
        datos = tree.item(selected_item, "values")
        id_entry.insert(0, datos[0])
        usuario_entry.insert(0, datos[1])
        contrasena_entry.insert(0, datos[2])
        rol_entry.insert(0, datos[3])
        
        # Si es "Actualizar" o "Eliminar", bloquear el campo de ID
        id_entry.config(state="readonly")
        if accion == "Eliminar":
            usuario_entry.config(state="readonly")
            contrasena_entry.config(state="readonly")
            rol_entry.config(state="readonly")

    # Botón de acción en la ventana de edición
    def realizar_accion():
        from conexion_bd import conexion
        conn = conexion()
        cursor = conn.cursor()

        if accion == "Agregar":
            # Obtener datos de los campos de entrada

            nuevo_usuario = usuario_entry.get()
            nueva_contrasena = contrasena_entry.get()
            nuevo_rol = rol_entry.get()

            # Consulta para agregar un nuevo usuario
            cursor.execute("INSERT INTO usuarios (usuario, contrasena, rol) VALUES (%s, %s, %s)",
                           (nuevo_usuario, nueva_contrasena, nuevo_rol))
            conn.commit()
            messagebox.showinfo("Éxito", "Usuario agregado correctamente.")

        elif accion == "Actualizar":
            # Obtener datos de los campos de entrada
            id_usuario = id_entry.get()
            usuario_actualizado = usuario_entry.get()
            contrasena_actualizada = contrasena_entry.get()
            rol_actualizado = rol_entry.get()

            # Consulta para actualizar el usuario seleccionado
            cursor.execute("UPDATE usuarios SET usuario=%s, contrasena=%s, rol=%s WHERE id=%s",
                           (usuario_actualizado, contrasena_actualizada, rol_actualizado, id_usuario))
            conn.commit()
            cargarDatos()
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")

        elif accion == "Eliminar":
            # Obtener el ID del usuario a eliminar
            id_usuario = id_entry.get()

            # Consulta para eliminar el usuario seleccionado
            cursor.execute("DELETE FROM usuarios WHERE id=%s", (id_usuario,))
            conn.commit()
            cargarDatos()
            messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")

        # Cerrar la conexión y destruir la ventana de edición
        cursor.close()
        conn.close()
        cargarDatos()  # Recargar los datos en el Treeview
        ventana_edicion.destroy()


    # Botón para confirmar la acción
    confirmar_button = tk.Button(ventana_edicion, text=accion, command=realizar_accion)
    confirmar_button.grid(row=4, column=0, columnspan=2, pady=20)

def abrir_usuarios(rol):   
    global tree 
    global root
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Usuarios")
    root.geometry("800x600")

    # Crear el marco para el menú lateral
    menu_frame = tk.Frame(root, bg="#333333", width=150)
    menu_frame.pack(side="left", fill="y")

    # Opciones del menú lateral
    if rol == "A":
        menu_options = ["Recompensas", "Usuarios", "Tareas", "Inventario", "Recetas","Punto ventas","Cerrar secion"]
    else:
        menu_options = ["Recompensas", "Tareas", "Inventario", "Recetas","Punto ventas","Cerrar secion"]

    for option in menu_options:
        button = tk.Button(menu_frame, text=option, bg="#333333", fg="white", bd=0, font=("Arial", 10), anchor="w")
        button.pack(fill="x", padx=10, pady=5)
        button.bind("<Button-1>", lambda e, texto=option: destruir(texto, root,rol))

    # Crear el marco principal para la tabla y los botones
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(side="right", fill="both", expand=True)

    # Título
    title_label = tk.Label(main_frame, text="usuarios", bg="white", font=("Arial", 14))
    title_label.pack(pady=10)

    # Crear la tabla usando Treeview
    global tree
    columns = ("ID", "Usuario", "Contraseña", "Rol")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=8)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    tree.pack(pady=20)

    # Crear botones de acción
    button_frame = tk.Frame(main_frame, bg="white")
    button_frame.pack(pady=10)

    add_button = tk.Button(button_frame, text="AGREGAR USUARIO", bg="#28A745", fg="white", font=("Arial", 10), width=20, command=lambda: abrir_ventana_edicion("Agregar"))
    add_button.grid(row=0, column=0, padx=5)

    update_button = tk.Button(button_frame, text="ACTUALIZAR USUARIO", bg="#FFC107", fg="black", font=("Arial", 10), width=20, command=lambda: abrir_ventana_edicion("Actualizar"))
    update_button.grid(row=0, column=1, padx=5)

    delete_button = tk.Button(button_frame, text="ELIMINAR USUARIO", bg="#DC3545", fg="white", font=("Arial", 10), width=20, command=lambda: abrir_ventana_edicion("Eliminar"))
    delete_button.grid(row=0, column=2, padx=5)

    cargarDatos()
    root.mainloop()

def destruir(texto, root,rol):
    from funcionalidad import seleccionar_opcion
    root.destroy()
    print("texto")
    print(rol)
    time.sleep(1)
    seleccionar_opcion(texto,rol)

