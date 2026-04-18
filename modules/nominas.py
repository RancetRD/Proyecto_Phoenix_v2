from modules.validaciones import (campo_texto,campo_cedula,campo_float,campo_fecha)


class Empleado():

 def __init__(self):

        self.status_empleado = True
        self.fecha_salida = None
        self.historial_pagos_empleado = []
        self.regalia_acumulada = 0.0
        
        self.nombre_empleado = campo_texto("Introduce el nombre del empleado")
        self.cedula_empleado = campo_cedula("Introduce la cedula del empleado")
        self.cargo_empleado = campo_texto("Introduce el cargo del empleado dentro de la empresa")
        self.fecha_entrada = campo_fecha("Introduce ingreso del empleado dentro de la empresa")
        self.sueldo_bruto = campo_float("Introduce el sueldo bruto del empleado")
        self.sfs,self.afp = self.calcular_retenciones_ley(self.sueldo_bruto)
        sueldo_despues_sfs =  self.sueldo_bruto - self.sfs
        sueldo_limpio  = self.sueldo_bruto - self.sfs - self.afp
        self.isr = self.escala_isr_dgii(sueldo_limpio)
        self.sueldo_neto = self.sueldo_bruto - self.sfs - self.afp - self.isr
        ###########################CALCULAMOS AHORA LA PARTE DE LA EMPRESA###########################
        self.sfs_patronal,self.afp_patronal,self.srl_empresa,self.infotep = self.calcular_aportes_empresa(self.sueldo_bruto)
        self.costo_total_empleado =  self.sueldo_bruto + self.sfs_patronal + self.afp_patronal + self.srl_empresa + self.infotep



def calcular_retenciones_ley(self,sueldo_bruto):
    sfs = 0.0304 * sueldo_bruto  #SEGURO FAMILIAR DE SALUD
    afp = 0.0287 * sueldo_bruto # FONDO DE PENSIONES
   
    return sfs,afp

def calcular_aportes_empresa(self,sueldo_bruto):
    sfs_patronal = 0.0709 * sueldo_bruto #APORTE EMPRESA
    afp_patronal = 0.0710 * sueldo_bruto #APORTE EMPRESA
    srl_empresa = 0.0110 * sueldo_bruto #APORTE EMPRESA
    infotep = 0.01 * sueldo_bruto #APORTE EMPRESA
    return sfs_patronal,afp_patronal,srl_empresa,infotep
def escala_isr_dgii(self,sueldo_neto_tss):
    
      if sueldo_neto_tss <= 34684:
        isr = 0.0
      elif sueldo_neto_tss <= 52027 :
        excedente = sueldo_neto_tss -34685
        isr =   excedente * 0.15

      elif sueldo_neto_tss <= 72260:
        excedente = sueldo_neto_tss - 52027
        isr = (excedente * 0.20)+  2601.33
      else:
         excedente = sueldo_neto_tss -72260
         isr = (excedente * 0.25) + 6648
      return isr