from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # Importamos Pillow

import time
import tkinter as tk
from tkinter import ttk


def abrir_interfaz_Recompensas():
    root = tk.Tk()
    root.title("Recompensas")
    root.geometry("650x500")

    # Crear el marco para el menú lateral
    menu_frame = tk.Frame(root, bg="#333333", width=150)
    menu_frame.pack(side="left", fill="y")

    # Opciones del menú lateral
    menu_options = ["Recompensas", "Usuarios", "Tareas", "Inventario", "Recetas"]
    for option in menu_options:
        button = tk.Button(menu_frame, text=option, bg="#333333", fg="white", bd=0, font=("Arial", 10), anchor="w")
        button.pack(fill="x", padx=10, pady=5)
        button.bind("<Button-1>", lambda e, texto=option: destruir(texto, root))
    root.mainloop()

def destruir(texto,root):
    from funcionalidad import seleccionar_opcion
    root.destroy()
    print(texto)
    time.sleep(1)
    seleccionar_opcion(texto)
    
# Ejecutar el bucle principal de la aplicación

