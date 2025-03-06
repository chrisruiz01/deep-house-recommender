import schedule
import time
import subprocess

def update_spotify_data():
    print("Fetching new Spotify data...")
    subprocess.run(["python", "spotify_auth.py"])  # Runs the script automatically

# Run every hour
schedule.every(1).hours.do(update_spotify_data)

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
