// ==============================
// SentinelAI Frontend Script
// ==============================

const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const outputImage = document.getElementById("outputImage");

const statusBox = document.getElementById("status");
const totalBox = document.getElementById("total");
const crackBox = document.getElementById("cracks");
const potholeBox = document.getElementById("potholes");
const detectionsBox = document.getElementById("detections");


// ==============================
// Preview Uploaded Image
// ==============================

imageInput.addEventListener("change", function () {

    const file = imageInput.files[0];

    if (!file) return;

    previewImage.src = URL.createObjectURL(file);

    outputImage.src = "";

    detectionsBox.innerHTML = "";

    statusBox.innerHTML = "📷 Image Ready for AI Analysis";

    statusBox.style.background = "#0ea5e9";

});


// ==============================
// Scroll Function
// ==============================

function scrollToUpload() {

    document.getElementById("upload").scrollIntoView({

        behavior: "smooth"

    });

}


// ==============================
// Animate Numbers
// ==============================

function animateValue(element, endValue) {

    let start = 0;

    const duration = 800;

    const stepTime = Math.max(Math.floor(duration / endValue), 30);

    const timer = setInterval(() => {

        start++;

        element.innerHTML = start;

        if (start >= endValue) {

            element.innerHTML = endValue;

            clearInterval(timer);

        }

    }, stepTime);

}


// ==============================
// AI Prediction
// ==============================

async function predict() {

    const file = imageInput.files[0];

    if (!file) {

        alert("Please upload an infrastructure image.");

        return;

    }

    const button = document.querySelector(".upload-box button");

    button.disabled = true;

    button.innerHTML = "Analyzing...";

    statusBox.innerHTML = "🤖 AI is analyzing the image...";

    statusBox.style.background = "#f59e0b";

    detectionsBox.innerHTML = "";

    outputImage.src = "";

    const formData = new FormData();

    formData.append("file", file);

    try {

        const response = await fetch("http://127.0.0.1:8000/predict", {

            method: "POST",

            body: formData

        });

        if (!response.ok) {

            throw new Error("Backend Error");

        }

        const data = await response.json();

        animateValue(totalBox, data.total_detections);

        let crackCount = 0;

        let potholeCount = 0;

        let detectionHTML = "";

        data.detections.forEach((item, index) => {

            if (item.class.toLowerCase() === "crack") crackCount++;

            if (item.class.toLowerCase() === "pothole") potholeCount++;

            detectionHTML += `

            <div class="detection-item">

                <strong>${index + 1}. ${item.class.toUpperCase()}</strong>

                <br>

                Confidence :
                ${(item.confidence * 100).toFixed(1)}%

            </div>

            `;

        });

        animateValue(crackBox, crackCount);

        animateValue(potholeBox, potholeCount);

        detectionsBox.innerHTML = detectionHTML;

        if (data.total_detections > 0) {

            statusBox.innerHTML = "⚠ Maintenance Required";

            statusBox.style.background = "#dc2626";

        }

        else {

            statusBox.innerHTML = "✅ Infrastructure is Safe";

            statusBox.style.background = "#16a34a";

        }

        outputImage.src = data.output_image + "?t=" + new Date().getTime();

    }

    catch (error) {

        console.log(error);

        statusBox.innerHTML = "❌ Unable to connect to FastAPI Backend";

        statusBox.style.background = "#dc2626";

    }

    finally {

        button.disabled = false;

        button.innerHTML = "Analyze Image";

    }

}


// ==============================
// Navbar Scroll Effect
// ==============================

window.addEventListener("scroll", () => {

    const navbar = document.querySelector(".navbar");

    if (window.scrollY > 50) {

        navbar.style.background = "rgba(5,17,31,0.98)";

        navbar.style.boxShadow = "0 10px 30px rgba(0,0,0,.35)";

    }

    else {

        navbar.style.background = "rgba(7,20,38,.92)";

        navbar.style.boxShadow = "none";

    }

});


// ==============================
// Fade In Animation
// ==============================

const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            entry.target.style.opacity = "1";

            entry.target.style.transform = "translateY(0px)";

        }

    });

}, {

    threshold: 0.15

});

document.querySelectorAll(

    ".feature-card,.workflow-card,.impact-card,.dash-card,.stat-card"

).forEach(card => {

    card.style.opacity = "0";

    card.style.transform = "translateY(50px)";

    card.style.transition = "0.8s";

    observer.observe(card);

});