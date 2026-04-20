


#ESTO SERA UNA FUNCION , PARA BUSCAR EN TODAS LAS LISTAS , YA SEA PROFORMA , COTIZACION ,FACTURA
# 1. FUNCIÓN PARA BÚSQUEDA POR ID (La que usa el Débito/Pago)
def buscar_por_id(empresa, id_buscado):
    lista_universal = (
        empresa.compras + empresa.ventas + empresa.cotizaciones + 
        empresa.proformas + empresa.telecomunicaciones + 
        empresa.restaurantes + empresa.gastos_menores + 
        empresa.reporte_ajusteros
    )
    
    id_buscado = id_buscado.strip().upper()
    
    for factura in lista_universal:
        if factura.id_transaccion == id_buscado or factura.ncf == id_buscado:
            return factura
    return None

def buscar_facturas(empresa, ncf):
    # Aquí llamamos a la de arriba para no repetir código (DRY)
    return buscar_por_id(empresa, ncf)


############################################### BUSCAR FACTURAS #################################################################################
############################################### BUSCAR FACTURAS #################################################################################

