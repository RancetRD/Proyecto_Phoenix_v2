import datetime
from decimal import Decimal, InvalidOperation

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
           datetime.strptime(campo_fecha,"%d/%m/%Y")
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
      if  ncf.startswith("B0") or  ncf.startswith("E3"):
         print(f"✅ NCF {ncf} aceptado.")
         
      else:
         print("Error!, El NCF debe empezar con B0 o E3")
         continue
      return ncf  
      
      
      

#ESTE CAMPO ES EXCLUSIVO PARA ENCAPSULAR REGLAR CONTABLES DE ISC , SE LE DA UN MARGEN DE ERROR DE 3 PESOS , POR POSIBLES REDONDEOS 
def campo_isc(mensaje, monto_neto):
    while True:
        try:
            valor_isc = cast_decimal(input(mensaje))
            if valor_isc < Decimal("0.00"):
                print("❌ No se aceptan números negativos.")
                continue 
           
            if valor_isc > (monto_neto * Decimal("0.10")) + Decimal("3"):
                print("❌ El monto de ISC no puede ser mayor al 10%, pero tiene un margen de error de 3 pesos.")
                continue 
            return valor_isc   
        
        except ValueError:
            print("❌ Error: Formato numérico inválido.")
            continue

#ESTE CAMPO ES EXCLUSIVO PARA ENCAPSULAR REGLAR CONTABLES DE CDT , SE LE DA UN MARGEN DE ERROR DE 3 PESOS , POR POSIBLES REDONDEOS 
def campo_cdt(mensaje,monto_neto):
   while True:
      try:
          valor_cdt = cast_decimal(input(mensaje))
          if valor_cdt < Decimal("0.00"):
            print("No se aceptan numeros negativos")
            continue
          
          if valor_cdt > (monto_neto * Decimal ("0.02"))+ Decimal ("3"):
            print("El monto de CDT, no puede ser mayor al 2%,pero tiene un margen de error de 3 pesos")
            continue
          return valor_cdt
     
      except ValueError:
         print("❌ Error: Formato numérico inválido.")
         continue

#ESTA FUNCION ES EXCLUSIVAMENTE PARA ENCAPSULAR REGLAS CONTABLES DEL 10% DE LEY
def campo_10_ley(mensaje,monto_neto):
   while True:
      try:
          propina_10_ley = cast_decimal(input(mensaje))
          if propina_10_ley < Decimal("0.00"):
              print("Monto,invalido , no puede introducir numeros negativos")
              continue
          if propina_10_ley > (monto_neto * Decimal ("0.10"))+ Decimal ("3"):
              print("El monto de la propina legal no puede ser mayor al 10% , tiene un margen error de 3 pesos")
              continue
          return propina_10_ley
      except ValueError:
         print("❌ Error: Formato numérico inválido.")
         continue


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
      
from datetime import datetime, timedelta
def campo_fecha_hora(mensaje): 
    while True:
        campo_fecha_hora = input(mensaje)
        if not campo_fecha_hora:
            print("Campo vacio, debe introducir un formato valido ejm 15/06/2026")
            continue
        try:
           
            fecha_validada = datetime.strptime(campo_fecha_hora, "%d/%m/%Y")
            ahora = datetime.now()
            limite_inferior = ahora - timedelta(days=90)
            if fecha_validada > ahora:
                print("❌ Error: La fecha no puede ser futura.")
                continue
            
            elif fecha_validada < limite_inferior:
                print("❌ Error: La fecha tiene más de 3 meses de antigüedad.")
                continue
            fecha_final = fecha_validada.replace(hour=ahora.hour, minute=ahora.minute)
            return fecha_final
            
        except ValueError:
            print("❌ Formato inválido. Use DD/MM/YYYY")
def funcion_soporte_hora(nombre_usuario):
   ahora = datetime.now()
   fecha_texto = ahora.strftime("%d/%m/%Y %H:%M:%S")
   return f"Registro realizado por {nombre_usuario} el {fecha_texto}"

def id_phoenix(empresa):
  
   empresa.contador_maestro += 1
   return f"PHX-{empresa.contador_maestro:06d}"

def campo_cedula(mensaje):

   while True:
      cedula = input(mensaje).strip()
      if not cedula:
         print("Campo vacio debe introducir su cedula sin dejar campos vacios ")
         continue
      if not cedula.isdigit():
         print("La cedula solo debe contener numeros sin guiones")
         continue
      if len(cedula) != 11:
         print("Tu cedula debe tener 11 digitos sin guiones")
         continue
      return cedula
   
def campo_itbis(mensaje, monto_neto):
    while True:
        try:
            opciones = None
            campo_itbis = cast_decimal(input(mensaje))
            
            if campo_itbis < Decimal("0"):
                print("Lo sentimos el ITBIS no puede ser menor a 0")
                continue
            
            if campo_itbis > (monto_neto *  Decimal ("0.18")):
                print("Los sentimos el ITBIS, no puede ser mayor al 18%")     
                continue
            
            return campo_itbis
            
        except ValueError:
         print("❌ Error: Formato numérico inválido.")
         continue


def ejecutar_seguro(funcion, *args, **kwargs):
    try:
        funcion(*args, **kwargs)
    except Exception as e:
        # AQUÍ ESTÁ EL CAMBIO: Usamos datetime.datetime.now() para que coincida con el import
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nombre_modulo = funcion.__name__
        
        print(f"\n❌ Error detectado en el módulo: {nombre_modulo}")
        print(f"Detalle técnico: {e}")
        print("Disculpe los inconvenientes, el sistema se mantiene estable.")

        with open("log_errores.txt", "a") as archivo:
            archivo.write(f"[{ahora}] Módulo: {nombre_modulo} | Error: {e}\n")
      

def cast_decimal(valor_entrada):

   try:
      valor_limpio = str(valor_entrada).strip()
      return Decimal(valor_limpio)
   except (InvalidOperation,ValueError,TypeError):
      raise ValueError(f"El valor '{valor_entrada}' no es un formato numérico válido para contabilidad.")
   
      

def campo_moneda(mensaje):
    while True:
        entrada = input(mensaje).strip()
        if not entrada:
            print("Campo vacío, debe introducir un valor.")
            continue    
        try:
            valor_moneda = cast_decimal(entrada)
            if valor_moneda < Decimal("0.00"):
                print("El campo no admite valores negativos.")
                continue
                
            return valor_moneda  
            
        except (ValueError, InvalidOperation):
            print("❌ Error: Formato numérico inválido.")
            continue