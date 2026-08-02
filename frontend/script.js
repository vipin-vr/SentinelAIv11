// ==============================
// SentinelAI Frontend Script
// ==============================

// Backend API URL
const API_URL =
"https://sentinelai-backend-namk.onrender.com/predict";


// ==============================
// Elements
// ==============================

const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const outputImage = document.getElementById("outputImage");

const statusBox = document.getElementById("status");

const totalBox = document.getElementById("total");
const crackBox = document.getElementById("cracks");
const potholeBox = document.getElementById("potholes");

const detectionsBox = document.getElementById("detections");

const dashboardBtn =
document.getElementById("dashboardBtn");


// ==============================
// Preview Image
// ==============================

imageInput.addEventListener("change", () => {

    const file = imageInput.files[0];

    if (!file) return;

    previewImage.src = URL.createObjectURL(file);

    outputImage.src = "";

    detectionsBox.innerHTML = "";

    dashboardBtn.style.display = "none";

    totalBox.innerHTML = "0";
    crackBox.innerHTML = "0";
    potholeBox.innerHTML = "0";

    statusBox.innerHTML =
        "📷 Image Ready For AI Analysis";

    statusBox.style.background =
        "#0ea5e9";

});



// ==============================
// Scroll To Upload
// ==============================

function scrollToUpload() {

    document
        .getElementById("upload")
        .scrollIntoView({

            behavior: "smooth"

        });

}



// ==============================
// Go To Dashboard
// ==============================

function goToDashboard() {

    document
        .getElementById("dashboard")
        .scrollIntoView({

            behavior: "smooth"

        });

}



// ==============================
// Animate Numbers
// ==============================

function animateValue(element, value) {

    let start = 0;

    const timer = setInterval(() => {

        start++;

        element.innerHTML = start;

        if (start >= value) {

            element.innerHTML = value;

            clearInterval(timer);

        }

    }, 40);

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

    const button =
        document.querySelector(".upload-box button");

    button.disabled = true;

    button.innerHTML = "Analyzing...";

    statusBox.innerHTML =
        "🤖 AI is analyzing image...";

    statusBox.style.background = "#f59e0b";

    detectionsBox.innerHTML = "";

    outputImage.src = "";

    dashboardBtn.style.display = "none";

    const formData = new FormData();

    formData.append("file", file);

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            body: formData

        });

        if (!response.ok) {

            throw new Error("Backend Error");

        }

        const data = await response.json();

        console.log(data);

        animateValue(totalBox, data.total_detections);

        let cracks = 0;
        let potholes = 0;

        let html = "";

        data.detections.forEach((item, index) => {

            const cls = item.class.toLowerCase();

            if (cls.includes("crack"))
                cracks++;

            if (cls.includes("pothole"))
                potholes++;

            html += `

            <div class="detection-item">

                <strong>${index + 1}. ${item.class.toUpperCase()}</strong>

                <br>

                Confidence :
                ${(item.confidence * 100).toFixed(1)}%

            </div>

            `;

        });

        animateValue(crackBox, cracks);

        animateValue(potholeBox, potholes);

        detectionsBox.innerHTML = html;

        if (data.total_detections > 0) {

            statusBox.innerHTML =
                "⚠ Maintenance Required";

            statusBox.style.background =
                "#dc2626";

        }

        else {

            statusBox.innerHTML =
                "✅ Infrastructure is Safe";

            statusBox.style.background =
                "#16a34a";

        }

        outputImage.src =
            data.output_image +
            "?time=" +
            Date.now();

        // Show Dashboard Button
        dashboardBtn.style.display = "block";

    }

    catch (error) {

        console.log(error);

        statusBox.innerHTML =
            "❌ Unable To Connect Backend";

        statusBox.style.background =
            "#dc2626";

    }

    finally {

        button.disabled = false;

        button.innerHTML = "Analyze Image";

    }

}



// ==============================
// Navbar Effect
// ==============================

window.addEventListener("scroll", () => {

    const navbar =
        document.querySelector(".navbar");

    if (window.scrollY > 50) {

        navbar.style.background =
            "rgba(5,17,31,0.98)";

        navbar.style.boxShadow =
            "0 10px 30px rgba(0,0,0,.35)";

    }

    else {

        navbar.style.background =
            "rgba(7,20,38,.92)";

        navbar.style.boxShadow =
            "none";

    }

});



// ==============================
// Scroll Animation
// ==============================

const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            entry.target.style.opacity = "1";

            entry.target.style.transform =
                "translateY(0px)";

        }

    });

}, {

    threshold: 0.15

});

document.querySelectorAll(

    ".feature-card,.workflow-card,.impact-card,.dash-card,.stat-card"

).forEach(card => {

    card.style.opacity = "0";

    card.style.transform =
        "translateY(50px)";

    card.style.transition =
        "0.8s";

    observer.observe(card);

});