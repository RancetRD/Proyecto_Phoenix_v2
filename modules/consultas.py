


#ESTO SERA UNA FUNCION , PARA BUSCAR EN TODAS LAS LISTAS , YA SEA PROFORMA , COTIZACION ,FACTURA
# 1. FUNCIÓN PARA BÚSQUEDA POR ID (La que usa el Débito/Pago)
def buscar_por_id(empresa, id_buscado):
    lista_universal = empresa.compras + empresa.ventas + empresa.cotizaciones + empresa.proformas + empresa.nominas  + empresa.telecomunicaciones + empresa.restaurantes + empresa.gastos_menores + empresa.reporte_ajusteros
    
    id_buscado = id_buscado.strip().upper()
    
    for factura in lista_universal:
       if isinstance (factura,dict):
        f_id = factura.get("id_transaccion")
        f_ncf = factura.get("ncf")
       else:
          f_ncf = None
          f_id = factura.cedula_empleado    
       if f_id == id_buscado or f_ncf == id_buscado:
           return factura
            
    print("❌ No se encontró nada")
    return None

# 2. FUNCIÓN PARA BÚSQUEDA POR NCF
def buscar_facturas(empresa, ncf):
    # Aquí llamamos a la de arriba para no repetir código (DRY)
    return buscar_por_id(empresa, ncf)


############################################### BUSCAR FACTURAS #################################################################################
############################################### BUSCAR FACTURAS #################################################################################

