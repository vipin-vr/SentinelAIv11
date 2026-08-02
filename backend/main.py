import os
import shutil
from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO

app = FastAPI()

# -------------------------------
# Enable CORS
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Load YOLO model
# -------------------------------
model = YOLO("runs/detect/runs/sentinel_ai/weights/best.pt")

# -------------------------------
# Results folder
# -------------------------------
RESULTS_DIR = "results"
Path(RESULTS_DIR).mkdir(exist_ok=True)

# Serve images
app.mount("/results", StaticFiles(directory=RESULTS_DIR), name="results")


@app.get("/")
def home():
    return {
        "message": "Sentinel AI Backend Running"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Save uploaded image
    image_path = file.filename

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Predict
    results = model.predict(
        source=image_path,
        conf=0.05,
        save=True
    )

    detections = []

    filename = os.path.basename(image_path)

    for result in results:

        # Collect detections
        for box in result.boxes:
            detections.append({
                "class": model.names[int(box.cls[0])],
                "confidence": round(float(box.conf[0]), 2)
            })

        # Copy the generated image from runs/... to results/
        output_image = os.path.join(
            result.save_dir,
            filename
        )

        shutil.copy(
            output_image,
            os.path.join(RESULTS_DIR, filename)
        )

    return {
        "total_detections": len(detections),
        "detections": detections,
        "output_image": f"http://127.0.0.1:8000/results/{filename}"
    }