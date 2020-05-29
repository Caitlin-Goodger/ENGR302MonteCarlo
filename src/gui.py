import tkinter as tk 
from tkinter import filedialog
r = tk.Tk() 
r.title('Loader') 

class Window:
    def __init__(self, master):
        tk.Button(master, text='Open Rocket', width=25, command=self.getFile).pack()
        
        vnumber = (master.register(self.validateNumber),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        #rda
        tk.Label(master, text="Rod angle").pack()
        self.rodAngle=tk.StringVar()
        rodAngleInp=tk.Entry(master,width=25,textvariable=self.rodAngle,validate="key",validatecommand=vnumber).pack()
        # rdas
        tk.Label(master, text="rod angle sigma").pack()
        self.rodanglesigmaInp=tk.StringVar()
        rodanglesigma=tk.Entry(master,width=25,textvariable=self.rodanglesigmaInp,validate="key",validatecommand=vnumber).pack()
        # rdd
        tk.Label(master, text="rod direction").pack()
        self.roddirectionInp=tk.StringVar()
        roddirection=tk.Entry(master,width=25,textvariable=self.roddirectionInp,validate="key",validatecommand=vnumber).pack()
        # rdds
        tk.Label(master, text="rod direction sigma").pack()
        self.roddirectionsigmaInp=tk.StringVar()
        roddirectionsigma=tk.Entry(master,width=25,textvariable=self.roddirectionsigmaInp,validate="key",validatecommand=vnumber).pack()
        # wsa
        tk.Label(master, text="wind speed").pack()
        self.windspeedInp=tk.StringVar()
        windspeed=tk.Entry(master,width=25,textvariable=self.windspeedInp,validate="key",validatecommand=vnumber).pack()
        # wsas
        tk.Label(master, text="wind speed sigma").pack()
        self.windspeedsigmaInp=tk.StringVar()
        windspeedsigma=tk.Entry(master,width=25,textvariable=self.windspeedsigmaInp,validate="key",validatecommand=vnumber).pack()
        # lat
        tk.Label(master, text="lat").pack()
        self.latInp=tk.StringVar()
        lat=tk.Entry(master,width=25,textvariable=self.latInp,validate="key",validatecommand=vnumber).pack()
        # long
        tk.Label(master, text="long").pack()
        self.longaInp=tk.StringVar()
        longa=tk.Entry(master,width=25,textvariable=self.longaInp,validate="key",validatecommand=vnumber).pack()
        # n
        tk.Label(master, text="Number of iteration").pack()
        self.nInp=tk.StringVar()
        n=tk.Entry(master,width=25,textvariable=self.nInp,validate="key",validatecommand=vnumber).pack()

        tk.Button(master, text='Execute', width=25, command=self.exec).pack()

    def getFile(self):
        self.filename =  tk.filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = [("Rocket File","*.ork")])
        print (self.filename)
    
    def validateNumber(self, d, i, P, s, S, v, V, W):
        # Only supports int (no decimal or minus)
        return S.isdigit()

    def exec(self):
        print(self.rodAngle.get())


window=Window(r)
r.mainloop() 