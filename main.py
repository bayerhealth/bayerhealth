import os
import os.path
import random
import sys
import json
import string
from flask import Flask, flash, render_template, redirect, request, url_for, jsonify, session, Response
from utils import handle_video
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'static/plants'
ALLOWED_EXTENSIONS = {'jpg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



app = Flask(__name__)
app.secret_key = 'trzyq'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def main():
    return redirect(url_for('index'))


@app.route('/index', methods=["GET", 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == 'POST':
        # check if the post request has the file part
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
            handle_video(rand_id)
            return redirect(url_for('index'))

@app.route('/map')
def plant_map():
    return render_template('map.html')

@app.route('/stats')
def statistics():
    return render_template('stats.html')


if __name__ == '__main__':
    app.run(debug=True)
