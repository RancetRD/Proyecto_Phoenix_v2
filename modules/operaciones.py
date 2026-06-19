from modules.validaciones import *
from modules.consultas import buscar_por_id
from modules.factura import Factura
from modules.base_datos import buscar_rnc_id,guardar_factura_db
from decimal import Decimal, InvalidOperation
#---------------FUNCION BASE DE REGISTRO DE FACTURAS-------------------
def registrar_gasto(empresa):# ESTA SER LA FUNCION BASE DE LAS FACTURAS
   print("REGISTROS GASTOS 606")
   while True:
        ncf = campo_ncf("NCF-->").upper()
        if any (f.ncf== ncf for f in empresa.compras):
         print("NCF duplicado, vuelva introcuir el ncf",ncf)
         continue
        break
   rnc = campo_rnc("RNC/CEDULA-->")
   tercero_encontrado = buscar_rnc_id(rnc)
   if tercero_encontrado:
       proveedor = tercero_encontrado[1]
       # En vez de imprimir la tupla cruda, imprimes líneas limpias y alineadas:
       print(f"🔍 Status: SUPLIDOR ENCONTRADO")
       print(f"🏢 Nombre: {proveedor}")
       print(f"🪪 Tipo: {tercero_encontrado[3]}")
   else:
      print("❌ Error: Este suplidor no está registrado en el sistema. Vaya al módulo de Terceros.")
      return
   fecha = campo_fecha("FECHA-->")
   monto_neto = campo_moneda("MONTO NETO-->")
   print("Ingrese 0 para calcular el 18% de itbis automatico , si no digite el itbis manualmente")
   itbis_ingresado = campo_moneda("Introduce su Itbis")
   if itbis_ingresado == Decimal("0.00"):
      itbis_final = monto_neto * Decimal ("0.18")
      print(f"✅ ITBIS calculado automáticamente: RD${itbis_final:,.2f}")
   else:
      itbis_final = itbis_ingresado
   
   

   nueva_factura = Factura(empresa,"compras")
   nueva_factura.proveedor = tercero_encontrado[1] 
   nueva_factura.rnc = tercero_encontrado[2]
   nueva_factura.llenar_datos(ncf,fecha,monto_neto)
   
   nueva_factura.calculos_automaticos_impuestos(itbis_manual=itbis_final, aplicar_itbis=True)

   nueva_factura.concepto = campo_texto("Digite el concepto del gasto de su factura: ").strip()
   nueva_factura.comentario = input("Digite un comentario si gusta: ").strip().upper()
   nueva_factura.saldo_pendiente = nueva_factura.total
   if guardar_factura_db(nueva_factura):
      empresa.compras.append(nueva_factura)
   

# --- Resumen Final de Registro 606 ---
      print(f"\n" + "—"*40)
      print(f"✅ GASTO 606 REGISTRADO CON ÉXITO")
      print(f"🆔 ID PHOENIX: {nueva_factura.id_transaccion}")
      print(f"📄 NCF:        {nueva_factura.ncf}")
      print(f"🏢 PROVEEDOR:  {nueva_factura.proveedor}")
      print(f"💰 TOTAL:      RD${nueva_factura.total:,.2f}") # Formato con comas y decimales
      print("—"*40)
      print(f"Detalle: Neto RD${nueva_factura.monto_neto:,.2f} | ITBIS RD${nueva_factura.itbis:,.2f}")
      print("—"*40 + "\n")
    
   else:
     print("❌ ERROR CRÍTICO: No se pudo guardar en la base de datos. Factura descartada para evitar corrupción.")
     return empresa
   
  
  ############################################### REGISTRAR PROFORMA  #################################################################################
   ############################################### REGISTRAR PROFORMA  #################################################################################

def registrar_proforma(empresa):
    print("REGISTRO DE PROFORMA")
    rnc = campo_rnc("RNC-->").strip()
    tercero_encontrado = buscar_rnc_id(rnc)
    
    if not tercero_encontrado:
        print("❌ Error: Este suplidor no está registrado en el sistema. Vaya al módulo de Terceros.")
        return empresa # Retornamos la empresa para mantener la consistencia

    proveedor = tercero_encontrado[1]
    print(f"🔍 Status: SUPLIDOR ENCONTRADO\n🏢 Nombre: {proveedor}\n🪪 Tipo: {tercero_encontrado[3]}")

    fecha = campo_fecha("Fecha-->")
    monto_neto = campo_moneda("Monto Neto-->")
    
    print("💡 Ingrese 0 para ITBIS automático (18%) o digite el valor exacto.")
    itbis_ingresado = campo_moneda("Introduzca el ITBIS -->")
    
    if itbis_ingresado == Decimal("0.00"):
        itbis_final = monto_neto * Decimal("0.18")
        print(f"✅ ITBIS automático aplicado: RD${itbis_final:,.2f}")
    else:
        itbis_final = itbis_ingresado

    documento_proformas = Factura(empresa, "proformas")
    documento_proformas.proveedor = tercero_encontrado[1]
    documento_proformas.rnc = tercero_encontrado[2]
    documento_proformas.llenar_datos("", fecha, monto_neto) 

    documento_proformas.calculos_automaticos_impuestos(
        itbis_manual=itbis_final, 
        aplicar_itbis=True
    ) 

    documento_proformas.comentario = input("Introduce un comentario si gusta: ").strip().upper()

    # Guardado Atómico (Misma lógica segura que en el 606)
    if guardar_factura_db(documento_proformas):
        empresa.proformas.append(documento_proformas)
        
        # 5. Print "Lindo"
        print(f"\n✅ PROFORMA REGISTRADA: {documento_proformas.id_transaccion}")
        print(f"   SUPLIDOR : {documento_proformas.proveedor}")
        print(f"   TOTAL    : RD${documento_proformas.total:,.2f}")
        if documento_proformas.comentario:
            print(f"   NOTA     : {documento_proformas.comentario}")
        print("═"*45 + "\n")
    else:
        print("❌ ERROR CRÍTICO: No se pudo guardar en la base de datos. Proforma descartada.")
    
    return empresa
   
   
 ############################################### REGISTRAR COTIZACION #################################################################################
 ############################################### REGISTRAR COTIZACION  #################################################################################
#FUNCION REUTILIZABLE DE COTIZACION
def registrar_cotizacion(empresa):
    print("REGISTRO DE COTIZACIONES")

    rnc = campo_rnc("RNC-->").strip()
    tercero_encontrado = buscar_rnc_id(rnc)
    
    if not tercero_encontrado:
        print("❌ Error: Este suplidor no está registrado en el sistema. Vaya al módulo de Terceros.")
        return empresa # Retorno de seguridad

    proveedor = tercero_encontrado[1]
    print(f"🔍 Status: SUPLIDOR ENCONTRADO\n🏢 Nombre: {proveedor}\n🪪 Tipo: {tercero_encontrado[3]}")
    
    fecha = campo_fecha("Fecha-->")
    monto_neto = campo_moneda("Monto Neto-->")
    
    print("💡 Ingrese 0 para ITBIS automático (18%) o digite el valor exacto.")
    itbis_ingresado = campo_moneda("Introduzca el ITBIS -->")

    if itbis_ingresado == Decimal("0.00"):
        itbis_final = monto_neto * Decimal("0.18")
        print(f"✅ ITBIS automático aplicado: RD${itbis_final:,.2f}")
    else:
        itbis_final = itbis_ingresado
    
    nueva_cotizacion = Factura(empresa, "cotizaciones")
    nueva_cotizacion.proveedor = tercero_encontrado[1]
    nueva_cotizacion.rnc = tercero_encontrado[2]
    nueva_cotizacion.llenar_datos("", fecha, monto_neto)
    
    nueva_cotizacion.calculos_automaticos_impuestos(
        itbis_manual=itbis_final, 
        aplicar_itbis=True
    )
    
    nueva_cotizacion.comentario = input("Introduce un comentario si gusta: ").strip().upper()
    
    if guardar_factura_db(nueva_cotizacion):
        empresa.cotizaciones.append(nueva_cotizacion)
        print("\n" + "─" * 45)
        print(f"✅ COTIZACIÓN REGISTRADA: {nueva_cotizacion.id_transaccion}")
        print(f"   PROVEEDOR: {nueva_cotizacion.proveedor}")
        print(f"   RNC      : {nueva_cotizacion.rnc}")
        print(f"   TOTAL    : RD${nueva_cotizacion.total:,.2f}")
        if nueva_cotizacion.comentario:
            print(f"   NOTA     : {nueva_cotizacion.comentario}")
        print("─" * 45 + "\n")
    else:
        print("❌ ERROR CRÍTICO: No se pudo guardar en la base de datos. Cotización descartada.")
    
    return empresa
       
  



############################################### REGISTRAR TELECOM #################################################################################
############################################### REGISTRAR TELECOM  #################################################################################


def registrar_telecom(empresa):
    print("Registros de telecomunicaciones")
    while True:
        ncf = campo_ncf("NCF-->").upper()
        if any(f.ncf == ncf for f in empresa.telecomunicaciones):
            print("❌ Error: NCF duplicado en Telecomunicaciones. NCF:", ncf)
            continue
        break
    
    rnc = campo_rnc("RNC-->")
    tercero_encontrado = buscar_rnc_id(rnc)
    
    if not tercero_encontrado:
        print("❌ Error: Este suplidor no está registrado. Vaya al módulo de Terceros.")
        return empresa

    print(f"🔍 Status: SUPLIDOR ENCONTRADO\n🏢 Nombre: {tercero_encontrado[1]}")
    
    fecha = campo_fecha("Introduzca su fecha, ejm 11/04/2026-->")
    monto_neto = campo_moneda("Monto neto-->")
    
    # --- LÓGICA BLINDADA CON DECIMAL ---
    print("💡 Ingrese 0 para ITBIS automático (18%) o digite el valor exacto.")
    itbis_ingresado = campo_moneda("Introduzca el ITBIS -->")
    
    if itbis_ingresado == Decimal("0.00"):
        # CORRECCIÓN: Decimal("0.18") en lugar de ("0.18")
        itbis_final = monto_neto * Decimal("0.18")
        print(f"✅ ITBIS automático aplicado: RD${itbis_final:,.2f}")
    else:
        itbis_final = itbis_ingresado
    
    nueva_telecom = Factura(empresa, "telecomunicaciones")
    nueva_telecom.proveedor = tercero_encontrado[1]
    nueva_telecom.rnc = tercero_encontrado[2]
    nueva_telecom.llenar_datos(ncf, fecha, monto_neto)
    
    # Cálculo automático con los flags de Telecomunicaciones
    nueva_telecom.calculos_automaticos_impuestos(
        itbis_manual=itbis_final,
        aplicar_itbis=True,
        aplicar_isc=True, 
        aplicar_cdt=True
    )
    
    nueva_telecom.saldo_pendiente = nueva_telecom.total
    nueva_telecom.concepto = campo_texto("Introduzca el concepto de la factura").strip()
    nueva_telecom.comentario = input("Introduce un comentario si gusta: ").strip().upper()
    
    if guardar_factura_db(nueva_telecom):
        empresa.telecomunicaciones.append(nueva_telecom)
        
        print(f"\n✅ Registro de Telecomunicaciones exitoso.")
        print(f"🆔 ID Phoenix: {nueva_telecom.id_transaccion}")
        print(f"💰 TOTAL A PAGAR: RD${nueva_telecom.total:,.2f}")
        print(f"------------------------------------------")
        # Asegúrate de usar los campos calculados por el objeto Factura (ISC y CDT)
        print(f"Detalle: Neto: {nueva_telecom.monto_neto:,.2f} | ITBIS: {nueva_telecom.itbis:,.2f} | ISC: {nueva_telecom.isc:,.2f} | CDT: {nueva_telecom.cdt:,.2f}")
    else:
        print("❌ ERROR CRÍTICO: No se pudo guardar en la base de datos. Factura Telecom descartada.")
    
    return empresa

############################################### REGISTRAR RESTAURANTE #################################################################################
############################################### REGISTRAR RESTAURANTE  #################################################################################

#FUNCION ESPECIALMENTE PARA LOS GASTOS DE RESTAURANTE
#FUNCION PARA TIPO GASTO FACTURA RESTAURANTE
def registrar_restaurante(empresa):
    print("REGISTRO DE RESTAURANTES")
    while True:
        ncf = campo_ncf("NCF-->").upper()
        if any(f.ncf == ncf for f in empresa.restaurantes):
            print("❌ Error: NCF duplicado en Restaurantes. NCF:", ncf)
            continue
        break

    rnc = campo_rnc("RNC-->")
    tercero_encontrado = buscar_rnc_id(rnc)
    
    if not tercero_encontrado:
        print("❌ Error: Este suplidor no está registrado. Vaya al módulo de Terceros.")
        return

    print(f"🔍 Status: SUPLIDOR ENCONTRADO")
    print(f"🏢 Nombre: {tercero_encontrado[1]}")
    
    fecha = campo_fecha("Fecha-->")
    monto_neto = campo_moneda("Monto neto-->")
    
    # --- LÓGICA HÍBRIDA PARA ITBIS ---
    print("💡 Ingrese 0 para ITBIS automático (18%) o digite el valor exacto.")
    itbis_ingresado = campo_moneda("Introduzca el ITBIS -->")
    
    if itbis_ingresado == Decimal("0.00"):
        itbis_final = monto_neto * Decimal("0.18")
        print(f"✅ ITBIS automático aplicado: RD${itbis_final:,.2f}")
    else:
        itbis_final = itbis_ingresado
    

    nueva_restaurantes = Factura(empresa, "restaurantes")
    
    # Asignación directa de atributos
    nueva_restaurantes.proveedor = tercero_encontrado[1]
    nueva_restaurantes.rnc = tercero_encontrado[2]
    
    nueva_restaurantes.llenar_datos(ncf, fecha, monto_neto)
    
    # Cálculo automático aplicando ITBIS y la Ley 10 (Propina legal)
    nueva_restaurantes.calculos_automaticos_impuestos(
        itbis_manual=itbis_final, 
        aplicar_itbis=True, 
        aplicar_ley10=True
    )
    
    
    nueva_restaurantes.saldo_pendiente = nueva_restaurantes.total
    nueva_restaurantes.concepto = campo_texto("Introduce el concepto de la factura").strip()
    nueva_restaurantes.comentario = input("Introduce un comentario si gusta: ").strip().upper()
    
    if  guardar_factura_db(nueva_restaurantes):

        empresa.restaurantes.append(nueva_restaurantes)
    
        print(f"\n✅ RESTAURANTE REGISTRADO CON ÉXITO")
        print(f"🆔 ID PHOENIX: {nueva_restaurantes.id_transaccion}")
        print(f"📄 NCF:        {nueva_restaurantes.ncf}")
        print(f"💰 TOTAL:      RD${nueva_restaurantes.total:,.2f}")
        print("-" * 40)
        print(f"Detalle: Neto RD${nueva_restaurantes.monto_neto:,.2f} | ITBIS RD${nueva_restaurantes.itbis:,.2f} | Ley 10 RD${nueva_restaurantes.ley_10:,.2f}")
        print("=" * 40 + "\n")
        
    else:
        print("❌ ERROR CRÍTICO: No se pudo guardar en la base de datos. Factura Restaurante descartada.")
    
    return empresa
############################################### REGISTRAR PAGO GLOBAL #################################################################################
############################################### REGISTRAR PAGO GLOBAL #################################################################################


#AQUI ES DONDE PROCEDEREMOS A REALIZAR LOS PAGOS , SEGUN EL TIPO DE PAGO QUE APLIQUE , O SI ES PARCIAL O COMPLETO
def registrar_pago_global(empresa):
    pago_id_ncf = campo_texto("Introduce el ID PHX o NCF de la factura").strip().upper()
    
    # 1. Buscamos la factura usando tu buscador universal
    factura = buscar_por_id(empresa, pago_id_ncf)
    
    # 2. Validamos si realmente se encontró algo
    if factura is None:
        print("❌ No se encontró la factura en el sistema.")
        return
        
    print(f"✅ Factura encontrada: {factura.proveedor} - Saldo: RD${factura.saldo_pendiente:,.2f}")
    
    monto_pagado = campo_moneda("Monto a pagar --->")
    if monto_pagado > factura.saldo_pendiente:
        print("❌ Error: El monto excede el saldo pendiente.")
        return
        
    fecha_pagada = campo_fecha("Introduzca la fecha pagada, ejm 11/04/2026")
    print("Bancos disponibles:", list(empresa.bancos.keys()))
    metodo_de_pago = campo_texto("Indique su método de pago ").strip().upper()
    
    # 3. Creamos el registro del pago (Diccionario dentro del Objeto)
    nuevo_pago = {
        "monto": monto_pagado,
        "metodo": metodo_de_pago,
        "fecha": fecha_pagada,
        "usuario": "Admin_Peter",
        "activo": True
    }
    
    factura.historial_pagos.append(nuevo_pago)
    
    # 4. Actualizamos el estado usando la función híbrida
    actualizar_estado_factura(factura)
    
    print(f"✅ Pago de RD${monto_pagado:,.2f} aplicado con éxito.")

    # 5. Lógica bancaria (Tu lógica original con puntos)
    if metodo_de_pago in empresa.bancos:
        if empresa.bancos[metodo_de_pago]["balance"] >= monto_pagado:
            empresa.bancos[metodo_de_pago]["balance"] -= monto_pagado
            print(f"💰 Nuevo balance en {metodo_de_pago}: RD${empresa.bancos[metodo_de_pago]['balance']:,.2f}")
        else:
            print(f"⚠️ Fondos insuficientes en {metodo_de_pago}. Saldo: RD${empresa.bancos[metodo_de_pago]['balance']:,.2f}")
    else:
        print(f"❌ El banco '{metodo_de_pago}' no existe en el sistema.")
############################################### ACTUALIZAR ESTADO FACTURA #################################################################################
############################################### ACTUALIZAR ESTADO FACTURA #################################################################################

def actualizar_estado_factura(factura):
   total_acumulado = 0.0#EMPEZAMOS EL CONTADOR EN 0 , DIRECTAMENTE CON NUMERO FLOTANTE

   for pago in factura.historial_pagos :# AQUI REALIZAMOS LA RECORRIDA DE LA LISTA FACTURA
       if pago["activo"] == True:
         total_acumulado += pago["monto"]#GUARDAMOS Y ACUTLIZANOS EL MONTO INMEDIATAMENTE


   factura.monto_acumulado= total_acumulado
   factura.saldo_pendiente = factura.total - total_acumulado

   if factura.saldo_pendiente == 0:#AQUI PONEMOS LAS CONDICIONALES DEL ESTADO DE LA FACTURA
       print("PAGADO")
   elif factura.saldo_pendiente == factura.total:
       print("PENDIENTE")
   elif factura.saldo_pendiente > 0 and factura.saldo_pendiente < factura.total:
       print("ABONADO")

   return factura

############################################### CONVERTIR PROFORMA A FACTURA #################################################################################
############################################### CONVERTIR PROFORMA A FACTURA #################################################################################

def convertir_proformar_a_factura_607(empresa, id_buscado):
    factura_encontrada = buscar_por_id(empresa, id_buscado)
    
    if factura_encontrada is None:
        print("No se encontró el documento")
        return empresa

    if factura_encontrada.tipo_documento == "proformas":
        print(f"Proforma encontrada: {factura_encontrada.proveedor}")
        
        reglas_ncf = {
            "1": {"prefijo": "B01", "longitud": 8},
            "2": {"prefijo": "B02", "longitud": 10},
            "3": {"prefijo": "E31", "longitud": 13}
        }
        
        while True:
            print("\nSeleccione el tipo de NCF:")
            print("1- B01 (Crédito Fiscal) | 2- B02 (Consumo) | 3- E31 (Electrónica)")
            opciones = campo_texto("Elija una opción (1-3): ")
            
            if opciones in reglas_ncf:
                reglas = reglas_ncf[opciones]
                prefijo = reglas["prefijo"]
                longitud = reglas["longitud"]
                break
            print("⚠️ Opción inválida, intente de nuevo.")

        # 1. GENERANDO EL NCF (Una sola vez)
        secuencia_actual = empresa.ncf_secuencia.get(prefijo, 1)
        factura_encontrada.ncf = f"{prefijo}{secuencia_actual:0{longitud}d}"
        
        # 2. ACTUALIZANDO LA EMPRESA
        empresa.ncf_secuencia[prefijo] = secuencia_actual + 1
        
        # 3. MOVIENDO LOS DATOS (Solo al final, cuando ya tienes el NCF)
        factura_encontrada.tipo_documento = "ventas"
        empresa.ventas.append(factura_encontrada)
        empresa.proformas.remove(factura_encontrada)
        
        print(f"✅ Documento convertido. Nuevo NCF: {factura_encontrada.ncf}")
        
    else:
        print("EL documento no es una proforma")
        
    return empresa
      
      
def convertir_proforma_cotizacion_606(empresa, id_buscado):
    factura_encontrada = buscar_por_id(empresa, id_buscado)

    if not factura_encontrada:
        print("❌ No se encontró el documento")
        return empresa

    if factura_encontrada.tipo_documento not in ["proformas", "cotizaciones"]:
        print("❌ El documento no es una proforma ni cotización válida.")
        return empresa

    print(f"✅ Documento encontrado: {factura_encontrada.proveedor}")
    ncf = campo_ncf("NCF--->").upper()
    
    # Preparamos el cambio de estado
    factura_original_tipo = factura_encontrada.tipo_documento
    factura_encontrada.ncf = ncf
    factura_encontrada.tipo_documento = "compras"
    
    # Guardamos en DB ANTES de mover en memoria
    if guardar_factura_db(factura_encontrada):
        empresa.compras.append(factura_encontrada)
        
        # Eliminación segura
        if factura_encontrada in empresa.proformas:
            empresa.proformas.remove(factura_encontrada)
        elif factura_encontrada in empresa.cotizaciones:
            empresa.cotizaciones.remove(factura_encontrada)
            
        print(f"✅ Documento {id_buscado} registrado en 606 con éxito.")
    else:
        # Revertimos el cambio si falla la BD
        factura_encontrada.tipo_documento = factura_original_tipo
        print("❌ ERROR CRÍTICO: No se pudo actualizar el documento en la base de datos.")
        
    return empresa
   

def reporte_ajustero(empresa):
    print("Registro de Reporte ajustero")
    nombre_reporte_ajustero = campo_texto("Introduzca el nombre").strip().upper()
    
    # Validación robusta de ID
    while True:
        identificacion_ajustero = input("Introduzca el número de identificación (6-13 caracteres): ").strip()
        if 6 <= len(identificacion_ajustero) <= 13:
            break
        print("❌ Error: Debe introducir entre 6 y 13 caracteres.")
    
    monto_ajustero = campo_moneda("Introduzca el monto del reporte --->")
    fecha = campo_fecha("Introduzca la fecha (dd/mm/aaaa) -->")
    
    while True:
        opciones_valor_isr = campo_texto("Introduzca 1-para 2% ISR o 2-para 10% ISR--->").strip()
        if opciones_valor_isr in ("1", "2"):
            break
        print("❌ Error: Debe seleccionar 1 o 2.")

    nuevo_ajustero = Factura(empresa, "reporte_ajusteros")
    nuevo_ajustero.llenar_datos("N/A", fecha, monto_ajustero)
    nuevo_ajustero.proveedor = nombre_reporte_ajustero
    
    # Cálculo con Decimal
    nuevo_ajustero.calculos_automaticos_impuestos(
        aplicar_isr_2=(opciones_valor_isr == "1"), 
        aplicar_isr_10=(opciones_valor_isr == "2")
    )
    
    nuevo_ajustero.concepto = campo_texto("Introduzca el tipo de trabajo del ajustero")
    
    # Guardado atómico
    if guardar_factura_db(nuevo_ajustero):
        empresa.reporte_ajusteros.append(nuevo_ajustero)
        
        porcentaje = "2%" if opciones_valor_isr == "1" else "10%"
        valor_retenido = nuevo_ajustero.isr_2 if opciones_valor_isr == "1" else nuevo_ajustero.isr_10
        
        print("\n" + "═"*40)
        print(f"✅ REPORTE REGISTRADO: {nuevo_ajustero.id_transaccion}")
        print(f"   Ajustero: {nuevo_ajustero.proveedor}")
        print(f"   Retención ({porcentaje}): RD${valor_retenido:,.2f}")
        print(f"   Neto a Pagar: RD${nuevo_ajustero.total:,.2f}")
        print("═"*40 + "\n")
    else:
        print("❌ ERROR CRÍTICO: No se pudo guardar en la base de datos.")
    
    return empresa