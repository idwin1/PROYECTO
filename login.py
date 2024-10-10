from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # Importamos Pillow
import mysql.connector

# Crear la ventana principal
root = Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

# Definir el tamaño máximo para la imagen (el tamaño de la ventana)
max_width = 400  # Ajusta según lo necesites
max_height = 400  # Ajusta según lo necesites

# Cargar y redimensionar la imagen con Pillow
image = Image.open('logo.png')
original_width, original_height = image.size

# Calcular la proporción para redimensionar manteniendo la relación de aspecto
ratio = min(max_width / original_width, max_height / original_height)
new_width = int(original_width * ratio)
new_height = int(original_height * ratio)

# Redimensionar la imagen
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
    name = user.get()
    if name == '':
        user.insert(0, 'Username')

user = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

# Campo de contraseña
def on_enter_pass(e):
    code.delete(0, "end")

def on_leave_pass(e):
    if code.get() == '':
        code.insert(0, 'Password')

code = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11), show="*")
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter_pass)
code.bind('<FocusOut>', on_leave_pass)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

# Guardar datos en las variables y conectarse a la base de datos
def login():

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
        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error de conexión: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Botón para iniciar sesión
Button(frame, width=39, pady=7, text='Sign in', fg='white', bg='#57a1f8', border=0, command=login).place(x=35, y=204)

label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
label.place(x=75, y=270)

sign_up = Button(frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#57a1f8')
sign_up.place(x=215, y=270)

root.mainloop()
