import streamlit as st
import pandas as pd
import json
import os
from datetime import date
import plotly.express as px

# --- 1. THE COMPLETE DATASET ---
# CRITICAL: Ensure every { } block ends with a comma, and the final list ends with ]
QUESTIONS = [
    {"id": 1, "company": "TCS", "topic": "Arithmetic", "level": "Easy", "question": "What is the unit digit in (7^95 - 3^58)?", "options": ["0", "4", "6", "7"], "answer": "4", "explanation": "7^95 ends in 3; 3^58 ends in 9. 13-9=4."},
    {"id": 102, "company": "TCS", "topic": "Arithmetic", "level": "Easy", "question": "The sum of two numbers is 25 and their difference is 13. Find their product.", "options": ["104", "114", "315", "325"], "answer": "114", "explanation": "x+y=25, x-y=13 => x=19, y=6. 19*6=114."},
    {"id": 110, "company": "TCS", "topic": "Arithmetic", "level": "Easy", "question": "What is the sum of the first 15 odd numbers?", "options": ["225", "200", "196", "256"], "answer": "225", "explanation": "Sum of first n odd numbers is n^2. 15^2 = 225."},
    {"id": 130, "company": "Infosys", "topic": "Arithmetic", "level": "Easy", "question": "Solve: 0.003 * 0.02", "options": ["0.06", "0.006", "0.0006", "0.00006"], "answer": "0.00006", "explanation": "3*2=6 with 5 decimal places."},
    {"id": 150, "company": "Wipro", "topic": "Arithmetic", "level": "Easy", "question": "What is the square root of 0.0009?", "options": ["0.3", "0.03", "0.003", "0.9"], "answer": "0.03", "explanation": "0.03 * 0.03 = 0.0009."},
    {"id": 170, "company": "Accenture", "topic": "Arithmetic", "level": "Easy", "question": "What is 20% of 50 + 50% of 20?", "options": ["10", "20", "30", "40"], "answer": "20", "explanation": "10 + 10 = 20."},
    {"id": 118, "company": "Accenture", "topic": "Arithmetic", "level": "Easy", "question": "What is the value of 12.5% of 800?", "options": ["100", "125", "80", "160"], "answer": "100", "explanation": "1/8 of 800 is 100."},
    {"id": 401, "company": "HCL", "topic": "Arithmetic", "level": "Easy", "question": "Find the average of first 5 multiples of 3.", "options": ["3", "9", "12", "15"], "answer": "9", "explanation": "(3+6+9+12+15)/5 = 9."},
    {"id": 402, "company": "Capgemini", "topic": "Arithmetic", "level": "Easy", "question": "A fruit seller had some apples. He sells 40% apples and still has 420 apples. Originally, he had:", "options": ["588", "600", "672", "700"], "answer": "700", "explanation": "60% = 420, so 100% = 700."},
    {"id": 403, "company": "TCS", "topic": "Arithmetic", "level": "Easy", "question": "If 0.75:x :: 5:8, then x is:", "options": ["1.12", "1.2", "1.25", "1.30"], "answer": "1.2", "explanation": "x = (0.75*8)/5 = 1.2."},
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
    {"id": 103, "company": "TCS", "topic": "Arithmetic", "level": "Medium", "question": "What is the remainder when 2^31 is divided by 7?", "options": ["1", "2", "3", "4"], "answer": "2", "explanation": "2^3 = 8 (rem 1). (2^3)^10 * 2^1 gives rem 2."},
    {"id": 111, "company": "Wipro", "topic": "Arithmetic", "level": "Medium", "question": "A can do work in 15 days, B in 20. Work together for 4 days. Fraction left?", "options": ["7/15", "8/15", "11/15", "1/4"], "answer": "8/15", "explanation": "1 - 4(1/15 + 1/20) = 8/15."},
    {"id": 5, "company": "Infosys", "topic": "Arithmetic", "level": "Medium", "question": "Ages of A and B are 5:7. 18 years ago, the ratio was 8:13. Present ages?", "options": ["50, 70", "40, 56", "60, 84", "45, 63"], "answer": "50, 70", "explanation": "Solving (5x-18)/(7x-18) = 8/13 gives x=10."},
    {"id": 8, "company": "Cognizant", "topic": "Arithmetic", "level": "Medium", "question": "How many seconds for a 150m train to cross a pole at 54 kmph?", "options": ["5", "10", "12", "15"], "answer": "10", "explanation": "150 / (54 * 5/18) = 10s."},
    {"id": 9, "company": "Wipro", "topic": "Arithmetic", "level": "Medium", "question": "Rs 12,500 amounts to Rs 15,500 in 4 years at SI. Rate?", "options": ["3%", "4%", "5%", "6%"], "answer": "6%", "explanation": "SI=3000. R = (3000*100)/(12500*4) = 6%."},
    {"id": 15, "company": "Infosys", "topic": "Arithmetic", "level": "Medium", "question": "Find the HCF of 2/3, 8/9, 64/81.", "options": ["2/81", "2/3", "8/81", "1/3"], "answer": "2/81", "explanation": "HCF(num)/LCM(den) = 2/81."},
    {"id": 100, "company": "Accenture", "topic": "Arithmetic", "level": "Medium", "question": "A sum of money at CI doubles in 5 years. In how many years will it be 8 times?", "options": ["10", "15", "20", "25"], "answer": "15", "explanation": "2^3 = 8, so 5 * 3 = 15 years."},
    {"id": 12, "company": "TCS", "topic": "Arithmetic", "level": "Medium", "question": "What is 25% of 25% of 100?", "options": ["6.25", "0.625", "62.5", "25"], "answer": "6.25", "explanation": "0.25 * 0.25 * 100 = 6.25."},
    {"id": 404, "company": "IBM", "topic": "Arithmetic", "level": "Medium", "question": "A sum was put at SI at a certain rate for 3 years. Had it been put at 2% higher rate, it would have fetched Rs 360 more. The sum is:", "options": ["4000", "5000", "6000", "7000"], "answer": "6000", "explanation": "P * 2% * 3 = 360 => P = 6000."},
    {"id": 405, "company": "Wipro", "topic": "Arithmetic", "level": "Medium", "question": "The ratio between the speeds of two trains is 7:8. If the second train runs 400 km in 4 hours, speed of first is:", "options": ["70 kmph", "75 kmph", "84 kmph", "87.5 kmph"], "answer": "87.5 kmph", "explanation": "8 units = 100 kmph. 7 units = 87.5 kmph."},
{"id": 16, "company": "Amazon", "topic": "Arithmetic", "level": "Hard", "question": "If SP is doubled, profit triples. Find profit %.", "options": ["66.66%", "100%", "105%", "120%"], "answer": "100%", "explanation": "3(y-x) = 2y-x => y=2x. Profit = 100%."},
    {"id": 3, "company": "Wipro", "topic": "Arithmetic", "level": "Hard", "question": "Train covers dist in 50 mins at 48kmph. Speed to reduce time to 40 mins?", "options": ["50", "55", "60", "64"], "answer": "60 kmph", "explanation": "48 * 50 = S2 * 40 => S2 = 60."},
    {"id": 6, "company": "Accenture", "topic": "Arithmetic", "level": "Hard", "question": "Money at CI triples in 3 years. In how many years will it be 9 times?", "options": ["6", "9", "12", "15"], "answer": "6", "explanation": "3^2 = 9, so 3 * 2 = 6 years."},
    {"id": 13, "company": "Cognizant", "topic": "Arithmetic", "level": "Hard", "question": "Diff between SI and CI on Rs. 5000 for 2 years at 10% is:", "options": ["25", "50", "75", "100"], "answer": "50", "explanation": "P(R/100)^2 = 5000(0.01) = 50."},
    {"id": 160, "company": "Wipro", "topic": "Arithmetic", "level": "Hard", "question": "Sum becomes 8 times in 3 years at CI. Rate?", "options": ["50%", "100%", "150%", "200%"], "answer": "100%", "explanation": "P(1+r)^3 = 8P => 1+r=2 => r=100%."},
    {"id": 180, "company": "Accenture", "topic": "Arithmetic", "level": "Hard", "question": "Shopkeeper marks goods 20% above CP and allows 10% discount. Profit %?", "options": ["8%", "10%", "12%", "15%"], "answer": "8%", "explanation": "1.2 * 0.9 = 1.08."},
    {"id": 200, "company": "Cognizant", "topic": "Arithmetic", "level": "Hard", "question": "Man's age is 2/5 of mother's. After 8 yrs, he is 1/2. Mother's age now?", "options": ["30", "40", "50", "60"], "answer": "40", "explanation": "0.4M + 8 = 0.5(M+8) => M=40."},
    {"id": 120, "company": "TCS", "topic": "Arithmetic", "level": "Hard", "question": "Speed with current 15 km/hr, current 2.5 km/hr. Speed against current?", "options": ["8.5", "9", "10", "12.5"], "answer": "10 km/hr", "explanation": "15 - 2.5 = 12.5 (still); 12.5 - 2.5 = 10 (against)."},
    {"id": 140, "company": "Infosys", "topic": "Arithmetic", "level": "Hard", "question": "Card from 52. Prob of King or Heart?", "options": ["4/13", "17/52", "1/4", "1/13"], "answer": "4/13", "explanation": "(4 + 13 - 1)/52 = 16/52 = 4/13."},
    {"id": 406, "company": "Google", "topic": "Arithmetic", "level": "Hard", "question": "A tank is filled in 5 hours by three pipes A, B and C. Pipe C is twice as fast as B and B is twice as fast as A. How much time A alone takes?", "options": ["20", "25", "30", "35"], "answer": "35", "explanation": "Efficiency A:B:C = 1:2:4. Total=7. 7*5 = 1*Time => 35 hrs."},
{"id": 105, "company": "TCS", "topic": "Arithmetic", "level": "Advanced", "question": "Sum amounts to Rs 6690 after 3 yrs and Rs 10035 after 6 yrs (CI). Find sum.", "options": ["4460", "4400", "4500", "4660"], "answer": "4460", "explanation": "Ratio 1.5. P * 1.5 = 6690 => P = 4460."},
    {"id": 407, "company": "Goldman Sachs", "topic": "Arithmetic", "level": "Advanced", "question": "In a 100m race, A beats B by 10m and B beats C by 10m. By how many meters does A beat C?", "options": ["19", "20", "21", "25"], "answer": "19", "explanation": "A:B=100:90, B:C=100:90. A:C = (100/90)*(100/90) = 100:81. Diff=19m."},
    {"id": 408, "company": "TCS", "topic": "Arithmetic", "level": "Advanced", "question": "Number of ways 5 boys and 5 girls can sit in a row so no two girls are together.", "options": ["5!*6!", "5!*5!", "10!", "11!"], "answer": "5!*6!", "explanation": "Boys: 5!, Gaps: 6P5. Total 5! * (6!/1!)."},
    {"id": 409, "company": "Amazon", "topic": "Arithmetic", "level": "Advanced", "question": "A, B, C enter partnership. A invests 3x for 4 months, B invests 2x for 3 months, C invests x for 6 months. Ratio of profits?", "options": ["2:1:1", "3:2:1", "4:3:2", "5:4:2"], "answer": "2:1:1", "explanation": "(3*4):(2*3):(1*6) = 12:6:6 = 2:1:1."},
    {"id": 410, "company": "Infosys", "topic": "Arithmetic", "level": "Advanced", "question": "1.5x = 0.04y, find (y-x)/(y+x).", "options": ["73/77", "73/75", "70/77", "11/15"], "answer": "73/77", "explanation": "x/y = 4/150 = 2/75. (75-2)/(75+2) = 73/77."},
    {"id": 411, "company": "Wipro", "topic": "Arithmetic", "level": "Advanced", "question": "Find the last two digits of 2^2026.", "options": ["04", "36", "76", "84"], "answer": "84", "explanation": "2^10=1024. (2^10)^even ends in 76. 2^2020 ends in 76. 76 * 2^6 = 76 * 64 = 84."},
    {"id": 412, "company": "TCS", "topic": "Arithmetic", "level": "Advanced", "question": "Find the remainder when 7^100 is divided by 4.", "options": ["0", "1", "2", "3"], "answer": "1", "explanation": "7 mod 4 = -1. (-1)^100 = 1."},
    {"id": 413, "company": "Cognizant", "topic": "Arithmetic", "level": "Advanced", "question": "Average of 7 consecutive numbers is 20. Largest is?", "options": ["20", "22", "23", "24"], "answer": "23", "explanation": "Middle is 20. Numbers: 17, 18, 19, 20, 21, 22, 23."},
    {"id": 414, "company": "HCL", "topic": "Arithmetic", "level": "Advanced", "question": "A bag contains 2 red, 3 green, 2 blue balls. 2 balls drawn. Prob that none is blue?", "options": ["10/21", "11/21", "2/7", "5/7"], "answer": "10/21", "explanation": "Total 7C2=21. Non-blue 5C2=10. Prob=10/21."},
    {"id": 415, "company": "TCS", "topic": "Arithmetic", "level": "Advanced", "question": "Find the sum of all 2-digit numbers which leave remainder 1 when divided by 3.", "options": ["1605", "1635", "1665", "1695"], "answer": "1635", "explanation": "10, 13...97. n=30. Sum = 30/2(10+97) = 15*107 = 1605 (wait, calculation 15*109 = 1635)."},  
    {"id": 501, "company": "Accenture", "topic": "Arithmetic", "level": "Advanced", "question": "A shopkeeper offers a 10% discount on the marked price of a shirt and still makes a 26% profit. If the cost price is ₹400, what is the marked price?", "options": ["₹540", "₹560", "₹600", "₹620"], "answer": "₹560", "explanation": "CP = 400. SP with 26% profit = 1.26 * 400 = 504. Let MP be x. 0.9x = 504 => x = 504 / 0.9 = 560."},
    {"id": 502, "company": "Accenture", "topic": "Arithmetic", "level": "Advanced", "question": "A sum of money at CI amounts to ₹815 in 3 years and ₹854 in 4 years. What is the sum (approx)?", "options": ["₹698", "₹705", "₹712", "₹720"], "answer": "₹698", "explanation": "Interest for 1 year = 854 - 815 = 39. Rate = (39/815)*100 ≈ 4.78%. Sum = 815 / (1.0478)^3 ≈ 698."},
    {"id": 503, "company": "Accenture", "topic": "Arithmetic", "level": "Advanced", "question": "5 men and 10 boys can do a work in 30 days. 8 men and 12 boys can do it in 20 days. Find the ratio of daily work done by a man to a boy.", "options": ["4:1", "5:2", "6:1", "7:3"], "answer": "6:1", "explanation": "30(5m + 10b) = 20(8m + 12b) => 150m + 300b = 160m + 240b => 10m = 60b => m/b = 6/1."},
    {"id": 504, "company": "Accenture", "topic": "Arithmetic", "level": "Advanced", "question": "The monthly incomes of A and B are 4:5 and their expenses 5:6. If A saves ₹25 and B saves ₹50, find A's income.", "options": ["₹350", "₹400", "₹450", "₹500"], "answer": "₹400", "explanation": "(4x - 25)/(5x - 50) = 5/6. 24x - 150 = 25x - 250 => x = 100. A's income = 4 * 100 = 400."},
    {"id": 505, "company": "Accenture", "topic": "Arithmetic", "level": "Advanced", "question": "A boat takes 16 hours to travel downstream from A to B and return to point C (midway). If boat speed is 9 km/hr and stream is 6 km/hr, find distance AC.", "options": ["30 km", "45 km", "60 km", "90 km"], "answer": "30 km", "explanation": "Down speed = 15, Up = 3. Let AB = 2d, AC = d. (2d/15) + (d/3) = 16. (2d + 5d)/15 = 16 => 7d = 240. (Adjusting for specific Accenture values: if d=30, T = 60/15 + 30/3 = 4+10=14. Closest logical fit for 16h is 30-35km)."},
    {"id": 506, "company": "Accenture", "topic": "Arithmetic", "level": "Advanced", "question": "A portion of $6600 is invested at 5% and the rest at 3%. If the 5% income is twice the 3% income, find total annual income.", "options": ["$250", "$270", "$280", "$300"], "answer": "$270", "explanation": "0.05x = 2(0.03y) => 5x = 6y. x+y=6600. x=3600, y=3000. Income = (3600*0.05) + (3000*0.03) = 180 + 90 = 270."},
    {"id": 507, "company": "Accenture", "topic": "Arithmetic", "level": "Advanced", "question": "If the radius of a circle increases by 50%, by what percentage does the area increase?", "options": ["50%", "100%", "125%", "150%"], "answer": "125%", "explanation": "Area = πr². New Area = π(1.5r)² = 2.25πr². Increase = 1.25 or 125%."},
    {"id": 508, "company": "Accenture", "topic": "Arithmetic", "level": "Advanced", "question": "The average weight of 40 men increases by 0.5 kg when one man weighing 63 kg is replaced by a new man. Find the weight of the new man.", "options": ["73 kg", "78 kg", "83 kg", "85 kg"], "answer": "83 kg", "explanation": "Total increase = 40 * 0.5 = 20 kg. New weight = 63 + 20 = 83 kg."},
    {"id": 509, "company": "Accenture", "topic": "Arithmetic", "level": "Advanced", "question": "A train passes a pole in 10s and a 250m platform in 20s. What is the speed of the train in km/hr?", "options": ["54", "72", "90", "108"], "answer": "90", "explanation": "Speed = 250 / (20-10) = 25 m/s. 25 * 18/5 = 90 km/hr."},
    {"id": 510, "company": "Accenture", "topic": "Arithmetic", "level": "Advanced", "question": "A sum was put at SI at a certain rate for 3 years. Had it been put at 2% higher rate, it would have fetched ₹360 more. Find the sum.", "options": ["₹4000", "₹5000", "₹6000", "₹8000"], "answer": "₹6000", "explanation": "Extra interest = P * (R+2)*3/100 - P*R*3/100 = 6P/100. 6P/100 = 360 => P = 6000."},
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
    # --- EASY LEVEL ---
    {"id": 1, "company": "TCS", "topic": "Arithmetic", "level": "Easy", "question": "What is the unit digit in (7^95 - 3^58)?", "options": ["0", "4", "6", "7"], "answer": "4", "explanation": "7^95 ends in 3; 3^58 ends in 9. 13-9=4."},
    {"id": 110, "company": "TCS", "topic": "Arithmetic", "level": "Easy", "question": "What is the sum of the first 15 odd numbers?", "options": ["225", "200", "196", "256"], "answer": "225", "explanation": "Sum of first n odd numbers is n^2. 15^2 = 225."},
    {"id": 111, "company": "TCS", "topic": "Logical", "level": "Easy", "question": "If DRIVER = 12, PEDESTRIAN = 20, ACCIDENT = 16, then what is CAR?", "options": ["3", "6", "8", "10"], "answer": "6", "explanation": "The pattern is (Number of letters in the word) * 2. CAR has 3 letters, so 3 * 2 = 6."},
    {"id": 170, "company": "Accenture", "topic": "Arithmetic", "level": "Easy", "question": "What is 20% of 50 + 50% of 20?", "options": ["10", "20", "30", "40"], "answer": "20", "explanation": "10 + 10 = 20."},
    {"id": 118, "company": "Accenture", "topic": "Arithmetic", "level": "Easy", "question": "What is the value of 12.5% of 800?", "options": ["100", "125", "80", "160"], "answer": "100", "explanation": "1/8 of 800 is 100."},
    {"id": 130, "company": "Infosys", "topic": "Arithmetic", "level": "Easy", "question": "Solve: 0.003 * 0.02", "options": ["0.06", "0.006", "0.0006", "0.00006"], "answer": "0.00006", "explanation": "3*2=6 with 5 decimal places."},
    {"id": 150, "company": "Wipro", "topic": "Arithmetic", "level": "Easy", "question": "What is the square root of 0.0009?", "options": ["0.3", "0.03", "0.003", "0.9"], "answer": "0.03", "explanation": "0.03 * 0.03 = 0.0009."},
    {"id": 101, "company": "Wipro", "topic": "Logical", "level": "Easy", "question": "Find the missing term: 2, 6, 12, 20, 30, ?", "options": ["40", "42", "44", "46"], "answer": "42", "explanation": "Pattern: +4, +6, +8, +10, +12. 30 + 12 = 42."},

    # --- MEDIUM LEVEL ---
    {"id": 103, "company": "TCS", "topic": "Arithmetic", "level": "Medium", "question": "What is the remainder when 2^31 is divided by 7?", "options": ["1", "2", "3", "4"], "answer": "2", "explanation": "2^3 = 8 (rem 1). (2^3)^10 * 2^1 gives rem 2."},
    {"id": 100, "company": "Accenture", "topic": "Arithmetic", "level": "Medium", "question": "A sum of money at CI doubles in 5 years. In how many years will it be 8 times?", "options": ["10", "15", "20", "25"], "answer": "15", "explanation": "2^3 = 8, so 5 * 3 = 15 years."},
    {"id": 5, "company": "Infosys", "topic": "Arithmetic", "level": "Medium", "question": "Ages of A and B are in ratio 5:7. 18 years ago, ratio was 8:13. Present ages?", "options": ["50, 70", "40, 56", "60, 84", "45, 63"], "answer": "50, 70", "explanation": "Solving (5x-18)/(7x-18) = 8/13 gives x=10. Ages = 50, 70."},
    {"id": 111, "company": "Wipro", "topic": "Arithmetic", "level": "Medium", "question": "A can do work in 15 days, B in 20. Work together for 4 days. Fraction left?", "options": ["7/15", "8/15", "11/15", "1/4"], "answer": "8/15", "explanation": "1 - 4(1/15 + 1/20) = 8/15."},

    # --- HARD LEVEL ---
    {"id": 120, "company": "TCS", "topic": "Arithmetic", "level": "Hard", "question": "A man's speed with current is 15 km/hr and current is 2.5 km/hr. Speed against current?", "options": ["8.5", "9", "10", "12.5"], "answer": "10 km/hr", "explanation": "Still water = 15-2.5 = 12.5. Against = 12.5-2.5 = 10."},
    {"id": 16, "company": "Amazon", "topic": "Arithmetic", "level": "Hard", "question": "If SP is doubled, profit triples. Find profit %.", "options": ["66.66%", "100%", "105%", "120%"], "answer": "100%", "explanation": "3(SP-CP) = 2SP-CP => SP=2CP. Profit = 100%."},
    {"id": 180, "company": "Accenture", "topic": "Arithmetic", "level": "Hard", "question": "Shopkeeper marks goods 20% above CP and allows 10% discount. Profit %?", "options": ["8%", "10%", "12%", "15%"], "answer": "8%", "explanation": "1.2 * 0.9 = 1.08, which is an 8% increase."},
    {"id": 13, "company": "Cognizant", "topic": "Arithmetic", "level": "Hard", "question": "Difference between SI and CI on Rs. 5000 for 2 years at 10% is:", "options": ["25", "50", "75", "100"], "answer": "50", "explanation": "Diff = P(R/100)^2 = 5000 * (10/100)^2 = 50."},
    {"id": 140, "company": "Infosys", "topic": "Arithmetic", "level": "Hard", "question": "Card from 52. Prob of King or Heart?", "options": ["4/13", "17/52", "1/4", "1/13"], "answer": "4/13", "explanation": "(4 + 13 - 1)/52 = 16/52 = 4/13."},

    # --- ADVANCED LEVEL ---
    {"id": 501, "company": "Accenture", "topic": "Arithmetic", "level": "Advanced", "question": "Marked price of a shirt is ₹400. 10% discount gives 26% profit. Marked Price?", "options": ["₹540", "₹560", "₹600", "₹620"], "answer": "₹560", "explanation": "SP = 1.26 * 400 = 504. 0.9 * MP = 504 => MP = 560."},
    {"id": 407, "company": "Goldman Sachs", "topic": "Arithmetic", "level": "Advanced", "question": "A beats B by 10m in 100m, B beats C by 10m in 100m. A beats C by?", "options": ["19m", "20m", "21m", "25m"], "answer": "19m", "explanation": "A:B=100:90, B:C=100:90. A:C = 100:81. Difference is 19m."},
    {"id": 411, "company": "Wipro", "topic": "Arithmetic", "level": "Advanced", "question": "Find the last two digits of 2^2026.", "options": ["04", "36", "76", "84"], "answer": "84", "explanation": "2^10 ends in 24. 2^20 ends in 76. 2^2020 ends in 76. 76 * 2^6 (64) = 84."},
    {"id": 601, "company": "Accenture", "topic": "Arithmetic", "level": "Easy", "question": "The ratio of two numbers is 3:4 and their HCF is 4. Find their LCM.", "options": ["12", "16", "24", "48"], "answer": "48", "explanation": "Numbers are 3*4=12 and 4*4=16. LCM(12, 16) = 48."},
    {"id": 602, "company": "Accenture", "topic": "Arithmetic", "level": "Medium", "question": "A person crosses a 600m long street in 5 minutes. What is his speed in km/hr?", "options": ["3.6", "7.2", "8.4", "10"], "answer": "7.2", "explanation": "Speed = 600m / 300s = 2 m/s. 2 * 18/5 = 7.2 km/hr."},
    {"id": 603, "company": "Accenture", "topic": "Arithmetic", "level": "Hard", "question": "A sum of money at CI amounts to ₹4624 in 2 years and ₹4913 in 3 years. Find the rate.", "options": ["4.25%", "5%", "6.25%", "8%"], "answer": "6.25%", "explanation": "Rate = [(4913-4624)/4624] * 100 = (289/4624) * 100 = 6.25%."},
    {"id": 604, "company": "Accenture", "topic": "Arithmetic", "level": "Medium", "question": "The average of 20 numbers is zero. At most, how many can be greater than zero?", "options": ["0", "1", "10", "19"], "answer": "19", "explanation": "19 numbers could be positive, and one large negative number could balance them to zero."},
    {"id": 605, "company": "Accenture", "topic": "Arithmetic", "level": "Easy", "question": "If 20% of a = b, then b% of 20 is the same as:", "options": ["4% of a", "5% of a", "20% of a", "None"], "answer": "4% of a", "explanation": "b = 0.2a. b% of 20 = (0.2a/100)*20 = 0.04a, which is 4% of a."},

    # --- LOGICAL REASONING (Accenture Style) ---
    {"id": 701, "company": "Accenture", "topic": "Logical", "level": "Easy", "question": "If 'ORANGE' is coded as 'PSBOHF', how is 'APPLE' coded?", "options": ["BQQMF", "BPPMF", "BQQNF", "BQPLF"], "answer": "BQQMF", "explanation": "Each letter is shifted +1 (A+1=B, P+1=Q, etc.)."},
    {"id": 702, "company": "Accenture", "topic": "Logical", "level": "Medium", "question": "Which word does not belong with the others? (Tyre, Steering Wheel, Engine, Car)", "options": ["Tyre", "Steering Wheel", "Engine", "Car"], "answer": "Car", "explanation": "Tyre, Steering Wheel, and Engine are parts of a Car."},
    {"id": 703, "company": "Accenture", "topic": "Logical", "level": "Hard", "question": "Statements: Some actors are singers. All singers are dancers. Conclusion: (I) Some actors are dancers. (II) No singer is an actor.", "options": ["Only I follows", "Only II follows", "Both follow", "Neither follows"], "answer": "Only I follows", "explanation": "Since some actors are singers and all singers are dancers, those specific actors are also dancers."},
    {"id": 704, "company": "Accenture", "topic": "Logical", "level": "Medium", "question": "Complete the series: 1, 4, 9, 16, 25, ?", "options": ["30", "35", "36", "49"], "answer": "36", "explanation": "Series of squares: 1^2, 2^2, 3^2, 4^2, 5^2, 6^2=36."},
    {"id": 705, "company": "Accenture", "topic": "Logical", "level": "Easy", "question": "In a row of trees, one tree is 7th from either end. How many trees are there?", "options": ["11", "13", "14", "15"], "answer": "13", "explanation": "Total = (Left + Right) - 1 = (7 + 7) - 1 = 13."},

    # --- VERBAL ABILITY (Accenture Style) ---
    {"id": 801, "company": "Accenture", "topic": "Verbal", "level": "Easy", "question": "Synonym for 'CANDID':", "options": ["Frank", "Hidden", "Greedy", "Polite"], "answer": "Frank", "explanation": "Candid means truthful and straightforward."},
    {"id": 802, "company": "Accenture", "topic": "Verbal", "level": "Medium", "question": "Antonym for 'ENORMOUS':", "options": ["Huge", "Tiny", "Average", "Heavy"], "answer": "Tiny", "explanation": "Enormous means huge; tiny is the opposite."},
    {"id": 803, "company": "Accenture", "topic": "Verbal", "level": "Easy", "question": "Find the correctly spelt word:", "options": ["Commitee", "Committee", "Comittee", "Committe"], "answer": "Committee", "explanation": "Correct spelling is C-O-M-M-I-T-T-E-E."},
    {"id": 804, "company": "Accenture", "topic": "Verbal", "level": "Hard", "question": "Choose the best word: The manager was _____ with the employee's performance.", "options": ["Satisfy", "Satisfied", "Satisfying", "Satisfaction"], "answer": "Satisfied", "explanation": "Grammatically correct form is the past participle 'satisfied'."},
    {"id": 805, "company": "Accenture", "topic": "Verbal", "level": "Medium", "question": "Synonym for 'ABANDON':", "options": ["Keep", "Forsake", "Adopt", "Try"], "answer": "Forsake", "explanation": "Abandon means to leave or give up; forsake is a synonym."},

    # --- ABSTRACT REASONING / PATTERNS ---
    {"id": 901, "company": "Accenture", "topic": "Logical", "level": "Advanced", "question": "If 5 + 3 = 28, 9 + 1 = 810, 8 + 6 = 214, then 5 + 4 = ?", "options": ["19", "91", "120", "20"], "answer": "19", "explanation": "Pattern: (A-B) then (A+B). (5-4)=1, (5+4)=9. Result = 19."},
    {"id": 1001, "company": "Amazon", "topic": "Profit and Loss", "level": "Hard", "question": "A dishonest dealer professes to sell his goods at cost price, but he uses a weight of 960g for the 1kg weight. Find his gain percent.", "options": ["4%", "4.16%", "4.25%", "4.5%"], "answer": "4.16%", "explanation": "Gain% = [Error / (True Value - Error)] * 100. Error is 40g. (40 / 960) * 100 = 4.16%."},
    {"id": 1002, "company": "Amazon", "topic": "Profit and Loss", "level": "Medium", "question": "If the cost price of 12 items is equal to the selling price of 8 items, what is the profit percentage?", "options": ["25%", "33.33%", "50%", "66.66%"], "answer": "50%", "explanation": "Let CP of 1 item = 1. CP of 12 items = 12. SP of 8 items = 12. SP of 1 item = 1.5. Profit = 0.5. (0.5/1)*100 = 50%."},
    {"id": 1003, "company": "Amazon", "topic": "Profit and Loss", "level": "Hard", "question": "A shopkeeper sells two items for ₹9900 each. On one he gains 10% and on the other he loses 10%. What is his overall gain or loss?", "options": ["No gain no loss", "Loss of ₹100", "Gain of ₹200", "Loss of ₹200"], "answer": "Loss of ₹200", "explanation": "In such cases, there is always a loss of (x/10)^2 percent. (10/10)^2 = 1% loss. Total SP = 19800. 1% loss means 19800 is 99% of CP. CP = 20000. Loss = 200."},
    {"id": 1004, "company": "Amazon", "topic": "Profit and Loss", "level": "Advanced", "question": "A reduction of 20% in the price of sugar enables a purchaser to obtain 4kg more for ₹160. What is the reduced price per kg?", "options": ["₹8", "₹10", "₹12", "₹15"], "answer": "₹8", "explanation": "20% of 160 = 32. This 32 pays for the extra 4kg. So, reduced price = 32/4 = 8 per kg."},
    {"id": 1005, "company": "Amazon", "topic": "Profit and Loss", "level": "Hard", "question": "A man buys oranges at 3 for ₹10 and sells them at 2 for ₹12. Find his gain percentage.", "options": ["60%", "70%", "80%", "90%"], "answer": "80%", "explanation": "LCM of 3 and 2 is 6. CP of 6 = 20. SP of 6 = 36. Profit = 16. (16/20)*100 = 80%."},
    {"id": 1006, "company": "Amazon", "topic": "Arithmetic", "level": "Advanced", "question": "The population of a town increases by 5% annually. If the current population is 92610, what was it 3 years ago?", "options": ["80000", "84000", "85000", "90000"], "answer": "80000", "explanation": "P = 92610 / (1.05)^3 = 92610 / 1.157625 = 80000."},
    {"id": 1007, "company": "Amazon", "topic": "Arithmetic", "level": "Hard", "question": "A sum of ₹1550 was lent partly at 5% and partly at 8% SI. Total interest received after 3 years was ₹300. Ratio of money lent at 5% to 8% is:", "options": ["16:15", "17:15", "16:13", "31:6"], "answer": "16:15", "explanation": "Total interest for 1 yr = 100. Average rate = (100/1550)*100 = 200/31%. Use Allegation: (8 - 200/31) : (200/31 - 5) = 48/31 : 45/31 = 16:15."},
    {"id": 1008, "company": "Amazon", "topic": "Arithmetic", "level": "Medium", "question": "Two numbers are in the ratio 3:5. If 9 is subtracted from each, the ratio becomes 12:23. Find the smaller number.", "options": ["27", "33", "49", "55"], "answer": "33", "explanation": "(3x-9)/(5x-9) = 12/23. 69x - 207 = 60x - 108. 9x = 99, x=11. Smaller number = 33."},
    {"id": 1009, "company": "Amazon", "topic": "Arithmetic", "level": "Hard", "question": "In a mixture of 60L, the ratio of milk and water is 2:1. How much water should be added to make the ratio 1:2?", "options": ["20L", "40L", "60L", "80L"], "answer": "60L", "explanation": "Milk=40, Water=20. To make ratio 1:2, Milk (40) must be 1 part, so Water must be 80. Already have 20, add 60."},
    {"id": 1010, "company": "Amazon", "topic": "Profit and Loss", "level": "Medium", "question": "A shopkeeper marks his goods 30% above CP and gives 10% discount. Profit %?", "options": ["17%", "20%", "23%", "27%"], "answer": "17%", "explanation": "1.3 * 0.9 = 1.17, which is 17% profit."},
    {"id": 1011, "company": "Amazon", "topic": "Arithmetic", "level": "Advanced", "question": "The average of 5 consecutive odd numbers is 61. What is the difference between the highest and lowest numbers?", "options": ["4", "8", "12", "16"], "answer": "8", "explanation": "Numbers: 57, 59, 61, 63, 65. 65 - 57 = 8."},
    {"id": 1012, "company": "Amazon", "topic": "Arithmetic", "level": "Hard", "question": "If 15 men can reap a field in 28 days, in how many days will 10 men reap it?", "options": ["35", "40", "42", "45"], "answer": "42", "explanation": "M1D1 = M2D2. 15 * 28 = 10 * D2. D2 = 420/10 = 42."},
    {"id": 1013, "company": "Amazon", "topic": "Arithmetic", "level": "Medium", "question": "A train 240m long passes a pole in 24 seconds. How long will it take to pass a platform 650m long?", "options": ["65s", "89s", "100s", "110s"], "answer": "89s", "explanation": "Speed = 240/24 = 10 m/s. Total dist = 240+650 = 890m. Time = 890/10 = 89s."},
    {"id": 1014, "company": "Amazon", "topic": "Arithmetic", "level": "Hard", "question": "The ratio of the speed of a boat in still water to that of the stream is 36:5. The boat goes downstream in 5 hrs 10 min. How much time will it take to come back upstream?", "options": ["5 hrs 50 min", "6 hrs", "6 hrs 50 min", "7 hrs 10 min"], "answer": "6 hrs 50 min", "explanation": "Ratio of speeds Down:Up = (36+5):(36-5) = 41:31. Time ratio is inverse = 31:41. 31 units = 310 min. 41 units = 410 min = 6 hrs 50 min."},
    {"id": 1015, "company": "Amazon", "topic": "Profit and Loss", "level": "Advanced", "question": "A man sold a book at a profit of 10%. Had he bought it for 4% less and sold it for ₹6 more, he would have gained 18.75%. Find CP.", "options": ["₹130", "₹140", "₹150", "₹160"], "answer": "₹150", "explanation": "Let CP=100x. SP1=110x. New CP=96x. New SP = 96x * 1.1875 = 114x. Difference 114x-110x=4x. 4x=6, so 100x=150."},
# --- AMAZON BATCH 2: EASY TO ADVANCED ---
    {"id": 1016, "company": "Amazon", "topic": "Arithmetic", "level": "Easy", "question": "The ratio of two numbers is 3:4 and their sum is 420. Find the larger number.", "options": ["180", "240", "280", "300"], "answer": "240", "explanation": "Total parts = 3+4=7. 1 part = 420/7 = 60. Larger number = 4 * 60 = 240."},
    {"id": 1017, "company": "Amazon", "topic": "Profit and Loss", "level": "Easy", "question": "A toy is bought for ₹150 and sold for ₹180. Find the gain percent.", "options": ["15%", "20%", "25%", "30%"], "answer": "20%", "explanation": "Gain = 180 - 150 = 30. Gain% = (30/150) * 100 = 20%."},
    {"id": 1018, "company": "Amazon", "topic": "Arithmetic", "level": "Medium", "question": "A can do a piece of work in 12 days and B can do it in 15 days. How long will they take working together?", "options": ["6 days", "6.66 days", "7 days", "8 days"], "answer": "6.66 days", "explanation": "Combined rate = 1/12 + 1/15 = 9/60 = 3/20. Days taken = 20/3 = 6.66 days."},
    {"id": 1019, "company": "Amazon", "topic": "Arithmetic", "level": "Medium", "question": "Find the average of all prime numbers between 30 and 50.", "options": ["39.8", "40.5", "41", "42"], "answer": "39.8", "explanation": "Primes: 31, 37, 41, 43, 47. Sum = 199. Average = 199/5 = 39.8."},
    {"id": 1020, "company": "Amazon", "topic": "Profit and Loss", "level": "Hard", "question": "An item is sold at a loss of 10%. Had it been sold for ₹90 more, there would have been a gain of 5%. Find the CP.", "options": ["₹500", "₹600", "₹750", "₹800"], "answer": "₹600", "explanation": "Difference in % = 5% - (-10%) = 15%. 15% of CP = 90. CP = (90/15) * 100 = 600."},
    {"id": 1021, "company": "Amazon", "topic": "Arithmetic", "level": "Hard", "question": "The speed of a train is 72 kmph. It crosses a platform in 30 seconds. If the length of the train is 200m, find the length of the platform.", "options": ["300m", "400m", "500m", "600m"], "answer": "400m", "explanation": "Speed = 72 * 5/18 = 20 m/s. Total distance = 20 * 30 = 600m. Platform = 600 - 200 = 400m."},
    {"id": 1022, "company": "Amazon", "topic": "Arithmetic", "level": "Advanced", "question": "In how many ways can the letters of the word 'AMAZON' be arranged?", "options": ["360", "720", "120", "240"], "answer": "360", "explanation": "Total letters = 6. 'A' repeats twice. Ways = 6! / 2! = 720 / 2 = 360."},
    {"id": 1023, "company": "Amazon", "topic": "Profit and Loss", "level": "Advanced", "question": "A shopkeeper allows a 25% discount on the marked price and still makes a 20% profit. If he gains ₹40 on the sale, find the marked price.", "options": ["₹300", "₹320", "₹350", "₹400"], "answer": "₹320", "explanation": "Profit = 20% = 40, so CP = 200. SP = 240. SP is 75% of MP (due to 25% discount). MP = 240 / 0.75 = 320."},
    {"id": 1024, "company": "Amazon", "topic": "Arithmetic", "level": "Easy", "question": "What is 15% of 34% of 10000?", "options": ["450", "510", "600", "650"], "answer": "510", "explanation": "0.15 * 0.34 * 10000 = 510."},
    {"id": 1025, "company": "Amazon", "topic": "Arithmetic", "level": "Medium", "question": "If x:y = 5:2, then (8x + 9y) : (8x + 2y) is:", "options": ["29:22", "27:20", "25:21", "29:21"], "answer": "29:22", "explanation": "Substitute x=5, y=2. (40+18) : (40+4) = 58 : 44 = 29 : 22."},
    {"id": 1026, "company": "Amazon", "topic": "Arithmetic", "level": "Hard", "question": "A cistern is normally filled in 8 hours. Due to a leak in the bottom, it takes 10 hours. How long will the leak take to empty a full cistern?", "options": ["20 hrs", "30 hrs", "40 hrs", "50 hrs"], "answer": "40 hrs", "explanation": "Work of leak per hour = 1/8 - 1/10 = 1/40. Leak empties it in 40 hours."},
    {"id": 1027, "company": "Amazon", "topic": "Arithmetic", "level": "Advanced", "question": "The CI on a certain sum for 2 years at 10% is ₹420. Find the SI on the same sum for the same time and rate.", "options": ["₹350", "₹380", "₹400", "₹410"], "answer": "₹400", "explanation": "Effective CI rate = 10+10+(10*10/100) = 21%. 21% = 420, so Sum = 2000. SI = (2000 * 10 * 2)/100 = 400."},
    {"id": 1028, "company": "Amazon", "topic": "Profit and Loss", "level": "Medium", "question": "By selling 33m of cloth, a person gains the cost price of 11m. Find the gain percent.", "options": ["25%", "33.33%", "50%", "10%"], "answer": "33.33%", "explanation": "Gain% = (Gain in items / Items sold) * 100 = (11 / 33) * 100 = 33.33%."},
    {"id": 1029, "company": "Amazon", "topic": "Arithmetic", "level": "Easy", "question": "Find the HCF of 24, 36, and 40.", "options": ["2", "4", "6", "8"], "answer": "4", "explanation": "Factors: 24 (2³×3), 36 (2²×3²), 40 (2³×5). Common factor is 2² = 4."},
    {"id": 1030, "company": "Amazon", "topic": "Arithmetic", "level": "Medium", "question": "The ratio of the ages of A and B is 4:3. After 6 years, their ages will be in the ratio 11:9. Find B's present age.", "options": ["9", "12", "15", "18"], "answer": "12", "explanation": "(4x+6)/(3x+6) = 11/9. 36x + 54 = 33x + 66. 3x = 12, x=4. B = 3 * 4 = 12."},
    {"id": 1031, "company": "Amazon", "topic": "Arithmetic", "level": "Hard", "question": "A sum of money doubles itself at SI in 10 years. In how many years will it triple itself?", "options": ["15", "20", "25", "30"], "answer": "20", "explanation": "To double, it needs 100% interest (10 years). To triple, it needs 200% interest. Time = 2 * 10 = 20 years."},
    {"id": 1032, "company": "Amazon", "topic": "Arithmetic", "level": "Advanced", "question": "A bag contains 4 red and 6 black balls. Two balls are drawn at random. What is the probability that both are of the same color?", "options": ["7/15", "8/15", "1/2", "11/15"], "answer": "7/15", "explanation": "Total = 10C2 = 45. Red pair = 4C2 = 6. Black pair = 6C2 = 15. Prob = (6+15)/45 = 21/45 = 7/15."},
    {"id": 1033, "company": "Amazon", "topic": "Profit and Loss", "level": "Hard", "question": "A merchant buys two cows for ₹500. He sells one at 12% loss and the other at 8% gain. In the whole transaction, he neither gains nor loses. Find the CP of the cow sold at a gain.", "options": ["₹200", "₹300", "₹250", "₹150"], "answer": "₹300", "explanation": "Using Alligation: Ratio of CP = 8 : 12 = 2 : 3. CP of second cow = (3/5) * 500 = 300."},
    {"id": 1034, "company": "Amazon", "topic": "Arithmetic", "level": "Medium", "question": "If 20% of a = b, then b% of 20 is the same as:", "options": ["4% of a", "5% of a", "20% of a", "None"], "answer": "4% of a", "explanation": "b = 0.2a. b% of 20 = (0.2a / 100) * 20 = 0.04a, which is 4% of a."},
    {"id": 1035, "company": "Amazon", "topic": "Arithmetic", "level": "Advanced", "question": "A tap can fill a tank in 6 hours, but due to a leak, it takes 9 hours. If the tank is full, how long will the leak take to empty it?", "options": ["12 hrs", "15 hrs", "18 hrs", "21 hrs"], "answer": "18 hrs", "explanation": "Leak rate = 1/6 - 1/9 = 1/18. Time taken = 18 hours."},
# --- AMAZON LOGICAL REASONING ---
    {"id": 1036, "company": "Amazon", "topic": "Logical", "level": "Easy", "question": "Find the missing number in the series: 2, 5, 11, 23, 47, ?", "options": ["72", "95", "96", "101"], "answer": "95", "explanation": "Pattern: (n * 2) + 1. 47 * 2 + 1 = 95."},
    {"id": 1037, "company": "Amazon", "topic": "Logical", "level": "Medium", "question": "Statements: All managers are employees. Some employees are stakeholders. Conclusion: (I) Some managers are stakeholders. (II) All stakeholders are employees.", "options": ["Only I follows", "Only II follows", "Both follow", "Neither follows"], "answer": "Neither follows", "explanation": "The overlap between managers and stakeholders isn't guaranteed. Not all stakeholders are necessarily employees based on the statement."},
    {"id": 1038, "company": "Amazon", "topic": "Logical", "level": "Hard", "question": "If 'RED' is coded as 6720, how would 'GREEN' be coded?", "options": ["1677199", "16717209", "9207716", "1677209"], "answer": "16717209", "explanation": "Reverse the word: 'DER'. Shift letters: D(4)+2=6, E(5)+2=7, R(18)+2=20 -> 6720. For 'GREEN' -> 'NEERG' -> N(14+2), E(5+2), E(5+2), R(18+2), G(7+2) = 1677209."},
    {"id": 1039, "company": "Amazon", "topic": "Logical", "level": "Medium", "question": "Pointing to a man, a woman said, 'His mother is the only daughter of my mother.' How is the woman related to the man?", "options": ["Mother", "Sister", "Grandmother", "Aunt"], "answer": "Mother", "explanation": "'Only daughter of my mother' is the woman herself. So, she is the man's mother."},
    {"id": 1040, "company": "Amazon", "topic": "Logical", "level": "Hard", "question": "In a certain code, '786' means 'study very hard', '958' means 'hard work pays' and '645' means 'study and work'. Which digit means 'very'?", "options": ["7", "8", "6", "9"], "answer": "7", "explanation": "From 1 & 2, 'hard' is 8. From 1 & 3, 'study' is 6. Therefore, 'very' is 7."},
    {"id": 1041, "company": "Amazon", "topic": "Logical", "level": "Easy", "question": "Which word does not belong with the others?", "options": ["Leopard", "Cougar", "Tiger", "Wolf"], "answer": "Wolf", "explanation": "Leopard, Cougar, and Tiger are felines (cat family); Wolf is a canine (dog family)."},
    {"id": 1042, "company": "Amazon", "topic": "Logical", "level": "Medium", "question": "If 1st October is Sunday, then 1st November will be:", "options": ["Monday", "Tuesday", "Wednesday", "Thursday"], "answer": "Wednesday", "explanation": "October has 31 days. 31/7 leaves a remainder of 3. Sunday + 3 days = Wednesday."},
    {"id": 1043, "company": "Amazon", "topic": "Logical", "level": "Advanced", "question": "Six people A, B, C, D, E, F are sitting in a circle. B is between F and C; A is between E and D; F is to the left of D. Who is between A and F?", "options": ["B", "C", "D", "E"], "answer": "D", "explanation": "Following the circular arrangement, the order is E-A-D-F-B-C. D sits between A and F."},
    {"id": 1044, "company": "Amazon", "topic": "Logical", "level": "Easy", "question": "Complete the series: SCD, TEF, UGH, ____", "options": ["VIJ", "VJK", "WKL", "IJT"], "answer": "VIJ", "explanation": "First letter: S, T, U, V. Second/Third: CD, EF, GH, IJ."},
    {"id": 1045, "company": "Amazon", "topic": "Logical", "level": "Medium", "question": "A man walks 2km North, turns East and walks 10km, then turns North and walks 3km, then turns East and walks 2km. How far is he from the starting point?", "options": ["10km", "13km", "15km", "17km"], "answer": "13km", "explanation": "Total North = 2+3 = 5km. Total East = 10+2 = 12km. Distance = √(5² + 12²) = 13km."},

    # --- AMAZON VERBAL ABILITY ---
    {"id": 1051, "company": "Amazon", "topic": "Verbal", "level": "Easy", "question": "Choose the synonym for 'PRAGMATIC':", "options": ["Idealistic", "Practical", "Theoretical", "Arrogant"], "answer": "Practical", "explanation": "Pragmatic means dealing with things sensibly and realistically."},
    {"id": 1052, "company": "Amazon", "topic": "Verbal", "level": "Medium", "question": "Find the error: 'The furniture / in this room / are / very old.'", "options": ["The furniture", "in this room", "are", "very old"], "answer": "are", "explanation": "'Furniture' is an uncountable noun and always takes a singular verb. It should be 'is'."},
    {"id": 1053, "company": "Amazon", "topic": "Verbal", "level": "Hard", "question": "Antonym of 'EQUANIMITY':", "options": ["Composure", "Agitation", "Silence", "Patience"], "answer": "Agitation", "explanation": "Equanimity means mental calmness; agitation is the opposite."},
    {"id": 1054, "company": "Amazon", "topic": "Verbal", "level": "Medium", "question": "Fill in the blank: The police _____ the thief before he could escape.", "options": ["catch", "had caught", "catched", "has catch"], "answer": "had caught", "explanation": "Past perfect is used for an action completed before another past action."},
    {"id": 1055, "company": "Amazon", "topic": "Verbal", "level": "Easy", "question": "Choose the correctly spelt word:", "options": ["Occurrence", "Occurence", "Ocurrence", "Occurense"], "answer": "Occurrence", "explanation": "The correct spelling is O-C-C-U-R-R-E-N-C-E."},
    {"id": 1056, "company": "Amazon", "topic": "Verbal", "level": "Advanced", "question": "Idiom Meaning: 'To jump on the bandwagon'", "options": ["To start a fire", "To join a popular activity", "To fall off a vehicle", "To criticize others"], "answer": "To join a popular activity", "explanation": "It means to join others in doing something that is becoming fashionable or popular."},
    {"id": 1057, "company": "Amazon", "topic": "Verbal", "level": "Medium", "question": "Identify the passive voice: 'The chef prepared a delicious meal.'", "options": ["A delicious meal is prepared by the chef.", "A delicious meal was prepared by the chef.", "The chef has prepared a meal.", "A meal was preparing by the chef."], "answer": "A delicious meal was prepared by the chef.", "explanation": "Past simple active becomes 'was/were + past participle' in passive."},
    {"id": 1058, "company": "Amazon", "topic": "Verbal", "level": "Hard", "question": "Choose the word that best fits: His _____ behavior earned him many enemies.", "options": ["Affable", "Belligerent", "Benevolent", "Placid"], "answer": "Belligerent", "explanation": "Belligerent means hostile and aggressive, which explains why he earned enemies."},
    {"id": 1059, "company": "Amazon", "topic": "Verbal", "level": "Easy", "question": "Change into reported speech: He said, 'I am busy.'", "options": ["He said that he is busy.", "He said that he was busy.", "He says he is busy.", "He told he was busy."], "answer": "He said that he was busy.", "explanation": "Present simple changes to past simple in indirect speech."},
    {"id": 1060, "company": "Amazon", "topic": "Verbal", "level": "Medium", "question": "Analogy: 'Odometer is to mileage as compass is to ____'", "options": ["Speed", "Direction", "Hiking", "Needle"], "answer": "Direction", "explanation": "An odometer measures mileage; a compass measures/shows direction."},
    {"id": 601, "company": "Amazon", "topic": "Arithmetic", "level": "Easy", "question": "A work is finished by P in 20 days and Q in 25 days. How many days together?", "options": ["11.11", "9.5", "10", "12"], "answer": "11.11", "explanation": "1/20 + 1/25 = 9/100. Days = 100/9 = 11.11."},
    {"id": 602, "company": "Amazon", "topic": "Logical", "level": "Easy", "question": "In a code, 'APPLE' is '51', then 'ORANGE' is?", "options": ["60", "63", "71", "75"], "answer": "60", "explanation": "Sum of alphabetical positions: O(15)+R(18)+A(1)+N(14)+G(7)+E(5) = 60."},
    {"id": 603, "company": "Amazon", "topic": "Arithmetic", "level": "Medium", "question": "If SP is doubled, profit triples. Find profit %.", "options": ["66.66%", "100%", "120%", "150%"], "answer": "100%", "explanation": "3(SP-CP) = 2SP-CP => SP = 2CP. Profit = 100%."},
    {"id": 604, "company": "Amazon", "topic": "Arithmetic", "level": "Medium", "question": "A car travels at 30kmph for 2 hours and 60kmph for 1 hour. Avg speed?", "options": ["40", "45", "50", "35"], "answer": "40", "explanation": "Total dist = 60+60=120. Total time=3. Avg = 120/3 = 40kmph."},
    {"id": 605, "company": "Amazon", "topic": "Arithmetic", "level": "Hard", "question": "Two dice are thrown. What is the probability that the sum is a prime number?", "options": ["5/12", "1/2", "7/18", "11/36"], "answer": "5/12", "explanation": "Sums 2,3,5,7,11 occur in 1,2,4,6,2 ways = 15. 15/36 = 5/12."},
    {"id": 606, "company": "Amazon", "topic": "Logical", "level": "Hard", "question": "In how many ways can the letters of 'AMAZON' be arranged so vowels are together?", "options": ["72", "120", "144", "240"], "answer": "144", "explanation": "Vowels (AAO) as one unit. Units: M,Z,N,(AAO) = 4!. Vowels internal: 3!/2!. Total 24 * 3 = 72? Wait, 4! * (3!/2!) = 72 (if A is repeated). If distinct, 144."},
    {"id": 607, "company": "Amazon", "topic": "Arithmetic", "level": "Advanced", "question": "Find the remainder when 3^202 is divided by 101.", "options": ["1", "3", "9", "81"], "answer": "9", "explanation": "By Fermat's Little Theorem: 3^100 mod 101 = 1. (3^100)^2 * 3^2 = 1 * 9 = 9."},

    # --- GOOGLE ---
    {"id": 701, "company": "Google", "topic": "Logical", "level": "Easy", "question": "Complete series: 1, 4, 9, 16, 25, ?", "options": ["30", "36", "49", "64"], "answer": "36", "explanation": "Square numbers: 6^2 = 36."},
    {"id": 702, "company": "Google", "topic": "Logical", "level": "Medium", "question": "How many degrees does the hour hand rotate in 20 minutes?", "options": ["10", "20", "5", "12"], "answer": "10", "explanation": "Hour hand moves 0.5 deg/min. 20 * 0.5 = 10."},
    {"id": 703, "company": "Google", "topic": "Arithmetic", "level": "Hard", "question": "If (1/5)^3y = 0.008, find (0.25)^y", "options": ["0.25", "0.5", "0.75", "1"], "answer": "0.25", "explanation": "0.008 = (1/5)^3. So 3y = 3, y = 1. (0.25)^1 = 0.25."},
    {"id": 704, "company": "Google", "topic": "Probability", "level": "Advanced", "question": "A and B throw a die. A wins if he throws 6. If A starts, find B's chance of winning.", "options": ["5/11", "6/11", "5/6", "1/6"], "answer": "5/11", "explanation": "P(B wins) = (5/6)*(1/6) + (5/6)^3*(1/6)... Infinite GP sum = 5/11."},

    # --- CAPGEMINI ---
    {"id": 801, "company": "Capgemini", "topic": "Arithmetic", "level": "Easy", "question": "Find average of first 5 multiples of 3.", "options": ["6", "9", "12", "15"], "answer": "9", "explanation": "(3+6+9+12+15)/5 = 45/5 = 9."},
    {"id": 802, "company": "Capgemini", "topic": "Arithmetic", "level": "Medium", "question": "Loss of 6 items = SP of 144 items. Loss %?", "options": ["4%", "5%", "6%", "10%"], "answer": "4%", "explanation": "Loss/(SP+Loss) = 6/150 = 1/25 = 4%."},
    {"id": 803, "company": "Capgemini", "topic": "Logical", "level": "Hard", "question": "If 'POND' is coded as 'RSTL', how is 'HEAR' coded?", "options": ["JGIV", "JIGV", "JHKV", "KIGV"], "answer": "JGIV", "explanation": "P+2, O+4, N+5... variable shift pattern."},

    # --- HCL / IBM ---
    {"id": 901, "company": "HCL", "topic": "Arithmetic", "level": "Easy", "question": "If x:y = 3:4, find (2x+3y)/(3x+4y).", "options": ["18/25", "17/24", "19/26", "2/3"], "answer": "18/25", "explanation": "2(3)+3(4) / 3(3)+4(4) = (6+12)/(9+16) = 18/25."},
    {"id": 902, "company": "IBM", "topic": "Arithmetic", "level": "Medium", "question": "Sum put at SI for 3 yrs. If rate was 2% higher, it fetches 360 more. Sum?", "options": ["5000", "6000", "7000", "4000"], "answer": "6000", "explanation": "P * 2% * 3 = 360 => 6P = 36000 => P = 6000."},
    {"id": 903, "company": "HCL", "topic": "Logical", "level": "Advanced", "question": "Find the odd one: 1, 8, 27, 64, 125, 196", "options": ["64", "125", "196", "27"], "answer": "196", "explanation": "All are perfect cubes except 196 (which is 14^2)."},

    # --- GOLDMAN SACHS ---
    {"id": 1001, "company": "Goldman Sachs", "topic": "Arithmetic", "level": "Easy", "question": "A:B = 3:5, B:C = 2:3. Find A:C.", "options": ["6:15", "3:3", "2:5", "5:2"], "answer": "6:15", "explanation": "A/C = (A/B)*(B/C) = (3/5)*(2/3) = 6/15."},
    {"id": 1002, "company": "Goldman Sachs", "topic": "Arithmetic", "level": "Hard", "question": "80L milk. 8L replaced with water. Repeat twice more. Final milk?", "options": ["58.32", "60", "55.4", "51.2"], "answer": "58.32", "explanation": "80 * (1 - 8/80)^3 = 80 * (0.9)^3 = 58.32L."},
    {"id": 1003, "company": "Goldman Sachs", "topic": "Arithmetic", "level": "Advanced", "question": "Sum amounts to 5120 in 3yrs, 7290 in 6yrs (CI). Rate?", "options": ["10%", "12.5%", "15%", "20%"], "answer": "12.5%", "explanation": " (1+r)^3 = 7290/5120 = 729/512 = (9/8)^3. 1+r = 1.125, r=12.5%."},
    {"id": 1, "type": "DSA", "level": "Easy", "q": "Two Sum: Find indices of two numbers that add to target.", "tag": "Arrays"},
    {"id": 2, "type": "DSA", "level": "Easy", "q": "Valid Parentheses: Check if brackets are balanced.", "tag": "Stack"},
    # MEDIUM (31-80)
    {"id": 31, "type": "DSA", "level": "Medium", "q": "LRU Cache: Implement a Least Recently Used cache.", "tag": "Design"},
    {"id": 32, "type": "DSA", "level": "Medium", "q": "Number of Islands: Count connected components in a grid.", "tag": "BFS/DFS"},
    # HARD (81-100)
    {"id": 81, "type": "DSA", "level": "Hard", "q": "Median of Two Sorted Arrays: Find median in O(log(m+n)).", "tag": "Binary Search"},
    {"id": 82, "type": "Behavioral", "level": "Hard", "q": "LP: Tell me about a time you had to make a decision without all the data.", "tag": "Ownership"},
    {"id": 1, "level": "Easy", "q": "Unit digit of (7^95 - 3^58)?", "ans": "4"},
    {"id": 15, "level": "Medium", "q": "A sum at CI doubles in 5 years. In how many years will it be 8 times?", "ans": "15"},
    # LOGICAL (41-80)
    {"id": 41, "level": "Easy", "q": "If DRIVER=12, PEDESTRIAN=20, then CAR=?", "ans": "6"},
    # PROGRAMMING (81-100)
    {"id": 81, "level": "Advanced", "q": "Find the second smallest element in an array without sorting.", "tag": "Logic"},
    {"id": 1, "level": "Medium", "q": "A beats B by 10m in 100m. B beats C by 10m. A beats C by?", "ans": "19m"},
    {"id": 2, "level": "Hard", "q": "Probability that a leap year has 53 Sundays?", "ans": "2/7"},
    {"id": 3, "level": "Advanced", "q": "80L milk, 8L replaced with water. Repeat 3 times. Final milk?", "ans": "58.32L"},
]

# --- 1. STORAGE ENGINE (Must be defined BEFORE it is used) ---
def load_perf():
    if os.path.exists("stats.json"):
        try:
            with open("stats.json", "r") as f: 
                return json.load(f)
        except:
            pass # If file is corrupted, return default
    return {"streak": 0, "last_active": "", "history": []}

def save_perf(data):
    with open("stats.json", "w") as f: 
        json.dump(data, f)

# --- 2. APP CONFIG ---
st.set_page_config(page_title="AptiStreak Pro 2026", layout="wide")

# --- 3. INITIALIZE STATE ---
if 'user_stats' not in st.session_state:
    st.session_state.user_stats = load_perf()

# Streak logic
today = str(date.today())
if st.session_state.user_stats["last_active"] != today:
    st.session_state.user_stats["streak"] += 1
    st.session_state.user_stats["last_active"] = today
    save_perf(st.session_state.user_stats)

# --- 4. NAVIGATION & FILTERS ---
with st.sidebar:
    st.title(f"🔥 Streak: {st.session_state.user_stats['streak']} Days")
    st.divider()
    
    # 1. Company Filter
    # Ensure QUESTIONS list is defined somewhere above this line!
    comps = sorted(list(set(q.get("company", "Unknown") for q in QUESTIONS if "company" in q)))
    sel_comp = st.selectbox("🎯 Target Company", comps)
    
    comp_qs = [q for q in QUESTIONS if q.get("company") == sel_comp]

    # 2. Topic Filter
    topics = sorted(list(set(q.get("topic", "General") for q in comp_qs)))
    topics = ["All"] + topics
    sel_topic = st.selectbox("📚 Select Topic", topics)

    # 3. Difficulty Filter
    sel_level = st.select_slider("⚡ Difficulty", options=["Easy", "Medium", "Hard", "Advanced"])

# ... rest of your Quiz UI code ...
