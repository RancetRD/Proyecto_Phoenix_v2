import datetime
from modules.validaciones import campo_texto, campo_float,campo_fecha

def registrar_transaccion(empresa, tipo, entidad, monto, moneda, banco, usuario,tasa,fecha,cuenta):

    
    
    monto_dop = monto * tasa if moneda =="USD" else monto
    
    if not "historial" in empresa:
     empresa["historial"] = []

    movimiento = {
        "fecha":fecha,
        "usuario":usuario,
        "tipo":tipo,
        "entidad":entidad,
        "monto_original":monto,
        "moneda":moneda,
        "monto_dop":monto_dop,
        "banco":banco,
        "cuenta_bancaria":cuenta
     }
    empresa["historial"].append(movimiento)
    print(f" ✅ Movimiento registrado en historial por: {usuario}")

def mostrar_historial(empresa):
   if "historial" not in empresa or len (empresa["historial"])==0:
      print("No hay movimientos registrados")
      return
   print("\n" + "="*90)
   print(f"{'FECHA':<20} | {'TIPO':<10} | {'ENTIDAD':<15} | {'MONTO':<18} | {'BANCO':<15} | {'CUENTA':<15}")
   print("-" * 115)

   for movimiento in empresa["historial"]:
      fecha = movimiento["fecha"]
      tipo = movimiento["tipo"]
      entidad = movimiento["entidad"]
      monto_formateado = f"{movimiento['moneda']} {movimiento['monto_original']:,.2f}"
      banco = movimiento["banco"] # Asegúrate de que sea 'banco' (singular)
      cuenta = movimiento.get("cuenta_bancaria", "N/A")
      print(f"{fecha:<20} | {tipo:<10} | {entidad:<15} | {monto_formateado:<18} | {banco:<15} | {cuenta:<15}")
   print("="*115 + "\n")
      
