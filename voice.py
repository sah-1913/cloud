import streamlit as st
import speech_recognition as sr
import csv
import pyttsx3
from datetime import datetime
import pandas as pd
import os

# Function to recognize speech
def recognize_present(timeout=5):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.sidebar.write(f"Listening for 'present' for {timeout} seconds...")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source, timeout=timeout)
    
    try:
        spoken_word = recognizer.recognize_google(audio_data)
        if "present" in spoken_word.lower():
            st.sidebar.success("Student is present.")
            return "present"
        else:
            st.sidebar.error("Did not recognize 'present'.")
            return None
    except sr.UnknownValueError:
        st.sidebar.error("Sorry, could not understand audio.")
        return None
    except sr.RequestError as e:
        st.sidebar.error(f"Could not request results from Google Speech Recognition service: {e}")
        return None

# Function to speak text
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Streamlit app
def main():
    st.set_page_config(page_title="Voice Recognition Roll Call", page_icon="🎤")
    st.title("Voice Recognition Roll Call")

    st.sidebar.header("Settings")
    num_lecture = st.sidebar.number_input("Lecture number of the subject for the day", 
                                           min_value=1, max_value=10, value=1)

    # Upload attendance.csv file
    uploaded_file = st.sidebar.file_uploader("Upload attendance.csv file", type=["csv"])
    
    if uploaded_file is not None:
        attendance = pd.read_csv(uploaded_file)
    else:
        attendance = pd.DataFrame(columns=["Lec_num", "Date", "Time", "1", "2", "3", "4"])

    if num_lecture in attendance['Lec_num'].values:
        st.sidebar.error("Roll Call already done for this lecture.")
        return

    st.sidebar.success("Roll Call Started...")

    enrolled_students = {"1": "Sakshi", "2": "Prasad", "3": "Bhavin", "4": "Nairutya"}

    current_date = datetime.now().strftime("%d-%m-%Y")
    current_time = datetime.now().strftime("%H:%M:%S")

    attendance = attendance.append({'Lec_num': num_lecture,
                                    'Date': current_date,
                                    'Time': current_time,
                                    '1': 'A', 
                                    '2': 'A', 
                                    '3': 'A', 
                                    '4': 'A', 
                                    }, ignore_index=True)

    roll_call_output = []  # List to store roll call results
    
    for roll_number in enrolled_students.keys():
        st.sidebar.write(f"### Roll Number: {roll_number}")
        speak(f"Roll Number {roll_number}")
        student_name = enrolled_students[roll_number]
        st.write(f"Calling {student_name}...")
        st.sidebar.write("Please say 'present' when called.")
        st.sidebar.write("Listening...")
        status = recognize_present(timeout=5)
        if status:
            roll_call_output.append(f"{student_name}: present")
            st.success("Attendance marked.")
            attendance.loc[attendance['Lec_num'] == num_lecture, roll_number] = 'P'
        else:
            roll_call_output.append(f"{student_name}: absent")
            st.error("Attendance not marked.")
            attendance.loc[attendance['Lec_num'] == num_lecture, roll_number] = 'A'
        attendance.to_csv('attendance.csv', index=False)

    st.sidebar.success("Roll Call Completed.")
    
    empty_roll_call = pd.DataFrame(columns=["Roll Number", "Attendance"])
    st.table(empty_roll_call)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Roll Call Data")
        st.table(attendance)
        
    with col2:
        st.write("### Roll Call Summary")
        st.write(roll_call_output)

if __name__ == "__main__":
    main()
