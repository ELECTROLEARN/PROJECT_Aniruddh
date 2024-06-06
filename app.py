from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from gtts import gTTS
import wikipedia
import os

app = Flask(__name__)

listener = sr.Recognizer()

def talk(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("response.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source, timeout=10, phrase_time_limit=10)
            print("Recognizing...")
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'project' in command:
                command = command.replace('project', '')
                print(f"Command: {command}")
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for phrase to start.")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"Error: {e}")
    return command

def run_project():
    command = take_command()
    print(f"Received Command: {command}")
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
        try:
            info = wikipedia.summary(person, 1)
            response += " " + info
        except wikipedia.exceptions.DisambiguationError as e:
            response += " Multiple results found. Be more specific."
        except wikipedia.exceptions.PageError:
            response += " No information available on this person."
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
    talk(response)
    return jsonify({'response': response})

if __name__ == '__main__':
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    import pygame
    pygame.init()
    app.run(host='0.0.0.0', port=5000)
