from flask import Flask, render_template, request, jsonify, send_file
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from langdetect import detect
import os
from datetime import datetime
import csv

app = Flask(__name__)
translator = Translator()
csv_file = "patientdata.csv.txt"

# Create CSV file with headers
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Serial No.", "Timestamp", "Patient ID", "Name", "Age", "Original Speech", "Translated Text", "Language"])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    pid = data['pid']
    name = data['name']
    age = data['age']
    target_lang = data['language']

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        original_text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio."})
    except sr.RequestError:
        return jsonify({"error": "Speech recognition error."})

    try:
        source_lang = detect(original_text)
        translated = translator.translate(original_text, src=source_lang, dest=target_lang).text
    except Exception as e:
        return jsonify({"error": f"Translation failed: {str(e)}"})
    
    # Text to speech
    tts = gTTS(text=translated, lang=target_lang)
    tts.save("output.mp3")

    # Save to CSV
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        serial_no = len(list(csv.reader(file)))

    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([serial_no, timestamp, pid, name, age, original_text, translated, target_lang])

    return jsonify({
        "original": original_text,
        "translated": translated
    })


@app.route('/audio')
def audio():
    return send_file("output.mp3")

if __name__ == '__main__':
    app.run(debug=True)
