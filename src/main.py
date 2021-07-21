from flask import Flask,json,request
from flask_cors import CORS, cross_origin
from jinja2 import Environment, FileSystemLoader
import yaml
from gpapi import gpapi
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/show',methods=['POST'])
@cross_origin()
def getvrf():
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

#VRF
@app.route('/getvrfconfig',methods=['POST'])
@cross_origin()
def getvrfconfig():
    try:
        json_data = request.get_json()
        connection =  gpapi(json_data)
        parse = connection.showconfig("show vrf detail")
        data = {"data":parse} 
        env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template('./plantillas/vrfdetail.j2')
        doc = template.render(data)
        s=200
    except:
        doc="No data"
        s=400
    response = app.response_class(response=doc,
                                  status=s,
                                  mimetype='text/cfg')
    return response

@app.route('/getvrfyaml',methods=['POST'])
@cross_origin()
def getvrfyaml():
    try:
        json_data = request.get_json()
        name = json_data["name"]
        connection =  gpapi(json_data)
        parse = connection.showconfig("show vrf detail")
        data = {"data":parse} 
        env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template('./plantillas/vrfdetailyaml.j2')
        doc = template.render(data)
        s=200
    except:
        doc="No data"
        s=400
    response = app.response_class(response=doc,
                                  status=s,
                                  mimetype='text/yaml')
    return response

#MP BGP VRF
@app.route('/getmpbgpvrfconfig',methods=['POST'])
@cross_origin()
def getmpbgpvrfconfig():
    try:
        json_data = request.get_json()
        name = json_data["name"]
        connection =  gpapi(json_data)
        parse = connection.showconfig("show vrf detail")
        data = {"data":parse} 
        env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template('./plantillas/mpbgpvrf.j2')
        doc = template.render(data)
        s=200
    except:
        doc="No data"
        s=400
    response = app.response_class(response=doc,
                                  status=s,
                                  mimetype='text/cfg')
    return response

@app.route('/getmpbgpvrfyaml',methods=['POST'])
@cross_origin()
def getmpbgpvrfyaml():
    try:
        json_data = request.get_json()
        name = json_data["name"]
        connection =  gpapi(json_data)
        parse = connection.showconfig("show vrf detail")
        data = {"data":parse} 
        env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template('./plantillas/mpbgpvrfyaml.j2')
        doc = template.render(data)
        s=200
    except:
        doc="No data"
        s=400
    response = app.response_class(response=doc,
                                  status=s,
                                  mimetype='text/yaml')
    return response

#ACCESS-LIST
@app.route('/getaclconfig',methods=['POST'])
@cross_origin()
def getaclconfig():
    try:
        json_data = request.get_json()
        name = json_data["name"]
        connection =  gpapi(json_data)
        parse = connection.showconfig("show access-list")
        data = {"data":parse} 
        env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template('./plantillas/accesslist.j2')
        doc = template.render(data)
        s=200
    except:
        doc="No data"
        s=400
    response = app.response_class(response=doc,
                                  status=s,
                                  mimetype='text/cfg')
    return response

@app.route('/getaclyaml',methods=['POST'])
@cross_origin()
def getaclyaml():
    try:
        json_data = request.get_json()
        name = json_data["name"]
        connection =  gpapi(json_data)
        parse = connection.showconfig("show access-list")
        data = {"data":parse} 
        env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
        template = env.get_template('./plantillas/accesslistyaml.j2')
        doc = template.render(data)
        s=200
    except:
        doc="No data"
        s=400
    response = app.response_class(response=doc,
                                  status=s,
                                  mimetype='text/yaml')
    return response

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

   

if __name__ == "__main__":
    app.run(debug=True)
