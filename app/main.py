from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os, shutil
from app.model import predict_image

app = FastAPI()

# Mount static files for CSS, JS, and images
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Create folder for temporary uploads
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def serve_home():
    """Serve the frontend HTML page."""
    return FileResponse("app/templates/index.html")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Handle image upload and prediction."""
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    # Save the uploaded image temporarily
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Make prediction
    pred_class, confidence = predict_image(file_path)
    
    # Remove file after prediction
    os.remove(file_path)
    
    # Return JSON response
    return JSONResponse({
        "prediction": pred_class,
        "confidence": round(confidence * 100, 2)
    })
