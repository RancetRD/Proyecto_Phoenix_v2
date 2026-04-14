from modules.validaciones import (
    campo_ncf, campo_rnc, campo_texto, 
    campo_float, campo_fecha, funcion_soporte_hora,id_phoenix
)
from modules.consultas import buscar_por_id

class factura():
    def __init__(self, empresa, destino):
        # 1. Identificación y Destino
        self.proveedor = empresa["nombre"]
        self.destino = destino.lower()
        self.id_transaccion = id_phoenix(empresa)
        self.validar = True
        
        # 2. Inicialización de Impuestos (Evita errores en el cálculo del total)
        self.isc = 0.0
        self.cdt = 0.0
        self.ley_10 = 0.0
        
        # 3. Lógica de NCF "Multitarea" (Internos vs Fiscales)
        # Agregamos 'reporte_ajustero' en singular para que coincida con el diccionario
        internos = ["gasto_menores", "reporte_ajustero", "cotizaciones", "proformas"]
        
        if self.destino in internos:
            prefijos = {
                "gasto_menores": "B13",
                "reporte_ajustero": "AJ",
                "cotizaciones": "COT",
                "proformas": "PROF"
            }
            # Buscamos el prefijo; si no existe, por defecto pone 'INT'
            prefijo_actual = prefijos.get(self.destino, "INT") 
            self.ncf = f"{prefijo_actual}-{self.id_transaccion}"
            print(f"--- GENERANDO DOCUMENTO INTERNO: {self.ncf} ---")
        else:
            # Si no es interno, es una factura real y pide NCF fiscal
            self.ncf = campo_ncf("Introduzca su NCF Fiscal (B o E) ---> ")

        # 4. Datos Generales (Se piden SIEMPRE, por eso van fuera del if/else)
        self.proveedor = campo_texto("Introduzca su proveedor ---> ").strip().upper()
        self.rnc = campo_rnc("Introduzca su RNC ---> ")
        self.fecha = campo_fecha("Introduzca su fecha (DD/MM/AAAA) ---> ")
        self.registro_sistema = funcion_soporte_hora("SISTEMA")
        self.monto_neto = campo_float("Introduce el monto neto ---> ")
        
        # 5. Validación de ITBIS
        while True:
            self.itbs = campo_float("Introduce su ITBIS ---> ")   
            if self.itbs <= self.monto_neto:
                break
            print("Error: El ITBIS no puede ser mayor al monto neto.")

        # 6. Cálculo de Impuestos Específicos según el destino
        if self.destino == "telecomunicaciones":
            self.isc = self.monto_neto * 0.10
            self.cdt = self.monto_neto * 0.02
        elif self.destino == "restaurantes":
            self.ley_10 = self.monto_neto * 0.10
        
        # 7. Totales y Estados Finales
        self.total = self.monto_neto + self.itbs + self.isc + self.cdt + self.ley_10
        self.saldo_pendiente = self.total
        self.estado_pago = "PENDIENTE"
        self.metodo_pago = "PENDIENTE"
        self.moneda = "DOP"
        self.comentario = input("COMENTARIO (Opcional) ---> ").strip().upper() or "SIN COMENTARIOS"
    
        self.historial = [f"EVENTO 1: DOCUMENTO CREADO COMO {self.destino.upper()} - FECHA: {self.registro_sistema}"]
        self.historial.append(f"Documento {self.ncf} registrado con éxito.")

    # Método para convertir la clase a diccionario (para guardar en JSON/Base de datos)
    def to_dict(self):
        return self.__dict__
    
    # ... (Tu __init__ está perfecto ahora)

    def conversion_fiscal(self, nuevo_destino):
        self.ncf = campo_ncf(f"Introduzca el NCF Fiscal para {nuevo_destino.upper()} ---> ")
        self.destino = nuevo_destino.lower()
        fecha_act = funcion_soporte_hora("SISTEMA")
        self.historial.append(f"CONVERSIÓN: Movido a {self.destino.upper()} con NCF {self.ncf} el {fecha_act}")
        
        print(f"✅ Documento convertido y listo para el reporte fiscal.")

    def to_dict(self):
        return self.__dict__
        
        

        
        