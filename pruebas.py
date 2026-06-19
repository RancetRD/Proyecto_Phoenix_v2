while True:
    identifacion_ajustero = input("Introduzca el numero de identificacion CEDULA O PASAPORTE: ")

    longitud = len(identifacion_ajustero)

    if 6 <= longitud <= 13:
        print("Rango Permitido")
        break
    else:
        print("Debe introducir un rango de caracteres entre 6 y 13")