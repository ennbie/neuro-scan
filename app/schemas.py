from pydantic import BaseModel, Field

class PredictionResponse(BaseModel):
    prediction: str = Field(..., example="Malignant")
    confidence: float = Field(..., example=0.97, description="Probability of tumor presence (0 to 1)")

class PredictionRequest(BaseModel):
    filename: str = Field(..., example="mri_scan_001.jpg", description="Filename of the MRI image")
