"""
import tkinter as tk
import serial
import time

# Configuración del puerto Bluetooth y la velocidad (ajusta el puerto según tu sistema)
# Cambia 'COM3' a tu puerto Bluetooth (en Linux podría ser '/dev/rfcomm0')
ser = serial.Serial('COM3', 9600)  # Reemplaza 'COM3' con el puerto Bluetooth de tu HC-06
time.sleep(2)  # Espera para que se establezca la conexión

def enviar_comando(comando):
    ser.write(str(comando).encode())
    print(f"Enviado: {comando}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Control Bluetooth Arduino")
ventana.geometry("300x400")

# Función para enviar comandos del 1 al 9
for i in range(1, 10):
    boton = tk.Button(ventana, text=f"Instrucción {i}", font=("Arial", 12),
                      command=lambda i=i: enviar_comando(i))
    boton.pack(pady=5, fill=tk.BOTH, expand=True)

# Iniciar la ventana
ventana.mainloop()
ser.close()
"""

import serial
import tkinter as tk
from tkinter import messagebox

# Configuración de la conexión serial
def conectar_serial():
    global ser
    try:
        ser = serial.Serial('COM3', 9600)  # Cambia 'COM3' por el puerto al que está conectado tu HC-06
        messagebox.showinfo("Conexión", "Conexión serial establecida.")
    except Exception as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar al módulo: {e}")

# Función para enviar el número seleccionado al módulo HC-06
def enviar_numero(numero):
    try:
        ser.write(f"{numero}\n".encode())  # Envía el número al módulo
        messagebox.showinfo("Enviado", f"Número {numero} enviado al módulo.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo enviar el número: {e}")

# Configuración de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Interfaz Serial")
ventana.geometry("300x400")

# Botones del 1 al 10
for i in range(1, 11):
    boton = tk.Button(ventana, text=str(i), command=lambda i=i: enviar_numero(i), width=10, height=2)
    boton.pack(pady=5)

# Botón para conectar serial
boton_conectar = tk.Button(ventana, text="Conectar Serial", command=conectar_serial, bg="blue", fg="white")
boton_conectar.pack(pady=20)

ventana.mainloop()
