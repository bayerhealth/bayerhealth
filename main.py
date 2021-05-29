import os
import os.path
import random
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
    ImageFile = db.Column(db.String(20), nullable=False)
    PlantType = db.Column(db.String(20))
    Health = db.Column(db.String(20))
    AuthorEMail = db.Column(db.String(150))

    def __repr__(self):
        return f"Plant('{self.DateTime}', '{self.ImageFile}', '{self.PlantType}', '{self.Health}')"

# -----------------^DATABASE^-----------------------

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
def upload_plant(ImageFile, PlantType, Health, AuthorEMail):
    entry = Plant(ImageFile=ImageFile, PlantType=PlantType, Health=Health, AuthorEMail=AuthorEMail)
    print(entry)
    db.session.add(entry)
    db.session.commit()

# ------------------^FUNCTIONS^------------------------------

@app.route('/')
def main():
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
            handle_img(rand_id)
            return render_template('results.html', 
                plant_img=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            )

@app.route('/map')
def plant_map():
    return render_template('map.html')

@app.route('/stats')
def statistics():
    return render_template('stats.html')

# -------^ROUTES^-------

if __name__ == '__main__':
    app.run(debug=True)
