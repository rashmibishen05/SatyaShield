import cv2
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv(override=True)


def analyze_with_gemini(image_bytes):
    """Use Gemini Vision to analyze the image for manipulation/deepfakes."""
    try:
        from google import genai
        from google.genai import types

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return None

        client = genai.Client(api_key=api_key)

        prompt = (
            "You are a digital forensics expert. Analyze this image for signs of manipulation, "
            "deepfake generation, AI synthesis, or photo editing artifacts. "
            "Look for: unnatural lighting, inconsistent shadows, blurry edges around subjects, "
            "facial distortions, background inconsistencies, and pixel-level anomalies. "
            "Respond ONLY in this format:\n"
            "Result: [AUTHENTIC / SUSPICIOUS / MANIPULATED]\n"
            "Explanation: [One clear sentence describing what you found]"
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                prompt
            ]
        )
        if response and response.text:
            return response.text.strip()
    except Exception as e:
        print(f"[Image Detector] Gemini Vision error: {e}")
    return None


def detect_fake_image(file):
    try:
        image_bytes = file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            return "❌ Error: Could not decode the image. Please upload a valid JPG, PNG, or WEBP file."

        # --- Try Gemini Vision first ---
        gemini_result = analyze_with_gemini(image_bytes)
        if gemini_result:
            return gemini_result

        # --- Fallback: OpenCV heuristic analysis ---
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Edge analysis (high edges = possible cut-paste artifacts)
        edges = cv2.Canny(gray, 100, 200)
        edge_ratio = np.sum(edges > 0) / edges.size

        # Noise / smoothness analysis (low = AI-generated or over-filtered)
        noise_score = cv2.Laplacian(gray, cv2.CV_64F).var()

        # ELA-like analysis: compress and compare difference
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 75]
        _, encoded = cv2.imencode('.jpg', image, encode_param)
        compressed = cv2.imdecode(np.frombuffer(encoded, np.uint8), cv2.IMREAD_COLOR)
        ela_diff = cv2.absdiff(image, compressed)
        ela_mean = ela_diff.mean()

        report_lines = [
            f"📊 Forensic Analysis Report",
            f"  • Edge Ratio: {edge_ratio:.4f}",
            f"  • Noise Score: {noise_score:.2f}",
            f"  • ELA Score: {ela_mean:.2f}"
        ]

        if edge_ratio > 0.18:
            report_lines.append("\n🚨 Result: SUSPICIOUS")
            report_lines.append("Explanation: High frequency of sharp edges detected — possible cut-paste or compositing artifacts.")
        elif noise_score < 10:
            report_lines.append("\n⚠️ Result: SUSPICIOUS")
            report_lines.append("Explanation: Image is abnormally smooth — may indicate AI-generation or excessive filtering.")
        elif ela_mean > 15:
            report_lines.append("\n⚠️ Result: SUSPICIOUS")
            report_lines.append("Explanation: High Error Level Analysis score — certain regions show signs of re-compression typical of edited areas.")
        else:
            report_lines.append("\n✅ Result: AUTHENTIC")
            report_lines.append("Explanation: No obvious manipulation artifacts found. Pixel distribution and edge patterns look consistent.")

        return "\n".join(report_lines)

    except Exception as e:
        return f"❌ Error processing image: {str(e)}"
