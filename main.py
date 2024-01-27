# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def upload_page():
    return render_template('upload.html')

@app.route('/loading')
def loading_page():
    return render_template('loading.html')

@app.route('/result')
def result_page():
    # Retrieve data from query parameters or other sources
    data = {
        'original_image_url': request.args.get('original_image_url'),
        'processed_image_urls': request.args.getlist('processed_image_urls')
    }
    return render_template('result.html', **data)

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        file = request.files['file']

        # Save the original file temporarily
        original_file_path = 'original_image.jpg'
        file.save(original_file_path)

        # Run the api.py script with the file path as a command-line argument
        command = ['python', 'api.py', original_file_path]
        subprocess.run(command)

        # Assume some data is returned by the processing
        processed_image_urls = [
            'processed_image_url_1.jpg',
            'processed_image_url_2.jpg',
            'processed_image_url_3.jpg'
        ]

        # Redirect to the result page with the data as query parameters
        return redirect(url_for('result_page', original_image_url=original_file_path, processed_image_urls=processed_image_urls))

    except Exception as e:
        print('Error:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
