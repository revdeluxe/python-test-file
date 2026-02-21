from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import base64
import io, os

app = Flask(__name__)

# Load the pre-trained model (MobileNetV2 is lightweight and fast)
model = MobileNetV2(weights='imagenet')

@app.route('/')
def index():
    # Serve the HTML UI
    return render_template('index.html')

@app.route('/api/detect', methods=['POST'])
def detect():
    try:
        data = request.get_json()
        if 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400

        # Extract the base64 image data sent from the phone
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # Open the image and resize it to match MobileNetV2's required input (224x224)
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        image = image.resize((224, 224))
        
        # Preprocess the image into a numpy array
        img_array = img_to_array(image)
        img_array = np.expand_dims(img_array, axis=0) # Add batch dimension
        img_array = preprocess_input(img_array)
        
        # Run the TensorFlow detection
        predictions = model.predict(img_array)
        
        # Decode the top 3 predictions
        decoded_predictions = decode_predictions(predictions, top=3)[0]
        
        # Format the results into a clean dictionary
        results = [
            {'entity': pred[1].replace('_', ' ').title(), 'confidence': float(pred[2])} 
            for pred in decoded_predictions
        ]
        
        return jsonify({'success': True, 'detections': results})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Running on 0.0.0.0 allows your phone to access the server on your local network
    cert_path = 'static/certs/cert.pem'
    key_path = 'static/certs/key.pem'
    
    # Check if files exist to avoid silent errors
    if os.path.exists(cert_path) and os.path.exists(key_path):
        context = (cert_path, key_path)
        app.run(host='0.0.0.0', port=5000, ssl_context=context, debug=True)
    else:
        print("Certificates not found! Please check the static/certs/ folder.")