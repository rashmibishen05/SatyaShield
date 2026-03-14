from pyzbar.pyzbar import decode
from PIL import Image
from url_detector import check_url

def check_qr(file):
    try:
        img = Image.open(file)
        decoded = decode(img)

        if decoded:
            data = decoded[0].data.decode("utf-8")
            if data.startswith("http"):
                url_result = check_url(data)
                return f"🔍 Found URL: {data}\n\nScan Result: {url_result}"
            else:
                return f"📝 QR Code Data: {data}"
        
        return " No QR code found in the image."
    except Exception as e:
        return f"Error reading QR: {str(e)}"
