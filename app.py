import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date
import plotly.express as px

# --- EXPANDED DATASET (TCS, COGNIZANT, WIPRO) ---
# Sourced from a2zinterviews logic
QUESTIONS = [
    {
        "id": 1, "company": "TCS", "topic": "Alligation or Mixture",
        "question": "In what ratio must rice at Rs. 9.30 per kg be mixed with rice at Rs. 10.80 per kg so that the mixture be worth Rs. 10 per kg?",
        "options": ["7:8", "8:7", "5:6", "6:5"], "answer": "8:7",
        "explanation": "Ratio = (Dearer - Mean) : (Mean - Cheaper) = (10.80 - 10) : (10 - 9.30) = 0.80 : 0.70 = 8:7."
    },
    {
        "id": 2, "company": "Cognizant", "topic": "Alligation or Mixture",
        "question": "A container contains 40 litres of milk. 4 litres are taken out and replaced by water. This process is repeated twice more. How much milk is left?",
        "options": ["26.34L", "27.36L", "28L", "29.16L"], "answer": "29.16L",
        "explanation": "Formula: x(1 - y/x)^n => 40(1 - 4/40)^3 = 40 * (0.9)^3 = 29.16L."
    },
    {
        "id": 3, "company": "TCS", "topic": "Profit and Loss",
        "question": "A merchant sells sugar, part at 8% profit and rest at 18% profit. Total gain is 14%. If total sugar is 1000kg, find the amount sold at 18%.",
        "options": ["400kg", "560kg", "600kg", "640kg"], "answer": "600kg",
        "explanation": "Ratio = (18-14):(14-8) = 4:6 = 2:3. Part at 18% = (3/5)*1000 = 600kg."
    },
    {
        "id": 4, "company": "Wipro", "topic": "Time and Work",
        "question": "A can do work in 15 days, B in 20 days. They work together for 4 days. What fraction of work is left?",
        "options": ["1/4", "1/10", "7/15", "8/15"], "answer": "8:15",
        "explanation": "1 day work = (1/15 + 1/20) = 7/60. 4 days = 28/60 = 7/15. Left = 1 - 7/15 = 8/15."
    }
]

# --- DATABASE LOGIC ---
DB_FILE = "user_stats.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"history": [], "last_login": None, "streak": 0}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# --- APP CONFIG & STREAK ---
st.set_page_config(page_title="AptiStreak Pro", layout="wide")
user_data = load_data()
today = str(date.today())

# Streak Logic
if user_data["last_login"] != today:
    yesterday = str(date.fromordinal(date.today().toordinal() - 1))
    if user_data["last_login"] == yesterday:
        user_data["streak"] += 1
    else:
        user_data["streak"] = 1
    user_data["last_login"] = today
    save_data(user_data)

# --- SIDEBAR: PRODUCTIVITY ---
st.sidebar.title("📊 My Productivity")
st.sidebar.metric("Current Streak", f"{user_data['streak']} Days", "🔥")

if user_data["history"]:
    df = pd.DataFrame(user_data["history"])
    st.sidebar.subheader("Progress Trend")
    fig = px.line(df, x="date", y="score", markers=True)
    st.sidebar.plotly_chart(fig, use_container_width=True)

# --- MAIN UI ---
st.title("🎯 Company-wise Aptitude Practice")

# Filters
c1, c2 = st.columns(2)
with c1:
    sel_company = st.selectbox("Select Company", ["All", "TCS", "Cognizant", "Wipro"])
with c2:
    sel_topic = st.selectbox("Select Topic", ["All", "Alligation or Mixture", "Profit and Loss", "Time and Work"])

# Filtering Data
filtered_qs = [q for q in QUESTIONS if 
               (sel_company == "All" or q["company"] == sel_company) and 
               (sel_topic == "All" or q["topic"] == sel_topic)]

if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.submitted = False

if not filtered_qs:
    st.warning("No questions found for this selection.")
elif st.session_state.current_q < len(filtered_qs):
    q = filtered_qs[st.session_state.current_q]
    
    st.markdown(f"**Target Company:** `{q['company']}` | **Topic:** `{q['topic']}`")
    st.subheader(f"Question {st.session_state.current_q + 1}")
    st.write(q["question"])

    choice = st.radio("Choose the correct option:", q["options"], key=f"q_{st.session_state.current_q}")

    if st.button("Submit Answer"):
        if choice == q["answer"]:
            st.success("✔ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"✖ Incorrect. The answer is {q['answer']}")
        
        # Rule of Alligation Formula Visualization
        if q["topic"] == "Alligation or Mixture":
            st.write("---")
            st.markdown("**Rule of Alligation Logic:**")
            
        
        st.info(f"**Explanation:** {q['explanation']}")
        st.session_state.submitted = True

    if st.session_state.submitted:
        if st.button("Next Question ➡"):
            st.session_state.current_q += 1
            st.session_state.submitted = False
            st.rerun()
else:
    st.balloons()
    st.header("Session Complete!")
    st.metric("Final Score", f"{st.session_state.score}/{len(filtered_qs)}")
    
    if st.button("Save Daily Progress"):
        user_data["history"].append({"date": today, "score": st.session_state.score, "topic": sel_topic})
        save_data(user_data)
        st.success("Productivity Logged!")
        if st.button("Start New Session"):
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.rerun()
