import tkinter as tk 
import tkinter.ttk as ttk
import simulation 
import asyncio
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
        self.results = Namespace()
        for f in (InputOptions, RunningSimulations, Results):
            page_name = f.__name__
            frame = f(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("InputOptions")

    #Switch which frame is visible
    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()
        frame.update()
        if isinstance(frame, Results):
                frame.displayResults()

class InputOptions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.filename = 'model.ork'
        self.outfile = './out.csv'
        tk.Button(self, text='Open Rocket', width=25, command=self.getFile).grid(column=0, row=0)

        #rda
        self.rodangle = tk.Entry(self, width=25)
        self.rodangle.insert(0, 45)
        self.createLabel(tk, self.rodangle, "Rod angle", 0, 1)
        # rdas
        self.rodanglesigma = tk.Entry(self,width=25)
        self.rodanglesigma.insert(0, 5)
        self.createLabel(tk, self.rodanglesigma, "Rod angle sigma", 0, 3)
        # rdd
        self.roddirection = tk.Entry(self,width=25)
        self.roddirection.insert(0, 0)
        self.createLabel(tk, self.roddirection, "Rod direction", 0, 5)
        # rdds
        self.roddirectionsigma = tk.Entry(self,width=25)
        self.roddirectionsigma.insert(0, 5)
        self.createLabel(tk, self.roddirectionsigma, "Rod direction sigma", 0, 7)
        # wsa
        self.windspeed = tk.Entry(self,width=25)
        self.windspeed.insert(0, 15)
        self.createLabel(tk, self.windspeed, "Wind speed", 1, 1)
        # wsas
        self.windspeedsigma = tk.Entry(self,width=25)
        self.windspeedsigma.insert(0, 5)
        self.createLabel(tk, self.windspeedsigma, "Wind speed sigma", 1, 7)
        # lat
        self.lat = tk.Entry(self,width=25)
        self.lat.insert(0, 0)
        self.createLabel(tk, self.lat, "lat", 0, 14)
        # long
        self.longa = tk.Entry(self,width=25)
        self.longa.insert(0, 0)
        self.createLabel(tk, self.longa, "long", 0, 16)
        # n
        self.n = tk.Entry(self,width=25)
        self.n.insert(0, 25)
        self.createLabel(tk, self.n, "Number of iteration", 0, 18)

        tk.Button(self, text='Execute', width=25, command=self.exec,padx=0).grid(column=0, row=20)

    def createLabel(self, tk, var, name, colNum, rowNum):
        tk.Label(self, text=name).grid(column=colNum, row=rowNum)
        var.grid(column=colNum, row=rowNum+1)

    def getFile(self):
        self.filename =  tk.filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = [("Rocket File","*.ork")])

    def exec(self):
        args = Namespace(rocket='model.ork', outfile='./out.csv', rodangle=45, rodanglesigma=5, 
                        roddirection=0, roddirectionsigma=5,
                        windspeed=15,windspeedsigma=5, 
                        startlat=0,startlong=0, simcount=25)
        
        values = Namespace(rocket=self.filename, outfile='./out.csv', rodangle=self.rodangle.get(), rodanglesigma=self.rodanglesigma.get(), 
                    roddirection=self.roddirection.get(), roddirectionsigma=self.roddirectionsigma.get(),
                    windspeed=self.windspeed.get(),windspeedsigma=self.windspeedsigma.get(), 
                    startlat=self.lat.get(),startlong=self.longa.get(), simcount=self.n.get())

        for k in args.__dict__:
            if values.__dict__[k] != '':                
                if k == 'rocket' or k == 'outfile':
                    args.__dict__[k] = values.__dict__[k]
                elif k == 'simcount':
                    args.__dict__[k] = int(values.__dict__[k])
                else:
                    args.__dict__[k] = float(values.__dict__[k])
        
        sim = simulation.Simulation()
        sim.set_args(args)
        thread1 = threading.Thread(target = self.runSims,args=[sim])
        thread1.start()

    def runSims(self,sim):
        self.controller.show_frame("RunningSimulations")
        self.controller.results = sim.runSimulation()
        self.controller.show_frame("Results")

class RunningSimulations(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Running Simulations").grid(column=0, row=0)
        self.controller = controller
        self.progressBar = ttk.Progressbar(self,orient='horizontal', mode='indeterminate')
        self.progressBar.grid(column=0, row=1)    
        self.stepProgressBar()    

    def stepProgressBar(self):
        self.progressBar.step(5)
        self.after(50, self.stepProgressBar) # run again after 50ms,

class Results(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Results").grid(column=0, row=0)
        self.controller = controller

    def displayResults(self):
        count = 1
        for k in list(vars(self.controller.results).keys()):
            tk.Label(self, text=k).grid(column=0, row=count)
            tk.Label(self, text=getattr(self.controller.results, k)).grid(column=1, row=count)
            count = count + 1

if __name__ == "__main__":
    app = MonteCarloApp()
    app.mainloop()