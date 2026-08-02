import os
import shutil
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Request
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
# Directories
# -------------------------------
BASE_DIR = Path(__file__).parent

UPLOAD_DIR = BASE_DIR / "uploads"
RESULTS_DIR = BASE_DIR / "results"
MODEL_PATH = BASE_DIR / "best.pt"

UPLOAD_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# -------------------------------
# Load YOLO Model
# -------------------------------
model = YOLO(str(MODEL_PATH))

# -------------------------------
# Serve Result Images
# -------------------------------
app.mount("/results", StaticFiles(directory=str(RESULTS_DIR)), name="results")


@app.get("/")
def home():
    return {
        "message": "✅ SentinelAI Backend Running Successfully"
    }


@app.post("/predict")
async def predict(request: Request, file: UploadFile = File(...)):

    # Save uploaded image
    image_path = UPLOAD_DIR / file.filename

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run prediction
    results = model.predict(
        source=str(image_path),
        conf=0.05,
        save=True
    )

    detections = []

    filename = image_path.name

    for result in results:

        # Collect detections
        for box in result.boxes:

            detections.append({

                "class": model.names[int(box.cls[0])],

                "confidence": round(float(box.conf[0]), 2)

            })

        output_image = Path(result.save_dir) / filename

        if output_image.exists():

            shutil.copy(
                output_image,
                RESULTS_DIR / filename
            )

    # Dynamic URL (works locally and on Render)
    base_url = str(request.base_url).rstrip("/")

    return {

        "total_detections": len(detections),

        "detections": detections,

        "output_image": f"{base_url}/results/{filename}"

    }