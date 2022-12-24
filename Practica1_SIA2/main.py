from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from tkinter import *
from tkinter.ttk import *

class Window:
    
    def __init__(self, window):
        style = Style()
        style.configure('W.TButton', font =('Arial', 12, 'bold'),foreground = 'black')
        
        self.window = window
        self.window.title("Practica 1")
        self.window.geometry("750x450")

        self.X1 = []
        self.X2 = []
        self.umbral = 0
        self.campoX1 = None
        self.campoX2 = None
        self.Peso1 = None
        self.Peso2 = None
        self.LauncherUI()

    def LauncherUI(self):
        actionFrame = Frame(self.window)
        actionFrame.grid(row=0, column=1, padx=20, ipady=70)
        
        #Definimos la parte superior donde pedimos los datos
        upperFrame = Frame(actionFrame)
        # upperFrame.place(x=30, y= 5, width=300, height=50)
        upperFrame.grid(row=0, column=0, ipadx=10, ipady=20)
        
        Label(upperFrame, text="Peso 1 :", width=10,font =('Arial', 12, 'bold')).grid(row=0, column=0)
        self.Peso1 = Entry(upperFrame, width=8)
        self.Peso1.grid(row=0, column=1)

        Label(upperFrame, text="Peso 2 :", width=10,font =('Arial', 12, 'bold')).grid(row=1, column=0)
        self.Peso2 = Entry(upperFrame, width=8)
        self.Peso2.grid(row=1, column=1, pady=5)
        
        Label(upperFrame, text="Ɵ  :", width=10,font =('Arial', 12, 'bold')).grid(row=2, column=0)
        self.umbral = Entry(upperFrame, width=8)
        self.umbral.grid(row=2, column=1, pady=5)

        lowerFrame = Frame(actionFrame)
        lowerFrame.background = "#769cb5"
        lowerFrame.grid(row=1, column=0, ipadx=10)
        
        self.button = Button(lowerFrame,style = 'W.TButton', text="Iniciar",command=self.iniciar, width=20)
        self.button.grid(row=2, column=0, columnspan=2)
        self.graficar()

    def onClick(self, event: Event):
            self.X1.append(event.xdata)
            self.X2.append(event.ydata)
            self.graficar()

    def iniciar(self):
        w1 = float(self.Peso1.get())
        w2 = float(self.Peso2.get())
        u = float(self.umbral.get())
        m = -w1/w2
        a = u/w2

        figure = Figure(figsize=(5, 4), dpi=100)
        grafica = figure.add_subplot(111)
        grafica.grid(axis='both',linestyle='dotted', color='k')

        for i in range(len(self.X1)):
            y = ((m*self.X1[i])+a)
            y2 = ((m*self.X2[i])+a)
            grafica.plot([self.X1[i], self.X2[i]], [y, y2], color='black')
            
            punto = float(((self.X1[i]*w1)+(self.X2[i]*w2)) - u)

            if (punto <= 0):
                grafica.plot(self.X1[i], self.X2[i], 'bo')
            else:
                grafica.plot(self.X1[i], self.X2[i], 'ro')
        

        canvas = FigureCanvasTkAgg(figure, master=self.window)
        canvas.get_tk_widget().grid(row=0, column=2)
        grafica.set_xlim([-3, 3])
        grafica.set_ylim([-3, 3])

        cid = figure.canvas.mpl_connect('button_press_event', self.onClick)
        return None

    def graficar(self):
        figure = Figure(figsize=(5, 4), dpi=100)
        grafica = figure.add_subplot(111)
        grafica.grid(axis='both',linestyle='dotted', color='k')
        grafica.plot(self.X1, self.X2, 'ko')

        canvas = FigureCanvasTkAgg(figure, master=self.window)
        canvas.get_tk_widget().grid(row=0, column=2)

        grafica.set_xlim([-3, 3])
        grafica.set_ylim([-3, 3])
        cid = figure.canvas.mpl_connect('button_press_event', self.onClick)

window = Tk()
app = Window(window)
window.mainloop()