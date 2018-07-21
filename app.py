#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import label_image
import subprocess

# Initialize the Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), "api_images")

os.makedirs(os.path.dirname(app.config['UPLOAD_FOLDER']), exist_ok=True)  # Create directory if does not exist
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Disable all debugging logs
label_image.tf.logging.set_verbosity(label_image.tf.logging.WARN)


@app.route('/classify', methods=['POST'])
def image():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_full_path))
    output_graph_file = os.path.join(os.getcwd(), "output_graph.pb")
    output_labels_file  = os.path.join(os.getcwd(), "output_labels.txt")
    classification_output = classify_herb_image(file_full_path, output_graph_file, output_labels_file)
    return jsonify({'results': classification_output})


def classify_herb_image(file_name, model_file, label_file, input_layer='Placeholder', output_layer='final_result'):
    print("Classifying", file_name)
    input_height = 299
    input_width = 299
    input_mean = 0
    input_std = 255

    # if args.input_height:
    #     input_height = args.input_height
    # if args.input_width:
    #     input_width = args.input_width
    # if args.input_mean:
    #     input_mean = args.input_mean
    # if args.input_std:
    #     input_std = args.input_std
    # if args.input_layer:
    #     input_layer = args.input_layer
    # if args.output_layer:
    #     output_layer = args.output_layer

    graph = label_image.load_graph(model_file)
    t = label_image.read_tensor_from_image_file(
        file_name,
        input_height=input_height,
        input_width=input_width,
        input_mean=input_mean,
        input_std=input_std)

    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name)

    with label_image.tf.Session(graph=graph) as sess:
        results = sess.run(output_operation.outputs[0], {
            input_operation.outputs[0]: t
        })
    results = label_image.np.squeeze(results)

    top_k = results.argsort()[-5:][::-1]
    labels = label_image.load_labels(label_file)
    classification_output = []
    for i in top_k:
        out = {
            'label': labels[i],
            'score': results[i].item()
        }
        classification_output.append(out)
        # print(labels[i], results[i])
    print(classification_output)
    return (classification_output)

# start flask app
app.run(host="127.0.0.1", port=5000, debug=True)
