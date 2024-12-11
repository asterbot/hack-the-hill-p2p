"""
TODO
"""

import os
import io
import json

from code.utils import get_filename_by_file_id, custom_encoding
from code.p2p_client import P2PClient
from code.file_tokenizer import hash_file_blocks

from pathlib import Path
from flask_cors import CORS
from flask import Flask, request, jsonify, send_file

from config import UPLOADS_FOLDER, HASH_EXTENSION, SOURCES_FOLDER, WEBSITE_DATA

app = Flask(__name__)
CORS(app)

# Ensure the upload directory exists
if not os.path.exists(UPLOADS_FOLDER):
    os.makedirs(UPLOADS_FOLDER)

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

    hash_file_blocks(file_path)

    hackthehill_file = os.path.join(SOURCES_FOLDER, Path(file_path).stem + HASH_EXTENSION)

    with open(hackthehill_file, 'r', encoding="utf-8") as f:
        file_hash = custom_encoding(f.read())

    fileData[file_hash] = {'path': file_path, 'hackthehill': hackthehill_file}

    with open(WEBSITE_DATA, "w", encoding="utf-8") as f:
        f.write(json.dumps(fileData, indent=2))

    return jsonify({"status": "File uploaded", "file_path": file_path, "data": fileData}), 200


@app.route('/receive-token', methods=['POST'])
def receive_token():
    """
    TODO
    """

    data = request.get_json()
    file_hash = data.get('final_id')

    client.request_file(file_hash)

    files = get_filename_by_file_id(file_hash)

    if files is None:
        print("Could not find the fucking file with file id " + file_hash)
        return jsonify({"error": "Can't find file hash"}), 400

    file_path = os.path.join(SOURCES_FOLDER, files[1])

    with open(file_path, 'r', encoding="utf-8") as f:
        file_with_extension = json.loads(f.read())['header']['file_name']

    with open(os.path.join(UPLOADS_FOLDER, file_with_extension), 'rb') as f:
        file_data = f.read()

    file_blob = io.BytesIO(file_data)

    if file_hash:
        return send_file(file_blob,
                         as_attachment=True,
                         download_name=file_with_extension,
                         mimetype='text/plain'), 200

    return jsonify({"error": "No ID provided"}), 400


if __name__ == '__main__':
    with P2PClient() as client:
        client.start()
        app.run(debug=False)
