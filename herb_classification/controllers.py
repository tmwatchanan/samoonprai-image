import os
from flask import current_app, jsonify
from werkzeug.utils import secure_filename
from herb_classification import label_image


def predict_herb_image(request):
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file_full_path))
    classification_output = label_image.classify_herb_image(file_full_path)
    return jsonify({'results': classification_output})