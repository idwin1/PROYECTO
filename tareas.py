from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # Importamos Pillow
from funcionalidad import seleccionar_opcion

import tkinter as tk
from tkinter import ttk

def abrir_tareas(rol):
    # Crear la ventana principal
    root = tk.Tk()
    root.title('Tareas')
    root.geometry('950x500+300+200')
    root.configure(bg="#f4f4f9")
    root.resizable(False, False)

    menu_lateral = tk.Frame(root, bg="#333", width=150)
    menu_lateral.pack(side="left", fill="y")
    frame_central = Frame(root, bg="#fff")
    frame_central.pack(side="right", expand=True, fill="both")


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
        frame_opcion = tk.Frame(menu_lateral, bg="#333")
        frame_opcion.pack(fill="x", pady=1)

        etiqueta = tk.Label(frame_opcion, text=f"{opcion['icono']} {opcion['texto']}", anchor="w", padx=10, bg="#333", fg="#fff", font=('Helvetica', 10, 'bold'))
        etiqueta.pack(fill="x")

        if opcion.get("notificacion"):
            notificacion = tk.Label(frame_opcion, text="●", fg="red", bg="#333", anchor="e")
            notificacion.pack(side="right", padx=5)

        ventana = root
        etiqueta.bind("<Button-1>", lambda e, texto=opcion['texto']: destruir(texto, ventana,rol))
    root.mainloop()

def destruir(texto,root,rol) :
    root.destroy()
    seleccionar_opcion(texto,rol)
    print("se elimino")
    
# Ejecutar el bucle principal de la aplicación
