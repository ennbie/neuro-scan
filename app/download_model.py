import os
import gdown
from dotenv import load_dotenv

load_dotenv()

def download_model():
    DEFAULT_PATH = "app/model/model.tflite"
    MODEL_PATH = os.getenv("MODEL_PATH", DEFAULT_PATH)
    FILE_ID = os.getenv("MODEL_FILE_ID")

    if not os.path.exists(MODEL_PATH):
        print(f"🔽 Model not found at {MODEL_PATH}. Downloading...")
        try:

            if not FILE_ID:
                print("❗ MODEL_FILE_ID not set. Set the MODEL_FILE_ID environment variable (or add it to .env) to enable automatic download.")
                return

            MODEL_URL = f"https://drive.google.com/uc?id={FILE_ID}"

            # ensure parent directory exists
            parent_dir = os.path.dirname(MODEL_PATH)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)

            gdown.download(MODEL_URL, MODEL_PATH, quiet=False)
            print("✅ Model downloaded successfully.")
        except Exception as exc:
            print("❌ Failed to download model:", exc)
    else:
        print(f"✅ Model already exists at {MODEL_PATH}. Skipping download.")


if __name__ == "__main__":
    download_model()
