# Wardiyyah Project

Wardiyyah is a smart web application powered by AI to identify different types of flowers based on user-uploaded images. The platform aims to simplify flower recognition using a trained deep learning model and provide users with clear descriptions and information in Arabic.

----
https://wardiyyah.onrender.com/
----


## Features

- Upload an image of a flower to get its predicted name and description.
- Confidence levels are displayed to indicate the accuracy of the prediction.
- Supports both Arabic and English for flower names and descriptions.
- Friendly user interface, responsive across devices


## Full Stack Breakdown

Front-End:
--HTML, CSS, JavaScript
--Responsive design

Back-End:
--Flask, Flask-CORS
--TensorFlow, Keras, NumPy

## AI Model

--Base Model: MobileNetV2 (pretrained on ImageNet)
--Training Dataset: Oxford 102 Flowers
--Trained with: TensorFlow & Keras
--Saved Model: flower_model.h5
--Augmentation: Rotation, zoom, brightness, flips, etc.


## Project Structure

wardiyyah/
│
├── static/
│   └── style.css      # Front-end styling
│   └── script.js      # Front-end interaction logic
│   └── assets/        # web assets
│
├── templates/
│   └── index.html      # Main page
│
├── flower_model.h5          # Trained model
├── flower_info.json         # Flower names, descriptions, and care info
├── flower_class_labels.txt  # Class ID mapping
├── app.py                   # Flask backend server
├── requirements.txt         # Python dependencies


## How to Run Locally

1.Clone the repo:
git clone https://github.com/GhaidaAL36/Wardiyyah.git
cd Wardiyyah
نس
تحر
2. Create a virtual environment:
python -m venv venv
.venv\Scripts\activate

3.Install dependencies
pip install -r requirements.txt

4.Run the app:
python app.py

5.Open http://127.0.0.1:5000 in your browser


## Notes

- The model was trained on a limited dataset and may not recognize unfamiliar or poor-quality images.
- The dataset is large, so it's not included directly in GitHub
