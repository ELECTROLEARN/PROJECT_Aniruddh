from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import pyttsx3
import wikipedia

app = Flask(__name__)

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            print("Recognizing...")
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'project' in command:
                command = command.replace('project', '')
                print(command)
    except Exception as e:
        print(f"Error: {e}")
    return command

def run_project():
    command = take_command()
    print(command)
    response = ""
    if 'hello' in command:
        response = 'Hello there !!, How are you ??'
    elif 'name' in command:
        response = 'I am --- !!! , powerfully designed by -----'
    elif 'nice' in command:
        response = 'Thats great !!!! , Nice to Assist You By the Way!!!'
    elif 'designed' in command:
        response = 'I am Designed By ------ Team but!!!!!!!!!, I ESPECIALLY THANK ---- Because ---- Powerfully Coded me !!'
    elif 'who is' in command:
        response = 'Getting results !!!'
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        response += " " + info
    elif 'fine' in command:
        response = "Nice to meet you by the way!! What's your name??"
    elif "bye" in command:
        response = 'Bye !! Have a Nice Day !!'
    else:
        response = 'I cannot listen !!!!, Try saying it Properly'
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    response = run_project()
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
 
