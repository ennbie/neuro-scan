from tensorflow.keras.applications.vgg16 import preprocess_input
import cv2
import numpy as np
import os
from download_model import download_model

# Ensure model is present
download_model()

MODEL_PATH = "model.keras"
model = load_model(MODEL_PATH)

CLASS_NAMES = ['Benign', 'Malignant']

def predict_image(img_path):
    X=[]
    img = cv2.imread(img_file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = img/255
    X.append(img)
    X=np.array(X)
    X_test=preprocess_input(X)
    Y_pred = model.predict(X_test)
    confidence = Y_pred[0]
    Y_pred = np.round(Y_pred).astype(int)
    pred_class = Y_pred[0]
    return CLASS_NAMES[pred_class], confidence


    # img = image.load_img(img_path, target_size=(224, 224))
    # img_array = image.img_to_array(img)
    # img_array = np.expand_dims(img_array, axis=0) / 255.0

    # preds = model.predict(img_array)
    # pred_class = np.argmax(preds, axis=1)[0]
    # confidence = float(np.max(preds))
    # return CLASS_NAMES[pred_class], confidence
