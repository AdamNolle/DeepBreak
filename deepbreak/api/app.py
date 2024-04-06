from flask import Flask, request, jsonify  
import PIL
import io
from PIL import Image
import numpy as np
import base64


app = Flask(__name__)

processed_image = [{}]

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/upload', methods=['POST'])
def deepbreak():
    imageb64 = (request.get_json())['image']
    image = base64.b64decode(imageb64)
    im = Image.open(io.BytesIO(image))
    new_image = process_image(im)
    converted_string = base64.b64encode(new_image.read()) 
    returnValue = jsonify(converted_string)
    getDeepBreak(returnValue)



@app.route('/upload')
def getDeepBreak(json):
    return json

def invert_pixel_color(pixel):
    # Assuming the pixel is in RGB format
    return 255 - pixel

def process_image(image):
    """
    Takes an image represented as a 3D NumPy array (height x width x channels)
    and inverts one pixel's color out of every group of 10 pixels in each row.
    """
    # Copy the image to avoid altering the original
    processed_image = np.copy(image)
    
    height, width, _ = image.shape
    
    # Iterate over each row
    for i in range(height):
        # Iterate over each group of 10 pixels in the row
        for j in range(0, width, 10):
            # Choose which pixel to invert in this group
            pixel_to_invert = j  # For simplicity, always choose the first pixel in the group
            if pixel_to_invert < width:  # Check to avoid index error at the end of a row
                # Invert the color of the chosen pixel
                processed_image[i, pixel_to_invert] = invert_pixel_color(processed_image[i, pixel_to_invert])
    
    return processed_image
if __name__ == '__main__':
    app.run()