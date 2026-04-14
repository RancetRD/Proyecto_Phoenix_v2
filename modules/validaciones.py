import datetime

def campo_texto(mensaje):#FUNCION REUTILIZABLE , PARA CUALQUIER VALOR EN TEXTO
    while True:
     valor_texto = input(mensaje).strip().upper()
     if not valor_texto:
        print("Campo vacio!, debe introducir un valor valido ")
        continue
     return valor_texto

def campo_float(mensaje):#FUNCION REUTILIZABLE, PARA CUALQUIER VALOR EN NUMEROS
   while True:
      try:
         valor_float = float(input(mensaje))
         if valor_float < 0:
            print("El valor no puede ser negativo")
            continue
         return valor_float
      except ValueError:
         print("Debe introducir un monto valido por ejm 150.75")



def campo_fecha(mensaje):#FUNCION REUTILIZABLE, PARA CUALQUIER FECHA 
    while True:
        campo_fecha = input(mensaje)
        try:
           datetime.datetime.strptime(campo_fecha,"%d/%m/%Y")
           return campo_fecha
        except ValueError:
           print("Formato invalido")

#ESTE CAMPO ES EXCLUSIVAMENTE PARA REGLAS DE NCF, QUE TENGA UN RANGO MINIMO DE CARACTERES A UN RANGO MAXIMO DE CARACTERES 
def campo_ncf(mensaje):
   while True:
      ncf = campo_texto(mensaje).strip().upper()
      largo = len(ncf)
      if largo == 11 or largo == 13:#VALIDAMOS QUE TENGA EXACTAMENTE 11 O 13 CARACTERES PARA EVITAR ERROR DE TYPING
        pass
      else:
         print("❌ Error: El NCF debe tener exactamente 11 (actual) o 13 (viejos) caracteres.")
         continue
      if  ncf.startswith("B") or  ncf.startswith("E3"):
         print(f"✅ NCF {ncf} aceptado.")
         return ncf
      else:
         print("Error!, El NCF debe empezar con B o E3")
         continue
      

#ESTE CAMPO ES EXCLUSIVO PARA ENCAPSULAR REGLAR CONTABLES DE ISC , SE LE DA UN MARGEN DE ERROR DE 3 PESOS , POR POSIBLES REDONDEOS 
def campo_isc(mensaje,monto_neto):
   while True:
     valor_isc = campo_float((mensaje))
     if valor_isc < 0:
        print("No se aceptan numeros negativos")
        continue
     if valor_isc > (monto_neto * 0.10) +3:
      print("El monto de ISC, no puede ser mayor al 10%,pero tiene un margen de error de 3 pesos")
      continue    
     return valor_isc

#ESTE CAMPO ES EXCLUSIVO PARA ENCAPSULAR REGLAR CONTABLES DE CDT , SE LE DA UN MARGEN DE ERROR DE 3 PESOS , POR POSIBLES REDONDEOS 
def campo_cdt(mensaje,monto_neto):
   while True:
      valor_cdt = campo_float((mensaje))
      if valor_cdt < 0:
         print("No se aceptan numeros negativos")
         continue
      if valor_cdt > (monto_neto *0.02)+3:
         print("El monto de CDT, no puede ser mayor al 2%,pero tiene un margen de error de 3 pesos")
         continue
      return valor_cdt

#ESTA FUNCION ES EXCLUSIVAMENTE PARA ENCAPSULAR REGLAS CONTABLES DEL 10% DE LEY
def campo_10_ley(mensaje,monto_neto):
   while True:
      propina_10_ley = campo_float(mensaje)
      if propina_10_ley < 0:
         print("Monto,invalido , no puede introducir numeros negativos")
         continue
      if propina_10_ley > (monto_neto * 0.10)+3:
         print("El monto de la propina legal no puede ser mayor al 10% , tiene un margen error de 3 pesos")
         continue
      return propina_10_ley


#ESTA FUNCION ES EXCLUSVIAMENTE PARA ENCAPUSLAR LOS ERRORES DE TIPEO Y COMO REGLA LONGITUD DE CARACTERES
def campo_rnc(mensaje):
   while True:
      valor_rnc = input(mensaje).strip().upper()
      largo = len(valor_rnc)
      if not valor_rnc:
         print("Campo vacio,debe introducir un valor")
         continue
      if not valor_rnc.isdigit():
         print("Error: El RNC o CEDULA, no deben contener letras ni piuntos decimales")
         continue
      if largo == 9 or largo == 11:
         return valor_rnc
      else:
         print("Debe tener exactamente 9 (RNC) o 11 (Cédula) dígitos")

def campo_fecha_hora(mensaje):#FUNCION REUTILIZABLE, PARA CUALQUIER FECHA 
    while True:
        campo_fecha_hora = input(mensaje)
        if not campo_fecha_hora:
           print("Campo vacio,debe introducir un formato valido ejm 15/6/2026 ")
           continue
        try:
           fecha_validada = datetime.datetime.strptime(campo_fecha_hora, "%d/%m/%Y")
           ahora = datetime.datetime.now()
           fecha_final = fecha_validada.replace(hour=ahora.hour, minute =ahora.minute)
           return fecha_final
        except ValueError:
         print("Formato invalido")

def funcion_soporte_hora(nombre_usuario):
   ahora = datetime.datetime.now()
   nombre_usuario = "ADMIN"
   fecha_texto = ahora.strftime("%d/%m/%Y %H:%M:%S")
   return f"Registro realizado por {nombre_usuario} el {fecha_texto}"

def id_phoenix(empresa):
  
   
   lista_universal = (
        empresa.compras + 
        empresa.ventas + 
        empresa.cotizaciones + 
        empresa.proformas + 
        empresa.telecomunicaciones + 
        empresa.restaurantes + 
        empresa.gastos_menores + 
        empresa.reporte_ajusteros
    )
   if len(lista_universal) == 0:
      return "PHX-000001"
   
   todos_los_numeros = []
   for factura in lista_universal:
      id_texto = factura["id_transaccion"]
      numero_final = int(id_texto[4:])
      todos_los_numeros.append(numero_final)
      
        
  
   
   id_maximo = max (todos_los_numeros) 
   nuevo_id_numerico = id_maximo +1 
   return f"PHX-{nuevo_id_numerico:06d}"
      
      



         