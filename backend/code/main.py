"""
TODO
"""

import os
import io
import json

from code.utils import get_filename_by_file_id, custom_hash
from code.p2p_client import P2PClient
from code.file_tokenizer import SenderTokenizer

from pathlib import Path
from flask_cors import CORS
from flask import Flask, request, jsonify, send_file


app = Flask(__name__)
CORS(app)

# Define the folder to save uploaded files
# TODO: Modify UPLOAD_FOLDER to the path you wanna save the received file in locally
UPLOAD_FOLDER = 'uploads'                       # NOTE: This is a placeholder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

fileData = {}


@app.route('/receive-file', methods=['POST'])
def receive_file():
    """
    TODO
    """

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the file to the upload folder (we will need to tokenize this later)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    tokenized_file = SenderTokenizer(file_path)
    tokenized_file.hash_file_blocks()

    with open("./sources/" + Path(file_path).stem + ".hackthehill", 'r', encoding="utf-8") as f:
        file_hash = custom_hash(f.read())

    fileData[file_hash] = {'path': file_path, 'hackthehill': "./sources/" +
                           Path(file_path).stem + ".hackthehill"}
    # print(fileData)

    with open("website_data.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(fileData, indent=2))

    return jsonify({"status": "File uploaded", "file_path": file_path, "data": fileData}), 200


@app.route('/receive-token', methods=['POST'])
def receive_token():
    """
    TODO
    """

    data = request.get_json()
    file_hash = data.get('final_id')

    # TODO process file_hash here and store result in file_path

    client.request_file_fingerprint(file_hash)

    files = get_filename_by_file_id(file_hash)

    if files is None:
        print("Could not find the fucking file with file id " + file_hash)
        return jsonify({"error": "Can't find file hash"}), 400

    file_path = os.path.join('sources', files[1])
    # file_path='file.txt'

    with open(file_path, 'r', encoding="utf-8") as f:
        file_with_extension = json.loads(f.read())['header']['file_name']

    with open(os.path.join('uploads', file_with_extension), 'rb') as f:
        file_data = f.read()

    file_blob = io.BytesIO(file_data)

    if file_hash:
        return send_file(file_blob,
                         as_attachment=True,
                         download_name=file_with_extension,
                         mimetype='text/plain'), 200

    return jsonify({"error": "No ID provided"}), 400


if __name__ == '__main__':
    client = P2PClient()
    client.start()
    app.run(debug=False)
