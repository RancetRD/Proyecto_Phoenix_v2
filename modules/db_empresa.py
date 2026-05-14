import sqlite3
#AQUI SEPARAREMOS TODOS LOS DATOS , PARA QUE SE ESCALABLE
def obtener_empresas_db():
    conexion = sqlite3.connect("phoenix.db")

     #CREAR UN CURSOR PARA EJECUTAR COMANDOS
    cursor = conexion.cursor()

    cursor.execute("SELECT id_empresa, nombre, rnc, regimen FROM Empresa")   
    lista_db = cursor.fetchall()

    conexion.close()

    return lista_db

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

    



def eliminar_empresa_db(id_empresa):
     #CONECTAR O CREAR BASE DE DATOS
    conexion = sqlite3.connect("phoenix.db")

     #CREAR UN CURSOR PARA EJECUTAR COMANDOS
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM Empresa WHERE id_empresa = ?", (id_empresa,)) 
    
    conexion.commit()
    conexion.close()

   
def crear_tabla__tercero():

    #CONECTAR O CREAR BASE DE DATOS
    conexion = sqlite3.connect("phoenix.db")

    #CREAR EL CURSOR PARA CREAR LOS COMANDOS
    cursor = conexion.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Terceros(
     id_tercero INTEGER PRIMARY KEY AUTOINCREMENT,
     nombre TEXT,
     rnc TEXT UNIQUE,
     tipo TEXT                
    )
""")
    
    conexion.commit()

    conexion.close()

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

def eliminar_tercero(id_eliminar):
    conexion = sqlite3.connect("phoenix.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM Terceros WHERE id = ?", (id_eliminar,))
    exito = cursor.rowcount > 0 
    conexion.commit()
    conexion.close()
    return exito # Retornamos el estado, NO imprimimos nada

