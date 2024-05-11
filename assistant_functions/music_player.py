import os
import random
import pygame 
import threading

from assistant_functions.determine_most_similar import determine_most_similar_phrase
from assistant_functions.speak_listen import speak_listen

class MusicPlayer: 
    def __init__(self):
        self.is_playing = False
        self.is_paused = False

    def main(self, text, intent):
        samples = {
            "play music": {'func': self.play_song, 'param': None},
            "play song": {'func': self.play_song, 'param': None},
            "stop music": {'func': self.stop_song, 'param': None}
            # ... Add more variations here 
        }

        most_similar = determine_most_similar_phrase(text, samples)
        func = samples[most_similar]['func']
        param = samples[most_similar]['param']  
        speak_listen.say(func(param))  

    def play_song(self, param):
        if self.is_playing:
            return "Music is already playing"

        playlist_path = "playlist"  # Replace with your actual playlist path
        if not os.path.exists(playlist_path):
            return "Playlist path not found. Please check the path."

        music_files = [f for f in os.listdir(playlist_path) if f.endswith('.mp3')]
        if not music_files:
            return "Playlist is empty."

        song_to_play = random.choice(music_files)
        song_path = os.path.join(playlist_path, song_to_play)

        try:
            # Initialize pygame
            pygame.mixer.init()

            # Load and play the song
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()

            self.is_playing = True  # Mark music as playing

            # Wait in a separate thread until the music finishes playing
            def wait_for_song_end():
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)  # Small delay
                self.is_playing = False  # Mark music as stopped
                pygame.mixer.music.stop() 
                pygame.mixer.quit()

            threading.Thread(target=wait_for_song_end, daemon=True).start()

            return f"Playing {song_to_play}"

        except Exception as e:
            return f"Error playing song: {str(e)}" 
    
    def _play_song_thread(self):
        self.is_playing = True  # Start with assumption of playing

        playlist_path = "playlist" 
        if not os.path.exists(playlist_path):
            self.is_playing = False
            return "Playlist path not found. Please check the path."

    def play_song_from_playlist(self, playlist_path):
        if not os.path.exists(playlist_path):
            return "Playlist path not found. Please check the path."

        music_files = [f for f in os.listdir(playlist_path) if f.endswith('.mp3')]

        if music_files:
            song_to_play = random.choice(music_files)
            song_path = os.path.join(playlist_path, song_to_play)

            try:
                # Initialize pygame
                pygame.init()
                pygame.mixer.init()

                # Load and play the song
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play()

                # Wait until the music finishes playing
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

                pygame.mixer.quit()
                pygame.quit()

                return f"Playing {song_to_play}"
            except Exception as e:
                return f"Error playing song: {str(e)}"
        else:
            return "Playlist is empty."
        self.is_playing = False  # Set to False when music stops

    def stop_song(self, param):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            return "Music stopped"
        else:
            return "Music is not currently playing"
        
    def pause_song(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_paused = True

    def resume_song(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False

music_player = MusicPlayer() 