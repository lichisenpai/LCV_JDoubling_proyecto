import tensorflow as tf
import leerarchivos
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import numpy as np


class Jdoubling:
    def __init__(self, nombre):
        self.yy, self.a, self.b = leerarchivos.leer_archivo(nombre)
        self.paso_hz = abs(self.a-self.b)/len(self.yy)
        self.xx = [i*self.paso_hz+min([self.a, self.b]) for i in range(0, len(self.yy))]
    
     
    def imprimir (self):
        plt.plot(self.yy)
        plt.show()
        print(self.a, self.b)
        return 

    
    def det_with (self):
        self.w, self.r1, self.r2 = leerarchivos.det_width(self.xx, self.yy)
        return self.w, self.r1, self.r2
    
    def S_Nratio(self):
        onlynoise = leerarchivos.exp_noise(self.xx, self.yy, self.r1, self.r2)
        mse, rmse, s_n = leerarchivos.Noise(self.yy, onlynoise)
        return mse, rmse, s_n
    

    def aplicar (self, x, y, m):
        return leerarchivos.aplicar(x, y, m)


    def integrar (self, intervalo=60, m=8):
        return leerarchivos.integrar(self.yy, intervalo, m)
    
    def trasladar (self, ys, n):
        return leerarchivos.trasladar(ys, n)
    
    def Armonics (self, x, integ):
        return leerarchivos.Armonics(x, integ)


class Running_JDoub(Jdoubling):
    """def __init__(self):
        super().__init__()"""
    
    def GraficaIntegral (self):
        self.intervalo = int(len(self.yy)/4)
        m = 164
        self.integral = super().integrar(self.intervalo, m)
        plt.plot(self.integral, marker = 'o')
        plt.xlabel("no. de punto * resolución digital (Hz)")
        plt.show()
    
    def SerchingMinima (self):
        busqueda = int(self.intervalo/7)
        minimosR = argrelextrema(self.integral, np.less, order=busqueda, mode= 'wrap')[0]#busca el minimo mas minimo
        minimos = argrelextrema(self.integral, np.less, mode='wrap')[0] #me da todos los minimos con ruido

        print(f"valores minimos (+ ruido) en: {minimosR}")
        print(f"resolucion digital: {self.paso_hz} Hz")
        armonic1 = int((minimosR[-1])/3)

        subarmos= super().Armonics(armonic1, minimos)

        Jota = minimosR[-1] * self.paso_hz

        distance = Jota - (subarmos * self.paso_hz)

        print(f"Constante de acoplamiento: {Jota} Hz")
        return Jota, distance, subarmos
    
    def ExperimentalWidth (self):
        w, r1, r2 = super().det_with()
        return w, r1, r2
    
    def ExperimentalNoise (self):
        #only_noise = super().only_noise()
        mse, rmse, s_n = super().S_Nratio()
        return mse, rmse, s_n


#prueba= Jdoubling("ha_06.slc")

nose = Running_JDoub("ha_06.slc")
grafica = nose.GraficaIntegral()
J, dist, sub = nose.SerchingMinima()
ancho = nose.ExperimentalWidth()
mse, rmse, s_n = nose.ExperimentalNoise()

#print(type(tupla))
