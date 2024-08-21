import pyttsx3
import speech_recognition as sr
import pyttsx3 as ptt
import pyaudio as pad
import datetime

command_off=True
listener = sr.Recognizer()
alexa = pyttsx3.init()
voices=alexa.getProperty('voices')
alexa.setProperty('voice',voices[0].id)
def take(text):
    alexa.say(text)
    alexa.runAndWait()






def run_command(command_off):

    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)  # Using Google Speech Recognition
            command=command.lower()
            if 'hello' in command:
                take("hi , how can i help you ")
            if 'time' in command:
                take(datetime.datetime.now())
            if 'stop' in command:
                take("studown alexa.........")

                command_off = False
                return command_off




    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
    except sr.RequestError as e:
        print(f"Sorry, there was an error with the request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

while command_off:
    run_command(command_off)