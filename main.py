from modules.validaciones import *
from modules.bodega import registrar_nueva_empresa, agregar_banco
from modules.pagos import procesar_debito_banco
from modules.contabilidad import mostrar_historial
from modules.factura import Factura  
from modules.nominas import Empleado
from modules.consultas import buscar_facturas, buscar_por_id
from modules.operaciones import (
    registrar_gasto,
    registrar_telecom,
    registrar_restaurante,
    registrar_pago_global,
    registrar_cotizacion,
    registrar_proforma,
    convertir_proformar_a_factura,
    reporte_ajustero
    
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
    print("13-Reporte ajusteros")
    print("14-Nominas")
    print("15-Buscar por ID o NCF")
    

    opciones = input("Seleccione la opcion que mas desee--->").strip()
    if opciones not in [str(i) for i in range(1, 20)]:
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
            ingresar_id_convertir = campo_texto("Introduce el ID del documento a convertir").strip().upper() 
            
            # Unimos las listas solo para buscar
            lista_busqueda = empresa_activa.cotizaciones + empresa_activa.proformas
            documento_encontrado = None
            origen = ""

            # 1. BUSCAMOS EL DOCUMENTO
            for documento in lista_busqueda:
                if documento.id_transaccion == ingresar_id_convertir:
                    documento_encontrado = documento
                    # Identificamos de dónde viene para borrarlo luego
                    if documento in empresa_activa.cotizaciones:
                        origen = "cotizaciones"
                    else:
                        origen = "proformas"
                    break
            
            # 2. SI LO ENCONTRAMOS, PROCESAMOS (FUERA DEL FOR)
            if documento_encontrado:
                print(f"✅ Documento encontrado: {documento_encontrado.proveedor}")

                while True:
                    print("\n1-Compras(GASTOS 606)")
                    print("2-Ventas(INGRESOS 607)")
                    seleccionar = campo_texto("Elija la opción del destino final")
                    
                    if seleccionar not in ["1", "2"]:
                        print("⚠️ Opción inválida, intente de nuevo")
                        continue

                    nuevo_ncf = campo_texto("Introduzca su nuevo NCF").strip().upper()
                    documento_encontrado.ncf = nuevo_ncf

                    if seleccionar == "1":
                        documento_encontrado.destino = "606"
                        empresa_activa.compras.append(documento_encontrado)
                        print(f"🚀 {ingresar_id_convertir} convertido a Gasto 606 exitosamente.")
                    else:
                        documento_encontrado.destino = "607"
                        empresa_activa.ventas.append(documento_encontrado)
                        print(f"🚀 {ingresar_id_convertir} convertido a Venta 607 exitosamente.")

                    # BORRAR DEL ORIGEN PARA NO DUPLICAR
                    if origen == "cotizaciones":
                        empresa_activa.cotizaciones.remove(documento_encontrado)
                    else:
                        empresa_activa.proformas.remove(documento_encontrado)
                    break
            else:
                print("❌ Documento no encontrado en proformas ni cotizaciones.")
        
        else:
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
    elif opciones =="13":
        if empresa_activa:
            reporte_ajustero(empresa_activa)
        else:
            print("Seleccione una empresa primero")
    elif opciones =="14":
        if empresa_activa:
            nuevo_colaborador = Empleado(empresa_activa)
            empresa_activa.nominas.append(nuevo_colaborador)
            print(f"\n✅ {nuevo_colaborador.nombre_empleado} ha sido registrado exitosamente.")
            print(f"Sueldo Neto: RD${nuevo_colaborador.sueldo_neto:,.2f}")
        else:
            print("Seleccione una empresa primero")
    elif opciones =="15":
        if empresa_activa:
            busqueda_factura = campo_texto("Introduce la ID PHX-XXXXX o el NCF a buscar").strip().upper()
            resultado = buscar_por_id(empresa_activa,buscar_facturas)
            if busqueda_factura:
                print(f"\n✅ DOCUMENTO ENCONTRADO")
                print(f"------------------------------------------")
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
