import numpy as np
from nmrsim import Multiplet
from nmrsim.plt import mplplot
import numpy as np
from scipy.signal import argrelextrema
import json

"""Hola! Soy Liat!!! 
1-Como puedes ver, de las lineas 36 a 146 estan declaradas todas las funciones que 
se usan a lo largo del programa
2- En la linea 152 esta delcarado el bucle que corre el programa conjunto (mi simulacion + JDoubling)
una cantidad n de veces, dependiendo de cuantos datos quiero generar
3-Con respecto a lo de correr el programa una cantidad n de veces: es con respecto a ls variable "jotas" 
de la linea 29, yo le meti 201 puntos pues para generar datos de la simulacion (con J definida) y ver que 
me devuelve J Doubling
4- Para calcular el error (jota - calc) en la linea 230 uso una resta de matrices por que vi que es mas
rapido que estar usando bucles. PD: en la linea x guardo la variable "calc" que es donde se van almacenando
los valores de J que devuelve J Doubling
5- la funcion "archiv_txt(v, I, J,r) es el lo que genera la simulacion de mi multiplete y aparte genera
el archivo de texto que despues lee JDoubling, al archivo se guarda con el nombre de "multiplete7.slc 
pero por alguna razon no funciona correctamente cuando intento llamarla dentro del bucle, asi que decidi 
simplemente copiar y pegar todo literal dentro del bucle para evitar problemas. PD: esto tiene un pequeño 
bug ya que en la linea x, donde se ejecuta el comando grafica = mplplot(td.peaklist(), points=1000) la
instruccion mplplot me genera una molesta grafica que no necesito en realidad, solo los datos, pero si no
lo meto asi, entonces no tengo los valores de mi simulacion, asi que se la pasa generando en cada iteracion
una molesta grafica, supongo que tiene solucion, pero no me he sentado a resolverlo con calma
"""

jotas = np.linspace(0.5,12.0, 201)#el intervalo de trabajo de las J´s en las que quiero trabajar

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
def integrar(yy, intervalo = 60, m = 8):
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
    dato_n['Width'] = 0.5 #este lo pongo constante pues por que estoy corriendo el programa para un ancho de señal de 0.5 Hz
    dato_n['Error'] = E 
    return dato_n

#crear el Json 
def escritura_json ():
    with open('W_puntocinco.json', 'w') as archivo: 
        json.dump(Jota_0_5Hz, archivo)
        print("Archivo exportado con éxito")
    return 


for i in range (len(jotas)): 
    # v = 1200 Hz, I = intensidad, J = cte. acoplamiento, r = vecinos 
    v = 1200.0
    min_x = v - 20 
    max_x = v + 20

    """la funcion Multiplet() es la que genera practicamente el multiplete que yo quiera, sus argumentos son:
    el primero "v" es el valor en Hz donde quiero tener centrada mi señal
    el segundo es la integracion que yo quiera(en este caso es irrelevante)
    el tercero y el cuarto, que estan dentro de la tupla, son:[(constante de acoplamiento, no. de H vecinos)]
    y eso es todo para la simulacion en realidad!!! la linea de abajo:  grafica = mplplot(td.peaklist(), points=1000, w = 0.5, limits= (min_x, max_x))
    lo que hace es generarme los datos como tal y le pongo algunas delimitaciones como el no. de puntos que quiero
    es el ancho que le quiero dar a la señal (en hz) y limits pues son los limites que le quiero dar a la ventana espectral"""

    td = Multiplet(v , 1, [(jotas[i], 1)]) #aqui entra en juego jotas 
    grafica = mplplot(td.peaklist(), points=1000, w = 0.5, limits= (min_x, max_x))

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
    intervalo = 400 #aqui le puse 400 por que como ya hay mas puntos en la simulacion hay que abrir mas esta ventana de la integral
    m = 300
    integrs = integrar(yy, intervalo, m)

    minimos = argrelextrema(integrs, np.less)[0]

    print(f"valores minimos en: {minimos}")
    print("Mínimo: ", integrs[19]) 
    
    Jota = minimos[-1] * paso_hz #aqui le meti que siempre busque el ultimo dato de toda la lista de minimos de la integral pues por que es la Jdeterminada


    calc.append(Jota) #se guarda las i veces que da la vuelta el codigo pero solo de la ultima J

    print(f"Jota: {Jota}         Resolución Digital: {paso_hz}")


Error = list(np.array(jotas)-np.array(calc)) #esto es lo que te digo de la resta de listas pasadas a matriz para calcular el error

print("Los valores de J determinados por JDoubling son: ", calc)
print("Los errores son:", Error)

"""este de aqui es el bucle que me va ordenando las parejitas para ir guardando todo en la lista J-0_5Hz
 de al principio y aqui las listas de la Jdeterminada (calc) y el error ya estan llenas y se puede empezar a crear el Json """

for a, b, c in zip(jotas, calc, Error):
    new_entry = new_data(a, b, c) #aqui llamo a la funcion que gice para que me valla guardando las parejitas ordenadas dentro de cada diccionario
    Jota_0_5Hz.append(new_entry) #cuando ya esta llenito cada diccionario (las i veces que se haga el bucle gigante) los va guardando dentro de la lista de antes

escritura_json()#por ultimo ya con la lista J_0_5Hz con todos los diccionarios lo guardo llamando esta funcion y al fin acaba el programa!!! 