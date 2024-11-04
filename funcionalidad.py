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
    elif opcion == "Usuarios":
        from usuarios import abrir_usuarios
        print("abriendo Usuarios")
        print("entron a la opcion de usuarios") 
        abrir_usuarios()
    elif opcion == "Tareas":
        print("abriendo Tareas")   
    elif opcion == "Inventario":
        from inventario import abrir_inventario
        print("abriendo BUSCAR PRODUCTOS")
        abrir_inventario()
    elif opcion == "Recetas":
        from recetas import abrir_recetas
        print("abriendo Recetas")
        abrir_recetas()
    else:
        print(f"No se encontró la opción: {opcion}")
