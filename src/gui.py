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
        print("Starting gui")
        #App window size
        self.title('Loader')
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True, padx = 5, pady = 5)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.geometry("500x450")

        frame = InputOptions(container, self)
        frame.grid(row = 0, column = 0, sticky = "nsew")
        frame.update()

class InputOptions(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.filename = 'model.ork'
        self.outfile = './out.csv'
        tk.Button(self, text = 'select .ork file', width = 25, command=self.getFile).grid(column = 0, row = 0)
        #rda
        self.rodAngleEntry = tk.StringVar()
        self.rodAngle = tk.Entry(self, width=25,textvariable=self.rodAngleEntry)
        self.createLabel(tk, self.rodAngle, "Rod angle", 0, 1, 45)
        # rdas
        self.rodAngleSigmaEntry = tk.StringVar()
        self.rodAngleSigma = tk.Entry(self,width=25,textvariable=self.rodAngleSigmaEntry)
        self.createLabel(tk, self.rodAngleSigma, "Rod angle sigma", 0, 3, 5)
        # rdd
        self.rodDirectionEntry = tk.StringVar()
        self.rodDirection = tk.Entry(self,width=25,textvariable=self.rodDirectionEntry)
        self.createLabel(tk, self.rodDirection, "Rod direction", 0, 5, 0)
        # rdds
        self.rodDirectionSigmaEntry = tk.StringVar()
        self.rodDirectionSigma = tk.Entry(self,width=25,textvariable=self.rodDirectionSigmaEntry)
        self.createLabel(tk, self.rodDirectionSigma, "Rod direction sigma", 0, 7 , 5)
        # wsa
        self.windSpeedEntry = tk.StringVar()
        self.windSpeed = tk.Entry(self,width=25,textvariable=self.windSpeedEntry)
        self.createLabel(tk, self.windSpeed, "Wind speed", 1, 1, 15)
        # wsas
        self.windSpeedSigmaEntry = tk.StringVar()
        self.windSpeedSigma = tk.Entry(self,width=25,textvariable=self.windSpeedSigmaEntry)
        self.createLabel(tk, self.windSpeedSigma, "Wind speed sigma", 1, 3, 5)
        # wd
        self.windDirectionEntry = tk.StringVar()
        self.windDirection = tk.Entry(self,width=25,textvariable=self.windDirectionEntry)
        self.createLabel(tk, self.windDirection, "Wind direction", 1, 5, 0)
        # lat
        self.latEntry = tk.StringVar()
        self.lat = tk.Entry(self,width=25,textvariable=self.latEntry)
        self.createLabel(tk, self.lat, "lat", 0, 14, 0)
        # long
        self.longaEntry = tk.StringVar()
        self.longa = tk.Entry(self,width=25,textvariable=self.longaEntry)
        self.createLabel(tk, self.longa, "long", 0, 16, 0)
        # n
        self.nEntry = tk.StringVar()
        self.n = tk.Entry(self,width=25,textvariable=self.nEntry)
        self.createLabel(tk, self.n, "Number of iteration", 0, 18, 25)
        # n
        self.motorPerformanceEntry = tk.StringVar()
        self.motorPerformance = tk.Entry(self,width=25,textvariable=self.motorPerformanceEntry)
        self.createLabel(tk, self.motorPerformance, "Motor performance variation", 1, 7, 0.1)
        # load weather
        tk.Button(self, text='Load data from csv', width=25, command=self.getWeather).grid(column=1, row=0)

        tk.Button(self, text='Execute', width=25, command=self.exec,padx=0).grid(column=0, row=20)

    def createLabel(self, tk, var, name, colNum, rowNum, insertValue):
        var.insert(0,insertValue)
        tk.Label(self, text = name).grid(column = colNum, row = rowNum)
        var.grid(column = colNum, row = rowNum+1)

    def getFile(self):
        self.filename = tk.filedialog.askopenfilename(initialdir = "./", title = "Select file", filetypes = [("Rocket File","*.ork")])

    def getWeather(self):
        ''' Read parameters from csv file, example:
        windspeed,windspeedsigma,rodangle,rodanglesigma,roddirection,roddirectionsigma,lat,long
        10,5,10,5,0,5,40,40 '''
        self.weather_name =  tk.filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = [("Weather data","*.csv")])
        data = simulation.WeatherData().read_weather_data(self.weather_name)
        
        array = data.to_numpy()
        
        for n in range(0, len(array[0])):
            name = array[0][n]
            value = array[1][n]
            if name == "rodAngle":
                self.rodAngleEntry.set(value)
            if name == "rodAngleSigma":
                self.rodAngleSigmaEntry.set(value)
            if name == "rodDirection":
                self.rodDirectionEntry.set(value)
            if name == "rodDirectionSigma":
                self.rodDirectionSigmaEntry.set(value)
            if name == "windSpeed":
                self.windSpeedEntry.set(value)
            if name == "windSpeedSigma":
                self.windSpeedSigmaEntry.set(value)
            if name == "lat":
                self.latEntry.set(value)
            if name == "long":
                self.longaEntry.set(value)
            if name == "windDirection":
                self.windDirectionEntry.set(value)



    def exec(self):
        values = Namespace(rocket=self.filename, outfile='./out.csv', rodAngle=self.rodAngle.get(), rodAngleSigma=self.rodAngleSigma.get(), 
                    rodDirection=self.rodDirection.get(), rodDirectionSigma=self.rodDirectionSigma.get(),
                    windSpeed=self.windSpeed.get(),windSpeedSigma=self.windSpeedSigma.get(), 
                    startLat=self.lat.get(),startLong=self.longa.get(), simCount=self.n.get(), windDirection=self.windDirection.get(), motorPerformance = self.motorPerformance.get())

        if(self.checkValues(values)):
            self.parseAndRun(values)
        else:
            pass
            # TODO give feedback to user

    def checkValues(self, values):
        for k in values.__dict__:
            if values.__dict__[k] != '':                
                if k == 'rocket' or k == 'outfile':
                    pass # is string
                elif k == 'simCount':
                    if not (self.checkIntValue(values.__dict__[k])):
                        return False
                else:
                    if not (self.checkFloatValue(values.__dict__[k])):
                        return False
        return True

    def checkIntValue(self,value):
        try: 
            int(value)
            return True
        except ValueError:
            return False
    def checkFloatValue(self,value):
        try: 
            float(value)
            return True
        except ValueError:
            return False

    def parseAndRun(self, values):
        args = Namespace(rocket='model.ork', outfile='./out.csv', rodAngle=45, rodAngleSigma=5, 
                        rodDirection=0, rodDirectionSigma=5,
                        windSpeed=15,windSpeedSigma=5, 
                        startLat=0,startLong=0, simCount=25, windDirection=0, motorPerformance = 0.1)

        for k in args.__dict__:
            if values.__dict__[k] != '':                
                if k == 'rocket' or k == 'outfile':
                    args.__dict__[k] = values.__dict__[k]
                elif k == 'simCount':
                    args.__dict__[k] = int(values.__dict__[k])
                else:
                    args.__dict__[k] = float(values.__dict__[k])
        
        sim = simulation.Simulation()
        sim.set_args(args)
        self.runSims(sim)

    def runSims(self,sim):
        self.showLoading()
        self.resp = sim.runSimulation()
        self.controller.results = self.resp.getResults()
        self.showResults()

    def showResults(self):
        self.destroy()
        resultFrame = Results(self.parent, self.controller)
        resultFrame.grid(row = 0, column = 0, sticky = "nsew")
        resultFrame.displayResults()
        resultFrame.update_idletasks() 

    def showLoading(self):
        self.destroy()
        loadingFrame = RunningSimulations(self.parent, self.controller)
        loadingFrame.grid(row = 0, column = 0, sticky = "nsew")
        loadingFrame.stepProgressBar()
        loadingFrame.update()

class RunningSimulations(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text = "Running Simulations").grid(column = 0, row = 0)
        self.controller = controller

        self.progressBar = ttk.Progressbar(self,orient='horizontal', mode='indeterminate')
        self.progressBar.grid(column=0, row=1)    
        self.stepProgressBar()    

    def stepProgressBar(self):
        self.progressBar.step(5)

class Results(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text = "Results").grid(column = 0, row = 0)
        self.controller = controller

    def displayResults(self):
        count = 1
        for k in list(vars(self.controller.results).keys()):
            tk.Label(self, text = k).grid(column = 0, row = count)
            tk.Label(self, text=getattr(self.controller.results, k)).grid(column = 1, row = count)
            count = count + 1

if __name__ == "__main__":
    app = MonteCarloApp()
    app.mainloop()