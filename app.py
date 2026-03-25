import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date
import plotly.express as px

# --- DATA: Questions from a2zinterviews logic ---
QUESTIONS = [
    {
        "id": 1,
        "question": "In what ratio must rice at Rs. 9.30 per kg be mixed with rice at Rs. 10.80 per kg so that the mixture be worth Rs. 10 per kg?",
        "options": ["7:8", "8:7", "5:6", "6:5"],
        "answer": "8:7",
        "explanation": "By Rule of Alligation:\n(Cheaper Price) 9.30  |  10.80 (Dearer Price)\n           (Mean) 10.00\n(10.80-10.00) = 0.80  |  (10.00-9.30) = 0.70\nRatio = 0.80 : 0.70 = 8:7"
    },
    {
        "id": 2,
        "question": "A container contains 40 litres of milk. From this container, 4 litres of milk was taken out and replaced by water. This process was repeated further two times. How much milk is now contained by the container?",
        "options": ["26.34L", "27.36L", "28L", "29.16L"],
        "answer": "29.16L",
        "explanation": "Formula: Amount of liquid left = x(1 - y/x)^n\n= 40(1 - 4/40)^3 = 40(9/10)^3 = 40 * 729/1000 = 29.16 litres."
    },
    {
        "id": 3,
        "question": "In what ratio must water be mixed with milk to gain 16 2/3% by selling the mixture at cost price?",
        "options": ["1:6", "6:1", "2:3", "4:3"],
        "answer": "1:6",
        "explanation": "Profit = 16 2/3% = 50/3%. Ratio of Water:Milk = Profit% : 100% = (50/3) : 100 = 50 : 300 = 1:6."
    }
]

# --- DATABASE LOGIC (JSON) ---
DB_FILE = "user_stats.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"history": [], "last_login": None, "streak": 0}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# --- APP CONFIG ---
st.set_page_config(page_title="AptiStreak - Daily Practice", layout="wide")
user_data = load_data()

# --- STREAK CALCULATOR ---
today = str(date.today())
if user_data["last_login"] != today:
    if user_data["last_login"] == str(date.fromordinal(date.today().toordinal() - 1)):
        user_data["streak"] += 1
    elif user_data["last_login"] is None or user_data["last_login"] < today:
        user_data["streak"] = 1
    user_data["last_login"] = today
    save_data(user_data)

# --- SIDEBAR: PRODUCTIVITY ---
st.sidebar.title("📊 Productivity")
st.sidebar.metric("Daily Streak", f"{user_data['streak']} Days", "🔥")

if user_data["history"]:
    df = pd.DataFrame(user_data["history"])
    fig = px.line(df, x="date", y="score", title="Score Trend")
    st.sidebar.plotly_chart(fig, use_container_width=True)

# --- MAIN UI ---
st.title("🎯 Alligation & Mixture Practice")
st.write("Reference: a2zinterviews.com logic")

if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.submitted = False

# Question Display
q_idx = st.session_state.current_q

if q_idx < len(QUESTIONS):
    q = QUESTIONS[q_idx]
    st.subheader(f"Question {q_idx + 1}")
    st.write(q["question"])
    
    choice = st.radio("Select an option:", q["options"], key=f"q_{q_idx}")
    
    if st.button("Submit Answer"):
        if choice == q["answer"]:
            st.success("Correct!")
            st.session_state.score += 1
        else:
            st.error(f"Wrong! Correct answer is {q['answer']}")
        
        st.info(f"**Explanation:** {q['explanation']}")
        st.session_state.submitted = True

    if st.session_state.submitted:
        if st.button("Next Question"):
            st.session_state.current_q += 1
            st.session_state.submitted = False
            st.rerun()
else:
    st.balloons()
    st.header("Practice Complete!")
    final_score = st.session_state.score
    st.metric("Final Score", f"{final_score}/{len(QUESTIONS)}")
    
    # Save to history
    if st.button("Save Result & End Day"):
        user_data["history"].append({"date": today, "score": final_score})
        save_data(user_data)
        st.success("Progress Saved!")
        if st.button("Restart"):
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.rerun()
