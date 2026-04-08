import streamlit as st
import pandas as pd
import json
import os
from datetime import date
import plotly.express as px

# --- 1. THE COMPLETE DATASET ---
# CRITICAL: Ensure every { } block ends with a comma, and the final list ends with ]
QUESTIONS = [
    {"id": 209, "company": "Cognizant", "topic": "Data Interpretation", "level": "Hard", "question": "Sales Jan: 100, Feb: 120, Mar: 110. Average?", "options": ["100", "110", "120", "115"], "answer": "110", "explanation": "330/3 = 110."},
    {"id": 102, "company": "TCS", "topic": "Arithmetic", "level": "Easy", "question": "The sum of two numbers is 25 and their difference is 13. Find their product.", "options": ["104", "114", "315", "325"], "answer": "114", "explanation": "x+y=25, x-y=13. Adding gives 2x=38, x=19. Then y=6. Product = 19*6 = 114."},
    {"id": 103, "company": "TCS", "topic": "Arithmetic", "level": "Medium", "question": "What is the remainder when 2^31 is divided by 7?", "options": ["1", "2", "3", "4"], "answer": "2", "explanation": "2^3 = 8. 8/7 leaves remainder 1. (2^3)^10 * 2^1 = 1^10 * 2 = 2."},
    {"id": 104, "company": "TCS", "topic": "Programming Logic", "level": "Hard", "question": "In C, what is the output of printf('%d', 10 ? 0 ? 5 : 11 : 12);?", "options": ["10", "0", "11", "12"], "answer": "11", "explanation": "Nested ternary: 10 is true, so it evaluates (0 ? 5 : 11). 0 is false, so it results in 11."},
    {"id": 105, "company": "TCS", "topic": "Arithmetic", "level": "Advanced", "question": "A sum of money amounts to Rs. 6690 after 3 years and to Rs. 10035 after 6 years on compound interest. Find the sum.", "options": ["4460", "4400", "4500", "4660"], "answer": "4460", "explanation": "Ratio = 10035/6690 = 1.5. P * (1.5) = 6690. P = 4460."},
    {"id": 106, "company": "Cognizant", "topic": "Logical", "level": "Easy", "question": "If FISH is coded as EHRG, what is the code for JUNGLE?", "options": ["ITMFKD", "ITMFLD", "KVOHMF", "TIMFKD"], "answer": "ITMFKD", "explanation": "Each letter shifted backward by 1."},
    {"id": 111, "company": "Wipro", "topic": "Arithmetic", "level": "Medium", "question": "A can do work in 15 days, B in 20. Work together for 4 days. Fraction left?", "options": ["7/15", "8/15", "11/15", "1/4"], "answer": "8/15", "explanation": "1 day = 7/60. 4 days = 7/15. Left = 1 - 7/15 = 8/15."},
    {"id": 117, "company": "Infosys", "topic": "Puzzle", "level": "Hard", "question": "8 identical coins, 1 is fake (lighter). Min weighings to find it?", "options": ["2", "3", "4", "8"], "answer": "2", "explanation": "Group 3-3-2. First weighing narrow it to a group of 3 or 2. Second confirms."},
    {"id": 16, "company": "Amazon", "topic": "Profit and Loss", "level": "Hard", "question": "If SP is doubled, profit triples. Find profit %.", "options": ["66.66%", "100%", "105%", "120%"], "answer": "100%", "explanation": "3(y-x) = 2y-x => y=2x. Profit = 100%."},
    {"id": 18, "company": "Google", "topic": "Surds and Indices", "level": "Hard", "question": "If (1/5)^3y = 0.008, find (0.25)^y", "options": ["0.25", "0.5", "0.625", "1"], "answer": "0.25", "explanation": "y=1. (0.25)^1 = 0.25."},
    # --- PASTE ALL YOUR OTHER 200+ QUESTIONS BELOW THIS LINE ---
    
]

# --- 2. STORAGE ENGINE ---
def load_perf():
    if os.path.exists("stats.json"):
        with open("stats.json", "r") as f: return json.load(f)
    return {"streak": 0, "last_active": "", "history": []}

def save_perf(data):
    with open("stats.json", "w") as f: json.dump(data, f)

# --- 3. APP CONFIG ---
st.set_page_config(page_title="AptiStreak Pro 2026", layout="wide")
user_stats = load_perf()

# Streak logic
today = str(date.today())
if user_stats["last_active"] != today:
    user_stats["streak"] += 1
    user_stats["last_active"] = today
    save_perf(user_stats)

# --- 4. NAVIGATION ---
with st.sidebar:
    st.title(f"🔥 Streak: {user_stats['streak']} Days")
    st.divider()
    
    # 1. Company Filter
    comps = sorted(list(set(q["company"] for q in QUESTIONS)))
    sel_comp = st.selectbox("🎯 Target Company", comps)
    
    # 2. Topic Filter (Dynamic)
    comp_qs = [q for q in QUESTIONS if q["company"] == sel_comp]
    topics = sorted(list(set(q["topic"] for q in comp_qs)))
    sel_topic = st.selectbox("📚 Topic", ["All"] + topics)
    
    # 3. Difficulty Filter
    sel_level = st.select_slider("⚡ Difficulty", options=["Easy", "Medium", "Hard", "Advanced"])

# Final Pool Selection
final_pool = [q for q in comp_qs if 
              (sel_topic == "All" or q["topic"] == sel_topic) and 
              (q["level"] == sel_level)]

# --- 5. QUIZ UI ---
st.title(f"🚀 {sel_comp} Placement Drive")

if not final_pool:
    st.info(f"No {sel_level} level questions available for {sel_topic} yet.")
else:
    if 'q_no' not in st.session_state: st.session_state.q_no = 0
    
    curr_q = final_pool[st.session_state.q_no % len(final_pool)]
    
    st.info(f"Topic: {curr_q['topic']} | Difficulty: {curr_q['level']}")
    st.write(f"### {curr_q['question']}")
    
    choice = st.radio("Options:", curr_q["options"], key=f"rad_{curr_q['id']}")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Submit"):
            if choice == curr_q["answer"]:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Wrong! Correct: {curr_q['answer']}")
            with st.expander("Explanation"):
                st.write(curr_q["explanation"])
                if "P(" in curr_q["explanation"]:
                    st.latex(r"A = P(1 + \frac{R}{100})^t")
                    
    with col2:
        if st.button("Next ➡"):
            st.session_state.q_no += 1
            st.rerun()

# --- 6. ANALYTICS ---
st.divider()
st.subheader("📈 Your Journey")
if user_stats["history"]:
    df = pd.DataFrame(user_stats["history"])
    st.plotly_chart(px.line(df, x="date", y="score"), use_container_width=True)
else:
    st.caption("Complete a full set to see your progress graph here.")
