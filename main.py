import speech_recognition as sr
import pyttsx3
import webbrowser
import time
#import musicLibrary
import urllib.parse
import pywhatkit
import requests
import openai

openai.api_key = "{your_api_key_here}"

recognizer = sr.Recognizer()
engine = pyttsx3.init()
 
def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def get_news():
    api_key = "your_api_key_here"
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={"your_api_key_here"}"

    try:
        response = requests.get(url)
        news = response.json()
        articles = news["articles"][:5]
        for i, article in enumerate(article, 1):
            speak(f"News {i}:{article['title']}")
    except:
        speak("Sorry, i couldn't fetch the news at the moment")

    
def get_weather(city):
    api_key = "your_api_key_here"  
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            speak("City not found.")
            return

        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]

        speak(f"The temperature in {city} is {temp} degree Celsius with {description}.")

    except:
        speak("Sorry, I couldn't fetch the weather details.")

# def chat_with_gpt(query):
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",  
#             messages=[
#                 {"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
#                 {"role": "user", "content": query}
#             ]
#         )
#         answer = response.choices[0].message.content.strip()
#         print("GPT:", answer)
#         speak(answer)
#     except Exception as e:
#         print("Error talking to GPT:", e)
#         speak("Sorry, I couldn't get a response.")

def answer_with_gpt(query):
    print(f"Query: {query}")
    response = f"That's a great question! I'm sorry I can't fetch the actual answer right now."
    speak(response)

def process_command(c):
     c = c.lower()

     if "open google" in c:
        webbrowser.open("https://google.com")

     elif "open youtube" in c:
        webbrowser.open("https://youtube.com")

     elif "open facebook" in c:
        webbrowser.open("https://facebook.com")

     elif "news" in c:
        speak("Fetching the latest news headlines...")
        get_news()

     elif "weather" in c:
        speak("Please tell me the city name.")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            city = recognizer.recognize_google(audio)
            get_weather(city)

     elif c.startswith("play"):
        song = c.replace("play", "").strip()
        if song:
            speak(f"Playing {song} on YouTube")
            try:
                pywhatkit.playonyt(song)
            except:
                speak("Sorry, I couldn't play the song")
        else:
            speak("Please say a song name.")

    #  else:
    #     chat_with_gpt
       
     elif c.lower().startswith("who") or c.lower().startswith("what") or c.lower().startswith("how"):
       answer_with_gpt(c)
 

    


 # Start
speak("Initializing Jarvis...")
while True:
    try:
        with sr.Microphone() as source:
            print("\n Listening for wake word...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
            word = recognizer.recognize_google(audio)
            print("You said:", word)
            if "jarvis" in word.lower():
                speak("Ya, I am listening...")
                # Now listen for actual command
                with sr.Microphone() as source:
                    print("Speak your command:")
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source, timeout=4, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    print("Command:", command)
                    process_command(command)
                time.sleep(2)  # pause before looping again
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError:
        speak("Sorry, network error.")
    except Exception as e:
        print("Error:", e)
