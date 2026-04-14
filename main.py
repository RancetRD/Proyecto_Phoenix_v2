from modules.validaciones import *
from modules.bodega import registrar_nueva_empresa, agregar_banco
from modules.pagos import procesar_debito_banco
from modules.contabilidad import mostrar_historial
from modules.factura import factura
from modules.operaciones import (
    registrar_gasto,
    registrar_telecom,
    registrar_restaurante,
    registrar_pago_global,
    registrar_cotizacion,
    registrar_proforma,
    convertir_proformar_a_factura,
    
)
mis_empresas = []
empresa_activa = None

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
    

    opciones = input("Seleccione la opcion que mas desee--->").strip()
    if opciones not in [str(i) for i in range(1, 15)]:
        print("ERROR: SELECCIONE UNA OPCIÓN VÁLIDA (1-15)")
        continue

    if opciones =="1":
        resultado = registrar_nueva_empresa(mis_empresas)

        if resultado is not None:
         mis_empresas.append(resultado)
         print("Empresa guardada con exito")
        else:
            print("Registro cancelado: El RNC ya existe")
    
    elif opciones =="2":
        if not mis_empresas:
            print("No hay registros todavia")
        else:
            print("Listas de empresas")
            for emp in mis_empresas:
                print(f"ID: {emp.id_empresa} - {emp.nombre}")
            try:
                id_buscar = int(input("Ingrese el ID para entrar: "))
                encontrada = False
                for emp in mis_empresas:
                    if emp.id_empresa== id_buscar:
                        empresa_activa = emp
                        encontrada = True
                        print(f"\n[OK] Bienvenido de nuevo a la empresa #{emp.id_empresa}--{emp.nombre}")
                        break
                if not encontrada:
                    print("ID no encontrado")
            except ValueError:
                print("Por favor, Ingrese un numero ID valido")
    
    elif opciones =="3":
        if empresa_activa:
            registrar_gasto(empresa_activa)
        else:
            print("Error: Debe crear o seleccionar una empresa primero")
    
    elif opciones == "4":
        if empresa_activa:
            registrar_telecom(empresa_activa) # Conectamos telecom
        else:
            print("Error: Seleccione una empresa primero")

    elif opciones =="5":
        if empresa_activa:
           registrar_restaurante(empresa_activa)
        else:
           print("Error:Seleccione una empresa primero")
    
    elif opciones =="6":
        if empresa_activa:
            if not empresa_activa.bancos:
                print("FONDO INSUFICIENTE, DEBE REIGSTRAR EL BANCO EN LA OPCION 10")
            else:
                procesar_debito_banco(empresa_activa)
        else:
           print("Error:Seleccione una empresa primero")
    
    elif opciones =="7":
        if empresa_activa:
            registrar_cotizacion(empresa_activa)
        else:   
            print("Error: Seleccione una empresa primero")
    
    elif opciones =="8":
        if empresa_activa:
            registrar_proforma(empresa_activa)
        else:
            print("Error: Seleccione una empresa primero")
    
    elif opciones == "9":
        if empresa_activa:
            ingresar_id_convertir = campo_texto("Introduce el ID del documento a convertir") 
            # Asegúrate que el nombre sea "proformas" en tu diccionario
            lista_busqueda = empresa_activa.cotizaciones + empresa_activa.proformas
            encontrado = False 
            
            for documento in lista_busqueda:
                if documento.id_transaccion == ingresar_id_convertir:
                    print(f"✅ Documento encontrado: {documento.proveedor}")

                    while True:
                        print("1-Compras(GASTOS 606)")
                        print("2-Ventas(INGRESOS 607)")
                        seleccionar = campo_texto("Elija la opción del destino final")
                        
                        if seleccionar not in ["1","2"]:
                            print("⚠️ Opción inválida, intente de nuevo")
                            continue
                        
                        destino_final = "compras" if seleccionar == "1" else "ventas"
                        documento.conversion_fiscal(destino_final)
                        encontrado = True
                        break 
                
                if encontrado:
                    break
            
            # CLAVE: Este IF debe estar alineado con el FOR (Dentro de empresa_activa)
            if not encontrado:
                print("❌ Error: Documento no encontrado en el sistema.")
        
        else:
            # Este es el else del 'if empresa_activa'
            print("⚠️ Error: No ha seleccionado una empresa todavía. Use la Opción 2.")
    elif opciones =="10":
         if empresa_activa:
            agregar_banco(empresa_activa) # Puerta abierta para crear dinero
         else:
            print("Seleccione una empresa primero")
    elif opciones =="11":
        print("Saliendo del programa")
        break
    
    elif opciones =="12":
        if empresa_activa:
            mostrar_historial(empresa_activa)
        else:
            print("Seleccione una empresa primero")