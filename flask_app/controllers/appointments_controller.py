from flask import Flask,render_template, redirect, request, session, flash
from flask_app import app

#importamos los modelos/clases
from flask_app.models.users import User
from flask_app.models.appointments import Appointment

from datetime import datetime


@app.route("/new/appointment")
def new_grade():
    #verificar inicio se sesion
    if "user_id" not in session:
        flash("Favor iniciar sesion", "not_in_session")
        return  redirect("/")
    
    return render_template("new.html")

@app.route("/create/appointment", methods=["POST"])
def create_appointment():
    #verificar inicio se sesion
    if "user_id" not in session:
        flash("Favor iniciar sesion", "not_in_session")
        return  redirect("/")
    
    #validar cita
    if not Appointment.validate_task(request.form):
        return redirect("/new/appointment")
    
    #Guardar cita 
    Appointment.save(request.form)
    
    return redirect("/dashboard")

@app.route("/edit/appointment/<int:id>")
def edit_appointment(id):
    #verificar inicio se sesion
    if "user_id" not in session:
        flash("Favor iniciar sesion", "not_in_session")
        return  redirect("/")
    
    #buscar la isntancia de grade que corresponde al id
    diccionario = {"id":id}
    appointment = Appointment.get_by_id(diccionario)
    
    return render_template("edit.html", appointment=appointment)

@app.route("/update/appointment", methods=["POST"])
def update_appointment():
    #verificar inicio se sesion
    if "user_id" not in session:
        flash("Favor iniciar sesion", "not_in_session")
        return  redirect("/")
    #Validar formulario correcto
    if not Appointment.validate_task(request.form):
        return redirect("/edit/appointment/"+request.form["id"])
    
    #actualizar registro
    Appointment.update(request.form)
    return redirect("/dashboard")

@app.route("/delete/appointment/<int:id>")
def delete_appointment(id):
    #verificar inicio se sesion
    if "user_id" not in session:
        flash("Favor iniciar sesion", "not_in_session")
        return  redirect("/")
    #Borrar
    form ={"id":id}
    Appointment.delete(form)
    
    return redirect("/dashboard")