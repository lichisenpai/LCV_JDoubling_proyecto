import numpy as np
from nmrsim import Multiplet
from nmrsim.plt import mplplot
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import json 

def ReadJsonNoise (x, c):
    prueba = pd.read_json(x)
    Y = prueba['Random']#para tenerlo como array
    Rvalue = np.random.choice(Y, 1000)#wlige 1000 puntos al azar, y 1000 por que es el valor de puntos que yo meti por default a mi simulacion
    Norm = list(map(lambda w: w / c, Rvalue))#El c es el valor que divide los valores random de ruido, entre mayor el no. se ve menis el ruido
    return Norm


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

def new_data (J, d, E): #Escribir los datos que quiero dentro del diccionario
    #J= cte. de acoplamiento que yo puse(jota), d= cte. de acoplamiento determinada(calc), E=error 
    dato_n = {}
    
    dato_n['Jref'] = J
    dato_n['Jdet'] = d
    dato_n['Width'] = 1.5 
    dato_n['Error'] = E 
    return dato_n

#crear el Json 
def escritura_json (x):
    nombre = f"W_{x}Hz.json"
    with open(nombre, 'w') as archivo: 
        json.dump(Jota_0_5Hz, archivo)
        #print("Archivo exportado con éxito")
    return 

#jotas = np.linspace(0.5, 12.0, 201)#el intervalo de trabajo de las J´s en las que quiero trabajar
jotas = [1.0, 7.0, 12.0]

calc = [] #lista para guardar la J que determina JDoubling

Jota_0_5Hz = [] #lista donde guardar los datos para el json


for i in range (len(jotas)):
    #Para simular 
    J = jotas[i]
    ruido = ReadJsonNoise("RandomNoise.json", 80) 
    multiplete = multiplet(1200.0, 1, J, 1) 
    intensidades = multiplete[1] 
    desplazamiento = multiplete[0] 
    señalCruido = ruido + intensidades 
    mse, rmse, s_n = Noise(intensidades, ruido) 
    """#Grafica 
    plt.plot(desplazamiento, señalCruido)
    plt.title(f"Relación Señal/Ruido: {s_n}")
    plt.xlabel("Desplazamiento (Hz)")
    plt.ylabel("Intensidades")
    plt.show()
    """
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
    intervalo = int((J / paso_hz) * 4)
    m = 164
    integrs = integrar(yy, intervalo, m)

    plt.figure(figsize=(20,10))
    plt.plot(integrs, marker = 'o')
    plt.show()

    minimos = argrelextrema(integrs, np.less)[0]

    print(f"valores minimos en: {minimos}")
    print("Mínimo: ", integrs[19])

    Jota = minimos[-1] * paso_hz

    calc.append(Jota) 

    #Seleccionar el mínimo deseado para que se determine la J.¶
    print(f"Jota: {Jota}         Resolución Digital: {paso_hz}")


Error = list(np.array(jotas)-np.array(calc)) 

print("Los valores de J determinados por JDoubling son: ", calc)
print("Los errores son:", Error)


for a, b, c in zip(jotas, calc, Error):
    new_entry = new_data(a, b, c)
    Jota_0_5Hz.append(new_entry) 

escritura_json(1111)