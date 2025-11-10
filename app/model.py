from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input
import cv2
import numpy as np
import os
from app.download_model import download_model

# Ensure model is present
download_model()

MODEL_PATH = "model.keras"
model = load_model(MODEL_PATH)

CLASS_NAMES = ['Benign', 'Malignant']

def predict_image(img_path):
    X=[]
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    X.append(img)
    X=np.array(X)
    X_test=preprocess_input(X)
    X_test /= 255.0
    Y_pred = model.predict(X_test)
    confidence = Y_pred[0][0]
    Y_pred = np.round(Y_pred).astype(int)
    pred_class = Y_pred[0][0]
    if pred_class==0:
        confidence = 1 - confidence
    return CLASS_NAMES[pred_class], float(confidence)
