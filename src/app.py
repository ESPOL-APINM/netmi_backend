from flask import Flask, json, request
import logging
from flask_cors import CORS, cross_origin
from jinja2 import Environment, FileSystemLoader
import yaml
from gpapi import gpapi
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# CROSS ORIGIN PERMITE CONEXION CON FRONTEND

#FUNCION PARA PROBAR MICROSERVICIO
@app.route('/', methods=['GET'])
@cross_origin()
def status():
    print("Ok!")
    return "Hello Netmi!"

#FUNCION PARA PROBAR COMANDOS SHOWS EN DISPOSITIVOS
@app.route('/show', methods=['POST'])
@cross_origin()
def getshow():
    try:
        json_data = request.get_json() #RECIBE JSON DEL BODY DEL POST
        show = json_data["show"] #RECIBE PARAMETRO SHOW
        connection = gpapi(json_data)  #DEFINE CONEXION
        connection.connect() #INICIAR SESION
        parse = connection.showconfig("show version") #RECIBE DICCIONARIO DE SHOW
        connection.disconnect() #CIERRA SESION
        data = {"data": parse}  #DICCIONARIO FINAL 
        s = 200
    except:
        data = {"data": ""}
        s = 400
    response = app.response_class(response=json.dumps(data), #ENVIA EN FORMATO JSON EL REQUEST
                                  status=s,
                                  mimetype='application/json')
    return response

#FUNCION PARA PARSEAMIENTO EN YAML
@app.route('/getparsingyaml', methods=['POST'])
@cross_origin()
def getparsingyaml():
    try:
        json_data = request.get_json() #RECIBE JSON DEL BODY DEL POST
        show = json_data["show"] #RECIBE PARAMETRO SHOW
        plantilla = json_data["plantilla"]  #RECIBE PARAMETRO PLANTILLA
        connection = gpapi(json_data)  #DEFINE CONEXION
        connection.connect() #INICIAR SESION
        parse = connection.showconfig(show) #RECIBE DICCIONARIO DE SHOW
        data = {"data": parse} #DICCIONARIO FINAL
        try:
            show2 = json_data["show2"] #RECIBE PARAMETRO SHOW
            parse2 = connection.showconfig(show2) #RECIBE DICCIONARIO DE SHOW2
            data = {"data": parse, "data2": parse2} #DICCIONARIO FINAL
        except:
            data = {"data": parse} #DICCIONARIO FINAL
        connection.disconnect() #CIERRA SESION
        env = Environment(loader=FileSystemLoader( #DEFINE DIRECTORIO DE TRABAJO
            './'), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(plantilla) #DEFINE PLANTILLA A UTILIZAR
        doc = template.render(data) #RENDERIZACION
        s = 200
    except:
        doc = "no data"
        s = 400
    response = app.response_class(response=doc, #ENVIA DOCUMENTO FORMATO YAML
                                  status=s,
                                  mimetype='text/yaml')
    return response

# #FUNCION PARA PARSEAMIENTO EN CFG
@app.route('/getparsingcfg', methods=['POST'])
@cross_origin()
def getparsingcfg():
    try:
        json_data = request.get_json() #RECIBE JSON DEL BODY DEL POST
        show = json_data["show"]  #RECIBE PARAMETRO SHOW
        plantilla = json_data["plantilla"]  #RECIBE PARAMETRO PLANTILLA
        connection = gpapi(json_data)  #DEFINE CONEXION
        connection.connect() #INICIAR SESION
        parse = connection.showconfig(show) #RECIBE DICCIONARIO DE SHOW2
        data = {"data": parse} #DICCIONARIO FINAL
        try:
            show2 = json_data["show2"] #RECIBE PARAMETRO SHOW2
            parse2 = connection.showconfig(show2) #RECIBE DICCIONARIO DE SHOW2
            data = {"data": parse, "data2": parse2} #DICCIONARIO FINAL
        except:
            data = {"data": parse} #DICCIONARIO FINAL
        connection.disconnect() #CIERRA SESION
        env = Environment(loader=FileSystemLoader( #DEFINE DIRECTORIO DE TRABAJO
            './'), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(plantilla) #DEFINE PLANTILLA A UTILIZAR
        doc = template.render(data) #RENDERIZACION
        s = 200
    except:
        doc = "No data"
        s = 400
    response = app.response_class(response=doc, #ENVIA DOCUMENTO FORMATO YAML
                                  status=s,
                                  mimetype='text/cfg')
    return response

# STATIC ROUTE VRF


@app.route('/getvrfstaticroute', methods=['POST'])
@cross_origin()
def getvrfstaticroute():
    try:
        json_data = request.get_json()  #RECIBE JSON DEL BODY DEL POST
        plantilla = json_data["plantilla"] #RECIBE PARAMETRO PLANTILLA
        connection = gpapi(json_data)  #DEFINE CONEXION
        connection.connect() #INICIAR SESION
        parse = connection.showconfig("show vrf") #RECIBE DICCIONARIO DE COMANDO SHOW VRF
        vrf = {}
        for v in parse['vrf']:
            try:
                cmd = "show ip static route vrf "+v #DEFINE CADA SHOW DE RUTA ESTATICA CON VRF
                a = connection.showconfig(cmd) #RECIBE DICCIONARIO DE CADA RUTA ESTATICA VRF
                vrf[v] = a['vrf'][v] #DICCIONARIO PARA CADA VRF
            except:
                vrf = vrf 
        data = {"data": vrf} #DICCIONARIO FINAL
        connection.disconnect() #CIERRE SESION 
        env = Environment(loader=FileSystemLoader( #DEFINE DIRECTORIO DE TRABAJO
            './'), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(plantilla) #DEFINE PLANTILLA A UTILIZAR
        doc = template.render(data) #RENDERIZACION
        s = 200
    except:
        doc = "No data"
        s = 400
    response = app.response_class(response=doc, #ENVIA DOCUMENTO FORMATO TXT
                                  status=s,
                                  mimetype='text/txt')
    return response


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True) #DEFINE IP Y PUERTO DE MICROSERVICIO
