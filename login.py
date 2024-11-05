from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # Importamos Pillow
import ast
import mysql.connector
import os


def abrir_login():
    # Crear ventana principal
    root = Tk()
    root.title('Acceso')
    root.geometry('925x500+300+200')
    root.configure(bg="#fff")
    root.resizable(False, False)

    def signin():
        username = user.get()
        password = code.get()
        # Verificar el archivo de datos
        with open('datasheet.txt', 'r') as file:
            d = file.read()
            r = ast.literal_eval(d)

        if username in r and password == r[username]:
            from funcionalidad import seleccionar_opcion  # Importar la función que manejará la selección de opción
            root.destroy()  # Destruir la ventana de inicio de sesión antes de pasar a la siguiente
            seleccionar_opcion('pagina_principal')  # Aquí se llama la función que abrirá la nueva ventana
        else:
            messagebox.showerror('Invalida', 'Usuario o contraseña incorrectos')

    # Cargar y redimensionar la imagen con Pillow
    max_width = 400  # Ajusta según lo necesites
    max_height = 400  # Ajusta según lo necesites

    image = Image.open('logo.png')
    original_width, original_height = image.size
    ratio = min(max_width / original_width, max_height / original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)
    image = image.resize((new_width, new_height))

    # Convertir la imagen a un formato que Tkinter pueda usar
    img = ImageTk.PhotoImage(image)

    # Mostrar la imagen redimensionada en la ventana
    Label(root, image=img, bg='white').place(x=50, y=50)

    # Crear un frame para los elementos de inicio de sesión
    frame = Frame(root, width=350, height=350, bg="white")
    frame.place(x=480, y=70)

    heading = Label(frame, text='Iniciar Sesión', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x=100, y=5)

    # Campo de usuario
    def on_enter(e):
        user.delete(0, "end")

    def on_leave(e):
        if user.get() == '':
            user.insert(0, 'Usuario')

    user = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
    user.place(x=30, y=80)
    user.insert(0, 'Usuario')
    user.bind('<FocusIn>', on_enter)
    user.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

    # Campo de contraseña
    def on_enter(e):
        code.delete(0, "end")

    def on_leave(e):
        if code.get() == '':
            code.insert(0, 'Contraseña')

    code = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
    code.place(x=30, y=150)
    code.insert(0, 'Contraseña')
    code.bind('<FocusIn>', on_enter)
    code.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

    # Función para iniciar sesión y llamar a la opción correspondiente
    def login():
        from conexion_bd import conexion
        texto = "pagina_principal"
        Nom = user.get()
        contr = code.get()

        try:
            # Conectar a la base de datos MySQL
            connection = conexion()

            cursor = connection.cursor()

            # Verificar usuario en la base de datos (ejemplo simple, asegúrate de tener la tabla `usuarios`)
            query = "SELECT usuario, contrasena, rol FROM usuarios WHERE usuario=%s AND contrasena=%s"
            cursor.execute(query, (Nom, contr))
            result = cursor.fetchone()
            
            if result:
                messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
                from funcionalidad import seleccionar_opcion  # Importar la función que manejará la selección de opción
                root.destroy()  # Destruir la ventana actual
                rol = result[2]
                print(rol)
                seleccionar_opcion(texto,rol)  # Llamar a la función para abrir la nueva ventana
            else:
                messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error de conexión: {err}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    # Botón para iniciar sesión
    Button(frame, width=39, pady=7, text='Iniciar Sesión', fg='white', bg='#57a1f8', border=0, command=login).place(x=35, y=204)

    # Iniciar el bucle de la ventana

    root.mainloop()

abrir_login()