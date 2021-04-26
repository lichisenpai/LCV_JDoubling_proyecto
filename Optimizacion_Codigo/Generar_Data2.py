import numpy as np
from nmrsim import Multiplet
from nmrsim.plt import mplplot
import numpy as np
from scipy.signal import argrelextrema
import json
import matplotlib.pyplot as plt

jotas = np.linspace(0.5, 12.0, 201)#el intervalo de trabajo de las J´s en las que quiero trabajar
#jotas = [0.7, 1.0, 12.0]

calc = [] #lista para guardar la J que determina JDoubling

Jota_0_5Hz = [] #lista donde guardar los datos para el json

#esta es la funcion que te digo que no sirve cuando la intento llamar dentro del bucle
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
def integrar(yy, intervalo , m):
    #intervalo es el maximo valor de las n
    
    integrs = np.zeros(intervalo)
    
    for i in range(1, intervalo):
        y_new = convolucion(yy, i, m)
        integral = sum(abs(y_new))
        integrs[i] = integral
    return integrs

#Generando un vector con la señal trasladada 1 vez
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


for i in range (len(jotas)): 
    # v = 1200 Hz, I = intensidad, J = cte. acoplamiento, r = vecinos 
    J = jotas[i]
    v = 1200.0
    min_x = v - 20 
    max_x = v + 20
    td = Multiplet(v , 1, [(J, 1)]) #aqui entra en juego jotas 
    grafica = mplplot(td.peaklist(), points=1000, w =1.5, limits= (min_x, max_x))

    #para crear el archivo de texto
    intensidades = (grafica[1]) * 10000 #aqui lo multiplico x10000 por que si no me da valores bien pequeños, pero si lo ves innecesario piedes quitarlo
    no_datos = len(grafica[1])
    intensidades1 = [] #creo esta lista por que como ves en el buclesito de abajo, guardo los valores hasta 6 cifras para no hacer el archivo de texto bien pesado 

    for i in range (len(intensidades)):
        intensidades1.append(round(intensidades[i], 6))

    Hz = (grafica[0])# Son los valores en x (Hz)de la simulacion que nos daba grafica, y grafica[1] son los valores en y de esa simulacion (intensidades)
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
    
    for i in range (len(intensidades1)): #simplemente me va acomodando dato por dato en el archivo slc
        f.write(str(intensidades1[i])+"\n")
    
    f.close()

    #A partir de aqui es JDoubling

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
    intervalo = int((J/ paso_hz) * 2.1)
    m = 128
    integrs = integrar(yy, intervalo, m)

    minimos = argrelextrema(integrs, np.less)[0]

    print(f"valores minimos en: {minimos}") 
    
    Jota = minimos[-1] * paso_hz 


    calc.append(Jota) 

    print(f"Jota: {Jota}         Resolución Digital: {paso_hz}")


Error = list(np.array(jotas)-np.array(calc)) 

print("Los valores de J determinados por JDoubling son: ", calc)
print("Los errores son:", Error)


for a, b, c in zip(jotas, calc, Error):
    new_entry = new_data(a, b, c) 
    Jota_0_5Hz.append(new_entry) 

escritura_json("1_5")