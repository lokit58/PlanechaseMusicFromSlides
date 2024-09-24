import keyboard 
from pygame import mixer 
import time
import os

class ChaseTracking:
    def __init__(self, planes, music_files):
        self.planes = planes
        self.music_file = music_files

        self.global_index = 0

        mixer.init()

        keyboard.add_hotkey('left', lambda: self.__on_left_arrow())
        keyboard.add_hotkey('right', lambda: self.__on_right_arrow())

    def __play_song(self, song_name):
        mixer.music.stop()

        current_directory = os.getcwd()
        relative_path = "MusicForPlanes/" + song_name + ".mp3"
        file_path = os.path.join(current_directory, relative_path)

        mixer.music.load(file_path)
        mixer.music.play()

    def __on_left_arrow(self):
        self.global_index -= 1
        self.__play_song((self.planes["Planes"][self.global_index]["plane"]).strip())

    def __on_right_arrow(self):
        self.global_index += 1
        self.__play_song((self.planes["Planes"][self.global_index]["plane"]).strip())

    def start(self):
        keyboard.wait('ctrl + F5')
        #print((self.planes["Planes"][self.global_index]["plane"]).strip())
        self.__play_song((self.planes["Planes"][self.global_index]["plane"]).strip())
        keyboard.wait('esc')
        mixer.music.stop()