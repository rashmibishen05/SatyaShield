# SatyaShield: AI-Powered Forensic Suite 🛡️
[🚀 Live Application](https://satyashield.onrender.com/)

**SatyaShield** is an advanced, high-performance forensic toolkit designed to defend truth in the era of AI. Built for hackathons and professional security analysts, it provides a comprehensive suite of tools to verify facts, detect deepfakes, and stop digital scams using the power of **Google Gemini 2.0 Flash**.

---

## 🚀 Key Features

*   🔍 **Fact Verification**: Real-time cross-referencing of textual claims using Google Gemini AI.
*   🖼️ **Deepfake Detection**: Forensic pixel examination to identify AI-generated image manipulations.
*   📱 **WhatsApp Scam Shield**: Heuristic-based analysis to flag social engineering and phishing attempts.
*   🌐 **URL Risk Assessment**: Multi-layered check for malicious domains and phishing patterns.
*   🏁 **Secure QR Scanner**: Payload analysis for hidden malicious links in QR codes.
*   🎥 **Video Authenticity**: Frame-by-frame consistency checks for advanced media verification.

---

## 🛠️ Tech Stack

| Category | Technologies |
| :--- | :--- |
| **Backend** | Python 3.x, Flask |
| **AI Engine** | Google Gemini 2.0 Flash (`google-genai`) |
| **Forensics** | OpenCV, NumPy, TLDextract, PIL |
| **Frontend** | HTML5, Modern CSS (Glassmorphism), Vanilla JavaScript |
| **Deployment** | Gunicorn, Procfile, Render |

---

## 📦 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/rashmibishen05/SatyaShield.git
cd SatyaShield
```

### 2. Set up environment
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_new_api_key_from_google_ai_studio
   ```

### 3. Run the Suite
```bash
python app.py
```
Open `http://localhost:5000` in your browser.

---

## 🛡️ Hybrid Intelligence
SatyaShield features a unique **Hybrid Heuristic Engine**. This ensures that even during API rate-limiting or network instability, the system provides pattern-based forensic reports, ensuring zero downtime for critical fact-checking tasks.

---

*Developed for Advanced Digital Forensics and Fact-Checking.*
