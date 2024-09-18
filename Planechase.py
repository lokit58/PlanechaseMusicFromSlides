import tkinter
import os

from MainWindow import MainWindow

if __name__ == "__main__":
    #PRESENTATION_ID = "1Z6LnFS2RGmgkCkjhRyi6XwxIeewn1dT8uf8-EDcpy-A"

    os.makedirs("MusicForPlanes", exist_ok=True)

    root = tkinter.Tk()
    app = MainWindow(root)
    app.mainloop()


    