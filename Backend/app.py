import os
import random
import time
import requests
from vosk import Model, KaldiRecognizer
import wave
from flask import Flask, request, jsonify, render_template

# --- App Setup ---
app = Flask(__name__)

# Directory to save uploaded audio files
UPLOAD_FOLDER = 'uploads'
# Create the uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# List of emotions used for simulation
EMOTIONS = ["Joy", "Sadness", "Anger", "Calmness", "Fear", "Disgust", "Surprise", "Neutral", "Excitement", "Love"]

def detect_emotion_from_audio(filepath):
    """
    Converts audio to text, sends text to Gemini API, and returns detected emotion.
    """
    print(f"[INFO] Audio file: {os.path.basename(filepath)} received for processing.")
    transcript = ""
    # Convert .webm to .wav using ffmpeg
    wav_path = filepath.replace('.webm', '.wav')
    try:
        import subprocess
        ffmpeg_cmd = [
            'ffmpeg', '-y', '-i', filepath, wav_path
        ]
        subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[INFO] Converted {filepath} to {wav_path}")
    except Exception as e:
        print(f"[ERROR] ffmpeg conversion failed: {e}")
        wav_path = None

    # Transcribe the .wav file using Vosk
    if wav_path and os.path.exists(wav_path):
        try:
            # Download Vosk model if not present (small English model)
            model_path = "vosk-model-small-en-us-0.15"
            if not os.path.exists(model_path):
                print("[INFO] Downloading Vosk model (this may take a while)...")
                import urllib.request
                import tarfile
                url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
                zip_path = "vosk-model-small-en-us-0.15.zip"
                urllib.request.urlretrieve(url, zip_path)
                import zipfile
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall('.')
                os.remove(zip_path)
            model = Model(model_path)
            wf = wave.open(wav_path, "rb")
            rec = KaldiRecognizer(model, wf.getframerate())
            rec.SetWords(True)
            results = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    res = rec.Result()
                    results.append(res)
            final_res = rec.FinalResult()
            import json
            try:
                final_json = json.loads(final_res)
                transcript = final_json.get("text", "")
            except Exception:
                transcript = ""
            print(f"[INFO] Transcribed text: {transcript}")
            wf.close()
        except Exception as e:
            print(f"[ERROR] Vosk speech-to-text failed: {e}")
            transcript = ""
        # Clean up the wav file
        try:
            os.remove(wav_path)
            print(f"[INFO] Cleaned up file: {os.path.basename(wav_path)}")
        except Exception as e:
            print(f"[ERROR] Error removing file {wav_path}: {e}")
    else:
        print(f"[ERROR] .wav file not found for transcription.")

    # Clean up the uploaded .webm file
    try:
        os.remove(filepath)
        print(f"[INFO] Cleaned up file: {os.path.basename(filepath)}")
    except Exception as e:
        print(f"[ERROR] Error removing file {filepath}: {e}")

    if not transcript:
        return "Unknown"

    # Use provided Gemini API key and model
    gemini_api_key = "AIzaSyDII36KZEiYIpdONmgKG-IDXau4hZGLJ5I"
    gemini_model = "gemini-2.5-flash-preview-09-2025"
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent?key={gemini_api_key}"
    prompt = f"What emotion is expressed in the following text? Reply with only the emotion word.\nText: {transcript}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        response = requests.post(gemini_url, json=payload)
        result = response.json()
        # Extract emotion from Gemini response
        emotion = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Unknown")
        print(f"[GEMINI LOG] Emotion detected: {emotion}")
        return emotion
    except Exception as e:
        print(f"[ERROR] Gemini API call failed: {e}")
        return "Unknown"

# --- Simulated Emotion Detection for Text ---
def detect_emotion_from_text(text_input):
    """
    Simulates emotion detection from text input.
    """
    time.sleep(random.uniform(0.5, 1.5)) # simulate processing

    # Simple keyword-based hint for simulation realism
    if "energetic" in text_input.lower() or "conquer" in text_input.lower():
        predicted_emotion = random.choice(["Joy", "Excitement", "Anger"])
    elif "sad" in text_input.lower() or "melancholy" in text_input.lower():
        predicted_emotion = "Sadness"
    else:
        predicted_emotion = random.choice(EMOTIONS)

    # Logs the input and the result to the terminal
    print(f"[TEXT INPUT LOG] Input: '{text_input[:50]}...' -> Detected Emotion: {predicted_emotion}")
    
    return predicted_emotion

# ----------------------------------------------------------------------
#                             FLASK ROUTES
# ----------------------------------------------------------------------

# --- Route to Handle Audio Upload (Voice Input) ---
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    # 1. Check for the file key 'audio_blob' as defined in the frontend JS
    if 'audio_blob' not in request.files:
        # NOTE: Using a placeholder path here as the function requires one. 
        # The first instance of detect_emotion_from_audio was redundant and removed.
        return jsonify({"success": False, "message": "No audio file in request."}), 400

    audio_file = request.files['audio_blob']
    if audio_file.filename == '':
        return jsonify({"success": False, "message": "No file selected."}), 400

    # 2. Save uploaded file with a unique name
    filename = f"recording_{int(time.time())}_{random.randint(100, 999)}.webm"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    audio_file.save(filepath)

    # 3. Convert audio to text and detect emotion using Gemini
    emotion_result = detect_emotion_from_audio(filepath)

    # 4. Return JSON response to the frontend
    return jsonify({"success": True, "emotion": emotion_result})

# --- Route to Handle Text Submission (Describe Your Vibe) ---
@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.get_json()
    text = data.get('text_input', '').strip()

    if not text:
        return jsonify({"success": False, "message": "No text provided."}), 400

    # Detect emotion from text (logging happens inside this function)
    emotion_result = detect_emotion_from_text(text)

    return jsonify({"success": True, "emotion": emotion_result})

# --- Route to Handle Quick Mood Picker ---
@app.route('/quick_mood', methods=['POST'])
def quick_mood():
    """
    Handles mood selection from the quick picker. 
    It receives the mood key and immediately returns it as the 'detected emotion'.
    """
    data = request.get_json()
    mood_key = data.get('mood', '').strip()

    if not mood_key:
        return jsonify({"success": False, "message": "No mood selected."}), 400
    
    # Capitalize for consistency with other route outputs (e.g., 'joy' -> 'Joy')
    detected_emotion = mood_key.capitalize()

    print(f"[QUICK PICK LOG] Mood Selected: {detected_emotion}")

    # The result is the mood itself, ready to be processed by the frontend JS
    return jsonify({"success": True, "emotion": detected_emotion})


# --- Route to serve HTML ---
@app.route('/')
def index():
    # Serve the index.html from the 'templates' folder
    return render_template('index.html')

if __name__ == '__main__':
    # use_reloader=False is kept as per your original prompt
    app.run(debug=True, use_reloader=False)