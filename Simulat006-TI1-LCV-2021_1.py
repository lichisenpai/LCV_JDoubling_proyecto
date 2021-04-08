import numpy as np
from nmrsim import Multiplet
from nmrsim.plt import mplplot
import matplotlib.pyplot as plt 


# 1200 Hz, 2H, td, J= 7.1, 1.1 Hz
td = Multiplet(1200.0, 1, [(7.1, 1)])
print(td.v)
print(td.I)
print(td.J)

grafica = mplplot(td.peaklist(), points = 1000, w= 5) #w es ancho de señal

#para cuando quiero recuperar la imagen del multiplete
plt.plot(grafica[0], grafica[1])
plt.xlabel("Frecuencia (Hz)")
plt.show()

#para crear el archivo de texto
intensidades = (grafica[1]) * 10000
no_datos = len(grafica[1])
intensidades1 = []

for i in range (len(intensidades)):
    intensidades1.append(round(intensidades[i], 6))

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
#f.write(str(lista1))
for i in range (len(intensidades1)):
    f.write(str(intensidades1[i])+"\n")
f.close()
