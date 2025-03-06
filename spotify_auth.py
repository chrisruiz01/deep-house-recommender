import spotipy
from spotipy.oauth2 import SpotifyOAuth
import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Spotify API credentials

SPOTIPY_CLIENT_ID = "a4fa647a9aae4a50ba0e593cec485938"
SPOTIPY_CLIENT_SECRET = "df47a3c0b5444b92adffd4924bfe1eef"
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:8080/callback/"  # Updated per Spotify's warning

# PostgreSQL credentials
DB_NAME = "deep_house_db"
DB_USER = "postgres"
DB_PASSWORD = "password"  # Replace with your actual password
DB_HOST = "localhost"
DB_PORT = "5432"

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

# Authenticate with Spotify
scope = "user-read-recently-played user-top-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope
))

# Fetch recently played tracks
results = sp.current_user_recently_played(limit=10)

for item in results["items"]:
    track = item["track"]
    track_name = track["name"]
    artist = track["artists"][0]["name"]
    played_at = item["played_at"]  # Timestamp

    # Insert into PostgreSQL
    cursor.execute("""
        INSERT INTO spotify_history (track_name, artist, played_at) 
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING;
    """, (track_name, artist, played_at))

    print(f"✅ Inserted: {track_name} by {artist}")

# Commit and close connection
conn.commit()
cursor.close()
conn.close()
