import mysql_final as MSQ
import sqlserver_final as SQL
import pruebas as PS

try:
    #Ingreso de credenciales para mysql 
    print("Verifique sus Credencianles antes de conectar a MYSQL")
    anfitrion : str = input("Ingrese su host: ")
    usuario : str = input("Ingresa su usuario: ")
    contraseña : str = input("Ingrese su contaseña: ")
    puerto : str = input("Ingrese su port: ")
    print()

    #FUNCION QUE DEVUELVE CONEXION MYSQL
    conexion1 = MSQ.connection(anfitrion,usuario,contraseña,puerto)
    #FUNCION QUE DEVUELVE CURSOR MYSQL
    cursor1 = MSQ.cursor(conexion1)

    #MUESTRA LOS DRIVER A ELECCION
    lista_de_Driver : str = ["ODBC Driver 13.1 for SQL Server;",
                             "ODBC Driver 17 for SQL Server;",
                             "ODBC Driver 18 for SQL Server;"]
    print("Verifique sus Credencianles antes de conectar a SQLSERVER")
    for driver in lista_de_Driver:
        print(driver)
    #Ingreso de credenciales para mysql
    Driver : int = int(input("Seleccione el Driver de numeración 0 - 2: "))
    Servidor : str = input("Ingrese su Servidor: ")
    print()
    
    #FUNCION QUE DEVUELVE CONEXION SQLSERVER
    conexion2 = SQL.connection(lista_de_Driver[Driver],Servidor)
    #FUNCION QUE DEVUELVE CURSOR SQLSERVER
    cursor2 = SQL.cursor(conexion2)

    #VARIABLES AUXILIARES
    tablas : list[str] = []
    tablas_con_funcion_incremento = []
    codigos_para_creacion_de_tablas : list[str] = []
    orden_logico : list[int] = []
    nombre_de_columnas : list[str] = []
    codigo_auxiliar = ""
    numero_auxiliar = 0
    #FUNCION QUE MUESTRA LAS BASES DE DATOS EXISTENTES EN MYSQL
    MSQ.mostrar_base_de_datos(cursor1)
    #FUNCION QUE SELECCIONA LA BASE DE DATOS A MIGRAR Y DEVUELVE LA BASE SELECCIONADA
    base_origen = MSQ.elegir_base_origen(cursor1)
    #VERIFICA SI EXISTE LA BASE SELECCIONADA EN SQLSERVER, RETORNA 1 SI EXISTE
    numero_auxiliar = SQL.verificacion(base_origen,cursor2)

    #EXISTE EN SQLSERVER
    if(numero_auxiliar == 1):
        print("Se compararan las bases de datos")
        print()

        #Comparación

        #CREAR OBJETOS BASE DE DATOS Y TABLA DE pruebas.py
        MYSQL = PS.Database(base_origen, cursor1)
        SQLSERVER = PS.Database(base_origen,cursor2)

        TABLA_MYSQL = PS.Tabla_MYSQL(MYSQL.nombre_base,MYSQL.cursor,"TABLA_MYSQL")
        TABLA_SQLSERVER = PS.Tabla_SQLSERVER(SQLSERVER.nombre_base,SQLSERVER.cursor,"TABLA_SQLSERVER")

        #OBTENER NOMBRES DE LAS TABLAS
        tablas = MSQ.tablas(cursor1,base_origen)

        for tabla in tablas:
            registros_mysql = PS.Tabla_MYSQL.calcular_registros_msq(TABLA_MYSQL,tabla)
            registros_sqlserver = PS.Tabla_SQLSERVER.calcular_registros_sql(TABLA_SQLSERVER, tabla)
            print(f"Registros de MYSQL de la tabla {tabla} = {registros_mysql}")
            print(f"Registros de SQLSERVER de la tabla {tabla} = {registros_sqlserver}")
            assert registros_sqlserver == registros_mysql, "Los registros no son Iguales"
        print()

        for tabla in tablas:
            MSQ.extraer_columnas(cursor1,nombre_de_columnas,tabla)
            registros_sqlserver = PS.Tabla_MYSQL.extraer_datos(TABLA_MYSQL,tabla, nombre_de_columnas)
            registros_mysql = PS.Tabla_SQLSERVER.extraer_datos(TABLA_SQLSERVER, tabla, nombre_de_columnas)
            if(registros_sqlserver == registros_mysql):
                print(f"datos de mysql son iguales a los datos de sql server respecto a la tabla {tabla}")
            else:
                print("datos de mysql no son iguales a los datos de sql server respecto a la tabla {tabla}")
            assert registros_sqlserver == registros_mysql, "Los registros no son Iguales"
            nombre_de_columnas.clear()
        print()

        print("Bases Comparadas, contienen la misma información")



    else:
        print("Comenzando Proceso de Transferiencia")
        print()
        #EXTRAE TABLAS
        tablas = MSQ.tablas(cursor1,base_origen)

        codigo_creacion : str = ""

        #GUARDA CODIGOS DE CREACION DE TABLA Y GUARDA CANTIDAD DE LLAVES FORANEAS
        for tabla in tablas:
            codigo_creacion = MSQ.extraer_codigo_creacion(cursor1,tabla)
            codigo_auxiliar = MSQ.limpiar_codigo_creacion(codigo_creacion,tablas_con_funcion_incremento)
            codigos_para_creacion_de_tablas.append(codigo_auxiliar)
            orden_logico.append(MSQ.cantidad_llaves_foraneas(cursor1,tabla))

        #ORDENA LOGICA PARA CREAR TABLAS
        MSQ.orden_de_creación(codigos_para_creacion_de_tablas,orden_logico,tablas)

        #CREA TABLAS
        SQL.creacion_de_tablas(cursor2,codigos_para_creacion_de_tablas)

        
        for tabla in tablas:
            #EXTRAE DATOS
            datos = MSQ.extracción_datos(tabla,cursor1)
            #EXTRAE COLUMNAS
            MSQ.extraer_columnas(cursor1,nombre_de_columnas,tabla)
            numero_auxiliar = 0
            #VERIFICA SI LA ID DE LA TABLA SE GENRA AUTOMATICAMENTE
            for subtabla in tablas_con_funcion_incremento:
                if(tabla == subtabla):
                    numero_auxiliar += 1
            if(numero_auxiliar == 1): #SI SE GENRA AUTOMATICAMNETE RETORNA NUMERO AUXILIAR 1
                codigo_auxiliar = SQL.codigo_de_ejecución_increase(tabla,nombre_de_columnas)
                SQL.transferiencia_incrementado(cursor2, datos, nombre_de_columnas, codigo_auxiliar, tabla)
            else: #NO SE GENERA AUTOMATICAMENET
                codigo_auxiliar = SQL.codigo_de_ejecución_sin_incremento(tabla,nombre_de_columnas)
                SQL.transferiencia_sin_incremento(cursor2, datos, nombre_de_columnas, codigo_auxiliar, tabla)
            numero_auxiliar = 0
            nombre_de_columnas.clear()
        print()

        #Pruebas

        MYSQL = PS.Database(base_origen, cursor1)
        SQLSERVER = PS.Database(base_origen,cursor2)

        TABLA_MYSQL = PS.Tabla_MYSQL(MYSQL.nombre_base,MYSQL.cursor,"TABLA_MYSQL")
        TABLA_SQLSERVER = PS.Tabla_SQLSERVER(SQLSERVER.nombre_base,SQLSERVER.cursor,"TABLA_SQLSERVER")

        for tabla in tablas:
            registros_mysql = PS.Tabla_MYSQL.calcular_registros_msq(TABLA_MYSQL,tabla)
            registros_sqlserver = PS.Tabla_SQLSERVER.calcular_registros_sql(TABLA_SQLSERVER, tabla)
            print(f"Registros de MYSQL de la tabla {tabla} = {registros_mysql}")
            print(f"Registros de SQLSERVER de la tabla {tabla} = {registros_sqlserver}")
            assert registros_sqlserver == registros_mysql, "Los registros no son Iguales"
        print()

        for tabla in tablas:
            MSQ.extraer_columnas(cursor1,nombre_de_columnas,tabla)
            registros_sqlserver = PS.Tabla_MYSQL.extraer_datos(TABLA_MYSQL,tabla, nombre_de_columnas)
            registros_mysql = PS.Tabla_SQLSERVER.extraer_datos(TABLA_SQLSERVER, tabla, nombre_de_columnas)
            if(registros_sqlserver == registros_mysql):
                print(f"datos de mysql son iguales a los datos de sql server respecto a la tabla {tabla}")
            else:
                print("datos de mysql no son iguales a los datos de sql server respecto a la tabla {tabla}")
            assert registros_sqlserver == registros_mysql, "Los registros no son Iguales"
            nombre_de_columnas.clear()
        print()

        if(base_origen == 'manga_store'):
            PS.prueba(cursor2)
            print()
            PS.prueba_join(cursor2)
            print()

except Exception as error:
    print("Error:")
    print(error)

finally:
    print()
    MSQ.disconnection(conexion1,cursor1)
    SQL.disconnection(conexion2,cursor2)