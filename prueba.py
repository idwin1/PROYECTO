#from tkinter import ttk
import tkinter as tk

fondo_entrar = "#004AAD"
fondo_salir = "#FF1616"
fondo_correcto = "#8C52FF"
fondo_incorrecto = "#FF5757"
fondo_entrada = "#D9D9D9"



ventana = tk.Tk()
ventana.title("login")
ventana.geometry("500x500+500+50")
ventana.resizable(width=False, height=False)
#fondo = tk.PhotoImage(file="entrada.png")
#fondo1 = tk.Label(ventana,image=fondo).place(x=0,y=0,relwidth=1,relheight=1)

usuario = tk.StringVar()
password = tk.StringVar()


def login():
    nombre = usuario.get()
    contraseña =password.get()

def salir():
    ventana.destroy()

#Entradas
entrada = tk.Entry(ventana,textvar=usuario,width=22,relief="flat",bg=fondo_entrada)
entrada.place(x=255,y=204)

entrada1 = tk.Entry(ventana,textvar=password,width=22,relief="flat",bg=fondo_entrada,show="*")
entrada1.place(x=255,y=244)

#Botones
boton = tk.Button(ventana, text="Entrar",cursor="hand2",bg =fondo_entrar, width=12,relief="flat",font=("Comic Sans MS",12,"bold"))
boton.place(x=60,y=400)


boton1= tk.Button(ventana, text="salir",command=salir,cursor="hand2",bg = fondo_salir,width=12,relief="flat",font=("Comic Sans MS",12, "bold"))

boton1.place(x=310,y=400)
ventana.mainloop()