import sqlite3
from modules.factura import Factura



def cargar_empresas_guardadas():

    conexion = sqlite3.connect("phoenix.db")#AQUI ABRIMOS LA CONEXIN A LA BASE DE DATOS

    cursor = conexion.cursor()#ESTO SE UTILIZA PARA EJECUTAR LOS COMANDOS

    cursor.execute("""SELECT * FROM Empresa""")#AQUI ESTAMOS SELECCIONANDO EMPRESA PARA QUE ME BUSQUE TODAS LAS EMPRESAS , ES DECIR QUE SE ABRA UN CATALOGO DE TODAS LAS EMPRESAS POR ASI DECIRLO

    empresas_crudas = cursor.fetchall()# METODO PARA PODER GUARDAR TODO EN EMPRESA

    conexion.close()

    return empresas_crudas#AQUI DEVOLVEMOS EL VALOR , YA QUE UNA FUNCION , CUANDO SE UTILIZA DESAPARECEN LOS DATOS

#AQUI CREAMOS NUESTRA TABLAS DE BASE DE DATOS
def inicializar_base_datos():
    conexion = sqlite3.connect("phoenix.db")
    cursor = conexion.cursor()

    cursor.execute(""" CREATE TABLE IF NOT EXISTS Empresa(
                   id_empresa INTEGER PRIMARY KEY AUTOINCREMENT,
                   nombre TEXT,
                   rnc TEXT,
                   regimen TEXT )
                   """)
    
    
    cursor.execute(""" CREATE TABLE IF NOT EXISTS Terceros(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nombre TEXT NOT NULL,
                   rnc TEXT NOT NULL UNIQUE,
                   tipo TEXT NOT NULL)
                   """)
    
    conexion.commit()
    conexion.close()
    print("✅ Base de datos inicializada correctamente.")


#AQUI SEPARAREMOS TODOS LOS DATOS , PARA QUE SE ESCALABLE
def obtener_empresas_db():
    conexion = sqlite3.connect("phoenix.db")

     #CREAR UN CURSOR PARA EJECUTAR COMANDOS
    cursor = conexion.cursor()

    cursor.execute("SELECT id_empresa, nombre, rnc, regimen FROM Empresa")   
    lista_db = cursor.fetchall()

    conexion.close()

    return lista_db

#ESTO ES PARA ACTUALIZAR LAS INFORMACIONES DE NUESTRA EMPRESA GUARDADA EN LA BASE DE DATOS
def actualizar_empresa_db(nuevo_nombre,nuevo_rnc,nuevo_regimen,id_empresa):
    
     #CONECTAR O CREAR BASE DE DATOS
    conexion = sqlite3.connect("phoenix.db")

     #CREAR UN CURSOR PARA EJECUTAR COMANDOS
    cursor = conexion.cursor()

    cursor.execute("""UPDATE Empresa 
        SET nombre=?, rnc=?, regimen=?
        WHERE id_empresa=?""", (nuevo_nombre, nuevo_rnc,nuevo_regimen, id_empresa))
    

    conexion.commit()
    conexion.close()

    

#ESTO ES PARA ELIMINAR LA EMPRESA QUE TENEMOS EN NUESTRA BASE DE DATOS

def eliminar_empresa_db(id):
     #CONECTAR O CREAR BASE DE DATOS
    conexion = sqlite3.connect("phoenix.db")

     #CREAR UN CURSOR PARA EJECUTAR COMANDOS
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM Empresa WHERE id_empresa = ?", (id,)) 
    
    conexion.commit()
    conexion.close()

   
#ESTO ES PARA MANTENER UN REGISTRO CONECTADO CON NUESTRA CREACION DE LOS PROVEEDORES(TERCEROS)

def registrar_tercero_db(nombre,rnc,tipo):
    try:
        conexion = sqlite3.connect("phoenix.db")

        cursor = conexion.cursor()

        sql = "INSERT INTO Terceros (nombre, rnc, tipo) VALUES (?, ?, ?)"

        cursor.execute(sql, (nombre, rnc, tipo))

        conexion.commit()
        print(f"✅ Tercero '{nombre}' registrado con éxito.")
        return True
    except sqlite3.IntegrityError:
        print("❌ Error: Este RNC ya está registrado en el sistema.")
        return False
    except sqlite3.Error as e:
        print(f"❌ Error de base de datos: {e}")
        return False
    finally:
        if conexion:
            conexion.close()

#ESTO ES PARA MANTENER  Y TRAER LAS INFORMACIONES DE BASES DE DATOS
def obtener_terceros_db():
    conexion = None
    terceros = []  # Nuestra red para atrapar los datos

    try: 
        conexion = sqlite3.connect("phoenix.db")
        cursor = conexion.cursor()

        
        cursor.execute("SELECT * FROM Terceros")
        
        
        terceros = cursor.fetchall()

    except sqlite3.Error as e:
        # La 'f' hace que {e} se convierta en el mensaje de error real
        print(f"❌ Error al consultar la bóveda: {e}")

    finally:
        if conexion:
            conexion.close()
            
    return terceros # Siempre devolvemos la variable en minúsculas

#ESTO ES PARA ELIMINAR CUALQUIER PROVEEDOR(TERCERO) EN LA BASE DE DATOS
def eliminar_tercero(id):
    conexion = sqlite3.connect("phoenix.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM Terceros WHERE id = ?", (id,))
    exito = cursor.rowcount > 0 
    conexion.commit()
    conexion.close()
    return exito # Retornamos el estado, NO imprimimos nada

#AQUI BUSCAMOS EL RNC O ID DE UNA FACTURA CONECTADO A LA BASES DE DATOS
def buscar_rnc_id(rnc):
    conexion = sqlite3.connect("phoenix.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM  terceros WHERE rnc=? ",(rnc,))

    lista_db_rnc_id = cursor.fetchone()

    return lista_db_rnc_id
#AQUI ES DONDE CREAREMOS TODAS LAS VARIABLES DE LA BASES DE DATOS , PARA MANTENER LA FACTURA
def facturas_db():
    conexion = sqlite3.connect("phoenix.db")
    cursor = conexion.cursor()

    cursor.execute("""  CREATE TABLE IF NOT EXISTS Factura(id_transaccion TEXT PRIMARY KEY ,
                   ncf TEXT NULL,
                   rnc TEXT,
                   proveedor TEXT,
                   fecha TEXT,
                   monto_neto REAL,
                   itbis REAL,
                   isc REAL DEFAULT 0,
                   cdt REAL DEFAULT 0,
                   ley_10 REAL DEFAULT 0,
                   total REAL,
                   saldo_pendiente REAL,
                   concepto TEXT,
                   comentario TEXT,
                   tipo_documento TEXT,
                   estado TEXT
                   )""")
    conexion.commit()
    conexion.close()
facturas_db()

def guardar_factura_db(documento):
    try:
        conexion = sqlite3.connect("phoenix.db")
        cursor = conexion.cursor()

        sql = """INSERT INTO Factura (
                    id_transaccion, ncf, rnc, proveedor, fecha, 
                    monto_neto, itbis, isc, cdt, ley_10, 
                    total, saldo_pendiente, concepto, comentario, 
                    tipo_documento, estado
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        valores = (
            documento.id_transaccion,
            documento.ncf,
            documento.rnc,
            documento.proveedor,
            documento.fecha,
            documento.monto_neto,
            documento.itbis,
            documento.isc,
            documento.cdt,
            documento.ley_10,
            documento.total,
            documento.saldo_pendiente,
            documento.concepto,
            documento.comentario,
            documento.tipo_documento,
            documento.estado
        )

        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()
        print(f"💾 Base de Datos: Documento {documento.id_transaccion} guardado exitosamente en disco.")
        return True
    except sqlite3.IntegrityError:
        print(f"❌ Error DB: El ID de transacción {documento.id_transaccion} ya existe en la base de datos.")
        return False
    except Exception  as e:
        print(f"❌ Error DB inesperado al guardar la factura: {e}")
        return False

def cargar_factura_db(empresa):

    conexion = sqlite3.connect("phoenix.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM Factura WHERE rnc_empresa = ?", (empresa.rnc,))

    filas = cursor.fetchall()
    empresa.compras = []
    for fila in filas:

        f = Factura(empresa, "compras") 
        f.id_transaccion = fila[0]
        f.ncf = fila[1]
        f.rnc = fila[2]
        f.proveedor = fila[3]
        f.fecha = fila[4]
        f.monto_neto = fila[5]
        f.itbis = fila[6]
        f.isc = fila[7]
        f.cdt = fila[8]
        f.ley_10 = fila[9]
        f.total = fila[10]
        f.saldo_pendiente = fila[11]
        f.concepto = fila[12]
        f.comentario = fila[13]
        f.tipo_documento = fila[14]
        f.estado = fila[15]

        empresa.compras.append(f)
    conexion.close()
    print(f"✅ Se cargaron {len(filas)} facturas desde la base de datos.")