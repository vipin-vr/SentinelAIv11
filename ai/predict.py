from pathlib import Path
from ultralytics import YOLO
import sys

# ==========================
# Project Paths
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "backend" / "best.pt"

# ==========================
# Load Model
# ==========================

print("Loading model...")
model = YOLO(str(MODEL_PATH))
print("Model loaded successfully!")
print("Classes:", model.names)

# ==========================
# Check Input Image
# ==========================

if len(sys.argv) < 2:
    print("\nUsage:")
    print("python ai/predict.py images/image.jpg")
    sys.exit()

image_path = Path(sys.argv[1])

if not image_path.exists():
    print(f"\nImage not found: {image_path}")
    sys.exit()

# ==========================
# Run Prediction
# ==========================

results = model.predict(
    source=str(image_path),
    conf=0.05,
    imgsz=640,
    save=True,
    verbose=True
)

# ==========================
# Display Results
# ==========================

print("\n==============================")
print("DETECTION RESULTS")
print("==============================")

total = 0

for result in results:

    if len(result.boxes) == 0:
        print("No objects detected.")

    for box in result.boxes:

        cls = int(box.cls[0])
        conf = float(box.conf[0])

        print(
            f"{model.names[cls]}  |  Confidence: {conf:.2f}"
        )

        total += 1

    output_image = Path(result.save_dir) / image_path.name

print("\n------------------------------")
print("Total Detections :", total)
print("Output Image     :", output_image)
print("------------------------------")
print("\nPrediction Completed Successfully!")