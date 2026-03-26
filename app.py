import streamlit as st
import pandas as pd
import random
import os

# --- Configuration & Styling ---
st.set_page_config(page_title="Bible Trivia", page_icon="📖")

st.markdown("""
    <style>
    .verse-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        font-size: 20px;
        font-style: italic;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Data Loading (Cached for Speed) ---
@st.cache_data
def load_data():
    if os.path.exists('kjv.csv'):
        # Skip 0 because you edited your file, but clean headers
        df = pd.read_csv('kjv.csv', skiprows=0)
        df.columns = [c.replace('"', '').strip().lower() for c in df.columns]
        df.rename(columns={'book name': 'book', 'text': 'text'}, inplace=True)
        return df
    return None

df = load_data()

# --- Game State Management ---
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.total = 0
if 'current_verse' not in st.session_state:
    # Pick initial verse
    row = df.sample(n=1).iloc[0]
    st.session_state.current_verse = row
    
# --- UI Layout ---
st.title("📖 Bible Trivia Challenge")
st.write(f"**Score:** {st.session_state.score} / {st.session_state.total}")

if df is not None:
    # Display the Verse
    verse = st.session_state.current_verse
    st.markdown(f'<div class="verse-box">"{verse["text"]}"</div>', unsafe_allow_html=True)

    # Generate Options
    all_books = df['book'].unique().tolist()
    correct_book = verse['book']
    
    # We use a button form to handle choices
    cols = st.columns(2)
    options = [correct_book]
    while len(options) < 4:
        cand = random.choice(all_books)
        if cand not in options: options.append(cand)
    random.shuffle(options)

    # Handle Answer
    for i, option in enumerate(options):
        if cols[i % 2].button(option, use_container_width=True):
            st.session_state.total += 1
            if option == correct_book:
                st.success(f"Correct! It was {correct_book}.")
                st.session_state.score += 1
            else:
                st.error(f"Wrong! That was {correct_book}.")
            
            # Load next verse for next interaction
            st.session_state.current_verse = df.sample(n=1).iloc[0]
            st.button("Next Verse ➡️")

else:
    st.error("CSV file not found. Please check kjv.csv")

# --- Sidebar Stats ---
with st.sidebar:
    st.header("Your Stats")
    if st.session_state.total > 0:
        accuracy = (st.session_state.score / st.session_state.total) * 100
        st.metric("Accuracy", f"{accuracy:.1f}%")
    if st.button("Reset Stats"):
        st.session_state.score = 0
        st.session_state.total = 0
        st.rerun()