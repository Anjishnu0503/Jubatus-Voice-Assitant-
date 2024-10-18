import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import datetime
import pyaudio
import distutils
import os 
import spotipy
import random
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'cf51083871f94846889dc893024bd25a'
client_secret = '2cc72ac13dda4b4a8bbffb19325a678b'
credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials)

r = sr.Recognizer()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User  said: {query}\n")
    except Exception as e:
        print(e)
        speak("Say that again please...")
        return "None"
    return query

def play_random_song():
    results = sp.search(q='track', type='track', limit=50)  
    if results['tracks']['items']:
        random_track = random.choice(results['tracks']['items'])  
        track_name = random_track['name']
        artist_name = random_track['artists'][0]['name']
        track_url = random_track['external_urls']['spotify']
        
        speak(f"Playing {track_name} by {artist_name}")
        print(f"Playing {track_name} by {artist_name}")
        print(f"You can listen to it here: {track_url}")
        
        webbrowser.open(track_url)
    else:
        speak("No tracks found.")

if __name__ == "__main__":
    speak("Hello Sir, I am jubatus, your Voice Assistant. Please tell me how may I help you")
    MAX_QUERIES = 5
    query_count = 0  

    while True:
        query = takeCommand().lower()
        query_count += 1  

        if query_count > MAX_QUERIES:
            r = sr.Recognizer()
            query_count = 0  

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=5)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        
        elif 'play a random song' in query:
            play_random_song()
            
        elif 'exit' in query:
            speak("Thanks for giving me your time")
            exit()
