import tkinter as tk 
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo
import simulation 
import upwind_rocket_vectors
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
        container = tk.Frame(self, name="frame")
        container.pack(side = "top", fill = "both", expand = True, padx = 5, pady = 5)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.geometry("700x550")

        self.frame = InputOptions(container, self)
        self.frame.grid(row = 0, column = 0, sticky = "nsew")
        self.frame.update()

class InputOptions(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.filename = 'model.ork'
        self.outfile = 'out.csv'
        tk.Button(self, text = 'select .ork file', width = 25, command=self.getFile).grid(column = 0, row = 0)
        tk.Button(self, text = 'select output file', width = 25, command=self.saveFile).grid(column = 2, row = 0)
        
        #Monte carlo header
        tk.Label(self, text = "Monte Carlo Parameters").grid(column = 0, row = 2,columnspan = 2)
        
        #rda
        self.rodAngleEntry = tk.StringVar()
        self.rodAngle = tk.Entry(self, width=25,textvariable=self.rodAngleEntry)
        self.createLabel(tk, self.rodAngle, "Rod angle", 0, 4, 45)
        self.rowconfigure(3, minsize=10)
        # rdas
        self.rodAngleSigmaEntry = tk.StringVar()
        self.rodAngleSigma = tk.Entry(self,width=25,textvariable=self.rodAngleSigmaEntry)
        self.createLabel(tk, self.rodAngleSigma, "Rod angle sigma", 0, 7, 5)
        self.rowconfigure(6, minsize=10)
        # rdd
        self.rodDirectionEntry = tk.StringVar()
        self.rodDirection = tk.Entry(self,width=25,textvariable=self.rodDirectionEntry)
        self.createLabel(tk, self.rodDirection, "Rod direction", 0, 10, 0)
        self.rowconfigure(9, minsize=10)
        # rdds
        self.rodDirectionSigmaEntry = tk.StringVar()
        self.rodDirectionSigma = tk.Entry(self,width=25,textvariable=self.rodDirectionSigmaEntry)
        self.createLabel(tk, self.rodDirectionSigma, "Rod direction sigma", 0, 13 , 5)
        self.rowconfigure(12, minsize=15)
        # wsa
        self.windSpeedEntry = tk.StringVar()
        self.windSpeed = tk.Entry(self,width=25,textvariable=self.windSpeedEntry)
        self.createLabel(tk, self.windSpeed, "Wind speed", 1, 13, 15)
        # wsas
        self.windSpeedSigmaEntry = tk.StringVar()
        self.windSpeedSigma = tk.Entry(self,width=25,textvariable=self.windSpeedSigmaEntry)
        self.createLabel(tk, self.windSpeedSigma, "Wind speed sigma", 1, 16, 5)
        # wd
        self.windDirectionEntry = tk.StringVar()
        self.windDirection = tk.Entry(self,width=25,textvariable=self.windDirectionEntry)
        self.createLabel(tk, self.windDirection, "Wind direction", 1, 19, 0)
        # lat
        self.latEntry = tk.StringVar()
        self.lat = tk.Entry(self,width=25,textvariable=self.latEntry)
        self.createLabel(tk, self.lat, "lat", 0, 16, 0)
        self.rowconfigure(15, minsize=15)
        # long
        self.longaEntry = tk.StringVar()
        self.longa = tk.Entry(self,width=25,textvariable=self.longaEntry)
        self.createLabel(tk, self.longa, "long", 0, 19, 0)
        self.rowconfigure(18, minsize=15)
        # n
        self.nEntry = tk.StringVar()
        self.n = tk.Entry(self,width=25,textvariable=self.nEntry)
        self.createLabel(tk, self.n, "Number of iteration", 1, 4, 25)
        self.rowconfigure(21, minsize=20)

        # parachute failure
        self.parachuteFailure = tk.StringVar()
        self.parachute= tk.Entry(self,width=25, textvariable=self.parachuteFailure)
        self.createLabel(tk, self.parachute, "Number of Parachute Failures", 1, 7, 0)
        
        # n
        self.motorPerformanceEntry = tk.StringVar()
        self.motorPerformance = tk.Entry(self,width=25,textvariable=self.motorPerformanceEntry)
        self.createLabel(tk, self.motorPerformance, "Motor performance variation", 1, 10, 0.1)

        # Upwind rocket vector only fields
        tk.Label(self, text = "Upwind Vector").grid(column = 2, row = 1)
        tk.Label(self, text = "Calculation Parameters").grid(column = 2, row = 2)
        self.upwindMinAngleEntry = tk.StringVar()
        self.upwindMinAngle = tk.Entry(self,width=25,textvariable=self.upwindMinAngleEntry)
        self.createLabel(tk, self.upwindMinAngle, "Upwind Min Angle", 2, 4, -15)

        self.upwindMaxAngleEntry = tk.StringVar()
        self.upwindMaxAngle = tk.Entry(self,width=25,textvariable=self.upwindMaxAngleEntry)
        self.createLabel(tk, self.upwindMaxAngle, "Upwind Max Angle", 2, 7, 15)

        self.upwindStepSizeEntry = tk.StringVar()
        self.upwindStepSize = tk.Entry(self,width=25,textvariable=self.upwindStepSizeEntry)
        self.createLabel(tk, self.upwindStepSize, "Upwind Step Size", 2, 10, 2)
        
        # load weather
        self.rowconfigure(24, minsize=15)
        tk.Button(self, text='Load data from csv', width=25, command=self.getWeather, padx=0).grid(column=1, row=0)
        tk.Button(self, text='Execute Monte Carlo', width=25, command=self.exec,padx=0).grid(column=0, row=26, columnspan = 2)
        tk.Button(self, text='Calculate Upwind Vector', width=25, command=self.upwindCalc ,padx=0).grid(column=2, row=26)

    def createLabel(self, tk, var, name, colNum, rowNum, insertValue):
        var.insert(0,insertValue)
        tk.Label(self, text = name).grid(column = colNum, row = rowNum)
        var.grid(column = colNum, row = rowNum+1)

    def getFile(self):
        self.filename = tk.filedialog.askopenfilename(initialdir = "./", title = "Select file", filetypes = [("Rocket File","*.ork")])
        if type(self.filename) is tuple :
            self.filename = "model.ork"
    
    def saveFile(self):
        self.outfile = tk.filedialog.asksaveasfilename(initialdir = "./",initialfile="out.csv", title = "Select file",filetypes = [("CSV","*.csv")], defaultextension = ".csv")
        if type(self.outfile) is tuple :
            self.outfile = "./out.csv"

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

    def upwindCalc(self):
        self.updateArgs()
        self.updateUpwindArgs()
        self.runUpwindArgs(self.upwindSim)

    def updateUpwindArgs(self):
        self.upwindArgs = Namespace(upwindMinAngle = -25, upwindMaxAngle = 25, upwindStepSize = 2)
        
        values = Namespace(upwindMinAngle = self.upwindMinAngle.get(), upwindMaxAngle = self.upwindMaxAngle.get(), upwindStepSize = self.upwindStepSize.get())
        if(self.checkUpwindValues(values)):
            self.parseAndRunUpwind(values)

    def checkUpwindValues(self, values):
        self.upwindNames = Namespace(upwindMinAngle='Upwind Min Angle', upwindMaxAngle='Upwind Max Angle', upwindStepSize='Upwind Step Size')

        for k in values.__dict__:
            if values.__dict__[k] != '':                
                if not (self.checkFloatValue(values.__dict__[k])):
                    showinfo("Invalid Input", "Incorrect input: "+ self.upwindNames.__dict__[k] + " needs to be a float value")
                    return False
        return True

    def parseAndRunUpwind(self, values):
        self.upwindArgs = Namespace(upwindMinAngle = -25, upwindMaxAngle = 25, upwindStepSize = 2)

        for k in self.upwindArgs.__dict__:
            if values.__dict__[k] != '':                
                self.upwindArgs.__dict__[k] = float(values.__dict__[k])
        
        self.upwindSim = upwind_rocket_vectors.UpwindRocketVectors()
        self.upwindSim.set_args(self.args, self.upwindArgs)

    def runUpwindArgs(self,sim):
        self.showUpwindCalculating()
        self.upwindSim.run_analysis()
        self.controller.upwindResults = Namespace(bestAngle = self.upwindSim.get_bestAngle(), bestDistance = self.upwindSim.get_bestDistance())
        self.showUpwindResults()

    def exec(self):
        if(self.updateArgs()):
            self.runSims(self.sim)

    def updateArgs(self):
        self.args = Namespace(rocket='model.ork', outfile='./out.csv', rodAngle=45, rodAngleSigma=5, 
                        rodDirection=0, rodDirectionSigma=5,
                        windSpeed=15,windSpeedSigma=5, 
                        startLat=0,startLong=0, simCount=25, windDirection=0, motorPerformance = 0.1, parachute = 0)
        
        values = Namespace(rocket=self.filename, outfile=self.outfile, rodAngle=self.rodAngle.get(), rodAngleSigma=self.rodAngleSigma.get(), 
                    rodDirection=self.rodDirection.get(), rodDirectionSigma=self.rodDirectionSigma.get(),
                    windSpeed=self.windSpeed.get(),windSpeedSigma=self.windSpeedSigma.get(), 
                    startLat=self.lat.get(),startLong=self.longa.get(), simCount=self.n.get(), windDirection=self.windDirection.get(), motorPerformance = self.motorPerformance.get(), parachute = self.parachute.get())

        if(self.checkValues(values)):
            self.parseAndRun(values)
            return True
        return False

    def checkValues(self, values):

        self.names = Namespace(rocket='filename', outfile='outfile', rodAngle='Rod angle', rodAngleSigma='Rod angle sigma', 
                    rodDirection='Rod direction', rodDirectionSigma='Rod direction sigma', windSpeed='Wind speed',windSpeedSigma='Wind speed sigma', 
                    startLat='lat',startLong='long', simCount='Number of iteration', windDirection='Wind direction', motorPerformance = 'Motor performance variation',
                    parachute = 'Number of Parachute Failures')

        for k in values.__dict__:
            if values.__dict__[k] != '':                
                if k == 'rocket' or k == 'outfile':
                    pass # is string
                elif k == 'simCount':
                    if not (self.checkIntValue(values.__dict__[k])):
                        showinfo("Invalid Input", "Incorrect input: "+ self.names.__dict__[k] + " needs to be an integer value")
                        return False
                else:
                    if not (self.checkFloatValue(values.__dict__[k])):
                        showinfo("Invalid Input", "Incorrect input: "+ self.names.__dict__[k] + " needs to be a float value")
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
                        startLat=0,startLong=0, simCount=25, windDirection=0, motorPerformance = 0.1, parachute = 0)

        for k in args.__dict__:
            if values.__dict__[k] != '':                
                if k == 'rocket' or k == 'outfile':
                    self.args.__dict__[k] = values.__dict__[k]
                elif k == 'simCount':
                    self.args.__dict__[k] = int(values.__dict__[k])
                else:
                    self.args.__dict__[k] = float(values.__dict__[k])
        
        self.sim = simulation.Simulation()
        self.sim.set_args(self.args)

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

    def showUpwindResults(self):
        self.destroy()
        resultFrame = UpwindResults(self.parent, self.controller)
        resultFrame.grid(row = 0, column = 0, sticky = "nsew")
        resultFrame.displayResults()
        resultFrame.update_idletasks() 

    def showUpwindCalculating(self):
        self.destroy()
        loadingFrame = UpwindVector(self.parent, self.controller)
        loadingFrame.grid(row = 0, column = 0, sticky = "nsew")
        loadingFrame.stepProgressBar()
        loadingFrame.update()

    def showLoading(self):
        self.destroy()
        loadingFrame = RunningSimulations(self.parent, self.controller)
        loadingFrame.grid(row = 0, column = 0, sticky = "nsew")
        loadingFrame.stepProgressBar()
        loadingFrame.update()

class UpwindVector(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text = "Calculating Upwind Vector").grid(column = 0, row = 0)
        self.controller = controller

        self.progressBar = ttk.Progressbar(self,orient='horizontal', mode='indeterminate')
        self.progressBar.grid(column=0, row=1)    
        self.stepProgressBar()    

    def stepProgressBar(self):
        self.progressBar.step(5)


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

class UpwindResults(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text = "Upwind Results").grid(column = 0, row = 0)
        self.controller = controller

    def displayResults(self):
        count = 1
        for k in list(vars(self.controller.upwindResults).keys()):
            tk.Label(self, text = k).grid(column = 0, row = count)
            tk.Label(self, text=getattr(self.controller.upwindResults, k)).grid(column = 1, row = count)
            count = count + 1

if __name__ == "__main__":
    app = MonteCarloApp()
    app.mainloop()