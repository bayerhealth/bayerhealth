import os
import os.path
import random
import re
import sys
import json
import string
from datetime import datetime
from flask import Flask, flash, render_template, redirect, request, url_for, jsonify, session, Response
from flask_sqlalchemy import SQLAlchemy
from utils import handle_img
from werkzeug.utils import secure_filename

# -----------^IMPORTS^---------------


UPLOAD_FOLDER = 'static/plants'
ALLOWED_EXTENSIONS = {'jpg'}

app = Flask(__name__)
app.secret_key = 'trzyq'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


# -------------^CONFIGS^-------------

db = SQLAlchemy(app)

class Plant(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    DateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Latitude = db.Column(db.Float, nullable=False)
    Longitude = db.Column(db.Float, nullable=False)
    ImageFile = db.Column(db.String(20), nullable=False)
    PlantType = db.Column(db.String(20))
    Health = db.Column(db.String(20))
    AuthorEMail = db.Column(db.String(150))

    def __repr__(self):
        return f"Plant('{self.DateTime}', '{self.Latitude}', '{self.Longitude}', '{self.ImageFile}', '{self.PlantType}', '{self.Health}','{self.AuthorEMail}')"

# -----------------^DATABASE^-----------------------

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
def upload_plant(ImageFile, Latitude, Longitude, PlantType, Health, AuthorEMail):
    entry = Plant(ImageFile=ImageFile, Latitude=Latitude, Longitude=Longitude, PlantType=PlantType.lower(), Health=Health.lower(), AuthorEMail=AuthorEMail)
    print(entry)
    db.session.add(entry)
    db.session.commit()
    id = entry.Id
    return id

def get_plant_types(plant_types):
    if plant_types:
        plant_types = [x.lower() for x in plant_types]
        plants = Plant.query.filter(Plant.PlantType.in_(plant_types)).all()
    else:
        plants = Plant.query.all()
    parsed = []
    for plant in plants:
        pl_data = {'id': plant.Id, 'lat': plant.Latitude, 'lng': plant.Longitude, 'health': plant.Health}
        parsed.append(pl_data)
    return parsed

# ------------------^FUNCTIONS^------------------------------

@app.route('/')
def main():
    session["email"] = "admin@hadamard.pl"
    session["model"] = "World"
    return redirect(url_for('index'))


@app.route('/index')
def index():
    return render_template('index.html')
    

@app.route('/process', methods=["GET", "POST"])
def process():
    if request.method == "GET":
        return redirect(url_for('index'))
    elif request.method == 'POST':
        # check if the post request has the file part
        print(request.form)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            rand_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            filename = secure_filename(rand_id + '.jpg')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pred = handle_img(rand_id, session["model"])
            id = upload_plant(filename, float(request.form['lat']), float(request.form['lng']), pred[0], pred[1], session["email"])
            return redirect(f'/results/{id}')

@app.route('/map', methods=["GET", "POST"])
def plant_map():
    if request.method == "GET":
        return render_template('map.html', plants=get_plant_types(None))
    elif request.method == "POST":
        print(request.form)
        plant_types = request.form['plants'].split()
        plants = get_plant_types(plant_types)
        return render_template('map.html', plants=plants, searched=request.form['plants'].split())

@app.route('/stats')
def statistics():
    return render_template('stats.html')



@app.route('/settings', methods=["GET", "POST"])
def settings():
    if request.method == "GET":
        return render_template('settings.html', email=session["email"], model=session["model"])
    elif request.method == 'POST':
        session.permanent = True
        session["model"] = request.form["model"]
        session["email"] = request.form["email"]
        return render_template('settings.html', email=session["email"], model=session["model"])

@app.route("/results/<id>")
def results(id):
    plant = Plant.query.get(id)
    return render_template("results.html",
        type=plant.PlantType,
        health=plant.Health,
        date=plant.DateTime.date(), 
        lat=plant.Latitude, 
        lng=plant.Longitude, 
        plant_img=url_for('static', filename=os.path.join('plants', plant.ImageFile)
        ))

# -------^ROUTES^-------

if __name__ == '__main__':
    app.run(debug=True)
