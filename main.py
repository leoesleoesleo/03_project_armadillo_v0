"""
Created on Mon Feb 10 10:51:34 2020

@author: leonardo.patino
"""
import argparse
import math
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib

from conf.logger import logger
from bd.sql import Sql
from clase.Dataminig.analisis import Analisis
from clase.Dataminig.limpieza import Limpieza

class Main:    
    def __init__(self):        
        pass
               
    def get_config(self,bd):
        with open('conexion/'+bd+'.json') as f_in:
            json_str = f_in.read()
            return json.loads(json_str)
            
    def main(self):
        log.Info("********** Ejecución iniciada *********")
        log.Info("********** Fin Ejecución **************")

                                         
#instancias         
log = logger()
a = Analisis()
l = Limpieza()

reto = Main()
m = Sql(reto.get_config('mysql'))
df = reto.main()
reto.predict(df)
reto.fit(df)    
        
    
    
    