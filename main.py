import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from google import generativeai as genai
import pygame
from gtts import gTTS
import os

recognizer = sr.Recognizer() 
engine = pyttsx3.init()
newsapi = "8fc88b02f1d0489dbe94888ee0920d29"

def speak_old(text):
    engine.say(text) 
    engine.runAndWait()

pygame.mixer.init()

def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")
   
    # pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
      
    pygame.mixer.music.unload()
    os.remove("temp.mp3")
    
def aiProcess(command):
    model = genai.GenerativeModel(model_name ="gemini-2.5-flash")
    genai.configure(api_key="GOOGLE_API_KEY")
    
    response = model.generate_content([
            f"You are a virtual assistant named Jarvis, a smart and helpful AI assistant. Give a short response please: {command}"
        ])   
         
    return response.text

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    
    elif "news" in c.lower():
        speak("Fetching the latest news for you.")
        # url = f"https://newsapi.org/v2/everything?q=India&apiKey={newsapi}" # For India News
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}" #For US or other country news 
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            for article in articles[:5]:
                speak(article['title'])
                
        #     if not articles:
        #         speak("Sorry, I couldn't find any news right now.")
        #     else:
        #         speak("Here are the top news headlines.")
        #         for article in articles[:5]:  # Limit to top 5
        #             speak(article['title'])
        # else:
        #     speak("Sorry, I'm unable to fetch news right now.")
        
    else: 
        # Let OpenAI Handle the request  
        output = aiProcess(c)
        speak(output)   
 
if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        print("recognizing...")  # Listen for the wake word "Jarvis"
        # r = sr.Recognizer()      # Obtain the audio from the microphone
# recognize speech using Sphinx # pip install pocketsphinx // command to install sphinx
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1) 
                print("Listening...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)
                
            word = recognizer.recognize_google(audio)
            print("Heard:", word)
            
            if word.lower() == "jarvis":
                speak("Ya")
                # Listen for command 
                with sr.Microphone() as source: 
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    print("Jarvis Active...") 
                    # audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
                    audio = recognizer.listen(source)
                    
                    command = recognizer.recognize_google(audio)
                    print("command:", command)
                    processCommand(command)
        
        except Exception as e:
            print("Error;{0}".format(e))        
            
