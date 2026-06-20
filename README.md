# 🚀 Smart PiP Assistant

An enterprise-grade, cloud-synced Picture-in-Picture (PiP) architecture. Click a button on YouTube in your browser, and watch the video instantly pop open into a sleek, borderless, always-on-top desktop media player window.

---

## 🛠️ Architecture Overview

The system uses a decentralized triple-mesh pipeline to safely route media frames globally:



---

## 📥 Installation & Setup

### 1. Download the Desktop App
* Go to the **Releases** tab on the right side of this GitHub repository page.
* Download the latest `main.exe` binary.
* Place it in a dedicated folder on your computer.

### 2. Install the Chrome Extension
* Clone or download this repository to your computer.
* Open Google Chrome and navigate to `chrome://extensions/`.
* Enable **Developer mode** (top-right toggle).
* Click **Load unpacked** (top-left button) and select the `extension` folder from this project.

---

## ⚙️ Configuration (One-Time Setup)

To link your desktop app and browser extension together, they both need to point to your live cloud server:

1. **Configure the Extension:** * Right-click the Smart PiP Assistant icon in your browser toolbar and select **Options**.
   * Paste your live Render backend URL (e.g., `https://your-service.onrender.com`).
   * Click **Save Endpoint Connection**.

2. **Configure the Desktop App:**
   * In the same folder as your downloaded `main.exe`, create a file named `config.json`.
   * Paste the following code inside it, replacing the URL with your live Render backend URL:
     ```json
     {
       "CLOUD_SERVER_URL": "[https://your-service.onrender.com](https://your-service.onrender.com)"
     }
     ```

---

## 🚀 How to Use It

1. **Launch the Desktop Receiver:** Double-click `main.exe`. You will see a terminal open printing: `Cloud PiP Signalling Server Active!`. (Minimize this window, but keep it running in the background).
2. **Browse YouTube:** Open Google Chrome, head to any YouTube video, and you will see a bright red **🚀 Send to Cloud PiP** button placed neatly under the video title.
3. **Trigger PiP:** Click the button! The stream payload will route up through the cloud and instantly snap open your borderless desktop media player window.

* **Move Window:** Click and drag anywhere inside the video window.
* **Close Window:** Press `Esc` or standard close options to exit.
