from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector

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
    Label(frame_central, text="Recetas", font=('Arial', 16)).grid(row=0, column=0, columnspan=3, pady=10)

    tree = ttk.Treeview(frame_central, columns=("ID", "Nombre"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.column("ID", width=100)
    tree.column("Nombre", width=200)
    tree.grid(row=1, column=0, columnspan=3, padx=20)

    # Botones para agregar y modificar recetas
    frame_botones = Frame(frame_central)
    frame_botones.grid(row=2, column=0, columnspan=3, pady=10)
    Button(frame_botones, text="Agregar Receta", command=lambda: abrir_ventana_agregar(tree), bg='lightgreen').grid(row=0, column=0, padx=10)
    Button(frame_botones, text="Modificar Receta", command=lambda: abrir_ventana_modificar(tree), bg='lightyellow').grid(row=0, column=1, padx=10)
    Button(frame_botones, text="Ver Detalles", command=lambda: ver_detalles(tree), bg='lightblue').grid(row=0, column=2, padx=10)

    # Actualizar la tabla de recetas al inicio
    actualizar_tabla(tree)

def actualizar_tabla(tree):
    # Limpiar la tabla existente
    for row in tree.get_children():
        tree.delete(row)

    # Conectar a la base de datos y obtener las recetas
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Wario2400_",
            database="prueba"
        )
        cursor = conn.cursor()

        query = "SELECT ID, Nombre FROM recetas"
        cursor.execute(query)
        recetas = cursor.fetchall()

        for receta in recetas:
            tree.insert("", END, values=receta)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al obtener recetas: {err}")
    finally:
        cursor.close()
        conn.close()

# Función para abrir la ventana de agregar receta
def abrir_ventana_agregar(tree):
    ventana_agregar = Toplevel(root)
    ventana_agregar.title("Agregar Receta")

    Label(ventana_agregar, text="Nombre de la Receta:").grid(row=0, column=0)
    entry_nombre = Entry(ventana_agregar)
    entry_nombre.grid(row=0, column=1)

    Label(ventana_agregar, text="Detalles:").grid(row=1, column=0)
    entry_detalles = Entry(ventana_agregar)
    entry_detalles.grid(row=1, column=1)

    Button(ventana_agregar, text="Agregar", 
           command=lambda: agregar_receta(entry_nombre.get(), entry_detalles.get(), tree)).grid(row=2, columnspan=2)

def agregar_receta(nombre_receta, detalles_receta, tree):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Wario2400_",
            database="prueba"
        )
        cursor = conn.cursor()

        query = "INSERT INTO recetas (Nombre, Detalles) VALUES (%s, %s)"
        cursor.execute(query, (nombre_receta, detalles_receta))
        conn.commit()

        messagebox.showinfo("Éxito", "Receta agregada correctamente.")
        actualizar_tabla(tree)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al agregar la receta: {err}")
    finally:
        cursor.close()
        conn.close()

# Función para abrir la ventana de modificar receta
def abrir_ventana_modificar(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione una receta para modificar.")
        return

    id_receta = tree.item(selected_item, 'values')[0]
    nombre_receta = tree.item(selected_item, 'values')[1]

    ventana_modificar = Toplevel(root)
    ventana_modificar.title("Modificar Receta")

    Label(ventana_modificar, text="ID de la Receta:").grid(row=0, column=0)
    entry_id = Entry(ventana_modificar)
    entry_id.insert(0, id_receta)
    entry_id.config(state='readonly')
    entry_id.grid(row=0, column=1)

    Label(ventana_modificar, text="Nombre de la Receta:").grid(row=1, column=0)
    entry_nombre = Entry(ventana_modificar)
    entry_nombre.insert(0, nombre_receta)
    entry_nombre.grid(row=1, column=1)

    Button(ventana_modificar, text="Modificar", 
           command=lambda: modificar_receta(entry_id.get(), entry_nombre.get(), tree)).grid(row=2, columnspan=2)

def modificar_receta(id_receta, nuevo_nombre_receta, tree):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Wario2400_",
            database="prueba"
        )
        cursor = conn.cursor()

        query = "UPDATE recetas SET Nombre = %s WHERE ID = %s"
        cursor.execute(query, (nuevo_nombre_receta, id_receta))
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showwarning("Advertencia", "No se encontró ninguna receta con ese ID.")
        else:
            messagebox.showinfo("Éxito", "Receta modificada correctamente.")
            actualizar_tabla(tree)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al modificar la receta: {err}")
    finally:
        cursor.close()
        conn.close()

# Función para ver detalles de la receta seleccionada
def ver_detalles(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione una receta para ver detalles.")
        return

    id_receta = tree.item(selected_item, 'values')[0]
    nombre_receta = tree.item(selected_item, 'values')[1]

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Wario2400_",
            database="prueba"
        )
        cursor = conn.cursor()

        query = "SELECT ingredientes,Elaboracion FROM recetas WHERE ID = %s"
        cursor.execute(query, (id_receta,))
        detalles_receta = cursor.fetchone()

        if detalles_receta:
            messagebox.showinfo(f"Detalles de {nombre_receta}", detalles_receta[0])
        else:
            messagebox.showwarning("Advertencia", "No se encontraron detalles para esta receta.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al obtener detalles: {err}")
    finally:
        cursor.close()
        conn.close()

# Configuración principal de la ventana
root = Tk()
root.title("Gestión de Recetas")
root.geometry('400x400+300+300')
root.configure(bg="#fff")
root.resizable(False, False)

# Frame central donde se mostrará el contenido dinámico
frame_central = Frame(root, bg="#fff")
frame_central.pack(expand=True, fill="both")

# Llamar a la función para mostrar recetas
mostrar_recetas(frame_central)

# Ejecutar el bucle principal de la aplicación
root.mainloop()
