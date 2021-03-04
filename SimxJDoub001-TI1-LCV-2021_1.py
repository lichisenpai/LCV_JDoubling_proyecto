"""
Este es el intento crudo de conjuncion de la simulacion con nmrsim con el copy paste 
del programa J Doubling de Federico del Rio 
"""

import numpy as np
from nmrsim import Multiplet
from nmrsim.plt import mplplot
import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy.signal import argrelextrema

# 1200 Hz, 2H, td, J= 7.1, 1.1 Hz
td = Multiplet(1200.0, 1, [(7.1, 1)])
print(td.v)
print(td.I)
print(td.J)

grafica = mplplot(td.peaklist())

#para cuando quiero recuperar la imagen del multiplete
plt.plot(grafica[0], grafica[1])
plt.xlabel("Frecuencia (Hz)")
plt.ylim(0,1)
plt.show()

#para crear el archivo de texto
intensidades = (grafica[1]) * 10000
no_datos = len(grafica[1])
intensidades1 = []

for i in range (len(intensidades)):
    intensidades1.append(round(intensidades[i], 8))

Hz = (grafica[0])
min_Hz = (Hz[0])
max_Hz = (Hz[799])

oracion1 = f"Number of data points      : {no_datos} \n"
oracion2 = f"Chemical shift range (ppm) : 1 1\n"
oracion3 = f"Chemical shift range (Hz)  : {min_Hz} {max_Hz}\n"

#escritura del archivo para guardar los datos
f = open('multiplete7.slc','w')
f.write(oracion1)
f.write(oracion2)
f.write(oracion3)
#f.write(str(lista1))
for i in range (len(intensidades1)):
    f.write(str(intensidades1[i])+"\n")
f.close()

#Intento de programa conjunto (JDoubling del profe)

# abrimos el archivo y obtenemos las columnas que nos itneresan
# Se baso en la siguiente pagina web: https://realpython.com/python-csv/


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
            yy[i] = int(float(contenido[i+3]))
            
    else:
        print("No existe el archivo")
    
    return [yy, float(a), float(b)]


def aplicar(x, y, m):
    # El tama;o de x tiene que ser del tama;o de y mas m
    #x y y son arreglos
    x_new = np.copy(x)
    for i in range(0, len(y)):
        x_new[m+i] += y[i]
    return x_new


def convolucion(yy, n = 40, m = 128): #que n va de 1 hasta 64
    tamano = len(yy)
    ceros = np.zeros(tamano+n*m)

    for i in range(0, m):
        ceros = aplicar(ceros, (-1)**i*yy, n*i)
    return ceros


#Input: yy
def integrar(yy, intervalo = 60, m = 8):
    #intervalo es el maximo valor de las n
    
    integrs = np.zeros(intervalo)
    
    for i in range(1, intervalo):
        y_new = convolucion(yy, i, m)
        integral = sum(abs(y_new))
        integrs[i] = integral
    return integrs

#Generando un vector con la se;al trasladada 1 vez
def trasladar(ys, n):
    # delta = xs[n]
    tam = len(ys) + n
    y_new = np.zeros(tam)
    
    for i in range( 0, tam ):
        if i < len(ys):
            y_new[i] += ys[i]
        if i >= n:
            y_new[i] += -ys[i-n]
    return y_new    


yy, a, b = leer_archivo('multiplete7.slc')
# Con escala en enteros
plt.figure(figsize=(20,10))
plt.plot(yy, color = "red")
#plt.plot([iz, de], [yy[iz], yy[de]])
plt.show()
print(len(yy))

print(list(yy).index(min(yy)))
#Eliminación de regiones sin ajuste de línea base
iz = 0
de = 799
if de > len(yy):
    de = len(yy) - 1
pendiente = (yy[de]-yy[iz])/(de-iz)
ordenada_o = pendiente*iz - yy[iz]
plt.figure(figsize=(20,10))
plt.plot(yy)
plt.plot([iz, de], [yy[iz], yy[de]])

#Reducción de ventana y corrección de línea base"]
pendiente = (yy[de]-yy[iz])/(de-iz)
ordenada_o = pendiente*iz - yy[iz]

print(pendiente,ordenada_o, yy[de],yy[iz],de,iz)

y = np.zeros(de-iz-1)
for i in range(0, de-iz-1):
    y[i] = yy[iz+i] - (pendiente*i-ordenada_o)

print("Minimo: ", min(y))
y = y - min(y)
plt.figure(figsize=(20,10))
plt.plot(yy[iz:de], color = "red")
plt.plot(yy, color = "blue")
plt.plot(y, color = "green")
plt.show()
#print(y)

# Generar la secuencia xx
paso_hz = abs(a-b)/len(yy)
xx = [i*paso_hz+min([a, b]) for i in range(0, len(yy))]

#Redefiniendo el arreglo en y
yy = yy[iz:de]
xx = xx[iz:de]
nuevo_paso_hz = (xx[-1]-xx[0])/len(yy)

# La escala en X de la siguiente figura está en enteros. Utilizar paso_Hz para convertir a Hz
intervalo = 80
m = 256
integrs = integrar(y, intervalo, m)

plt.figure(figsize=(20,10))
plt.plot(integrs, marker = 'o')
plt.show()

print("valores minimos en: "+str(argrelextrema(integrs, np.less)[0]))
print("Mínimo: ", integrs[19])

#Seleccionar el mínimo deseado para que se determine la J.¶
print("Jota: ",  53*paso_hz, "        Resolución Digital", paso_hz,)
