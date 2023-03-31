# VoiceChatGPT: Accepts voice input,
# converts it to text, sends the transcript
# to the ChatGPT API and reads ChatGPT's 
# response aloud.
# 
# WARNING!!: This program will not work without
# an OpenAI API key. More information at
# https://help.openai.com/en/collections/3675931-openai-api
#
# @author: Austine D. Odhiambo AKA Ace Declan
# Written with the help of ChatGPT

import speech_recognition as sr
import requests
from gtts import gTTS
from playsound import playsound
import tkinter as tk

class Application:
    def __init__(self, master):
        self.master = master
        master.title("ChatGPT Voice Assistant")

        self.label = tk.Label(master, text="Click the button and speak into your microphone:")
        self.label.pack()

        self.button = tk.Button(master, text="Speak", command=self.speak)
        self.button.pack()

    def speak(self):
        # Obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        # Recognize speech using Google Speech Recognition
        try:
            print("You said: " + r.recognize_google(audio))
            query = r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            query = ""
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            query = ""

        # Send the text to ChatGPT's API and obtain response
        if query:
            url = 'https://api.openai.com/v1/engine/<ENGINE_ID>/completions'
            prompt = query
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer <API_KEY>',
            }
            data = '{"prompt": "' + prompt + '", "max_tokens": 60, "temperature": 0.5}'
            response = requests.post(url, headers=headers, data=data)
            text = response.json()['choices'][0]['text']

            # Convert the text response to audio using gTTS
            tts = gTTS(text)
            tts.save('response.mp3')

            # Play the audio response
            playsound('response.mp3')

root = tk.Tk()
root.geometry("400x400")
app = Application(root)
root.mainloop()
