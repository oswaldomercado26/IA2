import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import random
import threading

X = []
d = [] #arreglo de deseados
W_oculta = []
W_salida = []


def FuncionActivacion (W,X, funcion_evaluar):
    global  a
    v = np.dot(W,X)

    if funcion_evaluar == 0:
        #logistica
        F_u = 1/(1+np.exp(-(float(a.get()))*v))

    elif funcion_evaluar == 1:
        #Tangente hiperbolica
        F_u = float(a.get())*(np.tanh(v))
        
    elif funcion_evaluar == 2:
        #Lineal
        F_u = 0.5*v

    return F_u


def FuncionDerivacion(Y, funcion_evaluar):
    global  a

    if funcion_evaluar == 0:
        #Logistica
        F_u = float(a.get())*Y*(1-Y)

    elif funcion_evaluar == 1:
        #Tangente hiperbolica
        F_u = float(a.get())*(1-(Y**2))
    
    elif funcion_evaluar == 2:
        #Lineal
        F_u = 0.5

    return F_u


def Clasificacion():
    global  eta_interfaz, Epocas_str, X, d, W_oculta, W_salida, funcion_evaluar
    eta = float(eta_interfaz.get())

    W_oculta = np.random.rand(2,2)
    W_salida = np.random.rand(3)
    print(W_oculta, W_salida)
    Epocas = int(Epocas_str.get())
    error = True
    error_grafico = []
    funcion = funcion_evaluar.get()
    linear = 2

    x_completa = X
    d_completa = d
    X, d = seleccionar_datos_entrenamiento(X, d)


    while Epocas and error:
        error = False 
        errores_matrices = []

        salida_oculta = FuncionActivacion(X, np.transpose(W_oculta), funcion)
        X_oculta = np.c_[np.ones(len(salida_oculta)),salida_oculta]
        salida = FuncionActivacion(X_oculta, np.array(W_salida).flatten(), linear)
        errores = d - salida 

        #Capa de salida 
        delta_salida = []
        for i in range(len(X_oculta)):
            salida_derivada = FuncionDerivacion(np.array(salida).flatten()[i], linear)
            delta_salida.append(salida_derivada*np.array(errores).flatten()[i])
            W_salida = W_salida + np.dot(X_oculta[i],eta*delta_salida[-1])

        #Capa oculta
        for i in range(len(X)):
            for j in range(len(W_oculta)):
                salida_derivada = FuncionDerivacion(salida_oculta[i,j], funcion)
                delta_oculta = np.array(W_salida).flatten()[j+1]*np.array(delta_salida).flatten()[i]*salida_derivada
                W_oculta[j] = W_oculta[j] + np.dot(X[i],eta*delta_oculta)

        square_error = np.average(np.power(errores,2))
        if square_error > float(error_minimo.get()):
            error = True
        error_grafico.append(square_error)

        #Imprimimos los puntos de la grafica 
        salida_oculta = FuncionActivacion(x_completa, np.transpose(W_oculta), funcion)
        X_oculta = np.c_[np.ones(len(salida_oculta)),salida_oculta]
        salida = FuncionActivacion(X_oculta, np.array(W_salida).flatten(), linear)

        ax.cla()

        ax.plot(np.array(x_completa[:,1]),d_completa, 'o', color="black")
        ax.plot(np.array(X[:,1]),np.array(d).flatten(), 'o', color="green")
        ax.plot(np.array(x_completa[:,1]),np.array(salida).flatten(), '--',color="red")

        ax_error.cla()
        ax_error.plot(error_grafico)

        canvas.draw()
        canvas_error.draw()
        
        Epocas = Epocas - 1
        print(square_error)

#Inicializar la grafica con mathplotlib
fig, ax = plt.subplots(facecolor='#88ECF6')
plt.xlim(-2,2)
plt.ylim(-2,2)
fig_error, ax_error = plt.subplots(facecolor='#88ECF6')


#Ingresar los archivos 
archivo_d = input("Escribir el nombre del archivo D: ")
archivo_x = input("Escribir el nombre del archivo X: ")

#Abrir el archivo de texto
with open(archivo_d) as f:
    lineas = f.readlines()

for i in range(len(lineas)):
    d.append(float(lineas[i]))
d = np.array(d)

def seleccionar_datos_entrenamiento(x_completa, d_completa):
    i = 0
    x_train = []
    d_train = []
    while i < len(x_completa):
        x_train.append([x_completa[i,0],x_completa[i,1]])
        d_train.append(d_completa[i])
        i+=5
    x_train = np.matrix(x_train)
    d_train = np.array(d_train)
    return x_train, d_train


#Abrir el archivo de texto
with open(archivo_x) as f:
    lineas = f.readlines()

#Llenar la matriz X con los valores del archivo de texto
for i in range(len(lineas)):
    X.append([1, float(lineas[i])])
X = np.matrix(X)

for i in range(1,len(X)):
    for j in range(0,len(X)-i):
        if(X[j+1,1] < X[j,1]):
            aux=X[j,1]
            X[j,1]=X[j+1,1]
            X[j+1,1]=aux
            aux=d[j]
            d[j]=d[j+1]
            d[j+1]=aux

ax.plot(np.array(X[:,1]),d, 'o', color="black")

#Interfaz Grafica 
mainwindow = Tk()
mainwindow.geometry('1200x600')
mainwindow.wm_title('Red Neuronal Multicapa')

#Valores de los pesos
eta_interfaz = StringVar(mainwindow)
Epocas_str = StringVar(mainwindow)
funcion_evaluar = IntVar(mainwindow)
error_minimo = StringVar(mainwindow)
a = StringVar(mainwindow)

#Grafica en la interfaz 
canvas = FigureCanvasTkAgg(fig, master = mainwindow)
canvas.get_tk_widget().place(x=10, y=10, width=580, height=580) 

#Grafica del error
canvas_error = FigureCanvasTkAgg(fig_error, master = mainwindow)
canvas_error.get_tk_widget().place(x=750, y=30, width=400, height=300) 


#Etiquetas
a_label = Label(mainwindow, text = "A: ")
a_label.place(x=600, y=40) 
a_entry = Entry(mainwindow, textvariable=a)
a_entry.place(x=600, y=70) 

Eta_label = Label(mainwindow, text = "Valor de Eta: ")
Eta_label.place(x=600, y=100) 
Eta_entry = Entry(mainwindow, textvariable=eta_interfaz)
Eta_entry.place(x=600, y=130) 

Epocas_label = Label(mainwindow, text = "Epocas: ")
Epocas_label.place(x=600, y=160) 
Epocas_entry = Entry(mainwindow, textvariable=Epocas_str)
Epocas_entry.place(x=600, y=190) 

Error_label = Label(mainwindow, text = "Error Minimo: ")
Error_label.place(x=600, y=220) 
Error_entry = Entry(mainwindow, textvariable=error_minimo)
Error_entry.place(x=600, y=250) 

#button
logistica_rb = Radiobutton(mainwindow, text="Logistica", variable=funcion_evaluar, value=0)
logistica_rb.place(x=600, y=280)

tangente_rb = Radiobutton(mainwindow, text="Tangente", variable=funcion_evaluar, value=1)
tangente_rb.place(x=600, y=310)

Lineal_rb = Radiobutton(mainwindow, text="Lineal", variable=funcion_evaluar, value=2)
Lineal_rb.place(x=600, y=340)


#button
start_button = Button(mainwindow, text="Graficar", command=lambda:threading.Thread(target=Clasificacion).start())
start_button.place(x=600, y=370)

mainwindow.mainloop()


