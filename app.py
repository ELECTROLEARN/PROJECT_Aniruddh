import speech_recognition as sr
from flask import Flask, request, jsonify, render_template
import pyttsx3
import wikipedia

app = Flask(__name__)

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def talk(text):
    if not engine.isBusy():
        engine.say(text)
        engine.runAndWait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listen', methods=['POST'])
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=10)
        print("Recognizing...")
        try:
            command = recognizer.recognize_google(audio_data).lower()
            return jsonify({'command': command})
        except sr.UnknownValueError:
            return jsonify({'command': ''})
        except sr.RequestError:
            return jsonify({'command': ''})

@app.route('/process', methods=['POST'])
def process_command():
    data = request.get_json()
    command = data.get('command', '').lower()
    response = ""
    if 'hello' in command:
        response = 'Hello there !!, How are you ??'
    elif 'name' in command:
        response = 'I am Eron !!! , powerfully designed by Aniruddh'
    elif 'nice' in command:
        response = 'Thats great !!!! , Nice to Assist You By the Way!!!'
    elif 'who is aniruddh' in command or 'who is anirudh' in command:
        response = 'Thats My creator !!!!!, I thank to him'
    elif 'designed' in command:
        response = 'I am Designed By Emergent Robotics Operating Network Team but!!!!!!!!!, I Thank especially Aniruddh Because He Powerfully Coded me !!'
    elif 'who is' in command:
        person = command.replace('who is', '')
        response = wikipedia.summary(person, 1)
    elif 'bye' in command:
        response = "Nice to assist you!!"
    else:
        response = 'I cannot listen !!!!, Try saying it Properly'

    talk(response)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
