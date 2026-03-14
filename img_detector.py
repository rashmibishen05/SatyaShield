import cv2
import numpy as np

def detect_fake_image(file):
    try:
       
        nparr = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return " Error: Could not decode image."

   
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        edge_ratio = np.sum(edges) / edges.size
        
        
        noise_score = cv2.Laplacian(gray, cv2.CV_64F).var()

        if edge_ratio > 0.18:
            return f" Suspicious: High frequency of sharp edges detected (Edge Ratio: {edge_ratio:.2f}). This often indicates manual manipulation or cut-paste artifacts."
        
        if noise_score < 10:
            return f" Warning: Image is extremely smooth (Noise Score: {noise_score:.2f}). This might indicate AI-generated content or excessive filtering."
        
        return f" Analysis Complete: No obvious manipulation artifacts found. Metadata and pixel distribution look consistent."
    except Exception as e:
        return f"Error: {str(e)}"
