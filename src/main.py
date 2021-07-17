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
        connection =  gpapi("./testbed.yaml","RIOS1")
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
        name = json_data["name"]
        connection =  gpapi("./testbed.yaml",name)
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
        connection =  gpapi("./testbed.yaml",name)
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
        connection =  gpapi("./testbed.yaml",name)
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
        connection =  gpapi("./testbed.yaml",name)
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
        connection =  gpapi("./testbed.yaml",name)
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
        connection =  gpapi("./testbed.yaml",name)
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

#TESTBED FUNCTIONS
@app.route('/addtoyaml',methods=['POST'])
@cross_origin()
def addYaml():
    try:
        json_data = request.get_json()
        name = json_data["name"]
        os = json_data["os"]
        ip = json_data["ip"]
        username = json_data["username"]
        password = json_data["password"]
        secret = json_data["epassword"]
        print(name)
        new_yaml_data_dict = {
            name:{
                'connections':{
                    'cli':{
                        'ip': ip,
                        'protocol': 'ssh -c aes128-cbc'
                    }
                },
                'credentials':{
                    'default':{
                        'username': username,
                        'password': password
                    },'enable':{
                        'password': secret                }
                },
                'os': os,
                'type': os
            }
        }
            
        with open('./testbed.yaml','r') as yamlfile:
            testbedyaml = yaml.safe_load(yamlfile) # Note the safe_load
            testbedyaml['devices'].update(new_yaml_data_dict)

        if testbedyaml:
            with open('testbed.yaml','w') as yamlfile:
                yaml.safe_dump(testbedyaml, yamlfile) 
        d="OK"
        s=200
    except:
        d="Error addYaml"
        s=400
    
    data = {"data":d}
    response = app.response_class(response=json.dumps(data),
                                  status=s,
                                  mimetype='application/json')
    return response
    
if __name__ == "__main__":
    app.run(debug=True)
