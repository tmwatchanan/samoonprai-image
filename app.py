#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request
import herb_classification.controllers

# Initialize the Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), "api_images")
os.makedirs(os.path.dirname(app.config['UPLOAD_FOLDER']), exist_ok=True)  # Create directory if does not exist


@app.route('/classify/image', methods=['POST'])
def classify_image():
    return herb_classification.controllers.predict_herb_image(request)


@app.route('/classify/url', methods=['POST'])
def classify_url_image():
    return herb_classification.controllers.predict_herb_image_url(request)


# start flask app
app.run(host="127.0.0.1", port=5001, debug=True)
