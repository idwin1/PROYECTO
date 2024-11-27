"""import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Configuración de la conexión con MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sandrauno",
    database="pr"
)

# Función para insertar datos en la base de datos
def insertar_datos():
    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO pacientes (nombre, edad, diagnostico, sexo, apoyos, estado_salud, hospital, medico, anio_diagnostico, edad_ingreso, fecha_nacimiento, madre, padre, direccion, telefono) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        # Obtención de datos de los campos de entrada
        nombre = entry_nombre.get()
        edad = entry_edad.get()
        diagnostico = entry_diagnostico.get()
        sexo = entry_sexo.get()
        apoyos = ", ".join([apoyo.get() for apoyo in apoyos_vars if apoyo.get()])
        estado_salud = entry_estado_salud.get()
        hospital = entry_hospital.get()
        medico = entry_medico.get()
        anio_diagnostico = entry_anio_diagnostico.get()
        edad_ingreso = entry_edad_ingreso.get()
        fecha_nacimiento = entry_fecha_nacimiento.get()
        madre = entry_madre.get()
        padre = entry_padre.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()
        
        cursor.execute(sql, (nombre, edad, diagnostico, sexo, apoyos, estado_salud, hospital, medico, anio_diagnostico, edad_ingreso, fecha_nacimiento, madre, padre, direccion, telefono))
        conexion.commit()
        messagebox.showinfo("Éxito", "Datos insertados correctamente")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al insertar datos: {err}")
    finally:
        cursor.close()

# Creación de la ventana principal
ventana = tk.Tk()
ventana.title("Registro de Pacientes")
ventana.geometry("600x400")
ventana.configure(bg="#f0f4f8")

# Configuración de los campos y etiquetas
tk.Label(ventana, text="Nombre", bg="#f0f4f8", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
entry_nombre = tk.Entry(ventana, font=("Arial", 10))
entry_nombre.grid(row=0, column=1, padx=10, pady=5)

tk.Label(ventana, text="Edad", bg="#f0f4f8", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_edad = tk.Entry(ventana, font=("Arial", 10))
entry_edad.grid(row=1, column=1, padx=10, pady=5)

# Campo de diagnóstico
tk.Label(ventana, text="Diagnóstico", bg="#f0f4f8", font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
entry_diagnostico = tk.Entry(ventana, font=("Arial", 10))
entry_diagnostico.grid(row=2, column=1, padx=10, pady=5)

# Campo de sexo
tk.Label(ventana, text="Sexo", bg="#f0f4f8", font=("Arial", 10)).grid(row=3, column=0, sticky="w", padx=10, pady=5)
entry_sexo = ttk.Combobox(ventana, values=["Masculino", "Femenino"], font=("Arial", 10))
entry_sexo.grid(row=3, column=1, padx=10, pady=5)

# Desplegable múltiple para Apoyos
tk.Label(ventana, text="Apoyos", bg="#f0f4f8", font=("Arial", 10)).grid(row=4, column=0, sticky="w", padx=10, pady=5)
apoyos = ["Despensa", "Pediasure", "Sueros", "Productos limpieza", "Ensure", "Productos higiene", "Bloqueadores", "Juguetes"]
apoyos_vars = [tk.StringVar(value="") for _ in apoyos]
for i, apoyo in enumerate(apoyos):
    tk.Checkbutton(ventana, text=apoyo, variable=apoyos_vars[i], bg="#f0f4f8", font=("Arial", 10)).grid(row=4 + i // 3, column=1 + (i % 3), padx=10, pady=5)

# Campos restantes
tk.Label(ventana, text="Estado de Salud", bg="#f0f4f8", font=("Arial", 10)).grid(row=8, column=0, sticky="w", padx=10, pady=5)
entry_estado_salud = tk.Entry(ventana, font=("Arial", 10))
entry_estado_salud.grid(row=8, column=1, padx=10, pady=5)

tk.Label(ventana, text="Hospital", bg="#f0f4f8", font=("Arial", 10)).grid(row=8, column=0, sticky="w", padx=10, pady=5)
entry_hospital = tk.Entry(ventana, font=("Arial", 10))
entry_hospital.grid(row=8, column=1, padx=10, pady=5)

tk.Label(ventana, text="Medico", bg="#f0f4f8", font=("Arial", 10)).grid(row=8, column=0, sticky="w", padx=10, pady=5)
entry_medico = tk.Entry(ventana, font=("Arial", 10))
entry_medico.grid(row=8, column=1, padx=10, pady=5)

tk.Label(ventana, text="Año de diagnostico", bg="#f0f4f8", font=("Arial", 10)).grid(row=8, column=0, sticky="w", padx=10, pady=5)
entry_anio_diagnostico = tk.Entry(ventana, font=("Arial", 10))
entry_anio_diagnostico.grid(row=8, column=1, padx=10, pady=5)

tk.Label(ventana, text="Edad de ingreso", bg="#f0f4f8", font=("Arial", 10)).grid(row=8, column=0, sticky="w", padx=10, pady=5)
entry_edad_ingreso = tk.Entry(ventana, font=("Arial", 10))
entry_edad_ingreso.grid(row=8, column=1, padx=10, pady=5)

tk.Label(ventana, text="Fecha de nacimiento", bg="#f0f4f8", font=("Arial", 10)).grid(row=8, column=0, sticky="w", padx=10, pady=5)
entry_fecha_nacimiento = tk.Entry(ventana, font=("Arial", 10))
entry_fecha_nacimiento.grid(row=8, column=1, padx=10, pady=5)

tk.Label(ventana, text="Nombre de la madre", bg="#f0f4f8", font=("Arial", 10)).grid(row=8, column=0, sticky="w", padx=10, pady=5)
entry_madre = tk.Entry(ventana, font=("Arial", 10))
entry_madre.grid(row=8, column=1, padx=10, pady=5)

tk.Label(ventana, text="Nombre del padre", bg="#f0f4f8", font=("Arial", 10)).grid(row=8, column=0, sticky="w", padx=10, pady=5)
entry_padre = tk.Entry(ventana, font=("Arial", 10))
entry_padre.grid(row=8, column=1, padx=10, pady=5)

tk.Label(ventana, text="Direccion", bg="#f0f4f8", font=("Arial", 10)).grid(row=8, column=0, sticky="w", padx=10, pady=5)
entry_direccion = tk.Entry(ventana, font=("Arial", 10))
entry_direccion.grid(row=8, column=1, padx=10, pady=5)

tk.Label(ventana, text="Telefono", bg="#f0f4f8", font=("Arial", 10)).grid(row=8, column=0, sticky="w", padx=10, pady=5)
entry_telefono = tk.Entry(ventana, font=("Arial", 10))
entry_telefono.grid(row=8, column=1, padx=10, pady=5)


# Botón para insertar datos
btn_insertar = tk.Button(ventana, text="Insertar Datos", command=insertar_datos)
btn_insertar.grid(row=18, column=0, columnspan=2)

ventana.mainloop()
"""

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkcalendar import Calendar 
# Configuración de la conexión con MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sandrauno",
    database="pr"
)

# Función para insertar datos en la base de datos
def insertar_datos():
    try:
        cursor = conexion.cursor()
        sql = "INSERT INTO pacientes (nombre, edad, diagnostico, sexo, apoyos, estado_salud, hospital, medico, anio_diagnostico, edad_ingreso, fecha_nacimiento, madre, padre, direccion, telefono) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        # Obtención de datos de los campos de entrada
        nombre = entry_nombre.get()
        edad = entry_edad.get()
        diagnostico = entry_diagnostico.get()
        sexo = entry_sexo.get()
        apoyos = ", ".join([apoyo.get() for apoyo in apoyos_vars if apoyo.get()])
        estado_salud = entry_estado_salud.get()
        hospital = entry_hospital.get()
        medico = entry_medico.get()
        anio_diagnostico = entry_anio_diagnostico.get()
        edad_ingreso = entry_edad_ingreso.get()
        fecha_nacimiento = entry_fecha_nacimiento.get()
        madre = entry_madre.get()
        padre = entry_padre.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()
        
        cursor.execute(sql, (nombre, edad, diagnostico, sexo, apoyos, estado_salud, hospital, medico, anio_diagnostico, edad_ingreso, fecha_nacimiento, madre, padre, direccion, telefono))
        conexion.commit()
        messagebox.showinfo("Éxito", "Datos insertados correctamente")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al insertar datos: {err}")
    finally:
        cursor.close()


def mostrar_calendario():
    # Crear un pop-up para el calendario
    def seleccionar_fecha():
        fecha_seleccionada.set(cal.get_date())  # Asignar la fecha seleccionada
        ventana_calendario.destroy()  # Cerrar el calendario

    # Crear la ventana emergente para el calendario
    ventana_calendario = tk.Toplevel(ventana)
    ventana_calendario.title("Seleccionar Fecha")

    # Crear el calendario
    cal = Calendar(ventana_calendario, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(padx=20, pady=20)

    # Botón para seleccionar la fecha
    boton_seleccionar = ttk.Button(ventana_calendario, text="Seleccionar", command=seleccionar_fecha)
    boton_seleccionar.pack(pady=10)

# Variable para almacenar la fecha seleccionada 

# Creación de la ventana principal
ventana = tk.Tk()
ventana.title("Registro de Pacientes")
ventana.geometry("600x600")  # Aumenté el tamaño para más espacio
ventana.configure(bg="#f0f4f8")

fecha_seleccionada = tk.StringVar()
# Configuración de las filas y columnas para que se ajusten al tamaño de la ventana
ventana.grid_rowconfigure(0, weight=1)
ventana.grid_rowconfigure(1, weight=1)
ventana.grid_rowconfigure(2, weight=1)
ventana.grid_rowconfigure(3, weight=1)
ventana.grid_rowconfigure(4, weight=1)
ventana.grid_rowconfigure(5, weight=1)
ventana.grid_rowconfigure(6, weight=1)
ventana.grid_rowconfigure(7, weight=1)
ventana.grid_rowconfigure(8, weight=1)
ventana.grid_columnconfigure(0, weight=1)
ventana.grid_columnconfigure(1, weight=3)

# Configuración de los campos y etiquetas
tk.Label(ventana, text="Nombre", bg="#f0f4f8", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
entry_nombre = tk.Entry(ventana, font=("Arial", 10))
entry_nombre.grid(row=0, column=1, padx=10, pady=5)

tk.Label(ventana, text="Edad", bg="#f0f4f8", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_edad = tk.Entry(ventana, font=("Arial", 10))
entry_edad.grid(row=1, column=1, padx=10, pady=5)

tk.Label(ventana, text="Diagnóstico", bg="#f0f4f8", font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
entry_diagnostico = tk.Entry(ventana, font=("Arial", 10))
entry_diagnostico.grid(row=2, column=1, padx=10, pady=5)

tk.Label(ventana, text="Sexo", bg="#f0f4f8", font=("Arial", 10)).grid(row=3, column=0, sticky="w", padx=10, pady=5)
entry_sexo = ttk.Combobox(ventana, values=["Masculino", "Femenino"], font=("Arial", 10))
entry_sexo.grid(row=3, column=1, padx=10, pady=5)

# Desplegable múltiple para Apoyos
tk.Label(ventana, text="Apoyos", bg="#f0f4f8", font=("Arial", 10)).grid(row=4, column=0, sticky="w", padx=10, pady=5)
apoyos = ["Despensa", "Pediasure", "Sueros", "Productos limpieza", "Ensure", "Productos higiene", "Bloqueadores", "Juguetes"]
apoyos_vars = [tk.StringVar(value="") for _ in apoyos]
for i, apoyo in enumerate(apoyos):
    tk.Checkbutton(ventana, text=apoyo, variable=apoyos_vars[i], bg="#f0f4f8", font=("Arial", 10)).grid(row=5 + i // 3, column=1 + (i % 3), padx=10, pady=5)

# Campos restantes
tk.Label(ventana, text="Estado de Salud", bg="#f0f4f8", font=("Arial", 10)).grid(row=6, column=0, sticky="w", padx=10, pady=5)
entry_estado_salud = tk.Entry(ventana, font=("Arial", 10))
entry_estado_salud.grid(row=6, column=1, padx=10, pady=5)

tk.Label(ventana, text="Hospital", bg="#f0f4f8", font=("Arial", 10)).grid(row=7, column=0, sticky="w", padx=10, pady=5)
entry_hospital = tk.Entry(ventana, font=("Arial", 10))
entry_hospital.grid(row=7, column=1, padx=10, pady=5)

tk.Label(ventana, text="Médico", bg="#f0f4f8", font=("Arial", 10)).grid(row=8, column=0, sticky="w", padx=10, pady=5)
entry_medico = tk.Entry(ventana, font=("Arial", 10))
entry_medico.grid(row=8, column=1, padx=10, pady=5)

tk.Label(ventana, text="Año de Diagnóstico", bg="#f0f4f8", font=("Arial", 10)).grid(row=9, column=0, sticky="w", padx=10, pady=5)
entry_anio_diagnostico = tk.Entry(ventana, font=("Arial", 10))
entry_anio_diagnostico.grid(row=9, column=1, padx=10, pady=5)

tk.Label(ventana, text="Edad de Ingreso", bg="#f0f4f8", font=("Arial", 10)).grid(row=10, column=0, sticky="w", padx=10, pady=5)
entry_edad_ingreso = tk.Entry(ventana, font=("Arial", 10))
entry_edad_ingreso.grid(row=10, column=1, padx=10, pady=5)

tk.Label(ventana, text="Fecha Nacimiento Seleccionada", bg="#f0f4f8", font=("Arial", 10)).grid(row=16, column=0, sticky="w", padx=10, pady=5)
entry_fecha_seleccionada = tk.Entry(ventana, textvariable=fecha_seleccionada, font=("Arial", 10), state="readonly")
entry_fecha_seleccionada.grid(row=16, column=1, padx=10, pady=5)
tk.Label(ventana, text="Nombre de la Madre", bg="#f0f4f8", font=("Arial", 10)).grid(row=12, column=0, sticky="w", padx=10, pady=5)
entry_madre = tk.Entry(ventana, font=("Arial", 10))
entry_madre.grid(row=12, column=1, padx=10, pady=5)

tk.Label(ventana, text="Nombre del Padre", bg="#f0f4f8", font=("Arial", 10)).grid(row=13, column=0, sticky="w", padx=10, pady=5)
entry_padre = tk.Entry(ventana, font=("Arial", 10))
entry_padre.grid(row=13, column=1, padx=10, pady=5)

tk.Label(ventana, text="Dirección", bg="#f0f4f8", font=("Arial", 10)).grid(row=14, column=0, sticky="w", padx=10, pady=5)
entry_direccion = tk.Entry(ventana, font=("Arial", 10))
entry_direccion.grid(row=14, column=1, padx=10, pady=5)

tk.Label(ventana, text="Teléfono", bg="#f0f4f8", font=("Arial", 10)).grid(row=15, column=0, sticky="w", padx=10, pady=5)
entry_telefono = tk.Entry(ventana, font=("Arial", 10))
entry_telefono.grid(row=15, column=1, padx=10, pady=5)



# Botón para insertar datos
insertar_btn = tk.Button(ventana, text="Insertar Datos", command=insertar_datos, bg="#4CAF50", fg="white", font=("Arial", 12))
insertar_btn.grid(row=16, column=1, padx=10, pady=20)

# Ejecutar la ventana principal
ventana.mainloop()
