import tkinter as tk 
import tkinter.ttk as ttk
import simulation 
import asyncio
from tkinter import filedialog
from argparse import Namespace
import threading
import Events

class MonteCarloApp(tk.Tk,Events.Events):
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
        self.createLabel(tk, self.rodangle, "Rod angle", 0, 1, 45)
        # rdas
        self.rodanglesigma = tk.Entry(self,width=25)
        self.createLabel(tk, self.rodanglesigma, "Rod angle sigma", 0, 3, 5)
        # rdd
        self.roddirection = tk.Entry(self,width=25)
        self.createLabel(tk, self.roddirection, "Rod direction", 0, 5, 0)
        # rdds
        self.roddirectionsigma = tk.Entry(self,width=25)
        self.createLabel(tk, self.roddirectionsigma, "Rod direction sigma", 0, 7 , 5)
        # wsa
        self.windspeed = tk.Entry(self,width=25)
        self.createLabel(tk, self.windspeed, "Wind speed", 1, 1, 15)
        # wsas
        self.windspeedsigma = tk.Entry(self,width=25)
        self.createLabel(tk, self.windspeedsigma, "Wind speed sigma", 1, 7, 5)
        # lat
        self.lat = tk.Entry(self,width=25)
        self.createLabel(tk, self.lat, "lat", 0, 14, 0)
        # long
        self.longa = tk.Entry(self,width=25)
        self.createLabel(tk, self.longa, "long", 0, 16, 0)
        # n
        self.n = tk.Entry(self,width=25)
        self.createLabel(tk, self.n, "Number of iteration", 0, 18, 25)

        tk.Button(self, text='Execute', width=25, command=self.exec,padx=0).grid(column=0, row=20)

    def createLabel(self, tk, var, name, colNum, rowNum, insertValue):
        var.insert(0,insertValue)
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
        simListen=sim.set_args(args)
        simListen.on("sim_stage_done", self.stagedone)
        self.controller.trigger("sim_set_simcount", args.__dict__["simcount"])
        thread1 = threading.Thread(target = self.runSims,args=[sim])
        thread1.start()

    def runSims(self,sim):
        self.controller.show_frame("RunningSimulations")
        self.resp=sim.runSimulation()
        self.controller.results = self.resp.getResults()
        self.controller.show_frame("Results")
    
    def stagedone(self,step):
        self.controller.trigger("sim_stage_done",step)

class RunningSimulations(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Running Simulations").grid(column=0, row=0)
        self.controller = controller
        self.progressBar = ttk.Progressbar(self,orient='horizontal', mode='determinate',length = 100)
        self.progressBar.grid(column=0, row=1)    
        self.totalSteps=1
        self.controller.on("sim_stage_done",self.setStep)
        self.controller.on("sim_set_simcount",self.stepWorth)
        self.progressBar["value"]=0
        self.progressBar.update()
    
    def stepWorth(self,total):
        self.totalSteps=total
    
    def setStep(self,upto):
        self.progressBar["value"]=((upto+1)/self.totalSteps)*100
        self.progressBar.update_idletasks()

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