import shutil
from pathlib import Path

import cv2
from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from ultralytics import YOLO

app = FastAPI(
    title="SentinelAI API",
    version="1.0"
)

# ---------------------------------
# CORS
# ---------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------
# Paths
# ---------------------------------

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"
RESULT_DIR = BASE_DIR / "results"
MODEL_PATH = BASE_DIR / "best.pt"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------
# Load Model
# ---------------------------------

print("================================")
print("Loading SentinelAI Model...")
print("================================")

model = YOLO(str(MODEL_PATH))

print("Model Loaded Successfully")
print("Classes:", model.names)

# ---------------------------------
# Home
# ---------------------------------

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "SentinelAI Backend Running Successfully"
    }

# ---------------------------------
# Serve Output Image
# ---------------------------------

@app.get("/results/{filename}")
def get_result(filename: str):

    image_path = RESULT_DIR / filename

    if not image_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Image not found"
        )

    return FileResponse(image_path)

# ---------------------------------
# Prediction
# ---------------------------------

@app.post("/predict")
async def predict(
    request: Request,
    file: UploadFile = File(...)
):

    try:

        image_path = UPLOAD_DIR / file.filename

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        results = model.predict(
            source=str(image_path),
            conf=0.05,
            imgsz=640,
            device="cpu",
            save=False,
            verbose=False
        )

        detections = []

        output_path = RESULT_DIR / file.filename

        for result in results:

            for box in result.boxes:

                detections.append({
                    "class": model.names[int(box.cls[0])],
                    "confidence": round(float(box.conf[0]), 2)
                })

            annotated = result.plot()

            cv2.imwrite(
                str(output_path),
                annotated
            )

        if not output_path.exists():

            raise HTTPException(
                status_code=500,
                detail="Failed to save output image."
            )

        print("--------------------------------")
        print("Saved:", output_path)
        print("Exists:", output_path.exists())
        print("--------------------------------")

        base_url = str(request.base_url).rstrip("/")

        return {

            "success": True,

            "total_detections": len(detections),

            "detections": detections,

            "output_image":
                f"{base_url}/results/{file.filename}"

        }

    except Exception as e:

        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )