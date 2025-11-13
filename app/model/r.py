import tensorflow as tf

# Path to your Keras model
keras_model_path = "app/model/model.keras"
# Output path for the TFLite model
tflite_model_path = "app/model/model.tflite"

# Load the Keras model
model = tf.keras.models.load_model(keras_model_path)

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

# Save the TFLite model
with open(tflite_model_path, "wb") as f:
    f.write(tflite_model)

print(f"TFLite model saved to {tflite_model_path}")