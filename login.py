#Primera pagina que se muestra
#verificar el inicio de sesion
#Pasar a la pagina de inicio
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # Importamos Pillow
import ast
from funcionalidad import seleccionar_opcion

# Crear ventana principal
root = Tk()
root.title('Acceso')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

import os

def signin():
    username = user.get()
    password = code.get()
    
    # Verificar el archivo de datos
    file = open('datasheet.txt', 'r')
    d = file.read()
    r = ast.literal_eval(d)
    file.close()
    
    if username in r.keys() and password == r[username]:
        # Cerrar la ventana de login actual
        root.destroy()
 # Ejecutar el archivo inicio.py
        archivo_inicio = 'inicio.py'  # Usar solo el nombre del archivo
        if os.path.exists(archivo_inicio):
            exec(open(archivo_inicio).read())
        else:
            messagebox.showerror('Error', f'No se encontró el archivo {archivo_inicio}')
    else:
        messagebox.showerror('Invalida', 'Invalid username or password')


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

heading = Label(frame, text='Sign in', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

# Campo de usuario
def on_enter(e):
    user.delete(0, "end")

def on_leave(e):
    if user.get() == '':
        user.insert(0, 'Username')

user = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

# Campo de contraseña
def on_enter(e):
    code.delete(0, "end")

def on_leave(e):
    if code.get() == '':
        code.insert(0, 'Password')

code = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)
# Guardar datos en las variables y conectarse a la base de datos
def login():
    texto = "pagina_principal"
    Nom = user.get()  # Guardar nombre de usuario en la variable Nom
    contr = code.get()  # Guardar la contraseña en la variable contr

    try:
        # Conectar a la base de datos MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Reemplaza con tu usuario de MySQL
            password='sandrauno',  # Reemplaza con tu contraseña de MySQL
            database='cafe'  # Base de datos 'cafe'
        )
        
        cursor = connection.cursor()

        # Verificar usuario en la base de datos (ejemplo simple, asegúrate de tener la tabla `usuarios`)
        query = "SELECT usuario,contrasena FROM usuarios WHERE usuario=%s AND contrasena=%s"
        cursor.execute(query, (Nom, contr))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
            inicio(texto)
            
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error de conexión: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def inicio(texto):
    root.destroy()
    seleccionar_opcion(texto)
    

# Botón para iniciar sesión
Button(frame, width=39, pady=7, text='Sign in', fg='white', bg='#57a1f8', border=0, command=login).place(x=35, y=204)

# Iniciar el bucle de la ventana
root.mainloop()

