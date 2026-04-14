from modules.validaciones import *
from modules.bodega import guardar_factura_bodega
from modules.consultas import buscar_por_id, buscar_facturas
from modules.factura import factura
#---------------FUNCION BASE DE REGISTRO DE FACTURAS-------------------
def registrar_gasto(empresa):# ESTA SER LA FUNCION BASE DE LAS FACTURAS
   print("REGISTROS GASTOS 606")
   while True:
        ncf = campo_ncf("NCF-->").upper()
        if any (f["ncf"]== ncf for f in empresa.compras):
         print("NCF duplicado, vuelva introcuir el ncf",ncf)
         continue
        break
   proveedor = campo_texto("PROVEEDOR-->").strip()
   rnc = campo_rnc("RNC/CEDULA-->")
   fecha = campo_fecha("FECHA-->")
   monto_neto = campo_float("MONTO NETO-->")
   while True:
            
        itbs = campo_float("ITBS-->")    
        if itbs > monto_neto:
            print("EL itbs no puede ser mayor al monto neto")
            continue
        break
   isc = 0
   cdt = 0
   ley_10 = 0

   
   concepto = campo_texto("Concepto del gasto-->").strip()
   comentario = input("Comentario (Opcional)-->").strip().upper()

   empresa = guardar_factura_bodega(empresa, ncf, proveedor, rnc, fecha, monto_neto, itbs, isc, cdt, ley_10, concepto, comentario)
   
   ultima_factura = empresa.compras[-1]
   print(f"\n Registro exitoso.")
   print(f"Su numero de facturo registrado es el #{len(empresa.compras)}" )
   print(f"Resumen: {ultima_factura['proveedor']} | NCF: {ultima_factura['ncf']} | Total: {ultima_factura['total']}")
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
   itbs = campo_float("ITBS")
   isc = campo_isc("ISC-->",monto_neto)
   cdt = campo_cdt("CDT-->",monto_neto)
   ley_10 = 0
   concepto = campo_texto("Concepto del gasto-->").strip()
   comentario = input("Comentario (Opcional)-->").strip().upper()
   print(f"Tu ISC es: {isc} | Tu CDT es: {cdt} ")

   return guardar_factura_bodega(empresa,ncf,proveedor,rnc,fecha,monto_neto,itbs,isc,cdt,ley_10,concepto, comentario)


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
   itbs = monto_neto * 0.18
   ley_10 = monto_neto * 0.10
   concepto = campo_texto("Concepto del gasto-->").strip()
   comentario = input("Comentario (Opcional)-->").strip().upper()
   print("Su itbs es: ",itbs,"La propina legal es : ",ley_10)


   return guardar_factura_bodega(empresa, ncf, proveedor, rnc, fecha, monto_neto, itbs, 0, 0, ley_10, concepto, comentario)

############################################### REGISTRAR PAGO GLOBAL #################################################################################
############################################### REGISTRAR PAGO GLOBAL #################################################################################


#AQUI ES DONDE PROCEDEREMOS A REALIZAR LOS PAGOS , SEGUN EL TIPO DE PAGO QUE APLIQUE , O SI ES PARCIAL O COMPLETO
def registrar_pago_global(empresa):
   pago_id_ncf = campo_texto("Introduce el numero de ID PHX o el NCF de la factura").strip().upper()
   guardar_pago_id_ncf = None
   for f in empresa.compras:
      if f["id_transaccion"]==pago_id_ncf or f["ncf"]==pago_id_ncf:
         guardar_pago_id_ncf = f
         break
   if guardar_pago_id_ncf == None:
      print("No se encontro la factura")
      return
   factura = guardar_pago_id_ncf
   print("Factura encontrada")
   print(f"Factura encontrada: {factura['proveedor']} - Saldo: {factura['saldo_pendiente']}")
   monto_pagado = campo_float("Monto a pagar --->")
   if monto_pagado > factura["saldo_pendiente"]:
      print("Error el monto excede el saldo pendiente")
      return
   fecha_pagada = campo_fecha("Debe Introducir la fecha pagada, ejm 11/04/2026")
   print("Bancos disponible",list(empresa.bancos.keys()))
   metodo_de_pago = campo_texto("Indique su metodo de pago ").strip().upper()
   usuario = "Admin_Peter"
   nuevo_pago = {
      "monto":monto_pagado,
      "metodo":metodo_de_pago,
      "fecha":fecha_pagada,
      "usuario":usuario,
      "activo":True

   }
   factura["historial_pagos"].append(nuevo_pago)
   actualizar_estado_factura(factura)
   print(f"Pago de {monto_pagado} aplicado con exito")

   if metodo_de_pago in empresa.bancos:

      if empresa.bancos[metodo_de_pago]["balance"] >= monto_pagado:
       empresa.bancos[metodo_de_pago]["balance"] -= monto_pagado
       print(f" Pago aplicado. Nuevo balance en {metodo_de_pago}: RD${empresa.bancos[metodo_de_pago]["balance"]:,.2f}")
      else:
          print(f" Fondos insuficientes en {metodo_de_pago}. Saldo: RD${empresa.bancos[metodo_de_pago]["balance"]:,.2f}")
   else:
      print(f"El banco '{metodo_de_pago}' no existe en el sistema")
      

   

############################################### ACTUALIZAR ESTADO FACTURA #################################################################################
############################################### ACTUALIZAR ESTADO FACTURA #################################################################################

def actualizar_estado_factura(factura):
   total_acumulado = 0.0#EMPEZAMOS EL CONTADOR EN 0 , DIRECTAMENTE CON NUMERO FLOTANTE

   for pago in factura ["historial_pagos"]:# AQUI REALIZAMOS LA RECORRIDA DE LA LISTA FACTURA
       if pago ["activo"]== True:
         total_acumulado += pago["monto"]#GUARDAMOS Y ACUTLIZANOS EL MONTO INMEDIATAMENTE


   factura["monto_acumulado"]= total_acumulado
   factura["saldo_pendiente"] = factura["total"] - total_acumulado

   if factura["saldo_pendiente"] == 0:#AQUI PONEMOS LAS CONDICIONALES DEL ESTADO DE LA FACTURA
       print("PAGADO")
   elif factura["saldo_pendiente"] == factura["total"]:
       print("PENDIENTE")
   elif factura["saldo_pendiente"] > 0 and factura["saldo_pendiente"] < factura["total"]:
       print("ABONADO")

   return factura

############################################### CONVERTIR PROFORMA A FACTURA #################################################################################
############################################### CONVERTIR PROFORMA A FACTURA #################################################################################

def convertir_proformar_a_factura(empresa, id_buscado):
   factura_encontrada = buscar_por_id(empresa, id_buscado)
   
   if factura_encontrada == None:
      print("No se encontro el documento")
      return empresa

   if factura_encontrada["tipo_documento"] == "proformas":
      print(f"Proforma encontrada: {factura_encontrada['proveedor']}")
      
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
      factura_encontrada["tipo_documento"] = "ventas"
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
      factura_encontrada["ncf"] = f"{tipo}{secuencia_actual:0{longitud}d}"
      empresa.ncf_secuencia[tipo] += 1
      
      print(f"Pago aplicado. Nuevo NCF: {factura_encontrada['ncf']}")
       
   else:
      print("EL documento no es una proforma")
      
   return empresa