from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# Route to send a string to the API
@app.route('/send-string', methods=['POST'])
def send_string():
    data = request.get_json()
    if 'input_string' not in data:
        return jsonify({"error": "No string provided"}), 400

    input_string = data['input_string']
    reversed_string = input_string[::-1]

    return jsonify({"original_string": input_string, "reversed_string": reversed_string}), 200

if __name__ == '__main__':
    app.run(debug=True)
