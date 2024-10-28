from tkinter import *
from tkinter import messagebox, ttk
from tkinter import simpledialog
import mysql.connector
import time
# Función para mostrar la interfaz de recetas en el área central

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

        query = "SELECT ID, Nombre, Ingredientes, Elaboracion FROM recetas WHERE Nombre LIKE %s OR ID LIKE %s"
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
            query = "SELECT ID, Nombre, Ingredientes, Elaboracion FROM recetas"
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
def abrir_ventana_agregar(tree):
    global root  # Asegúrate de que root está disponible
    ventana_agregar = Toplevel(root)
    ventana_agregar.title("Agregar Receta")

    Label(ventana_agregar, text="ID de la Receta:").grid(row=0, column=0)
    entry_id = Entry(ventana_agregar)
    entry_id.grid(row=0, column=1)

    Label(ventana_agregar, text="Nombre de la Receta:").grid(row=1, column=0)
    entry_nombre = Entry(ventana_agregar)
    entry_nombre.grid(row=1, column=1)

    Label(ventana_agregar, text="Ingredientes:").grid(row=2, column=0)
    entry_ingredientes = Entry(ventana_agregar)
    entry_ingredientes.grid(row=2, column=1)

    Label(ventana_agregar, text="Elaboración:").grid(row=3, column=0)
    entry_elaboracion = Entry(ventana_agregar)
    entry_elaboracion.grid(row=3, column=1)

    Button(ventana_agregar, text="Agregar", 
           command=lambda: agregar_receta(entry_id.get(), entry_nombre.get(), entry_ingredientes.get(), entry_elaboracion.get(), tree, ventana_agregar)).grid(row=4, columnspan=2)

# Función para agregar una receta
def agregar_receta(id_receta, nombre_receta, ingredientes, elaboracion, tree, ventana_agregar):
    from conexion_bd import conexion
    try:
        conn = conexion()
        cursor = conn.cursor()

        query = "INSERT INTO recetas (ID, Nombre, Ingredientes, Elaboracion) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (id_receta, nombre_receta, ingredientes, elaboracion))
        conn.commit()

        messagebox.showinfo("Éxito", "Receta agregada correctamente.")
        actualizar_tabla(tree)
        ventana_agregar.destroy()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al agregar la receta: {err}")
    finally:
        cursor.close()
        conn.close()

# Función para abrir la ventana para modificar una receta
def abrir_ventana_modificar(tree):
    global root  # Asegúrate de que root está disponible
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Seleccione una receta para modificar.")
        return

    id_receta = tree.item(selected_item, 'values')[0]
    nombre_receta = tree.item(selected_item, 'values')[1]
    ingredientes = tree.item(selected_item, 'values')[2]
    elaboracion = tree.item(selected_item, 'values')[3]

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

    Label(ventana_modificar, text="Ingredientes:").grid(row=2, column=0)
    entry_ingredientes = Entry(ventana_modificar)
    entry_ingredientes.insert(0, ingredientes)
    entry_ingredientes.grid(row=2, column=1)

    Label(ventana_modificar, text="Elaboración:").grid(row=3, column=0)
    entry_elaboracion = Entry(ventana_modificar)
    entry_elaboracion.insert(0, elaboracion)
    entry_elaboracion.grid(row=3, column=1)

    Button(ventana_modificar, text="Modificar", 
           command=lambda: modificar_receta(entry_id.get(), entry_nombre.get(), entry_ingredientes.get(), entry_elaboracion.get(), tree, ventana_modificar.destroy())).grid(row=4, columnspan=2)

def agregar_receta(self):
        nombre = simpledialog.askstring("Agregar Receta", "Ingrese el nombre de la receta:")
        elaboracion = simpledialog.askstring("Agregar Receta", "Ingrese la elaboración:")
        if nombre and elaboracion:
            self.cursor.execute("INSERT INTO recetas (nombre, elaboracion) VALUES (%s, %s)", (nombre, elaboracion))
            self.conn.commit()
            receta_id = self.cursor.lastrowid
            self.agregar_ingredientes(receta_id)

def agregar_ingredientes(self, receta_id):
        while True:
            cantidad = simpledialog.askfloat("Agregar Ingrediente", "Ingrese la cantidad:")
            if cantidad is None:
                break
            unidad = simpledialog.askstring("Agregar Ingrediente", "Ingrese la unidad:")
            ingrediente = simpledialog.askstring("Agregar Ingrediente", "Ingrese el ingrediente:")
            if unidad and ingrediente:
                self.cursor.execute("INSERT INTO ingredientes (receta_id, cantidad, unidad, ingrediente) VALUES (%s, %s, %s, %s)", 
                                    (receta_id, cantidad, unidad, ingrediente))
                self.conn.commit()
            else:
                break

        self.cargar_recetas()

def modificar_receta(self):
        seleccion = self.lista_recetas.curselection()
        if seleccion:
            id_receta = self.lista_recetas.get(seleccion[0])[0]
            nombre = simpledialog.askstring("Modificar Receta", "Ingrese el nuevo nombre de la receta:")
            elaboracion = simpledialog.askstring("Modificar Receta", "Ingrese la nueva elaboración:")
            if nombre and elaboracion:
                self.cursor.execute("UPDATE recetas SET nombre = %s, elaboracion = %s WHERE id = %s", 
                                    (nombre, elaboracion, id_receta))
                self.conn.commit()

                # Modificar ingredientes
                self.modificar_ingredientes(id_receta)

                self.cargar_recetas()

def modificar_ingredientes(self, receta_id):
        # Mostrar ingredientes actuales
        self.cursor.execute("SELECT id, cantidad, unidad, ingrediente FROM ingredientes WHERE receta_id = %s", (receta_id,))
        ingredientes = self.cursor.fetchall()
        
        for id_ingrediente, cantidad, unidad, ingrediente in ingredientes:
            respuesta = messagebox.askyesno("Modificar Ingrediente", f"¿Desea modificar el ingrediente: {cantidad} {unidad} de {ingrediente}?")
            if respuesta:
                nueva_cantidad = simpledialog.askfloat("Modificar Ingrediente", "Ingrese la nueva cantidad:", initialvalue=cantidad)
                nueva_unidad = simpledialog.askstring("Modificar Ingrediente", "Ingrese la nueva unidad:", initialvalue=unidad)
                nuevo_ingrediente = simpledialog.askstring("Modificar Ingrediente", "Ingrese el nuevo ingrediente:", initialvalue=ingrediente)
                
                if nueva_cantidad is not None and nueva_unidad and nuevo_ingrediente:
                    self.cursor.execute("UPDATE ingredientes SET cantidad = %s, unidad = %s, ingrediente = %s WHERE id = %s", 
                                        (nueva_cantidad, nueva_unidad, nuevo_ingrediente, id_ingrediente))
                    self.conn.commit()

def eliminar_receta(self):
        seleccion = self.lista_recetas.curselection()
        if seleccion:
            id_receta = self.lista_recetas.get(seleccion[0])[0]
            confirmar = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar esta receta?")
            if confirmar:
                self.cursor.execute("DELETE FROM recetas WHERE id = %s", (id_receta,))
                self.cursor.execute("DELETE FROM ingredientes WHERE receta_id = %s", (id_receta,))
                self.conn.commit()
                self.cargar_recetas()
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


-- Insertar recetas
INSERT INTO recetas (nombre, elaboracion) VALUES 
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
(2, 2, 'tazas', 'Pollo deshebrado'),
(2, 4, 'unidad', 'Tortillas de maíz'),
(2, 0.5, 'taza', 'Cebolla picada'),
(2, 0.5, 'taza', 'Cilantro picado');

"""