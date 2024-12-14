from dataclasses import dataclass
#OBJETOS
@dataclass
class Database:
    nombre_base : str 
    cursor : any 

    #RETORNA CURSOR
    def llamar_base(self):
        self.cursor.execute("USE " + self.nombre_base)
        return self.cursor

@dataclass
class Tabla_MYSQL(Database):
    nombre : str
    #RETORNA REGISTROS MYSQL
    def calcular_registros_msq(self, tabla) -> int:
        cursor = self.llamar_base()
        cursor.execute("SELECT count(*) FROM " + tabla)
        cantidad_registros = cursor.fetchone()
        return cantidad_registros[0]

    #RETORNA DATOS PERO EN UNA LISTA MYSQL
    def extraer_datos(self,tabla,columnas):
        cursor = self.llamar_base()
        inicio = 0
        fin = len(columnas)-1
        columnas_nombre = ""
        for i in range (0,fin,1):
            if(i == fin-1):
                columnas_nombre += columnas[i]
            else: 
                columnas_nombre += columnas[i] + ", "
        cursor.execute("SELECT " + columnas_nombre + " FROM " + tabla)
        datos = cursor.fetchall()
        lista = []
        for dato in datos:
            for i in range (0,fin,1):
                lista.append(dato[i])
        return lista
    
@dataclass
class Tabla_SQLSERVER(Database):
    nombre : str

    #RETORNA REGISTROS SQLSERVER
    def calcular_registros_sql(self, tabla) -> int:
        cursor = self.llamar_base()
        cursor.execute("SELECT count(*) FROM " + tabla)
        cantidad_registros = cursor.fetchone()
        return cantidad_registros[0]
    
    #RETORNA DATOS PERO EN UNA LISTA SQLSERVER
    def extraer_datos(self,tabla,columnas):
        cursor = self.llamar_base()
        inicio = 0
        fin = len(columnas)-1
        columnas_nombre = ""
        for i in range (0,fin,1):
            if(i == fin-1):
                columnas_nombre += columnas[i]
            else: 
                columnas_nombre += columnas[i] + ", "
        cursor.execute("SELECT " + columnas_nombre + " FROM " + tabla)
        datos = cursor.fetchall()
        lista = []
        for dato in datos:
            for i in range (0,fin,1):
                lista.append(dato[i])
        return lista
    
    #PRUEBA DE TRANSFERENCIA 1, MUESTRA DATOS DE TABLA MANGA
def prueba(cursor):
        cursor.execute("SELECT * FROM MANGA")
        datos = cursor.fetchall()
        for dato in datos:
            print(f"{dato[0]}  {dato[1]}  {dato[2]}  {dato[3]}  {dato[4]}  {dato[5]}")

    #PRUEBA DE TRANSFERENCIA 2, MUESTRA DATOS DE TABLA MANGA Y VOLUMEN
def prueba_join(cursor):
        cursor.execute("select * from manga inner join Volume on manga.Id_Manga = volume.Id_Manga where manga.Id_Manga = 1;")
        datos = cursor.fetchall()
        for dato in datos:
            print(f"{dato[0]}  {dato[1]}  {dato[2]}  {dato[3]}  {dato[4]}  {dato[5]}  {dato[6]}  {dato[11]}")