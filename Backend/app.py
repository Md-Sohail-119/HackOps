import os
import random
import time
from flask import Flask, request, jsonify, render_template

# --- Flask App Initialization ---
app = Flask(__name__)

# Directory to save uploaded audio files (only for demonstration/simulated storage)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# --- Simulated Emotion Detection Function ---
def detect_emotion(filepath):
    """
    SIMULATED FUNCTION: Replaces actual Speech Emotion Recognition (SER) model logic.
    In a real application, this function would analyze the audio file 
    at the given filepath to predict emotion.
    """
    # Simulate processing time (3-5 seconds)
    time.sleep(random.uniform(3, 5))

    emotions = ["Joy", "Sadness", "Anger", "Calmness", "Fear", "Disgust", "Surprise"]
    predicted_emotion = random.choice(emotions)

    # Clean up uploaded file
    try:
        os.remove(filepath)
        print(f"Cleaned up file: {filepath}")
    except Exception as e:
        print(f"Error removing file {filepath}: {e}")

    return predicted_emotion


# --- Backend Route to Handle Audio Upload ---
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'audio_blob' not in request.files:
        return jsonify({"success": False, "message": "No audio file part in request."}), 400

    audio_file = request.files['audio_blob']

    if audio_file.filename == '':
        return jsonify({"success": False, "message": "No selected file."}), 400

    if audio_file:
        filename = f"recording_{int(time.time())}.webm"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(filepath)

        # Perform simulated analysis
        emotion_result = detect_emotion(filepath)

        return jsonify({
            "success": True,
            "emotion": emotion_result,
            "message": "Analysis complete (simulated)."
        })

    return jsonify({"success": False, "message": "Unknown error during file upload."}), 500


# --- Frontend Route ---
@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
