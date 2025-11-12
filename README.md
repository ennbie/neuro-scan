# NeuroScan — Brain Tumor Detection System

A web-based AI application for detecting brain tumors in MRI scans using deep learning and transfer learning. Built with FastAPI, TensorFlow, and Bootstrap for modern, real-time insights.

## 🎯 Overview

NeuroScan is an intelligent brain tumor detection system that analyzes MRI scans to classify tumors as **benign** or **malignant**. The system uses a Convolutional Neural Network (CNN) with VGG16 transfer learning to provide accurate predictions with confidence scores.

**⚠️ Disclaimer:** This tool is for educational and research purposes only. It should not be used as a standalone diagnostic tool. Always consult with qualified medical professionals for diagnosis and treatment decisions.

## ✨ Features

- **AI-Powered Detection** — Uses a CNN model with VGG16 transfer learning for accurate classification
- **Batch Upload** — Process multiple MRI images at once with drag-and-drop interface
- **Real-Time Progress** — Monitor upload and processing with dynamic progress indicators
- **Confidence Metrics** — Transparent confidence scores help assess prediction reliability
- **Session History** — Track all predictions during the current session
- **Retry on Failure** — Easily retry failed uploads with a single click
- **Responsive Design** — Works seamlessly on desktop, tablet, and mobile devices
- **Educational Content** — Dedicated about page explaining the technology and methodology

## 🏗️ Technology Stack

### Backend
- **Framework:** FastAPI
- **Server:** Uvicorn
- **Python:** 3.8+
- **Machine Learning:** TensorFlow, Keras
- **Image Processing:** OpenCV
- **File Handling:** python-multipart

### Frontend
- **HTML5/CSS3/JavaScript** 
- **Bootstrap 5** for responsive UI
- **Drag-and-drop file upload**
- **Session storage for history**

### Model
- **Architecture:** Convolutional Neural Network (CNN)
- **Transfer Learning:** VGG16 pre-trained weights
- **Input Size:** 224×224 pixels
- **Output:** Binary classification (Benign/Malignant)
- **Model File:** `model.keras`

## 📋 Requirements

- Python 3.8 or higher
- pip or conda for package management
- 2GB+ RAM recommended for model inference

All dependencies are listed in `requirements.txt`.

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ennbie/neuro-scan.git
cd brain-tumor-detection
```

### 2. Create a Virtual Environment (Recommended)

**Using venv:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Using conda:**
```bash
conda create -n neuroscan python=3.12
conda activate neuroscan
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Model File
Ensure `model.keras` exists in the project root directory. If missing, run:
```bash
python app/download_model.py
```

## 🔧 Configuration

### Model Path
Edit `app/model.py` to change the model file path:
```python
MODEL_PATH = "app/model/model.keras"  # Change this path if needed
```

### Environment (.env)

Create a `.env` file at the project root to hold environment variables. `app/main.py` calls `load_dotenv()` on startup, so variables in `.env` are loaded automatically when the server runs.

Minimal example (`.env`):

```text
MODEL_FILE_ID=1A2B3C4D...    # (Google Drive file id for model.keras)
# Optional override:
MODEL_PATH=app/model/model.keras
```

If you don't use a `.env` file, set `MODEL_FILE_ID` in your shell before running the downloader, or place `model.keras` manually in `app/model/`.

## 🎮 Usage

### Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The application will be available at:
```
http://localhost:8000
```

### Accessing the Application

1. **Home Page** — Navigate to `http://localhost:8000/` for the landing page
2. **Diagnosis** — Go to `http://localhost:8000/diagnose` to upload and analyze MRI scans
3. **About** — Visit `http://localhost:8000/about` to learn about the technology

### Using the Diagnosis Page

1. **Upload Images:**
   - Click "Select Images" or drag-and-drop MRI files onto the zone
   - Supports JPEG, PNG, and other standard image formats

2. **Monitor Progress:**
   - Progress bar shows upload status
   - Real-time prediction feedback

3. **View Results:**
   - Prediction (Benign/Malignant) displayed with confidence percentage
   - Color-coded badge indicates result severity
   - Results are automatically saved to session history

4. **Retry Failed Uploads:**
   - If an upload fails, a "Retry" button appears
   - Click to re-attempt the upload

5. **Session History:**
   - All predictions are stored during your session
   - Clear history with the "Clear History" button
   - History persists across page refreshes (until session ends)

## 📁 Project Structure

```
brain-tumor-detection/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── model.py                # Model loading and prediction logic
│   ├── download_model.py       # Download pre-trained model
│   ├── schemas.py              # Pydantic models for validation
│   ├── static/
│   │   ├── css/
│   │   │   ├── index.css       # Home page styling
│   │   │   ├── diagnose.css    # Diagnosis page styling
│   │   │   └── about.css       # About page styling
│   │   ├── js/
│   │   │   └── diagnose.js     # Diagnosis page interactivity
│   │   └── images/             # Static images and icons
│   └── templates/
│       ├── index.html          # Home page
│       ├── about.html          # About page
│       └── diagnose.html       # Diagnosis page
├── uploads/                    # Temporary upload directory
├── model.keras                 # Pre-trained model file
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── venv/                       # Virtual environment (if created locally)
```

## 📊 API Endpoints

### GET /
Serves the home page.

### GET /about
Serves the about page with technology information.

### GET /diagnose
Serves the diagnosis page for MRI upload and analysis.

### POST /predict
**Request:** Multipart form with image file
```bash
curl -X POST -F "file=@mri_scan.jpg" http://localhost:8000/predict
```

**Response:**
```json
{
  "prediction": "Benign",
  "confidence": 92.5
}
```

## 🧠 Model Details

- **Framework:** TensorFlow 2.19.0 + Keras
- **Architecture:** CNN with VGG16 transfer learning
- **Input:** 224×224 RGB images (normalized with VGG16 preprocessing)
- **Output:** Probability of malignancy (0-100%)
- **Classes:** Benign, Malignant

### Preprocessing Pipeline
1. Load image with OpenCV
2. Convert BGR to RGB
3. Resize to 224×224 pixels
4. Apply VGG16 preprocessing
5. Normalize pixel values (0-1 range)



---

**NeuroScan v1.0.0** — Built with ❤️ using FastAPI, TensorFlow, and Bootstrap
