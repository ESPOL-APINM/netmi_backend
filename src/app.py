from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hola, Caro! Ya esta listo el entorno de desarrollo bb'