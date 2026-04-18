from modules.validaciones import id_phoenix, funcion_soporte_hora

class factura():
    def __init__(self, empresa, destino):
        # 1. Identificación básica (Conexión con la Empresa)
        self.nombre_empresa = empresa.nombre
        self.destino = destino.lower()
        self.id_transaccion = id_phoenix(empresa)
        self.registro_sistema = funcion_soporte_hora("SISTEMA")
        self.tipo_documento = destino.lower() # Para saber si es gasto, telecom, etc.
        
        # 2. Atributos base (Nacen vacíos para ser llenados en operaciones.py)
        self.ncf = ""
        self.proveedor = ""
        self.rnc = ""
        self.fecha = ""
        self.monto_neto = 0.0
        self.itbis = 0.0
        self.isc = 0.0
        self.cdt = 0.0
        self.ley_10 = 0.0
        self.total = 0.0
        self.saldo_pendiente = 0.0
        self.monto_acumulado = 0.0
        self.concepto = ""
        self.comentario = ""
        self.estado = "PENDIENTE"
        
        # 3. Listas de seguimiento
        self.historial_pagos = []
        self.historial_eventos = [f"Documento creado en {self.destino} el {self.registro_sistema}"]
        
        # 4. AUTO-REGISTRO: La factura se guarda sola en la lista correcta de la empresa
        if hasattr(empresa, self.destino):
            lista_destino = getattr(empresa, self.destino)
            lista_destino.append(self)
        else:
            print(f"⚠️ Alerta: La lista '{self.destino}' no existe en la empresa.")