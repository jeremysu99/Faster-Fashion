# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_session import Session
import subprocess
import os
from io import BytesIO
from PIL import Image
import base64
from helpers import detect_objects_and_dominant_colors_from_bytes, detect_objects_and_dominant_colors_from_url

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def upload_page():
    return render_template('upload.html')

@app.route('/process_image', methods=['GET', 'POST'])
def process_image():
    try:
        file = request.files['file']

        # Read the uploaded image data directly from the BytesIO stream
        uploaded_image_data = file.read()

        # Save the image data to the session
        session['uploaded_image'] = uploaded_image_data

        # Run the api.py script with the image data as a command-line argument
        #command = ['python', 'api.py', '--image_data', base64.b64encode(uploaded_image_data).decode('utf-8')]
        #subprocess.run(command)

        # Assume some data is returned by the processing
        processed_image_urls = [
            'processed_image_url_1.jpg',
            'processed_image_url_2.jpg',
            'processed_image_url_3.jpg'
        ]

        # Redirect to the result page with the data as query parameters
        return redirect(url_for('result_page'))

    except Exception as e:
        print('Error:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/result', methods=['GET', 'POST'])
def result_page():
    # Retrieve the image data from the session
    uploaded_image_data = session.get('uploaded_image', None)

    if uploaded_image_data is None:
        # Handle the case where there is no image data
        return "No image data found in session"

    # Process the image data as needed

    # Pass the image data to the result template
    #data = {
    #    'original_image_data': uploaded_image_data,
    #    'processed_image_urls': process_image(uploaded_image_data)  # Replace with your actual image processing logic
    #}
    
    uploaded_image_data_string = base64.b64encode(uploaded_image_data).decode('utf-8')
    uploaded_image_color_data = detect_objects_and_dominant_colors_from_bytes(uploaded_image_data)
    print(uploaded_image_color_data)
    
    return render_template('result.html', uploaded_image_data=uploaded_image_data_string)

if __name__ == '__main__':
    app.run(debug=True)
