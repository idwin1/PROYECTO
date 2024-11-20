import tkinter as tk
from tkinter import ttk, messagebox
from conexion_bd import conexion


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

    menu_frame = tk.Frame(root, bg="#333333", width=150)
    menu_frame.pack(side="left", fill="y")

    if rol == "A":
        menu_options = ["Recompensas", "Usuarios", "Tareas", "Inventario", "Recetas", "Punto ventas", "Cerrar sesión"]
    else:
        menu_options = ["Recompensas", "Tareas", "Inventario", "Recetas", "Punto ventas", "Cerrar sesión"]

    for option in menu_options:
        button = tk.Button(menu_frame, text=option, bg="#333333", fg="white", bd=0, font=("Arial", 12), anchor="w")
        button.pack(fill="x", padx=10, pady=10)
        button.bind("<Button-1>", lambda e, texto=option: destruir(texto, root, rol))

    main_frame = tk.Frame(root, bg="white", padx=20, pady=20)
    main_frame.pack(side="right", fill="both", expand=True)

    title_label = tk.Label(main_frame, text="Punto de Venta", bg="white", font=("Arial", 20, "bold"), fg="#333333")
    title_label.pack(pady=10)

    productos = cargarProductos()
    if not productos:
        return

    productos_frame = tk.Frame(main_frame, bg="white")
    productos_frame.pack(side="left", padx=10, pady=10)

    tk.Label(productos_frame, text="Productos", bg="white", font=("Arial", 14, "bold")).pack(pady=10)

    for prod, precio in productos:
        tk.Button(
            productos_frame,
            text=f"{prod}\n${precio:.2f}",
            font=("Arial", 12),
            width=20,
            height=2,
            command=lambda p=prod: agregarProducto(p)
        ).pack(pady=5)

    # Scrollable Frame
    canvas = tk.Canvas(main_frame, bg="white")
    scroll_y = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    carrito_frame = scrollable_frame

    # Total directamente debajo de la tabla de productos
    total_frame = tk.Frame(main_frame, bg="white", pady=10)
    total_frame.pack(fill="x", side="bottom")

    total_label = tk.Label(total_frame, text="Total: $0.00", bg="white", font=("Arial", 16, "bold"), fg="#333333")
    total_label.pack(side="right", padx=10)

    cobrar_button = tk.Button(total_frame, text="Cobrar", bg="#DC3545", fg="white", font=("Arial", 16), command=cobrar)
    cobrar_button.pack(side="right", padx=10)

    carrito = []

    root.mainloop()


def destruir(texto, root, rol):
    from funcionalidad import seleccionar_opcion
    root.destroy()
