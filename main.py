import os
import io
import numpy as np
import tensorflow as tf
import joblib
import cv2

from PIL import Image
from tensorflow import keras
from flask import Flask, request, jsonify
from tensorflow.keras.utils import load_img, img_to_array
from tensorflow.keras.applications.efficientnet import preprocess_input

#Load model
# model_name = 'specific_PH_model.h5'
model_name = 'specific_PH_mobilenet_v2_model.h5'

model = keras.models.load_model(model_name)

# model_name = './random_forest.joblib'

# model = joblib.load(model_name)

IMG_SIZE = (224, 224)
#Preprocess
def resize_and_preprocess(img):
    img = tf.image.resize(img, IMG_SIZE)
    # feature scaling
    img = preprocess_input(img)
    return img

def ml_preprocess(flatten_img):
    return flatten_img / 255.0

#Predict
def predict(batch_img):
    pred = model.predict(batch_img)
    return pred

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
# For Deep Learning

def index():
    if request.method == "POST":
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({"error":"no file"})
        try:
            image_bytes = file.read()
            pillow_img = Image.open(io.BytesIO(image_bytes))
            img = img_to_array(pillow_img)
            img = resize_and_preprocess(img) # batchsize = 10 -> 10 * 100 images
            batch_img = tf.expand_dims(img, axis=0) # (1, 224, 224, 3)
            pred = predict(batch_img)
            data = {"Prediction (pH)": float(pred)}
            return jsonify(data)
        except Exception as e:
            print(img)
            return jsonify({"error": str(e)})
    return "OK"


#For Machine Learning

# def index():
#     if request.method == "POST":
#         file = request.files.get('file')
#         if file is None or file.filename == "":
#             return jsonify({"error":"no file"})
#         try:
#             image_bytes = file.read()
#             pillow_img = Image.open(io.BytesIO(image_bytes))
#             img = img_to_array(pillow_img)
#             img = cv2.resize(img,IMG_SIZE)
#             img = img.flatten()
#             img = ml_preprocess(img)
#             batch_img = tf.expand_dims(img, axis=0) # (1, 224, 224, 3)
#             pred = predict(batch_img)
#             data = {"Prediction (pH)": float(pred)}
#             return jsonify(data)
#         except Exception as e:
#             print(img)
#             return jsonify({"error": str(e)})
#     return "OK"

if __name__ == "__main__":
    app.run(debug=True)