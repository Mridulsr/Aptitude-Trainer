# ⚡ AptiStreak - Daily Aptitude & Coding Practice Tracker

AptiStreak is a Streamlit-based web application designed to help students and job seekers crack corporate placement exams (TCS, Infosys, Wipro, Accenture, Cognizant, Amazon, Google, etc.). It features an interactive quiz dashboard across multiple difficulty levels, tracks daily practice streaks using a persistent SQLite backend, and visualizes preparation metrics.

## 🚀 Live Demo
🔗 **Access the live web app here:** [AptiStreak Live Dashboard](https://aptitude-trainer-ww52k5fca9njn9axqvacjp.streamlit.app/)

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
├── .devcontainer/         # Codespaces and docker container environment setup
├── app.py                 # Main Streamlit UI and app gateway
├── db_manager.py          # Database operations handler & connection abstraction
├── setup_db.py            # Initialization script to build initial database schemas
├── find_my_db.py          # Diagnostic utility to track the localized database path
├── fix.py                 # Schema maintenance or data patch utility script
├── requirements.txt       # Project python dependencies
└── README.md              # Project documentation
