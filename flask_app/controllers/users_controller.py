from flask import Flask,render_template, redirect, request, session, flash
from flask_app import app

#importamos los modelos/clases
from flask_app.models.users import User
from flask_app.models.appointments import Appointment

#importacion bcrypt,  nos ayuda a encriptar la contraseñña
from flask_bcrypt import Bcrypt
Bcrypt = Bcrypt(app)


from datetime import datetime

@app.route("/")
def  index():
    return render_template("index.html")

@app.route("/register",methods=["POST"])
def register():
    #recibimos request.form , el diccionario que ingreso del formmulario de registro
    #validar info
    if not User.validate_user(request.form):
        #no es valida, rediccionaremos al formulario
        return redirect("/")
    
    #encripatamos la contraseña
    pass_encrypt = Bcrypt.generate_password_hash(request.form["password"])
    #generar un diccionaario con toda la info fel formulario
    form = {
        "name": request.form["name"],
        "email": request.form["email"],
        "password": pass_encrypt
    }
    id = User.save(form) #recibo a cambio el id del nuevo usuario
    session["user_id"]= id #guardamos en sesion el identificador de usuario
    return redirect("/dashboard")

@app.route("/login", methods=["POST"])
def login():
    #verificamos que email este en base de dtos
    user= User.get_by_email(request.form) #recibo falso u objeto de usuario
    if not user: #si usuario no existe
        flash("E-mail no registrado", "login")
        return redirect("/")
    
    #si user es instancia, existe
    #password guardado viene encriptado por lo que se ocupa otra funcion de bcrypt para comparar la contraseña con la de la bd
    if not Bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Password incorrecto", "login")
        return redirect("/")
    
    session["user_id"]=user.id #guardo en mi sesion el id del usuario
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    #PENDIENTE:VERIFICAR SI EL USUARIO INICIO SESION
    if "user_id" not in session:
        flash("Favor iniciar sesion", "not_in_session")
        return  redirect("/")
    #crear una instancia deñ usuario. Id en sesion (session["user_id"])
    #funcion que en base del id instancia ususario
    form = {"id": session["user_id"]}
    user= User.get_by_id(form)
    
    #lista citas
    appointments= Appointment.get_all()
    
    return render_template("dashboard.html", user= user, appointments=appointments, now=datetime.now)