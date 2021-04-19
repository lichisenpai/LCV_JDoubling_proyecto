"""
Recorte de codigo para acciones no necesarias en este caso 
Cambios:
1. reduccion de las lineas 128 a 133 (impresion de grafica de los datos)
2. reduccion de las lineas 133 a 143 (eliminacion de regiones sin ajuste de linea)
3. reduccion de las lineas 145 a 162 (correcion de linea base)
"""

import numpy as np
from nmrsim import Multiplet
from nmrsim.plt import mplplot
import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy.signal import argrelextrema

# 1200 Hz, 2H, td, J= 7.1, 1.1 Hz
td = Multiplet(1200.0, 1, [(7, 1)])
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

iz = 0
de = len(intensidades) - 1

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
integrs = integrar(yy, intervalo, m)

plt.figure(figsize=(20,10))
plt.plot(integrs, marker = 'o')
plt.show()

minimos = argrelextrema(integrs, np.less)[0]

print(f"valores minimos en: {minimos}")
print("Mínimo: ", integrs[19])

Jota = minimos[-1] * paso_hz

#Seleccionar el mínimo deseado para que se determine la J.¶
print(f"Jota: {Jota}         Resolución Digital: {paso_hz}")
