import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import random
import threading

X = []
d = [] #arreglo de deseados



def Perceptron():
    global W1, W2, Theta, Eta, Epocas_str, X, d
    Epocas = int(Epocas_str.get())
    error = True
    while Epocas and error:
        e = [] #arreglo de errores 
        for i in range(len(X)):
            Y = np.dot(X[i],[W1,W2]) - Theta >=0
            e.append(d[i]-Y)
            W1 = W1 + (float(Eta.get())*e[-1]*X[i][0])
            W2 = W2 + (float(Eta.get())*e[-1]*X[i][1])
            Theta = Theta - (float(Eta.get())*e[-1]*1)
        
        W = [W1,W2]

        #Generamos los valores para la funcion de la recta 
        m = -W[0]/W[1] #pendiente 
        b = Theta/W[1] #altura en la que se coloca el punto 

        ax.cla()

        #Imprimir plano cartesiano    
        ejeX = [-10,10] #marcar las rectas del plano cartesiano 
        ejeY = [-10,10]
        ceros = [0,0] 
        plt.plot(ejeX, ceros, 'c') #se grafica una linea en el eje x
        plt.plot(ceros, ejeY, 'c') #se grafica una linea en el eje y

        #Recorrer la matriz y graficar los puntos correspondientes 
        for i in range(len(X)):
            if X[i][0]*W[0] + X[i][1]*W[1] - Theta >=0: #Si es mayor o igual a cero pasa 
                plt.plot(X[i][0],X[i][1],'Dg')
            else:
                plt.plot(X[i][0],X[i][1],'Dr')
        plt.axline((X[0][0], (X[0][0]*m)+b), slope=m, color='b') #Dibujar la recta 

        plt.xlim(-10,10)
        plt.ylim(-10,10)

        canvas.draw()
        W1_label.config(text = "Valor de W1: {:.2f}".format(W1))
        W2_label.config(text = "Valor de W2: {:.2f}".format(W2))
        Theta_label.config(text = "Valor de Theta: {:.2f}".format(Theta))

        if not(1 in e) and not(-1 in e):
            error = False

        Epocas = Epocas - 1

#Inicializar la grafica con mathplotlib
fig, ax = plt.subplots(facecolor='#88ECF6')
plt.xlim(-10,10)
plt.ylim(-10,10)

#Imprimir plano cartesiano    
ejeX = [-10,10] #marcar las rectas del plano cartesiano 
ejeY = [-10,10]
ceros = [0,0] 
plt.plot(ejeX, ceros, 'c') #se grafica una linea en el eje x
plt.plot(ceros, ejeY, 'c') #se grafica una linea en el eje y

#Ingresar los archivos 
archivo_x = input("Escribir el nombre del archivo X: ")
archivo_d = input("Escribir el nombre del archivo D: ")


#Abrir el archivo de texto
with open(archivo_d) as f:
    lineas = f.readlines()

for line in lineas:
    d.append(int(line))

#Abrir el archivo de texto
with open(archivo_x) as f:
    lineas = f.readlines()

#Llenar la matriz X con los valores del archivo de texto
for i in range(len(lineas)):
    vector = lineas[i].split('/') #Funciones de python para trabajar cadenas 
    vector[0] = float(vector[0])
    vector[1] = float(vector[1])
    if d[i]:
        ax.plot(vector[0],vector[1],'Dg')
    else:
        ax.plot(vector[0],vector[1],'Dr')
    X.append(vector)

#Interfaz Grafica 
mainwindow = Tk()
mainwindow.geometry('750x600')
mainwindow.wm_title('Perceptron')

#Valores de los pesos
W1 = random.random()
W2 = random.random()
Theta = random.random()
Eta = StringVar(mainwindow)
Epocas_str = StringVar(mainwindow)

#Grafica en la interfaz 
canvas = FigureCanvasTkAgg(fig, master = mainwindow)
canvas.get_tk_widget().place(x=10, y=10, width=580, height=580) 


#Etiquetas
W1_label = Label(mainwindow, text = "Valor de W1: {:.2f}".format(W1))
W1_label.place(x=600, y=20) 

W2_label = Label(mainwindow, text = "Valor de W2: {:.2f}".format(W2))
W2_label.place(x=600, y=50) 

Theta_label = Label(mainwindow, text = "Valor de Theta: {:.2f}".format(Theta))
Theta_label.place(x=600, y=80) 

Eta_label = Label(mainwindow, text = "Valor de Eta: ")
Eta_label.place(x=600, y=110) 
Eta_entry = Entry(mainwindow, textvariable=Eta)
Eta_entry.place(x=600, y=140) 

Epocas_label = Label(mainwindow, text = "Epocas: ")
Epocas_label.place(x=600, y=160) 
Epocas_entry = Entry(mainwindow, textvariable=Epocas_str)
Epocas_entry.place(x=600, y=190) 


#button
start_button = Button(mainwindow, text="Graficar", command=lambda:threading.Thread(target=Perceptron).start())
start_button.place(x=600, y=230)

mainwindow.mainloop()


