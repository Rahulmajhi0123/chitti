import pygame
import os

def play_music(file_path):
    try:
        # Initialize pygame
        pygame.init()

        # Initialize mixer module for audio playback
        pygame.mixer.init()

        # Load the MP3 file
        pygame.mixer.music.load(file_path)

        # Play the loaded MP3 file
        pygame.mixer.music.play()

        # Wait until the music finishes playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Clean up resources
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.quit()

if __name__ == "__main__":
    mp3_file = "playlist/[iSongs.info] 01 - Maate Vinadhuga.mp3"  # Replace with the path to your MP3 file
    if os.path.exists(mp3_file):
        play_music(mp3_file)
    else:
        print("MP3 file not found.")

