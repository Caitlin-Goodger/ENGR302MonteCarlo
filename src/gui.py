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
        
        vnumber = (master.register(self.validateNumber),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        #rda
        tk.Label(master, text="Rod angle").pack()
        self.rodangleInp=tk.StringVar()
        self.rodangle=tk.Entry(master,width=25,textvariable=self.rodangleInp,validate="key",validatecommand=vnumber)
        self.rodangle.pack()
        # rdas
        tk.Label(master, text="rod angle sigma").pack()
        self.rodanglesigmaInp=tk.StringVar()
        self.rodanglesigma=tk.Entry(master,width=25,textvariable=self.rodanglesigmaInp,validate="key",validatecommand=vnumber)
        self.rodanglesigma.pack()
        # rdd
        tk.Label(master, text="rod direction").pack()
        self.roddirectionInp=tk.StringVar()
        self.roddirection=tk.Entry(master,width=25,textvariable=self.roddirectionInp,validate="key",validatecommand=vnumber)
        self.roddirection.pack()
        # rdds
        tk.Label(master, text="rod direction sigma").pack()
        self.roddirectionsigmaInp=tk.StringVar()
        self.roddirectionsigma=tk.Entry(master,width=25,textvariable=self.roddirectionsigmaInp,validate="key",validatecommand=vnumber)
        self.roddirectionsigma.pack()
        # wsa
        tk.Label(master, text="wind speed").pack()
        self.windspeedInp=tk.StringVar()
        self.windspeed=tk.Entry(master,width=25,textvariable=self.windspeedInp,validate="key",validatecommand=vnumber)
        self.windspeed.pack()
        # wsas
        tk.Label(master, text="wind speed sigma").pack()
        self.windspeedsigmaInp=tk.StringVar()
        self.windspeedsigma=tk.Entry(master,width=25,textvariable=self.windspeedsigmaInp,validate="key",validatecommand=vnumber)
        self.windspeedsigma.pack()
        # lat
        tk.Label(master, text="lat").pack() 
        self.latInp=tk.DoubleVar()
        self.lat=tk.Entry(master,width=25,textvariable=self.latInp,validate="key",validatecommand=vnumber)
        self.lat.pack()
        # long
        tk.Label(master, text="long").pack()
        self.longaInp=tk.StringVar()
        self.longa=tk.Entry(master,width=25,textvariable=self.longaInp,validate="key",validatecommand=vnumber)
        self.longa.pack()
        # n
        tk.Label(master, text="Number of iteration").pack()
        self.nInp=tk.StringVar()
        self.n=tk.Entry(master,width=25,textvariable=self.nInp,validate="key",validatecommand=vnumber)
        self.n.pack()

        tk.Button(master, text='Execute', width=25, command=self.exec).pack()

    def getFile(self):
        self.filename =  tk.filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = [("Rocket File","*.ork")])
        print (self.filename)
    
    def validateNumber(self, d, i, P, s, S, v, V, W):
        # Only supports int (no decimal or minus)
        return S.isdigit()

    def exec(self):
        # print(self.rodAngle.get())
        args = Namespace(outfile='./out.csv', rocket='model.ork', rodangle=45, rodanglesigma=5, roddirection=0, roddirectionsigma=5, simcount=20, startlat=0, startlong=0, windspeed=15)
        
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
        if self.nInp.get() != '':
            args.simcount = float(self.nInp.get())
        if self.lat.get() != '':
            args.startlat = float(self.lat.get())
        if self.longa.get() != '':
            args.startlong = float(self.longa.get())
        if self.windspeed.get() != '':
            args.windspeed = float(self.windspeed.get())
        
        print(args)
        sim = simulation.Simulation()
        sim.set_args(args)
        #sim.parse_args()
        sim.runSimulation()


window=Window(r)
r.mainloop() 