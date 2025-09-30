import os
import random
import time
from flask import Flask, request, jsonify, render_template

# --- App Setup ---
app = Flask(__name__)

# Directory to save uploaded audio files
UPLOAD_FOLDER = 'uploads'
# Create the uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Simulated Emotion Detection ---
def detect_emotion(filepath):
    """
    Simulates emotion detection on an audio file.
    Logs the emotion to console (not displayed in HTML).
    """
    time.sleep(random.uniform(1, 2))  # simulate processing
    
    # Ensure this list aligns with the mood keys (or moods) used in the JS logic
    emotions = ["Joy", "Sadness", "Anger", "Calmness", "Fear", "Disgust", "Surprise", "Neutral"]
    predicted_emotion = random.choice(emotions)

    # Log the detected emotion
    print(f"[INFO] Audio file: {os.path.basename(filepath)}")
    print(f"[INFO] Predicted Emotion: {predicted_emotion}")

    # Clean up the uploaded file
    try:
        os.remove(filepath)
        print(f"[INFO] Cleaned up file: {os.path.basename(filepath)}")
    except Exception as e:
        print(f"[ERROR] Error removing file {filepath}: {e}")

    return predicted_emotion

# --- Route to Handle Audio Upload ---
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    # 1. Check for the file key 'audio_blob' as defined in the frontend JS
    if 'audio_blob' not in request.files:
        return jsonify({"success": False, "message": "No audio file in request."}), 400

    audio_file = request.files['audio_blob']
    if audio_file.filename == '':
        return jsonify({"success": False, "message": "No file selected."}), 400

    # 2. Save uploaded file with a unique name
    filename = f"recording_{int(time.time())}_{random.randint(100, 999)}.webm"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    audio_file.save(filepath)

    # 3. Detect emotion and clean up the file
    emotion_result = detect_emotion(filepath)

    # 4. Return JSON response to the frontend
    return jsonify({"success": True, "emotion": emotion_result})

# --- Route to serve HTML ---
@app.route('/')
def index():
    # Serve the index.html from the 'templates' folder
    return render_template('index.html')

if __name__ == '__main__':
    # use_reloader=False is kept as per your original prompt
    app.run(debug=True, use_reloader=False)