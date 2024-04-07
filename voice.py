import streamlit as st
import speech_recognition as sr
import csv
import pyttsx3
from datetime import datetime
import pandas as pd
import os



# try:
#     # Attempt to record audio
#     audio_data = st.audio("Record audio", format="audio/wav", start_recording=True, encoding="wav")
#     st.write("Microphone is available.")
# except Exception as e:
#     st.error("Microphone is not available. Please grant microphone permissions.")




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

    st.sidebar.success("Roll Call Started...")

    enrolled_students = {"1": "Sakshi", "2": "Prasad", "3": "Bhavin", "4": "Nairutya"}

    current_date = datetime.now().strftime("%d-%m-%Y")
    current_time = datetime.now().strftime("%H:%M:%S")

    attendance = pd.DataFrame(columns=["Roll Number", "Student Name", "Attendance"])
    
    for roll_number, student_name in enrolled_students.items():
        st.sidebar.write(f"### Roll Number: {roll_number}")
        speak(f"Roll Number {roll_number}")
        st.write(f"Calling {student_name}...")
        st.sidebar.write("Please say 'present' when called.")
        st.sidebar.write("Listening...")
        status = recognize_present(timeout=5)
        if status:
            attendance = attendance.append({"Roll Number": roll_number, "Student Name": student_name, "Attendance": "Present"}, ignore_index=True)
            st.success("Attendance marked.")
        else:
            attendance = attendance.append({"Roll Number": roll_number, "Student Name": student_name, "Attendance": "Absent"}, ignore_index=True)
            st.error("Attendance not marked.")
    
    st.sidebar.success("Roll Call Completed.")
    
    st.write("### Roll Call Data")
    st.table(attendance)

if __name__ == "__main__":
    main()
