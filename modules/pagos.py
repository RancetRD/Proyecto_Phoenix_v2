from modules.validaciones import campo_texto, campo_float
from modules.contabilidad import registrar_transaccion
from modules.consultas import buscar_por_id
from modules.validaciones import campo_fecha_hora
from modules.validaciones import funcion_soporte_hora

import datetime
def procesar_debito_banco(empresa): 
    pago_id_o_ncf = campo_texto("Introduce el ID PHX-XXX o el NCF de la factura si aplica-->").strip().upper()
    factura = None
   
    factura = buscar_por_id(empresa,pago_id_o_ncf)
    if factura == None:
       print("No se encontro la factura con ID PHX-XXX o NCF")
       return
    if factura.saldo_pendiente <= 0:
     print(f"¡Atención! La factura {pago_id_o_ncf} ya está saldada (Estado: {factura.estado}).")
     return
    print(f"\n--- Datos de la Factura ---")
    print(f"Factura de: {factura.proveedor} - Saldo: {factura.moneda}${factura.saldo_pendiente:,.2f}")
    if not  empresa.bancos:
       print("No hay bancos registrados")
       return
    print("Balance Actuales")

    for nombre in empresa.bancos:
        balance = empresa.bancos [nombre] ["balance"]
        moneda_banco = empresa.bancos[nombre]["moneda"]
        cuenta = empresa.bancos[nombre].get("numero_cuenta","n/a")
        print(f"- {nombre} (CTA: {cuenta}) | {moneda_banco} ${balance:,.2f}")
    seleccion = campo_texto("Indique el banco que desea realizar la transaccion").upper().strip()
    

    if seleccion not in empresa.bancos:
        print("Ese banco no se encuentra en la lista de bancos registrados")
        return
    if empresa.bancos[seleccion]["balance"] <= 0:#AQUI LE DECIMOS QUE SI EL BANCO NO TIENE SUFICIENTE , SALGA DEL FUNCION Y AGREGUE FONDOS , PARA TRABAJAR
       print("El banco no tiene fondos, agregue fondos para seguir trabajando")
       return
    moneda_factura = factura.moneda
    moneda_banco = empresa.bancos[seleccion]["moneda"]
    if moneda_banco != moneda_factura:
       print(f"¡Atención! La factura es {moneda_factura} y el banco es {moneda_banco}")

    monto_pago = campo_float("Introduce el monto a pagar")
    fecha_pago = campo_fecha_hora("Introduce la fecha del pago (DD/MM/YYYY): ")
    print(f"📅 Fecha procesada para el reporte: {fecha_pago.strftime('%d/%m/%Y')}")
    if monto_pago > factura.saldo_pendiente:
       print(f"Error: el monto excede el saldo de {factura.saldo_pendiente}")
       return
    tasa = 1
    if moneda_banco != moneda_factura:
       tasa = getattr(factura,"tasa_cambio",1)
       while True:
          opciones = campo_texto(f"Tasa actual: {tasa}. ¿Cambiar tasa? (S/N): ").strip().upper()
          if opciones not in ("S","N"):
             print("Invalido , debe introducir S o N")
          if opciones =="S":
             tasa = campo_float("Introduce la tasa del dia por ejm 59.65")
             break
          elif opciones =="N":
             print("Continua con la tasa registrada")
             break
       
    monto_a_descontar = monto_pago
    if moneda_factura =="USD" and moneda_banco =="DOP":
       monto_a_descontar = monto_pago * tasa
       print(f" Conversión: {monto_pago} USD x {tasa} = {monto_a_descontar:,.2f} DOP")
    elif moneda_factura =="DOP" and moneda_banco=="USD":
       if tasa > 0:
          monto_a_descontar = monto_pago/tasa
          print(f" 💱 Conversión: {monto_pago} DOP / {tasa} = {monto_a_descontar:,.2f} USD")
       else:
            print("Error: La tasa de cambio no puede ser 0.")
            return
    if monto_a_descontar > empresa.bancos[seleccion]["balance"]:
       print(f"❌ Error: No hay dinero suficiente en {seleccion}")
       return
    empresa.bancos[seleccion]["balance"]-= monto_a_descontar
    factura.saldo_pendiente -= monto_pago

    if moneda_banco != moneda_factura:
        factura.tasa_cambio = tasa
    cuenta_usada = empresa.bancos[seleccion].get("numero_cuenta", "N/A")

    sello_auditoria = funcion_soporte_hora("ADMIN")

    registrar_transaccion(
    empresa,                        # 1. Objeto empresa
        factura.id_transaccion,         # 2. ID PHX
        "SALIDA",                       # 3. Tipo (Fijo)
        factura.destino,                # 4. Tipo documento (606, restaurante, etc.)
        factura.proveedor,              # 5. Entidad (Suplidor)
        monto_pago,                     # 6. Monto que se pagó hoy
        factura.moneda,                 # 7. Moneda de la factura
        seleccion,                      # 8. Banco (Usamos tu variable 'seleccion')
        "ADMIN",                        # 9. Usuario (O sello_auditoria)
        tasa,                           # 10. Tasa (Tu variable calculada arriba)
        fecha_pago,                     # 11. Fecha (Tu variable campo_fecha_hora)
        cuenta_usada,                   # 12. Cuenta (Tu variable extraída del banco)
        empresa.bancos[seleccion]["balance"], # 13. Balance momento
        factura.saldo_pendiente
   )
    
    print(f" Pago exitoso.")
    print(f" Saldo restante en factura: {moneda_factura}${factura.saldo_pendiente:,.2f}")
    print(f" Nuevo balance en {seleccion}: {moneda_banco}${empresa.bancos[seleccion]['balance']:,.2f}")
    if factura.saldo_pendiente == 0:
       factura.estado= "Pagada"
       print("Factura completa al 100%")
    else:
       factura.estado ="Abonada"
       print(f" Factura abonada. Aún debe: {factura.saldo_pendiente}")
    




   