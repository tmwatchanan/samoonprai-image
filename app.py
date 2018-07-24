#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request
from herb_classification.controllers import predict_herb_image

# Initialize the Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), "api_images")
os.makedirs(os.path.dirname(app.config['UPLOAD_FOLDER']), exist_ok=True)  # Create directory if does not exist


@app.route('/classify', methods=['POST'])
def image():
    return predict_herb_image(request)


# start flask app
app.run(host="127.0.0.1", port=5000, debug=True)
