import tkinter as tk
from tkinter import ttk
import threading
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from langdetect import detect
import os
from datetime import datetime
import csv

# CSV file name
csv_file = "patientdata.csv.txt"

# Create CSV file with headers if not exists
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Serial No.", "Timestamp", "Patient ID", "Name", "Age", "Original Speech", "Translated Text", "Language"])

# translator
translator = Translator()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text=" Listening... Please speak now.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        status_label.config(text=" Processing your speech...")
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return "Connection error."

def translate_text(text, target_language='en'):
    try:
        source_lang = detect(text)
        return translator.translate(text, src=source_lang, dest=target_language).text
    except Exception as e:
        return f"Translation error: {str(e)}"

def text_to_speech(text, language='en'):
    try:
        tts = gTTS(text=text, lang=language)
        tts.save("output.mp3")
        os.system("start output.mp3") 
    except:
        print("Audio playback failed.")

def save_to_csv(pid, name, age, original, translated, language):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = list(csv.reader(file))
        serial_no = len(reader)

    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([serial_no, timestamp, pid, name, age, original, translated, language])

def emergency_launch():
    status_label.config(text=" Emergency protocol activated!")
    os.system("start emergency.mp3")  # You can replace this with any emergency action

def process_speech():
    def inner_process():
        pid = entry_pid.get().strip()
        name = entry_name.get().strip()
        age = entry_age.get().strip()

        if not pid or not name or not age:
            status_label.config(text=" Please fill in patient details first.")
            return

        status_label.config(text=" Listening and translating...")
        original_text = recognize_speech()

        if not original_text:
            status_label.config(text=" Couldn't understand. Please try again.")
            return

        source_text.set(original_text)
        target_lang = language_selector.get()
        translated = translate_text(original_text, target_lang)
        translated_text.set(translated)
        text_to_speech(translated, target_lang)
        save_to_csv(pid, name, age, original_text, translated, target_lang)
        status_label.config(text=" Saved to CSV. Audio played.")

    threading.Thread(target=inner_process).start()

# GUI
root = tk.Tk()
root.title("Hospital Speech Translator")
root.geometry("650x500")
root.configure(bg="#e8f0fe")

tk.Label(root, text=" Hospital Speech Translator", font=("Helvetica", 20, "bold"), bg="#e8f0fe", fg="#2c3e50").pack(pady=10)

# Patient Info
frame_patient = tk.Frame(root, bg="#e8f0fe")
frame_patient.pack(pady=5)

tk.Label(frame_patient, text="Patient ID:", bg="#e8f0fe").grid(row=0, column=0, sticky="e", padx=5)
entry_pid = tk.Entry(frame_patient, width=15)
entry_pid.grid(row=0, column=1, padx=5)

tk.Label(frame_patient, text="Name:", bg="#e8f0fe").grid(row=0, column=2, sticky="e", padx=5)
entry_name = tk.Entry(frame_patient, width=20)
entry_name.grid(row=0, column=3, padx=5)

tk.Label(frame_patient, text="Age:", bg="#e8f0fe").grid(row=0, column=4, sticky="e", padx=5)
entry_age = tk.Entry(frame_patient, width=5)
entry_age.grid(row=0, column=5, padx=5)

# Status Label
status_label = tk.Label(root, text=" Fill details and click below to start...", font=("Helvetica", 12), bg="#e8f0fe")
status_label.pack(pady=10)

# Fields
source_text = tk.StringVar()
translated_text = tk.StringVar()

ttk.Label(root, text="Detected Speech:", background="#e8f0fe").pack()
tk.Entry(root, textvariable=source_text, font=("Helvetica", 12), width=70).pack()

ttk.Label(root, text="Translated Text:", background="#e8f0fe").pack(pady=5)
tk.Entry(root, textvariable=translated_text, font=("Helvetica", 12), width=70).pack()

ttk.Label(root, text="Select Doctor's Language:", background="#e8f0fe").pack(pady=10)
language_selector = ttk.Combobox(root, values=["en", "hi", "de", "fr", "es"], state="readonly")
language_selector.set("en")
language_selector.pack()

# Start Button
tk.Button(
    root,
    text=" Start Recording",
    font=("Helvetica", 14),
    bg="#27ae60",
    fg="white",
    command=process_speech
).pack(pady=20)

tk.Button(
    root,
    text=" Emergency Launch",
    font=("Helvetica", 14, "bold"),
    bg="#c0392b",
    fg="white",
    command=emergency_launch
).pack(pady=10)

root.mainloop()



