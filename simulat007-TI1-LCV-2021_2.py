import numpy as np
from nmrsim import Multiplet
from nmrsim.plt import mplplot
import matplotlib.pyplot as plt 

# J: cte acoplamiento (Hz), v: frecuencia central (Hz), r: vecinos, i: integracion

class Simulat:
    """
    def __init__(self, J, v, r, i):
        self.J = J
        self.v = v 
        self.r = r
        self.i = i 
    """
    def Grafica (self, points, w, J, v, r, i):
        self.points = points
        self.linewidth = w
        self.td = Multiplet(v, i, [(J, r)])
        self.grafica = mplplot(self.td.peaklist(), points , w) #w es ancho de señal
        

    def GraficBonita (self):
        plt.plot(self.grafica[0], self.grafica[1])
        plt.xlim(1100,1300)
        #plt.ylim(0, 0.055)
        plt.xlabel("Frecuencia (Hz)")
        plt.show()
"""
    def ArchivoTxt (self): 
        intensidades = (grafica[1]) * 10000
        no_datos = len(grafica[1])
        intensidades1 = [] 
"""
simulacion1 = Simulat()
simulacion1.Grafica(1000,5,7.1,1200.0,1,1)
simulacion1.GraficBonita() 

td = Multiplet(1200.0, 1, [(7.1, 1)])
print(td.v)
print(td.I)
print(td.J)

grafica = mplplot(td.peaklist(), points = 1000, w= 5) #w es ancho de señal