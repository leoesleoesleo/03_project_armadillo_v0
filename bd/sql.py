"""
Created on Mon Feb 10 10:51:34 2020

@author: leonardo.patino
"""

from sqlalchemy import create_engine
import mysql.connector
import sqlalchemy # Import dataframe into MySQL
import pandas as pd
import time
from conf.logger import logger


class Sql():
    
    def __init__(self,cache):
        self.cache = cache
        self.log = logger()
        
        self.database_username   = self.cache["database_username"]
        self.database_password   = self.cache["database_password"]
        self.database_ip         = self.cache["database_ip"]
        self.database_name       = self.cache["database_name"]
        
        self.database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(self.cache["database_username"],
                                                      self.cache["database_password"], 
                                                      self.cache["database_ip"],
                                                      self.cache["database_name"]))
        
        
    def insert_sql(self,df,name_table,metodo='replace',debug=True):  
        """ Inserta un un dataframe a la base de datos, creando la estrucura"""
        try:
            df.to_sql(con=self.database_connection, name=name_table, if_exists=metodo)
            if debug:
                self.log.Info("Tabla creada en sql con el nombre:" + str(name_table) + " metodo: " + str(metodo) + " en la base de datos: " + str(self.database_name))
            conn = self.database_connection.connect()
            conn.close()
            return 'registros Insertados'
        except Exception as e:
            self.log.Error("Problemas para insertar en sql " + str(e))
    
    def insert_sql_masivo(self,df,name_table,lote=300,metodo="replace"):
        """Inserta de forma masiva un dataframe a la base de datos, 
        , recibe parametro metodo=append para agregar, si no recibe este parametro
        por defecto creara la estructura en el primer recorrido,
        tambien recibe como parametro los lotes en el que se divide la ingesta masiva"""
        try:
            n = len(df)
            incremento = lote
            aux = 0
            v_lote = []
            while lote < n:
                df_ = df.loc[aux:lote,]
                self.insert_sql(df_,name_table,metodo=metodo,debug=False)
                metodo = "append"
                aux = lote + 1
                lote += incremento
                v_lote.append(lote)
            res = 'registros Insertados, ciclos: ',len(v_lote)   
            return res    
        except Exception as e:
            self.log.Error("Problemas inserción masiva en sql " + str(e))       
        
    def listar_sql(self,query,fichero=False,nombre=False):
        """Ejecuta un query y lo convierte a objeto pandas"""
        try:            
            res = self.execute(query,param='interno')            
            data = pd.DataFrame(data=res) 
            if fichero:
                if nombre == False:
                    time.ctime()
                    nombre = time.strftime('%Y%m%d%H%M%S')
                else:
                    nombre = nombre
                data.to_excel('ficheros/' + str(nombre) + '.xlsx', sheet_name='dataframe')
                self.log.Info("Archivo " + str(nombre) + " generado en la carpeta ficheros correctamente")                    
                return "Archivo generado correctamente"
            else:
                return data
        except Exception as e:
            self.log.Error("Problemas para listar en sql " + str(e))
    
    def execute(self,query,param='none'):
        """Ejecuta un query en específico sin devolución de resultados"""
        try:
            mydb = mysql.connector.connect(
              host=self.database_ip, 
              user=self.database_username,
              passwd=self.database_password,
              database=self.database_name
            )
            mycursor = mydb.cursor()
            mycursor.execute(query)
            
            if param == 'none':
                mydb.commit()            
                mydb.close()
                return "ejecución ok"
            else:
                res  = mycursor.fetchall() #método, que recupera todas las filas de la última instrucción ejecutada.
                mydb.close()
                return res
                
        except Exception as e:
            self.log.Error("Problemas para ejecutar en sql " + str(e))
            

