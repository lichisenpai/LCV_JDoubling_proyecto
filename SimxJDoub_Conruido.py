import numpy as np
from nmrsim import Multiplet
from nmrsim.plt import mplplot
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from statistics import mean

def ReadJsonNoise (x, c):
    prueba = pd.read_json(x)
    Y = prueba['Random']#para tenerlo como array
    Rvalue = np.random.choice(Y, 1000)#wlige 1000 puntos al azar, y 1000 por que es el valor de puntos que yo meti por default a mi simulacion
    Norm = list(map(lambda w: w / c, Rvalue))#El c es el valor que divide los valores random de ruido, entre mayor el no. se ve menis el ruido
    return Norm


def Noise (a, b):
    original = a
    noise = b
    prom = sum(noise)/len(noise)
    msex = list(map(lambda x: np.square(x - prom), noise))
    mse = mean(msex)
    rmse = pow(mse, 0.5) #la raiz cuadrada del anterior
    maxim = max(original)# nos da el maximo de la simulacion original
    s_n = maxim / rmse #relacion señal ruido
    print("El mse es: ", mse)
    print("El rmse es: ", rmse)
    print("El maximo es: ", maxim)
    print("La relación señal ruido es: ", s_n)
    return mse, rmse, s_n


def multiplet (v, I, J, r, ww):
    #La simulacion tan famosa que ya conoces
    min_x = v - 20 
    max_x = v + 20
    td = Multiplet(v , I, [(J, r)]) 
    grafica = mplplot(td.peaklist(), points=1000, w=ww, limits=(min_x, max_x))
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

#Jdoubling
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

#Confirmacion subarmonicos 
def Armonics (x, integ):
    armonic1 = x
    if armonic1 in integ: 
        print(f"armonico coincide perfectamente: {armonic1}")
        return armonic1 
    
    elif armonic1 + 1 in integ:
        print(f"armonico coincide +1: {armonic1 + 1}") 
        
        return armonic1 + 1

    elif armonic1 + 2 in integ: 
        print(f"armonico coincide +2: {armonic1 + 2}")
        
        return armonic1 + 2
    
    elif armonic1 - 1 in integ: 
        print(f"armonico coincide -1: {armonic1 - 1}")
        return armonic1 - 1
    
    elif armonic1 - 2 in integ:
        print(f"armonico coincide -2: {armonic1 -2}") 
        return armonic1 - 2
    
    else:
        print("subarmonico no confirmado")
        return 0
    

#Para simular 
J = 1.0
ww = 0.5
dividir = 5
print(f"J referencia: {J}")
print(f"W ancho de señal: {ww}")
ruido = ReadJsonNoise("RandomNoise.json", dividir) 
multiplete = multiplet(1200.0, 1, J, 1, ww) 
intensidades = multiplete[1] 
desplazamiento = multiplete[0] 
señalCruido = ruido + intensidades 
mse, rmse, s_n = Noise(intensidades, ruido) 
#Grafica 
plt.plot(desplazamiento, señalCruido)
#plt.title(f"Relación Señal/Ruido: {s_n}")
plt.xlabel("Desplazamiento (Hz)")
plt.ylabel("Intensidades")
plt.show()


archiv_txt(desplazamiento, señalCruido)

#JDoubling
yy, a, b = leer_archivo('Prueba.slc')

iz = 0
de = len(yy) - 1

# Generar la secuencia xx
paso_hz = abs(a-b)/len(yy)
xx = [i*paso_hz+min([a, b]) for i in range(0, len(yy))]

#Redefiniendo el arreglo en y
yy = yy[iz:de]
xx = xx[iz:de]
nuevo_paso_hz = (xx[-1]-xx[0])/len(yy)

# La escala en X de la siguiente figura está en enteros. Utilizar paso_Hz para convertir a Hz
intervalo = int((J / paso_hz) * 1.3)
m = 164
integrs = integrar(yy, intervalo, m)

plt.figure(figsize=(20,10))
plt.plot(integrs, marker = 'o')
plt.xlabel("no. de punto * resolución digital (Hz)")
plt.show()

busqueda = int(intervalo/7)
minimosR = argrelextrema(integrs, np.less, order=busqueda, mode= 'wrap')[0]#busca el minimo mas minimo

minimos = argrelextrema(integrs, np.less, mode='wrap')[0] #me da todos los minimos con ruido

print(f"valores minimos (+ ruido) en: {minimos}")

armonic1 = int((minimosR[-1])/3)

subarmos= Armonics(armonic1, minimos)

Jota = minimosR[-1] * paso_hz

distance = Jota - (subarmos * paso_hz)
Er = J - Jota
er2 = pow(Er, 2)

#Seleccionar el mínimo deseado para que se determine la J.¶
print(f"Jota Determinada: {Jota}         Resolución Digital: {paso_hz}")
print(f"la distancia es: {distance} Hz")
print(f"Error: {Er}         Error al cuadrado: {er2}")


