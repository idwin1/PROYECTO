from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
from login import pedir_ip
# Función para mostrar la interfaz de inventario en el área central
def mostrar_inventario(frame_central):
    
    # Limpiar el contenido actual del área central
    for widget in frame_central.winfo_children():
        widget.destroy()

    # Aplicar un estilo
    style = ttk.Style()
    style.theme_use('classic')  # Puedes probar otros temas como 'default', 'alt', 'classic'
    style.configure("Treeview", foreground="black", background="white")
    style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
    style.map("Treeview", background=[('selected', 'lightblue')])

    # Configurar la tabla de productos
    Label(frame_central, text="Inventario", font=('Arial', 16)).grid(row=0, column=0, columnspan=3, pady=10)

    tree = ttk.Treeview(frame_central, columns=("ID", "Producto", "Cantidad"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Producto", text="Producto")
    tree.heading("Cantidad", text="Cantidad")
    tree.column("ID", width=100)
    tree.column("Producto", width=200)
    tree.column("Cantidad", width=100)
    tree.grid(row=1, column=0, columnspan=3, padx=20)

    # Botones para agregar, modificar y eliminar productos
    frame_botones = Frame(frame_central)
    frame_botones.grid(row=2, column=0, columnspan=3, pady=10)

    Button(frame_botones, text="Agregar Producto", command=lambda: abrir_ventana_agregar(tree), bg='lightgreen', font=('Arial', 12)).grid(row=0, column=0, padx=5)
    Button(frame_botones, text="Modificar Producto", command=lambda: abrir_ventana_modificar(tree), bg='lightyellow', font=('Arial', 12)).grid(row=0, column=1, padx=5)
    Button(frame_botones, text="Eliminar Producto", command=lambda: eliminar_producto(tree), bg='lightcoral', font=('Arial', 12)).grid(row=0, column=2, padx=5)

    # Actualizar la tabla de productos al inicio
    actualizar_tabla(tree)

# Función para actualizar la tabla de productos
def actualizar_tabla(tree):
    # Limpiar la tabla existente
    for row in tree.get_children():
        tree.delete(row)

    # Conectar a la base de datos y obtener los productos
    try:
        conn = mysql.connector.connect(
            host=pedir_ip(),            
            user="root",           
            password="sandrauno",    
            database="cafe"   
        )
        cursor = conn.cursor()

        query = "SELECT ID, Producto, Cantidad FROM productos"
        cursor.execute(query)
        productos = cursor.fetchall()

        for producto in productos:
            tree.insert("", END, values=producto)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al obtener productos: {err}")
    finally:
        cursor.close()
        conn.close()

# Función para agregar un producto
def agregar_producto(id_producto, nombre_producto, cantidad_producto, tree):
    try:
        conn = mysql.connector.connect(
            host=pedir_ip(),            
            user="root",           
            password="sandrauno",    
            database="cafe"    
        )
        cursor = conn.cursor()

        query = "INSERT INTO productos (ID, Producto, Cantidad) VALUES (%s, %s, %s)"
        cursor.execute(query, (id_producto, nombre_producto, cantidad_producto))
        conn.commit()

        messagebox.showinfo("Éxito", "Producto agregado correctamente.")
        actualizar_tabla(tree)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al agregar el producto: {err}")
    finally:
        cursor.close()
        conn.close()

# Función para modificar un producto
def modificar_producto(id_producto, nuevo_nombre_producto, nueva_cantidad_producto, tree):
    try:
        conn = mysql.connector.connect(
            host=pedir_ip(),            
            user="root",           
            password="sandrauno",    
            database="cafe"    
        )
        cursor = conn.cursor()

        query = "UPDATE productos SET Producto = %s, Cantidad = %s WHERE ID = %s"
        cursor.execute(query, (nuevo_nombre_producto, nueva_cantidad_producto, id_producto))
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showwarning("Advertencia", "No se encontró ningún producto con ese ID.")
        else:
            messagebox.showinfo("Éxito", "Producto modificado correctamente.")
            actualizar_tabla(tree)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al modificar el producto: {err}")
    finally:
        cursor.close()
        conn.close()

# Función para mostrar la interfaz de inventario en el área central
def mostrar_inventario(frame_central):
    # Limpiar el contenido actual del área central
    for widget in frame_central.winfo_children():
        widget.destroy()

    # Aplicar un estilo
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Treeview", foreground="black", background="white")
    style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
    style.map("Treeview", background=[('selected', 'lightblue')])

    # Configurar la tabla de productos
    Label(frame_central, text="Inventario", font=('Arial', 16)).grid(row=0, column=0, columnspan=4, pady=10)

    tree = ttk.Treeview(frame_central, columns=("ID", "Producto", "Cantidad"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Producto", text="Producto")
    tree.heading("Cantidad", text="Cantidad")
    tree.column("ID", width=100)
    tree.column("Producto", width=200)
    tree.column("Cantidad", width=100)
    tree.grid(row=2, column=0, columnspan=4, padx=20)

    # Crear barra de búsqueda
    Label(frame_central, text="Buscar Producto:").grid(row=1, column=0, padx=10, pady=10)
    entry_busqueda = Entry(frame_central)
    entry_busqueda.grid(row=1, column=1, padx=10, pady=10)

    Button(frame_central, text="Buscar", command=lambda: buscar_producto(tree, entry_busqueda.get()), bg='lightblue', font=('Arial', 12)).grid(row=1, column=2, padx=10)

    # Botones para agregar, modificar y eliminar productos
    frame_botones = Frame(frame_central)
    frame_botones.grid(row=3, column=0, columnspan=4, pady=10)

    Button(frame_botones, text="Agregar Producto", command=lambda: abrir_ventana_agregar(tree), bg='lightgreen', font=('Arial', 12)).grid(row=0, column=0, padx=5)
    Button(frame_botones, text="Modificar Producto", command=lambda: abrir_ventana_modificar(tree), bg='lightyellow', font=('Arial', 12)).grid(row=0, column=1, padx=5)
    Button(frame_botones, text="Eliminar Producto", command=lambda: eliminar_producto(tree), bg='lightcoral', font=('Arial', 12)).grid(row=0, column=2, padx=5)

    # Actualizar la tabla de productos al inicio
    actualizar_tabla(tree)

# Función para buscar productos
def buscar_producto(tree, termino_busqueda):
    # Limpiar la tabla existente
    for row in tree.get_children():
        tree.delete(row)

    # Conectar a la base de datos y buscar productos
    try:
        conn = mysql.connector.connect(
            host=pedir_ip(),
            user="root",
            password="sandrauno",
            database="cafe"
        )
        cursor = conn.cursor()

        query = "SELECT ID, Producto, Cantidad FROM productos WHERE Producto LIKE %s OR ID LIKE %s"
        termino = f"%{termino_busqueda}%"
        cursor.execute(query, (termino, termino))
        productos = cursor.fetchall()

        for producto in productos:
            tree.insert("", END, values=producto)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al buscar productos: {err}")
    finally:
        cursor.close()
        conn.close()

# Función para actualizar la tabla de productos
def actualizar_tabla(tree):
    # Limpiar la tabla existente
    for row in tree.get_children():
        tree.delete(row)

    # Conectar a la base de datos y obtener los productos
    try:
        conn = mysql.connector.connect(
            host=pedir_ip(),
            user="root",
            password="sandrauno",
            database="cafe"
        )
        cursor = conn.cursor()

        query = "SELECT ID, Producto, Cantidad FROM productos"
        cursor.execute(query)
        productos = cursor.fetchall()

        for producto in productos:
            tree.insert("", END, values=producto)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al obtener productos: {err}")
    finally:
        cursor.close()
        conn.close()

# Función para eliminar un producto
def eliminar_producto(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar.")
        return

    id_producto = tree.item(selected_item, 'values')[0]

    try:
        conn = mysql.connector.connect(
            host=pedir_ip(),            
            user="root",           
            password="sandrauno",    
            database="cafe"    
        )
        cursor = conn.cursor()

        query = "DELETE FROM productos WHERE ID = %s"
        cursor.execute(query, (id_producto,))
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showwarning("Advertencia", "No se encontró ningún producto con ese ID.")
        else:
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            actualizar_tabla(tree)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al eliminar el producto: {err}")
    finally:
        cursor.close()
        conn.close()

# Función para abrir la ventana de agregar producto
def abrir_ventana_agregar(tree):
    ventana_agregar = Toplevel(root)
    ventana_agregar.title("Agregar Producto")

    Label(ventana_agregar, text="ID del Producto:").grid(row=0, column=0)
    entry_id = Entry(ventana_agregar)
    entry_id.grid(row=0, column=1)

    Label(ventana_agregar, text="Nombre del Producto:").grid(row=1, column=0)
    entry_nombre = Entry(ventana_agregar)
    entry_nombre.grid(row=1, column=1)

    Label(ventana_agregar, text="Cantidad:").grid(row=2, column=0)
    entry_cantidad = Entry(ventana_agregar)
    entry_cantidad.grid(row=2, column=1)

    Button(ventana_agregar, text="Agregar", 
           command=lambda: agregar_producto(entry_id.get(), entry_nombre.get(), entry_cantidad.get(), tree)).grid(row=3, columnspan=2)

# Función para abrir la ventana de modificar producto
def abrir_ventana_modificar(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un producto para modificar.")
        return

    id_producto = tree.item(selected_item, 'values')[0]
    nombre_producto = tree.item(selected_item, 'values')[1]
    cantidad_producto = tree.item(selected_item, 'values')[2]

    ventana_modificar = Toplevel(root)
    ventana_modificar.title("Modificar Producto")

    Label(ventana_modificar, text="ID del Producto:").grid(row=0, column=0)
    entry_id = Entry(ventana_modificar)
    entry_id.insert(0, id_producto)
    entry_id.config(state='readonly')
    entry_id.grid(row=0, column=1)

    Label(ventana_modificar, text="Nombre del Producto:").grid(row=1, column=0)
    entry_nombre = Entry(ventana_modificar)
    entry_nombre.insert(0, nombre_producto)
    entry_nombre.grid(row=1, column=1)

    Label(ventana_modificar, text="Cantidad:").grid(row=2, column=0)
    entry_cantidad = Entry(ventana_modificar)
    entry_cantidad.insert(0, cantidad_producto)
    entry_cantidad.grid(row=2, column=1)

    Button(ventana_modificar, text="Modificar", 
           command=lambda: modificar_producto(entry_id.get(), entry_nombre.get(), entry_cantidad.get(), tree)).grid(row=3, columnspan=2)

# Función para seleccionar opción desde el menú lateral
def seleccionar_opcion(opcion, frame_central):
    if opcion == "Inventario":
        mostrar_inventario(frame_central)
    elif opcion == "Recompensas":
        print("Abrir interfaz de Recompensas")  # Aquí puedes integrar la interfaz de Recompensas
    # Añadir más opciones según el menú

# Configuración principal de la ventana
root = Tk()
root.title("Gestión de Inventario")
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

# Crear el frame del menú lateral
menu_lateral = Frame(root, bg="#f0f0f0", width=150)
menu_lateral.pack(side="left", fill="y")

# Crear el frame central donde se mostrará el contenido dinámico
frame_central = Frame(root, bg="#fff")
frame_central.pack(side="right", expand=True, fill="both")

# Crear las opciones del menú lateral
opciones_menu = [
    {"texto": "Recompensas", "icono": "★"},
    {"texto": "Reportes", "icono": "📊"},
    {"texto": "Estadísticas", "icono": "📈", "notificacion": True},
    {"texto": "Usuarios", "icono": "👤"},
    {"texto": "Tareas", "icono": "📝"},
    {"texto": "Reservas", "icono": "📅"},
    {"texto": "Inventario", "icono": "📦"}
]

# Crear los botones en el menú lateral
for opcion in opciones_menu:
    frame_opcion = Frame(menu_lateral, bg="white")
    frame_opcion.pack(fill="x", pady=1)

    # Icono y texto de la opción
    etiqueta = Label(frame_opcion, text=f"{opcion['icono']} {opcion['texto']}", anchor="w", padx=10, bg="white")
    etiqueta.pack(fill="x")

    # Si hay una notificación, mostrarla como un punto rojo
    if opcion.get("notificacion"):
        notificacion = Label(frame_opcion, text="●", fg="red", bg="white", anchor="e")
        notificacion.pack(side="right", padx=5)

    # Agregar evento para seleccionar opción
    etiqueta.bind("<Button-1>", lambda e, texto=opcion['texto']: seleccionar_opcion(texto, frame_central))

# Ejecutar el bucle principal de la aplicación
root.mainloop()