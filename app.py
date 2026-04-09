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
