import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def get_supported_model():
    # Directly return the desired model name
    return "gemini-2.5-flash-preview-09-2025"

def recommend_songs_by_mood(mood, api_key):
    try:
        genai.configure(api_key=api_key)
        model_name = get_supported_model()
        if not model_name:
            print("No models support generateContent in your setup.")
            return None
        print("Using model:", model_name)
        model = genai.GenerativeModel(model_name)
        prompt = f"Recommend 5 popular songs that match the mood: {mood}. List only the song title and artist."
        response = model.generate_content(prompt)
        if hasattr(response, "text") and response.text.strip():
            return response.text.strip()
        else:
            print("No response text received from Gemini API.")
            return None
    except Exception as e:
        print("Error while generating content:", str(e))
        return None

if __name__ == "__main__":
    mood = input("Enter your mood: ")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("API key not found in .env file.")
    else:
        songs = recommend_songs_by_mood(mood, api_key)
        if songs:
            print("\nRecommended songs:\n", songs)
        else:
            print("Could not fetch recommendations. Please check your API key, internet connection, and Gemini API access.")
