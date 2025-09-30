from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# ----------------------------
# 1. Load environment variables
# ----------------------------
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# ----------------------------
# 2. Authenticate with Spotipy
# ----------------------------
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# ----------------------------
# 3. Search for an artist
# ----------------------------
def search_for_artist(artist_name):
    results = sp.search(q=artist_name, type="artist", limit=1)
    if results['artists']['items']:
        artist = results['artists']['items'][0]
        artist_id = artist['id']

        # Fetch full artist info
        full_artist = sp.artist(artist_id)
        
        # Fallback for empty genres
        artist_genres = full_artist['genres'] if full_artist['genres'] else ['pop']
        
        print(f"Name: {full_artist['name']}")
        print(f"Followers: {full_artist['followers']['total']}")
        print(f"Popularity: {full_artist['popularity']}")
        print(f"Genres: {artist_genres}")
        print(f"Spotify URL: {full_artist['external_urls']['spotify']}")
    else:
        print("Artist not found.")

def search_for_song(song_name):
    results = sp.search(q=song_name, type="track", limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_name = track['name']
        artist_names = [artist['name'] for artist in track['artists']]
        track_id = track['id']
        popularity = track['popularity']
        spotify_url = track['external_urls']['spotify']
        
        # Try genre from the artist of the track.
        artist_id = track['artists'][0]['id']
        artist_info = sp.artist(artist_id)
        track_genres = artist_info['genres'] if artist_info['genres'] else ['pop']

        print(f"Song Name: {track_name}")
        print(f"Artists: {artist_names}")
        print(f"Genres: {track_genres}")
        print(f"Popularity: {popularity}")
        print(f"Spotify URL: {spotify_url}")
    else:
        print("Song not found.")



# Example
search_for_song("ROCKSTAR MADE")
