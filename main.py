from modules.validaciones import *
from modules.base_datos import inicializar_base_datos,cargar_empresas_guardadas
from modules.bodega import registrar_nueva_empresa, agregar_banco,Empresa
from modules.pagos import procesar_debito_banco
from modules.contabilidad import mostrar_historial
from modules.factura import Factura  
from modules.nominas import Empleado
from modules.terceros import listar_terceros, flujo_registro_tercero,flujo_eliminar_tercero
from modules.base_datos import obtener_empresas_db,cargar_factura_db
from modules.gestor_empresa import gestor_empresa, eliminar_empresa
from modules.consultas import buscar_facturas, buscar_por_id
from modules.reportes import reporte_facturas,generar_reporte_ajusteros
from modules.operaciones import (
    registrar_gasto,
    registrar_telecom,
    registrar_restaurante,
    registrar_pago_global,
    registrar_cotizacion,
    registrar_proforma,
    convertir_proforma_cotizacion_606,
    convertir_proformar_a_factura_607,
    reporte_ajustero
    
)
mis_empresas = []
empresa_activa = None
inicializar_base_datos()
datos_descargados = cargar_empresas_guardadas()
for fila in datos_descargados:
    id_db = fila[0]
    nombre_db = fila[1]
    rnc_db = fila[2]
    regimen_db =fila[3]
    empresa_armada = Empresa(id_db,nombre_db,rnc_db,regimen_db)
    mis_empresas.append(empresa_armada)
while True:
    print("\n==============================")
    print("      SISTEMA PHOENIX")
    print("==============================")
    print
    if empresa_activa:
        print(f"Sesion: {empresa_activa.nombre} | RNC: {empresa_activa.rnc}")
    else:
       print("Sesion: [NINGUNA EMPRESA SELECCIONADA]")

    print("1- Crear empresa")
    print("2-Seleccionar empresa(Login)")
    print("3-Registrar gasto (606)")
    print("4-Registrar Telecomunicaciones")
    print("5-Registrar Restaurante")
    print("6-Aplicar Pago")
    print("7- Registrar Cotización")
    print("8- Registrar Proforma")
    print("9- Convertir Proforma a Factura")
    print("10- Registrar Banco")
    print("11- Salir del sistema")
    print("12-Historial de pagos")
    print("13-Reporte ajusteros")
    print("14-Nominas")
    print("15-Buscar por ID o NCF")
    print("16-Editar Empresa")
    print("17-Eliminar Empresa")
    print("18-Registrar Proveedor")
    print("19-ver proveedor")
    print("20-Eliminar Proveedor")
    print("21-Reporte Facturas")
    print("22-Reporte de los  Ajusteros Totales")
    opciones = input("Seleccione la opcion que mas desee--->").strip()
    if opciones not in [str(i) for i in range(1, 25)]:
        print("ERROR: SELECCIONE UNA OPCIÓN VÁLIDA (1-25)")
        continue

    elif opciones == "1":
        def ejecutar_opcion_1():
            resultado = registrar_nueva_empresa(mis_empresas)
            if resultado is not None:
                mis_empresas.append(resultado)
                print("Empresa guardada con exito")
            else:
                print("Registro cancelado: El RNC ya existe")
        
        ejecutar_seguro(ejecutar_opcion_1)
    
    elif opciones == "2":
        def ejecutar_opcion_2():
            lista_db = obtener_empresas_db()

            if not lista_db:
                print("No hay registros todavia")
            else:
                print("Listas de empresas")
                for emp in lista_db:
                    print(f"ID: {emp[0]} - {emp[1]}")
                
                try:
                    id_buscar = int(input("Ingrese el ID para entrar: "))
                    encontrada = False
                    
                    for emp in lista_db:
                        if str(emp[0]) == str(id_buscar):  
                            for obj_empresa in mis_empresas:
                                if str(obj_empresa.id_empresa) == str(id_buscar) or  obj_empresa.rnc == emp[2]:
                                    obj_empresa.id_empresa = emp[0]
                                    obj_empresa.nombre = emp [1]
                                    obj_empresa.rnc = emp[2]
                                    obj_empresa.regimen = emp[3]

                                    global empresa_activa
                                    empresa_activa = obj_empresa
                                    cargar_factura_db(empresa_activa)
                                    
                                encontrada = True

                                print(f"\n[OK] Bienvenido de nuevo a la empresa #{emp[0]}--{emp[1]}")
                                break  
                                
                    if not encontrada:
                        print("ID no encontrado")
                        
                except ValueError:
                    print("Por favor, Ingrese un numero ID valido")

        
        ejecutar_seguro(ejecutar_opcion_2)
    elif opciones == "3":
        if empresa_activa:
            # En lugar de registrar_gasto(empresa_activa), lo envuelves:
            ejecutar_seguro(registrar_gasto, empresa_activa)
        else:
            print("Error: Debe crear o seleccionar una empresa primero")
    
    elif opciones == "4":
        def ejecutar_opcion_4():
            if empresa_activa:
                registrar_telecom(empresa_activa)
            else:
                print("Error: Seleccione una empresa primero")
        
        ejecutar_seguro(ejecutar_opcion_4)

    elif opciones == "5":
        def ejecutar_opcion_5():
            if empresa_activa:
                registrar_restaurante(empresa_activa)
            else:
                print("Error:Seleccione una empresa primero")
        
        ejecutar_seguro(ejecutar_opcion_5)
    
    elif opciones == "6":
        if empresa_activa:
            if not empresa_activa.bancos:
                print("FONDO INSUFICIENTE, DEBE REIGSTRAR EL BANCO EN LA OPCION 10")
            else:
                ejecutar_seguro(procesar_debito_banco, empresa_activa)
        else:
            print("Error:Seleccione una empresa primero")
    
    elif opciones == "7":
        def ejecutar_opcion_7():
            if empresa_activa:
                registrar_cotizacion(empresa_activa)
            else:   
                print("Error: Seleccione una empresa primero")
        
        ejecutar_seguro(ejecutar_opcion_7)
    
    elif opciones == "8":
        def ejecutar_opcion_8():
            if empresa_activa:
                registrar_proforma(empresa_activa)
            else:
                print("Error: Seleccione una empresa primero")
        
        ejecutar_seguro(ejecutar_opcion_8)
    elif opciones == "9":
        def ejecutar_opcion_9():
            if  not empresa_activa:
                print("Debe seleccionar una empresa primero")
                return 
            id_a_convertir = campo_texto("Introduce el ID del documento a convertir").strip().upper()
            print("\n¿Qué desea hacer con el documento?")
            print("1 - Registrar como GASTO (606)")
            print("2 - Registrar como VENTA (607)")
            tipo_conversion = campo_texto("Elija opción (1-2): ")
            
            if tipo_conversion =="1":
                convertir_proforma_cotizacion_606(empresa_activa,id_a_convertir)
               

            elif tipo_conversion == "2":
                convertir_proformar_a_factura_607(empresa_activa, id_a_convertir)
            else:
                print("Opciones invalida")
        ejecutar_seguro(ejecutar_opcion_9)
            

    elif opciones == "10":
        if empresa_activa:
            ejecutar_seguro(agregar_banco, empresa_activa)
        else:
            print("Seleccione una empresa primero")

    elif opciones == "11":
        print("Saliendo del programa")
        break
    
    elif opciones == "12":
        if empresa_activa:
            ejecutar_seguro(mostrar_historial, empresa_activa)
        else:
            print("Seleccione una empresa primero")

    elif opciones == "13":
        if empresa_activa:
            ejecutar_seguro(reporte_ajustero, empresa_activa)
        else:
            print("Seleccione una empresa primero")
    elif opciones == "14":
        def ejecutar_opcion_14():
            if empresa_activa:
                nuevo_colaborador = Empleado(empresa_activa)
                empresa_activa.nominas.append(nuevo_colaborador)
                print(f"\n✅ {nuevo_colaborador.nombre_empleado} ha sido registrado exitosamente.")
                print(f"Sueldo Neto: RD${nuevo_colaborador.sueldo_neto:,.2f}")
            else:
                print("Seleccione una empresa primero")
        
        ejecutar_seguro(ejecutar_opcion_14)
    elif opciones =="15":
        if empresa_activa:
            busqueda_factura = campo_texto("Introduce la ID PHX-XXXXX o el NCF a buscar").strip().upper()
            resultado = buscar_por_id(empresa_activa,busqueda_factura)
            if resultado is not None:
              
                print(f"\n✅ DOCUMENTO ENCONTRADO")
                print(f"------------------------------------------")
                print(f"ID PHX:    {resultado.id_transaccion}")
                print(f"NCF:       {resultado.ncf}")
                print(f"Tipo:      {resultado.tipo_documento.upper()}")
                print(f"Entidad:   {resultado.proveedor}")
                print(f"Monto:     RD${resultado.total:,.2f}")
                print(f"ESTADO:    {resultado.estado.upper()}") # <--- Aquí agregamos el Estado
                print(f"Pendiente: RD${resultado.saldo_pendiente:,.2f}")
                print(f"------------------------------------------")
            else:
                print(f"❌ No se encontró nada con el ID: {busqueda_factura}")
            
        else:
            print("Seleccione una empresa primero")
    elif opciones == "16":
        if empresa_activa:
            ejecutar_seguro(gestor_empresa)
        else:
            print("Seleccione una empresa primero")
    
    elif opciones == "17":
        if empresa_activa:
            ejecutar_seguro(eliminar_empresa)
        else:
            print("Seleccione una empresa primero")
    
    elif opciones == "18":
        def ejecutar_opcion_18():
            print("\n--- NUEVO REGISTRO DE TERCERO ---")
            nombre = input("Nombre o Razón Social: ")
            rnc = input("RNC o Cédula (solo números): ")
            while True:
                opc_tipo = input("Introduce 1-Cliente o 2-Suplidor: ").strip()
                if opc_tipo not in ("1","2"):
                    print("Invalido, Debe seleccionar 1 o 2")
                    continue
                tipo = "CLIENTE" if opc_tipo == "1" else "SUPLIDOR"
                print(tipo)
                break
            flujo_registro_tercero(nombre, rnc, tipo)
        
        ejecutar_seguro(ejecutar_opcion_18)

    elif opciones == "19":
        ejecutar_seguro(listar_terceros)

    elif opciones == "20":
        if empresa_activa:
            ejecutar_seguro(flujo_eliminar_tercero)
        else:
            print("No ha seleccionado la empresa")

    elif opciones == "21":
        if empresa_activa:
            ejecutar_seguro(reporte_facturas, empresa_activa)
        else:
            print("No ha seleccionado empresa")

    elif opciones == "22":
        def ejecutar_opcion_22():
            if not empresa_activa:
                print("❌ No ha sido seleccionada la empresa.")
            else:
                fecha_busqueda = input("Introduzca el período a buscar (ej. 05/2026): ").strip()
                if not fecha_busqueda:
                    print("❌ Error: Debe ingresar una fecha válida.")
                else:
                    generar_reporte_ajusteros(empresa_activa, fecha_busqueda)
        
        ejecutar_seguro(ejecutar_opcion_22)