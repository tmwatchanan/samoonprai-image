#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

# Initialize the Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), "api_images")

os.makedirs(os.path.dirname(app.config['UPLOAD_FOLDER']), exist_ok=True) # Create directory if does not exist


@app.route('/image', methods=['POST'])
def image():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify({'message': "OK"})


# start flask app
app.run(host="127.0.0.1", port=5000, debug=True)
