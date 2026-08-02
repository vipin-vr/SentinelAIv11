import os
import shutil
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO


app = FastAPI(
    title="SentinelAI API",
    description="AI Powered Infrastructure Damage Detection",
    version="1.0"
)


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

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"
RESULTS_DIR = BASE_DIR / "results"
MODEL_PATH = BASE_DIR / "best.pt"


UPLOAD_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)


# -------------------------------
# Load YOLO Model
# -------------------------------

print("Loading YOLO model...")

model = YOLO(str(MODEL_PATH))

print("YOLO model loaded successfully")


# -------------------------------
# Serve Result Images
# -------------------------------

app.mount(
    "/results",
    StaticFiles(directory=str(RESULTS_DIR)),
    name="results"
)


# -------------------------------
# Home API
# -------------------------------

@app.get("/")
def home():

    return {
        "status": "running",
        "message": "SentinelAI Backend Successfully Deployed 🚀"
    }


# -------------------------------
# Prediction API
# -------------------------------

@app.post("/predict")
async def predict(
    request: Request,
    file: UploadFile = File(...)
):

    try:

        # Save uploaded image

        image_path = UPLOAD_DIR / file.filename


        with open(image_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


        # Run YOLO prediction

        results = model.predict(
            source=str(image_path),
            conf=0.05,
            imgsz=320,
            save=True,
            project=str(RESULTS_DIR),
            name="prediction",
            exist_ok=True,
            verbose=False
        )
        print("YOLO RESULTS:")
        for r in results:
            print(r.boxes)


        detections = []


        for result in results:


            # Extract detections

            for box in result.boxes:


                detections.append({

                    "class":
                    model.names[int(box.cls[0])],

                    "confidence":
                    round(float(box.conf[0]), 2)

                })


            # YOLO output path

            output_image = (
                Path(result.save_dir)
                / file.filename
            )


            final_image = RESULTS_DIR / file.filename


            if output_image.exists():

                shutil.copy(
                    output_image,
                    final_image
                )


        base_url = str(request.base_url).rstrip("/")


        return {


            "success": True,

            "total_detections":
            len(detections),


            "detections":
            detections,


            "output_image":
            f"{base_url}/results/{file.filename}"

        }


    except Exception as e:


        raise HTTPException(
            status_code=500,
            detail=str(e)
        )