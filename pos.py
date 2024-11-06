from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector

class PuntoDeVenta:
    def __init__(self, root):
        self.root = root
        self.root.title("Punto de Venta")
        self.root.geometry("800x600")
        self.carrito = []
        
        # Conectar a la base de datos
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sandrauno",  # Cambia esto a la contraseña correspondiente
            database="cafe"
        )
        self.cursor = self.db.cursor()
        
        # Configuración de la interfaz
        self.configurar_interfaz()
        self.crear_menu_lateral()
        self.cargar_lista_productos()
        
    def configurar_interfaz(self):
        # Marco para productos y carrito
        self.productos_frame = Frame(self.root, width=400, height=600)
        self.productos_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.carrito_frame = Frame(self.root, width=300, height=600, bg="lightgrey")
        self.carrito_frame.pack(side=RIGHT, fill=BOTH)

        # Campo de búsqueda
        self.search_var = StringVar()
        search_entry = Entry(self.productos_frame, textvariable=self.search_var)
        search_entry.pack(pady=10)
        search_button = Button(self.productos_frame, text="Buscar", command=self.buscar_producto)
        search_button.pack()

    def crear_menu_lateral(self):
        # Menú lateral
        menu_lateral = Frame(self.root, bg="lightblue", width=100)
        menu_lateral.pack(side=LEFT, fill=Y)
        
        # Botones del menú lateral
        btn_inventario = Button(menu_lateral, text="Inventario", command=self.mostrar_inventario)
        btn_inventario.pack(pady=10, padx=10, fill=X)
        btn_ventas = Button(menu_lateral, text="Ventas", command=self.mostrar_ventas)
        btn_ventas.pack(pady=10, padx=10, fill=X)

    def cargar_lista_productos(self):
        # Consulta de productos con precios
        consulta = """
            SELECT r.ID, r.Nombre, p.precio 
            FROM recetas r 
            JOIN precios_productos p ON r.ID = p.receta_id
        """
        self.cursor.execute(consulta)
        productos = self.cursor.fetchall()
        
        # Listar los productos en la interfaz
        for producto in productos:
            producto_id, nombre, precio = producto
            boton_producto = Button(self.productos_frame, text=f"{nombre} - ${precio:.2f}", 
                                    command=lambda p=producto: self.agregar_al_carrito(p))
            boton_producto.pack(anchor=W)

    def buscar_producto(self):
        # Búsqueda de productos
        buscar = self.search_var.get()
        consulta = """
            SELECT r.ID, r.Nombre, p.precio 
            FROM recetas r 
            JOIN precios_productos p ON r.ID = p.receta_id 
            WHERE r.Nombre LIKE %s
        """
        self.cursor.execute(consulta, (f"%{buscar}%",))
        productos = self.cursor.fetchall()
        
        # Actualizar productos mostrados
        for widget in self.productos_frame.winfo_children():
            widget.destroy()
        for producto in productos:
            producto_id, nombre, precio = producto
            boton_producto = Button(self.productos_frame, text=f"{nombre} - ${precio:.2f}", 
                                    command=lambda p=producto: self.agregar_al_carrito(p))
            boton_producto.pack(anchor=W)

    def agregar_al_carrito(self, producto):
        producto_id, nombre, precio = producto
        self.carrito.append({"id": producto_id, "nombre": nombre, "precio": precio})
        self.mostrar_carrito()

    def mostrar_carrito(self):
        for widget in self.carrito_frame.winfo_children():
            widget.destroy()

        total = 0
        for item in self.carrito:
            frame_producto = Frame(self.carrito_frame)
            frame_producto.pack(anchor=W, pady=2)

            label_producto = Label(frame_producto, text=f"{item['nombre']} - ${item['precio']:.2f}")
            label_producto.pack(side=LEFT)
            boton_eliminar = Button(frame_producto, text="X", command=lambda p=item: self.eliminar_producto(p))
            boton_eliminar.pack(side=RIGHT)

            total += item['precio']

        Label(self.carrito_frame, text=f"Total: ${total:.2f}", bg="lightgrey").pack(anchor=W, pady=10)
        Button(self.carrito_frame, text="Continuar", command=self.procesar_compra).pack(pady=10)

    def eliminar_producto(self, producto):
        self.carrito.remove(producto)
        self.mostrar_carrito()

    def procesar_compra(self):
        # Función para procesar la compra
        messagebox.showinfo("Compra", "Compra procesada exitosamente")
        self.carrito.clear()
        self.mostrar_carrito()

    def mostrar_inventario(self):
        # Mostrar inventario (ejemplo)
        messagebox.showinfo("Inventario", "Mostrando inventario")

    def mostrar_ventas(self):
        # Mostrar ventas (ejemplo)
        messagebox.showinfo("Ventas", "Mostrando ventas")
    
    
# Configuración y ejecución de la interfaz


def abrir_puntoVentas(rol):
    global root
    global role 
    role = rol
    root = Tk()
    root.iconbitmap("punto de ventas.ico")
    app = PuntoDeVenta(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def on_closing():
    from funcionalidad import seleccionar_opcion  
    print("La ventana se ha cerrado.")  
    root.destroy()
    seleccionar_opcion("pagina_principal",role)  

"""
CREATE TABLE precios_productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    receta_id INT,
    precio DECIMAL(10, 2),
    FOREIGN KEY (receta_id) REFERENCES recetas(ID)
);

INSERT INTO precios_productos (receta_id, precio) VALUES (1, 50.00); -- precio para la receta con ID 1
INSERT INTO precios_productos (receta_id, precio) VALUES (2, 30.00); -- precio para la receta con ID 2
"""