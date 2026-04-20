import datetime
from modules.validaciones import campo_texto, campo_float,campo_fecha

def registrar_transaccion(empresa, id_phx, tipo, tipo_documento, entidad, monto, moneda, banco, usuario, tasa, fecha, cuenta, balance_momento, saldo_pendiente):
    monto_dop = monto * tasa if moneda =="USD" else monto
    
    if not hasattr (empresa,"historial"):
     empresa.historial = []

    movimiento = {
        "id_phx": id_phx,
        "fecha": fecha,
        "usuario": usuario,
        "tipo": tipo, 
        "tipo_documento": tipo_documento,
        "entidad": entidad,
        "monto_original": monto,
        "moneda": moneda,
        "tasa": tasa,
        "monto_dop": monto_dop,
        "banco": banco,
        "cuenta_bancaria": cuenta,
        "balance_banco": balance_momento,
        "saldo_factura_luego_pago": saldo_pendiente  # <--- ¡AGREGADO ESTO!
    }
    empresa.historial.append(movimiento)
    print(f" ✅ Movimiento {id_phx} [{tipo_documento}] registrado exitosamente.")
def mostrar_historial(empresa):
    if not hasattr(empresa, "historial") or len(empresa.historial) == 0:
        print("No hay movimientos registrados")
        return

   
    print("\n" + "═"*145)
    print(f"{'ID PHX':<12} | {'FECHA':<18} | {'ENTIDAD (SUPL)':<20} | {'TIPO DOC':<12} | {'PAGADO':<15} | {'PENDIENTE':<15} | {'USUARIO':<10}")
    print("─" * 145)

    for movimiento in empresa.historial:
        # --- PROCESAMIENTO ---
        fecha = movimiento["fecha"]
        fecha_str = fecha.strftime('%d/%m/%Y %H:%M') if hasattr(fecha, 'strftime') else str(fecha)
        
        # Extraemos con .get por si acaso hay registros viejos sin estas llaves
        id_phx = movimiento.get("id_phx", "N/A")
        entidad = movimiento.get("entidad", "N/A")
        tipo_doc = movimiento.get("tipo_documento", "N/A").upper()
        usuario = movimiento.get("usuario", "N/A")
        
        # Montos formateados
        moneda = movimiento.get("moneda", "DOP")
        monto_pagado = f"{moneda} {movimiento['monto_original']:,.2f}"
        
        pendiente_val = movimiento.get("saldo_factura_luego_pago", 0.0)
        pendiente_fmt = f"{moneda} {pendiente_val:,.2f}"

        
        print(f"{id_phx:<12} | {fecha_str:<18} | {entidad:<20} | {tipo_doc:<12} | {monto_pagado:<15} | {pendiente_fmt:<15} | {usuario:<10}")
    
    print("═"*145 + "\n")
