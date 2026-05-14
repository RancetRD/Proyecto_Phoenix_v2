import sqlite3

def inicializar_base_datos():
    #CONECTAR O CREAR BASE DE DATOS
    conexion = sqlite3.connect("phoenix.db")

    #CREAR UN CURSOR PARA EJECUTAR COMANDOS
    cursor = conexion.cursor()

    #AQUI VAMOS A CREAR LA BASE DE DATOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Empresa(
    id_empresa INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    rnc TEXT,
    regimen TEXT
)
""")


    #GUARDAR CAMBIOS EN LA BASE DE DATOS
    conexion.commit()

    #CERRAR CONEXION EN LA BASE DE DATOS
    conexion.close()


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
                   rnc TEXT NOT NULL,
                   tipo TEXT NOT NULL)
                   """)
    
    conexion.commit()
    conexion.close()
    print("✅ Base de datos inicializada correctamente.")