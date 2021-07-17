from genie import testbed

class gpapi(object):
    def __init__(self, testbed_file=None,device_name=None):
        test = testbed.load(testbed_file)
        self.device = test.devices[device_name]

    def connect(self):
        self.device.connect(init_exec_commands=[], init_config_commands=[], log_stdout=False)

    def disconnect(self):
        self.device.disconnect()

    def showconfig(self,show=None):
        self.connect()
        parse = self.device.parse(show)
        self.disconnect()
        return parse
