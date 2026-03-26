import csv
import pandas as pd
import requests
import json
import random
import os
import matplotlib.pyplot as plt

# File paths
CSV_FILE = 'kjv.csv'
STATS_FILE = 'player_stats.json'

def load_local_data():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(
                CSV_FILE, 
                sep=',', 
                skiprows=0,           # Changed to 0 because you deleted the intro lines
                engine='python', 
                encoding='utf-8', 
                quoting=csv.QUOTE_MINIMAL, 
                on_bad_lines='skip'
            )
            
            # Clean headers
            df.columns = [c.replace('"', '').strip().lower() for c in df.columns]
            print(f"Detected Columns: {df.columns.tolist()}")
            
            rename_map = {'book name': 'book', 'text': 'text'}
            df.rename(columns=rename_map, inplace=True)
            
            # THE FIX: Added .str before .strip()
            if 'book' in df.columns and 'text' in df.columns:
                df['book'] = df['book'].astype(str).str.replace('"', '', regex=False).str.strip()
                df['text'] = df['text'].astype(str).str.replace('"', '', regex=False).str.strip()
                return df
            else:
                print(f"Error: Missing columns. Found: {df.columns.tolist()}")
                
        except Exception as e:
            print(f"Error reading CSV: {e}")
    return None
def get_stats(books):
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {book: {"correct": 0, "total": 0} for book in books}

def save_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f)

def run_trivia_logic(correct_book, verse_text, all_books, stats):
    options = [correct_book]
    while len(options) < 4:
        cand = random.choice(all_books)
        if cand not in options: options.append(cand)
    random.shuffle(options)

    print(f"\nVERSE: \"{verse_text}\"")
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")

    ans = input("Choice (1-4): ")
    try:
        idx = int(ans) - 1
        stats[correct_book]['total'] += 1
        if options[idx] == correct_book:
            print("Correct!")
            stats[correct_book]['correct'] += 1
        else:
            print(f"Wrong! It was {correct_book}")
        save_stats(stats)
    except:
        print("Invalid input.")

def play_game(df): 
    print("--- Running in Offline Mode (CSV) ---")
    
    # Standardize column names based on your interests in Python data cleaning
    if 'v_book' in df.columns: df.rename(columns={'v_book': 'book'}, inplace=True)
    if 'v_text' in df.columns: df.rename(columns={'v_text': 'text'}, inplace=True)
    
    all_books = df['book'].unique().tolist()
    stats = get_stats(all_books)
    
    while True:
        row = df.sample(n=1).iloc[0]
        correct_book = row['book']
        verse_text = row['text']
        
        run_trivia_logic(correct_book, verse_text, all_books, stats)
        if input("\nPlay again? (y/n): ").lower() != 'y': 
            break

if __name__ == "__main__":
    bible_df = load_local_data()

    if bible_df is not None:
        play_game(bible_df)
    else:
        print("Could not load Bible data. Check kjv.csv.")