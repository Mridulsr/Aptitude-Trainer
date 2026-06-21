Link https://aptitude-trainer-ww52k5fca9njn9axqvacjp.streamlit.app/
# ⚡ AptiStreak - Daily Aptitude & Coding Practice Tracker

AptiStreak is a Streamlit-based web application designed to help students and job seekers crack corporate placement exams (TCS, Infosys, Wipro, Accenture, Cognizant, Amazon, Google, etc.). It features an interactive quiz dashboard across multiple difficulty levels, tracks daily practice streaks using a persistent SQLite backend, and visualizes preparation metrics.

## 🚀 Live Demo
🔗 **Deploy your app to Streamlit Community Cloud and paste the link here!** e.g., [https://aptistreak.streamlit.app](https://aptistreak.streamlit.app)

---

## ✨ Features
* **Company-Specific Targeting:** Practice questions curated specifically from papers by TCS, Infosys, Wipro, Accenture, Cognizant, Google, Amazon, and more.
* **Comprehensive Topic Coverage:** Organized into fields like Arithmetic, Logical Reasoning, Data Interpretation, Verbal Ability, and Programming Logic.
* **Smart Streak Tracking:** Keeps you accountable by increasing your streak every calendar day you log in and practice.
* **Performance Logs & History:** Automatically logs quiz performance into a localized SQLite database (`aptistreak.db`).
* **Visual Analytics:** Interactive dashboards driven by Plotly to track your progress over time.

---

## 🛠️ Tech Stack
* **Frontend Dashboard:** Streamlit
* **Data Visualization:** Plotly Express
* **Database Backend:** SQLite3 (Self-contained file-based storage)
* **Data Manipulation:** Pandas

---

## 📂 Project Structure
```text
aptistreak/
│
├── app.py                 # Main Streamlit application file
├── aptistreak.db          # SQLite Database (Auto-generated on first run)
├── requirements.txt       # Project python dependencies
└── README.md              # Project documentation
