from flask import Flask
from flask import request

app = Flask(__name__)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown')
def shutdown():
    shutdown_server()
    app.run()
    return 'Server restarting now...'


@app.route('/')
def hello_world():
    return 'Hola, Caro! Ya esta listo el entorno de desarrollo abb'
