// ✅ QR Scanner using qr-scanner library (fast + worker-based)
import QrScanner from "https://cdn.jsdelivr.net/npm/qr-scanner@1.4.2/qr-scanner.min.js";

let scanner = null;

async function startScanner() {
    const videoElem = document.getElementById("video");

    if (scanner) {
        await scanner.start();
        return;
    }

    scanner = new QrScanner(
        videoElem,
        async (result) => {
            console.log("QR detected:", result.data);
            await handleQRSuccess(result.data);
        },
        {
            maxScansPerSecond: 35, // 15  // ⚡ fast but not too heavy
            highlightScanRegion: false,
            highlightCodeOutline: true
        }
    );

    await scanner.start();
    showMessage("📷 Camera started. Point at a QR code.", "info");
}

async function stopScanner() {
    if (scanner) {
        await scanner.stop();
    }
    showMessage("⏹️ Scanner stopped.", "info");
}

// ✅ Auto brightness/contrast adjustment (optional preprocessing)
function preprocessFrame(imageData) {
    const data = imageData.data;
    for (let i = 0; i < data.length; i += 4) {
        let r = data[i], g = data[i + 1], b = data[i + 2];
        let brightness = 30;
        let contrast = 1.1;

        r = (r - 128) * contrast + 128 + brightness;
        g = (g - 128) * contrast + 128 + brightness;
        b = (b - 128) * contrast + 128 + brightness;

        data[i] = Math.max(0, Math.min(255, r));
        data[i + 1] = Math.max(0, Math.min(255, g));
        data[i + 2] = Math.max(0, Math.min(255, b));
    }
    return imageData;
}

async function handleQRSuccess(qrData) {
    await stopScanner(); // stop camera immediately

    try {
        const response = await fetch("/api/scan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ qr_data: qrData }),
        });

        const result = await response.json();
        if (result.success) {
            window.location.href = result.redirect_url;
        } else {
            showMessage(`❌ ${result.message}`, "error");
            setTimeout(() => startScanner(), 1000); // 2000
        }
    } catch (error) {
        console.error("QR processing error:", error);
        showMessage("❌ Error processing QR code. Please try again.", "error");
        setTimeout(() => startScanner(), 1000); // 2000
    }
}

let messageTimeout = null; // global timeout reference

function showMessage(text, type = "info", duration = 1000) {
    const messageDiv = document.getElementById("message");
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = "block";
    messageDiv.textContent = text;
    messageDiv.className = `message ${type} show`; // add 'show' class to fade in
    // Clear any previous timeout
    if (messageTimeout) {
        clearTimeout(messageTimeout);
    }

    // Hide the message after `duration` milliseconds
    messageTimeout = setTimeout(() => {
        messageDiv.classList.remove("show"); // fade out
    }, duration);
}


// Auto-start scanner
document.addEventListener("DOMContentLoaded", () => {
    startScanner();
});

// Stop scanner when leaving page
window.addEventListener("beforeunload", () => {
    stopScanner();
});
