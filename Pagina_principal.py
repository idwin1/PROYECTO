from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # Importamos Pillow

import tkinter as tk
from tkinter import ttk

def abrir_pagina_principal(rol):  
# Crear la ventana principal
    root = tk.Tk()
    root.title('Pagina_Principal')
    root.geometry('925x500+300+200')
    root.configure(bg="#fff")
    root.resizable(False, False)

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
        {"texto": "Recetas", "icono": "🗒️"}
        ]
    else:
        opciones_menu = [
        {"texto": "Recompensas", "icono": "★"},
        {"texto": "Tareas", "icono": "📝"},
        {"texto": "Inventario", "icono": "📦"},
        {"texto": "Recetas", "icono": "🗒️"}
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

    root.mainloop()

def destruir(texto,root,rol) :
    from funcionalidad import seleccionar_opcion
    root.destroy()
    print("entro a pagina principal")
    print(rol)
    seleccionar_opcion(texto,rol)

    
# Ejecutar el bucle principal de la aplicación
