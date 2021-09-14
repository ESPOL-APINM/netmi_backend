from genie import testbed

class gpapi(object):
    def __init__(self,json_data=None):

        name = json_data["name"]
        ip = json_data["ip"]
        protocol = json_data["protocol"]
        password = json_data["password"]
        username = json_data["username"]
        os = json_data["os"]
        enable = json_data["enable"]
        port = json_data["port"]
        encriptacion = json_data["encryp"]
        if(protocol=="ssh"):
            protocol=protocol+" -c "+encriptacion
        testbeddict={"devices":{
                name:{
                    "connections":{
                        "cli":{
                            "ip":ip,
                            "protocol": protocol,
                            "port":port
                        }
                    },
                    "credentials":{
                        "default":{
                            "username": username,
                            "password": password
                        },"enable":{
                            "password": enable
                        }
                    },    
                     "os": os
                    }
                 }}
        test = testbed.load(testbeddict)
        self.device = test.devices[name]

    def connect(self):
        self.device.connect(init_exec_commands=[], init_config_commands=[], log_stdout=False)

    def disconnect(self):
        self.device.disconnect()

    def showconfig(self,show=None):
        self.connect()
        parse = self.device.parse(show)
        return parse