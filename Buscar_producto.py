from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # Importamos Pillow
import mysql.connector


import tkinter as tk
from tkinter import ttk

def seleccionar_opcion(opcion):
    print(f"Opción seleccionada: {opcion}")

# Crear la ventana principal
root = tk.Tk()
root.title('Buscar Productos')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

# Crear el frame del menú lateral
menu_lateral = tk.Frame(root, bg="#f0f0f0", width=150)
menu_lateral.pack(side="left", fill="y")

# Crear las opciones del menú
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
    etiqueta.bind("<Button-1>", lambda e, texto=opcion['texto']: seleccionar_opcion(texto))

# Ejecutar el bucle principal de la aplicación
root.mainloop()
