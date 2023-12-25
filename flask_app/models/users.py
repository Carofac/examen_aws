#importar conexion bd
from flask_app.config.mysqlconnection import connectToMySQL

#importacion de expresiones regulares
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #Expresion regular de email

#importar flash para advertir errores al usuario
from flask import flash

#clase

class User:
    
    def __init__(self,data):
        #data = {diccionario con info de la instancia}
        self.id = data["id"]
        self.name = data["name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        
    @classmethod
    def save(cls, form):
        #form ={"first..": "elena"...} recibes un diccionario con el password ENCRIPTADO
        query = "INSERT INTO users (name, email, password) VALUES (%(name)s, %(email)s, %(password)s)"
        result = connectToMySQL("esquema_examen").query_db(query, form)
        return result #el id dell nuevo registro que se realizo
    
    #validar info que recibimos en el formulario
    @staticmethod
    def validate_user(form):
        #form con los names y valores que el usuario ingreso
        is_valid= True #pretendemos que el formulario esta correcto
        
        #validamos que el nombre tenga al menos dos caracteres
        if len(form["name"]) < 2:
            flash("Nombre debe tener al menos 2 caracteres", "register")
            is_valid = False
        
        #validamos que el password tenga al menos 6 cracteres
        if len(form["password"]) < 6:
            flash("Contraseña debe tener al menos 6 caracteres", "register")
            is_valid = False
        
        #validamos que el correo sea unico
        query = "SELECT * FROM  users WHERE email = %(email)s"
        results = connectToMySQL("esquema_examen").query_db(query, form)
        if len(results) >=1:
            flash("E-mail registrado previamente", "register")
            is_valid= False
        
        #verificamos contraseñas coinciden
        if form["password"] != form["confirm"]:
            flash("Contraseñas no coinciden", "register")
            is_valid = False
        
        #verificamos que el email tenfa el formaro correcto con ER
        if not EMAIL_REGEX.match(form["email"]):
            flash("E-mail invalido", "Register")
            is_valid = False
        
        return is_valid
    
    @classmethod
    def get_by_email(cls,form):

        query= "SELECT * FROM  users WHERE email = %(email)s"
        result= connectToMySQL("esquema_examen").query_db(query,form) # select regresa una lista de diccionario
        if len(result) < 1:
            return False
        else:
            #me regresa 1 registro
            #result=[{"id":1, "first_name": "ELena","last_name":.....}]
            user= cls(result[0])
            return user
        
    @classmethod
    def get_by_id(cls,form):
        #form = {"id":1}
        query = "SELECT * FROM users WHERE id=%(id)s"
        result = connectToMySQL("esquema_examen").query_db(query,form) #lista de diccionarios que solo tiene la posicion 0
        #result=[{"id":1, "first_name": "ELena","last_name":.....}]
        user = cls(result[0])
        return user
        