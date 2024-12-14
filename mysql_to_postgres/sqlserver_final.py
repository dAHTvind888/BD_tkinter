import pyodbc

#FUNCION QUE DEVUELVE CONEXION SQLSERVER
def connection(Driver : str, Servidor : str):
    base_sqlserver = pyodbc.connect("Driver="+Driver+
                                    "Server="+Servidor+";"
                                    "Trusted_Connection=yes;",
                                    autocommit=True)
    print("Conexión Exitosa a SQLSERVER")
    print()
    return base_sqlserver

#FUNCION QUE DEVUELVE CURSOR SQLSERVER
def cursor(connection):
    return connection.cursor()

#FUNCION QUE CIERRA CONEXION SQLSERVER
def disconnection(connection,cursor) -> None:
    cursor.close()
    connection.close()
    print("Desconectado de SQLSERVER")

#FUNCION QUE VERIFICA SI LA TABLA EXISTE EN SQLSERVER
def verificacion(nombre_de_base_de_dato_origen, cursor) -> int:
    cursor.execute("SELECT name FROM sys.databases") #SELECT name FROM sys.databases extrae las bases de sqlserver
    bases = cursor.fetchall()
    verificador = 0
    for base in bases:
        if(nombre_de_base_de_dato_origen == base[0]):
            verificador += 1
    if(verificador > 0): #MAYOR QUE 0 EXISTE
        print("Base de Datos Existente en SQLSERVER")
        print()
        return verificador
    else: #IGUAL A 0 NO EXISTE POR LO QUE SE CREA
        cursor.execute("CREATE DATABASE " + nombre_de_base_de_dato_origen)
        cursor.execute("USE " + nombre_de_base_de_dato_origen)
        print("Base de Datos no existe en SQLSERVER, por lo tanto se creara")
        print()
        return verificador
    
    #FUNCION QUE CREA LAS TABLAS EN SQLSERVER
def creacion_de_tablas(cursor, codigos_creacion : list[str]):
    for codigo in codigos_creacion: 
        cursor.execute(codigo)
    print("Creación Exitosa de las Tablas")
    print()

#Crea codigo para insertar valores con increase, pero no lo inserta directamente 
def codigo_de_ejecución_increase(table_name,columnas_nombre) -> str:
    inicio = 1
    fin = len(columnas_nombre)-1
    columnas = ""
    valores = ""
    for i in range (inicio,fin,1):
        if(i == fin-1):
            columnas += columnas_nombre[i]
            valores += "?"
        else:
            columnas += columnas_nombre[i] + ", "
            valores += "?, "
    codigo_guía = "insert into " + table_name +"(" + columnas + ") values (" + valores + ")" 
    return codigo_guía

#Inserta Datos a SQLSERVER
def transferiencia_incrementado(cursor,datos,columnas,codigo,table_name):
    inicio = 1
    fin = len(columnas)-1
    lista_datos = []
    for dato in datos: #Acceder a los datos
        for i in range (inicio,fin,1): #Acceder al dato/Celda
            lista_datos.append(dato[i])
        cursor.execute(codigo,(lista_datos)) #Codigo es insert into ... y iista de datos son los valores
        lista_datos.clear()
    cursor.execute("update " + table_name + " set " + columnas[fin] + " = GETDATE()")
    print(f"Migración exitosa a la tabla {table_name}")

#Crea codigo para insertar valores sin increase, pero no lo inserta directamente 
def codigo_de_ejecución_sin_incremento(table_name,columnas_nombre) -> str:
    inicio = 0
    fin = len(columnas_nombre)-1
    columnas = ""
    valores = ""
    for i in range (inicio,fin,1):
        if(i == fin-1):
            columnas += columnas_nombre[i]
            valores += "?"
        else:
            columnas += columnas_nombre[i] + ", "
            valores += "?, "
    query = "insert into " + table_name +"(" + columnas + ") values (" + valores + ")" 
    return query


#Inserta Datos a SQLSERVER sin increase
def transferiencia_sin_incremento(cursor,datos,columnas,codigo,table_name):
    inicio = 0
    fin = len(columnas)-1
    lista_datos = []
    for dato in datos:
        for i in range (inicio,fin,1):
            lista_datos.append(dato[i])
        cursor.execute(codigo,(lista_datos))
        lista_datos.clear()
    cursor.execute("update " + table_name + " set " + columnas[fin] + " = GETDATE()")
    print(f"Migración exitosa a la tabla {table_name}")