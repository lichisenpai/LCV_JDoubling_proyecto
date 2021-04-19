import numpy as np
from nmrsim import Multiplet
from nmrsim.plt import mplplot
import matplotlib.pyplot as plt 

# J: cte acoplamiento (Hz), v: frecuencia central (Hz), r: vecinos, I: integracion
def nmr_sim (v, I, J, r):
    td = Multiplet(v , I, [(J, r)]) 
    grafica = mplplot(td.peaklist(), points=1000)
    return grafica


def archiv_txt ():
    equis = nmr_sim(1200.0, 1, 7.0, 1) #para que me recupere los datos de la funcion nmr_sim
    intensidades = (equis[1])
    no_datos = len(equis[1])
    intensidades1 = []
    for i in range (len(intensidades)):
        intensidades1.append(round(intensidades[i], 6))

    #Datos en x 
    Hz = (equis[0])
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


archiv_txt()