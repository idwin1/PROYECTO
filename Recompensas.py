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
    cursor.execute("SELECT id, nombre, telefono, correo, fecha_nacimiento,puntos FROM miembro")
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

def cargarRecompensas():
    from conexion_bd import conexion
    conn = conexion()
    cursor = conn.cursor()
    
    # Consulta para obtener las recompensas
    cursor.execute("SELECT recompensa, puntos FROM precompensas")
    resultados = cursor.fetchall()

    # Limpiar la tabla antes de insertar nuevos datos
    for row in reward_tree.get_children():
        reward_tree.delete(row)

    # Insertar cada fila en el Treeview
    for fila in resultados:
        reward_tree.insert("", "end", values=fila)

    # Cerrar la conexión
    cursor.close()
    conn.close()

def validar_puntos(puntos):
    try:
        puntos = int(puntos)
        if puntos < 0:
            raise ValueError
        return True
    except ValueError:
        messagebox.showerror("Error", "Los puntos deben ser un número entero positivo.")
        return False


def abrir_ventana_edicion(accion):
    # Obtener el usuario seleccionado
    ventana_edicion = tk.Toplevel()
    ventana_edicion.geometry("400x320")

    # Colores y estilo
    color_fondo = "#f7f2f2"
    color_label = "#333"  # Azul para los labels
    color_boton = "#e06666"  # Rojo para el botón
    color_borde = "#ffd966"  # Amarillo para el borde del marco


    if accion == "Agregar":
        ventana_edicion.title("Agregar Usuario")

        # No crear campo para ID al agregar
        Label(ventana_edicion, text="Nombre:",bg=color_fondo,fg=color_label, font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=10)
        usuario_entry = Entry(ventana_edicion)
        usuario_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(ventana_edicion, text="Telefono:",bg=color_fondo,fg=color_label, font=("Arial", 10, "bold")).grid(row=1, column=0, padx=10, pady=10)
        telefono_entry = Entry(ventana_edicion)
        telefono_entry.grid(row=1, column=1, padx=10, pady=10)

        Label(ventana_edicion, text="Correo:",bg=color_fondo,fg=color_label, font=("Arial", 10, "bold")).grid(row=2, column=0, padx=10, pady=10)
        correo_entry = Entry(ventana_edicion)
        correo_entry.grid(row=2, column=1, padx=10, pady=10)

        Label(ventana_edicion, text="Fecha Nacimiento:",bg=color_fondo,fg=color_label, font=("Arial", 10, "bold")).grid(row=3, column=0, padx=10, pady=10)
        fecha_entry = Entry(ventana_edicion)
        fecha_entry.grid(row=3, column=1, padx=10, pady=10)

        Label(ventana_edicion, text="Puntos",bg=color_fondo,fg=color_label, font=("Arial", 10, "bold")).grid(row=4, column=0, padx=10, pady=10)
        puntos_entry = Entry(ventana_edicion)
        puntos_entry.grid(row=4, column=1, padx=10, pady=10)
        
    elif accion == "Agregar Recompensa":
        ventana_edicion.title("Agregar Recompensa")
        # No crear campo para ID al agregar
        Label(ventana_edicion, text="Recompensa:",bg=color_fondo,fg=color_label, font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=10)
        recompensa_entry = Entry(ventana_edicion)
        recompensa_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(ventana_edicion, text="Puntos:",bg=color_fondo,fg=color_label, font=("Arial", 10, "bold")).grid(row=1, column=0, padx=10, pady=10)
        puntos_entry = Entry(ventana_edicion)
        puntos_entry.grid(row=1, column=1, padx=10, pady=10)
        
    elif accion == "Actualizar Recompensas":
        selected_item = reward_tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona una recompensa para actualizar.")
            ventana_edicion.destroy()
            return

        ventana_edicion.title("Actualizar Recompensas")

        # Crear campos y etiquetas
        Label(ventana_edicion, text="Recompensa:",bg=color_fondo,fg=color_label, font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=10)
        recompensa_entry = Entry(ventana_edicion)
        recompensa_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(ventana_edicion, text="Puntos:",bg=color_fondo,fg=color_label, font=("Arial", 10, "bold")).grid(row=1, column=0, padx=10, pady=10)
        puntos_entry = Entry(ventana_edicion)
        puntos_entry.grid(row=1, column=1, padx=10, pady=10)

        # Obtener los datos de la recompensa seleccionada y cargarlos en los campos
        datos = reward_tree.item(selected_item, "values")
        recompensa_entry.insert(0, datos[0])
        puntos_entry.insert(0, datos[1])
        
    else:
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona un usuario para " + accion.lower())
            ventana_edicion.destroy()
            return

        ventana_edicion.title(f"{accion} Usuario")
        # Crear campo para ID y cargar datos del usuario seleccionado
        Label(ventana_edicion, text="ID:",bg=color_fondo,fg=color_label, font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=10)
        id_entry = Entry(ventana_edicion)
        id_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(ventana_edicion, text="Nombre:",bg=color_fondo,fg=color_label, font=("Arial", 10, "bold")).grid(row=1, column=0, padx=10, pady=10)
        usuario_entry = Entry(ventana_edicion)
        usuario_entry.grid(row=1, column=1, padx=10, pady=10)

        Label(ventana_edicion, text="Telefono:",bg=color_fondo,fg=color_label, font=("Arial", 10, "bold")).grid(row=2, column=0, padx=10, pady=10)
        telefono_entry = Entry(ventana_edicion)
        telefono_entry.grid(row=2, column=1, padx=10, pady=10)

        Label(ventana_edicion, text="Correo:",bg=color_fondo,fg=color_label, font=("Arial", 10, "bold")).grid(row=3, column=0, padx=10, pady=10)
        correo_entry = Entry(ventana_edicion)
        correo_entry.grid(row=3, column=1, padx=10, pady=10)

        Label(ventana_edicion, text="Fecha Nacimiento:",bg=color_fondo,fg=color_label, font=("Arial", 10, "bold")).grid(row=4, column=0, padx=10, pady=10)
        fecha_entry = Entry(ventana_edicion)
        fecha_entry.grid(row=4, column=1, padx=10, pady=10)

        Label(ventana_edicion, text="Puntos",bg=color_fondo,fg=color_label, font=("Arial", 10, "bold")).grid(row=5, column=0, padx=10, pady=10)
        puntos_entry = Entry(ventana_edicion)
        puntos_entry.grid(row=5, column=1, padx=10, pady=10)

        # Cargar los datos del usuario seleccionado
        datos = tree.item(selected_item, "values")
        id_entry.insert(0, datos[0])
        usuario_entry.insert(0, datos[1])
        telefono_entry.insert(0, datos[2])
        correo_entry.insert(0, datos[3])
        fecha_entry.insert(0, datos[4])
        puntos_entry.insert(0, datos[5])
        
        # Bloquear el campo de ID
        id_entry.config(state="readonly")
        if accion == "Eliminar":
            usuario_entry.config(state="readonly")
            telefono_entry.config(state="readonly")
            correo_entry.config(state="readonly")
            fecha_entry.config(state="readonly")
            puntos_entry.config(state="readonly")

    # Botón de acción en la ventana de edición
    def realizar_accion():
        from conexion_bd import conexion
        conn = conexion()
        cursor = conn.cursor()

        if accion == "Agregar":
            nuevo_usuario = usuario_entry.get()
            nuevo_telefono = telefono_entry.get()
            nuevo_correo = correo_entry.get()
            nueva_fecha = fecha_entry.get()
            nuevos_puntos = puntos_entry.get()
                
            if not validar_puntos(nuevos_puntos):
                return

            cursor.execute("INSERT INTO miembro (nombre, telefono, correo, fecha_nacimiento,puntos) VALUES (%s, %s, %s, %s, %s)",
                           (nuevo_usuario, nuevo_telefono, nuevo_correo, nueva_fecha, nuevos_puntos))
            conn.commit()
            messagebox.showinfo("Éxito", "Usuario agregado correctamente.")
        
        elif accion == "Agregar Recompensa":
            nueva_recompensa = recompensa_entry.get()
            nuevos_puntos = puntos_entry.get()
                
            if not validar_puntos(nuevos_puntos):
                return

            cursor.execute("INSERT INTO precompensas (recompensa, puntos) VALUES (%s, %s)",
                           (nueva_recompensa, nuevos_puntos))
            conn.commit()
            cargarRecompensas()
            messagebox.showinfo("Éxito", "Recompensa agregada correctamente.")
        
        elif accion == "Actualizar":
            id_usuario = id_entry.get()
            usuario_actualizado = usuario_entry.get()
            telefono_actualizado = telefono_entry.get()
            correo_actualizado = correo_entry.get()
            fecha_actualizado = fecha_entry.get()
            puntos_actualizados = puntos_entry.get()
                
            if not validar_puntos(puntos_actualizados):
                return

            cursor.execute("UPDATE miembro SET nombre=%s, telefono=%s, correo=%s, fecha_nacimiento=%s,puntos=%s WHERE id=%s",
                           (usuario_actualizado, telefono_actualizado, correo_actualizado, fecha_actualizado, puntos_actualizados,id_usuario))
            conn.commit()
            cargarDatos()
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
        
        elif accion == "Actualizar Recompensas":
            recompensa_actualizada = recompensa_entry.get()
            puntos_actualizados = puntos_entry.get()
                
            if not validar_puntos(puntos_actualizados):
                return

            # Obtener el ID de la recompensa seleccionada
            selected_item = reward_tree.focus()
            datos = reward_tree.item(selected_item, "values")
            recompensa_id = datos[0]

            cursor.execute("UPDATE precompensas SET recompensa=%s, puntos=%s WHERE recompensa=%s",
                           (recompensa_actualizada, puntos_actualizados, recompensa_id))
            conn.commit()
            cargarRecompensas()
            messagebox.showinfo("Éxito", "Recompensa actualizada correctamente.")
        
        elif accion == "Eliminar":
            id_usuario = id_entry.get()
            cursor.execute("DELETE FROM miembro WHERE id=%s", (id_usuario,))
            conn.commit()
            cargarDatos()
            messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
        
        elif accion == "Eliminar Recompensa":
            selected_item = reward_tree.focus()
            if not selected_item:
                messagebox.showwarning("Advertencia", "Selecciona una recompensa para eliminar.")
                return

            # Obtener el nombre de la recompensa
            datos = reward_tree.item(selected_item, "values")
            recompensa = datos[0]

            cursor.execute("DELETE FROM precompensas WHERE recompensa=%s", (recompensa,))
            conn.commit()
            cargarRecompensas()
            messagebox.showinfo("Éxito", "Recompensa eliminada correctamente.")
        
        cursor.close()
        conn.close()
        ventana_edicion.destroy()

    # Botón para realizar la acción
    action_button = Button(ventana_edicion, text=accion, bg=color_boton,
                           fg="white", font=("Arial", 12, "bold"),command=realizar_accion)
    action_button.grid(row=6, column=0, columnspan=2, pady=20)

def eliminarRecompensa():
    selected_item = reward_tree.focus()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Selecciona una recompensa para eliminar.")
        return

    # Obtener el nombre de la recompensa
    datos = reward_tree.item(selected_item, "values")
    recompensa = datos[0]

    # Eliminar recompensa de la base de datos
    from conexion_bd import conexion
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM precompensas WHERE recompensa=%s", (recompensa,))
    conn.commit()
    cargarRecompensas()
    messagebox.showinfo("Éxito", "Recompensa eliminada correctamente.")
    cursor.close()
    conn.close()

def cargarRecompensas():
    from conexion_bd import conexion
    conn = conexion()
    cursor = conn.cursor()
    
    # Consulta para obtener las recompensas
    cursor.execute("SELECT recompensa, puntos FROM precompensas")
    resultados = cursor.fetchall()

    # Limpiar la tabla antes de insertar nuevos datos
    for row in reward_tree.get_children():
        reward_tree.delete(row)

    # Insertar cada fila en el Treeview
    for fila in resultados:
        reward_tree.insert("", "end", values=fila)

    # Cerrar la conexión
    cursor.close()
    conn.close()

def abrir_interfaz_Recompensas(rol):
    global tree
    global reward_tree
    global root
    # Crear la ventana principal
    root = tk.Tk()
    root.iconbitmap("recompensa.ico")
    root.title("Recompensas")

    # Centrar la ventana principal
    screen_width = root.winfo_screenwidth()  # Ancho de la pantalla
    screen_height = root.winfo_screenheight()  # Alto de la pantalla
    window_width = 800  # Ancho de la ventana
    window_height = 600  # Alto de la ventana

    # Calculamos la posición X e Y para centrar la ventana
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)

    # Establecemos la geometría de la ventana
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
    
     # Crear el frame del menú lateral
    menu_lateral = tk.Frame(root, bg="#333333", width=150)
    menu_lateral.pack(side="left", fill="y")

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
        frame_opcion = Frame(menu_lateral, bg="#333333")  # Fondo gris oscuro para cada opción
        frame_opcion.pack(fill="x", pady=1)
        # Icono y texto de la opción
        etiqueta = Label(frame_opcion, text=f"{opcion['icono']} {opcion['texto']}", anchor="w", padx=10, 
                         bg="#333333", fg="#ffffff", font=("Arial", 10, "bold"))  # Texto en blanco y fuente negrita
        etiqueta.pack(fill="x")
        # Si hay una notificación, mostrarla como un punto rojo
        if opcion.get("notificacion"):
            notificacion = Label(frame_opcion, text="●", fg="#ff1744", bg="#333333", anchor="e")  # Punto de notificación en rojo
            notificacion.pack(side="right", padx=5)
        # Agregar evento para seleccionar opción
        ventana = root
        etiqueta.bind("<Button-1>", lambda e, texto=opcion['texto']: destruir(texto, ventana,rol))


    # Crear el marco principal para la tabla de usuarios y los botones con scroll
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(side="right", fill="both", expand=True)

    # Canvas para permitir el desplazamiento
    canvas = tk.Canvas(main_frame, bg="white")
    scroll_y = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="white")

    # Configurar el scroll
    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    # Crear la tabla de usuarios
    title_label = tk.Label(scroll_frame, text="Usuarios", bg="white", font=("Arial", 14))
    title_label.pack(pady=10)

    columns = ("ID", "Nombre", "Telefono", "Correo", "Fecha de Nacimiento", "Puntos")
    tree = ttk.Treeview(scroll_frame, columns=columns, show="headings", height=8)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    tree.pack(pady=20)

    # Botones de acción para usuarios
    button_frame = tk.Frame(scroll_frame, bg="white")
    button_frame.pack(pady=10)

    add_button = tk.Button(button_frame, text="AGREGAR USUARIO", bg="#28A745", fg="white", font=("Arial", 10), width=20, command=lambda: abrir_ventana_edicion("Agregar"))
    add_button.grid(row=0, column=0, padx=5)

    update_button = tk.Button(button_frame, text="ACTUALIZAR USUARIO", bg="#FFC107", fg="black", font=("Arial", 10), width=20, command=lambda: abrir_ventana_edicion("Actualizar"))
    update_button.grid(row=0, column=1, padx=5)

    delete_button = tk.Button(button_frame, text="ELIMINAR USUARIO", bg="#DC3545", fg="white", font=("Arial", 10), width=20, command=lambda: abrir_ventana_edicion("Eliminar"))
    delete_button.grid(row=0, column=2, padx=5)

    # Crear la tabla de recompensas
    reward_title_label = tk.Label(scroll_frame, text="Recompensas", bg="white", font=("Arial", 14))
    reward_title_label.pack(pady=10)

    reward_columns = ("Recompensa", "Puntos")
    reward_tree = ttk.Treeview(scroll_frame, columns=reward_columns, show="headings", height=8)
    for col in reward_columns:
        reward_tree.heading(col, text=col)
        reward_tree.column(col, width=150, anchor="center")
    reward_tree.pack(pady=20)

    # Botones de acción para recompensas
    reward_button_frame = tk.Frame(scroll_frame, bg="white")
    reward_button_frame.pack(pady=10)

    add_reward_button = tk.Button(reward_button_frame, text="AGREGAR RECOMPENSA", bg="#28A745", fg="white", font=("Arial", 10), width=25, command=lambda: abrir_ventana_edicion("Agregar Recompensa"))
    add_reward_button.grid(row=0, column=0, padx=5)

    update_reward_button = tk.Button(reward_button_frame, text="ACTUALIZAR RECOMPENSA", bg="#FFC107", fg="black", font=("Arial", 10), width=25, command=lambda: abrir_ventana_edicion("Actualizar Recompensas"))
    update_reward_button.grid(row=0, column=1, padx=5)

    delete_reward_button = tk.Button(reward_button_frame, text="ELIMINAR RECOMPENSA", bg="#DC3545", fg="white", font=("Arial", 10), width=25, command=eliminarRecompensa)
    delete_reward_button.grid(row=0, column=2, padx=5)

    # Cargar datos iniciales
    cargarDatos()
    cargarRecompensas()
    root.mainloop()



def destruir(texto, root,rol):
    from funcionalidad import seleccionar_opcion
    root.destroy()
    print("texto")
    print(rol)
    time.sleep(1)
    seleccionar_opcion(texto,rol)

abrir_interfaz_Recompensas("A")