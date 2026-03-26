import requests
import json

def download_bible():
    # Using a more stable direct link to the KJV JSON
    url = "https://raw.githubusercontent.com/sevenrepublic/KJV_Bible_JSON/master/kjv.json"
    
    try:
        print("Downloading Bible backup...")
        response = requests.get(url, timeout=10)
        response.raise_for_status() # This will catch 404 or 500 errors
        
        bible_data = response.json()
        with open("bible_backup.json", "w") as f:
            json.dump(bible_data, f)
        print("Success! 'bible_backup.json' is ready.")
    except Exception as e:
        print(f"Failed to download: {e}")

download_bible()