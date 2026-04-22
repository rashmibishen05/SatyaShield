from flask import Flask, render_template, request, jsonify
import logging
import os
from dotenv import load_dotenv

load_dotenv(override=True)

from img_detector import detect_fake_image
from video_detector import detect_fake_video
from url_detector import check_url
from qr_detector import check_qr
from whtapp_msg_detector import detect_whatsapp_scam
from fact_checker import check_claim

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB max upload size
logging.basicConfig(level=logging.INFO)

# Ensure JSON responses can contain emojis
app.config['JSON_AS_ASCII'] = False


@app.errorhandler(413)
def too_large(e):
    return jsonify({"result": "❌ File too large. Maximum upload size is 50MB."}), 413


@app.errorhandler(400)
def bad_request(e):
    return jsonify({"result": f"❌ Bad request: {str(e)}"}), 400


@app.errorhandler(500)
def server_error(e):
    return jsonify({"result": f"❌ Server error: {str(e)}"}), 500



@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/dashboard")
def home():
    return render_template("index.html")

@app.route("/text")
def text_page():
    return render_template("text.html")

@app.route("/url")
def url_page():
    return render_template("url.html")

@app.route("/message")
def message_page():
    return render_template("message.html")

@app.route("/image")
def image_page():
    return render_template("image.html")

@app.route("/qr")
def qr_page():
    return render_template("qr.html")

@app.route("/video")
def video_page():
    return render_template("video.html")

@app.route("/detect-image", methods=["POST"])
def image_detector():
    if 'image' not in request.files:
        return jsonify({"result": "No image uploaded"}), 400
    file = request.files["image"]
    try:
        result = detect_fake_image(file)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"}), 500

@app.route("/detect-news", methods=["POST"])
def detect_news():
    data = request.get_json()
    if not data or "news" not in data:
        return jsonify({"result": "No text provided"}), 400
    news = data["news"]
    try:
        result = check_claim(news)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"}), 500

@app.route("/detect-video", methods=["POST"])
def video_detector():
    if 'video' not in request.files:
        return jsonify({"result": "No video uploaded"}), 400
    file = request.files["video"]
    try:
        result = detect_fake_video(file)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"}), 500

@app.route("/detect-url", methods=["POST"])
def url_detector():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"result": "No URL provided"}), 400
    url = data["url"]
    try:
        result = check_url(url)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"}), 500

@app.route("/detect-qr", methods=["POST"])
def qr_detector():
    if 'qr' not in request.files:
        return jsonify({"result": "No QR code uploaded"}), 400
    file = request.files["qr"]
    try:
        result = check_qr(file)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"}), 500

@app.route("/detect-message", methods=["POST"])
def message_detector():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"result": "No message provided"}), 400
    text = data["message"]
    try:
        result = detect_whatsapp_scam(text)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)