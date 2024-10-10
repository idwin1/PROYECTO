
def seleccionar_opcion(opcion):
    from Recompensas import abrir_interfaz_Recompensas
    from Pagina_principal import abrir_pagina_principal

    print(opcion)

    print(f"Opción seleccionada: {opcion}")
    if opcion == "Recompensas" :
        abrir_interfaz_Recompensas()
    elif opcion == "pagina_principal" :
        abrir_pagina_principal()
    else :
        abrir_interfaz_Recompensas()

    
    
