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

    else:
        print(f"No se encontró la opción: {opcion}")
