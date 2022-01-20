# UPDATE: just before delivering this I realised that the mic input
# takes a long time to 'load'. This is probably related to the mic 
# power level.

# Important: the execution is blocked until the voice is done talking
# To disable the voice input and enable text input do a search in this 
# file for the words: "comment for text input" and then comment/uncomment
# the according lines appropriately.

# This import is done by the speech_recognition object
# import pyaudio
import socket
import sys

# To recognize the voice input and convert it to text.
import speech_recognition as sr
from speech_recognition import UnknownValueError
from speech_recognition import RequestError

# To 'speak' the response
import pyttsx3


# Convert some text to voice and 'speak' it.
def SpeakText(text):
    engine = pyttsx3.init(debug=True)
    
    # set speed of speeking
    engine. setProperty("rate", 145)
    engine.say(text)     
    engine.runAndWait()

# Instantiate a voice recognizer object
# alexis is the voice recognizer
# Default alexis values: 
# seconds of non-speaking audio before a phrase is considered complete: 0.8
# minimum seconds of speaking audio before we consider the speaking audio a phrase: 0.3
alexis = sr.Recognizer() 

# Set server address
HOST, PORT = "localhost", 65000

print("Start speaking only when you see \"Listening...\" in your screen.")
print("If your voice never gets sent try 'playing' with the mic power level.\n\n")
# Forever. User needs to Ctrl+C to stop the program.
while(1):

    # create a Microphone instance
    with sr.Microphone() as mic:
        try:
            # Adjust the energy for recording based on surrounding noise levels.
            #alexis.adjust_for_ambient_noise(mic, duration=0.5)

            #listens for the user's input 
            print("\nTry to reduce noise while the program is being executed.")
            print("Listening...")
            voice_input = alexis.listen(mic) # comment for text input

            # recognize the voice_input and convert it to text
            # Either Google or Sphinx are free. Sphinx can work offline.
            # Raises a ``speech_recognition.UnknownValueError`` exception if the speech is unintelligible.
            # Raises a ``speech_recognition.RequestError`` exception if the speech recognition
            # operation failed, if the key isn't valid, or if there is no internet connection.
            recognized_text_input = alexis.recognize_google(voice_input) # comment for text input
            #recognized_text_input = input("enter something:\n> ") # uncomment for text input
            recognized_text_input = recognized_text_input.lower()
            print("Recognized Text: " + recognized_text_input)
            
            # For each phrase, we open a new socket. This 'with' statement
            # automatically closes the socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Connect to server
                sock.connect((HOST, PORT))
                # send the recognized text
                data = recognized_text_input
                sock.sendall(bytes(data + "\n", "utf-8"))

                # get server's response
                received = str(sock.recv(1024), "utf-8")
                
                # print the data that was sent and received.
                print(f"Sent this text: {data}")
                print(f"Received this : {received}")
                print("Start speaking only when you see \"Listening...\" in your screen.")
                print("If your voice never gets sent try increasing mic power level.")
                # Speak alexis' response
                # Should be done in another thread.
                SpeakText(received)

        except RequestError as e:
            print("A working internet connection is needed.")
            print("There was an error with the voice recognition request")
            print(e)

        except UnknownValueError:
            print("Could not recognize what you said.")

# 
# This segment is a left-over from my testing on whether a
# greek voice can be used. It seems like neither a greek voice
# or a female voice can be set.
# 
# engine = pyttsx3.init("espeak", debug=True)
# voices = engine.getProperty('voices')
# print(voices[10])
# engine.setProperty("voice", voice[10].id)
# print(engine.getProperty("voice"))
# engine.say("hello, how are you?")
# engine.runAndWait()
# exit(1)
# 