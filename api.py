# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
import main

app = Flask(__name__)
CORS(app)
api = Api(app)

class Api(Resource):
    
    def get(self,fecha_ini,fecha_fin,secuencia,date):      
        
        res = main.main(fecha_ini,fecha_fin,secuencia)
            
        json = [{"res"               :res},
                {"date"              :date}
                ]
        
        return json
        
api.add_resource(Api, '/fecha_ini/<fecha_ini>/fecha_fin/<fecha_fin>/secuencia/<secuencia>/date/<date>')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000,debug=True) 
    
    
#http://localhost:8000/fecha_ini/2020-12-01/fecha_fin/2020-12-02/secuencia/leito/date/5-433-45-6   