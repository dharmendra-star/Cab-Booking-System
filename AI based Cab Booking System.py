"""*************************************** MODULES USED IN THE PROJECT ***************************************"""
import mysql.connector as co
from tabulate import tabulate
import os
from datetime import date, datetime
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
import spacy
import random

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

"""*************************************** AI MODEL TRAINING FUNCTIONS ***************************************"""
# Dummy data for cab recommendations (in real app, load from DB)
def train_recommendation_model():
    # Simulate cab features: [cab_type_encoded, nos, user_score]
    data = {
        'cab_type': [1, 2, 1, 3, 2],  # 1=Sedan, 2=SUV, 3=Hatchback
        'nos': [4, 6, 4, 4, 7],
        'user_score': [0.8, 0.9, 0.7, 0.6, 0.85]
    }
    df = pd.DataFrame(data)
    return df

# Train pricing model
def train_pricing_model():
    # Simulate: distance, time_of_day (0=off-peak, 1=peak), cab_type -> price
    data = {
        'distance': [10, 20, 15, 5, 25],
        'time_of_day': [0, 1, 0, 1, 1],
        'cab_type': [1, 2, 1, 3, 2],
        'price': [500, 1200, 800, 400, 1500]
    }
    df = pd.DataFrame(data)
    X = df[['distance', 'time_of_day', 'cab_type']]
    y = df['price']
    model = LinearRegression()
    model.fit(X, y)
    return model

# Train fraud detection model
def train_fraud_model():
    # Simulate booking amounts for anomaly detection
    data = [500, 600, 700, 800, 10000]  # 10000 is anomaly
    model = IsolationForest(contamination=0.1)
    model.fit([[x] for x in data])
    return model

rec_model_data = train_recommendation_model()
pricing_model = train_pricing_model()
fraud_model = train_fraud_model()

"""*************************************** AI FUNCTIONS ***************************************"""
def recommend_cabs(user_prefs, all_cabs):
    # user_prefs: {'cab_type': int, 'nos': int, 'user_score': float}
    cab_features = all_cabs[['cab_type_encoded', 'nos', 'user_score']].values
    user_vector = [[user_prefs['cab_type'], user_prefs['nos'], user_prefs['user_score']]]
    similarities = cosine_similarity(user_vector, cab_features)[0]
    top_indices = similarities.argsort()[-3:][::-1]  # Top 3
    return [all_cabs.iloc[i] for i in top_indices]

def predict_price(distance, time_of_day, cab_type):
    return pricing_model.predict([[distance, time_of_day, cab_type]])[0]

def detect_fraud(amount):
    prediction = fraud_model.predict([[amount]])
    return prediction[0] == -1  # -1 means anomaly

def nlp_chatbot(user_input):
    doc = nlp(user_input.lower())
    intents = {
        'book': ['book', 'booking', 'reserve'],
        'cancel': ['cancel', 'delete'],
        'show': ['show', 'view', 'list'],
        'search': ['search', 'find']
    }
    for intent, keywords in intents.items():
        if any(keyword in doc.text for keyword in keywords):
            return intent
    return 'unknown'

"""*************************************** FUNCTION TO GENERATE CAB ID ***************************************"""
def gen_cid():
    try:
        if not os.path.exists("cab.txt"):
            with open("cab.txt", "w") as f:
                f.write("1000")
        with open("cab.txt", "r+") as f:
            n = int(f.read())
            n += 1
            f.seek(0)
            f.write(str(n))
        return n
    except IOError:
        print("I/O error occurred")
        return None

"""********************************* Function to Add CAB *********************************"""
def add_cab():
    try:
        mycon = co.connect(host="localhost", user="root", password="Dhar@#3839", database="CAB_BOOKING")
        cursor = mycon.cursor()
        cid = gen_cid()
        if cid is None:
            print("Error generating CAB ID")
            return
        regno = input("\n\nEnter registration number: ")
        cab_type = input("\nEnter type of the CAB (Sedan/SUV/Hatchback): ")
        cab_type_encoded = {'sedan': 1, 'suv': 2, 'hatchback': 3}.get(cab_type.lower(), 1)
        cab_desc = input('Enter cab description: ')
        nos = int(input('Enter no. of seats: '))
        owner = input("Enter Owner's Name: ")
        driver = input("Enter driver's Name: ")
        ownadd = input('Enter owner address: ')
        mob = int(input('Enter Mobile no.: '))
        user_score = 0.5  # Default AI score
        cursor.execute("insert into CAB_MASTER values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (cid, regno, cab_type, cab_desc, nos, owner, driver, ownadd, mob, user_score))
        mycon.commit()
        mycon.close()
        cursor.close()
        print("\n Cab added Successfully")
        print("\n\n YOUR CAB ID IS: ", cid)
        print('Record has been saved in CAB_MASTER table')
    except Exception as e:
        print('Error in add_cab:', e)

"""************************************************* FUNCTION TO DISPLAY ALL CABS *************************************************"""
def show_all_cab():
    try:
        mycon = co.connect(host="localhost", user="root", password="Dhar@#3839", database="CAB_BOOKING")
        cursor = mycon.cursor()
        strQry = "select * from cab_master"
        cursor.execute(strQry)
        data = cursor.fetchall()
        if data == []:
            print("No records found")
        else:
            print("")
            h = ["CAB ID", "REG NO.", "CAB TYPE", "CAB DESC", "NO OF SEATS", "OWNER NAME", "DRIVER NAME", "OWNER ADDRESS", "MOB NO", "USER SCORE"]
            print(tabulate(data, headers=h))
        mycon.close()
        cursor.close()
    except Exception as e:
        print('Error:', e)

# Other functions (search_cab, modify_cab, delete_cab) remain similar, with minor tweaks for new columns.

"""*************************************** FUNCTION TO GENERATE BOOKING ID ***************************************"""
def gen_bid():
    try:
        if not os.path.exists("book.txt"):
            with open("book.txt", "w") as f:
                f.write("1000")
        with open("book.txt", "r+") as f:
            n = int(f.read())
            n += 1
            f.seek(0)
            f.write(str(n))
        return n
    except IOError:
        print("I/O error occurred")
        return None

"""********************************* Function to Add BOOKING *********************************"""
def add_booking():
    try:
        mycon = co.connect(host="localhost", user="root", password="Dhar@#3839", database="CAB_BOOKING")
        cursor = mycon.cursor()
        today = date.today()
        print("Date:", today)
        print("*" * 50)
        cid = int(input("Enter cab ID: "))
        q = "select * from CAB_MASTER where cid=%s"
        cursor.execute(q, (cid,))
        data = cursor.fetchall()
        if data == []:
            print("No record found")
            mycon.close()
            cursor.close()
            return
        h = ["CAB ID", "REG. NO.", "CAB TYPE", "DESCRIPTION", "SEATS", "OWNER'S NAME", "DRIVER'S NAME", "ADDRESS", "MOB. NUMBER", "USER SCORE"]
        print(tabulate(data, headers=h))
        bid = gen_bid()
        if bid is None:
            print("Error generating Booking ID")
            mycon.close()
            cursor.close()
            return
        cnm = input("Enter customer's Name: ")
        mob = input('Enter Mobile no.: ')
        source = input('Enter pickup location: ')
        dest = input('Enter drop location: ')
        distance = float(input('Enter approximate distance (km): '))
        time_of_day = int(input('Time of day (0=off-peak, 1=peak): '))
        cab_type_encoded = data[0][2]  # From DB
        amt = predict_price(distance, time_of_day, cab_type_encoded)
        if detect_fraud(amt):
            print("AI Alert: Potential fraud detected in pricing. Booking paused.")
            return
        cursor.execute("insert into BOOKINGS values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (bid, cid, cnm, mob, source, dest, amt, today, distance, time_of_day))
        mycon.commit()
        print("\n Cab booked Successfully")
        print("\n\n YOUR BOOKING ID IS:", bid)
        print('Record has been saved in BOOKINGS table')
        mycon.close()
        cursor.close()
    except Exception as e:
        print('Error in booking:', e)
        print("Booking Unsuccessful")

# Other functions (cancel_booking, show_all_bookings, bill_generate) updated similarly for new columns.

"""*************************************** AI CHATBOT MENU ***************************************"""
def ai_chatbot_menu():
    print("Welcome to the AI Chatbot! Type your request (e.g., 'book a cab', 'show bookings', 'cancel booking').")
    while True:
        user_input = input("You: ")
        intent = nlp_chatbot(user_input)
        if intent == 'book':
            add_booking()
        elif intent == 'cancel':
            n = int(input("Enter Booking ID: "))
            cancel_booking(n)
        elif intent == 'show':
            show_all_bookings()
        elif intent == 'search':
            search_cab()
        elif user_input.lower() in ['exit', 'quit']:
            break
        else:
            print("AI: Sorry, I didn't understand. Try 'book a cab' or 'show bookings'.")

"""**************************************************************************** INTRODUCTORY FUNCTION *****************************************************************************"""
def intro():
    print("SMART AI-BASED CAB BOOKING SYSTEM")
    print("PRESENTED BY: DHARMENDRA KUMAR SINGH")
    print("COLLEGE: GOVERNMENT POLYTECHNIC JAGANNATHPUR, WEST SINGHBHUM, (JHARKHAND)")
    print("BRANCH: COMPUTER SCIENCE AND ENGINEERING")
    print("SEMESTER: 3RD SEMESTER")
    print("YEAR: 2ND YEAR")
    input("Press Enter key to continue.............!")

"""************************************************************** CAB MENU FUNCTION **************************************************************"""
def cab_menu():
    while True:
        print(60 * "=")
        print("CAB MENU")
        print("1. Add New Cab")
        print("2. Modify Existing Cab")
        print("3. Delete Cab")
        print("4. View All Cab")
        print("5. Search Cab")
        print("6. AI Recommendations")
        print("7. Exit")
        try:
            ch = int(input("Enter Your Choice(1~7): "))
            if ch == 1:
                add_cab()
            elif ch == 2:
                modify_cab()
            elif ch == 3:
                n = int(input("Enter CAB ID: "))
                delete_cab(n)
            elif ch == 4:
                show_all_cab()
            elif ch == 5:
                search_cab()
            elif ch == 6:
                # AI Recommendation
                user_prefs = {'cab_type': int(input("Preferred cab type (1=Sedan, 2=SUV, 3=Hatchback): ")),
                            'nos': int(input("Min seats: ")), 'user_score': 0.8}
                all_cabs = pd.DataFrame(rec_model_data)  # In real app, fetch from DB
                recs = recommend_cabs(user_prefs, all_cabs)
                print("AI Recommendations:")
                for rec in recs:
                    print(f"Cab Type: {rec['cab_type']}, Seats: {rec['nos']}, Score: {rec['user_score']}")
            elif ch == 7:
                break
            else:
                print("Input correct choice...(1-7)")
        except ValueError:
            print("Input correct choice...(1-7)")

"""***************************************************************************** THE MAIN FUNCTION OF PROGRAM *****************************************************************************"""
intro()
while True:
    print(50 * "=")
    print("\tMAIN MENU:")
    print(50 * "=")
    print("1. Cab Master Menu")
    print("2. Cab Booking")
    print("3. Cancel Booking")
    print("4. Show All Booking")
    print("5. Generate Bill")
    print("6. AI Chatbot")
    print("7. Exit")
    try:
        ch = int(input("Enter Your Choice(1~7): "))
        if ch == 1:
            cab_menu()
        elif ch == 2:
            add_booking()
        elif ch == 3:
            n = int(input("Enter Booking ID: "))
            cancel_booking(n)
        elif ch == 4:
            show_all_bookings()
        elif ch == 5:
            num = int(input("\n\nEnter Booking Number: "))
            bill_generate(num)
        elif ch == 6:
            ai_chatbot_menu()
        elif ch == 7:
            break
        else:
            print("Input correct choice...(1-7)")
    except ValueError:
        print("Input correct choice...(1-7)")

input("\n\n\n\n\nTHANK YOU\n\n VISIT AGAIN \n\n Press any key to exit...")