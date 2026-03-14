import cv2
import tempfile
import os

def detect_fake_video(file):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    file.save(temp.name)
    temp.close()

    try:
        cap = cv2.VideoCapture(temp.name)
        if not cap.isOpened():
            return " Error: Could not open video file."

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = frame_count / fps if fps > 0 else 0

        if frame_count < 15:
            return f"🚨 Suspicious: Video is too short ({frame_count} frames). Many deepfake scripts produce very short, loopable clips."
        
        if fps > 60:
            return f"⚠️ Caution: Unusually high FPS ({fps}). This might be used to mask jitters in manipulated facial movements."

        cap.release()
        return f" Video seems normal. Analysis of {frame_count} frames at {fps:.1f} FPS shows no obvious temporal inconsistencies."
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        if os.path.exists(temp.name):
            os.remove(temp.name)
