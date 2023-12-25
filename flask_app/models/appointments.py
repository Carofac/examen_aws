#importar conexion bd
from flask_app.config.mysqlconnection import connectToMySQL

#importar flash para advertir errores al usuario
from flask import flash

#sirve para manipular fechas y saber la actual
from datetime import datetime

#clase
class Appointment:
    
    def __init__(self,data):
        
        self.id = data["id"]
        self.task = data["task"]
        self.date = data["date"]
        self.status = data["status"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        
        
#validar cita
        
    @staticmethod
    def validate_task(form):
        is_valid = True
        
        if form["task"] == "":
            flash("Cita no puede ser vacio", "appointments")
            is_valid = False
                
        if form["date"] == "":
            flash("Ingrese una fecha", "appointments")
            is_valid = False
            
        if datetime.strptime(form["date"], "%Y-%m-%d") > datetime.now():
            if form["status"] == "Olvidada":
                flash("Una cita futura no puede ser olvidada", "appointments")
                is_valid = False 
        if datetime.strptime(form["date"], "%Y-%m-%d") < datetime.now():
            if form["status"] == "Pendiente":
                flash("Una cita pasada no puede ser pendiente", "appointments")
                is_valid = False 
            
        
        return is_valid
    
#guardar cita    
    @classmethod
    def save(cls,form):
        query = "INSERT INTO appointments (task, date, status,user_id) VALUES (%(task)s, %(date)s, %(status)s, %(user_id)s)"
        result = connectToMySQL("esquema_examen").query_db(query,form)
        return result

#traer todas las citas del usuario segun su id
    @classmethod
    def get_all(cls):
        query = "SELECT appointments.*, users.name FROM appointments JOIN users ON user_id = users.id"
        results = connectToMySQL("esquema_examen").query_db(query)
        appointments = []
        for appointment in results:
            appointments.append(cls(appointment))
            
        return appointments
    
#tomar una cita por su id
    @classmethod
    def get_by_id(cls, form):
        query ="SELECT appointments.*, users.name FROM appointments JOIN users ON user_id = users.id WHERE appointments.id = %(id)s"
        result= connectToMySQL("esquema_examen").query_db(query, form)
        appointment = cls(result[0])
        return appointment

#Actualizar cita
    @classmethod
    def update( cls,form):
        query = "UPDATE appointments SET task = %(task)s, date = %(date)s, status=%(status)s WHERE id=%(id)s"
        result = connectToMySQL("esquema_examen").query_db(query, form)
        return result

#Eliminar cita
    @classmethod
    def delete(cls,form):
        query = "DELETE FROM appointments WHERE id =%(id)s"
        result= connectToMySQL("esquema_examen").query_db(query, form)
        return result