import tkinter as tk 
import simulation 
from tkinter import filedialog
from argparse import Namespace
r = tk.Tk() 
r.title('Loader') 

class Window:
    def __init__(self, master):
        self.filename = './out.csv'
        tk.Button(master, text='Open Rocket', width=25, command=self.getFile).pack()

        #rda
        tk.Label(master, text="Rod angle").pack()
        self.rodangleInp=tk.StringVar()
        self.rodangle=tk.Entry(master,width=25,textvariable=self.rodangleInp)
        self.rodangle.pack()
        # rdas
        tk.Label(master, text="rod angle sigma").pack()
        self.rodanglesigmaInp=tk.StringVar()
        self.rodanglesigma=tk.Entry(master,width=25,textvariable=self.rodanglesigmaInp)
        self.rodanglesigma.pack()
        # rdd
        tk.Label(master, text="rod direction").pack()
        self.roddirectionInp=tk.StringVar()
        self.roddirection=tk.Entry(master,width=25,textvariable=self.roddirectionInp)
        self.roddirection.pack()
        # rdds
        tk.Label(master, text="rod direction sigma").pack()
        self.roddirectionsigmaInp=tk.StringVar()
        self.roddirectionsigma=tk.Entry(master,width=25,textvariable=self.roddirectionsigmaInp)
        self.roddirectionsigma.pack()
        # wsa
        tk.Label(master, text="wind speed").pack()
        self.windspeedInp=tk.StringVar()
        self.windspeed=tk.Entry(master,width=25,textvariable=self.windspeedInp)
        self.windspeed.pack()
        # wsas
        tk.Label(master, text="wind speed sigma").pack()
        self.windspeedsigmaInp=tk.StringVar()
        self.windspeedsigma=tk.Entry(master,width=25,textvariable=self.windspeedsigmaInp)
        self.windspeedsigma.pack()
        # lat
        tk.Label(master, text="lat").pack() 
        self.latInp=tk.DoubleVar()
        self.lat=tk.Entry(master,width=25,textvariable=self.latInp)
        self.lat.pack()
        # long
        tk.Label(master, text="long").pack()
        self.longaInp=tk.StringVar()
        self.longa=tk.Entry(master,width=25,textvariable=self.longaInp)
        self.longa.pack()
        # n
        tk.Label(master, text="Number of iteration").pack()
        self.nInp=tk.StringVar()
        self.n=tk.Entry(master,width=25,textvariable=self.nInp)
        self.n.pack()

        tk.Button(master, text='Execute', width=25, command=self.exec).pack()

    def getFile(self):
        self.filename =  tk.filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = [("Rocket File","*.ork")])
        print (self.filename)

    def exec(self):
        args = Namespace(rocket='model.ork', output='./out.csv', rodangle=45, rodanglesigma=5, roddirection=0, roddirectionsigma=5,windspeed=15,windspeedsigma=5, simcount=20, lat=0, long=0, n=5)
        
        if self.filename != '':
            args.rocket = self.filename
        if self.rodangle.get() != '':
            args.rodangle = float(self.rodangle.get())
        if self.rodanglesigma.get() != '':
            args.rodanglesigma = float(self.rodanglesigma.get())
        if self.roddirection.get() != '':
            args.roddirection = float(self.roddirection.get())
        if self.roddirectionsigma.get() != '':
            args.roddirectionsigma = float(self.roddirectionsigma.get())
        if self.windspeed.get() != '':
            args.windspeed = float(self.windspeed.get())
            # __ Sigma version
        if self.nInp.get() != '':
            args.simcount = float(self.nInp.get())
        if self.lat.get() != '':
            args.lat = float(self.lat.get())
        if self.longa.get() != '':
            args.long = float(self.longa.get())
        # n iterations
        
        print(args)
        sim = simulation.Simulation()
        sim.set_args(args)
        #sim.parse_args()
        sim.runSimulation()


window=Window(r)
r.mainloop() 