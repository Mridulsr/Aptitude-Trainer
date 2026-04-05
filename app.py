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
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"history": [], "last_login": None, "streak": 0, "company_scores": {}}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# --- ADVANCED QUESTION BANK (Fixed Syntax) ---
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
    {"id": 40, "company": "Cognizant", "topic": "Logical", "level": "Hard", "question": "If 1st Oct is Sunday, then 1st Nov will be:", "options": ["Monday", "Tuesday", "Wednesday", "Thursday"], "answer": "Wednesday", "explanation": "Oct has 31 days. 31/7 leaves remainder 3. Sunday + 3 days = Wednesday."},
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
    {"id": 80, "company": "Accenture", "topic": "Arithmetic", "level": "Medium", "question": "A and B together have Rs. 1210. If 4/15 of A's amount is equal to 2/5 of B's amount, how much amount does B have?", "options": ["Rs. 460", "Rs. 484", "Rs. 550", "Rs. 664"], "answer": "Rs. 484", "explanation": "(4/15)A = (2/5)B => A = (2/5)*(15/4)B = 3/2B. A + B = 3/2B + B = 5/2B = 1210. B = (1210 * 2)/5 = 484."},
    {"id": 81, "company": "TCS", "topic": "Data Interpretation", "level": "Hard", "question": "Budget = 50L. Education: 25%, Health: 15%, Infrastructure: 40%, Others: 20%. Central angle for Infrastructure?", "options": ["144°", "120°", "150°", "108°"], "answer": "144°", "explanation": "(40/100) * 360 = 144°."},
    {"id": 82, "company": "Cognizant", "topic": "Data Interpretation", "level": "Medium", "question": "Profit grew from $20M (2024) to $25M (2025). % Increase?", "options": ["20%", "25%", "5%", "30%"], "answer": "25%", "explanation": "[(25-20)/20]*100 = 25%."},
    {"id": 83, "company": "Wipro", "topic": "Data Interpretation", "level": "Hard", "question": "Sales Year 1 (A:30, B:40, C:50), Year 2 (A:35, B:45, C:40). Highest % growth?", "options": ["Product A", "Product B", "Product C", "A and B both"], "answer": "Product A", "explanation": "A: 16.6%, B: 12.5%, C: Decrease."},
    {"id": 84, "company": "Infosys", "topic": "Data Interpretation", "level": "Medium", "question": "Ratio of TCS hiring (1800) to Wipro hiring (900) in 2025?", "options": ["1:2", "2:1", "3:2", "4:3"], "answer": "2:1", "explanation": "1800/900 = 2/1."},
    {"id": 85, "company": "Accenture", "topic": "Data Interpretation", "level": "Hard", "question": "Total Budget 1.2Cr. R&D is 35%. Amount in Lakhs?", "options": ["35L", "42L", "48L", "50L"], "answer": "42L", "explanation": "0.35 * 120 = 42 Lakhs."},
    {"id": 86, "company": "TCS", "topic": "Data Interpretation", "level": "Hard", "question": "If hiring grows by 20% each year, and 2025 hiring was 1000, what was 2023 hiring?", "options": ["694", "750", "800", "833"], "answer": "694", "explanation": "1000 / (1.2 * 1.2) = 694.4."},
    {"id": 87, "company": "Cognizant", "topic": "Data Interpretation", "level": "Medium", "question": "A bar chart shows 400, 500, 600, 700 units sold. What is the average?", "options": ["500", "550", "600", "650"], "answer": "550", "explanation": "(400+500+600+700)/4 = 550."},
    {"id": 88, "company": "Wipro", "topic": "Data Interpretation", "level": "Hard", "question": "In a pie chart, if 'Others' is 18°, what percentage does it represent?", "options": ["5%", "10%", "15%", "20%"], "answer": "5%", "explanation": "(18/360) * 100 = 5%."},
    {"id": 89, "company": "Infosys", "topic": "Data Interpretation", "level": "Medium", "question": "If 2024 revenue was 100Cr and 2025 is 150Cr, what is the ratio of increase to original?", "options": ["1:2", "2:3", "3:2", "1:1"], "answer": "1:2", "explanation": "Increase = 50. Ratio 50:100 = 1:2."},
    {"id": 90, "company": "Accenture", "topic": "Data Interpretation", "level": "Hard", "question": "Population: Pune(3.1M), Bang(8.4M). How much % larger is Bang than Pune?", "options": ["150%", "170%", "270%", "100%"], "answer": "170%", "explanation": "[(8.4-3.1)/3.1]*100 = 170.9%."},
    {"id": 91, "company": "TCS", "topic": "Data Interpretation", "level": "Medium", "question": "Table: A(10), B(20), C(30). What % of total is B?", "options": ["20%", "33.3%", "40%", "50%"], "answer": "33.3%", "explanation": "20 / (10+20+30) = 20/60 = 1/3."},
    {"id": 92, "company": "Cognizant", "topic": "Data Interpretation", "level": "Hard", "question": "Central angle of 72° represents what % of a circle?", "options": ["20%", "25%", "15%", "30%"], "answer": "20%", "explanation": "(72/360)*100 = 20%."},
    {"id": 93, "company": "Wipro", "topic": "Data Interpretation", "level": "Medium", "question": "Line graph: Jan(10), Feb(20), Mar(15). What is the % decrease from Feb to Mar?", "options": ["25%", "33%", "50%", "10%"], "answer": "25%", "explanation": "[(20-15)/20]*100 = 25%."},
    {"id": 94, "company": "Infosys", "topic": "Data Interpretation", "level": "Hard", "question": "Total 500 students. 40% like Java, 30% Python. How many like neither if 10% like both?", "options": ["150", "200", "250", "300"], "answer": "200", "explanation": "Total liking = 40+30-10 = 60%. Neither = 40%. 40% of 500 = 200."},
    {"id": 95, "company": "Accenture", "topic": "Data Interpretation", "level": "Medium", "question": "Revenue 2025: $400k. If it grows 10% for 2026, new revenue?", "options": ["$440k", "$410k", "$450k", "$480k"], "answer": "$440k", "explanation": "400 * 1.1 = 440."},
    {"id": 96, "company": "TCS", "topic": "Data Interpretation", "level": "Hard", "question": "In a Venn Diagram of 100 people, 60 drink Tea, 50 drink Coffee. How many drink both?", "options": ["10", "20", "30", "40"], "answer": "10", "explanation": "(60+50) - 100 = 10."},
    {"id": 97, "company": "Cognizant", "topic": "Arithmetic", "level": "Medium", "question": "Average of 10 numbers is 7. If each number is multiplied by 12, new average?", "options": ["7", "12", "84", "19"], "answer": "84", "explanation": "New Avg = Old Avg * 12 = 7 * 12 = 84."},
    {"id": 98, "company": "Wipro", "topic": "Logical", "level": "Hard", "question": "If 1st Jan 2024 is Monday, what is 1st Jan 2025? (2024 is Leap)", "options": ["Tuesday", "Wednesday", "Thursday", "Friday"], "answer": "Wednesday", "explanation": "Leap year has 2 odd days. Monday + 2 = Wednesday."},
    {"id": 99, "company": "Infosys", "topic": "Arithmetic", "level": "Easy", "question": "Square root of 0.0009?", "options": ["0.3", "0.03", "0.003", "3"], "answer": "0.03", "explanation": "0.03 * 0.03 = 0.0009."},
    {"id": 100, "company": "Accenture", "topic": "Arithmetic", "level": "Medium", "question": "A sum of money at CI doubles in 5 years. In how many years will it be 8 times?", "options": ["10", "15", "20", "25"], "answer": "15", "explanation": "2^1 in 5 years. 8 = 2^3. Time = 5 * 3 = 15 years."},
    {"id": 101, "company": "Wipro", "topic": "Logical", "level": "Easy", "question": "Find the missing term: 2, 6, 12, 20, 30, ?", "options": ["40", "42", "44", "46"], "answer": "42", "explanation": "The pattern is n^2 + n or adding consecutive even numbers: +4, +6, +8, +10, +12. 30 + 12 = 42."},
    {"id": 102, "company": "Wipro", "topic": "Logical", "level": "Medium", "question": "In a certain code, 'COMPUTER' is written as 'RFUVQNPC'. How is 'MEDICINE' written?", "options": ["EOJDJEFM", "EOJDEJFM", "MFEJDJOE", "EOJDJFME"], "answer": "EOJDJEFM", "explanation": "Reverse the word, then +1 to each letter except the first and last (which are swapped). R...C becomes C...R, then others shift."},
    {"id": 103, "company": "Wipro", "topic": "Logical", "level": "Hard", "question": "Statements: All bags are pockets. All pockets are pouches. Conclusions: I. All bags are pouches. II. Some pouches are pockets.", "options": ["Only I follows", "Only II follows", "Both I and II follow", "Neither follows"], "answer": "Both I and II follow", "explanation": "Bags ⊂ Pockets ⊂ Pouches. Therefore, Bags ⊂ Pouches (I) and since Pockets are a subset of Pouches, some Pouches must be Pockets (II)."},
    {"id": 104, "company": "Wipro", "topic": "Logical", "level": "Medium", "question": "If 'A $ B' means A is the brother of B; 'A @ B' means A is the wife of B; 'A # B' means A is the daughter of B. What does 'P # R $ Q' mean?", "options": ["P is the sister of Q", "P is the niece of Q", "P is the aunt of Q", "P is the mother of Q"], "answer": "P is the niece of Q", "explanation": "P is daughter of R, R is brother of Q. Father's brother's daughter or brother's daughter is a niece."},
    {"id": 105, "company": "Wipro", "topic": "Logical", "level": "Easy", "question": "Which of the following does not belong to the group?", "options": ["Acknowledge", "Accept", "Grant", "Deny"], "answer": "Deny", "explanation": "Acknowledge, Accept, and Grant are synonyms related to agreeing/receiving. Deny is the opposite."},
    {"id": 106, "company": "Wipro", "topic": "Logical", "level": "Medium", "question": "A man walks 5km East, then turns right and walks 4km, then turns left and walks 5km. Which direction is he facing now?", "options": ["North", "South", "East", "West"], "answer": "East", "explanation": "Initial: East. Turn Right: South. Turn Left: East. He is still moving East."},
    {"id": 107, "company": "Wipro", "topic": "Logical", "level": "Hard", "question": "If 1st January 2023 was a Sunday, what day of the week was 1st January 2026?", "options": ["Wednesday", "Thursday", "Friday", "Saturday"], "answer": "Thursday", "explanation": "2023 (1 odd day), 2024 (2 odd days - Leap), 2025 (1 odd day). Total = 4 odd days. Sunday + 4 = Thursday."},
    {"id": 108, "company": "Wipro", "topic": "Logical", "level": "Medium", "question": "In a class of 45 students, Amir's rank is 16th from the top. What is his rank from the bottom?", "options": ["29th", "30th", "31st", "32nd"], "answer": "30th", "explanation": "Rank from bottom = (Total - Rank from top) + 1 = (45 - 16) + 1 = 30."},
    {"id": 109, "company": "Wipro", "topic": "Logical", "level": "Easy", "question": "Complete the series: B2CD, ____, BCD4, B5CD, BC6D", "options": ["BC3D", "B3CD", "BC3D2", "B2C2D"], "answer": "BC3D", "explanation": "The number moves positions from the 2nd char to the 3rd, 4th, and resets with a higher number. 2 (after B), 3 (after C), 4 (after D), then 5 (after B)."},
    {"id": 110,"company": "TCS","topic": "Arithmetic","level": "Easy","question": "What is the sum of the first 15 odd numbers?","options": ["225", "200", "196", "256"],"answer": "225","explanation": "The sum of the first n odd numbers is given by n^2. Here n = 15, so 15^2 = 225."},
  {
    "id": 111,
    "company": "TCS",
    "topic": "Logical",
    "level": "Easy",
    "question": "If DRIVER = 12, PEDESTRIAN = 20, ACCIDENT = 16, then what is CAR?",
    "options": ["3", "6", "8", "10"],
    "answer": "6",
    "explanation": "The pattern is (Number of letters in the word) * 2. CAR has 3 letters, so 3 * 2 = 6."
  },
  {
    "id": 120,
    "company": "TCS",
    "topic": "Arithmetic",
    "level": "Hard",
    "question": "A man's speed with the current is 15 km/hr and the speed of the current is 2.5 km/hr. What is the man's speed against the current?",
    "options": ["8.5 km/hr", "9 km/hr", "10 km/hr", "12.5 km/hr"],
    "answer": "10 km/hr",
    "explanation": "Speed in still water = Speed with current - current speed = 15 - 2.5 = 12.5 km/hr. Speed against current = Still water speed - current speed = 12.5 - 2.5 = 10 km/hr."
  },
  {
    "id": 130,
    "company": "Infosys",
    "topic": "Arithmetic",
    "level": "Easy",
    "question": "Solve: 0.003 * 0.02",
    "options": ["0.06", "0.006", "0.0006", "0.00006"],
    "answer": "0.00006",
    "explanation": "Multiply the numbers: 3 * 2 = 6. Count decimal places: 3 + 2 = 5 places. Result = 0.00006."
  },
  {
    "id": 140,
    "company": "Infosys",
    "topic": "Arithmetic",
    "level": "Hard",
    "question": "A card is drawn from a pack of 52. What is the probability that it is either a King or a Heart?",
    "options": ["4/13", "17/52", "1/4", "1/13"],
    "answer": "4/13",
    "explanation": "P(King) = 4/52, P(Heart) = 13/52, P(King of Hearts) = 1/52. P(K or H) = (4+13-1)/52 = 16/52 = 4/13."
  },
  {
    "id": 150,
    "company": "Wipro",
    "topic": "Arithmetic",
    "level": "Easy",
    "question": "What is the square root of 0.0009?",
    "options": ["0.3", "0.03", "0.003", "0.9"],
    "answer": "0.03",
    "explanation": "0.03 * 0.03 = 0.0009. Therefore, the square root is 0.03."
  },
  {
    "id": 160,
    "company": "Wipro",
    "topic": "Arithmetic",
    "level": "Hard",
    "question": "A sum of money becomes 8 times itself in 3 years at compound interest. What is the rate of interest per annum?",
    "options": ["50%", "100%", "150%", "200%"],
    "answer": "100%",
    "explanation": "8P = P(1 + R/100)^3 => 2^3 = (1 + R/100)^3 => 2 = 1 + R/100 => R = 100%."
  },
  {
    "id": 170,
    "company": "Accenture",
    "topic": "Arithmetic",
    "level": "Easy",
    "question": "What is 20% of 50 + 50% of 20?",
    "options": ["10", "20", "30", "40"],
    "answer": "20",
    "explanation": "20% of 50 = 10. 50% of 20 = 10. 10 + 10 = 20."
  },
  {
    "id": 180,
    "company": "Accenture",
    "topic": "Arithmetic",
    "level": "Hard",
    "question": "A shopkeeper marks his goods 20% above the cost price and allows a 10% discount. What is his profit percentage?",
    "options": ["8%", "10%", "12%", "15%"],
    "answer": "8%",
    "explanation": "Let CP = 100. Marked Price = 120. Discount = 10% of 120 = 12. SP = 120 - 12 = 108. Profit = 8%."
  },
  {
    "id": 200,
    "company": "Cognizant",
    "topic": "Arithmetic",
    "level": "Hard",
    "question": "A man's present age is 2/5 of his mother's. After 8 years, he will be 1/2 of his mother's age. How old is the mother now?",
    "options": ["30", "40", "50", "60"],
    "answer": "40",
    "explanation": "Let Mother = M, Son = 2/5 M. (2/5 M + 8) = 1/2 (M + 8). Solve for M: 0.4M + 8 = 0.5M + 4 => 0.1M = 4 => M = 40."
  },
{"id": 110, "company": "TCS", "topic": "Arithmetic", "level": "Easy", "question": "What is the sum of the first 15 odd numbers?", "options": ["225", "200", "196", "256"], "answer": "225", "explanation": "Sum of first n odd numbers is n^2. 15^2 = 225."},
  {"id": 111, "company": "TCS", "topic": "Logical", "level": "Easy", "question": "If DRIVER = 12, PEDESTRIAN = 20, ACCIDENT = 16, then CAR = ?", "options": ["3", "6", "8", "10"], "answer": "6", "explanation": "Pattern: (Number of letters) * 2. 3 * 2 = 6."},
  {"id": 112, "company": "TCS", "topic": "Verbal", "level": "Easy", "question": "Choose the synonym of 'ABRIDGE':", "options": ["Expand", "Shorten", "Release", "Bind"], "answer": "Shorten", "explanation": "To abridge is to shorten a piece of writing without losing the sense."},
  {"id": 113, "company": "TCS", "topic": "Arithmetic", "level": "Easy", "question": "A fruit seller had some apples. He sells 40% apples and still has 420 apples. How many did he have originally?", "options": ["588", "600", "672", "700"], "answer": "700", "explanation": "60% = 420. So 100% = (420/60) * 100 = 700."},
  {"id": 114, "company": "TCS", "topic": "Logical", "level": "Easy", "question": "Find the next number: 1, 4, 9, 16, 25, 36, ?", "options": ["48", "49", "50", "56"], "answer": "49", "explanation": "Square of consecutive integers: 7^2 = 49."},
  {"id": 115, "company": "TCS", "topic": "Arithmetic", "level": "Easy", "question": "12.5% of 800 is:", "options": ["80", "100", "120", "150"], "answer": "100", "explanation": "(1/8) * 800 = 100."},
  {"id": 116, "company": "TCS", "topic": "Verbal", "level": "Easy", "question": "Identify the correctly spelt word:", "options": ["Recieve", "Receive", "Recievee", "Receve"], "answer": "Receive", "explanation": "Rule: 'i' before 'e' except after 'c'."},
  {"id": 117, "company": "TCS", "topic": "Arithmetic", "level": "Easy", "question": "If 15 men can reap a field in 35 days, in how many days will 21 men reap it?", "options": ["25", "20", "30", "28"], "answer": "25", "explanation": "M1D1 = M2D2 => 15 * 35 = 21 * D2 => D2 = 25."},
  {"id": 118, "company": "TCS", "topic": "Logical", "level": "Easy", "question": "Odd one out: 144, 169, 196, 210", "options": ["144", "169", "196", "210"], "answer": "210", "explanation": "210 is not a perfect square; others are 12^2, 13^2, 14^2."},
  {"id": 119, "company": "TCS", "topic": "Arithmetic", "level": "Easy", "question": "The average of 10, 20, 30, 40, 50 is:", "options": ["30", "35", "25", "40"], "answer": "30", "explanation": "Middle term of an AP with odd number of terms is the average."},
  {"id": 120, "company": "TCS", "topic": "Arithmetic", "level": "Hard", "question": "A man's speed with the current is 15 km/hr and the speed of the current is 2.5 km/hr. The man's speed against the current is:", "options": ["8.5", "9", "10", "12.5"], "answer": "10", "explanation": "Speed in still water = 15 - 2.5 = 12.5. Against current = 12.5 - 2.5 = 10."},
  {"id": 121, "company": "TCS", "topic": "Logical", "level": "Hard", "question": "In a code, 'SOLID' is 'WPSLPIMFHA'. How is 'AT' coded?", "options": ["BUV", "WXYZ", "BDVS", "SUWY"], "answer": "BDVS", "explanation": "Each letter is replaced by its preceding and succeeding letters. A->B,Z; T->S,U."},
  {"id": 122, "company": "TCS", "topic": "Data Interpretation", "level": "Hard", "question": "In a pie chart, if 'Rent' is 15% and 'Food' is 45%, what is the difference in central angles?", "options": ["108°", "90°", "115°", "120°"], "answer": "108°", "explanation": "(45-15)% = 30%. 0.3 * 360 = 108°."},
  {"id": 123, "company": "TCS", "topic": "Arithmetic", "level": "Hard", "question": "Find the remainder when 2^31 is divided by 5.", "options": ["1", "2", "3", "4"], "answer": "3", "explanation": "Cyclicity of 2 is 2,4,8,6. 31/4 rem 3. 2^3 = 8. 8/5 rem 3."},
  {"id": 124, "company": "TCS", "topic": "Arithmetic", "level": "Hard", "question": "4 men and 6 women can complete a work in 8 days. 3 men and 7 women in 10 days. In how many days will 10 women finish it?", "options": ["35", "40", "45", "50"], "answer": "40", "explanation": "8(4M+6W) = 10(3M+7W) => 1M=11W. Total work = 400W. 400/10 = 40 days."},
  {"id": 125, "company": "TCS", "topic": "Logical", "level": "Hard", "question": "All fans are cups. All cups are pillows. Which conclusion is true?", "options": ["All fans are pillows", "All pillows are fans", "No fan is pillow", "Some pillows are not fans"], "answer": "All fans are pillows", "explanation": "Standard syllogism: If A is in B and B is in C, then A is in C."},
  {"id": 126, "company": "TCS", "topic": "Arithmetic", "level": "Hard", "question": "A tank is filled by A in 20 mins and B in 30 mins. A leak empties it in 15 mins. If all are open, the tank fills in:", "options": ["40", "50", "60", "Never"], "answer": "60", "explanation": "Rate = 1/20 + 1/30 - 1/15 = 1/60."},
  {"id": 127, "company": "TCS", "topic": "Verbal", "level": "Hard", "question": "He is too weak to walk. (Remove 'too')", "options": ["He is so weak that he cannot walk", "He is very weak to walk", "He is weak so he walks", "None"], "answer": "He is so weak that he cannot walk", "explanation": "Transformation of 'too...to' into 'so...that...not'."},
  {"id": 128, "company": "TCS", "topic": "Arithmetic", "level": "Hard", "question": "Find the number of zeros at the end of 100!", "options": ["20", "24", "25", "30"], "answer": "24", "explanation": "100/5 + 100/25 = 20 + 4 = 24."},
  {"id": 129, "company": "TCS", "topic": "Logical", "level": "Hard", "question": "If 1st January 2001 was Monday, what day was 1st January 2005?", "options": ["Friday", "Saturday", "Sunday", "Monday"], "answer": "Saturday", "explanation": "2001, 2002, 2003 (1 odd day each), 2004 (2 odd days). Total 5 days. Mon+5 = Sat."},
  {"id": 130, "company": "Infosys", "topic": "Arithmetic", "level": "Easy", "question": "Solve: 0.003 * 0.02", "options": ["0.06", "0.006", "0.0006", "0.00006"], "answer": "0.00006", "explanation": "3*2=6; shift decimal 5 places."},
  {"id": 131, "company": "Infosys", "topic": "Logical", "level": "Easy", "question": "Complete the series: 2, 6, 12, 20, 30, ?", "options": ["40", "42", "44", "46"], "answer": "42", "explanation": "Pattern: +4, +6, +8, +10, +12."},
  {"id": 132, "company": "Infosys", "topic": "Verbal", "level": "Easy", "question": "Antonym of 'FRAIL':", "options": ["Weak", "Strong", "Small", "Fast"], "answer": "Strong", "explanation": "Frail means delicate or weak."},
  {"id": 133, "company": "Infosys", "topic": "Arithmetic", "level": "Easy", "question": "Ratio of 45 minutes to 3 hours is:", "options": ["1:4", "1:3", "1:2", "1:5"], "answer": "1:4", "explanation": "45 min : 180 min = 1:4."},
  {"id": 134, "company": "Infosys", "topic": "Logical", "level": "Easy", "question": "If COB is 3152, then what is TAX?", "options": ["20124", "21124", "20132", "19124"], "answer": "20124", "explanation": "T=20, A=1, X=24."},
  {"id": 135, "company": "Infosys", "topic": "Arithmetic", "level": "Easy", "question": "HCF of 12 and 18 is:", "options": ["2", "3", "6", "9"], "answer": "6", "explanation": "Largest common divisor."},
  {"id": 136, "company": "Infosys", "topic": "Verbal", "level": "Easy", "question": "Meaning of the idiom 'To cry wolf':", "options": ["To listen", "To give false alarm", "To keep a dog", "To be brave"], "answer": "To give false alarm", "explanation": "Raising a false alarm."},
  {"id": 137, "company": "Infosys", "topic": "Arithmetic", "level": "Easy", "question": "A person buys a cycle for Rs. 1400 and sells it at a loss of 15%. SP?", "options": ["1190", "1200", "1160", "1000"], "answer": "1190", "explanation": "1400 * 0.85 = 1190."},
  {"id": 138, "company": "Infosys", "topic": "Logical", "level": "Easy", "question": "Which word is the odd one?", "options": ["Inch", "Ounce", "Yard", "Centimeter"], "answer": "Ounce", "explanation": "Ounce is weight; others are length."},
  {"id": 139, "company": "Infosys", "topic": "Arithmetic", "level": "Easy", "question": "Sum of 1/2 and 1/4:", "options": ["1/6", "3/4", "2/3", "1/8"], "answer": "3/4", "explanation": "2/4 + 1/4 = 3/4."},
  {"id": 140, "company": "Infosys", "topic": "Arithmetic", "level": "Hard", "question": "A man rows 6 km/hr in still water. Current is 2 km/hr. It takes 3 hrs to go to a place and back. Distance?", "options": ["4km", "8km", "10km", "12km"], "answer": "8km", "explanation": "d/8 + d/4 = 3 => 3d/8 = 3 => d=8."},
  {"id": 141, "company": "Infosys", "topic": "Logical", "level": "Hard", "question": "What is age of X? 1. X is 3 yrs older than Y. 2. Ratio X:Y is 4:3.", "options": ["1 alone", "2 alone", "Both", "Neither"], "answer": "Both", "explanation": "Two equations for two unknowns."},
  {"id": 142, "company": "Infosys", "topic": "Arithmetic", "level": "Hard", "question": "Probability of drawing a King or a Heart from 52 cards?", "options": ["4/13", "17/52", "1/4", "1/13"], "answer": "4/13", "explanation": "(4+13-1)/52 = 16/52 = 4/13."},
  {"id": 143, "company": "Infosys", "topic": "Verbal", "level": "Hard", "question": "Choose correct sentence:", "options": ["I have seen him yesterday", "I saw him yesterday", "I had seen him yesterday", "I see him yesterday"], "answer": "I saw him yesterday", "explanation": "Past time markers take simple past."},
  {"id": 144, "company": "Infosys", "topic": "Arithmetic", "level": "Hard", "question": "Surface area of sphere is 616 cm^2. Radius?", "options": ["5", "6", "7", "8"], "answer": "7", "explanation": "4 * 22/7 * r^2 = 616 => r=7."},
  {"id": 145, "company": "Infosys", "topic": "Logical", "level": "Hard", "question": "Missing number: 8, 24, 12, 36, 18, 54, ?", "options": ["27", "108", "72", "68"], "answer": "27", "explanation": "*3, /2 pattern."},
  {"id": 146, "company": "Infosys", "topic": "Arithmetic", "level": "Hard", "question": "X invests 3x of Y. Y is 2/3 of Z. Investment ratio X:Y:Z?", "options": ["2:1:3", "6:2:3", "3:2:2", "1:2:3"], "answer": "6:2:3", "explanation": "Let Z=3, Y=2, X=6."},
  {"id": 147, "company": "Infosys", "topic": "Logical", "level": "Hard", "question": "Seven people in a circle. A between B and C... (complex seating)", "options": ["A", "B", "C", "D"], "answer": "C", "explanation": "Standard circular arrangement logic."},
  {"id": 148, "company": "Infosys", "topic": "Arithmetic", "level": "Hard", "question": "20% of a number is 120. 120% of that number is?", "options": ["20", "120", "480", "720"], "answer": "720", "explanation": "Number = 600. 1.2 * 600 = 720."},
  {"id": 149, "company": "Infosys", "topic": "Data Interpretation", "level": "Hard", "question": "Wheat 2020: 50 tons, 2021: 80 tons. % increase?", "options": ["30%", "60%", "40%", "50%"], "answer": "60%", "explanation": "(30/50)*100 = 60%."},
  {"id": 150, "company": "Wipro", "topic": "Arithmetic", "level": "Easy", "question": "Square root of 0.0009 is:", "options": ["0.3", "0.03", "0.003", "0.9"], "answer": "0.03", "explanation": "0.03 * 0.03 = 0.0009."},
  {"id": 151, "company": "Wipro", "topic": "Logical", "level": "Easy", "question": "Day : Night :: Dawn : ?", "options": ["Morning", "Dusk", "Evening", "Midnight"], "answer": "Dusk", "explanation": "Antonym pair."},
  {"id": 152, "company": "Wipro", "topic": "Verbal", "level": "Easy", "question": "Fill in: He is _____ honest man.", "options": ["a", "an", "the", "no"], "answer": "an", "explanation": "'h' is silent; vowel sound 'o'."},
  {"id": 153, "company": "Wipro", "topic": "Arithmetic", "level": "Easy", "question": "Train 100m long passes 150m bridge in 25s. Speed?", "options": ["10 m/s", "15 m/s", "20 m/s", "25 m/s"], "answer": "10 m/s", "explanation": "250/25 = 10."},
  {"id": 154, "company": "Wipro", "topic": "Logical", "level": "Easy", "question": "If RED is 27, BLUE is?", "options": ["36", "40", "48", "52"], "answer": "40", "explanation": "Sum of letter positions."},
  {"id": 155, "company": "Wipro", "topic": "Arithmetic", "level": "Easy", "question": "SI on 500 for 4 years at 5% p.a.?", "options": ["100", "120", "80", "150"], "answer": "100", "explanation": "500 * 4 * 0.05 = 100."},
  {"id": 156, "company": "Wipro", "topic": "Verbal", "level": "Easy", "question": "One who doesn't believe in God:", "options": ["Theist", "Atheist", "Devotee", "Saint"], "answer": "Atheist", "explanation": "Definition."},
  {"id": 157, "company": "Wipro", "topic": "Arithmetic", "level": "Easy", "question": "3/4 of 20% of 600 is:", "options": ["60", "90", "120", "150"], "answer": "90", "explanation": "0.75 * 120 = 90."},
  {"id": 158, "company": "Wipro", "topic": "Logical", "level": "Easy", "question": "Next term: AZ, CX, EV, GT, ?", "options": ["IR", "HS", "KP", "MN"], "answer": "IR", "explanation": "+2 for first letter, -2 for second."},
  {"id": 159, "company": "Wipro", "topic": "Arithmetic", "level": "Easy", "question": "Sum of angles in a triangle:", "options": ["90", "180", "270", "360"], "answer": "180", "explanation": "Geometric constant."},
  {"id": 160, "company": "Wipro", "topic": "Arithmetic", "level": "Hard", "question": "Sum becomes 8x in 3 yrs at CI. Rate?", "options": ["50%", "100%", "150%", "200%"], "answer": "100%", "explanation": "(1+r)^3 = 8 => 1+r = 2 => r=1 (100%)."},
  {"id": 161, "company": "Wipro", "topic": "Logical", "level": "Hard", "question": "Row of 40. A is 13th left, B is 9th right. Between?", "options": ["16", "18", "20", "22"], "answer": "18", "explanation": "40 - (13+9) = 18."},
  {"id": 162, "company": "Wipro", "topic": "Arithmetic", "level": "Hard", "question": "A+B in 12, B+C in 15, C+A in 20. A alone?", "options": ["20", "30", "40", "60"], "answer": "30", "explanation": "2(A+B+C) = 1/5 => A+B+C = 1/10. A = 1/10-1/15 = 1/30."},
  {"id": 163, "company": "Wipro", "topic": "Verbal", "level": "Hard", "question": "Error: 'The news are very depressing today.'", "options": ["News", "are", "depressing", "today"], "answer": "are", "explanation": "News is singular."},
  {"id": 164, "company": "Wipro", "topic": "Arithmetic", "level": "Hard", "question": "Diagonal of square is 10 cm. Area?", "options": ["50", "100", "25", "75"], "answer": "50", "explanation": "d^2 / 2 = 100/2 = 50."},
  {"id": 165, "company": "Wipro", "topic": "Logical", "level": "Hard", "question": "P+Q (Father), P*Q (Sister). A*B+C means?", "options": ["A is aunt of C", "A is sister of C", "A is mother of C", "None"], "answer": "A is aunt of C", "explanation": "A is sister of B, B is father of C."},
  {"id": 166, "company": "Wipro", "topic": "Arithmetic", "level": "Hard", "question": "Remainder: (67^67 + 67) / 68?", "options": ["1", "63", "66", "67"], "answer": "66", "explanation": "(-1)^67 + (-1) = -2 mod 68 = 66."},
  {"id": 167, "company": "Wipro", "topic": "Logical", "level": "Hard", "question": "Time between 7 and 8 when hands together?", "options": ["38 2/11 past 7", "35 past 7", "40 past 7", "None"], "answer": "38 2/11 past 7", "explanation": "30h - 5.5m = 0 => 210/5.5 = 38 2/11."},
  {"id": 168, "company": "Wipro", "topic": "Arithmetic", "level": "Hard", "question": "3 dice. Prob of total 18?", "options": ["1/216", "1/36", "1/72", "0"], "answer": "1/216", "explanation": "Only (6,6,6) works."},
  {"id": 169, "company": "Wipro", "topic": "Arithmetic", "level": "Hard", "question": "Solve: log2(x) + log2(x-1) = 1", "options": ["1", "2", "3", "4"], "answer": "2", "explanation": "x(x-1) = 2 => x=2."},
  {"id": 170, "company": "Accenture", "topic": "Arithmetic", "level": "Easy", "question": "20% of 50 + 50% of 20 = ?", "options": ["10", "20", "30", "40"], "answer": "20", "explanation": "10 + 10 = 20."},
  {"id": 171, "company": "Accenture", "topic": "Logical", "level": "Easy", "question": "ACE, GIK, MCQ, ?", "options": ["SUV", "STU", "RTU", "RSV"], "answer": "SUV", "explanation": "Skip 1 letter pattern."},
  {"id": 172, "company": "Accenture", "topic": "Verbal", "level": "Easy", "question": "Opposite of 'ANCIENT':", "options": ["Old", "New", "Modern", "Recent"], "answer": "Modern", "explanation": "Standard antonym."},
  {"id": 173, "company": "Accenture", "topic": "Arithmetic", "level": "Easy", "question": "Average of 1st five multiples of 3?", "options": ["3", "6", "9", "12"], "answer": "9", "explanation": "Middle term: 3,6,9,12,15."},
  {"id": 174, "company": "Accenture", "topic": "Logical", "level": "Easy", "question": "PEN is coded as 31. PARK is?", "options": ["40", "41", "42", "43"], "answer": "41", "explanation": "Sum of positions - some constant or simple sum."},
  {"id": 175, "company": "Accenture", "topic": "Arithmetic", "level": "Easy", "question": "LCM of 24, 36, 40:", "options": ["120", "240", "360", "480"], "answer": "360", "explanation": "Common denominator."},
  {"id": 176, "company": "Accenture", "topic": "Verbal", "level": "Easy", "question": "Correct spelling:", "options": ["Occurence", "Occurrence", "Ocurence", "Ocurrence"], "answer": "Occurrence", "explanation": "Double c, double r."},
  {"id": 177, "company": "Accenture", "topic": "Arithmetic", "level": "Easy", "question": "SP = 120, Profit = 20%. CP?", "options": ["100", "90", "110", "95"], "answer": "100", "explanation": "120/1.2 = 100."},
  {"id": 178, "company": "Accenture", "topic": "Logical", "level": "Easy", "question": "1, 8, 27, 64, ?", "options": ["100", "121", "125", "144"], "answer": "125", "explanation": "5^3 = 125."},
  {"id": 179, "company": "Accenture", "topic": "Arithmetic", "level": "Easy", "question": "Cube of 12:", "options": ["144", "1728", "1331", "2197"], "answer": "1728", "explanation": "12*12*12."},
  {"id": 180, "company": "Accenture", "topic": "Arithmetic", "level": "Hard", "question": "Mark 20% above CP, 10% discount. Profit %?", "options": ["8%", "10%", "12%", "15%"], "answer": "8%", "explanation": "1.2 * 0.9 = 1.08."},
  {"id": 181, "company": "Accenture", "topic": "Logical", "level": "Hard", "question": "Six friends in a row... (linear seating logic)", "options": ["A", "B", "C", "D"], "answer": "B", "explanation": "Positioning logic."},
  {"id": 182, "company": "Accenture", "topic": "Arithmetic", "level": "Hard", "question": "Sum: 1/(1*2) + 1/(2*3) ... + 1/(9*10)?", "options": ["0.9", "1.1", "0.5", "0.75"], "answer": "0.9", "explanation": "1 - 1/10 = 0.9."},
  {"id": 183, "company": "Accenture", "topic": "Verbal", "level": "Hard", "question": "Passive Voice: 'Who wrote this book?'", "options": ["By whom was this book written?", "By who this book written?", "This book written by whom?", "None"], "answer": "By whom was this book written?", "explanation": "Who -> By whom."},
  {"id": 184, "company": "Accenture", "topic": "Arithmetic", "level": "Hard", "question": "Radius ratio 2:3, height ratio 5:3. Volume ratio cylinder?", "options": ["10:9", "20:27", "4:9", "15:20"], "answer": "20:27", "explanation": "4*5 : 9*3 = 20:27."},
  {"id": 185, "company": "Accenture", "topic": "Logical", "level": "Hard", "question": "Add 2 to odd digit, sub 1 from even in 3658:", "options": ["5577", "5777", "5579", "None"], "answer": "5577", "explanation": "3+2, 6-1, 5+2, 8-1."},
  {"id": 186, "company": "Accenture", "topic": "Arithmetic", "level": "Hard", "question": "Shadow length = Pole height. Angle of elevation?", "options": ["30°", "45°", "60°", "90°"], "answer": "45°", "explanation": "tan(theta) = 1."},
  {"id": 187, "company": "Accenture", "topic": "Logical", "level": "Hard", "question": "Number of triangles in a complex star?", "options": ["8", "10", "12", "16"], "answer": "12", "explanation": "Manual counting logic."},
  {"id": 188, "company": "Accenture", "topic": "Arithmetic", "level": "Hard", "question": "5 white, 3 black balls. 2 drawn. Prob same color?", "options": ["13/28", "5/14", "3/14", "1/2"], "answer": "13/28", "explanation": "(10+3)/28 = 13/28."},
  {"id": 189, "company": "Accenture", "topic": "Arithmetic", "level": "Hard", "question": "Sum of all 2-digit numbers divisible by 5?", "options": ["945", "1045", "1145", "1245"], "answer": "945", "explanation": "n=18, sum = 9*(10+95)."},
  {"id": 190, "company": "Cognizant", "topic": "Arithmetic", "level": "Easy", "question": "10% of A = 20% of B. A:B?", "options": ["1:2", "2:1", "1:1", "3:1"], "answer": "2:1", "explanation": "0.1A = 0.2B."},
  {"id": 191, "company": "Cognizant", "topic": "Logical", "level": "Easy", "question": "5, 10, 15, 20, ?", "options": ["22", "25", "30", "35"], "answer": "25", "explanation": "Simple arithmetic progression."},
  {"id": 192, "company": "Cognizant", "topic": "Verbal", "level": "Easy", "question": "Correct: 'He don't know me.'", "options": ["He doesn't", "He didn't", "He do not", "No error"], "answer": "He doesn't", "explanation": "3rd person singular."},
  {"id": 193, "company": "Cognizant", "topic": "Arithmetic", "level": "Easy", "question": "Area of rectangle L=10, B=5:", "options": ["15", "50", "25", "30"], "answer": "50", "explanation": "L*B."},
  {"id": 194, "company": "Cognizant", "topic": "Logical", "level": "Easy", "question": "If BOOK is 43, PEN is?", "options": ["35", "40", "43", "31"], "answer": "35", "explanation": "16+5+14 = 35."},
  {"id": 195, "company": "Cognizant", "topic": "Arithmetic", "level": "Easy", "question": "Median of 3, 5, 7, 9, 11:", "options": ["3", "7", "9", "11"], "answer": "7", "explanation": "Middle value."},
  {"id": 196, "company": "Cognizant", "topic": "Verbal", "level": "Easy", "question": "Synonym of 'LUCID':", "options": ["Clear", "Dark", "Hard", "Soft"], "answer": "Clear", "explanation": "Lucid means easy to understand."},
  {"id": 197, "company": "Cognizant", "topic": "Arithmetic", "level": "Easy", "question": "0.5 as a fraction:", "options": ["1/2", "1/5", "5/1", "2/5"], "answer": "1/2", "explanation": "5/10 = 1/2."},
  {"id": 198, "company": "Cognizant", "topic": "Logical", "level": "Easy", "question": "North, South, East, ?", "options": ["West", "Left", "Right", "Up"], "answer": "West", "explanation": "Cardinal directions."},
  {"id": 199, "company": "Cognizant", "topic": "Arithmetic", "level": "Easy", "question": "1kg sugar costs 40, 250g costs?", "options": ["5", "10", "15", "20"], "answer": "10", "explanation": "40/4 = 10."},
  {"id": 200, "company": "Cognizant", "topic": "Arithmetic", "level": "Hard", "question": "Man is 2/5 mother's age. In 8 yrs, he's 1/2. Mother's age?", "options": ["30", "40", "50", "60"], "answer": "40", "explanation": "0.4M+8 = 0.5(M+8) => M=40."},
  {"id": 201, "company": "Cognizant", "topic": "Logical", "level": "Hard", "question": "A is B's brother, C is A's father... (blood relation)", "options": ["Uncle", "Father", "Brother", "Cousin"], "answer": "Cousin", "explanation": "Family tree analysis."},
  {"id": 202, "company": "Cognizant", "topic": "Arithmetic", "level": "Hard", "question": "Cone and cylinder same base/height. Volume ratio?", "options": ["1:3", "3:1", "1:2", "2:1"], "answer": "1:3", "explanation": "1/3*pi*r^2*h : pi*r^2*h."},
  {"id": 203, "company": "Cognizant", "topic": "Verbal", "level": "Hard", "question": "The _____ of the state is fragile.", "options": ["Policy", "Polity", "Police", "Politics"], "answer": "Polity", "explanation": "Polity means a form of government."},
  {"id": 204, "company": "Cognizant", "topic": "Arithmetic", "level": "Hard", "question": "Clock hands overlap in a day how many times?", "options": ["11", "12", "22", "24"], "answer": "22", "explanation": "Overlap occurs 11 times in 12 hours."},
  {"id": 205, "company": "Cognizant", "topic": "Logical", "level": "Hard", "question": "8+5=1340, 4+6=1024. 7+4=?", "options": ["1128", "1124", "1111", "1130"], "answer": "1128", "explanation": "(Sum)(Product)."},
  {"id": 206, "company": "Cognizant", "topic": "Arithmetic", "level": "Hard", "question": "Divided by 20, 25, 35, 40 leaves rem 14, 19, 29, 34. Smallest number?", "options": ["1394", "1400", "1406", "1386"], "answer": "1394", "explanation": "LCM - common difference (6)."},
  {"id": 207, "company": "Cognizant", "topic": "Logical", "level": "Hard", "question": "No paper is pen. Some pens are pencils. Conclusion?", "options": ["Some pencils are pens", "Some pencils are papers", "Both", "None"], "answer": "Some pencils are pens", "explanation": "Converse of 'Some pens are pencils'."},
  {"id": 208, "company": "Cognizant", "topic": "Arithmetic", "level": "Hard", "question": "CI on 5000 for 1.5 yrs at 4% compounded half-yearly?", "options": ["306.04", "300", "310", "320"], "answer": "306.04", "explanation": "5000(1.02)^3 - 5000."},
  {"id": 209, "company": "Cognizant", "topic": "Data Interpretation", "level": "Hard", "question": "Sales Jan: 100, Feb: 120, Mar: 110. Average?", "options": ["100", "110", "120", "115"], "answer": "110", "explanation": "330/3 = 110."},
    {"id": 102, "company": "TCS", "topic": "Arithmetic", "level": "Easy", "question": "The sum of two numbers is 25 and their difference is 13. Find their product.", "options": ["104", "114", "315", "325"], "answer": "114", "explanation": "x+y=25, x-y=13. Adding gives 2x=38, x=19. Then y=6. Product = 19*6 = 114."},
    {"id": 103, "company": "TCS", "topic": "Arithmetic", "level": "Medium", "question": "What is the remainder when 2^31 is divided by 7?", "options": ["1", "2", "3", "4"], "answer": "2", "explanation": "2^3 = 8. 8/7 leaves remainder 1. (2^3)^10 * 2^1 = 1^10 * 2 = 2."},
    {"id": 104, "company": "TCS", "topic": "Programming Logic", "level": "Hard", "question": "In C, what is the output of printf('%d', 10 ? 0 ? 5 : 11 : 12);?", "options": ["10", "0", "11", "12"], "answer": "11", "explanation": "Nested ternary: 10 is true, so it evaluates (0 ? 5 : 11). 0 is false, so it results in 11."},
    {"id": 105, "company": "TCS", "topic": "Arithmetic", "level": "Advanced", "question": "A sum of money amounts to Rs. 6690 after 3 years and to Rs. 10035 after 6 years on compound interest. Find the sum.", "options": ["4460", "4400", "4500", "4660"], "answer": "4460", "explanation": "Ratio of amounts = 10035/6690 = 1.5. P * (1.5) = 6690. P = 6690 / 1.5 = 4460."},

    # --- COGNIZANT (Logical Reasoning & Verbal) ---
    {"id": 106, "company": "Cognizant", "topic": "Logical", "level": "Easy", "question": "If FISH is coded as EHRG, what is the code for JUNGLE?", "options": ["ITMFKD", "ITMFLD", "KVOHMF", "TIMFKD"], "answer": "ITMFKD", "explanation": "Each letter is shifted one position backward (F-1=E, I-1=H, etc.)."},
    {"id": 107, "company": "Cognizant", "topic": "Logical", "level": "Medium", "question": "A man walks 5km South, then turns right and walks 3km. He then turns left and walks 5km. In which direction is he from the starting point?", "options": ["South", "South-West", "South-East", "North-West"], "answer": "South-West", "explanation": "Starting at origin (0,0), he goes to (0,-5), then (-3,-5), then (-3,-10). This is South-West."},
    {"id": 108, "company": "Cognizant", "topic": "Verbal", "level": "Hard", "question": "Choose the correct sentence:", "options": ["He is one of the best man in the world.", "He is one of the best men in the world.", "He is one of the better men in the world.", "He is one of best men in the world."], "answer": "He is one of the best men in the world.", "explanation": "'One of the' is followed by a plural noun and a superlative adjective."},
    {"id": 109, "company": "Cognizant", "topic": "Logical", "level": "Advanced", "question": "Statements: All bags are pockets. All pockets are pouches. Conclusion: I. All bags are pouches. II. Some pouches are bags.", "options": ["Only I follows", "Only II follows", "Both I and II follow", "Neither I nor II follow"], "answer": "Both I and II follow", "explanation": "Standard syllogism. Since Bags ⊂ Pockets ⊂ Pouches, All bags are pouches. Consequently, some pouches are bags."},

    # --- WIPRO (Quantitative & Analytical) ---
    {"id": 110, "company": "Wipro", "topic": "Arithmetic", "level": "Easy", "question": "The average of 5 numbers is 27. If one number is excluded, the average becomes 25. Find the excluded number.", "options": ["30", "35", "40", "45"], "answer": "35", "explanation": "Sum of 5 = 5*27 = 135. Sum of 4 = 4*25 = 100. Excluded = 135 - 100 = 35."},
    {"id": 111, "company": "Wipro", "topic": "Arithmetic", "level": "Medium", "question": "A can do a work in 15 days, B in 20 days. They work together for 4 days. What fraction of work is left?", "options": ["7/15", "8/15", "11/15", "1/4"], "answer": "8/15", "explanation": "1 day work = 1/15 + 1/20 = 7/60. 4 days work = 28/60 = 7/15. Left = 1 - 7/15 = 8/15."},
    {"id": 112, "company": "Wipro", "topic": "Arithmetic", "level": "Hard", "question": "A motorboat whose speed is 15 km/hr in still water goes 30 km downstream and comes back in a total of 4 hours 30 minutes. The speed of the stream (in km/hr) is:", "options": ["4", "5", "6", "10"], "answer": "5", "explanation": "30/(15+x) + 30/(15-x) = 4.5. Solving for x, we get x=5."},
    {"id": 113, "company": "Wipro", "topic": "Logical", "level": "Advanced", "question": "Find the missing number: 2, 6, 12, 20, 30, 42, ?", "options": ["50", "52", "54", "56"], "answer": "56", "explanation": "The differences are 4, 6, 8, 10, 12. Next difference is 14. 42 + 14 = 56."},

    # --- INFOSYS (Puzzles & Mathematical) ---
    {"id": 114, "company": "Infosys", "topic": "Arithmetic", "level": "Easy", "question": "A clock strikes once at 1 o’clock, twice at 2 o’clock, and so on. How many times will it strike in 24 hours?", "options": ["78", "156", "200", "300"], "answer": "156", "explanation": "Strikes in 12 hours = 1+2+...+12 = 78. In 24 hours = 78 * 2 = 156."},
    {"id": 115, "company": "Infosys", "topic": "Arithmetic", "level": "Medium", "question": "Find the number of ways in which 5 boys and 5 girls can be seated in a row so that no two girls are together.", "options": ["5! * 6!", "5! * 5!", "10!", "None"], "answer": "5! * 6!", "explanation": "Arrange 5 boys (5!). There are 6 gaps for 5 girls (6P5). Result: 5! * 6! / 1! = 5! * 6!."},
    {"id": 116, "company": "Infosys", "topic": "Arithmetic", "level": "Hard", "question": "If 1.5x = 0.04y, then the value of (y-x)/(y+x) is:", "options": ["73/77", "73/75", "70/77", "11/15"], "answer": "73/77", "explanation": "x/y = 0.04/1.5 = 4/150 = 2/75. Let x=2, y=75. (75-2)/(75+2) = 73/77."},
    {"id": 117, "company": "Infosys", "topic": "Puzzle", "level": "Advanced", "question": "There are 8 identical-looking gold coins, but one is fake and weighs slightly less. Using a balance scale, what is the minimum number of weighings to find it?", "options": ["2", "3", "4", "8"], "answer": "2", "explanation": "Group into 3, 3, 2. Weigh 3 vs 3. If equal, fake is in the 2. If unequal, fake is in the lighter 3. One more weighing confirms."},

    # --- ACCENTURE (Analytical & Critical) ---
    {"id": 118, "company": "Accenture", "topic": "Arithmetic", "level": "Easy", "question": "What is the value of 12.5% of 800?", "options": ["100", "125", "80", "160"], "answer": "100", "explanation": "12.5% is 1/8. 800 / 8 = 100."},
    {"id": 119, "company": "Accenture", "topic": "Logical", "level": "Medium", "question": "In a certain code, '256' means 'you are good', '637' means 'we are bad', and '358' means 'good and bad'. Which digit means 'and'?", "options": ["2", "5", "8", "3"], "answer": "8", "explanation": "Comparing 256 and 358, 'good' is 5. Comparing 637 and 358, 'bad' is 3. Remaining in 358 is 8, which means 'and'."},
    {"id": 120, "company": "Accenture", "topic": "Arithmetic", "level": "Hard", "question": "A sum of money at simple interest amounts to Rs. 2240 in 2 years and Rs. 2600 in 5 years. Find the interest rate.", "options": ["5%", "6%", "10%", "12%"], "answer": "6%", "explanation": "SI for 3 years = 2600-2240 = 360. SI for 1 year = 120. P = 2240 - (120*2) = 2000. R = (120/2000)*100 = 6%."},
    {"id": 121, "company": "Accenture", "topic": "Verbal", "level": "Advanced", "question": "Identify the synonym for 'Ephemeral':", "options": ["Eternal", "Short-lived", "Useless", "Beautiful"], "answer": "Short-lived", "explanation": "Ephemeral refers to something lasting for a very short time."},
{
    "id": 1,
    "topic": "Alligation or Mixture",
    "company": "HCL",
    "question": "In what ratio must a grocer mix two varieties of tea worth 60 per kg and 65 per kg so that by selling the mixture at 68.20 per kg he may gain 10%?",
    "options": ["3:2", "3:4", "3:5", "4:5"],
    "answer": "3:2",
    "explanation": "SP = 68.20, Profit = 10%. CP = (100/110) * 68.20 = 62. By Alligation: (65 - 62) : (62 - 60) = 3 : 2."
  },
  {
    "id": 2,
    "topic": "Permutation and Combination",
    "company": "Capgemini",
    "question": "How many 3-digit numbers can be formed from the digits 2, 3, 5, 6, 7 and 9, which are divisible by 5 and none of the digits is repeated?",
    "options": ["5", "10", "15", "20"],
    "answer": "20",
    "explanation": "For a number to be divisible by 5, the unit digit must be 5. Remaining 2 places can be filled by 5 remaining digits: 5 * 4 = 20."
  },
  {
    "id": 3,
    "topic": "Simple Interest",
    "company": "Tech Mahindra",
    "question": "A sum of money at simple interest amounts to 815 in 3 years and to 854 in 4 years. The sum is:",
    "options": ["650", "690", "698", "700"],
    "answer": "698",
    "explanation": "SI for 1 year = 854 - 815 = 39. SI for 3 years = 39 * 3 = 117. Principal = 815 - 117 = 698."
  },
  {
    "id": 4,
    "topic": "Time and Work",
    "company": "Mindtree",
    "question": "A is thrice as efficient as B and takes 60 days less than B to finish a work. In how many days can they finish it together?",
    "options": ["22 days", "22.5 days", "23 days", "25 days"],
    "answer": "22.5 days",
    "explanation": "Efficiency A:B = 3:1. Time A:B = 1:3. Difference 2 units = 60 days. A = 30, B = 90. Together = (30*90)/(30+90) = 22.5."
  },
  {
    "id": 5,
    "topic": "Logarithm",
    "company": "LTI",
    "question": "If log 2 = 0.30103, find the number of digits in 2^64.",
    "options": ["18", "19", "20", "21"],
    "answer": "20",
    "explanation": "log(2^64) = 64 * 0.30103 = 19.2659. Number of digits = Characteristic + 1 = 19 + 1 = 20."
  },
  {
    "id": 6,
    "topic": "Problems on Trains",
    "company": "DXC Technology",
    "question": "A train 125 m long passes a man, running at 5 kmph in the same direction in which the train is going, in 10 seconds. The speed of the train is:",
    "options": ["45 kmph", "50 kmph", "54 kmph", "55 kmph"],
    "answer": "50 kmph",
    "explanation": "Relative speed = 125/10 = 12.5 m/s = 45 kmph. Let train speed be x. x - 5 = 45 => x = 50 kmph."
  },
  {
    "id": 7,
    "topic": "Boats and Streams",
    "company": "Hexaware",
    "question": "A boat can travel with a speed of 13 kmph in still water. If the speed of the stream is 4 kmph, find the time taken by the boat to go 68 km downstream.",
    "options": ["2 hours", "3 hours", "4 hours", "5 hours"],
    "answer": "4 hours",
    "explanation": "Downstream speed = 13 + 4 = 17 kmph. Time = 68/17 = 4 hours."
  },
  {
    "id": 8,
    "topic": "Area",
    "company": "IBM",
    "question": "The diagonal of a rectangle is 17 cm long and its perimeter is 46 cm. The area of the rectangle is:",
    "options": ["100 cm²", "110 cm²", "120 cm²", "130 cm²"],
    "answer": "120 cm²",
    "explanation": "l + b = 23, l² + b² = 17² = 289. (l+b)² = l²+b²+2lb => 529 = 289 + 2lb => 2lb = 240 => lb = 120."
  },
  {
    "id": 9,
    "topic": "Percentage",
    "company": "Mphasis",
    "question": "If 20% of a = b, then b% of 20 is the same as:",
    "options": ["4% of a", "5% of a", "20% of a", "None"],
    "answer": "4% of a",
    "explanation": "b = 0.2a. b% of 20 = (b/100)*20 = (0.2a/100)*20 = 0.04a = 4% of a."
  },
  {
    "id": 10,
    "topic": "Problems on Ages",
    "company": "Virtusa",
    "question": "The ratio of present ages of P and Q is 3:4. 5 years ago, the ratio was 2:3. What is the present age of P?",
    "options": ["10", "12", "15", "20"],
    "answer": "15",
    "explanation": "(3x-5)/(4x-5) = 2/3. 9x - 15 = 8x - 10. x = 5. P = 3 * 5 = 15."
  },
  {
    "id": 11,
    "topic": "Decimal Fraction",
    "company": "CGI",
    "question": "The value of (0.1 * 0.1 * 0.1 + 0.02 * 0.02 * 0.02) / (0.2 * 0.2 * 0.2 + 0.04 * 0.04 * 0.04) is:",
    "options": ["0.125", "0.25", "0.5", "0.0625"],
    "answer": "0.125",
    "explanation": "The denominator is 2³ = 8 times the numerator. So, 1/8 = 0.125."
  },
  {
    "id": 12,
    "topic": "Average",
    "company": "Societe Generale",
    "question": "The average of 20 numbers is zero. Of them, at the most, how many may be greater than zero?",
    "options": ["0", "1", "10", "19"],
    "answer": "19",
    "explanation": "If 19 numbers are positive, the 20th number can be a negative value equal to the sum of the 19 numbers, making the total sum zero."
  },
  {
    "id": 13,
    "topic": "Compound Interest",
    "company": "Verizon",
    "question": "The compound interest on 30,000 at 7% per annum is 4347. The period (in years) is:",
    "options": ["2", "2.5", "3", "4"],
    "answer": "2",
    "explanation": "Amount = 34347. 30000(1.07)^n = 34347. (1.07)^n = 1.1449. Since 1.07 * 1.07 = 1.1449, n = 2."
  },
  {
    "id": 14,
    "topic": "HCF and LCM",
    "company": "Oracle",
    "question": "The HCF of two numbers is 11 and their LCM is 693. If one number is 77, find the other.",
    "options": ["88", "99", "101", "110"],
    "answer": "99",
    "explanation": "Product of numbers = HCF * LCM. 77 * x = 11 * 693. x = (11 * 693) / 77 = 99."
  },
  {
    "id": 15,
    "topic": "Probability",
    "company": "Goldman Sachs",
    "question": "In a box, there are 8 red, 7 blue and 6 green balls. One ball is picked up randomly. What is the probability that it is neither red nor green?",
    "options": ["1/3", "7/21", "8/21", "9/21"],
    "answer": "1/3",
    "explanation": "Neither red nor green means blue. Total balls = 21. Blue balls = 7. Prob = 7/21 = 1/3."
  },
  {
    "id": 16,
    "topic": "Profit and Loss",
    "company": "Amazon",
    "question": "If selling price is doubled, the profit triples. Find the profit percent.",
    "options": ["66.66%", "100%", "105%", "120%"],
    "answer": "100%",
    "explanation": "Let CP = x, SP = y. Profit = y - x. 3(y - x) = 2y - x => y = 2x. Profit = 2x - x = x. % = (x/x) * 100 = 100%."
  },
  {
    "id": 17,
    "topic": "Time and Distance",
    "company": "Microsoft",
    "question": "Excluding stoppages, the speed of a bus is 54 kmph and including stoppages, it is 45 kmph. For how many minutes does the bus stop per hour?",
    "options": ["9", "10", "12", "15"],
    "answer": "10",
    "explanation": "Time of rest = (Difference in speed / Speed without stoppages). (54-45)/54 = 9/54 = 1/6 hour = 10 minutes."
  },
  {
    "id": 18,
    "topic": "Surds and Indices",
    "company": "Google",
    "question": "If (1/5)^3y = 0.008, then the value of (0.25)^y is:",
    "options": ["0.25", "0.5", "0.625", "1"],
    "answer": "0.25",
    "explanation": "(0.2)^3y = (0.2)^3 => 3y = 3 => y = 1. (0.25)^1 = 0.25."
  },
  {
    "id": 19,
    "topic": "Simplification",
    "company": "Adobe",
    "question": "3/4 of 2/3 of 1/2 of 480 is:",
    "options": ["60", "120", "240", "300"],
    "answer": "120",
    "explanation": "(3/4) * (2/3) * (1/2) * 480 = (1/4) * 480 = 120."
  },
  {
    "id": 20,
    "topic": "Partnership",
    "company": "Samsung",
    "question": "A, B and C invest 2000, 3000 and 4000 in a business. After one year, the profit is 900. B's share is:",
    "options": ["200", "300", "400", "500"],
    "answer": "300",
    "explanation": "Ratio of investment = 2:3:4. Total parts = 9. B's share = (3/9) * 900 = 300."
  },
{"id": 1, "company": "TCS", "topic": "Arithmetic", "level": "Easy", "question": "What is the unit digit in (7^95 - 3^58)?", "options": ["0", "4", "6", "7"], "answer": "4", "explanation": "7^95 ends in 3, 3^58 ends in 9. 13-9=4."},
    {"id": 2, "company": "Virtusa", "topic": "Arithmetic", "level": "Medium", "question": "The ratio of present ages of P and Q is 3:4. 5 years ago, the ratio was 2:3. What is the present age of P?", "options": ["10", "12", "15", "20"], "answer": "15", "explanation": "3x-5/4x-5 = 2/3 => x=5. P=15."},
    {"id": 3, "company": "Accenture", "topic": "Arithmetic", "level": "Hard", "question": "A sum of money at CI amounts to thrice itself in 3 years. In how many years will it be 9 times itself?", "options": ["6", "9", "12", "15"], "answer": "6", "explanation": "3^1 in 3 yrs, 3^2 (9) in 3*2=6 yrs."},
    {"id": 4, "company": "Infosys", "topic": "Arithmetic", "level": "Easy", "question": "Find the HCF of 2/3, 8/9, 64/81.", "options": ["2/81", "2/3", "8/81", "1/3"], "answer": "2/81", "explanation": "HCF(num)/LCM(den) = 2/81."},
    
    # --- DATA INTERPRETATION ---
    {"id": 5, "company": "Virtusa", "topic": "Data Interpretation", "level": "Easy", "question": "In a pie chart, a sector represents 20% of the total. What is its central angle?", "options": ["36°", "72°", "90°", "108°"], "answer": "72°", "explanation": "20% of 360 = 0.2 * 360 = 72°."},
    {"id": 6, "company": "Wipro", "topic": "Data Interpretation", "level": "Medium", "question": "Revenue grew from 100Cr to 150Cr. What is the percentage increase?", "options": ["25%", "50%", "75%", "100%"], "answer": "50%", "explanation": "(50/100)*100 = 50%."},
    {"id": 7, "company": "Capgemini", "topic": "Data Interpretation", "level": "Hard", "question": "If the ratio of Import to Export is 0.65, and Imports are 650 units, what are Exports?", "options": ["1000", "800", "1200", "900"], "answer": "1000", "explanation": "650/x = 0.65 => x = 1000."},
    
    # --- LOGICAL REASONING ---
    {"id": 8, "company": "Cognizant", "topic": "Logical", "level": "Easy", "question": "Complete the series: 2, 6, 12, 20, 30, ?", "options": ["36", "40", "42", "48"], "answer": "42", "explanation": "Differences are 4, 6, 8, 10, 12. 30+12=42."},
    {"id": 9, "company": "HCL", "topic": "Logical", "level": "Medium", "question": "If 'CUP' is 40, what is 'KITE'?", "options": ["45", "48", "50", "52"], "answer": "45", "explanation": "Sum of alphabet positions: K(11)+I(9)+T(20)+E(5) = 45."},
    {"id": 10, "company": "IBM", "topic": "Logical", "level": "Hard", "question": "If A+B means A is daughter of B, A-B means A is husband of B, what does P-Q+R mean?", "options": ["P is father of Q", "P is son-in-law of R", "P is brother of R", "None"], "answer": "P is son-in-law of R", "explanation": "Q is daughter of R, P is husband of Q. So P is R's son-in-law."},
{"id": 11, "company": "TCS", "topic": "Arithmetic", "level": "Easy", "question": "What is the LCM of 12, 18, and 24?", "options": ["48", "72", "96", "120"], "answer": "72", "explanation": "12=2^2*3, 18=2*3^2, 24=2^3*3. LCM = 2^3 * 3^2 = 72."},
    {"id": 12, "company": "Infosys", "topic": "Arithmetic", "level": "Medium", "question": "A can do work in 10 days, B in 15 days. They work together for 2 days, then A leaves. How long for B to finish?", "options": ["8 days", "10 days", "12 days", "15 days"], "answer": "10 days", "explanation": "Combined 1-day work = 1/10 + 1/15 = 1/6. 2 days = 1/3. Remaining 2/3 done by B in (2/3)*15 = 10 days."},
    {"id": 13, "company": "Wipro", "topic": "Arithmetic", "level": "Hard", "question": "A sum of money doubles itself in 10 years at SI. In how many years will it triple?", "options": ["15", "20", "25", "30"], "answer": "20", "explanation": "To double, SI=P. To triple, SI=2P. If P takes 10 years, 2P takes 20 years."},
    {"id": 14, "company": "Virtusa", "topic": "Arithmetic", "level": "Easy", "question": "What is 15% of 200?", "options": ["20", "30", "40", "50"], "answer": "30", "explanation": "0.15 * 200 = 30."},
    
    # --- DATA INTERPRETATION (Focusing on Virtusa/TCS) ---
    {"id": 15, "company": "Virtusa", "topic": "Data Interpretation", "level": "Medium", "question": "In a bar graph, if X-axis represents Years and Y-axis represents Sales (in millions), and Sales for 2024 is 40 and 2025 is 60, what is the growth rate?", "options": ["20%", "40%", "50%", "60%"], "answer": "50%", "explanation": "Growth = (60-40)/40 = 20/40 = 50%."},
    {"id": 16, "company": "TCS", "topic": "Data Interpretation", "level": "Hard", "question": "A table shows students in 3 streams: Sci(120), Com(80), Arts(100). What percentage of total students are in Commerce?", "options": ["25.6%", "26.6%", "30%", "33%"], "answer": "26.6%", "explanation": "80 / (120+80+100) = 80/300 = 26.6%."},
    {"id": 17, "company": "Capgemini", "topic": "Data Interpretation", "level": "Easy", "question": "If 360 degrees in a pie chart equals $5000, how much does 90 degrees represent?", "options": ["$1000", "$1250", "$1500", "$2000"], "answer": "$1250", "explanation": "(90/360) * 5000 = 1/4 * 5000 = 1250."},

    # --- LOGICAL REASONING ---
    {"id": 18, "company": "Accenture", "topic": "Logical", "level": "Medium", "question": "In a certain code, 'ORANGE' is 'PSBOHF'. What is 'APPLE'?", "options": ["BQQMF", "BPQMF", "BQQNF", "BRQMF"], "answer": "BQQMF", "explanation": "Each letter is shifted +1 (A->B, P->Q, etc.)."},
    {"id": 19, "company": "IBM", "topic": "Logical", "level": "Hard", "question": "Pointing to a man, a woman says, 'His mother is the only daughter of my mother.' How is the woman related to the man?", "options": ["Sister", "Mother", "Grandmother", "Aunt"], "answer": "Mother", "explanation": "'Only daughter of my mother' is the woman herself. So, she is the man's mother."},
    {"id": 20, "company": "HCL", "topic": "Logical", "level": "Easy", "question": "Odd one out: 64, 125, 216, 343, 512, 721", "options": ["343", "512", "721", "216"], "answer": "721", "explanation": "All others are perfect cubes (4^3, 5^3, etc.). 721 is not."},
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
    target_comp = st.selectbox("🎯 Target Company", ["All"] + list(sorted(set(q["company"] for q in QUESTIONS))))
with col_b:
    target_topic = st.selectbox("📚 Topic", ["All"] + list(sorted(set(q["topic"] for q in QUESTIONS))))
with col_c:
    target_level = st.select_slider("⚡ Difficulty", options=["Easy", "Medium", "Hard"])

# Filter Logic
pool = [q for q in QUESTIONS if 
        (target_comp == "All" or q["company"] == target_comp) and 
        (target_topic == "All" or q["topic"] == target_topic) and
        (q.get("level") == target_level)]

if not pool:
    st.warning("No questions match your specific level filter for this company/topic. Showing all levels for your selection instead.")
    pool = [q for q in QUESTIONS if 
        (target_comp == "All" or q["company"] == target_comp) and 
        (target_topic == "All" or q["topic"] == target_topic)]

if not pool:
    st.error("No questions match your elite filters. Try broadening your search.")
elif st.session_state.q_idx < len(pool):
    q = pool[st.session_state.q_idx]
    
    st.markdown(f"### Question {st.session_state.q_idx + 1}")
    with st.container():
        st.info(f"**Company:** {q['company']} | **Difficulty:** {q['level']} | **Topic:** {q['topic']}")
        st.write(f"#### {q['question']}")
        
        user_choice = st.radio("Choose the correct option:", q["options"], key=f"choice_{st.session_state.q_idx}_{q['id']}")

        if st.button("Validate Answer") or st.session_state.ans_submitted:
            st.session_state.ans_submitted = True
            if user_choice == q["answer"]:
                st.success("🎯 Correct! You're on track for selection.")
                if f"counted_{st.session_state.q_idx}" not in st.session_state:
                    st.session_state.session_score += 1
                    st.session_state[f"counted_{st.session_state.q_idx}"] = True
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
    st.success(f"Session Complete! Accuracy: {score_pct:.1f}%")
    
    if st.button("Save to Career Profile"):
        user_data["history"].append({
            "date": str(date.today()),
            "score_pct": score_pct,
            "company": target_comp
        })
        save_data(user_data)
        st.session_state.q_idx = 0
        st.session_state.session_score = 0
        st.session_state.ans_submitted = False
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
