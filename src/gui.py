import tkinter as tk 
from tkinter import filedialog
r = tk.Tk() 
r.title('Loader') 

class Window:
    def __init__(self, master):
        button = tk.Button(master, text='Load', width=25, command=self.getFile) 
        button.pack()

    def getFile(self):
        self.filename =  tk.filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = [("Rocket File","*.ork")])
        print (self.filename)


window=Window(r)
r.mainloop() 