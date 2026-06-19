

def reporte_facturas(empresa):
    lista_universal = (
        empresa.compras + empresa.ventas + empresa.cotizaciones + 
        empresa.proformas + empresa.telecomunicaciones + 
        empresa.restaurantes + empresa.gastos_menores + 
        empresa.reporte_ajusteros
    )

    facturas_totales  = 0
    acumulador_factura_total = 0
    factura_pendiente_total = 0
    if not lista_universal:
        print("No Hay facturas que mostrar")
        return
    for facturas in  lista_universal:
        facturas_totales  += 1
        acumulador_factura_total += facturas.total
        factura_pendiente_total +=  facturas.saldo_pendiente

    ancho_total = 85
    print(f"\n{'='*ancho_total}")
    print(f"{'RESUMEN DE FACTURAS':^{ancho_total}}")
    print(f"{'='*ancho_total}")
    print(f"{'ID':<5} | {'NCF':<15} | {'Proveedor':<20} | {'Total':>15} | {'Pendiente':>15}")
    print(f"{'-'*ancho_total}")
    #AQUI ES DONDE SE VE LA ACUMULACION DE LOS MONTOS DE LA FACTURAS
    for facturas in lista_universal:
        
       print(f"{facturas.id_transaccion:<5} | {facturas.ncf:<15} | {facturas.proveedor[:20]:<20} | {facturas.total:>15,.2f} | {facturas.saldo_pendiente:>15,.2f}")
    
    print(f"{'-'*ancho_total}")
    print(f"Total de facturas: {facturas_totales}")
    print(f"Monto Total Acumulado:  ${acumulador_factura_total:>18,.2f}")
    print(f"Saldo Total Pendiente:  ${factura_pendiente_total:>18,.2f}")
    print(f"{'='*ancho_total}\n")


def generar_reporte_ajusteros(empresa,fecha_busqueda):
    total_neto = 0
    total_isr_2 = 0
    total_isr_10 = 0
    facturas_encontradas = 0

    ancho_total = 85
    print(f"\n{'='*ancho_total}")
    print(f"REPORTE DE AJUSTEROS - PERÍODO: {fecha_busqueda}".center(ancho_total))
    print(f"{'='*ancho_total}")
    print(f"{'ID':<5} | {'NCF':<15} | {'Neto':>15} | {'ISR 2%':>15} | {'ISR 10%':>15}")
    print(f"{'-'*ancho_total}")

    for reporte in empresa.reporte_ajusteros:
        if fecha_busqueda in reporte.fecha:
           facturas_encontradas += 1
           total_neto += reporte.monto_neto
           total_isr_2 += reporte.isr_2
           total_isr_10 += reporte.isr_10            
    
           print(f"{reporte.id_transaccion:<5} | {reporte.ncf:<15} | {reporte.monto_neto:>15,.2f} | {reporte.isr_2:>15,.2f} | {reporte.isr_10:>15,.2f}")

    print(f"{'-'*ancho_total}")
    print(f"Total Facturas: {facturas_encontradas}")
    print(f"Total Neto:   ${total_neto:>18,.2f}")
    print(f"Total ISR 2%: ${total_isr_2:>18,.2f}")
    print(f"Total ISR 10%:${total_isr_10:>18,.2f}")
    print(f"{'='*ancho_total}")
    print("Peter Creador de Phoenix\n")