import time

def seleccionar_opcion(opcion,rol):
    if opcion == "Recompensas":
        from Recompensas import abrir_interfaz_Recompensas  # Importa solo cuando se necesite
        print("Abriendo interfaz de recompensas...")
        time.sleep(1)
        abrir_interfaz_Recompensas(rol)  # Llamar directamente a la función
    elif opcion == "pagina_principal":
        from Pagina_principal import abrir_pagina_principal  # Importa solo cuando se necesite
        print("Abriendo página principal...")
        abrir_pagina_principal(rol)
    elif opcion == "Usuarios" and rol == "A":
        from usuarios import abrir_usuarios
        print("abriendo Usuarios")
        print("entron a la opcion de usuarios") 
        abrir_usuarios(rol)
    elif opcion == "Tareas":
        from tareas import abrir_tareas
        print("abriendo Tareas") 
        abrir_tareas(rol)
    elif opcion == "Inventario":
        from inventario import abrir_inventario
        print("abriendo BUSCAR PRODUCTOS")
        abrir_inventario(rol)
    elif opcion == "Recetas":
        from recetas import abrir_recetas
        print("abriendo Recetas")
        abrir_recetas(rol)
    else:
        print(f"No se encontró la opción: {opcion}")
