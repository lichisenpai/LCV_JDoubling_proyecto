import numpy as np
from nmrsim import Multiplet
from nmrsim.plt import mplplot
import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt 

"""YA FUNCIONA!! NO LE MUEVAS NI MADRES LIAT!!! O LO VAS A DESCOMPONER!! 
solo mueve los valores que quieres cambiar"""

ref = 0.5, 7.0

calc = []

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


for i in range (len(ref)): 
    # 1200 Hz, 2H, td, J= 7.1, 1.1 Hz
    td = Multiplet(1200 , 1, [(ref[i], 1)]) #aqui entra en juego ref 
    grafica = mplplot(td.peaklist(), points=1000)

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
    
    for i in range (len(intensidades1)):
        f.write(str(intensidades1[i])+"\n")
    
    f.close()

    #Intento de programa conjunto (JDoubling del profe)

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
    intervalo = 150
    m = 300
    integrs = integrar(yy, intervalo, m)

    minimos = argrelextrema(integrs, np.less)[0]

    print(f"valores minimos en: {minimos}")
    print("Mínimo: ", integrs[19]) 
    
    Jota = minimos[-1] * paso_hz #esta es la variable que quiero guardar 

    #for i in range (len(ref)): #Esta es la parte que no me sale para guardar los datos
    calc.append(Jota) #se guarda las i veces que da la vuelta el codigo pero solo de la ultima J

    print(f"Jota: {Jota}         Resolución Digital: {paso_hz}")


print("Los valores de J determinados por JDoubling son: ", calc)