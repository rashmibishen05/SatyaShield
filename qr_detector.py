import cv2
import numpy as np
from url_detector import check_url


def decode_qr(img):
    """Attempt to decode a QR code using OpenCV's built-in detector."""
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    if data:
        return data

    # Try with pre-processing: grayscale + threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    data, bbox, _ = detector.detectAndDecode(thresh)
    if data:
        return data

    # Try CLAHE enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    data, bbox, _ = detector.detectAndDecode(enhanced)
    return data if data else None


def check_qr(file):
    try:
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if img is None:
            return "❌ Error: Could not decode the image. Please upload a valid JPG or PNG file."

        data = decode_qr(img)

        if not data:
            return (
                "⚠️ No QR code detected in the image.\n"
                "Tips: Make sure the QR code is clear, well-lit, and fills most of the image."
            )

        # Analyze the QR content
        result_lines = [f"🔍 QR Code Decoded Successfully!"]
        result_lines.append(f"Content: {data}")

        if data.startswith("http://") or data.startswith("https://"):
            url_result = check_url(data)
            result_lines.append(f"\n🌐 URL Security Scan:\n{url_result}")
        elif data.startswith("WIFI:"):
            result_lines.append("\n📶 Type: WiFi Network Configuration")
            result_lines.append("⚠️ Caution: Only connect to WiFi QR codes from trusted sources.")
        elif data.startswith("BEGIN:VCARD") or data.startswith("MECARD:"):
            result_lines.append("\n👤 Type: Contact Card (vCard/MECARD)")
            result_lines.append("✅ This is a contact information QR code.")
        elif data.startswith("mailto:"):
            result_lines.append("\n📧 Type: Email Address")
            result_lines.append("⚠️ Verify before sending emails to unknown addresses.")
        elif data.startswith("tel:"):
            result_lines.append("\n📞 Type: Phone Number")
        elif data.startswith("upi://") or "upi" in data.lower():
            result_lines.append("\n💳 Type: UPI Payment QR")
            result_lines.append("⚠️ Caution: NEVER scan UPI QR codes from unknown sources — this is a common payment scam!")
        else:
            result_lines.append("\n📝 Type: Plain Text / Other Data")
            result_lines.append("✅ No suspicious URL or payment link detected.")

        return "\n".join(result_lines)

    except Exception as e:
        return f"❌ Error reading QR code: {str(e)}"
