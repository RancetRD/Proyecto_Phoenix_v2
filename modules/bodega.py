from modules.validaciones import campo_texto, campo_rnc,campo_float

class Empresa():
        def __init__(self,id_empresa,nombre,rnc,regimen):
            print("Bienvenido al registro de Sistema Phoenix")
            self.id_empresa = id_empresa
            self.nombre = nombre     
            self.rnc = rnc
            self.regimen = regimen
            self.ncf_secuencia = inicializar_secuencia()
            self.compras = []#AQUI PARA EL 606
            self.ventas = []# AQUI PARA EL 607
            self.cotizaciones = []#AQUI SE GUARDARAN TODAS LAS COTIZACIONES
            self.proformas = []#AQUI SE GUARDARAN TODAS LAS PROFORMAS
            self.nominas = []
            self.contador_maestro = 0
            self.bancos = {}
            self.telecomunicaciones = []
            self.restaurantes = []
            self.gastos_menores = []
            self.reporte_ajusteros = []
#ESTA SERA UNA FUNCION PARA ASIGARLES COMPROBANTE FISCALES DE MANERA AUTOMATICA SEGUN SU TIPO
def inicializar_secuencia():
   ncf_secuencia = {
      "B01":1,
      "B02":1,
      "B04":1,
      "E31":1,
      "E32":1,
      "E34":1
   }
   return ncf_secuencia 


def registrar_nueva_empresa(listas_empresas):
    print("\n--- Registro de Nueva Empresa ---")
    nombre = campo_texto("Introduzca el nombre de la Empresa a crear-->").strip().upper()
    
    # 1. Bucle para asegurar un RNC con formato válido (9 o 11 dígitos)
    while True:
        rnc = campo_rnc("Introduce el RNC de la empresa (9 o 11 dígitos)-->").strip()
        
        if rnc.isdigit() and len(rnc) in [9, 11]:
            # 2. Verificar duplicados AHORA que el formato es correcto
            duplicado = False
            for emp in listas_empresas:
                if emp.rnc == rnc: 
                    print(f"[!] ERROR: El RNC {rnc} ya existe en '{emp.nombre}'.")
                    return None # Abortamos porque ya existe
            
            break # Si llegamos aquí, el RNC es válido y no es duplicado
        else:
            print("[!] ERROR: El RNC debe ser numérico y tener 9 o 11 dígitos.")

    # 3. Selección de Régimen
    print("\nSeleccione el Tipo de Régimen:")
    print("1- Persona Física")
    print("2- Persona Jurídica")
    
    while True:
        opcion = input("Seleccione (1-2)--> ").strip()
        if opcion == "1":
            regimen = "FISICA"
            break
        elif opcion == "2":
            regimen = "JURIDICA"
            break
        else:
            print("[!] Opción inválida.")

    id_empresa = len(listas_empresas) + 1
    
    # 4. EL MOMENTO DE LA VERDAD: Retornamos el objeto
    print(f"\n✅ Empresa '{nombre}' creada exitosamente.")
    return Empresa(id_empresa, nombre, rnc, regimen)
########################################################### GUARDAR FACTURA BODEGA#####################################################################
########################################################### GUARDAR FACTURA BODEGA#####################################################################

def guardar_factura_bodega(empresa, ncf, proveedor, rnc, fecha, monto_neto, itbs, isc=0, cdt=0, ley_10=0,concepto="",comentario="0",destino="compras",moneda="DOP",tasa_cambio=1.0):
    destinos_validos = ["compras", "ventas", "cotizaciones", "proformas", "telecomunicaciones", "restaurantes", "gastos_menores", "nominas"]
    
    if destino not in destinos_validos:
        print(f" ERROR: El destino '{destino}' no existe en la estructura.")
        return empresa
    from modules.validaciones import id_phoenix
    id_fijo = id_phoenix(empresa)
    
    total = monto_neto + itbs + isc + cdt + ley_10
   
    factura = {
       "id_transaccion":id_fijo,
        "ncf": ncf,           # Empezamos con el NCF como llave principal
        "proveedor": proveedor,
        "rnc": rnc,
        "fecha": fecha,
        "monto_neto": monto_neto,
        "itbs": itbs,
        "isc": isc,
        "cdt": cdt,
        "ley_10": ley_10,
        "total": total,
        "moneda":moneda,
        "tasa_cambio":tasa_cambio,
        "concepto":concepto,
        "comentario":comentario,  
        "historial_pagos":[],
        "monto_acumulado": 0.0,
        "estado_pago":"PENDIENTE",
        "tipo_documento":destino,
        "saldo_pendiente":total
        
        

    }
    
    lista_destino = getattr(empresa, destino)
    lista_destino.append(factura)
    print(f"\n Guardado en Bodega con ID: {id_fijo}")
    print(f"\n Registro exitoso. Total: {total}")
    return empresa


################################################## CONFIGURAR EMPRESA ################################################################
################################################## CONFIGURAR EMPRESA ################################################################

def configurar_empresa():#CON ESTA FUNCION VAMOS A DECIDIR SI EL CLIENTE NECESITA SU DECLARACION FISCA ORDINARIO O RST
   nombre = campo_texto("Introduca el nombre").strip()
   rnc = campo_rnc("Introduce el RNC")
   
   print("Selecciona el regimen fiscal")
   print("1-RST")
   print("2-Ordinaria")

   while True:
    opcion_configuracion = campo_texto("Eliga la opcion 1 o 2-->").strip()
    if opcion_configuracion not in("1","2"):# NOS ASEGURAMOS DE CUALQUIER ERROR CON ESTA LINEA DE ESPACIO U OPCION DIFERENTE
      print("Opcion invalida,debe introducir 1 o 2")
      continue
   
    if opcion_configuracion =="1":
      regimen = "RST"
    elif opcion_configuracion =="2":
       regimen = "ordinario"
    print(f">>Configuracion guardada: {regimen}")
    break
   #DEVOLVEMOS LOS DATOS CON RETURN
   return nombre, rnc, regimen

##################################################### AGREGAR BANCO ####################################################################
##################################################### AGREGAR BANCO ####################################################################
#FUNCION DONDE PERMITIRA REGISTRA EL BANCO
def agregar_banco(empresa):
   nombre_banco = campo_texto("introduce el Nombre del banco que desees registrar-->").strip().upper()
   numero_cuenta = campo_texto("Introduce el numero de cuenta bancaria, segun su banco")
   while True:
      moneda = campo_texto("Introduce la moneda con que deseas agregar el banco DOP$ o USD$")
      if moneda =="DOP":
         print("La cuenta bancaria se abrira en RD$ pesos")
         break
      elif moneda =="USD":
         print("La cuenta bancaria se abrira en USD$")
         break
      else:
         print("Error debe seleccionar RD$ o USD$")     
         continue
         
   
   if nombre_banco in empresa.bancos:
      print(f"El banco {nombre_banco} esta registrado")
      return
      
   rnc_banco = campo_rnc("introduce el RNC del banco").strip().upper()
   print(rnc_banco)
   monto_apertura = campo_float(f"¿Con cuánto dinero iniciaria su apertura bancaria? {nombre_banco}?-->")
   empresa.bancos[nombre_banco] = {
      "rnc":rnc_banco,
      "balance":monto_apertura,
      "moneda":moneda,
      "numero_cuenta":numero_cuenta

   }
   print(f"✅ Banco {nombre_banco} (Cuenta: {numero_cuenta}) registrado con {moneda}${monto_apertura:,.2f}")
   



########################################### CREAR CONTENEDOR VACIO #########################################################################
########################################### CREAR CONTENEDOR VACIO #########################################################################

# Esta función es el "molde" que le faltaba a tu código
def crear_contenedor_vacio():
    return {
        "informacion": {
            "proveedor": "",
            "fecha": "",
            "comentario": ""
        },
        "montos": {
            "total_moneda_original": 0.0,
            "moneda": "DOP",
            "saldo_pendiente": 0.0
        },
        "tipo_documento": ""
    }

########################################### INICIAR NUEVA OPERACION #########################################################################
########################################### INICIAR NUEVA OPERACION #########################################################################
def iniciar_nueva_operacion(proveedor,monto_total,moneda,tipo_documento):
  operacion = crear_contenedor_vacio()
  operacion["informacion"]["proveedor"] = proveedor
  operacion["informacion"]["fecha"] = "2026-04-11"
  operacion["informacion"]["comentario"]= "Registro inicial"

  operacion["montos"]["total_moneda_original"] = monto_total
  operacion ["montos"]["moneda"]= moneda
  operacion ["montos"]["saldo_pendiente"]= monto_total
  
  operacion ["tipo_documento"]= tipo_documento
  return operacion