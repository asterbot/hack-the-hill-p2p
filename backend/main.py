import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)

# Define the folder to save uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/receive-file', methods=['POST'])
def receive_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the file to the upload folder (we will need to tokenize this later)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    return jsonify({"status": "File uploaded", "file_path": file_path}), 200

@app.route('/receive-token', methods=['POST'])
def receive_token():
    data = request.get_json()   
    file_hash = data.get('final_id')
    
    # TODO
    # process file_hash here
    # and store result in file_path
    
    file_path = "sample.hackthehill" # NOTE: placeholder
    
    
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    file_blob = io.BytesIO(file_data)
    
    
    if file_hash:
        return send_file(file_blob, as_attachment=True, download_name='example.txt', mimetype='text/plain'), 200
    else:
        return jsonify({"error": "No ID provided"}), 400


if __name__ == '__main__':
    app.run(debug=True)
