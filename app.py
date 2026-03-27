import streamlit as st
import pandas as pd
import json
import os
import random
from datetime import datetime, date
import plotly.express as px

# --- DATABASE SETUP ---
DB_FILE = "user_stats_v2.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"history": [], "last_login": None, "streak": 0, "company_scores": {}}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# --- ADVANCED QUESTION BANK (2024-2026 Trends) ---
QUESTIONS = [
    # TCS NQT Patterns
    {"id": 1, "company": "TCS", "topic": "Arithmetic", "level": "Hard", "question": "The average height of boys in a class is 165 cm, and girls is 155 cm. If the class average is 160 cm, what is the ratio of boys to girls?", "options": ["1:1", "3:2", "2:3", "5:4"], "answer": "1:1", "explanation": "Using Alligation: (165-160) : (160-155) = 5 : 5 = 1:1."},
    {"id": 2, "company": "TCS", "topic": "Number System", "level": "Medium", "question": "A student divided a number by 10 instead of 25 and got an answer 6 more than the correct one. Find the number.", "options": ["80", "100", "120", "150"], "answer": "100", "explanation": "x/10 - x/25 = 6 => (5x-2x)/50 = 6 => 3x = 300 => x = 100."},
    
    # Cognizant GenC/Elevate Patterns
    {"id": 3, "company": "Cognizant", "topic": "Logical Reasoning", "level": "Medium", "question": "Complete the series: 2, 6, 12, 20, 30, ?", "options": ["36", "40", "42", "48"], "answer": "42", "explanation": "Pattern: +4, +6, +8, +10, +12. So, 30 + 12 = 42."},
    {"id": 4, "company": "Cognizant", "topic": "Technical Aptitude", "level": "Hard", "question": "In a DBMS, which property ensures that once a transaction is committed, it remains so even in the event of a system failure?", "options": ["Atomicity", "Consistency", "Isolation", "Durability"], "answer": "Durability", "explanation": "Durability guarantees that committed transactions are permanent."},
    
    # Infosys SP/DSE Patterns
    {"id": 5, "company": "Infosys", "topic": "Data Structures", "level": "Expert", "question": "Which data structure is most efficient for implementing an LRU (Least Recently Used) Cache?", "options": ["Queue", "Stack", "HashMap + Doubly Linked List", "Binary Search Tree"], "answer": "HashMap + Doubly Linked List", "explanation": "HashMap provides O(1) lookup, and Doubly Linked List provides O(1) removal/addition at ends."},
    {"id": 6, "company": "Infosys", "topic": "Probability", "level": "Hard", "question": "A bag contains 4 red, 3 blue, and 5 green balls. If two balls are drawn, what is the probability that none are red?", "options": ["14/33", "7/22", "8/12", "1/3"], "answer": "14/33", "explanation": "Total = 12. Non-red = 8. Prob = (8C2) / (12C2) = 28/66 = 14/33."},

    # Accenture Patterns
    {"id": 7, "company": "Accenture", "topic": "Time & Work", "level": "Medium", "question": "If 18 workers can complete a project in 10 days, how many days will it take 15 workers?", "options": ["12", "15", "11", "13"], "answer": "12", "explanation": "M1D1 = M2D2 => 18 * 10 = 15 * x => x = 180/15 = 12."},
    {"id": 8, "company": "Accenture", "topic": "Profit & Loss", "level": "Hard", "question": "A shopkeeper offers 10% discount on MP and still makes 26% profit. If CP is Rs. 400, find MP.", "options": ["500", "560", "600", "620"], "answer": "560", "explanation": "SP = 1.26 * 400 = 504. MP = 504 / 0.9 = 560."}
]

# --- APP CONFIG ---
st.set_page_config(page_title="AptiStreak Pro - Enterprise", layout="wide")

# Custom CSS for "Premium" look
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #2e7d32; color: white; }
    .metric-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

user_data = load_data()

# --- SIDEBAR & ANALYTICS ---
with st.sidebar:
    st.title("🚀 Career Dashboard")
    st.metric("Daily Streak", f"{user_data['streak']} Days", "🔥")
    
    if user_data["history"]:
        st.subheader("Placement Readiness")
        # Simple readiness logic
        df_hist = pd.DataFrame(user_data["history"])
        avg_score = df_hist["score_pct"].mean()
        st.progress(avg_score/100)
        st.caption(f"Average Accuracy: {avg_score:.1f}%")

# --- MAIN INTERFACE ---
st.title("🏆 IT Placement Command Center")
st.write("Targeting 2024-2026 Recruitment Cycles")

# Session Management
if 'q_idx' not in st.session_state:
    st.session_state.q_idx = 0
    st.session_state.session_score = 0
    st.session_state.ans_submitted = False

# Filters
col_a, col_b, col_c = st.columns(3)
with col_a:
    target_comp = st.selectbox("🎯 Target Company", ["All"] + list(set(q["company"] for q in QUESTIONS)))
with col_b:
    target_topic = st.selectbox("📚 Topic", ["All"] + list(set(q["topic"] for q in QUESTIONS)))
with col_c:
    target_level = st.select_slider("⚡ Difficulty", options=["Medium", "Hard", "Expert"])

# Filter Logic
pool = [q for q in QUESTIONS if 
        (target_comp == "All" or q["company"] == target_comp) and 
        (target_topic == "All" or q["topic"] == target_topic)]

if not pool:
    st.error("No questions match your elite filters. Try broadening your search.")
elif st.session_state.q_idx < len(pool):
    q = pool[st.session_state.q_idx]
    
    # UI Card
    st.markdown(f"### Question {st.session_state.q_idx + 1}")
    with st.container():
        st.info(f"**Company:** {q['company']} | **Difficulty:** {q['level']} | **Topic:** {q['topic']}")
        st.write(f"#### {q['question']}")
        
        user_choice = st.radio("Choose the correct option:", q["options"], key=f"choice_{st.session_state.q_idx}")

        if st.button("Validate Answer") or st.session_state.ans_submitted:
            st.session_state.ans_submitted = True
            if user_choice == q["answer"]:
                st.success("🎯 Correct! You're on track for selection.")
                if not any(entry.get('counted') for entry in [st.session_state] if 'counted' in st.session_state):
                    st.session_state.session_score += 1
            else:
                st.error(f"❌ Incorrect. The correct answer was: {q['answer']}")
            
            with st.expander("Master the Logic (Explanation)", expanded=True):
                st.write(q["explanation"])
                if "ratio" in q["explanation"].lower():
                    st.latex(r"Ratio = \frac{|Value_2 - Mean|}{|Mean - Value_1|}")

            if st.button("Next Challenge ➡"):
                st.session_state.q_idx += 1
                st.session_state.ans_submitted = False
                st.rerun()
else:
    st.balloons()
    score_pct = (st.session_state.session_score / len(pool)) * 100
    st.success(f"Session Complete! Accuracy: {score_pct}%")
    
    if st.button("Save to Career Profile"):
        user_data["history"].append({
            "date": str(date.today()),
            "score_pct": score_pct,
            "company": target_comp
        })
        save_data(user_data)
        st.session_state.q_idx = 0
        st.session_state.session_score = 0
        st.rerun()

# --- ANALYTICS TAB ---
st.divider()
st.subheader("📈 Detailed Performance Analysis")
if user_data["history"]:
    plot_df = pd.DataFrame(user_data["history"])
    fig = px.bar(plot_df, x="date", y="score_pct", color="company", barmode="group", title="Performance by Company")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Complete your first session to see your placement analytics.")
