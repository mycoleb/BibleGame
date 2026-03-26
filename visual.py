import json
import random
import os

# Load your offline backup
with open('bible_backup.json', 'r') as f:
    bible_data = json.load(f)

# Load or initialize stats
stats_file = 'player_stats.json'
if os.path.exists(stats_file):
    with open(stats_file, 'r') as f:
        player_stats = json.load(f)
else:
    # Initialize { "Genesis": {"correct": 0, "total": 0}, ... }
    player_stats = {book['name']: {"correct": 0, "total": 0} for book in bible_data['books']}

def play_round():
    # 1. Pick a random book, chapter, and verse
    book = random.choice(bible_data['books'])
    chapter = random.choice(book['chapters'])
    verse = random.choice(chapter['verses'])
    
    print(f"\nVERSE: {verse['text']}")
    
    # 2. Logic for multiple choice (same as before)
    # ... (omitted for brevity)
    
    # 3. Update Stats
    player_stats[book['name']]['total'] += 1
    if user_is_correct:
        player_stats[book['name']]['correct'] += 1
        
    # 4. Save stats back to JSON
    with open(stats_file, 'w') as f:
        json.dump(player_stats, f)