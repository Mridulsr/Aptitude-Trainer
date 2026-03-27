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
  {"id": 41, "company": "TCS", "topic": "Arithmetic", "level": "Medium", "question": "What is the probability of getting at least one head when three coins are tossed simultaneously?", "options": ["1/8", "3/8", "5/8", "7/8"], "answer": "7/8", "explanation": "Total outcomes = 2^3 = 8. Outcome with no heads (all tails) = 1. At least one head = 1 - (1/8) = 7/8."},
  {"id": 42, "company": "Cognizant", "topic": "Logical", "level": "Easy", "question": "In a certain code, 'ROAD' is written as 'URDG'. How is 'SWAN' written in that code?", "options": ["VXDQ", "VZDQ", "VZDP", "UXDQ"], "answer": "VZDQ", "explanation": "Each letter is shifted 3 places forward: R+3=U, O+3=R, A+3=D, D+3=G. Similarly, S+3=V, W+3=Z, A+3=D, N+3=Q."},
  {"id": 43, "company": "Wipro", "topic": "Arithmetic", "level": "Medium", "question": "A sum of money doubles itself in 10 years at simple interest. What is the rate of interest?", "options": ["5%", "10%", "12%", "15%"], "answer": "10%", "explanation": "Let P = 100. Amount = 200, so SI = 100. R = (100 * 100) / (100 * 10) = 10%."},
  {"id": 44, "company": "Infosys", "topic": "Verbal", "level": "Medium", "question": "Choose the word which is most opposite in meaning to 'VAGUE':", "options": ["Clear", "Dull", "Unknown", "Shady"], "answer": "Clear", "explanation": "Vague means unclear or uncertain; the opposite is Clear."},
  {"id": 45, "company": "Accenture", "topic": "Arithmetic", "level": "Hard", "question": "If 2^x = 4^y = 8^z and 1/2x + 1/4y + 1/6z = 24/7, find z.", "options": ["7/16", "7/32", "7/48", "7/64"], "answer": "7/48", "explanation": "2^x = 2^2y = 2^3z => x=3z, 2y=3z. Substitute in equation: 1/6z + 1/6z + 1/6z = 3/6z = 1/2z = 24/7. So z = 7/48."},
  {"id": 46, "company": "TCS", "topic": "Arithmetic", "level": "Easy", "question": "The L.C.M. of two numbers is 48. The numbers are in the ratio 2 : 3. The sum of the numbers is:", "options": ["28", "32", "40", "64"], "answer": "40", "explanation": "Let numbers be 2x and 3x. LCM = 6x = 48 => x=8. Numbers are 16 and 24. Sum = 40."},
  {"id": 47, "company": "Cognizant", "topic": "Logical", "level": "Hard", "question": "If 'P + Q' means P is the mother of Q; 'P - Q' means P is the father of Q; 'P * Q' means P is the brother of Q. Which of the following means 'A is the uncle of B'?", "options": ["A * C - B", "A - C * B", "A + C * B", "None"], "answer": "A * C - B", "explanation": "A * C means A is brother of C. C - B means C is father of B. Thus, A is father's brother (Uncle) of B."},
  {"id": 48, "company": "Wipro", "topic": "Arithmetic", "level": "Medium", "question": "A can do a work in 15 days and B in 20 days. If they work on it together for 4 days, then the fraction of the work that is left is:", "options": ["1/4", "1/10", "7/15", "8/15"], "answer": "8/15", "explanation": "1 day work = 1/15 + 1/20 = 7/60. 4 days work = 28/60 = 7/15. Left = 1 - 7/15 = 8/15."},
  {"id": 49, "company": "Infosys", "topic": "Arithmetic", "level": "Easy", "question": "What is 15 percent of 34 kg?", "options": ["3.4 kg", "3.75 kg", "4.5 kg", "5.1 kg"], "answer": "5.1 kg", "explanation": "(15/100) * 34 = 5.1."},
  {"id": 50, "company": "Accenture", "topic": "Logical", "level": "Medium", "question": "Find the missing number in the sequence: 4, 9, 16, 25, 36, ?", "options": ["40", "45", "49", "64"], "answer": "49", "explanation": "The sequence consists of squares of consecutive numbers: 2^2, 3^2, 4^2, 5^2, 6^2. Next is 7^2 = 49."},
  {"id": 51, "company": "TCS", "topic": "Arithmetic", "level": "Hard", "question": "A mixture contains alcohol and water in the ratio 4 : 3. If 5 liters of water is added to the mixture, the ratio becomes 4 : 5. Find the quantity of alcohol in the mixture.", "options": ["10 liters", "12 liters", "15 liters", "18 liters"], "answer": "10 liters", "explanation": "Let alcohol be 4x, water 3x. 4x/(3x+5) = 4/5 => 20x = 12x + 20 => 8x = 20 => x = 2.5. Alcohol = 4 * 2.5 = 10."},
  {"id": 52, "company": "Cognizant", "topic": "Verbal", "level": "Easy", "question": "Identify the synonym for 'CANDID':", "options": ["Deceptive", "Frank", "Vague", "Arrogant"], "answer": "Frank", "explanation": "Candid means truthful and straightforward; Frank is the synonym."},
  {"id": 53, "company": "Wipro", "topic": "Arithmetic", "level": "Medium", "question": "The ratio between the speeds of two trains is 7 : 8. If the second train runs 400 km in 4 hours, then the speed of the first train is:", "options": ["70 kmph", "75 kmph", "84 kmph", "87.5 kmph"], "answer": "87.5 kmph", "explanation": "Speed of 2nd train = 400/4 = 100 kmph. 8 units = 100 => 1 unit = 12.5. 7 units = 7 * 12.5 = 87.5 kmph."},
  {"id": 54, "company": "Infosys", "topic": "Arithmetic", "level": "Hard", "question": "In how many ways can a committee of 5 members be formed from 6 men and 4 women such that it contains at least 3 men?", "options": ["162", "186", "200", "210"], "answer": "186", "explanation": "(6C3 * 4C2) + (6C4 * 4C1) + (6C5 * 4C0) = (20 * 6) + (15 * 4) + (6 * 1) = 120 + 60 + 6 = 186."},
  {"id": 55, "company": "Accenture", "topic": "Arithmetic", "level": "Easy", "question": "A shopkeeper sells an item at a profit of 20%. If he bought it for Rs. 60, what is the selling price?", "options": ["Rs. 70", "Rs. 72", "Rs. 75", "Rs. 80"], "answer": "Rs. 72", "explanation": "SP = 120% of 60 = 1.2 * 60 = 72."},
  {"id": 56, "company": "TCS", "topic": "Logical", "level": "Medium", "question": "Find the odd one out: 27, 64, 125, 144, 216", "options": ["27", "64", "144", "216"], "answer": "144", "explanation": "All others are cubes (3^3, 4^3, 5^3, 6^3). 144 is a square (12^2)."},
  {"id": 57, "company": "Cognizant", "topic": "Arithmetic", "level": "Hard", "question": "A sum of money invested at compound interest amounts to Rs. 4624 in 2 years and Rs. 4913 in 3 years. The rate of interest is:", "options": ["6.25%", "5%", "8%", "4.5%"], "answer": "6.25%", "explanation": "Rate = [(4913 - 4624) / 4624] * 100 = (289 / 4624) * 100 = 6.25%."},
  {"id": 58, "company": "Wipro", "topic": "Verbal", "level": "Easy", "question": "Which of these is the correct antonym for 'ARROGANT'?", "options": ["Proud", "Humble", "Selfish", "Vain"], "answer": "Humble", "explanation": "Arrogant means having an exaggerated sense of self-importance; Humble is the opposite."},
  {"id": 59, "company": "Infosys", "topic": "Arithmetic", "level": "Medium", "question": "Two numbers are in the ratio 3 : 5. If 9 is subtracted from each, the new ratio becomes 12 : 23. The smaller number is:", "options": ["27", "33", "49", "55"], "answer": "33", "explanation": "(3x-9)/(5x-9) = 12/23 => 69x - 207 = 60x - 108 => 9x = 99 => x = 11. Smaller number = 3 * 11 = 33."},
  {"id": 60, "company": "Accenture", "topic": "Logical", "level": "Easy", "question": "If Z = 52 and ACT = 48, then BAT will be equal to:", "options": ["39", "41", "44", "46"], "answer": "46", "explanation": "Letter positions are doubled: Z(26)*2=52. ACT: (1+3+20)*2=48. BAT: (2+1+20)*2=46."},
  {"id": 61, "company": "TCS", "topic": "Arithmetic", "level": "Medium", "question": "What is the unit digit in (3^65 * 6^59 * 7^71)?", "options": ["1", "2", "4", "6"], "answer": "4", "explanation": "3^65: 65/4 rem 1, ends in 3. 6^59 ends in 6. 7^71: 71/4 rem 3, ends in 3. 3 * 6 * 3 = 54, so unit digit is 4."},
  {"id": 62, "company": "Cognizant", "topic": "Arithmetic", "level": "Easy", "question": "Find the average of first five prime numbers.", "options": ["5.2", "5.6", "5.8", "6.2"], "answer": "5.6", "explanation": "Primes: 2, 3, 5, 7, 11. Sum = 28. Average = 28/5 = 5.6."},
  {"id": 63, "company": "Wipro", "topic": "Arithmetic", "level": "Hard", "question": "A boat can travel with a speed of 13 km/hr in still water. If the speed of the stream is 4 km/hr, find the time taken by the boat to go 68 km downstream.", "options": ["2 hours", "3 hours", "4 hours", "5 hours"], "answer": "4 hours", "explanation": "Downstream speed = 13 + 4 = 17 km/hr. Time = 68 / 17 = 4 hours."},
  {"id": 64, "company": "Infosys", "topic": "Logical", "level": "Medium", "question": "Look at this series: J14, L16, __, P20, R22. What should fill the blank?", "options": ["S24", "N18", "M18", "T24"], "answer": "N18", "explanation": "Letters skip one (J, L, N, P, R). Numbers increase by 2 (14, 16, 18, 20, 22)."},
  {"id": 65, "company": "Accenture", "topic": "Arithmetic", "level": "Medium", "question": "If a quarter kg of potato costs 60 paise, how many paise will 200 gm cost?", "options": ["48 paise", "54 paise", "56 paise", "60 paise"], "answer": "48 paise", "explanation": "250g = 60p => 1g = 60/250. 200g = (60/250) * 200 = 48 paise."},
  {"id": 66, "company": "TCS", "topic": "Arithmetic", "level": "Hard", "question": "A cistern is normally filled in 8 hours but takes two hours longer to fill because of a leak in its bottom. If the cistern is full, the leak will empty it in:", "options": ["20 hrs", "40 hrs", "45 hrs", "50 hrs"], "answer": "40 hrs", "explanation": "Fill rate = 1/8. Rate with leak = 1/10. Leak rate = 1/8 - 1/10 = 1/40. So 40 hours."},
  {"id": 67, "company": "Cognizant", "topic": "Verbal", "level": "Medium", "question": "Select the correct spelling:", "options": ["Mantenance", "Maintenance", "Maintenence", "Maintainance"], "answer": "Maintenance", "explanation": "The correct spelling is Maintenance."},
  {"id": 68, "company": "Wipro", "topic": "Logical", "level": "Easy", "question": "Which word does NOT belong with the others?", "options": ["Index", "Glossary", "Chapter", "Book"], "answer": "Book", "explanation": "Index, Glossary, and Chapter are parts of a book; Book is the whole."},
  {"id": 69, "company": "Infosys", "topic": "Arithmetic", "level": "Medium", "question": "A sum of money at simple interest amounts to Rs. 815 in 3 years and to Rs. 854 in 4 years. The sum is:", "options": ["Rs. 650", "Rs. 690", "Rs. 698", "Rs. 700"], "answer": "Rs. 698", "explanation": "SI for 1 year = 854 - 815 = 39. SI for 3 years = 39 * 3 = 117. Principal = 815 - 117 = 698."},
  {"id": 70, "company": "Accenture", "topic": "Arithmetic", "level": "Easy", "question": "The speed of a car is 90 km/hr. What is its speed in meters per second?", "options": ["20 m/s", "25 m/s", "30 m/s", "35 m/s"], "answer": "25 m/s", "explanation": "90 * (5/18) = 25 m/s."},
  {"id": 71, "company": "TCS", "topic": "Arithmetic", "level": "Medium", "question": "How many 3-digit numbers are divisible by 6?", "options": ["149", "150", "151", "166"], "answer": "150", "explanation": "Smallest is 102, largest is 996. AP: 996 = 102 + (n-1)6 => 894 = 6(n-1) => 149 = n-1 => n = 150."},
  {"id": 72, "company": "Cognizant", "topic": "Logical", "level": "Hard", "question": "In a row of boys, if A is 10th from left and B is 9th from right and they interchange positions, A becomes 15th from left. How many boys are there in the row?", "options": ["23", "27", "28", "31"], "answer": "23", "explanation": "A's new position (15th left) is B's old position (9th right). Total = 15 + 9 - 1 = 23."},
  {"id": 73, "company": "Wipro", "topic": "Arithmetic", "level": "Medium", "question": "At what time between 4 and 5 o'clock will the hands of a clock be at right angle?", "options": ["38 2/11 min past 4", "5 5/11 min past 4", "Both A and B", "None"], "answer": "Both A and B", "explanation": "Angles occur at (5h +/- 15) * 12/11. For h=4: (20-15)*12/11 = 5 5/11 and (20+15)*12/11 = 38 2/11."},
  {"id": 74, "company": "Infosys", "topic": "Arithmetic", "level": "Easy", "question": "If 5% of x is 600, then x is:", "options": ["10000", "12000", "15000", "20000"], "answer": "12000", "explanation": "0.05x = 600 => x = 600/0.05 = 12000."},
  {"id": 75, "company": "Accenture", "topic": "Logical", "level": "Medium", "question": "If 'FRANCE' is coded as '6, 18, 1, 14, 3, 5', how is 'INDIA' coded?", "options": ["9, 14, 4, 9, 1", "9, 13, 4, 9, 1", "8, 14, 4, 8, 1", "9, 14, 3, 9, 1"], "answer": "9, 14, 4, 9, 1", "explanation": "Each letter is replaced by its position in the alphabet (A=1, B=2, etc.)."},
  {"id": 76, "company": "TCS", "topic": "Verbal", "level": "Hard", "question": "Choose the correct part of speech for the underlined word: 'The flowers smell sweet.'", "options": ["Adverb", "Adjective", "Verb", "Noun"], "answer": "Adjective", "explanation": "In this sentence, 'sweet' describes the flowers (a noun), making it an adjective."},
  {"id": 77, "company": "Cognizant", "topic": "Arithmetic", "level": "Medium", "question": "A person crosses a 600 m long street in 5 minutes. What is his speed in km/hr?", "options": ["3.6", "7.2", "8.4", "10"], "answer": "7.2", "explanation": "Speed = 600 / 300 = 2 m/s. In km/hr: 2 * (18/5) = 7.2."},
  {"id": 78, "company": "Wipro", "topic": "Arithmetic", "level": "Easy", "question": "Which of the following is a prime number?", "options": ["33", "81", "93", "97"], "answer": "97", "explanation": "97 is not divisible by any number other than 1 and itself."},
  {"id": 79, "company": "Infosys", "topic": "Logical", "level": "Hard", "question": "If 'white' is called 'blue', 'blue' is called 'red', 'red' is called 'yellow', 'yellow' is called 'green', 'green' is called 'black', 'black' is called 'violet' and 'violet' is called 'orange', what would be the color of human blood?", "options": ["Red", "Yellow", "Green", "Violet"], "answer": "Yellow", "explanation": "Human blood is red, but according to the code, red is called yellow."},
  {"id": 80, "company": "Accenture", "topic": "Arithmetic", "level": "Medium", "question": "A and B together have Rs. 1210. If 4/15 of A's amount is equal to 2/5 of B's amount, how much amount does B have?", "options": ["Rs. 460", "Rs. 484", "Rs. 550", "Rs. 664"], "answer": "Rs. 484", "explanation": "(4/15)A = (2/5)B => A = (2/5)*(15/4)B = 3/2B. A + B = 3/2B + B = 5/2B = 1210. B = (1210 * 2)/5 = 484."}
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
