"""
Morse Code Analyzer - Flask Web Application
"""

import os
import base64
from flask import Flask, render_template, request, jsonify, send_file
from morse_engine import text_to_morse, morse_to_text, analyze_morse, get_morse_tree, get_full_table
from image_processor import process_image, generate_morse_image
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/encode', methods=['POST'])
def encode():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    morse = text_to_morse(text)
    return jsonify({'text': text, 'morse': morse})


@app.route('/api/decode', methods=['POST'])
def decode():
    data = request.get_json()
    morse = data.get('morse', '')
    if not morse:
        return jsonify({'error': 'No Morse code provided'}), 400
    text = morse_to_text(morse)
    return jsonify({'morse': morse, 'text': text})


@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    morse = data.get('morse', '')
    if not morse:
        return jsonify({'error': 'No Morse code provided'}), 400
    result = analyze_morse(morse)
    return jsonify(result)


@app.route('/api/table', methods=['GET'])
def table():
    return jsonify(get_full_table())


@app.route('/api/tree', methods=['GET'])
def tree():
    return jsonify(get_morse_tree())


@app.route('/api/process-image', methods=['POST'])
def process_img():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    file_bytes = file.read()
    result = process_image(file_bytes)
    return jsonify(result)


@app.route('/api/generate-image', methods=['POST'])
def generate_img():
    data = request.get_json()
    morse = data.get('morse', '')
    if not morse:
        return jsonify({'error': 'No Morse code provided'}), 400

    img_bytes = generate_morse_image(morse)
    img_b64 = base64.b64encode(img_bytes).decode('utf-8')
    return jsonify({'image': f'data:image/png;base64,{img_b64}'})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
