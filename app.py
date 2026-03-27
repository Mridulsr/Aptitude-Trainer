import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date
import plotly.express as px

# --- DATABASE SETUP ---
DB_FILE = "user_stats.json"
QS_FILE = "questions.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"history": [], "last_login": None, "streak": 0}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

def load_questions():
    if os.path.exists(QS_FILE):
        with open(QS_FILE, "r") as f:
            return json.load(f)
    # Default seed data if file doesn't exist
    return [
        {"id": 1, "company": "Cognizant", "topic": "Alligation or Mixture", "question": "In what ratio must tea at Rs. 62/kg be mixed with tea at Rs. 72/kg so that the mixture must be worth Rs. 64.50/kg?", "options": ["3:1", "3:4", "4:3", "7:3"], "answer": "3:1", "explanation": "By Alligation: (72-64.5) : (64.5-62) = 7.5 : 2.5 = 3:1."},
        {"id": 2, "company": "TCS", "topic": "Profit and Loss", "question": "A person sold a stove for Rs. 423 and incurred a loss of 6%. At what price would it be sold to gain 8%?", "options": ["486", "525", "450", "490"], "answer": "486", "explanation": "94% of CP = 423. CP = 450. 108% of 450 = 486."},
        {"id": 3, "company": "Wipro", "topic": "Time and Work", "question": "A is thrice as efficient as B. Working together they finish a task in 24 days. In how many days can A alone finish it?", "options": ["32", "48", "24", "72"], "answer": "32", "explanation": "Ratio of efficiency A:B = 3:1. Total efficiency = 4. Total work = 24 * 4 = 96. A's time = 96/3 = 32 days."},
    ]

# --- APP CONFIG ---
st.set_page_config(page_title="AptiStreak Pro", layout="wide", page_icon="🎯")

# Initialize Data
user_data = load_data()
QUESTIONS = load_questions()
today = str(date.today())

# Streak Logic
if user_data.get("last_login") != today:
    yesterday = str(date.fromordinal(date.today().toordinal() - 1))
    if user_data.get("last_login") == yesterday:
        user_data["streak"] += 1
    else:
        user_data["streak"] = 1
    user_data["last_login"] = today
    save_data(user_data)

# --- SIDEBAR ---
st.sidebar.title("📊 Performance")
st.sidebar.metric("Current Streak", f"{user_data['streak']} Days", "🔥")

if user_data["history"]:
    df = pd.DataFrame(user_data["history"])
    st.sidebar.subheader("Recent Scores")
    fig = px.line(df.tail(10), x="date", y="score", markers=True, title="Last 10 Sessions")
    st.sidebar.plotly_chart(fig, use_container_width=True)

# --- MAIN UI ---
st.title("🎯 Company-wise Aptitude Practice")

# Session State Initialization
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.submitted = False

# Filters
c1, c2 = st.columns(2)
with c1:
    companies = ["All"] + sorted(list(set(q["company"] for q in QUESTIONS)))
    sel_company = st.selectbox("Select Company", companies)
with c2:
    topics = ["All"] + sorted(list(set(q["topic"] for q in QUESTIONS)))
    sel_topic = st.selectbox("Select Topic", topics)

# Filtering Logic
filtered_qs = [q for q in QUESTIONS if 
               (sel_company == "All" or q["company"] == sel_company) and 
               (sel_topic == "All" or q["topic"] == sel_topic)]

# Quiz Logic
if not filtered_qs:
    st.warning("No questions found for this selection.")
elif st.session_state.current_q < len(filtered_qs):
    q = filtered_qs[st.session_state.current_q]
    
    st.info(f"**Target:** {q['company']} | **Category:** {q['topic']}")
    st.subheader(f"Question {st.session_state.current_q + 1} of {len(filtered_qs)}")
    st.write(q["question"])

    choice = st.radio("Select an option:", q["options"], key=f"q_{st.session_state.current_q}")

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Submit", disabled=st.session_state.submitted):
            st.session_state.submitted = True
            if choice == q["answer"]:
                st.session_state.score += 1
            st.rerun()

    if st.session_state.submitted:
        if choice == q["answer"]:
            st.success("✔ Correct!")
        else:
            st.error(f"✖ Incorrect. The correct answer is {q['answer']}")
        
        with st.expander("View Detailed Explanation", expanded=True):
            st.write(q["explanation"])
            if q["topic"] == "Alligation or Mixture":
                st.markdown("**Rule of Alligation Formula:**")
                st.latex(r"\frac{\text{Cheaper Quantity}}{\text{Dearer Quantity}} = \frac{CP_{Dearer} - Mean}{Mean - CP_{Cheaper}}")

        if st.button("Next Question ➡"):
            st.session_state.current_q += 1
            st.session_state.submitted = False
            st.rerun()

else:
    st.balloons()
    st.success("Session Completed!")
    st.metric("Final Score", f"{st.session_state.score}/{len(filtered_qs)}")
    
    if st.button("Log Progress & Finish"):
        user_data["history"].append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"), 
            "score": st.session_state.score, 
            "total": len(filtered_qs)
        })
        save_data(user_data)
        # Reset for next session
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.rerun()

# --- ADMIN PANEL ---
st.write("---")
with st.expander("🛠 Admin: Add New Questions"):
    with st.form("admin_form", clear_on_submit=True):
        a_comp = st.text_input("Company Name")
        a_topic = st.text_input("Topic")
        a_q = st.text_area("Question")
        a_opts = st.text_input("Options (Comma separated)")
        a_ans = st.text_input("Correct Answer (Exactly as written in options)")
        a_exp = st.text_area("Explanation")
        
        if st.form_submit_button("Add to Database"):
            new_entry = {
                "id": len(QUESTIONS) + 1,
                "company": a_comp,
                "topic": a_topic,
                "question": a_q,
                "options": [o.strip() for o in a_opts.split(",")],
                "answer": a_ans.strip(),
                "explanation": a_exp
            }
            QUESTIONS.append(new_entry)
            with open(QS_FILE, "w") as f:
                json.dump(QUESTIONS, f, indent=4)
            st.success("Question Bank Updated!")
