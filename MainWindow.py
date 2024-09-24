import tkinter
from GoogleSlidesAPI import GoogleSlidesAPI as GSA
from ChaseTracking import ChaseTracking
import json
import os
import re


class MainWindow(tkinter.Frame):

    def __init__(self, parent):
       
        super().__init__(parent)

        self.chase = None

        self.parent = parent
        self.log_text = "Log:\n"
        self.presentation_ID = ""

        self.presentation_Data = {}

        self.parent.title("Planechase music controller")
        self.parent.minsize(500, 600) # minimální velisost
        self.parent.resizable(True, True) # je okno měnite

        self.create_widgets()

   

    def Log(self, log_input):
        self.log_text = self.log_text + log_input + "\n"
        self.loglbl.config(text = self.log_text )

    def save_to_json(self, data, filename='CurrentPlanechase.json'):
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
            self.Log(f"Data has been written to {filename}")

    def __getPresentationID(self):
        regex = r'/d/([a-zA-Z0-9_-]+)'
        preproccesed_ID = self.inputtxt.get(1.0, "end-1c") 
        match = re.search(regex, preproccesed_ID)
        self.presentation_ID= match.group(1)
         
        if self.presentation_ID == "":
            self.Log("No text in ID")
        else:
            self.Log("ID confirmed: " + self.presentation_ID)
        
    def __getSlides (self):
        if self.presentation_ID == "":
            self.Log("ID is not set")
            return
        
        Google_API = GSA(self.presentation_ID)
        slides = Google_API.getSlides()

        slide_data = []
        for slide in slides:
            slide_data.append({"plane": slide["slideProperties"]["notesPage"]["pageElements"][1]["shape"]["text"]["textElements"][1]["textRun"]["content"]})
            #print(slide["slideProperties"]["notesPage"]["pageElements"][1]["shape"]["text"]["textElements"][1]["textRun"]["content"])

        self.presentation_Data = {
            "id": self.presentation_ID,
            "Planes" : slide_data
        }

        self.save_to_json(self.presentation_Data)

    def __Song_plane_checker(self, music_files, planes): #Possible optimalization with better checker
        for plane in planes["Planes"]:
            #print( plane["plane"].strip())
            for song in music_files:
                #print(song)
                if plane["plane"].strip() == song[:-4]:
                    #self.Log(plane["plane"].strip() +" nalezena schoda :D") #Show only for debug reasons
                    #print(plane["plane"].strip() +" nalezena schoda :D")
                    break

            if plane["plane"].strip() != song[:-4]:
                #print(plane["plane"].strip() + " nenalezena schoda :(")
                self.Log(plane["plane"].strip() + " nenalezena schoda :(")  

    def __Check_songs_againts_planes(self):
        music_files = [f for f in os.listdir(os.path.join(os.getcwd(), "MusicForPlanes")) if os.path.isfile(os.path.join(os.path.join(os.getcwd(), "MusicForPlanes"), f))]
        
        try:
            with open(os.path.join(os.getcwd(), "CurrentPlanechase.json"), "r") as file:
                planes = json.load(file)    

            self.__Song_plane_checker(music_files, planes)
            
        except FileNotFoundError:
            self.Log(f"No downloaded Plannechase.\n")
    
    def __setup(self):
        self.chase = ChaseTracking()
        
    def __get_music_files(self):
        return [f for f in os.listdir(os.path.join(os.getcwd(), "MusicForPlanes")) if os.path.isfile(os.path.join(os.path.join(os.getcwd(), "MusicForPlanes"), f))]
    
    def __get_planes(self):
        try:
            with open(os.path.join(os.getcwd(), "CurrentPlanechase.json"), "r") as file:
                return  json.load(file)    
 
        except FileNotFoundError:
            self.Log(f"No downloaded Plannechase.\n")
            return 0

    def __start_chase(self):
        planes = self.__get_planes()
        if planes == 0:
            return 0
        
        music_files = self.__get_music_files()

        self.chase = ChaseTracking(planes, music_files)

        if self.chase is not None:
            self.Log("Spusť prezentaci pro začátek chasu")
            self.parent.update()
            self.parent.update_idletasks()
            self.chase.start()
            
        else:
            self.Log("Neproběhl setup")

        self.Log("Konec chasu")
    

    def create_widgets(self):
        self.button_1 = tkinter.Button(text="Set presentation ID", command=lambda: self.__getPresentationID())
        self.button_1.grid(row = 0, column = 0, sticky=tkinter.NSEW)

        self.button_2 = tkinter.Button(text="Get slides", command=lambda: self.__getSlides())
        self.button_2.grid(row = 1, column = 0, sticky=tkinter.NSEW)

        self.button_3 = tkinter.Button(text="Check for missing songs", command=lambda: self.__Check_songs_againts_planes())
        self.button_3.grid(row = 2, column = 0, sticky=tkinter.NSEW)

        self.button_4 = tkinter.Button(text="Start chase", command=lambda: self.__start_chase())
        self.button_4.grid(row = 3, column = 0, sticky=tkinter.NSEW)

        self.inputtxt = tkinter.Text(height = 1, width = 60) 
        self.inputtxt.grid(row = 0, column = 1, sticky=tkinter.NSEW)

        self.loglbl = tkinter.Label(text = "") 
        self.loglbl.grid(row = 4, column = 0, sticky=tkinter.NSEW)
