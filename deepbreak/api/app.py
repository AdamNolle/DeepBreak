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

# @app.route('/upload', methods=['POST'])
# def deepbreak():
#     imageb64 = (request.get_json())['image']
#     prefix = 'data:image/webp;base64,'
#     cut = imageb64[len(prefix):]
#     im = Image.open(io.BytesIO(base64.b64decode(cut)))
#     np_image = np.array(im)
#     identifyFaces(np_image)
#     new_image = process_image(np_image)
#     converted_string = base64.b64encode(new_image) 
#     returnValue = [{'image': f"{converted_string}"}]
#     return jsonify(data=returnValue, status=200, mimetype='application/json')

@app.route('/upload', methods=['POST'])
def deepbreak():
    imageb64 = (request.get_json())['image']
    imageb64 = imageb64.split(',')
    imageb64 = imageb64[1]
    print(len(imageb64))
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
    return 255 - pixel

# def identifyFaces(image):
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     face_classifier = cv2.CascadeClassifier(
#     cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
#     )
#     face = face_classifier.detectMultiScale(
#     gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
#     )
#     for (x, y, w, h) in face:
#         cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 4)
#     img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    

#     img = Image.fromarray(img_rgb, 'RGB')
#     img.save('my.png')
#     img.show()

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
            for j in range(x, x + w, 10):  # Modify to invert every pixel if desired
                # Randomly decide whether to invert pixel or not
                if random.random() < 0.05:
                    processed_image[i, j] = invert_pixel_color(processed_image[i, j])

    return processed_image

# def process_image(image):
#     """
#     Takes an image represented as a 3D NumPy array (height x width x channels)
#     and inverts one pixel's color out of every group of 10 pixels in each row.
#     """
#     # Copy the image to avoid altering the original
#     processed_image = np.copy(image)
    
#     height, width, _ = image.shape
    
#     # Iterate over each row
#     for i in range(height):
#         # Iterate over each group of 10 pixels in the row
#         for j in range(0, width, 10):
#             # Choose which pixel to invert in this group
#             pixel_to_invert = j  # For simplicity, always choose the first pixel in the group
#             if pixel_to_invert < width:  # Check to avoid index error at the end of a row
#                 # Invert the color of the chosen pixel
#                 processed_image[i, pixel_to_invert] = invert_pixel_color(processed_image[i, pixel_to_invert])
    
    return processed_image
if __name__ == '__main__':
    app.run()