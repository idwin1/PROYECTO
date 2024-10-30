from tkinter import *
from tkinter import messagebox, ttk
from tkinter import simpledialog
import mysql.connector
import time
import tkinter as tk
from tkinter import ttk
# Función para mostrar la interfaz de recetas en el área central
from tkinter import *
from tkinter import messagebox, ttk
from tkinter import simpledialog
import mysql.connector
import time
import tkinter as tk

def mostrar_recetas(frame_central):
    for widget in frame_central.winfo_children():
        widget.destroy()

    # Configuración de estilo
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview", foreground="black", background="#F9F9F9")
    style.configure("Treeview.Heading", font=('Helvetica', 12, 'bold'), background="#4CAF50", foreground="white")
    style.map("Treeview", background=[('selected', '#AED6F1')])

    Label(frame_central, text="Recetas", font=('Helvetica', 18, 'bold'), fg="#333", bg="#fff").grid(row=0, column=0, columnspan=4, pady=10)

    tree = ttk.Treeview(frame_central, columns=("ID", "Nombre", "Ingredientes", "Elaboración"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Ingredientes", text="Ingredientes")
    tree.heading("Elaboración", text="Elaboración")
    tree.column("ID", width=80)
    tree.column("Nombre", width=180)
    tree.column("Ingredientes", width=300)
    tree.column("Elaboración", width=250)
    tree.grid(row=2, column=0, columnspan=4, padx=20)

    Label(frame_central, text="Buscar Receta:", bg="#fff").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_busqueda = Entry(frame_central, bg="#F1F1F1", font=('Helvetica', 12))
    entry_busqueda.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    Button(frame_central, text="Buscar", command=lambda: buscar_receta(tree, entry_busqueda.get()), bg='#5DADE2', font=('Helvetica', 12), fg="white").grid(row=1, column=2, padx=10, sticky="w")

    frame_botones = Frame(frame_central, bg="#fff")
    frame_botones.grid(row=3, column=0, columnspan=4, pady=10)

    Button(frame_botones, text="Agregar Receta", command=lambda: abrir_ventana_agregar(tree), bg='#58D68D', font=('Helvetica', 12), fg="white", padx=5, pady=5).grid(row=0, column=0, padx=5)
    Button(frame_botones, text="Modificar Receta", command=lambda: abrir_ventana_modificar(tree), bg='#F7DC6F', font=('Helvetica', 12), fg="black", padx=5, pady=5).grid(row=0, column=1, padx=5)
    Button(frame_botones, text="Eliminar Receta", command=lambda: eliminar_receta(tree), bg='#E74C3C', font=('Helvetica', 12), fg="white", padx=5, pady=5).grid(row=0, column=2, padx=5)

    actualizar_tabla(tree)

def abrir_recetas():
    global root
    root = tk.Tk()
    root.title('Recetas')
    root.geometry('950x500+300+200')
    root.configure(bg="#f4f4f9")
    root.resizable(False, False)

    menu_lateral = tk.Frame(root, bg="#333", width=150)
    menu_lateral.pack(side="left", fill="y")
    frame_central = Frame(root, bg="#fff")
    frame_central.pack(side="right", expand=True, fill="both")

    opciones_menu = [
        {"texto": "Recompensas", "icono": "★"},
        {"texto": "Reportes", "icono": "📊"},
        {"texto": "Estadísticas", "icono": "📈", "notificacion": True},
        {"texto": "Usuarios", "icono": "👤"},
        {"texto": "Tareas", "icono": "📝"},
        {"texto": "Inventario", "icono": "📦"}
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
        etiqueta.bind("<Button-1>", lambda e, texto=opcion['texto']: destruir(texto, ventana))

    menu_inferior = Frame(root, bg="#333", height=50)
    menu_inferior.pack(side="bottom", fill="x")

    opciones_inferiores = ["Ver Recetas"]

    for texto in opciones_inferiores:
        boton = Button(menu_inferior, text=texto, padx=10, pady=5, bg="#5DADE2", fg="white", font=('Helvetica', 12), borderwidth=0,
                       command=lambda t=texto: mostrar_recetas(frame_central))
        boton.pack(side="left", padx=20)

    root.mainloop()


"""
def mostrar_recetas(frame_central):
    # Limpiar el contenido actual del área central
    for widget in frame_central.winfo_children():
        widget.destroy()

    # Aplicar un estilo
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview", foreground="black", background="white")
    style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
    style.map("Treeview", background=[('selected', 'lightblue')])

    # Configurar la tabla de recetas
    Label(frame_central, text="Recetas", font=('Arial', 16)).grid(row=0, column=0, columnspan=4, pady=10)

    tree = ttk.Treeview(frame_central, columns=("ID", "Nombre", "Ingredientes", "Elaboración"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Ingredientes", text="Ingredientes")
    tree.heading("Elaboración", text="Elaboración")
    tree.column("ID", width=100)
    tree.column("Nombre", width=200)
    tree.column("Ingredientes", width=200)
    tree.column("Elaboración", width=200)
    tree.grid(row=2, column=0, columnspan=4, padx=20)

    # Crear barra de búsqueda
    Label(frame_central, text="Buscar Receta:").grid(row=1, column=0, padx=10, pady=10)
    entry_busqueda = Entry(frame_central)
    entry_busqueda.grid(row=1, column=1, padx=10, pady=10)

    Button(frame_central, text="Buscar", command=lambda: buscar_receta(tree, entry_busqueda.get()), bg='lightblue', font=('Arial', 12)).grid(row=1, column=2, padx=10)

    # Botones para agregar, modificar y eliminar recetas
    frame_botones = Frame(frame_central)
    frame_botones.grid(row=3, column=0, columnspan=4, pady=10)

    Button(frame_botones, text="Agregar Receta", command=lambda: abrir_ventana_agregar(tree), bg='lightgreen', font=('Arial', 12)).grid(row=0, column=0, padx=5)
    Button(frame_botones, text="Modificar Receta", command=lambda: abrir_ventana_modificar(tree), bg='lightyellow', font=('Arial', 12)).grid(row=0, column=1, padx=5)
    Button(frame_botones, text="Eliminar Receta", command=lambda: eliminar_receta(tree), bg='lightcoral', font=('Arial', 12)).grid(row=0, column=2, padx=5)

    # Actualizar la tabla de recetas al inicio
    actualizar_tabla(tree)
"""
# Función para buscar recetas
def buscar_receta(tree, termino_busqueda):
    from conexion_bd import conexion
    # Limpiar la tabla existente
    for row in tree.get_children():
        tree.delete(row)

    # Conectar a la base de datos y buscar recetas
    try:
        conn = conexion()
        cursor = conn.cursor()

        query = "SELECT r.ID, r.Nombre, GROUP_CONCAT(CONCAT(i.cantidad, ' ', i.unidad, ' ', i.ingrediente) SEPARATOR ', ') AS Ingredientes,  r.Elaboracion FROM receta r JOIN ingredientes i ON r.ID = i.receta_id WHERE r.Nombre LIKE %s OR r.ID LIKE %s GROUP BY r.ID, r.Nombre, r.Elaboracion;"
        termino = f"%{termino_busqueda}%"
        cursor.execute(query, (termino, termino))
        recetas = cursor.fetchall()

        for receta in recetas:
            tree.insert("", END, values=receta)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al buscar recetas: {err}")
    finally:
        cursor.close()
        conn.close()

# Función para actualizar la tabla de recetas
    # Conectar a la base de datos y obtener las recetas
def actualizar_tabla(tree):
    from conexion_bd import conexion     
    for row in tree.get_children():
        tree.delete(row)
    try:
        conn = conexion()
        cursor = conn.cursor()

        query = "SELECT r.ID, r.Nombre, GROUP_CONCAT(CONCAT(i.cantidad, ' ', i.unidad, ' ', i.ingrediente) SEPARATOR ', ') AS Ingredientes, r.Elaboracion FROM receta r JOIN ingredientes i ON r.ID = i.receta_id GROUP BY r.ID, r.Nombre, r.Elaboracion;"
        cursor.execute(query)
        recetas = cursor.fetchall()

        for receta in recetas:
            tree.insert("", END, values=receta)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al obtener recetas: {err}")
    finally:
        cursor.close()
        conn.close()  

# Función para abrir la ventana para agregar una receta
<<<<<<< HEAD
=======





>>>>>>> 1751676cfbe521d9b9f09014b421c3233aa83f25

def abrir_ventana_agregar(tree):
    global root  # Asegúrate de que root está disponible
    ventana_agregar = Toplevel(root)
    ventana_agregar.title("Agregar Receta")

    Label(ventana_agregar, text="Nombre de la Receta:").grid(row=0, column=0)
    entry_nombre = Entry(ventana_agregar)
    entry_nombre.grid(row=0, column=1)

    # Sección para los ingredientes
    Label(ventana_agregar, text="Ingredientes:").grid(row=1, column=0, columnspan=2)

    # Frame que contendrá los ingredientes y sus etiquetas
    ingredientes_frame = Frame(ventana_agregar)
    ingredientes_frame.grid(row=2, column=0, columnspan=2)

    # Encabezados para los campos de ingredientes
    Label(ingredientes_frame, text="Nombre del Ingrediente").grid(row=0, column=0)
    Label(ingredientes_frame, text="Cantidad").grid(row=0, column=1)
    Label(ingredientes_frame, text="Unidad").grid(row=0, column=2)

    # Lista para almacenar los campos de ingredientes
    ingredientes_entries = []

    # Función para agregar una nueva fila de ingredientes
    def agregar_ingrediente():
        row = len(ingredientes_entries) + 1  # Empieza en la fila siguiente a las etiquetas
        entry_nombre_ingrediente = Entry(ingredientes_frame)
        entry_nombre_ingrediente.grid(row=row, column=0)
        
        entry_cantidad = Entry(ingredientes_frame)
        entry_cantidad.grid(row=row, column=1)
        
        entry_unidad = Entry(ingredientes_frame)
        entry_unidad.grid(row=row, column=2)
        
        # Añadir los campos a la lista
        ingredientes_entries.append((entry_nombre_ingrediente, entry_cantidad, entry_unidad))

    # Agregar la primera fila de ingredientes
    agregar_ingrediente()

    # Botón para agregar más filas de ingredientes
    Button(ventana_agregar, text="Agregar Ingrediente", command=agregar_ingrediente).grid(row=3, columnspan=2)

    # Sección para la elaboración
    Label(ventana_agregar, text="Elaboración:").grid(row=4, column=0)
    entry_elaboracion = Entry(ventana_agregar)
    entry_elaboracion.grid(row=4, column=1)

    # Función para recopilar los datos y agregarlos al árbol
    def agregar_datos():
        nombre_receta = entry_nombre.get()
        elaboracion = entry_elaboracion.get()
        ingredientes = [(entry[0].get(), entry[1].get(), entry[2].get()) for entry in ingredientes_entries]
        agregar_receta(nombre_receta, ingredientes, elaboracion, tree, ventana_agregar)
        print("finalizar")

    # Botón para agregar la receta
    Button(ventana_agregar, text="Agregar", command=agregar_datos).grid(row=5, columnspan=2)

# Función para agregar una receta
def agregar_receta(nombre_receta, ingredientes, elaboracion, tree, ventana_agregar):
    from conexion_bd import conexion
    print("si entra")
    try:
        conn = conexion()
        cursor = conn.cursor()

        # Insertar la receta en la tabla `receta`
        query = "INSERT INTO receta (Nombre, Elaboracion) VALUES (%s, %s)"
        cursor.execute(query, (nombre_receta, elaboracion))
        conn.commit()

        # Obtener el ID de la receta insertada
        receta_id = cursor.lastrowid

        # Insertar cada ingrediente en la tabla `ingredientes`
        query_ingrediente = "INSERT INTO ingredientes (receta_id, ingrediente, cantidad, unidad) VALUES (%s, %s, %s, %s)"
        for ingrediente in ingredientes:
            cursor.execute(query_ingrediente, (receta_id, ingrediente[0], ingrediente[1], ingrediente[2]))

        # Confirmar los cambios
        conn.commit()

        messagebox.showinfo("Éxito", "Receta y ingredientes agregados correctamente.")
        actualizar_tabla(tree)  # Función para actualizar la tabla con los nuevos datos
        ventana_agregar.destroy()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al agregar la receta: {err}")
    finally:
        cursor.close()
        conn.close()

def abrir_ventana_modificar(tree):
    global root
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione una receta para modificar.")
        return

    id_receta = tree.item(selected_item, 'values')[0]
    nombre_receta = tree.item(selected_item, 'values')[1]
    elaboracion = tree.item(selected_item, 'values')[3]

    ventana_modificar = Toplevel(root)
    ventana_modificar.title("Modificar Receta")

    # Campos para la receta
    Label(ventana_modificar, text="Nombre de la Receta:").grid(row=0, column=0)
    entry_nombre = Entry(ventana_modificar)
    entry_nombre.insert(0, nombre_receta)
    entry_nombre.grid(row=0, column=1)

    # Sección para los ingredientes
    Label(ventana_modificar, text="Ingredientes:").grid(row=1, column=0, columnspan=2)

    ingredientes_frame = Frame(ventana_modificar)
    ingredientes_frame.grid(row=2, column=0, columnspan=2)

    Label(ingredientes_frame, text="Nombre del Ingrediente").grid(row=0, column=0)
    Label(ingredientes_frame, text="Cantidad").grid(row=0, column=1)
    Label(ingredientes_frame, text="Unidad").grid(row=0, column=2)

    # Lista para almacenar las entradas de ingredientes
    ingredientes_entries = []

    # Consulta para obtener los ingredientes de la receta
    from conexion_bd import conexion
    conn = conexion()
    cursor = conn.cursor()

    query = "SELECT ingrediente, cantidad, unidad FROM ingredientes WHERE receta_id = %s"
    cursor.execute(query, (id_receta,))
    ingredientes = cursor.fetchall()

    # Crear entradas para cada ingrediente
    for i, (nombre, cantidad, unidad) in enumerate(ingredientes, start=1):
        entry_nombre_ingrediente = Entry(ingredientes_frame)
        entry_nombre_ingrediente.insert(0, nombre)
        entry_nombre_ingrediente.grid(row=i, column=0)

        entry_cantidad = Entry(ingredientes_frame)
        entry_cantidad.insert(0, cantidad)
        entry_cantidad.grid(row=i, column=1)

        entry_unidad = Entry(ingredientes_frame)
        entry_unidad.insert(0, unidad)
        entry_unidad.grid(row=i, column=2)

        ingredientes_entries.append((entry_nombre_ingrediente, entry_cantidad, entry_unidad))

    cursor.close()
    conn.close()

    # Sección para la elaboración
    Label(ventana_modificar, text="Elaboración:").grid(row=3, column=0)
    entry_elaboracion = Entry(ventana_modificar)
    entry_elaboracion.insert(0, elaboracion)
    entry_elaboracion.grid(row=3, column=1)

    # Función para actualizar la receta en la base de datos
    def modificar_datos():
        nuevo_nombre = entry_nombre.get()
        nueva_elaboracion = entry_elaboracion.get()
        nuevos_ingredientes = [(entry[0].get(), entry[1].get(), entry[2].get()) for entry in ingredientes_entries]

        modificar_receta(id_receta, nuevo_nombre, nuevos_ingredientes, nueva_elaboracion, tree)
        ventana_modificar.destroy()

    Button(ventana_modificar, text="Modificar", command=modificar_datos).grid(row=4, columnspan=2)

# Función para modificar receta e ingredientes en la base de datos
def modificar_receta(id_receta, nombre_receta, ingredientes, elaboracion, tree):
    from conexion_bd import conexion
    try:
        conn = conexion()
        cursor = conn.cursor()

        # Actualizar la receta
        query = "UPDATE receta SET Nombre = %s, Elaboracion = %s WHERE id = %s"
        cursor.execute(query, (nombre_receta, elaboracion, id_receta))

        # Actualizar o insertar los ingredientes asociados
        query_ingrediente = "UPDATE ingredientes SET ingrediente = %s, cantidad = %s, unidad = %s WHERE receta_id = %s AND ingrediente = %s"
        for ingrediente in ingredientes:
            cursor.execute(query_ingrediente, (ingrediente[0], ingrediente[1], ingrediente[2], id_receta, ingrediente[0]))

        conn.commit()
        messagebox.showinfo("Éxito", "Receta y ingredientes modificados correctamente.")
        actualizar_tabla(tree)  # Actualizar la tabla en la interfaz
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al modificar la receta: {err}")
    finally:
        cursor.close()
        conn.close()

<<<<<<< HEAD

=======
>>>>>>> 1751676cfbe521d9b9f09014b421c3233aa83f25
def eliminar_receta(tree):
    # Obtener el elemento seleccionado en el Treeview
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione una receta para eliminar.")
        return

    # Obtener el id de la receta seleccionada
    id_receta = tree.item(seleccion[0], 'values')[0]

    # Confirmación de eliminación
    confirmar = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar esta receta?")
    if confirmar:
        try:
            # Conectar a la base de datos y eliminar la receta y sus ingredientes asociados
            from conexion_bd import conexion  # Importar la función de conexión
            conn = conexion()
            cursor = conn.cursor()

            # Ejecutar las consultas de eliminación
            cursor.execute("DELETE FROM receta WHERE id = %s", (id_receta,))
            cursor.execute("DELETE FROM ingredientes WHERE receta_id = %s", (id_receta,))
            conn.commit()

            # Actualizar el Treeview eliminando el elemento
            tree.delete(seleccion[0])

            # Cerrar conexión
            cursor.close()
            conn.close()

            messagebox.showinfo("Éxito", "Receta eliminada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar la receta: {e}")


"""
def abrir_recetas():    
    # Crear la ventana principal
    global root
    root = tk.Tk()
    root.title('Recetas')
    root.geometry('925x500+300+200')
    root.configure(bg="#fff")
    root.resizable(False, False)

    # Crear el frame del menú lateral
    menu_lateral = tk.Frame(root, bg="#f0f0f0", width=150)
    menu_lateral.pack(side="left", fill="y")
    # Crear el frame central donde se mostrará el contenido dinámico
    frame_central = Frame(root, bg="#fff")
    frame_central.pack(side="right", expand=True, fill="both")

    # Crear las opciones del menú
    opciones_menu = [
        {"texto": "Recompensas", "icono": "★"},
        {"texto": "Reportes", "icono": "📊"},
        {"texto": "Estadísticas", "icono": "📈", "notificacion": True},
        {"texto": "Usuarios", "icono": "👤"},
        {"texto": "Tareas", "icono": "📝"},
        {"texto": "Inventario", "icono": "📦"}
    ]

    # Crear los botones en el menú lateral
    for opcion in opciones_menu:
        frame_opcion = tk.Frame(menu_lateral, bg="white")
        frame_opcion.pack(fill="x", pady=1)

        # Icono y texto de la opción
        etiqueta = tk.Label(frame_opcion, text=f"{opcion['icono']} {opcion['texto']}", anchor="w", padx=10, bg="white")
        etiqueta.pack(fill="x")

        # Si hay una notificación, mostrarla como un punto rojo
        if opcion.get("notificacion"):
            notificacion = tk.Label(frame_opcion, text="●", fg="red", bg="white", anchor="e")
            notificacion.pack(side="right", padx=5)

        # Agregar evento para seleccionar opción
        ventana = root
        etiqueta.bind("<Button-1>", lambda e, texto=opcion['texto']: destruir(texto,ventana))
        
    menu_inferior = Frame(root, bg="#f0f0f0", height=50)
    menu_inferior.pack(side="bottom", fill="x")

    # Agregar las opciones al menú inferior
    opciones_inferiores = ["Ver Recetas"]

    for texto in opciones_inferiores:
        boton = Button(menu_inferior, text=texto, padx=10, pady=5, bg="white", borderwidth=0,
                   command=lambda t=texto: mostrar_recetas(frame_central))
        boton.pack(side="left", padx=20)

    # Ejecutar el bucle principal de la aplicación
    root.mainloop()
"""
def destruir(texto,root) :
    from funcionalidad import seleccionar_opcion
    root.destroy()
    # Añadir más opciones según el menú
    print("se elimino") 
    time.sleep(1)
    seleccionar_opcion(texto)


"""
USE prueba;


-- Crear la tabla de recetas
CREATE TABLE recetas (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(255) NOT NULL,
    Elaboracion TEXT NOT NULL
);



CREATE TABLE IF NOT EXISTS ingredientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    receta_id INT,
    cantidad FLOAT NOT NULL,
    unidad VARCHAR(50) NOT NULL,
    ingrediente VARCHAR(255) NOT NULL,
    FOREIGN KEY (receta_id) REFERENCES recetas(id) ON DELETE CASCADE
);


-- Insertar receta
INSERT INTO receta (nombre, elaboracion) VALUES 
('Guiso de Lentejas', 'Cocinar las lentejas con verduras y especias hasta que estén tiernas.'),
('Tacos de Pollo', 'Rellenar tortillas de maíz con pollo deshebrado, cebolla y cilantro.');

-- Insertar ingredientes para Guiso de Lentejas
INSERT INTO ingredientes (receta_id, cantidad, unidad, ingrediente) VALUES 
(1, 1.5, 'tazas', 'Lentejas'),
(1, 1, 'unidad', 'Cebolla'),
(1, 2, 'dientes', 'Ajo'),
(1, 1, 'unidad', 'Zanahoria'),
(1, 2, 'tazas', 'Caldo de verduras');

-- Insertar ingredientes para Tacos de Pollo
INSERT INTO ingredientes (receta_id, cantidad, unidad, ingrediente) VALUES 
(7, 2, 'tazas', 'Pollo deshebrado'),
(7, 4, 'unidad', 'Tortillas de maíz'),
(7, 0.5, 'taza', 'Cebolla picada'),
(7, 0.5, 'taza', 'Cilantro picado');

"""
