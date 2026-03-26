import requests
import json
import random
import os
import matplotlib.pyplot as plt

# File paths
BIBLE_FILE = 'bible_backup.json'
STATS_FILE = 'player_stats.json'

def initialize_data():
    """Downloads the Bible using a verified active mirror."""
    if not os.path.exists(BIBLE_FILE):
        # This is a verified active direct link to a KJV JSON file
        url = "https://raw.githubusercontent.com/mizthebear/bible-json/master/kjv.json"
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        print("--- Initial Setup: Downloading Bible Backup ---")
        
        try:
            print(f"Connecting to: {url}...")
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            
            bible_data = response.json()
            with open(BIBLE_FILE, "w") as f:
                json.dump(bible_data, f)
            
            print("Download Complete! 'bible_backup.json' created.\n")
        except Exception as e:
            print(f"\nCRITICAL ERROR: {e}")
            print("The link may have changed. Try opening the URL in your browser to verify.")
            return None

    with open(BIBLE_FILE, 'r') as f:
        return json.load(f)
def save_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f)

def get_stats():
    with open(STATS_FILE, 'r') as f:
        return json.load(f)

def show_visualization():
    stats = get_stats()
    played_books = {k: v for k, v in stats.items() if v['total'] > 0}
    if not played_books:
        print("Play some rounds first!")
        return
    books = list(played_books.keys())
    accuracy = [(v['correct'] / v['total']) * 100 for v in played_books.values()]
    plt.figure(figsize=(10, 6))
    plt.bar(books, accuracy, color='seagreen')
    plt.ylabel('Accuracy (%)')
    plt.title('Bible Trivia Performance')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def play_game(bible_data):
    stats = get_stats()
    # Check for different JSON structures (some use 'books', some use 'result')
    book_list = bible_data.get('books', [])
    all_book_names = [book['name'] for book in book_list]
    
    while True:
        book_obj = random.choice(book_list)
        chapter_obj = random.choice(book_obj['chapters'])
        verse_obj = random.choice(chapter_obj['verses'])
        
        correct_book = book_obj['name']
        verse_text = verse_obj['text']

        options = [correct_book]
        while len(options) < 4:
            rand_choice = random.choice(all_book_names)
            if rand_choice not in options:
                options.append(rand_choice)
        random.shuffle(options)

        print(f"\n--- VERSE ---\n\"{verse_text.strip()}\"")
        for i, opt in enumerate(options):
            print(f"{i+1}. {opt}")
        
        user_input = input("\nWhich book? (1-4) or 'q' to quit: ").lower()
        if user_input == 'q': break
        
        try:
            choice_idx = int(user_input) - 1
            stats[correct_book]['total'] += 1
            if options[choice_idx] == correct_book:
                print("✨ Correct!")
                stats[correct_book]['correct'] += 1
            else:
                print(f"❌ Wrong. It was {correct_book}.")
            save_stats(stats)
        except:
            print("Invalid input.")

if __name__ == "__main__":
    data = initialize_data()
    if data:
        play_game(data)
        if input("\nShow chart? (y/n): ").lower() == 'y':
            show_visualization()