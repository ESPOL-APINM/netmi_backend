from flask import Flask,json,request
import logging
from flask_cors import CORS, cross_origin
from jinja2 import Environment, FileSystemLoader
import yaml
from gpapi import gpapi
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/',methods=['GET'])
@cross_origin()
def defaultfunction():
    return "Hello World"

@app.route('/show',methods=['POST'])
@cross_origin()
def show():
    try:
        json_data = request.get_json()
        connection =  gpapi(json_data)
        parse = connection.showconfig("show access-list")
        data = {"data":parse} 
        s=200
    except:
        doc="No data"
        s=400
    response = app.response_class(response=json.dumps(data),
                                  status=200,
                                  mimetype='application/json')
    return response

#YAML
@app.route('/getparsingyaml',methods=['POST'])
@cross_origin()
def getparsingyaml():
    try:
        json_data = request.get_json()
        show = json_data["show"]
        plantilla = json_data["plantilla"]
        connection =  gpapi(json_data)
        parse = connection.showconfig(show)
        data = {"data":parse} 
        connection.disconnect()
        try:
            show2 = json_data["show2"]
            parse2 = connection.showconfig(show2)
            data = {"data":parse,"data2":parse2} 
        except:
            data = {"data":parse} 
        connection.disconnect()
        env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(plantilla)
        doc = template.render(data)
        s=200
    except:
        doc="No data"
        s=400
    response = app.response_class(response=doc,
                                  status=s,
                                  mimetype='text/yaml')
    return response

#CFG
@app.route('/getparsingcfg',methods=['POST'])
@cross_origin()
def getparsingcfg():
    try:
        json_data = request.get_json()
        show = json_data["show"]
        plantilla = json_data["plantilla"]
        connection =  gpapi(json_data)
        parse = connection.showconfig(show)
        data = {"data":parse} 
        connection.disconnect()
        try:
            show2 = json_data["show2"]
            parse2 = connection.showconfig(show2)
            data = {"data":parse,"data2":parse2} 
        except:
            data = {"data":parse} 
        connection.disconnect()
        env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(plantilla)
        doc = template.render(data)
        s=200
    except:
        doc="No data"
        s=400
    response = app.response_class(response=doc,
                                  status=s,
                                  mimetype='text/cfg')
    return response

#STATIC ROUTE VRF
@app.route('/getvrfstaticroute',methods=['POST'])
@cross_origin()
def getvrfstaticroute():
    try:
        json_data = request.get_json()
        plantilla = json_data["plantilla"]
        connection =  gpapi(json_data)
        parse = connection.showconfig("show vrf")
        vrf={}
        for v in parse['vrf']:
            try:
                cmd="show ip static route vrf "+v
                a= connection.showconfig(cmd)
                vrf[v]=a['vrf'][v]
            except:
                vrf=vrf
        data={"data":vrf}
        connection.disconnect()
        env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(plantilla)
        doc = template.render(data)
        s=200
    except:
        doc="No data"
        s=400
    response = app.response_class(response=doc,
                                  status=s,
                                  mimetype='text/cfg')
    return response

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == "__main__":
     app.run(host='127.0.0.1', port=8080, debug=True)
