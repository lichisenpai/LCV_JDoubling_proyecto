import numpy as np
from nmrsim import Multiplet
from nmrsim.plt import mplplot
import numpy as np
import pandas as pd
import random 


#jotas = np.linspace(0.5, 12.0, 201)#el intervalo de trabajo de las J´s en las que quiero trabajar
#jotas = [0.7, 1.0, 12.0]

#calc = [] #lista para guardar la J que determina JDoubling

#Jota_0_5Hz = [] #lista donde guardar los datos para el json

#Para leer el Json con ruido
def ReadJsonNoise ():
    prueba = pd.read_json('RandomNoise.json')
    Y = prueba['Random']#values.reshape(-1, 1) #valor a predecir
    Rvalue = np.random.choice(Y, 1000)
    print (type(Rvalue))
    print(Rvalue)
    return Rvalue

#esta es la funcion que te digo que no sirve cuando la intento llamar dentro del bucle
def archiv_txt (v, I, J, r):

    td = Multiplet(v , I, [(J, r)]) 
    grafica = mplplot(td.peaklist(), points=1000)

    intensidades = (grafica[1])
    no_datos = len(grafica[1])
    intensidades1 = []
    for i in range (len(intensidades)):
        intensidades1.append(round(intensidades[i], 6))

    #Datos en x 
    Hz = (grafica[0])
    min_Hz = (Hz[0])
    max_Hz = (Hz[no_datos - 1])

    oracion1 = f"Number of data points      : {no_datos} \n"
    oracion2 = f"Chemical shift range (ppm) : 1 1\n"
    oracion3 = f"Chemical shift range (Hz)  : {min_Hz} {max_Hz}\n"

    #escritura del archivo para guardar los datos
    f = open('multiplete7.slc','w')
    f.write(oracion1)
    f.write(oracion2)
    f.write(oracion3)
    
    for i in range (len(intensidades1)):
        f.write(str(intensidades1[i])+"\n")
    
    f.close()

ReadJsonNoise()
