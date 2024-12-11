import tkinter as tk
from tkinter import ttk, messagebox, Frame, Label
from conexion_bd import conexion
import time


def cargarProductos():
    """Carga los productos y precios desde la base de datos."""
    try:
        conn = conexion()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT r.nombre AS producto, pp.precio
            FROM recetas r
            INNER JOIN precios_productos pp ON r.id = pp.receta_id
        """)
        productos = cursor.fetchall()
        conn.close()
        return productos
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar los productos: {e}")
        return []


def abrir_puntoVentas(rol):
    def agregarProducto(producto):
        """Agrega un producto al carrito o incrementa su cantidad."""
        for item in carrito:
            if item["producto"] == producto:
                item["cantidad"] += 1
                item["total"] = item["cantidad"] * item["precio"]
                actualizarTabla()
                return

        for prod, precio in productos:
            if prod == producto:
                carrito.append({"producto": prod, "cantidad": 1, "precio": precio, "total": precio})
                actualizarTabla()
                return

    def actualizarTabla():
        """Actualiza la tabla del carrito con los productos seleccionados."""
        for widget in carrito_frame.winfo_children():
            widget.destroy()

        total_general = 0

        # Crear encabezados
        encabezados = ["Producto", "Cantidad", "Controles", "Precio Unitario", "Total"]
        for i, encabezado in enumerate(encabezados):
            tk.Label(carrito_frame, text=encabezado, font=("Arial", 12, "bold"), bg="white").grid(row=0, column=i, padx=5, pady=5)

        # Agregar productos al carrito con botones
        for idx, item in enumerate(carrito):
            tk.Label(carrito_frame, text=item["producto"], font=("Arial", 12), bg="white").grid(row=idx + 1, column=0, padx=5, pady=5)
            tk.Label(carrito_frame, text=item["cantidad"], font=("Arial", 12), bg="white").grid(row=idx + 1, column=1, padx=5, pady=5)

            # Botones de control (+, -, eliminar)
            control_frame = tk.Frame(carrito_frame, bg="white")
            control_frame.grid(row=idx + 1, column=2, padx=5, pady=5)

            tk.Button(control_frame, text="+", command=lambda p=item: actualizarCantidad(p, 1), width=3).pack(side="left")
            tk.Button(control_frame, text="-", command=lambda p=item: actualizarCantidad(p, -1), width=3).pack(side="left")
            tk.Button(control_frame, text="Eliminar", command=lambda p=item: eliminarProducto(p), width=6, bg="red", fg="white").pack(side="left")

            tk.Label(carrito_frame, text=f"${item['precio']:.2f}", font=("Arial", 12), bg="white").grid(row=idx + 1, column=3, padx=5, pady=5)
            tk.Label(carrito_frame, text=f"${item['total']:.2f}", font=("Arial", 12), bg="white").grid(row=idx + 1, column=4, padx=5, pady=5)

            total_general += item["total"]

        total_label.config(text=f"Total: ${total_general:.2f}")

    def actualizarCantidad(producto, cantidad):
        """Actualiza la cantidad de un producto en el carrito."""
        producto["cantidad"] += cantidad
        if producto["cantidad"] <= 0:
            eliminarProducto(producto)
        else:
            producto["total"] = producto["cantidad"] * producto["precio"]
        actualizarTabla()

    def eliminarProducto(producto):
        """Elimina un producto del carrito."""
        carrito.remove(producto)
        actualizarTabla()

    def cobrar():
        """Realiza el cobro y limpia el carrito."""
        if not carrito:
            messagebox.showwarning("Advertencia", "El carrito está vacío.")
            return

        total_general = sum(item["total"] for item in carrito)
        messagebox.showinfo("Cobro exitoso", f"El total a pagar es: ${total_general:.2f}")
        carrito.clear()
        actualizarTabla()

    # Crear la ventana principal
    root = tk.Tk()
    root.title("Punto de Venta")
    root.geometry("1000x600")
    root.configure(bg="#F9F9F9")

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
        frame_opcion = Frame(menu_lateral, bg="#333333")  # Fondo gris oscuro para cada opción
        frame_opcion.pack(fill="x", pady=1)
        # Icono y texto de la opción
        etiqueta = Label(frame_opcion, text=f"{opcion['icono']} {opcion['texto']}", anchor="w", padx=10, 
                         bg="#333333", fg="#ffffff", font=("Arial", 10, "bold"))  # Texto en blanco y fuente negrita
        etiqueta.pack(fill="x")
        # Agregar evento para seleccionar opción
        ventana = root
        etiqueta.bind("<Button-1>", lambda e, texto=opcion['texto']: destruir(texto, ventana, rol))

    main_frame = tk.Frame(root, bg="white", padx=20, pady=20)
    main_frame.pack(side="right", fill="both", expand=True)

    title_label = tk.Label(main_frame, text="Punto de Venta", bg="white", font=("Arial", 20, "bold"), fg="#333333")
    title_label.pack(pady=10)

    productos = cargarProductos()
    if not productos:
        return

    productos_frame = tk.Frame(main_frame, bg="white", width=100)
    productos_frame.pack(side="left", fill="both", padx=10, pady=10)

    tk.Label(productos_frame, text="Productos", bg="white", font=("Arial", 14, "bold")).pack(pady=10)

    # Frame para productos scrollables
    productos_scrollable_frame = tk.Frame(productos_frame, bg="white")
    productos_scrollable_frame.pack(side="left", fill="both", expand=True)

    for prod, precio in productos:
        tk.Button(
            productos_scrollable_frame,
            text=f"{prod}\n${precio:.2f}",
            font=("Arial", 12),
            width=20,
            height=2,
            command=lambda p=prod: agregarProducto(p)
        ).pack(pady=2)

    # Frame para el carrito
    carrito_frame = tk.Frame(main_frame, bg="white", pady=10)
    carrito_frame.pack(side="left", fill="both", expand=True, padx=10)

    total_frame = tk.Frame(main_frame, bg="white", pady=10)
    total_frame.pack(fill="x", side="bottom")

    total_label = tk.Label(total_frame, text="Total: $0.00", bg="white", font=("Arial", 16, "bold"), fg="#333333")
    total_label.pack(side="right", padx=10)

    cobrar_button = tk.Button(total_frame, text="Cobrar", bg="#DC3545", fg="white", font=("Arial", 16), command=cobrar)
    cobrar_button.pack(side="right", padx=10)

    carrito = []

    root.mainloop()


def destruir(texto, root,rol):
    from funcionalidad import seleccionar_opcion
    root.destroy()
    print("texto")
    print(rol)
    time.sleep(1)
    seleccionar_opcion(texto,rol)
