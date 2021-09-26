from genie import testbed

class gpapi(object):
    #FUNCION PARA DEFINIR DISPOSITIVO
    def __init__(self,json_data=None):
        encriptacion = ""
        name = json_data["name"]
        ip = json_data["ip"]
        protocol = json_data["protocol"]
        password = json_data["password"]
        username = json_data["username"]
        enable = json_data["enable"]
        os = json_data["os"]
        try:
            encriptacion = json_data["encryp"]
        except:
            encriptacion = ""        

        if(protocol=="ssh"):
            if(encriptacion != ""):
                protocol=protocol+" -c "+encriptacion
        #DEFINE AL DISPOSITIVO
        #IP direccion ip
        #PROTOCOL (SSH o TELNET)    ssh puede ingresar con encriptacion ssh -c aes128-cbc
        #username define usuario de ssh
        #password define contrasena de ssh
        #os define sistema operativo ios iosxe
        #enable define contrasena enable para conexion ssh
        testbeddict={"devices":{
                name:{
                    "connections":{
                        "cli":{
                            "ip":ip,
                            "protocol": protocol,
                            "port":0
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
        #load carga el diccioario
        test = testbed.load(testbeddict)
        #elige el dispositivo 
        self.device = test.devices[name]

    #FUNCION PARA INICIAR CONEXION 
    def connect(self):
        self.device.connect(init_exec_commands=[], init_config_commands=[], log_stdout=False)
    
    #FUNCION PARA DESCONECTAR CONEXION
    def disconnect(self):
        self.device.disconnect()
    
    #FUNCION PARA OBTENER PARSER DE SHOWS 
    def showconfig(self,show=None):
        parse = self.device.parse(show)
        return parse