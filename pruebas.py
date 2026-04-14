from modules.validaciones import campo_texto, campo_rnc,campo_float

class Empresa():
        def __init__(self,id_empresa,nombre,rnc,regimen):
            print("Bienvenido al registro de Sistema Phoenix")
            self.id_empresa = id_empresa
            self.nombre = nombre     
            self.rnc = rnc
            self.regimen = regimen
            self.ncf_secuencia = incializar_secuencia()
            self.compras = []#AQUI PARA EL 606
            self.ventas = []# AQUI PARA EL 607
            self.cotizaciones = []#AQUI SE GUARDARAN TODAS LAS COTIZACIONES
            self.proformas = []#AQUI SE GUARDARAN TODAS LAS PROFORMAS
            self.contador_maestro = 0
            self.bancos = {}
            self.telecomunicaciones = []
            self.restaurantes = []
            self.gastos_menores = []
            self.reporte_ajusteros = []
#ESTA SERA UNA FUNCION PARA ASIGARLES COMPROBANTE FISCALES DE MANERA AUTOMATICA SEGUN SU TIPO
def incializar_secuencia():
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
                # OJO: Si ya tienes objetos en la lista, usa emp.rnc
                # Si todavía son diccionarios, usa emp["rnc"]
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