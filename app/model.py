import tensorflow as tf
from tensorflow.keras.applications.vgg16 import preprocess_input
# import cv2
import numpy as np
import os
from app.download_model import download_model

# def preprocess_vgg16(img_array):
#     """
#     Manually replicates tf.keras.applications.vgg16.preprocess_input
#     using only NumPy.
#     """
#     img_array = img_array.astype('float32')
#     img_array_bgr = img_array[..., ::-1]
#     mean = [103.939, 116.779, 123.68] # BGR mean
#     img_array_bgr[..., 0] -= mean[0]
#     img_array_bgr[..., 1] -= mean[1]
#     img_array_bgr[..., 2] -= mean[2]
#     return img_array_bgr

# Ensure model is present
download_model()

MODEL_PATH = "app/model/model.tflite"
CLASS_NAMES = ['Benign', 'Malignant']

def predict_image(img_path):

    # Load TFLite model and allocate tensors (lazy loading)
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    
    # Get input and output tensors
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # Prepare image
    img_bytes = tf.io.read_file(img_path)
    img = tf.image.decode_image(img_bytes, channels=3)  # RGB uint8 tensor
    img = tf.image.resize(img, [224, 224])
    img = img.numpy()
    X = np.expand_dims(img, axis=0)
    # img = cv2.imread(img_path)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img = cv2.resize(img, (224, 224))
    # X = np.array([img])
    X_test = preprocess_input(X)
    X_test = X_test.astype(np.float32) / 255.0
    
    # Set input tensor
    interpreter.set_tensor(input_details[0]['index'], X_test)
    
    # Run inference
    interpreter.invoke()
    
    # Get output tensor
    Y_pred = interpreter.get_tensor(output_details[0]['index'])
    
    confidence = Y_pred[0][0]
    Y_pred = np.round(Y_pred).astype(int)
    pred_class = Y_pred[0][0]
    return CLASS_NAMES[pred_class], float(confidence)
