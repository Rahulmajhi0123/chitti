from flask import Flask, request
import struct
import pvporcupine
import pyaudio
import speech_recognition
import threading

from assistant_functions.date_time import date_time
from assistant_functions.location import location
from assistant_functions.open_browser import assistant_browser
from assistant_functions.repeat import repeat
from assistant_functions.reply import reply
from assistant_functions.speak_listen import speak_listen
from assistant_functions.timer import timer
from assistant_functions.weathe import weather
from assistant_functions.music_player import music_player
from assistant_functions.music_player import MusicPlayer
from intentclassification.intent_classification import IntentClassifier
from speech_recognition import WaitTimeoutError

class Assistant:
    
    def __init__(self, name, intentclassifier):
        self.name = name
        self.music_player = music_player
        self.music_player = MusicPlayer()
        self.intentclassifier = intentclassifier
        
    def reply(self, text):
        intent = self.intentclassifier.predict(text)
        if intent == 'leaving':
            speak_listen.say("Exiting")
            quit()

        if intent == 'play_music': 
            playlist_path = "playlist"  
            response = self.music_player.play_song_from_playlist(playlist_path) 
            speak_listen.say(response)

        replies = {
            'greeting' : reply,
            'insult' : reply,
            'personal_q' : reply,
            'weather' : weather.main,
            'location' : location.main,
            'open_in_browser':assistant_browser.main,
            'date_time': date_time.main,
            'repeat': repeat.repeat,
            'timer': timer.main,
            'play_music': self.music_player.main,
            }

        try:
            reply_func = replies[intent]

            if callable(reply_func):
                reply_func(text, intent)
        except KeyError:
            speak_listen.say("Sorry, I didn't understand")
        except Exception as e:
            print("Error: " + str(e))


    def main(self):
        print("Ready...Trying to detect Hotword")
        self.porcupine = pvporcupine.create(
            keyword_paths=["चिट्टी_hi_windows_v3_0_0.ppn"], 
            model_path="porcupine_params_hi.pv", 
            access_key="ycUy8TH7yGERhHplNA0l2Rzc5gBT/e/z0NJ2zcOKYl0FfjILKDEPTg=="
        )
        self.pa = pyaudio.PyAudio()  # Initialize PyAudio object

        while True:
            try:
                self.audio_stream = self.pa.open(
                    rate=self.porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=self.porcupine.frame_length
                )

                self.listen_for_hotword()  # Call hotword detection function

            except Exception as e:
                print("Error initializing audio stream:", e)        
        threading.Thread(target=self.listen_for_hotword, daemon=True).start()    

    def listen_for_hotword(self):
        while True:
            try:
                pcm = self.audio_stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                keyword_index = self.porcupine.process(pcm)

                if keyword_index >= 0:
                    if self.music_player.is_playing:
                        self.music_player.pause_song()  # Pause music
                    print("Hotword Detected")
                    self.audio_stream.close()
                    self.process_user_command()  
                    if self.music_player.is_paused:
                        self.music_player.resume_song()  # Resume music
            except Exception as e:
                print("Error in listen loop:", e)

        threading.Thread(target=listen_loop, daemon=True).start()

    def process_user_command(self):
        while True:
            try:
                said = speak_listen.listen()
                print(said)

                if said:
                    self.reply(said)
                else:
                    print("No speech detected.")

            except WaitTimeoutError:
                print("No speech detected within the timeout period. Please speak again.")
            except speech_recognition.UnknownValueError:
                print("Sorry, I didn't catch that.")
            except Exception as e:
                print("An error occurred during speech recognition:", e)

    def play_song_from_playlist(self, text, intent):
        playlist_path = "playlist"  # Replace with your playlist location
        response = self.music_player.play_song_from_playlist(playlist_path)
        speak_listen.say(response) 

                
# import speech_recognition as sr

# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(f"Microphone with name \"{name}\" found for `Microphone(device_index={index})`")

                
intentclassifier = IntentClassifier()
assistant = Assistant("चिट्टी", intentclassifier)  
assistant.main()

app = Flask(__name__)

@app.route('/process_command', methods=['POST'])
def process_command():
    command = request.json['command']
    assistant_response = assistant.reply(command)  
    return assistant_response 