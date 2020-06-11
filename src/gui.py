import tkinter as tk 
import simulation 
from tkinter import filedialog
from argparse import Namespace

class MonteCarloApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #App window size
        self.geometry("500x500")
        self.title('Loader')
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Layer frames on top of each other. The top of the stack order is the visible page.
        self.frames = {}
        for F in (InputOptions, RunningSimulations):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("InputOptions")

    #Switch which frame is visible
    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()

class InputOptions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.filename = './out.csv'
        tk.Button(self, text='Open Rocket', width=25, command=self.getFile).grid(column=0, row=0)

        #rda
        tk.Label(self, text="Rod angle").grid(column=0, row=1)
        self.rodangleInp=tk.StringVar()
        self.rodangle=tk.Entry(self,width=25,textvariable=self.rodangleInp)
        self.rodangle.grid(column=0, row=2)
        # rdas
        tk.Label(self, text="rod angle sigma").grid(column=0, row=3)
        self.rodanglesigmaInp=tk.StringVar()
        self.rodanglesigma=tk.Entry(self,width=25,textvariable=self.rodanglesigmaInp)
        self.rodanglesigma.grid(column=0, row=4)
        # rdd
        tk.Label(self, text="rod direction").grid(column=0, row=5)
        self.roddirectionInp=tk.StringVar()
        self.roddirection=tk.Entry(self,width=25,textvariable=self.roddirectionInp)
        self.roddirection.grid(column=0, row=6)
        # rdds
        tk.Label(self, text="rod direction sigma").grid(column=0, row=7)
        self.roddirectionsigmaInp=tk.StringVar()
        self.roddirectionsigma=tk.Entry(self,width=25,textvariable=self.roddirectionsigmaInp)
        self.roddirectionsigma.grid(column=0, row=8)
        # wsa
        tk.Label(self, text="wind speed").grid(column=0, row=9)
        self.windspeedInp=tk.StringVar()
        self.windspeed=tk.Entry(self,width=25,textvariable=self.windspeedInp)
        self.windspeed.grid(column=0, row=10)
        # wsas
        tk.Label(self, text="wind speed sigma").grid(column=0, row=11)
        self.windspeedsigmaInp=tk.StringVar()
        self.windspeedsigma=tk.Entry(self,width=25,textvariable=self.windspeedsigmaInp)
        self.windspeedsigma.grid(column=0, row=12)
        # lat
        tk.Label(self, text="lat").grid(column=0, row=13)
        self.latInp=tk.DoubleVar()
        self.lat=tk.Entry(self,width=25,textvariable=self.latInp)
        self.lat.grid(column=0, row=14)
        # long
        tk.Label(self, text="long").grid(column=0, row=15)
        self.longaInp=tk.StringVar()
        self.longa=tk.Entry(self,width=25,textvariable=self.longaInp)
        self.longa.grid(column=0, row=16)
        # n
        tk.Label(self, text="Number of iteration").grid(column=0, row=17)
        self.nInp=tk.StringVar()
        self.n=tk.Entry(self,width=25,textvariable=self.nInp)
        self.n.grid(column=0, row=18)

        tk.Button(self, text='Execute', width=25, command=self.exec).grid(column=0, row=19)

    def getFile(self):
        self.filename =  tk.filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = [("Rocket File","*.ork")])
        print (self.filename)

    def exec(self):
        args = Namespace(rocket='model.ork', outfile='./out.csv', rodangle=45, rodanglesigma=5, 
                        roddirection=0, roddirectionsigma=5,
                        windspeed=15,windspeedsigma=5, 
                        startlat=0,startlong=0, simcount=20)
        
        if self.filename != '':
            args.outfile = self.filename
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
        if self.windspeedsigmaInp.get() != '':
            args.windspeedsigma = float(self.windspeed.get())
        if self.lat.get() != '':
            args.startlat = float(self.lat.get())
        if self.longa.get() != '':
            args.startlong = float(self.longa.get())
        if self.nInp.get() != '':
            args.simcount = int(self.nInp.get())
        
        print(args)
        sim = simulation.Simulation()
        sim.set_args(args)
        #sim.parse_args()
        sim.runSimulation()
        self.controller.show_frame("RunningSimulations")

class RunningSimulations(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("InputOptions"))
        button.grid(column=0, row=0)

if __name__ == "__main__":
    app = MonteCarloApp()
    app.mainloop()