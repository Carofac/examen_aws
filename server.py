#importar la app
from flask_app import app

#importar controladores
from flask_app.controllers import users_controller
from flask_app.controllers import appointments_controller

#ejecucion de la app
if __name__ == "__main__":
    app.run(debug=True)