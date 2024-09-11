import pyttsx3
import speech_recognition as sr
import datetime
import os
import wikipedia
import pywhatkit  # Automation of YouTube or WhatsApp
from requests import get
import requests  # For weather updates
import webbrowser
import smtplib  # Email sending functionality
import time
import pyjokes
import pyautogui
import speedtest

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set the voice (you can choose other indices if you prefer)

# Function to convert text to speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to take voice commands
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=5)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"You said: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            speak("Sorry, I didn't hear anything. Please try again.")
            return None
        except sr.UnknownValueError:
            speak("I didn't understand.")
            return None

# Function to get the IP address
def get_ip_address():
    try:
        response = get('https://api.ipify.org')
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        ip = response.text
        speak(f"Your IP address is {ip}")
    except requests.RequestException as e:
        speak("Sorry, I couldn't retrieve your IP address.")
        print(f"Error: {e}")

# Function to send an email
def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    # Enable Less secure app access in Gmail settings
    server.login("bayava458@gmail.com", "Qwerty@123")  # your own id and password
    server.sendmail("sunamaya9844@gmail.com", to, content)
    server.close()

# Function to greet the user based on the time of day
def wish():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am Piyush. How may I help you")

# Function to get the weather update for a specific city
def get_weather(city):
    api_key = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + api_key + "&units=metric"
    try:
        response = requests.get(complete_url)
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        weather_data = response.json()
        
        if weather_data["cod"] != "404":
            main = weather_data["main"]
            temperature = main["temp"]
            pressure = main["pressure"]
            humidity = main["humidity"]
            weather_desc = weather_data["weather"][0]["description"]
            speak(f"The temperature in {city} is {temperature} degrees Celsius with {weather_desc}. "
                  f"The humidity is {humidity}% and the pressure is {pressure} hPa.")
        else:
            speak("City not found. Please check the city name and try again.")
    except requests.RequestException as e:
        speak("Sorry, I couldn't retrieve the weather information.")
        print(f"Error: {e}")

# Function to get the user's current location
def get_current_location():
    try:
        response = requests.get("https://ipinfo.io")
        response.raise_for_status()
        location_data = response.json()
        city = location_data["city"]
        return city
    except requests.RequestException as e:
        speak("Sorry, I couldn't retrieve your current location.")
        print(f"Error: {e}")
        return None

# Password check
passcode = "i am prashant"
speak("What's the password?")
password = takecommand()

if password != passcode:
    speak("Wrong password, access denied.")
else:
    if _name_ == '_main_':
        wish()
        while True:
            query = takecommand()

            if not query:
                continue

            # Command to open Notepad
            if 'open notepad' in query:
                os.system("start notepad")

            elif 'who made you' in query:
                speak("USN's 089, 113, and 115 made me as a mini project in their 4th semester")
            
            # Command to play a song on YouTube
            elif "play" in query:
                song = query.replace("play", "").strip()
                speak(f"Playing {song} on YouTube.")
                pywhatkit.playonyt(song)
            
            # Command to search for a person on Wikipedia
            elif "who" in query:
                person = query.replace('who is', "").strip()
                info = wikipedia.summary(person, sentences=1)
                speak(info)
                print(info)

            # Command to search for an object or concept on Wikipedia
            elif "what is" in query:
                object = query.replace('what is', "").strip()
                info = wikipedia.summary(object, sentences=1)
                speak(info)

            # Command to search for a date-related event on Wikipedia
            elif "when" in query:
                object = query.replace('when', "").strip()
                info = wikipedia.summary(object, sentences=1)
                speak(info)
            
            # Command to tell the current time
            elif "time" in query:
                current_time = datetime.datetime.now().strftime('%I:%M %p')
                speak(f"Current time: {current_time}")
            
            # Command to tell the current date
            elif "date" in query:
                current_date = datetime.datetime.now().strftime('%d / %m / %Y')
                speak(f"Today's date: {current_date}")
            
            # Command to tell the IP address
            elif "ip address" in query:
                get_ip_address()
            
            # Command to open an application
            elif "open" in query:
                app = query.replace("open", "").strip()
                os.system(f"start {app}")
            
            # Command to log in to a website
            elif "login" in query:
                data = query.replace("login", " ").strip()
                webbrowser.open(f"www.{data}.com")

            # Command to search Google
            elif "google about" in query:
                data = query.replace("google about", " ").strip()
                webbrowser.open(f"https://www.google.com/search?q={data}")
            
            # Command to send a WhatsApp message
            elif "whatsapp" in query:
                '''speak("to whom would you like to text")
                data = takecommand()'''
                speak("What message would you like to send")
                msg = takecommand()
                speak("Sending")
                current = datetime.datetime.now()
                hr = current.hour
                minutes = current.minute
                min = minutes + 1
                pywhatkit.sendwhatmsg('+917022173277', msg, hr, min)

            # Command to set an alarm
            elif "set alarm" in query:
                speak("Please tell me the time to set the alarm")
                timeee = takecommand()
                speak("The alarm has been set")
                
                # Extract the time part from the command
                alarm_time = timeee.replace("set alarm for", "").strip()
                
                while True:
                    # Get the current time in 'HH:MM' format
                    current_time = datetime.datetime.now().strftime('%H:%M')
                    if alarm_time == current_time:
                        alarm_file_path = "C:\\code with harry\\ada iat1\\mini\\alarm.mp3"
                        os.startfile(alarm_file_path)
                        break
                    time.sleep(30)  # Check every 30 seconds

            # Command to tell a joke
            elif "joke" in query:
                joke = pyjokes.get_joke()
                speak(joke)

            # Command to shut down the system
            elif "shut down the system" in query:
                os.system("shutdown /s /t 5")

            # Command to restart the system
            elif "restart the system" in query:
                os.system("shutdown /r /t 5")

            # Command to increase the volume
            elif "volume up" in query:
                pyautogui.press("volumeup")

            # Command to decrease the volume
            elif "volume down" in query:
                pyautogui.press("volumedown")
            
            # Command to mute the volume
            elif "mute" in query:
                pyautogui.press("volumemute")

            # Command to check internet speed
            elif "internet speed" in query: 
                try:
                    os.system ('cmd /k "speedtest"')
                except:
                    speak("sorry unable to find")

            elif "no thanks" in query:
                speak("Thank you for using me.")
                break;
    
            speak("anything else")