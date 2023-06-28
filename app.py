from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import base64

db= SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///database.db"

db.init_app(app)

class Animalito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal = db.Column(db.String)
    raza= db.Column(db.String)
    color = db.Column(db.String)
    ciudad = db.Column(db.String)
    barrio = db.Column(db.String)
    telefono = db.Column(db.String)
    descripcion = db.Column(db.String)
    image = db.Column(db.String)
    data = db.Column(db.LargeBinary)


    def __init__(self, animal, raza, color, ciudad, barrio, telefono, descripcion,image,data):
        self.animal = animal
        self.color = color
        self.raza = raza
        self.ciudad = ciudad
        self.barrio = barrio
        self.telefono = telefono 
        self.descripcion = descripcion  
        self.image = image
        self.data = data


@app.route("/")
def index():
    return render_template('homepage.html')


@app.route("/encontre_mascota",methods=(['POST','GET']))
def encontre():
    if request.method =='POST':
        animal = request.form['animal'] # traer desde el front 
        raza = request.form['raza']
        color = request.form['color']
        ciudad = request.form['ciudad']
        barrio = request.form['barrio']
        telefono = request.form['telefono']
        descripcion = request.form['descripcion']
        image = request.files['image']

        filename = secure_filename(image.filename)
        image_data = image.read()

        variable = Animalito(animal, raza, color, ciudad, barrio, telefono, descripcion,filename,image_data) # guardar en una variable los metodos de la clase animalitos

        db.session.add(variable) # preparas para mandar a la db
        db.session.commit() # mandas a la db
        return render_template("gracias.html")
    return render_template('encontre_mascota.html')

@app.route("/perdi_mascota",methods=(['POST','GET']))
def perdio():
    if request.method =='POST':
        animal = request.form['animal'] # traer desde el front 
        raza = request.form['raza']
        color = request.form['color']
        ciudad = request.form['ciudad']
        barrio = request.form['barrio']
        telefono = request.form['telefono']
        descripcion = request.form['descripcion']
        image =request.files['image']

        datos = Animalito.query.all()

        coincide = []

        for dato in datos:
            if animal == dato.animal and color == dato.color:
                dato.imagen = base64.b64encode(dato.data).decode('ascii')
                coincide.append(dato)
                print(dato.imagen)
        return render_template('lista_coincidencias.html', datos = coincide)
    return render_template('perdi_mascota.html')
    
@app.route("/descripcion/<int:id>")
def descripcion(id):
    dato = Animalito.query.get(id)
    dato.imagen = base64.b64encode(dato.data).decode('ascii')
    return render_template("descripcion.html",dato = dato)

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")


# with app.app_context():
#     db.create_all()


if __name__== "__main__":
    app.run(debug =True)