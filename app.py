from __future__ import division, print_function
# coding=utf-8
import cv2
import pytesseract
import os
from PIL import Image, ImageFilter, ImageFile
import re
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Defining a flask app
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


def img2date(path):
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    highestchar = 0
    for i in range(7, 18, 2):
        for j in range(6, 12, 1):
            img = cv2.imread(path, 0)
            img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, i, j)
            extractedInformation = pytesseract.image_to_string(img)
            if highestchar <= len(extractedInformation):
                highestchar = len(extractedInformation)

                a = i
                b = j
            else:
                continue
    date_re = re.compile(
        r"(\d{1,2}((/|-|\.)|\s)[a-zA-Z]{3}((/|-|\.)|\s)\d{2,4})|([a-zA-Z]{3}(')?\s?\d{2}((,|-|\.|,)|\s)\d{2,4})|(\d{1,2}(/|-|\.)\d{2}(/|-|\.)\d{2,4})")
    img = cv2.imread(path, 0)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, a, b)
    extractedInformation = pytesseract.image_to_string(img)
    # print(extractedInformation)
    date = date_re.search(extractedInformation)
    return date

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        date = img2date(file_path)

        # Processing date
        return date
    return None


if __name__ == '__main__':
    app.run(debug=True)


