from flask import Flask,json,request
import yaml
from gpapi import gpapi
app = Flask(__name__)

@app.route('/getvrf',methods=['POST'])
def getvrf():
    json_data = request.get_json()
    name = json_data["name"]
    connection =  gpapi("./testbed.yaml",name)
    parse = connection.get_vrf_detail()
    data = {"data":parse} 
    response = app.response_class(response=json.dumps(data),
                                  status=200,
                                  mimetype='application/json')
    return response

@app.route('/getvrfyaml',methods=['POST'])
def getvrfyaml():
    
    connection =  gpapi("./testbed.yaml","RIOS1")
    parse = connection.get_vrf_detail()
    vrfs = {}
    for i in parse: 
        vrfs[i]={"vrf_name" : i}   
        dict_target = parse[i] 
        print(dict_target)
        dict_routes=dict_target["address_family"]["ipv4"]
             
        if "route_distinguisher" in dict_target.keys():
            route_distinguisher=dict_target["route_distinguisher"]
            vrfs[i]["vrf_rd"] = route_distinguisher
        else:
            doc=i+" no tiene route_distinguisher"
            s=400
            break 

        if "route_targets" not in dict_routes.keys():
            doc=i+" no tiene route_targets"
            print("no route_targets")
            s=400
            break 
        route_targets = dict_routes["route_targets"] 

        if "description" in dict_target.keys():
            description=dict_target["description"]
            vrfs[i]["vrf_dct"] = description

        if "import_route_map" in dict_routes.keys():
            route_imap = dict_routes["import_route_map"] 
            vrfs[i]["vrf_imap"] = route_imap

        if "export_route_map" in dict_routes.keys():
            route_emap = dict_routes["export_route_map"] 
            vrfs[i]["vrf_emap"] = route_emap

        if "routing_table_limit" in dict_routes.keys():
            route_limit = dict_routes["routing_table_limit"]
            route_limit_percent = route_limit["routing_table_limit_action"]["enable_alert_percent"]["alert_percent_value"]
            route_limit_number = route_limit["routing_table_limit_number"]
            vrfs[i]["vrf_lper"] = route_limit_percent
            vrfs[i]["vrf_ln"] = route_limit_number
        print("n")
        n=1
        for rt in route_targets:
            dict_rt= route_targets.get(rt)
            rttype=dict_rt.get("rt_type")
            if rttype=="both":
                vrfs[i]["vrf_ex"+str(n)]=dict_rt.get("route_target")
                vrfs[i]["vrf_im"+str(n)]=dict_rt.get("route_target")
            elif rttype=="export":
                vrfs[i]["vrf_ex"+str(n)]=dict_rt.get("route_target")
            elif rttype=="import":
                vrfs[i]["vrf_im"+str(n)]=dict_rt.get("route_target")
            n=n+1

    doc = yaml.dump(vrfs)
    s=200
    #except:
    #    doc=""
    #    s=400

    #data = {"data":parse} # Your data in JSON-serializable type
    response = app.response_class(response=doc,
                                  status=s,
                                  mimetype='text/yaml')
    return response

@app.route('/addtoyaml',methods=['POST'])
def addYaml():
    try:
        json_data = request.get_json()
        name = json_data["name"]
        os = json_data["os"]
        ip = json_data["ip"]
        username = json_data["username"]
        password = json_data["password"]
        secret = json_data["secret"]
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
