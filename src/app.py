import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, current_app
from werkzeug.datastructures import FileStorage


# Flask Configuration.
app = Flask(__name__)
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'mysecret'

# Generate random vigenere encrypt table for handling full vigenere.

"""
--------------------------------------------------------------
# Default Route
--------------------------------------------------------------
"""
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
		return redirect(url_for('vigenere'))


"""
--------------------------------------------------------------
# Route for Home (Temporary)
--------------------------------------------------------------
"""
# Index route.
@app.route('/')
def home():
	return "<h1>Hello world</h1>"

"""
--------------------------------------------------------------
# Flask Main Program
--------------------------------------------------------------
"""
if __name__ == '__main__':
	app.run(debug=True,threaded=True)

