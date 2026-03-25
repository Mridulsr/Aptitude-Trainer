import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date
import plotly.express as px

# --- EXPANDED DATASET (TCS, COGNIZANT, WIPRO) ---
# Sourced from a2zinterviews logic
# Replace the old QUESTIONS list with this:
def load_all_questions():
    if os.path.exists("questions.json"):
        with open("questions.json", "r") as f:
            return json.load(f)
    return []

QUESTIONS = load_all_questions()
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

# --- ADMIN PANEL FOR UPLOADING ---
st.write("---")
with st.expander("🛠 Admin: Upload New Question"):
    with st.form("upload_form", clear_on_submit=True):
        u_company = st.selectbox("Company", ["TCS", "Cognizant", "Wipro", "Infosys", "Other"])
        u_topic = st.selectbox("Topic", ["Alligation or Mixture", "Profit and Loss", "Time and Work"])
        u_q = st.text_area("Question Text")
        u_opt = st.text_input("Options (comma-separated, e.g., A, B, C, D)")
        u_ans = st.text_input("Correct Answer (must match one option exactly)")
        u_exp = st.text_area("Explanation")
        
        if st.form_submit_button("Save to Question Bank"):
            new_q = {
                "id": len(QUESTIONS) + 1,
                "company": u_company,
                "topic": u_topic,
                "question": u_q,
                "options": [opt.strip() for opt in u_opt.split(",")],
                "answer": u_ans,
                "explanation": u_exp
            }
            # Add to local list and save to file
            QUESTIONS.append(new_q)
            with open("questions.json", "w") as f:
                json.dump(QUESTIONS, f, indent=4)
            st.success("New question added to the database!")
