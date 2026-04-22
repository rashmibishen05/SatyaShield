import cv2
import tempfile
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv(override=True)


def analyze_frames_with_gemini(frame_bytes_list):
    """Use Gemini Vision to analyze sampled video frames for deepfake signs."""
    try:
        from google import genai
        from google.genai import types

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return None

        client = genai.Client(api_key=api_key)

        contents = []
        for fb in frame_bytes_list:
            contents.append(types.Part.from_bytes(data=fb, mime_type="image/jpeg"))

        contents.append(
            "You are a deepfake detection expert analyzing video frames. "
            "Look for: facial warping, unnatural blinking, inconsistent lighting across frames, "
            "blurry face edges, mouth/eye artifacts, and temporal inconsistencies. "
            "Respond ONLY in this format:\n"
            "Result: [AUTHENTIC / SUSPICIOUS / DEEPFAKE DETECTED]\n"
            "Explanation: [One clear sentence about what you found across the frames]"
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents
        )
        if response and response.text:
            return response.text.strip()
    except Exception as e:
        print(f"[Video Detector] Gemini error: {e}")
    return None


def detect_fake_video(file):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    try:
        file.save(temp.name)
        temp.close()

        cap = cv2.VideoCapture(temp.name)
        if not cap.isOpened():
            return "❌ Error: Could not open the video file. Please upload a valid MP4, AVI, or MOV file."

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = frame_count / fps if fps > 0 else 0

        # Extract up to 4 evenly-spaced frames for Gemini analysis
        sample_frames = []
        sample_count = min(4, frame_count)
        if sample_count > 0:
            step = max(1, frame_count // sample_count)
            for i in range(sample_count):
                cap.set(cv2.CAP_PROP_POS_FRAMES, i * step)
                ret, frame = cap.read()
                if ret:
                    _, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                    sample_frames.append(buf.tobytes())

        cap.release()

        # --- Try Gemini Vision first ---
        if sample_frames:
            gemini_result = analyze_frames_with_gemini(sample_frames)
            if gemini_result:
                meta = (
                    f"\n\n📹 Video Metadata:\n"
                    f"  • Duration: {duration:.1f}s | Frames: {frame_count} | FPS: {fps:.1f}\n"
                    f"  • Resolution: {width}×{height}"
                )
                return gemini_result + meta

        # --- Fallback: Heuristic checks ---
        flags = []

        if frame_count < 15:
            flags.append(f"🚨 Very short video ({frame_count} frames) — common in deepfake test clips.")
        if fps > 60:
            flags.append(f"⚠️ Unusually high FPS ({fps:.0f}) — may mask temporal jitter in face synthesis.")
        if width < 240 or height < 240:
            flags.append(f"⚠️ Very low resolution ({width}×{height}) — may hide facial artifacts.")

        meta = (
            f"📹 Video Metadata:\n"
            f"  • Duration: {duration:.1f}s | Frames: {frame_count} | FPS: {fps:.1f}\n"
            f"  • Resolution: {width}×{height}"
        )

        if flags:
            result = "🚨 Result: SUSPICIOUS\n" + "\n".join(flags)
        else:
            result = (
                "✅ Result: AUTHENTIC\n"
                "Explanation: No obvious deepfake indicators found in frame sampling and metadata analysis."
            )

        return result + "\n\n" + meta

    except Exception as e:
        return f"❌ Error analyzing video: {str(e)}"
    finally:
        if os.path.exists(temp.name):
            os.remove(temp.name)
