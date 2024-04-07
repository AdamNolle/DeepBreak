import random
from flask import Flask, request, jsonify  
import PIL
import io
from PIL import Image
import numpy as np
import base64
import cv2
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

processed_image = [{}]

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/upload', methods=['POST'])
def deepbreak():
    imageb64 = (request.get_json())['image']
    imageb64 = imageb64.split(',')
    imageb64 = imageb64[1]
    im = Image.open(io.BytesIO(base64.b64decode(imageb64)))
    np_image = np.array(im)
    detected_faces = identifyFaces(np_image)
    new_image = process_image(np_image, detected_faces)
    new_image_pil = Image.fromarray(new_image)
    buffered = io.BytesIO()
    new_image_pil.save(buffered, format="PNG")
    converted_string = base64.b64encode(buffered.getvalue())
    returnValue = [{'image': f"{converted_string.decode()}"}]
    return jsonify(data=returnValue, status=200, mimetype='application/json')

def invert_pixel_color(pixel):
    # Assuming the pixel is in RGB format
    return  50 - pixel

def identifyFaces(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = face_classifier.detectMultiScale(
    gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
    )
    return faces

def process_image(image, faces):
    """
    Inverts the color of pixels inside detected face regions with a 5% chance.
    """
    processed_image = np.copy(image)

    for (x, y, w, h) in faces:
        for i in range(y, y + h):
            for j in range(x, x + w):  # Modify to invert every pixel if desired
                # Randomly decide whether to invert pixel or not
                if random.random() < 0.0005:  
                    processed_image[i, j] = invert_pixel_color(processed_image[i, j])
        face_region = processed_image[y:y+h, x:x+w]
        
        #Was messing with blurring images. Makes the generated images work better so stopped this. 
        # Generate uniform noise with reduced intensity
        # noise = np.random.randint(-10, 10, size=face_region.shape, dtype=np.int8)  # Uniform noise
        # noisy_face_region = np.clip(face_region + noise, 0, 255)  # Ensure pixel values are within [0, 255] range
        
        # # Apply blurring to reduce noise
        # blurred_face_region = cv2.GaussianBlur(noisy_face_region, (5, 5), 0)  # Gaussian blur with a 5x5 kernel size
        
        # # Update the processed image with the blurred face region
        # processed_image[y:y+h, x:x+w] = blurred_face_region
    return processed_image

if __name__ == '__main__':
    app.run()