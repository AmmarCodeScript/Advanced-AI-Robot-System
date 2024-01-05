import sys
sys.path.append('D:/2024/Arcada robot/ArcadaRobot/Linux/Flask/chatboot')

from TextToSpeechEngine import TextToSpeechEngine, Thread
from chatNLP import askRobot
import speech_recognition as sr

tts_engine = TextToSpeechEngine()
userinputText = "hello my names Snow  TechLabs how i can help you!"

def splitWords(textinput):
    password_list = []
    words = textinput.split()  # Split the input text into words
    password_list.extend(words)
    return password_list

def text_exit_match(userInput):
    exit_list = "out end exit bye goodbye stop close off"
    userInput = splitWords(userInput)
    exit_list = splitWords(exit_list)
    # Loopa igenom varje lösenord i exit_list
    for attempt in exit_list:
        if attempt in userInput:
            print (attempt)
            return True  # Lösenordet har hittats
        else: False

def get_askRobot(input):
    textsplit = text_exit_match(input)
    if textsplit: 
        return input
    x = askRobot([input])
    print(x)
    Thread(tts_engine.speak(x, "Female"))
    return x

callIsOpen = False
def stopCall():
    global callIsOpen
    callIsOpen = False

def listen_to_voice(input):
    textsplit = text_exit_match(input)
    if textsplit:
        return input
    
    error_list =[]
    callIsOpen = True
    while callIsOpen:
        if len(error_list) >= 2:break
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            textsplit = text_exit_match(text)

            if textsplit:
                print("You said:", text)
                t = "Thank you for using our robot app. The application is now exiting."
                Thread(tts_engine.speak(t, "Female"))
                break
            
            print("You said:", text)
            get_askRobot(text)
        except sr.UnknownValueError:
            
            t = "Sorry, could not understand audio."
            error_list.append(t)
            Thread(tts_engine.speak(t, "Female"))
            print(t)
        except sr.RequestError as e:
            t = "Could not request results from Arcada Speech Recognition service; "
            Thread(tts_engine.speak(t, "Female"))
            print(t)


# listen_to_voice("hello")