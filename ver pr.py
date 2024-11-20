"""import tkinter as tk
from tkinter import ttk
import mysql.connector

# Configuración de la conexión con MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sandrauno",
    database="pr"
)

# Función para cargar los datos en el Treeview
def cargar_datos():
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM pacientes")
    datos = cursor.fetchall()
    
    for row in datos:
        treeview.insert("", "end", values=row)
    
    cursor.close()

# Ventana para visualizar los datos
ventana = tk.Tk()
ventana.title("Visualizar Pacientes")
ventana.geometry("800x600")

# Crear el Treeview para mostrar los datos
columns = ("ID", "Nombre", "Edad", "Diagnóstico", "Sexo", "Apoyos", "Estado Salud", "Hospital", "Médico", "Año Diagnóstico", "Edad Ingreso", "Fecha Nacimiento", "Madre", "Padre", "Dirección", "Teléfono")
treeview = ttk.Treeview(ventana, columns=columns, show="headings", height=15)
treeview.pack(padx=20, pady=20, fill="both", expand=True)

# Definir encabezados
for col in columns:
    treeview.heading(col, text=col, anchor="w")
    treeview.column(col, width=120)

# Botón para cargar los datos
btn_cargar = tk.Button(ventana, text="Cargar Datos", command=cargar_datos, font=("Arial", 12), bg="#4CAF50", fg="white")
btn_cargar.pack(pady=10)

ventana.mainloop()
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

# Configuración de la conexión con MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sandrauno",
    database="pr"
)

# Función para cargar los datos en el Treeview
def cargar_datos():
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM pacientes")
    datos = cursor.fetchall()
    
    for row in datos:
        treeview.insert("", "end", values=row)
    
    cursor.close()

# Función para mostrar los datos detallados al hacer clic
def mostrar_detalles(event):
    # Obtener el ítem seleccionado
    selected_item = treeview.selection()
    if selected_item:
        item_data = treeview.item(selected_item[0])['values']
        detalles = "\n".join([f"{columns[i]}: {item_data[i]}" for i in range(len(item_data))])

        # Crear una nueva ventana para mostrar los detalles
        detalles_ventana = tk.Toplevel(ventana)
        detalles_ventana.title("Detalles del Paciente")
        detalles_ventana.geometry("600x400")

        # Crear un widget de texto para mostrar los detalles
        text = tk.Text(detalles_ventana, wrap=tk.WORD, font=("Arial", 12), height=15, width=60)
        text.pack(padx=10, pady=10)
        text.insert(tk.END, detalles)
        text.config(state=tk.DISABLED)  # Deshabilitar la edición

        # Agregar un botón de cierre
        btn_cerrar = tk.Button(detalles_ventana, text="Cerrar", command=detalles_ventana.destroy, font=("Arial", 12), bg="#FF6347", fg="white")
        btn_cerrar.pack(pady=10)

# Ventana para visualizar los datos
ventana = tk.Tk()
ventana.title("Visualizar Pacientes")
ventana.geometry("800x600")

# Crear el Treeview para mostrar los datos
columns = ("ID", "Nombre", "Edad", "Diagnóstico", "Sexo", "Apoyos", "Estado Salud", "Hospital", "Médico", "Año Diagnóstico", "Edad Ingreso", "Fecha Nacimiento", "Madre", "Padre", "Dirección", "Teléfono")
treeview = ttk.Treeview(ventana, columns=columns, show="headings", height=15)
treeview.pack(padx=20, pady=20, fill="both", expand=True)

# Definir encabezados
for col in columns:
    treeview.heading(col, text=col, anchor="w")
    treeview.column(col, width=120)

# Asociar la función para mostrar los detalles al hacer clic
treeview.bind("<ButtonRelease-1>", mostrar_detalles)

# Botón para cargar los datos
btn_cargar = tk.Button(ventana, text="Cargar Datos", command=cargar_datos, font=("Arial", 12), bg="#4CAF50", fg="white")
btn_cargar.pack(pady=10)

ventana.mainloop()
