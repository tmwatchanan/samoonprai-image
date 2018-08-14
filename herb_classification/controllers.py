import os
from flask import current_app, jsonify
from werkzeug.utils import secure_filename
from herb_classification import label_image
import requests
import urllib
from io import open as iopen
from urllib.parse import unquote
import pathlib
import uuid
import json

image_type_list = ['jpg', 'jpeg', 'gif', 'png']
SAVE_IMAGE_FROM_MSG_DIRECTORY = os.path.join(os.getcwd(), 'msg_images')
pathlib.Path(SAVE_IMAGE_FROM_MSG_DIRECTORY).mkdir(parents=True, exist_ok=True)


def predict_herb_image(request):
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file_full_path))
    classification_output = label_image.classify_herb_image(file_full_path)
    return jsonify({'results': classification_output})


def predict_herb_image_url(request):
    request_json = request.get_json()
    image_url = request_json['url']
    image_file_path = download_image(image_url)
    classification_output = label_image.classify_herb_image(image_file_path)
    return jsonify({'results': classification_output})


def download_image(file_url):
    file_url = unquote(file_url)
    try:
        i = requests.get(file_url, timeout=20)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
        # return 'Server taking too long. Try again later'
        return '',''
    else:
        file_name_from_web = urllib.parse.urlsplit(file_url)[2].split('/')[-1]
        image_type = i.headers['Content-Type'].split('/')[1]  # file_name.split('.')[1]
        image_extension = "." + ("jpg" if image_type == "jpeg" else image_type)
        image_file_name = str(uuid.uuid4().hex) + image_extension
        image_file_path = os.path.join(SAVE_IMAGE_FROM_MSG_DIRECTORY, image_file_name)
        # print(file_name, image_type)
        if image_type in image_type_list and i.status_code == requests.codes.ok:
            with iopen(image_file_path, 'wb') as file:
                file.write(i.content)
                return image_file_path
        else:
            return '', ''
