import pyttsx3
import speech_recognition as sr
from playsound import playsound


class Speak_Listen:
    def __init__(self):
        self.speech_engine = pyttsx3.init()
        self.speech_engine.setProperty("rate", 150)

        self.r = sr.Recognizer()
        self.mic = sr.Microphone(device_index=24)

    def say(self, text):
        """Uses pyttsx3 engine text-to-speech to to say 'text' argument"""
        # self.speech_engine.connect('finished-utterance', self.stop_speaking)
        print(text)
        self.speech_engine.say(text, "speech")
        self.speech_engine.runAndWait()
        
    def stop_speaking(self, name, completed):
        self.speech_engine.endLoop()

import pyttsx3
import speech_recognition as sr
from playsound import playsound


class Speak_Listen:
    def __init__(self):
        self.speech_engine = pyttsx3.init()
        self.speech_engine.setProperty("rate", 150)

        self.r = sr.Recognizer()
        self.mic = sr.Microphone(device_index=1)

    def say(self, text):
        """Uses pyttsx3 engine text-to-speech to to say 'text' argument"""
        # self.speech_engine.connect('finished-utterance', self.stop_speaking)
        print(text)
        self.speech_engine.say(text, "speech")
        self.speech_engine.runAndWait()
        
    def stop_speaking(self, name, completed):
        self.speech_engine.endLoop()

    def listen(self):
        """Uses speech_recognition library to listen to get audio input and understand what the user is saying"""
        try:
            with self.mic as source:
                print("Listening")
                self.r.non_speaking_duration = 0.5
                audio = self.r.listen(source, timeout=7, phrase_time_limit=5)
                return (self.r.recognize_google(audio))
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period. Please speak again.")
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except AssertionError:
            print("Audio source must be entered before listening.")
        except AttributeError:
            print("'NoneType' object has no attribute 'close'")


speak_listen = Speak_Listen()