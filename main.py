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
        if show=="show interfaces":
            show2 = json_data["show2"]
            parse=connection.showconfig2parsers(show,show2)
            data=parse
        else:
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
