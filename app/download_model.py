import os
import requests

def download_model():
    MODEL_PATH = "model.keras"
    MODEL_URL = "https://drive.google.com/uc?export=download&id=FILE_ID"
    # ^ Replace with your actual model URL

    if not os.path.exists(MODEL_PATH):
        print("🔽 Model not found. Downloading model.keras ...")
        response = requests.get(MODEL_URL, stream=True)
        if response.status_code == 200:
            with open(MODEL_PATH, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("✅ Model downloaded successfully.")
        else:
            raise Exception(f"❌ Failed to download model. Status code: {response.status_code}")
    else:
        print("✅ Model already exists. Skipping download.")

if __name__ == "__main__":
    download_model()
