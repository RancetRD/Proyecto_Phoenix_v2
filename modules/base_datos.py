import sqlite3




def cargar_empresas_guardadas():

    conexion = sqlite3.connect("phoenix.db")#AQUI ABRIMOS LA CONEXIN A LA BASE DE DATOS

    cursor = conexion.cursor()#ESTO SE UTILIZA PARA EJECUTAR LOS COMANDOS

    cursor.execute("""SELECT * FROM Empresa""")#AQUI ESTAMOS SELECCIONANDO EMPRESA PARA QUE ME BUSQUE TODAS LAS EMPRESAS , ES DECIR QUE SE ABRA UN CATALOGO DE TODAS LAS EMPRESAS POR ASI DECIRLO

    empresas_crudas = cursor.fetchall()# METODO PARA PODER GUARDAR TODO EN EMPRESA

    conexion.close()

    return empresas_crudas#AQUI DEVOLVEMOS EL VALOR , YA QUE UNA FUNCION , CUANDO SE UTILIZA DESAPARECEN LOS DATOS


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

    



def eliminar_empresa_db(id):
     #CONECTAR O CREAR BASE DE DATOS
    conexion = sqlite3.connect("phoenix.db")

     #CREAR UN CURSOR PARA EJECUTAR COMANDOS
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM Empresa WHERE id_empresa = ?", (id,)) 
    
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

def eliminar_tercero(id):
    conexion = sqlite3.connect("phoenix.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM Terceros WHERE id = ?", (id,))
    exito = cursor.rowcount > 0 
    conexion.commit()
    conexion.close()
    return exito # Retornamos el estado, NO imprimimos nada

def buscar_rnc_id(rnc):
    conexion = sqlite3.connect("phoenix.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM  terceros WHERE rnc=? ",(rnc,))

    lista_db_rnc_id = cursor.fetchone()

    return lista_db_rnc_id
