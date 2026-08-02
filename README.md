# 🚀 SentinelAI - AI Powered Smart Infrastructure Monitoring

SentinelAI is an AI-powered infrastructure monitoring system that detects road damages such as **cracks** and **potholes** using the **YOLOv11 Object Detection Model**. The application provides real-time detection through a modern web interface and helps authorities prioritize maintenance before infrastructure failures become critical.

---

## 🌐 Live Demo

### Frontend
https://YOUR-VERCEL-LINK.vercel.app

### Backend API
https://sentinelai-backend-namk.onrender.com

---

## 📌 Features

- 🧠 AI-powered crack & pothole detection
- 📷 Upload infrastructure images
- ⚡ Real-time object detection using YOLOv11
- 📊 Interactive AI dashboard
- 🎯 Detection confidence scores
- 📈 Damage statistics
- 🖼️ Processed image with bounding boxes
- ☁️ FastAPI backend deployment on Render
- 🌐 Responsive frontend deployed on Vercel

---

## 🛠️ Tech Stack

### Frontend

- HTML5
- CSS3
- JavaScript
- Font Awesome

### Backend

- Python
- FastAPI
- Uvicorn
- Ultralytics YOLOv11
- OpenCV

### Deployment

- Vercel (Frontend)
- Render (Backend)
- GitHub

---

# 📂 Project Structure

```
# 📂 Project Structure

```text
SentinelAIv11/
│
├── ai/
│   ├── prepare_dataset.py      # Dataset preprocessing and organization
│   ├── train.py                # YOLOv11 model training script
│   └── predict.py              # Local prediction/testing script
│
├── backend/
│   ├── main.py                 # FastAPI backend API
│   ├── best.pt                 # Trained YOLOv11 model weights
│   └── requirements.txt        # Python dependencies
│    
│
├── frontend/
│   ├── index.html              # User Interface
│   ├── style.css               # Website styling
│   └── script.js               # Frontend logic & API integration
│
├── runs/                       # YOLO training & prediction outputs
│
├── .gitignore                  # Ignored files
│
└── README.md                   # Project documentation

```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/SentinelAIv11.git
```

```bash
cd SentinelAIv11
```

---

# Backend Setup

```bash
cd backend
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Run FastAPI

```bash
uvicorn main:app --reload
```

Backend runs at

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

Open

```
frontend/index.html
```

or use Live Server in VS Code.

---

# API Endpoint

## POST

```
/predict
```

### Request

Multipart Form Data

```
file : image
```

---

### Sample Response

```json
{
    "success": true,
    "total_detections": 13,
    "detections": [
        {
            "class": "crack",
            "confidence": 0.94
        }
    ],
    "output_image": "https://your-backend/results/image.jpg"
}
```

---

# Workflow

```
User Uploads Image
        │
        ▼
Frontend (HTML/CSS/JS)
        │
        ▼
FastAPI Backend
        │
        ▼
YOLOv11 Model
        │
        ▼
Object Detection
        │
        ▼
Bounding Boxes Generated
        │
        ▼
Detection Results Returned
        │
        ▼
Frontend Dashboard
```

---

# Screenshots

## Home Page

(Add Screenshot)

---

## AI Detection

(Add Screenshot)

---

## Dashboard

(Add Screenshot)

---

# Future Improvements

- 🎥 Live CCTV Monitoring
- 🚁 Drone Image Analysis
- 🗺️ GPS Damage Mapping
- 📊 Analytics Dashboard
- 📄 PDF Inspection Reports
- 🔔 Email Notifications
- 📱 Mobile Application

---

# Contributors

**JRavi**

GitHub:
https://github.com/vipin-vr

---

# License

This project is licensed under the MIT License.

---

⭐ If you like this project, don't forget to Star the repository.