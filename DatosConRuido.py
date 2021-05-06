import numpy as np
from nmrsim import Multiplet
from nmrsim.plt import mplplot
import pandas as pd
import matplotlib.pyplot as plt


#Para leer el Json con ruido
def ReadJsonNoise (x, c):
    prueba = pd.read_json(x)
    Y = prueba['Random']#para tenerlo como array
    Rvalue = np.random.choice(Y, 1000)#wlige 1000 puntos al azar, y 1000 por que es el valor de puntos que yo meti por default a mi simulacion
    Norm = list(map(lambda w: w / c, Rvalue))#El c es el valor que divide los valores random de ruido, entre mayor el no. se ve menis el ruido
    return Norm

#Aqui genero los "estadisticos" para medir el ruido 
def Noise (a, b):
    original = a
    noise = b 
    mse = (np.square(original - noise)).mean() #aqui nos dice cuanto "ruido" hay en promedio al cuadrado
    rmse = pow(mse, 0.5) #la raiz cuadrada del anterior
    maxim = max(original)# nos da el maximo de la simulacion original
    s_n = maxim / rmse #relacion señal ruido
    print("El mse es: ", mse)
    print("El rmse es: ", rmse)
    print("El maximo es: ", maxim)
    print("La relación señal ruido es: ", s_n)
    return mse, rmse, s_n

def multiplet (v, I, J, r):
    #La simulacion tan famosa que ya conoces
    td = Multiplet(v , I, [(J, r)]) 
    grafica = mplplot(td.peaklist(), points=1000, w=0.5, limits=[])
    return grafica 

#la ya conocida funcion de archivo de texto
def archiv_txt (X, Y):
    #Datos en Y
    intensidades = Y
    no_datos = len(intensidades)
    intensidades1 = []
    for i in range (len(intensidades)):
        intensidades1.append(round(intensidades[i], 6))

    #Datos en x 
    Hz = X
    min_Hz = (Hz[0])
    max_Hz = (Hz[no_datos - 1])

    oracion1 = f"Number of data points      : {no_datos} \n"
    oracion2 = f"Chemical shift range (ppm) : 1 1\n"
    oracion3 = f"Chemical shift range (Hz)  : {min_Hz} {max_Hz}\n"

    #escritura del archivo para guardar los datos
    f = open('Prueba.slc','w')
    f.write(oracion1)
    f.write(oracion2)
    f.write(oracion3)
    
    for i in range (len(intensidades1)):
        f.write(str(intensidades1[i])+"\n")
    
    f.close()


ruido = ReadJsonNoise("RandomNoise.json", 50) #lee el Json y el segundo argumento es para dividir el ruido y se haga menos notorio en grafica
multiplete = multiplet(1200.0, 1, 1.0, 1) #aqui me genera el grafico de la señal SIN el ruido

intensidades = multiplete[1] #los valores en Y de la señal SIN el ruido
desplazamiento = multiplete[0] #los valores en x (Hz) de la señal SIN el ruido

señalCruido = ruido + intensidades #los valores de Y ya con el ruido

mse, rmse, s_n = Noise(intensidades, ruido) #aqui me genera los estadisticos para conocer la relacion señal/ruido

#Grafica 
plt.plot(desplazamiento, señalCruido)
plt.title(f"Relacion señal ruido: {s_n}")
plt.xlabel("Desplazamiento (Hz)")
plt.ylabel("Intensidades")
plt.show()

archiv_txt(desplazamiento, señalCruido) #me genera el ya famoso archivo de texto que lee JDoubling


