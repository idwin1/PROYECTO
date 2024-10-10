import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Función para actualizar la tabla de productos
def actualizar_tabla():
    # Limpiar la tabla existente
    for row in tree.get_children():
        tree.delete(row)

    # Conectar a la base de datos y obtener los productos
    try:
        conn = mysql.connector.connect(
            host="localhost",            # Cambia esto a tu servidor
            user="root",           # Cambia esto a tu usuario
            password="Wario2400_",    # Cambia esto a tu contraseña
            database="prueba"     # Nombre de tu base de datos
        )
        cursor = conn.cursor()

        query = "SELECT ID, Producto, Cantidad FROM productos"
        cursor.execute(query)
        productos = cursor.fetchall()

        for producto in productos:
            tree.insert("", tk.END, values=producto)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al obtener productos: {err}")
    finally:
        cursor.close()
        conn.close()

# Función para agregar un producto a la base de datos
def agregar_producto(id_producto, nombre_producto, cantidad_producto):
    try:
        conn = mysql.connector.connect(
            host="localhost",            # Cambia esto a tu servidor
            user="root",           # Cambia esto a tu usuario
            password="Wario2400_",    # Cambia esto a tu contraseña
            database="prueba"     # Nombre de tu base de datos   
        )
        cursor = conn.cursor()

        query = "INSERT INTO productos (ID, Producto, Cantidad) VALUES (%s, %s, %s)"
        cursor.execute(query, (id_producto, nombre_producto, cantidad_producto))
        conn.commit()

        messagebox.showinfo("Éxito", "Producto agregado correctamente.")
        actualizar_tabla()  # Actualiza la tabla después de agregar
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al agregar el producto: {err}")
    finally:
        cursor.close()
        conn.close()

# Función para modificar un producto en la base de datos
def modificar_producto(id_producto, nuevo_nombre_producto, nueva_cantidad_producto):
    try:
        conn = mysql.connector.connect(
            host="localhost",            # Cambia esto a tu servidor
            user="root",           # Cambia esto a tu usuario
            password="Wario2400_",    # Cambia esto a tu contraseña
            database="prueba"     # Nombre de tu base de datos    
        )
        cursor = conn.cursor()

        query = "UPDATE productos SET Producto = %s, Cantidad = %s WHERE ID = %s"
        cursor.execute(query, (nuevo_nombre_producto, nueva_cantidad_producto, id_producto))
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showwarning("Advertencia", "No se encontró ningún producto con ese ID.")
        else:
            messagebox.showinfo("Éxito", "Producto modificado correctamente.")
            actualizar_tabla()  # Actualiza la tabla después de modificar
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al modificar el producto: {err}")
    finally:
        cursor.close()
        conn.close()

# Función para eliminar un producto de la base de datos
def eliminar_producto():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar.")
        return

    id_producto = tree.item(selected_item, 'values')[0]

    try:
        conn = mysql.connector.connect(
            host="localhost",            # Cambia esto a tu servidor
            user="root",           # Cambia esto a tu usuario
            password="Wario2400_",    # Cambia esto a tu contraseña
            database="prueba"     # Nombre de tu base de datos     
        )
        cursor = conn.cursor()

        query = "DELETE FROM productos WHERE ID = %s"
        cursor.execute(query, (id_producto,))
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showwarning("Advertencia", "No se encontró ningún producto con ese ID.")
        else:
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            actualizar_tabla()  # Actualiza la tabla después de eliminar
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al eliminar el producto: {err}")
    finally:
        cursor.close()
        conn.close()

# Función para abrir la ventana de agregar producto
def abrir_ventana_agregar():
    ventana_agregar = tk.Toplevel(root)
    ventana_agregar.title("Agregar Producto")

    tk.Label(ventana_agregar, text="ID del Producto:").grid(row=0, column=0)
    entry_id = tk.Entry(ventana_agregar)
    entry_id.grid(row=0, column=1)

    tk.Label(ventana_agregar, text="Nombre del Producto:").grid(row=1, column=0)
    entry_nombre = tk.Entry(ventana_agregar)
    entry_nombre.grid(row=1, column=1)

    tk.Label(ventana_agregar, text="Cantidad:").grid(row=2, column=0)
    entry_cantidad = tk.Entry(ventana_agregar)
    entry_cantidad.grid(row=2, column=1)

    tk.Button(ventana_agregar, text="Agregar", 
              command=lambda: agregar_producto(entry_id.get(), entry_nombre.get(), entry_cantidad.get())).grid(row=3, columnspan=2)

# Función para abrir la ventana de modificar producto
def abrir_ventana_modificar():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione un producto para modificar.")
        return

    id_producto = tree.item(selected_item, 'values')[0]
    nombre_producto = tree.item(selected_item, 'values')[1]
    cantidad_producto = tree.item(selected_item, 'values')[2]

    ventana_modificar = tk.Toplevel(root)
    ventana_modificar.title("Modificar Producto")

    tk.Label(ventana_modificar, text="ID del Producto:").grid(row=0, column=0)
    entry_id = tk.Entry(ventana_modificar)
    entry_id.insert(0, id_producto)
    entry_id.config(state='readonly')
    entry_id.grid(row=0, column=1)

    tk.Label(ventana_modificar, text="Nombre del Producto:").grid(row=1, column=0)
    entry_nombre = tk.Entry(ventana_modificar)
    entry_nombre.insert(0, nombre_producto)
    entry_nombre.grid(row=1, column=1)

    tk.Label(ventana_modificar, text="Cantidad:").grid(row=2, column=0)
    entry_cantidad = tk.Entry(ventana_modificar)
    entry_cantidad.insert(0, cantidad_producto)
    entry_cantidad.grid(row=2, column=1)

    tk.Button(ventana_modificar, text="Modificar", 
              command=lambda: modificar_producto(entry_id.get(), entry_nombre.get(), entry_cantidad.get())).grid(row=3, columnspan=2)

# Crear la ventana principal
root = tk.Tk()
root.title("Gestión de Productos")

# Aplicar un estilo
style = ttk.Style()
style.theme_use('clam')  # Puedes probar otros temas como 'default', 'alt', 'classic'
style.configure("Treeview", foreground="black", background="white")
style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
style.map("Treeview", background=[('selected', 'lightblue')])

# Configurar la tabla de productos
tk.Label(root, text="Inventario", font=('Arial', 16)).grid(row=0, column=0, columnspan=3, pady=10)

tree = ttk.Treeview(root, columns=("ID", "Producto", "Cantidad"), show='headings')
tree.heading("ID", text="ID")
tree.heading("Producto", text="Producto")
tree.heading("Cantidad", text="Cantidad")
tree.column("ID", width=100)
tree.column("Producto", width=200)
tree.column("Cantidad", width=100)
tree.grid(row=1, column=0, columnspan=3, padx=20)

# Botones para agregar, modificar y eliminar productos
frame = tk.Frame(root)
frame.grid(row=2, column=0, columnspan=3, pady=10)

btn_agregar = tk.Button(frame, text="Agregar Producto", command=abrir_ventana_agregar, bg='lightgreen', font=('Arial', 12))
btn_agregar.grid(row=0, column=0, padx=5)

btn_modificar = tk.Button(frame, text="Modificar Producto", command=abrir_ventana_modificar, bg='lightyellow', font=('Arial', 12))
btn_modificar.grid(row=0, column=1, padx=5)

btn_eliminar = tk.Button(frame, text="Eliminar Producto", command=eliminar_producto, bg='lightcoral', font=('Arial', 12))
btn_eliminar.grid(row=0, column=2, padx=5)

# Actualizar la tabla de productos al inicio
actualizar_tabla()

# Ejecutar la interfaz
root.mainloop()
