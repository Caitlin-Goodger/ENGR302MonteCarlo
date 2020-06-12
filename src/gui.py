import tkinter as tk 
import simulation 
from tkinter import filedialog
from argparse import Namespace
import threading

class MonteCarloApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #App window size
        self.title('Loader')
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True, padx=5,pady=5)
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
        self.rodangle=tk.Entry(self,width=25)
        self.rodangle.grid(column=0, row=2)
        # rdas
        tk.Label(self, text="Rod angle sigma").grid(column=0, row=3)
        self.rodanglesigma=tk.Entry(self,width=25)
        self.rodanglesigma.grid(column=0, row=4)
        # rdd
        tk.Label(self, text="Rod direction").grid(column=0, row=5)
        self.roddirection=tk.Entry(self,width=25)
        self.roddirection.grid(column=0, row=6)
        # rdds
        tk.Label(self, text="Rod direction sigma").grid(column=0, row=7)
        self.roddirectionsigma=tk.Entry(self,width=25)
        self.roddirectionsigma.grid(column=0, row=8)
        # wsa
        tk.Label(self, text="Wind speed").grid(column=1, row=1)
        self.windspeed=tk.Entry(self,width=25)
        self.windspeed.grid(column=1, row=2)
        # wsas
        tk.Label(self, text="Wind speed sigma").grid(column=1, row=7)
        self.windspeedsigma=tk.Entry(self,width=25)
        self.windspeedsigma.grid(column=1, row=8)
        # lat
        tk.Label(self, text="lat").grid(column=0, row=14)
        self.lat=tk.Entry(self,width=25)
        self.lat.grid(column=0, row=15)
        # long
        tk.Label(self, text="long").grid(column=0, row=16)
        self.longa=tk.Entry(self,width=25)
        self.longa.grid(column=0, row=17)
        # n
        tk.Label(self, text="Number of iteration").grid(column=0, row=18)
        self.n=tk.Entry(self,width=25)
        self.n.grid(column=0, row=19)

        tk.Button(self, text='Execute', width=25, command=self.exec,padx=0).grid(column=0, row=20)

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
        if self.windspeedsigma.get() != '':
            args.windspeedsigma = float(self.windspeed.get())
        if self.lat.get() != '':
            args.startlat = float(self.lat.get())
        if self.longa.get() != '':
            args.startlong = float(self.longa.get())
        if self.n.get() != '':
            args.simcount = int(self.n.get())
        
        print(args)
        sim = simulation.Simulation()
        sim.set_args(args)
        thread1 = threading.Thread(target = self.runSims,args=[sim])
        thread1.start()

    def runSims(self,sim):
        self.controller.show_frame("RunningSimulations")
        sim.runSimulation()
        self.controller.show_frame("InputOptions")

class RunningSimulations(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Runnig Simulations").grid(column=0, row=18)

if __name__ == "__main__":
    app = MonteCarloApp()
    app.mainloop()