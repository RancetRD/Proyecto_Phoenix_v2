from modules.validaciones import *
from modules.consultas import buscar_por_id
from modules.factura import factura
#---------------FUNCION BASE DE REGISTRO DE FACTURAS-------------------
def registrar_gasto(empresa):# ESTA SER LA FUNCION BASE DE LAS FACTURAS
   print("REGISTROS GASTOS 606")
   while True:
        ncf = campo_ncf("NCF-->").upper()
        if any (f.ncf== ncf for f in empresa.compras):
         print("NCF duplicado, vuelva introcuir el ncf",ncf)
         continue
        break
   proveedor = campo_texto("PROVEEDOR-->").strip()
   rnc = campo_rnc("RNC/CEDULA-->")
   fecha = campo_fecha("FECHA-->")
   monto_neto = campo_float("MONTO NETO-->")
   while True:
            
        itbis = campo_float("ITBS-->")    
        if itbis > monto_neto:
            print("EL itbs no puede ser mayor al monto neto")
            continue
        break
   isc = 0
   cdt = 0
   ley_10 = 0

   

   nueva_factura = factura(empresa,"compras")
   nueva_factura.tipo_documento = "compras"
   nueva_factura.ncf = ncf
   nueva_factura.proveedor = proveedor
   nueva_factura.rnc = rnc
   nueva_factura.fecha = fecha
   nueva_factura.monto_neto = monto_neto
   nueva_factura.itbs = itbis
   nueva_factura.total = monto_neto + itbis
   nueva_factura.concepto = campo_texto("Digite el concepto del gasto de su factura").strip()
   nueva_factura.comentario = campo_texto("Digite un comentario si gusta").strip().upper()
   nueva_factura.saldo_pendiente = nueva_factura.total



   
   
   ultima_factura = empresa.compras[-1]
   print(f"\n Registro exitoso.")
   print(f"Su numero de facturo registrado es el #{len(empresa.compras)}" )
   print(f"Resumen: {nueva_factura.proveedor} | NCF: {nueva_factura.ncf} | Total: {nueva_factura.total}")
   return empresa
  
  ############################################### REGISTRAR PROFORMA  #################################################################################
   ############################################### REGISTRAR PROFORMA  #################################################################################

def registrar_proforma(empresa):
   print("REGISTRO DE PROFORMA")
   
   documento_proformas = factura(empresa,"proformas")
   empresa.proformas.append(documento_proformas)
   print(f"✅ Proforma registrada con éxito. ID: {documento_proformas.id_transaccion}")
   
   
 ############################################### REGISTRAR COTIZACION #################################################################################
 ############################################### REGISTRAR COTIZACION  #################################################################################
#FUNCION REUTILIZABLE DE COTIZACION
def registrar_cotizacion(empresa):
   print("REGISTRO DE COTIZACIONES")
   
   documento_cotizaciones = factura (empresa,"cotizaciones")
   empresa.cotizaciones.append(documento_cotizaciones)
   print(f"✅ Cotización registrada con éxito. ID: {documento_cotizaciones.id_transaccion}")



############################################### REGISTRAR TELECOM #################################################################################
############################################### REGISTRAR TELECOM  #################################################################################


def registrar_telecom(empresa):
   print("Registros de telecomunicaciones")

   ncf = campo_ncf("NCF-->").upper()
   proveedor = campo_texto("Proveedor-->").strip()
   rnc = campo_rnc("RNC-->")
   fecha = campo_fecha("Introduzca su fecha, ejm 11/04/2026-->")
   monto_neto = campo_float("Monto neto-->")
   itbis = campo_float("ITBS")
   isc = campo_isc("ISC-->",monto_neto)
   cdt = campo_cdt("CDT-->",monto_neto)
   ley_10 = 0
   
   print(f"Tu ISC es: {isc} | Tu CDT es: {cdt} ")

   nueva_telecom = factura(empresa,"telecomunicaciones")
   nueva_telecom.ncf = ncf
   nueva_telecom.proveedor = proveedor
   nueva_telecom.rnc = rnc
   nueva_telecom.fecha = fecha
   nueva_telecom.monto_neto = monto_neto
   nueva_telecom.itbis = itbis
   nueva_telecom.isc = isc
   nueva_telecom.cdt = cdt
   nueva_telecom.ley_10 = ley_10
   nueva_telecom.total = monto_neto + itbis + isc + cdt
   nueva_telecom.saldo_pendiente = nueva_telecom.total
   nueva_telecom.concepto = campo_texto("Introduzca el concepto de la factura").strip()
   nueva_telecom.comentario = campo_texto("Introduce un comentario si gusta")
   

   return empresa

############################################### REGISTRAR RESTAURANTE #################################################################################
############################################### REGISTRAR RESTAURANTE  #################################################################################

#FUNCION ESPECIALMENTE PARA LOS GASTOS DE RESTAURANTE
#FUNCION PARA TIPO GASTO FACTURA RESTAURANTE
def registrar_restaurante(empresa):

   ncf = campo_ncf("NCF-->").upper()
   proveedor = campo_texto("Proveedor").strip()
   rnc = campo_rnc("RNC-->")
   fecha = campo_fecha("Introduzca su fecha, ejm 11/04/2026-->")
   monto_neto = campo_float("Monto neto-->")
   itbis = monto_neto * 0.18
   ley_10 = monto_neto * 0.10
   print("Su itbs es: ",itbis,"La propina legal es : ",ley_10)

   nueva_restaurantes = factura(empresa,"restaurantes")
   nueva_restaurantes.ncf = ncf
   nueva_restaurantes.proveedor = proveedor
   nueva_restaurantes.rnc = rnc
   nueva_restaurantes.fecha = fecha
   nueva_restaurantes.monto_neto = monto_neto
   nueva_restaurantes.itbis = itbis
   nueva_restaurantes.ley_10 = ley_10
   nueva_restaurantes.total = monto_neto + itbis + ley_10
   nueva_restaurantes.saldo_pendiente = nueva_restaurantes.total
   nueva_restaurantes.concepto = campo_texto("Introduce el concepto de la factura").strip()
   nueva_restaurantes.comentario = campo_texto("Introduce un comentario si gusta").strip().upper()


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
    
    monto_pagado = campo_float("Monto a pagar --->")
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

def convertir_proformar_a_factura(empresa, id_buscado):
   factura_encontrada = buscar_por_id(empresa, id_buscado)
   
   if factura_encontrada == None:
      print("No se encontro el documento")
      return empresa

   if factura_encontrada.tipo_documento == "proformas":
      print(f"Proforma encontrada: {factura_encontrada.proveedor}")
      
      # USANDO TU FORMA: Un bucle para capturar la opción del NCF
      while True:
         print("Seleccione el tipo de NCF para la factura final")
         print("1- B01 (Credito Fiscal)")
         print("2- B02 (Consumo)")
         print("3- E31 (Electronica)")
         
         opciones = campo_texto("Elija una opcion del 1 al 3: ") # Usando tu funcion campo_texto
         
         if opciones not in ("1", "2", "3"):
            print("Opcion invalida, debe seleccionar una opcion del 1 al 3")
            continue
         
         # Asignamos el tipo según tu elección
         if opciones == "1": tipo = "B01"
         elif opciones == "2": tipo = "B02"
         else: tipo = "E31"
         break # Salimos del bucle cuando la opción es válida

      # MOVIENDO LOS DATOS 
      factura_encontrada.tipo_documento = "ventas"
      empresa.ventas.append(factura_encontrada)
      empresa.proformas.remove(factura_encontrada)

      #  LÓGICA DE LONGITUD
      if tipo == "B01":
         longitud = 8    
      elif tipo == "E31":
         longitud = 13
      else:
         longitud = 10
      
      # GENERANDO EL NCF 
      secuencia_actual = empresa.ncf_secuencia[tipo]
      factura_encontrada.ncf = f"{tipo}{secuencia_actual:0{longitud}d}"
      empresa.ncf_secuencia[tipo] += 1
      
      print(f"Pago aplicado. Nuevo NCF: {factura_encontrada.ncf}")
       
   else:
      print("EL documento no es una proforma")
      
   return empresa