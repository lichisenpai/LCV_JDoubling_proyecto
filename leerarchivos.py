"""import numpy as np
import matplotlib.pyplot as plt


def leer_archivo(nombre):
    #Hay que analizar las primeras 3 renglones por separado.
    #a, b seran los extremos del intervalo en Hz
    
    arch = open(nombre, "r")
    if arch.mode == 'r':
        contenido = arch.read()
        contenido = contenido.split("\n")
        tam = int(contenido[0].split(": ")[1])
        [a, b] = contenido[2].split(": ")[1].split(" ")

        yy = np.zeros(tam)
        for i in range(0, tam):
            yy[i] = (float(contenido[i+3]))
            
    else:
        print("No existe el archivo")
    
    return [yy, float(a), float(b)]


yy, a, b = leer_archivo('ha_57_traslape.slc')

plt.plot(yy)
plt.show()"""

from nmrsim import Multiplet
from nmrsim.plt import mplplot
import numpy as np
from scipy.interpolate import UnivariateSpline
import pylab as pl

def multiplet (v, I, J, r):
    #La simulacion tan famosa que ya conoces
    min_x = v - 20 
    max_x = v + 20
    td = Multiplet(v , I, [(J, r)]) 
    grafica = mplplot(td.peaklist(), points=1000, w=0.5, limits=(min_x, max_x))
    return grafica 

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

def leer_archivo(nombre):
    #Hay que analizar las primeras 3 renglones por separado.
    #a, b seran los extremos del intervalo en Hz
    
    arch = open(nombre, "r")
    if arch.mode == 'r':
        contenido = arch.read()
        contenido = contenido.split("\n")
        tam = int(contenido[0].split(": ")[1])
        [a, b] = contenido[2].split(": ")[1].split(" ")

        yy = np.zeros(tam)
        for i in range(0, tam):
            yy[i] = (float(contenido[i+3]))
            
    else:
        print("No existe el archivo")
    
    return [yy, float(a), float(b)]

def det_width (xx, yy):

    # create a spline of the multiplet
    spline = UnivariateSpline(xx, yy-np.max(yy)/2, s=0)
    raices = spline.roots() # find the roots

    r1 = raices[0]
    r2 =raices[-1]

    pl.plot(xx, yy)
    pl.axvspan(r1, r2, facecolor='g', alpha=0.5)
    pl.show()

    print(r1, r2)
    
    w = r2-r1
    print(w)

    return w, r1, r2

def exp_noise (xx, r1, r2):

    subsetter = np.where((xx <= int(r2 + 2)) & (xx >= int(r1 - 2)))
    only_noise = np.delete(xx, subsetter)

    print(len(only_noise))

    return only_noise


señal = multiplet(1200, 1, 3.0, 1)
archiv_txt(señal[0], señal[1])

yy, a, b = leer_archivo('Prueba.slc')

# Generar la secuencia xx
paso_hz = abs(a-b)/len(yy)
xx = [i*paso_hz+min([a, b]) for i in range(0, len(yy))]


w, r1, r2 = det_width(xx, yy)

funciona = exp_noise(xx, r1, r2)