import cv2
import numpy as np
from url_detector import check_url

def check_qr(file):
    try:
        # Read image file using OpenCV
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if img is None:
            return " Error: Could not decode image."

        # Use OpenCV's built-in QR Code detector 
        # (This is much better for Render as it doesn't need extra Linux libraries)
        detector = cv2.QRCodeDetector()
        data, bbox, straight_qrcode = detector.detectAndDecode(img)

        if data:
            if data.startswith("http"):
                url_result = check_url(data)
                return f"🔍 Found URL: {data}\n\nScan Result: {url_result}"
            else:
                return f"📝 QR Code Data: {data}"
        
        return " No QR code found in the image."
    except Exception as e:
        return f"Error reading QR: {str(e)}"
