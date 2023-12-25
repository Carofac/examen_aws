from flask import Flask #importamos flask

app = Flask(__name__) #inicializamos app

app.secret_key = "llave secreta" #se necesita para la sesion