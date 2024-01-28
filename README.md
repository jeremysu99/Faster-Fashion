# FASTER FASHION

## OVERVIEW

Faster Fashion is a web application that leverages image recognition and a PostgreSQL database to provide users with recommendations for clothing similar to their uploaded images. The project aims to streamline the fashion discovery process by offering personalized suggestions based on user preferences and interests.

## FEATURES

- **Image Upload**: Users can upload images of clothing items they like.
  
- **Image Recognition**: Utilizing image recognition technology, the application identifies key features of the uploaded image.

- **Database Query**: The system queries a PostgreSQL database to find similar clothing items based on the identified features.

- **User Interests**: The application takes into account user preferences to deliver personalized recommendations.

- **Web Interface**: The user interacts with the application through a user-friendly web interface.

## TECHNOLOGIES USED

- **Python**

- **Flask**
  
- **Google Cloud Vision API**

- **Bootstrap**

- **PostgreSQL**

- **HTML/CSS**
  
- **Jinja**

## SETUP AND INSTALLATION

- Run `git clone https://github.com/jeremysu99/Faster-Fashion`

- Activate Python 3.12 virtual environment and install all required libraries and frameworks

- Create a Google Cloud API account and follow the instructions to setup the project

- Create a test project with the Google Cloud Vision API enabled.

- Ensure you set up a Service Account tied to this project and download the corresponding JSON key attached to that Service Account

- Run **export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credential/json"** in the VSCode terminal to give yourself access to Google Cloud Vision API

- Run main.py and access the test server for Faster Fashion!
