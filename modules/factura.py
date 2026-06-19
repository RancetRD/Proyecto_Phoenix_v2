from modules.validaciones import id_phoenix, funcion_soporte_hora
from decimal import Decimal, ROUND_HALF_UP

class Factura():
    # Definimos la constante de redondeo contable fuera del __init__
    REDONDEO = Decimal("0.01") 

    def __init__(self, empresa, destino):
        self.id_empresa = empresa.id_empresa
        self.nombre_empresa = empresa.nombre
        self.destino = destino.lower()
        self.id_transaccion = id_phoenix(empresa)
        self.registro_sistema = funcion_soporte_hora("SISTEMA")
        self.tipo_documento = destino.lower()
        
        self.ncf = ""
        self.proveedor = ""
        self.rnc = ""
        self.fecha = ""
        self.monto_neto = Decimal("0.00")
        self.itbis = Decimal("0.00")
        self.isc = Decimal("0.00")
        self.cdt = Decimal("0.00")
        self.ley_10 = Decimal("0.00")
        self.isr_2 = Decimal("0.00")
        self.isr_10 = Decimal("0.00")
        self.total = Decimal("0.00")
        self.saldo_pendiente = Decimal("0.00")
        self.monto_acumulado = Decimal("0.00")
        self.concepto = ""
        self.comentario = ""
        self.estado = "PENDIENTE"
        self.moneda = "DOP"
        self.tasa_cambio = Decimal("1.00") # Arreglado: era float 1.0
        
        self.historial_pagos = []
        self.historial_eventos = [f"Documento creado en {self.destino} el {self.registro_sistema}"]

    def _redondear(self, valor):
        """Método auxiliar interno para mantener la precisión contable."""
        return valor.quantize(self.REDONDEO, rounding=ROUND_HALF_UP)
        
    def calculos_automaticos_impuestos(self, itbis_manual=None, aplicar_itbis=False, aplicar_isc=False, aplicar_cdt=False, aplicar_ley10=False, aplicar_isr_2=False, aplicar_isr_10=False):
        tmp_itbis, tmp_isc, tmp_cdt = Decimal("0.00"), Decimal("0.00"), Decimal("0.00")
        tmp_ley_10, tmp_isr_2, tmp_isr_10 = Decimal("0.00"), Decimal("0.00"), Decimal("0.00")
        tmp_total = self.monto_neto
        
        if aplicar_itbis: 
            val = (itbis_manual if itbis_manual is not None else self.monto_neto * Decimal("0.18"))
            tmp_itbis = self._redondear(val)
            tmp_total += tmp_itbis
            
        if aplicar_isc: 
            tmp_isc = self._redondear(self.monto_neto * Decimal("0.10"))
            tmp_total += tmp_isc 
            
        if aplicar_cdt: 
            tmp_cdt = self._redondear(self.monto_neto * Decimal("0.02"))
            tmp_total += tmp_cdt 
            
        if aplicar_ley10: 
            tmp_ley_10 = self._redondear(self.monto_neto * Decimal("0.10"))
            tmp_total += tmp_ley_10
            
        if aplicar_isr_2: 
            tmp_isr_2  = self._redondear(self.monto_neto * Decimal("0.02"))
            tmp_total -= tmp_isr_2
            
        if aplicar_isr_10: 
            tmp_isr_10 = self._redondear(self.monto_neto * Decimal("0.10"))
            tmp_total -= tmp_isr_10
        
        self.itbis = tmp_itbis 
        self.isc = tmp_isc 
        self.cdt = tmp_cdt 
        self.ley_10 = tmp_ley_10 
        self.isr_2 = tmp_isr_2 
        self.isr_10 = tmp_isr_10 
        self.total = self._redondear(tmp_total)

    def llenar_datos(self, ncf, fecha, monto_neto):
        """Asigna datos básicos asegurando el tipo Decimal."""
        self.ncf = ncf
        self.fecha = fecha
        # Convertimos forzosamente a Decimal usando str() para evitar errores de punto flotante
        self.monto_neto = Decimal(str(monto_neto))