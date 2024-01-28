# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_session import Session
import subprocess
import os
from io import BytesIO
from PIL import Image
import base64
from helpers import detect_objects_and_dominant_colors_from_bytes, get_similar_clothes
import time
from random import randint

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
        
        messages = [
            'Looking for clothes...',
            'Rummaging through our wardrobe...',
            'Searching our closet...',
            'Definitely not webscraping...',
            'Finding you heat...'           
        ]
        
        random_element = randint(0,4)
        
        file = request.files['file']

        # Read the uploaded image data directly from the BytesIO stream
        uploaded_image_data = file.read()

        # Save the image data to the session
        session['uploaded_image'] = uploaded_image_data
        session['gender'] = request.form['clothingOption']
        
        # Redirect to the result page with the data as query parameters
        return render_template('loading.html', loading_message=messages[random_element])

    except Exception as e:
        print('Error:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500
    
@app.route('/perform_switch')
def perform_switch():
    # Simulate some time-consuming operation
    time.sleep(2)

    # Redirect to another page
    return redirect(url_for('result_page'))

@app.route('/result', methods=['GET', 'POST'])
def result_page():
    # Retrieve the image data from the session
    uploaded_image_data = session.get('uploaded_image', None)
    gender_clothing = session.get('gender', 'Both')
    
    if uploaded_image_data is None:
        # Handle the case where there is no image data
        return "No image data found in session"
    
    uploaded_image_data_string = base64.b64encode(uploaded_image_data).decode('utf-8')
    uploaded_image_color_data = detect_objects_and_dominant_colors_from_bytes(uploaded_image_data)
    
    
    if gender_clothing == 'Male':
        gender = "Men's"
    elif gender_clothing == 'Female':
        gender = "Women's"
    elif gender_clothing == 'Other':
        gender = "Men and Women's"
    
    similar_clothes = get_similar_clothes(uploaded_image_data, gender_clothing)
    #print(uploaded_image_color_data)
    return render_template('result.html', uploaded_image_data=uploaded_image_data_string, uploaded_image_color_data=uploaded_image_color_data, gender=gender, similar_clothes=similar_clothes)

if __name__ == '__main__':
    app.run(debug=True)
