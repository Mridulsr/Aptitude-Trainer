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
  {"id": 1, "company": "TCS", "topic": "Arithmetic", "level": "Easy", "question": "What is the unit digit in (7^95 - 3^58)?", "options": ["0", "4", "6", "7"], "answer": "4", "explanation": "7^95: 95/4 rem 3, 7^3 ends in 3. 3^58: 58/4 rem 2, 3^2 ends in 9. 13 - 9 = 4."},
  {"id": 2, "company": "Cognizant", "topic": "Logical", "level": "Medium", "question": "Pointing to a photograph, a man said, 'I have no brother or sister but that man's father is my father's son.' Whose photograph was it?", "options": ["His own", "His son's", "His father's", "His nephew's"], "answer": "His son's", "explanation": "'My father's son' is the man himself. So, the man in the photo's father is the speaker. It's his son."},
  {"id": 3, "company": "Wipro", "topic": "Arithmetic", "level": "Hard", "question": "A train covers a distance in 50 minutes if it runs at 48kmph. At what speed must it run to reduce time to 40 mins?", "options": ["50 kmph", "55 kmph", "60 kmph", "64 kmph"], "answer": "60 kmph", "explanation": "Dist = Speed * Time = 48 * (50/60) = 40km. New Speed = 40 / (40/60) = 60 kmph."},
  {"id": 4, "company": "TCS", "topic": "Verbal", "level": "Easy", "question": "Find the correctly spelt word:", "options": ["Efficient", "Eficient", "Efficeint", "Efficent"], "answer": "Efficient", "explanation": "The correct spelling is Efficient."},
  {"id": 5, "company": "Infosys", "topic": "Arithmetic", "level": "Medium", "question": "The ages of two persons A and B are in the ratio 5:7. 18 years ago, the ratio was 8:13. Find their present ages.", "options": ["50, 70", "40, 56", "60, 84", "45, 63"], "answer": "50, 70", "explanation": "(5x-18)/(7x-18) = 8/13. 65x - 234 = 56x - 144. 9x = 90. x = 10. Ages are 50 and 70."},
  {"id": 6, "company": "Accenture", "topic": "Arithmetic", "level": "Hard", "question": "A sum of money at compound interest amounts to thrice itself in 3 years. In how many years will it be 9 times itself?", "options": ["6", "9", "12", "15"], "answer": "6", "explanation": "3^1 in 3 years. 9 is 3^2. Time = 3 * 2 = 6 years."},
  {"id": 7, "company": "TCS", "topic": "Logical", "level": "Easy", "question": "Find the odd one out: 3, 5, 11, 14, 17, 21", "options": ["14", "17", "21", "3"], "answer": "14", "explanation": "All others are odd numbers. 14 is even."},
  {"id": 8, "company": "Cognizant", "topic": "Arithmetic", "level": "Medium", "question": "How many seconds will a 150m long train take to cross a pole if it's running at 54 kmph?", "options": ["5 sec", "10 sec", "12 sec", "15 sec"], "answer": "10 sec", "explanation": "Speed = 54 * 5/18 = 15 m/s. Time = 150/15 = 10 sec."},
  {"id": 9, "company": "Wipro", "topic": "Arithmetic", "level": "Medium", "question": "A sum of Rs 12,500 amounts to Rs 15,500 in 4 years at simple interest. What is the rate?", "options": ["3%", "4%", "5%", "6%"], "answer": "6%", "explanation": "SI = 3000. R = (3000 * 100) / (12500 * 4) = 6%."},
  {"id": 10, "company": "Infosys", "topic": "Logical", "level": "Hard", "question": "In a certain code 'TIGER' is written as 'QDFHS'. How is 'FISH' written?", "options": ["GRHE", "HRGF", "GSHE", "GHRE"], "answer": "GRHE", "explanation": "Reverse the word and subtract 1 from each letter: R-1=Q, E-1=D, G-1=F..."},
  {"id": 11, "company": "Accenture", "topic": "Arithmetic", "level": "Easy", "question": "If x:y = 3:4, find (5x-2y)/(7x+2y).", "options": ["7/29", "1/3", "2/5", "5/12"], "answer": "7/29", "explanation": "Put x=3, y=4. (15-8)/(21+8) = 7/29."},
  {"id": 12, "company": "TCS", "topic": "Data Interpretation", "level": "Medium", "question": "What is 25% of 25% of 100?", "options": ["6.25", "0.625", "62.5", "25"], "answer": "6.25", "explanation": "0.25 * 0.25 * 100 = 6.25."},
  {"id": 13, "company": "Cognizant", "topic": "Arithmetic", "level": "Hard", "question": "The difference between SI and CI on Rs. 5000 for 2 years at 10% is:", "options": ["Rs. 25", "Rs. 50", "Rs. 75", "Rs. 100"], "answer": "Rs. 50", "explanation": "Diff = P(R/100)^2 = 5000 * (10/100)^2 = 50."},
  {"id": 14, "company": "Wipro", "topic": "Verbal", "level": "Easy", "question": "Antonym of 'ENORMOUS':", "options": ["Soft", "Tiny", "Weak", "Average"], "answer": "Tiny", "explanation": "Enormous means huge, antonym is tiny."},
  {"id": 15, "company": "Infosys", "topic": "Arithmetic", "level": "Medium", "question": "Find the HCF of 2/3, 8/9, 64/81.", "options": ["2/81", "2/3", "8/81", "1/3"], "answer": "2/81", "explanation": "HCF of fractions = HCF(Numerators)/LCM(Denominators) = HCF(2,8,64)/LCM(3,9,81) = 2/81."},
  {"id": 16, "company": "TCS", "topic": "Arithmetic", "level": "Hard", "question": "A can finish a work in 18 days and B can do the same work in 15 days. B worked for 10 days and left. In how many days can A finish the remaining work?", "options": ["5", "6", "8", "10"], "answer": "6", "explanation": "B's 10 day work = 10/15 = 2/3. Remaining = 1/3. A's time = 1/3 * 18 = 6 days."},
  {"id": 17, "company": "Cognizant", "topic": "Logical", "level": "Medium", "question": "Look at the series: 7, 10, 8, 11, 9, 12, ... What number should come next?", "options": ["7", "10", "12", "13"], "answer": "10", "explanation": "Pattern: +3, -2, +3, -2. 12-2 = 10."},
  {"id": 18, "company": "Wipro", "topic": "Arithmetic", "level": "Easy", "question": "Find the average of first 40 natural numbers.", "options": ["20", "20.5", "21", "21.5"], "answer": "20.5", "explanation": "Sum = n(n+1)/2. Avg = (n+1)/2 = 41/2 = 20.5."},
  {"id": 19, "company": "Infosys", "topic": "Arithmetic", "level": "Hard", "question": "In how many ways can the letters of 'LEADER' be arranged?", "options": ["72", "144", "360", "720"], "answer": "360", "explanation": "6 letters, E repeats twice. 6!/2! = 720/2 = 360."},
  {"id": 20, "company": "TCS", "topic": "Arithmetic", "level": "Medium", "question": "A vendor bought toffees at 6 for a rupee. How many for a rupee must he sell to gain 20%?", "options": ["3", "4", "5", "6"], "answer": "5", "explanation": "CP of 1 = 1/6. SP for 20% gain = 1/6 * 1.2 = 1/5. So 5 for a rupee."},
  {"id": 21, "company": "Cognizant", "topic": "Verbal", "level": "Easy", "question": "Synonym of 'ABANDON':", "options": ["Forsake", "Keep", "Cherish", "Enlarge"], "answer": "Forsake", "explanation": "To abandon is to leave or forsake."},
  {"id": 22, "company": "Wipro", "topic": "Logical", "level": "Hard", "question": "If 'A + B' means A is brother of B, 'A - B' means A is sister of B, what means 'M is uncle of P'?", "options": ["M+N-P", "M-N+P", "M+N+P", "None"], "answer": "None", "explanation": "Uncle requires a generation gap, which '+' and '-' do not provide here."},
  {"id": 23, "company": "Infosys", "topic": "Arithmetic", "level": "Medium", "question": "A man crosses a 600m long street in 5 mins. What is his speed in km/hr?", "options": ["3.6", "7.2", "8.4", "10"], "answer": "7.2", "explanation": "Speed = 600/300 = 2 m/s. 2 * 18/5 = 7.2 km/hr."},
  {"id": 24, "company": "Accenture", "topic": "Arithmetic", "level": "Easy", "question": "What is the cube root of 1331?", "options": ["11", "13", "17", "19"], "answer": "11", "explanation": "11 * 11 * 11 = 1331."},
  {"id": 25, "company": "TCS", "topic": "Arithmetic", "level": "Hard", "question": "Pipe A can fill a tank in 20 mins and Pipe B in 30 mins. Both are opened, but after 8 mins B is closed. How much more time to fill?", "options": ["6.6 mins", "4.6 mins", "12 mins", "8 mins"], "answer": "6.6 mins", "explanation": "1 min work = 1/20+1/30 = 5/60 = 1/12. In 8 mins = 8/12 = 2/3 filled. Left 1/3. A takes (1/3)*20 = 6.66 mins."},
  {"id": 26, "company": "Cognizant", "topic": "Arithmetic", "level": "Medium", "question": "Find the compound interest on Rs. 10,000 for 2 years at 4% per annum.", "options": ["Rs. 800", "Rs. 816", "Rs. 832", "Rs. 848"], "answer": "Rs. 816", "explanation": "Amount = 10000(1.04)^2 = 10816. CI = 816."},
  {"id": 27, "company": "Wipro", "topic": "Logical", "level": "Easy", "question": "SCD, TEF, UGH, ____, WKL", "options": ["CMN", "UJI", "VIJ", "IJT"], "answer": "VIJ", "explanation": "First letters: S,T,U,V,W. Second/Third: CD, EF, GH, IJ, KL."},
  {"id": 28, "company": "Infosys", "topic": "Arithmetic", "level": "Medium", "question": "A sum was put at SI at a certain rate for 3 years. Had it been put at 2% higher rate, it would have fetched Rs 360 more. Find sum.", "options": ["4000", "5000", "6000", "7000"], "answer": "6000", "explanation": "3 * 2% = 6%. 6% of Sum = 360. Sum = 360/0.06 = 6000."},
  {"id": 29, "company": "TCS", "topic": "Arithmetic", "level": "Hard", "question": "If log 27 = 1.431, then log 9 is:", "options": ["0.934", "0.945", "0.954", "0.958"], "answer": "0.954", "explanation": "log 27 = 3 log 3 = 1.431 => log 3 = 0.477. log 9 = 2 log 3 = 0.954."},
  {"id": 30, "company": "Cognizant", "topic": "Logical", "level": "Easy", "question": "Marathon is to race as hibernation is to:", "options": ["Winter", "Bear", "Sleep", "Dream"], "answer": "Sleep", "explanation": "Marathon is a long race; Hibernation is a long sleep."},
  {"id": 31, "company": "Wipro", "topic": "Arithmetic", "level": "Medium", "question": "The probability of getting a total of 7 in a single throw of two dice is:", "options": ["1/6", "1/4", "2/3", "3/4"], "answer": "1/6", "explanation": "Pairs: (1,6), (6,1), (2,5), (5,2), (3,4), (4,3). Total 6/36 = 1/6."},
  {"id": 32, "company": "Infosys", "topic": "Verbal", "level": "Easy", "question": "Choose the word which is least like others:", "options": ["Zebra", "Lion", "Tiger", "Horse"], "answer": "Horse", "explanation": "Horse is a domestic animal; others are wild."},
  {"id": 33, "company": "Accenture", "topic": "Arithmetic", "level": "Medium", "question": "The ratio of three numbers is 1:2:3 and their HCF is 12. The numbers are:", "options": ["12, 24, 36", "10, 20, 30", "12, 24, 48", "24, 48, 72"], "answer": "12, 24, 36", "explanation": "Numbers = 12*1, 12*2, 12*3."},
  {"id": 34, "company": "TCS", "topic": "Arithmetic", "level": "Hard", "question": "Find the area of a triangle whose sides are 13, 14, 15.", "options": ["84", "64", "74", "94"], "answer": "84", "explanation": "s = (13+14+15)/2 = 21. Area = sqrt(21*8*7*6) = 84."},
  {"id": 35, "company": "Cognizant", "topic": "Logical", "level": "Medium", "question": "Cup is to lip as bird is to:", "options": ["Bush", "Grass", "Forest", "Beak"], "answer": "Beak", "explanation": "You drink from a cup with lips; a bird eats/picks with a beak."},
  {"id": 36, "company": "Wipro", "topic": "Arithmetic", "level": "Easy", "question": "Find the value of 1.13 + 0.007 + 3.1", "options": ["4.237", "4.24", "4.3", "4.37"], "answer": "4.237", "explanation": "Simple addition."},
  {"id": 37, "company": "Infosys", "topic": "Arithmetic", "level": "Hard", "question": "A bag contains 2 red, 3 green and 2 blue balls. Two balls are drawn at random. What is the probability that none of the balls drawn is blue?", "options": ["10/21", "11/21", "2/7", "5/7"], "answer": "10/21", "explanation": "Total = 7. Non-blue = 5. Prob = 5C2 / 7C2 = 10 / 21."},
  {"id": 38, "company": "Accenture", "topic": "Verbal", "level": "Easy", "question": "Find the correctly spelt word:", "options": ["Calendar", "Calender", "Colendar", "Calander"], "answer": "Calendar", "explanation": "Correct spelling is Calendar."},
  {"id": 39, "company": "TCS", "topic": "Arithmetic", "level": "Medium", "question": "The cost price of 20 articles is the same as the selling price of x articles. If the profit is 25%, find x.", "options": ["15", "16", "18", "25"], "answer": "16", "explanation": "(20-x)/x * 100 = 25. 20-x = 0.25x. 1.25x = 20. x = 16."},
  {"id": 40, "company": "Cognizant", "topic": "Logical", "level": "Hard", "question": "If 1st Oct is Sunday, then 1st Nov will be:", "options": ["Monday", "Tuesday", "Wednesday", "Thursday"], "answer": "Wednesday", "explanation": "Oct has 31 days. 31/7 leaves remainder 3. Sunday + 3 days = Wednesday."}
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
