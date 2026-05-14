from modules.validaciones import campo_rnc, campo_texto,campo_float
from modules.db_empresa import registrar_tercero_db, obtener_terceros_db,eliminar_tercero

class Tercero():
    def __init__(self,id_tercero,nombre,rnc,tipo_negocio):
        self.id_tercero  = id_tercero
        self.nombre = nombre
        self.rnc = rnc
        self.tipo_negocio = tipo_negocio

    def obtener_tipo_fiscal(self):
        largo = len(self.rnc)

        if largo == 9:
            return "Persona Juridica(RNC)"
        
        elif largo ==11:
            return "Persona Fisica(CEDULA)"
        return "Invalido"
    
    def es_valido(self):
        return len(self.rnc) in [9,11] and self.rnc.isdigit()


def flujo_registro_tercero(nombre,rnc,tipo_negocio):
    nuevo = Tercero(None,nombre.upper(),rnc.strip(),tipo_negocio.upper())

    if not nuevo.es_valido():
        print(f"❌ Error: El RNC '{rnc}' no tiene 9 o 11 dígitos.")
        return False
    print(f"🔎 Detectado como: {nuevo.obtener_tipo_fiscal()}")

    return registrar_tercero_db(nuevo.nombre,nuevo.rnc,nuevo.tipo_negocio)


def listar_terceros():

   
    terceros = obtener_terceros_db()

    if not terceros:
        print("No hay proveedores registrados")
    else:
        print(f"\n{'ID':<5} | {'NOMBRE':<30} | {'RNC/CÉDULA':<15} | {'TIPO':<12}")
        print("-" * 70)
    
        for t in terceros:
            # Usamos tus variables para desempaquetar la tupla
            id_t, nombre, rnc, tipo = t
            
            # Limpiamos la lógica del tipo (S = Suplidor, lo demás Cliente)
            tipo_txt = "SUPLIDOR" if tipo == "S" else "CLIENTE"
            

            print(f"{id_t:<5} | {nombre[:30]:<30} | {rnc:<15} | {tipo_txt:<12}")
    return terceros


def flujo_eliminar_tercero():
    terceros = listar_terceros()
    
    if not terceros:
        return


    id_input = campo_texto("Introduce el ID a eliminar").strip().lower()
    if not id_input.isdigit():
        print("ERROR: Debe ser un numero")
        return
    id_eliminar = int(id_input)

    while True:

        
        opciones = campo_texto("Introduce si o no").lower().strip()
        if opciones not in ("si","no"):
           print("Debe seleccionar si o no")
           continue


        if opciones == "si":
            # Llamada única
            exito = eliminar_tercero(id_eliminar)
            
            # Bloque de decisión (La única forma de imprimir es entrando aquí)
            if exito:
                print(f"✅ El proveedor {id_eliminar} ha sido eliminado con éxito.")
            else:
                print(f"❌ Error: El ID {id_eliminar} no existe o no pudo ser eliminado.")
            break
        elif opciones == "no":
            print(f"⚠️ Operación cancelada. El proveedor {id_eliminar} permanece en el sistema.")
            break
        
        
    
    
