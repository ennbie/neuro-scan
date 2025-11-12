from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os, shutil
from app.model import predict_image
from app.schemas import PredictionResponse, PredictionRequest

app = FastAPI(
    title="Brain Tumor Detection API",
    description="Upload MRI scans to predict tumor presence using a CNN model.",
    version="1.0.0"
)

# Mount static files for CSS, JS, and images
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Create folder for temporary uploads
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post(
    "/predict",
    response_model=PredictionResponse,
    description="Uploads an MRI image file, runs it through the trained CNN model, and returns tumor classification along with confidence score.",
)
async def predict(file: UploadFile = File(..., description="Upload an MRI image in JPG/PNG format")):
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
    return PredictionResponse(prediction=pred_class, confidence=round(confidence * 100, 2)) 

@app.get("/")
def serve_home():
    """Serve the frontend HTML page."""
    return FileResponse("app/templates/index.html")

@app.get("/about")
def serve_about():
    """Serve the about page."""
    return FileResponse("app/templates/about.html")

@app.get("/diagnose")
def serve_diagnose():
    """Serve the diagnose page."""
    return FileResponse("app/templates/diagnose.html")
