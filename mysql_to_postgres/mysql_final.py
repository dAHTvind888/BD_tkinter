import mysql.connector
import sys

#FUNCION QUE DEVUELVE CONEXION MYSQL
def connection(anfitrion,usuario,contraseña,puerto):
    base_mysql = mysql.connector.connect(
        host = anfitrion,
        user = usuario,
        password = contraseña,
        port = puerto
    )
    print("Conexión Exitosa a MYSQL")
    print()
    return base_mysql

#FUNCION QUE DEVUELVE CURSOR MYSQL
def cursor(connection):
    return connection.cursor()

#FUNCION QUE CIERRA CONEXION MYSQL
def disconnection(connection, cursor) -> None:
    cursor.close()
    connection.close()
    print("Desconectado de MYSQL")

#MUESTRA TODAS LAS BASES DE DATOS DE MYSQL
def mostrar_base_de_datos(cursor) -> None:
    cursor.execute("SHOW DATABASES")
    bases = cursor.fetchall()
    print("Base de Datos en MYSQL: ")
    bases_cruciales_para_el_sistema = ["information_schema","mysql","performance_schema","sys"]
    for base in bases:
        if(base[0] not in bases_cruciales_para_el_sistema):
            print(base[0])

#FUNCION QUE RETORNA LA SELECCION DE LA BASE QUE SE MIGRARA
def elegir_base_origen(cursor) -> str:
    base_elección = input("Escriba que Base de Datos Migrara, en caso contrario escriba DETENER: ")
    cursor.execute("SHOW DATABASES") #SHOW DATABASES extrae las bases de datos existentes
    bases = cursor.fetchall()
    verificador = 0
    for base in bases:
        if(base_elección == base[0]):#SE COMPARAN LAS BASES CON LA ENTRADA DEL USUARIO
            verificador += 1
    if(base_elección == "DETENER"):
        print("Deteniendo Programa")
        print()
        sys.exit()
    elif(verificador == 0):
        return elegir_base_origen(cursor)
    else:
        print()
        return base_elección
    
    #DEVUELVE LAS TABLAS DE MYSQL
def tablas(cursor, base_elección) -> list[str]:
    cursor.execute("USE " + base_elección)
    cursor.execute("SHOW TABLES;") 
    nombre_de_tablas = cursor.fetchall()
    tablas : list[str] = []
    for nombres in nombre_de_tablas:
        tablas.append(nombres[0])
    return tablas

    #DEVUELVE LOS CODIGOS DE CREACION DE TABLAS DE MYSQL
def extraer_codigo_creacion(cursor,tabla) -> str:
    cursor.execute("show create table " + tabla) #Muestra su codigo base de la tabla
    codigo = cursor.fetchone()
    return codigo[1]

#Este codiga limpia el código y 
#almacena el nombre de las tablas que contienen auto_incremento en tablas_incrementos (lista)
def limpiar_codigo_creacion(codigo_creacion, tablas_incremento : list[str]) -> str:
    new_string = ""
    longitud = len(codigo_creacion)
    i = 0
    contador1 = 0
    contador2 = 0
    table_name : str = ""
    while i < longitud:
        if(codigo_creacion[i] == "T" and codigo_creacion[i+1] == "A" and codigo_creacion[i+2] == "B" and codigo_creacion[i+3] == "L" and codigo_creacion[i+4] == "E"):
            s = i+7 #s es un contador auxiliar y se suma 7 a i para que s se encuentre justo en la primera letra del nombre de la tabla
            while s < longitud: #Este while busca almacenar el nombre de la tabla en table_name
                if(codigo_creacion[s] != "`"):
                    table_name += codigo_creacion[s]
                    s = s +1
                else:
                    break
            new_string += codigo_creacion[i] #Esta i esta en la posición de T
            i = i + 1
            #ELIMINA AUTO_INCREMENT POR IDENTITY
        elif(codigo_creacion[i] == "A" and codigo_creacion[i+1] == "U" and codigo_creacion[i+2] == "T" and codigo_creacion[i+3] == "O" and codigo_creacion[i+4] == "_"):
            new_string += "IDENTITY(1,1)"
            tablas_incremento.append(table_name)
            i = i +13
            i = i + 1
            #ELIMINAS KEY HASTA " " ANTES DE FOREIGN KEY
        elif(codigo_creacion[i] == "K" and codigo_creacion[i+1] == "E" and codigo_creacion[i+2] == "Y" and codigo_creacion[i+3] == " " and codigo_creacion[i+4] != "("):
            e = i
            while e < longitud:
                if(codigo_creacion[e]=="F" and codigo_creacion[e+1]=="O" and codigo_creacion[e+2]=="R" and codigo_creacion[e+3]=="E" and codigo_creacion[e+4]=="I"):
                    i = e-1
                    break
                else:
                    e = e + 1
                #ELIMINA CONSERIA HASTA " " ANTES DE FOREIGN KEY
        elif(codigo_creacion[i] == "C" and codigo_creacion[i+1] == "O" and codigo_creacion[i+2] == "N" and codigo_creacion[i+3] == "S" and codigo_creacion[i+4] == "T" and codigo_creacion[i+5] == "R" and  codigo_creacion[i+6] == "A"):
            e = i
            while e < longitud:
                if(codigo_creacion[e]=="F" and codigo_creacion[e+1]=="O" and codigo_creacion[e+2]=="R" and codigo_creacion[e+3]=="E" and codigo_creacion[e+4]=="I"):
                    i = e-1
                    break
                else:
                    e = e + 1
                    #FINALIZA EL CODIGO
        elif(codigo_creacion[i] == " " and codigo_creacion[i-1] == ")" and codigo_creacion[i+1] == "E" and codigo_creacion[i+2] == "N" and codigo_creacion[i+3] == "G" and codigo_creacion[i+4] == "I"):
            break
        else:
            if(codigo_creacion[i] == "`"):
                i = i + 1
            else:
                new_string += codigo_creacion[i]
                i = i + 1
    return new_string #RETORNA CODIGO LIMPIO

#VERIFICA LA CANTIDAD DE LLAVES FORANEAS
def cantidad_llaves_foraneas(cursor, tabla : str) -> int:
    cantidad_de_llaves_foraneas : int = 0
    cantidad_de_llaves_primarias : int = 0
    cursor.execute("DESCRIBE " + tabla) #Obtiene la columna llaves
    llaves = cursor.fetchall()
    for llave in llaves:
        if(llave[3] == "MUL"):
            cantidad_de_llaves_foraneas += 1
        elif(llave[3] == "PRI"):
            cantidad_de_llaves_primarias += 1
    if(cantidad_de_llaves_primarias > 1):
        return 10 #10 es un valor cualquiera para discernir de los posibles valores de cantidades foraneas (0-2)
    else:
        return cantidad_de_llaves_foraneas

#ORDENA LA LOGICA PARA CREAR LAS TABLAS
def orden_de_creación(codigos_creacion : list[str], orden_creacion : list[int], Tabla : list[str]) -> None:
    tamaño = len(orden_creacion)
    for numero in orden_creacion:
        for i in range(0,tamaño-1):
             if(i < tamaño-1 and orden_creacion[i] > orden_creacion[i+1]): #Algoritmo de burbuja simple basado en llaves foraneas
                 auxiliar = orden_creacion[i+1]
                 auxiliar_str = codigos_creacion[i+1]
                 auxiliar_table = Tabla[i+1]
                 orden_creacion[i+1] = orden_creacion[i]
                 codigos_creacion[i+1] = codigos_creacion[i] 
                 Tabla[i+1] = Tabla[i]
                 orden_creacion[i] = auxiliar
                 codigos_creacion[i] = auxiliar_str
                 Tabla[i] = auxiliar_table

def extracción_datos(nombre_tabla:str,cursor):
    cursor.execute("select * from " + nombre_tabla)
    datos = cursor.fetchall()
    return datos

#EXTRAE LOS NOMBRES DE LAS COLUMNAS
def extraer_columnas(cursor, columnas : list[str], table_name):
    cursor.execute("DESCRIBE " + table_name)
    nombres = cursor.fetchall()
    for nombre in nombres:
        columnas.append(nombre[0])