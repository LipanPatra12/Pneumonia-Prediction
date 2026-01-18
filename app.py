from flask import Flask, request, render_template
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

app = Flask(__name__)

# Load your trained CNN model
model = load_model('cnn_model.h5')  # Make sure this file is in the same folder as app.py

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file uploaded", 400

    img_file = request.files['file']
    if img_file.filename == '':
        return "No selected file", 400

    # Create uploads folder if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    filepath = os.path.join("uploads", img_file.filename)
    img_file.save(filepath)

    # Resize uploaded image to match model input (224x224)
    img = image.load_img(filepath, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize like during training

    # Make prediction
    prediction = model.predict(img_array)

    # Convert prediction to class (adjust if multi-class)
    result = "normal" if prediction[0][0] > 0.5 else "pneumonia"

    # Remove temporary uploaded file
    os.remove(filepath)

    return render_template('home.html', prediction=result)

if __name__ == "__main__":
    app.run(debug=True)

