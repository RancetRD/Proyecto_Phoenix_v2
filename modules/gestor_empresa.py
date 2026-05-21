from modules.validaciones import campo_texto, campo_float,campo_rnc
from modules.base_datos import obtener_empresas_db, actualizar_empresa_db, eliminar_empresa_db

def gestor_empresa():
    
    lista_db = obtener_empresas_db()

    if not lista_db:
        print("No hay empresa que actulizar")
        return
    for indice,fila in enumerate(lista_db,start=1):
        print(f"[{indice}] - Empresa: {fila[1]} | RNC: {fila[2]}")
    
   
    seleccion = campo_float("Introduce el mumero de la empresa a editar")
    seleccion_entera = int(seleccion)
    indice_python = seleccion_entera -1
    if seleccion_entera< 1 or seleccion_entera > len(lista_db):
        print("Error numero fuera de rango")
        return
    empresa_elegida = lista_db[indice_python]
    id_real_empresa = empresa_elegida[0]
    print("El usuario eligió la opción:", seleccion)
    print(f"\n✅ Empresa seleccionada con éxito.")
    print(f"ID Real en Base de Datos: {id_real_empresa}")
    print(f"Nombre actual: {empresa_elegida[1]}")

    nuevo_nombre = campo_texto("Introduzca el nuevo nombre de la empresa").strip().upper()
    nuevo_rnc = campo_rnc("introduzca su nuevo RNC").strip().upper()
    print("Selecciona 1-Ordinario , 2-RST")
    while True:
        
        opciones = campo_texto("Selecciona 1-Ordinario , 2-RST: ").strip()
        if opciones not in ("1","2"):
            print("Error , debe seleccionar 1 o 2")
            continue
        else:
            print("Cualquier otro numero le pedira de nuevo Ordinario o RST")
        
        if opciones =="1":
            nuevo_regimen = "ordinario"
            print("Usted a seleccionado Ordinario")
            break
        elif opciones =="2":
            nuevo_regimen = "rst"
            print("Usted a seleccionado RST")
            break
        
    actualizar_empresa_db(nuevo_nombre, nuevo_rnc, nuevo_regimen, id_real_empresa)
    print("\n✅ ¡Empresa actualizada exitosamente en el Proyecto Phoenix!")

    

def eliminar_empresa():

    lista_db = obtener_empresas_db()

    if not lista_db:
        print("No hay empresa que eliminar")
    
        return
    for indice,fila in enumerate(lista_db,start=1):
        print(f"[{indice}] - Empresa: {fila[1]} | RNC: {fila[2]}")
    
    seleccion = campo_float("Introduce el mumero de la empresa a eliminar!")
    seleccion_entera = int(seleccion)
    indice_python = seleccion_entera -1
    if seleccion_entera< 1 or seleccion_entera > len(lista_db):
        print("Error numero fuera de rango")
        return
            
    empresa_elegida = lista_db[indice_python]
    id_real_empresa = empresa_elegida[0]
    print("El usuario eligió la opción:", seleccion)
    print(f"\n✅ Empresa seleccionada con éxito.")
    print(f"ID Real en Base de Datos: {id_real_empresa}")
    print(f"Nombre actual: {empresa_elegida[1]}")

    while True:
        
        opciones = campo_texto("Introduzca si o no para confirmar la eliminacion").strip().lower()
        if opciones not in ("si","no"):
            print("Error , debe seleccionar SI O NO")
            continue
        else:
            print("Cualquier opcion sera rechazada")
        
        if opciones =="si":
            eliminar_empresa_db(id_real_empresa)
            print("Empresa eliminada para siempre")
            
            break
        elif opciones =="no":
            print("Operacion cancelada")
            break
    
    