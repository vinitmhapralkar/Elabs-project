import speech_recognition as sr
import pyttsx3
import datetime
import os
import webbrowser
import pyjokes
import requests

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User: {query}")
    except Exception as e:
        speak("Sorry, Can you please repeat.")
        return ""
    return query.lower()

def tell_time():
    now = datetime.datetime.now().strftime("%H:%M")
    speak(f"The time is {now}")

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def get_news():
    try:
        api_key = "e5f6645e99eb4829ab66d674f5a91c4b"  # ← Replace this with your actual key
        url = f"https://newsapi.org/v2/everything?domains=firstpost.com&pageSize=5&sortBy=publishedAt&apiKey={api_key}"
        res = requests.get(url)
        data = res.json()

        if data["status"] != "ok":
            speak("Sorry, I couldn't fetch news at the moment.")
            return

        articles = data.get("articles", [])
        if not articles:
            speak("No news found from Firstpost right now.")
            return

        speak("Here are the latest news headlines from Firstpost:")
        for i, article in enumerate(articles):
            speak(f"{i + 1}. {article['title']}")
    except Exception as e:
        print("Error:", e)
        speak("Something went wrong while fetching the news.")

def take_note():
    speak("What should I write in your note?")
    note = take_command()
    if note:
        with open("note.txt", "a") as f:
            f.write(f"{datetime.datetime.now()}: {note}\n")
        speak("Note added.")

def open_app(app_name):
    paths = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    }
    if app_name in paths:
        os.startfile(paths[app_name])
        speak(f"Opening {app_name}")
    else:
        speak("Sorry, I don't know this application.")

def run_assistant():
    speak("Voice assistant online. How can I help?")
    while True:
        query = take_command()

        if 'open notepad' in query:
            open_app("notepad")
        elif 'open calculator' in query:
            open_app("calculator")
        elif 'open chrome' in query:
            open_app("chrome")
        elif 'time' in query:
            tell_time()
        elif 'joke' in query:
            tell_joke()
        elif 'news' in query:
            get_news()
        elif 'note' in query or 'remember this' in query:
            take_note()
        elif 'open youtube' in query:
            webbrowser.open("https://youtube.com")
            speak("Opening YouTube")
        elif 'open google' in query:
            webbrowser.open("https://google.com")
            speak("Opening Google")
        elif 'exit' in query or 'stop' in query:
            speak("Goodbye!")
            break
        else:
            speak("I did not understand that command.")

if __name__ == "__main__":
    run_assistant()