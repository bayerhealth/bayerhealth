import os
import os.path
import random
import sys
import json
import string
from flask import Flask, flash, render_template, redirect, request, url_for, jsonify, session, Response


app = Flask(__name__)
app.secret_key = 'trzyq'

@app.route('/')
def main():
    return redirect(url_for('index'))


@app.route('/index', methods=["GET", 'POST'])
def upload():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
