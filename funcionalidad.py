import time

def seleccionar_opcion(opcion):
    if opcion == "Recompensas":
        from Recompensas import abrir_interfaz_Recompensas  # Importa solo cuando se necesite
        print("Abriendo interfaz de recompensas...")
        time.sleep(1)
        abrir_interfaz_Recompensas()  # Llamar directamente a la función

    elif opcion == "pagina_principal":
        from Pagina_principal import abrir_pagina_principal  # Importa solo cuando se necesite
        print("Abriendo página principal...")
        abrir_pagina_principal()

    elif opcion == "Reportes":
        from Reportes import abrir_interfaz_Reportes  # Importa solo cuando se necesite
        print("Abriendo interfaz de reportes...")
        abrir_interfaz_Reportes()
        
    elif opcion == "Estadísticas":
        print("abriendo Estadisticas")
    elif opcion == "Usuarios":
        print("abriendo Usuarios") 
    elif opcion == "Tareas":
        print("abriendo Tareas")   
    elif opcion == "Inventario":
        from Buscar_productos import abrir_Buscar_Productos
        print("abriendo BUSCAR PRODUCTOS")
        abrir_Buscar_Productos()
    else:
        print(f"No se encontró la opción: {opcion}")
