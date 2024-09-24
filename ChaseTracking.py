import keyboard 
from pygame import mixer 
import os

class ChaseTracking:
    def __init__(self, planes, music_files):
        self.planes = planes
        self.music_file = music_files

        self.pause = 0
        self.global_index = 0

        mixer.init()

        keyboard.add_hotkey('left', lambda: self.__on_left_arrow())
        keyboard.add_hotkey('right', lambda: self.__on_right_arrow())
        keyboard.add_hotkey('space', lambda: self.__on_space())

    def __play_song(self, song_name):
        mixer.music.stop()

        try:
            current_directory = os.getcwd()
            relative_path = "MusicForPlanes/" + song_name + ".mp3"
            file_path = os.path.join(current_directory, relative_path)

            mixer.music.load(file_path)
            
        except:
            mixer.music.load("MusicForPlanes/Default.mp3")
        
        mixer.music.play()

    def __on_space(self):
        if self.pause == 1:
            print("pause")
            mixer.music.unpause()
            self.pause = 0
        else:
            print("unpause")
            mixer.music.pause()
            self.pause = 1

    def __on_left_arrow(self):
        self.global_index -= 1
        if self.global_index < 0:
            self.global_index = 0

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
        mixer.quit()