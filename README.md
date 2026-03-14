# SatyaShield: AI-Powered Forensic Suite 🛡️

SatyaShield is an advanced, high-performance forensic toolkit designed to defend truth in the era of AI. Built for hackathons and professional security analysts, it provides a comprehensive suite of tools to verify facts, detect deepfakes, and stop digital scams using **Gemini 2.0 Flash**.

## 🚀 Key Features

*   **Fact Detection**: Real-time verification of textual claims using Google Gemini AI.
*   **Deepfake Image Analysis**: Forensic pixel examination to detect AI-generated manipulations.
*   **WhatsApp Scam Detector**: Heuristic-based analysis to identify social engineering and phishing messages.
*   **URL Risk Assessment**: Multi-layered check for malicious domains and phishing patterns.
*   **Secure QR Scanner**: Payload analysis for hidden malicious links in QR codes.
*   **Video Authenticity**: Frame-by-frame consistency check for media verification.

## 🛠️ Tech Stack

*   **Backend**: Python, Flask
*   **AI Engine**: Google Gemini 2.0 Flash (via `google-genai`)
*   **Forensics**: OpenCV, NumPy, TLDextract
*   **UI/UX**: Modern CSS (Glassmorphism), Vanilla JS

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd SatyaShield
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure Environment:
   Create a `.env` file in the root directory and add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

4. Run the Application:
   ```bash
   python app.py
   ```

## 🛡️ Hybrid Intelligence
SatyaShield features a unique **Hybrid Heuristic Engine** that provides pattern-based forensic reports even if the cloud AI engine is syncing or bandwidth is limited, ensuring zero downtime in critical forensic tasks.

---
*Developed for Advanced Digital Forensics and Fact-Checking.*
