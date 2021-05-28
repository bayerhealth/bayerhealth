import os
import os.path
import random
import hashlib
import sys
import json
import string
from flask import Flask, flash, render_template, redirect, request, url_for, jsonify, session, Response

from werkzeug.utils import secure_filename
from utils import handle_video, load_data
from db import getVideos


UPLOAD_FOLDER = 'static/vid'
ALLOWED_EXTENSIONS = {'mp4'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



app = Flask(__name__)
app.secret_key = '9je0jaj09jk9dkakdwjnjq'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def main():
    if 'username' in session:
        return redirect(url_for('upload'))
    else:
        return redirect(url_for('viewall'))


@app.route('/upload', methods=["GET", 'POST'])
def upload():
    if request.method == "GET":
        if 'username' in session:
            return render_template('upload.html', username=session.get('username'))
        else:
            return redirect(url_for('login'))
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
            filename = secure_filename(rand_id + '.mp4')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            handle_video(rand_id)
            return redirect(url_for('viewall'))


if __name__ == '__main__':
    app.run(debug=True)
