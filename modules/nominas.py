from modules.validaciones import (campo_texto, campo_cedula, campo_float, campo_fecha)

class Empleado():

    def __init__(self,empresa):
        self.status_empleado = True
        self.fecha_salida = None
        self.historial_pagos_empleado = []
        self.regalia_acumulada = 0.0
        self.empresa_perteneciente = empresa.nombre
        
        # Captura de datos
        self.nombre_empleado = campo_texto("Introduce el nombre del empleado: ")
        self.cedula_empleado = campo_cedula("Introduce la cedula del empleado: ")
        self.cargo_empleado = campo_texto("Introduce el cargo del empleado: ")
        self.fecha_entrada = campo_fecha("Introduce ingreso del empleado (dd/mm/aaaa): ")
        self.sueldo_bruto = campo_float("Introduce el sueldo bruto del empleado: ")
        
        # --- CÁLCULOS AUTOMÁTICOS AL CREAR EL OBJETO ---
        
        # 1. Retenciones de Ley (TSS)
        self.sfs, self.afp = self.calcular_retenciones_ley(self.sueldo_bruto)
        
        # 2. Base Imponible para ISR (Sueldo Bruto menos TSS)
        sueldo_limpio = self.sueldo_bruto - self.sfs - self.afp
        
        # 3. Cálculo de ISR
        self.isr = self.escala_isr_dgii(sueldo_limpio)
        
        # 4. Sueldo Neto Final
        self.sueldo_neto = self.sueldo_bruto - self.sfs - self.afp - self.isr
        
        # 5. Aportes de la Empresa (Costo Patronal)
        self.sfs_patronal, self.afp_patronal, self.srl_empresa, self.infotep = self.calcular_aportes_empresa(self.sueldo_bruto)
        
        # 6. Costo Total para el empleador
        self.costo_total_empleado = self.sueldo_bruto + self.sfs_patronal + self.afp_patronal + self.srl_empresa + self.infotep

    # MÉTODOS DE CÁLCULO (Identados dentro de la clase)

    def calcular_retenciones_ley(self, sueldo_bruto):
        sfs = 0.0304 * sueldo_bruto  # 3.04% SFS
        afp = 0.0287 * sueldo_bruto  # 2.87% AFP
        return sfs, afp

    def calcular_aportes_empresa(self, sueldo_bruto):
        sfs_patronal = 0.0709 * sueldo_bruto # 7.09%
        afp_patronal = 0.0710 * sueldo_bruto # 7.10%
        srl_empresa = 0.0110 * sueldo_bruto  # 1.10% (Riesgos Laborales)
        infotep = 0.01 * sueldo_bruto       # 1%
        return sfs_patronal, afp_patronal, srl_empresa, infotep

    def escala_isr_dgii(self, sueldo_neto_tss):
        if sueldo_neto_tss <= 34685:
            isr = 0.0
        elif sueldo_neto_tss <= 52027:
            excedente = sueldo_neto_tss - 34685
            isr = excedente * 0.15
        elif sueldo_neto_tss <= 72260:
            excedente = sueldo_neto_tss - 52027
            isr = (excedente * 0.20) + 2601.33
        else:
            excedente = sueldo_neto_tss - 72260
            isr = (excedente * 0.25) + 6648
        return isr