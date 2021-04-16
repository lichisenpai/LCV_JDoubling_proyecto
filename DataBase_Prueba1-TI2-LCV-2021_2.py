import numpy as np
import json 

Jota_0_5Hz = [] #lista donde guardar los datos 

def new_data (E, J, S_n, d, w): #Escribir los datos que quiero dentro del diccionario 
    dato_n = {}
    dato_n['E'] = E 
    dato_n['J'] = J
    dato_n['S_n'] = S_n
    dato_n['d'] = d
    dato_n['w'] = w
    return dato_n

#variables que quiero meter 
Error = np.linspace(0.1, 0.5, 5)
jotas = np.linspace(0.5, 12.0, 5)
W = np.linspace(0.3, 9.0, 5)
s_n = np.linspace(0.5, 4.0, 5)
D = np.linspace(0.5, 3, 5)

#ciclo para que me guarde cada conjunto de datos en un diccionario para el Json
for a, b, c, e, f in zip(Error, jotas, s_n, D, W):
    new_entry = new_data(a, b, c, e, f)
    Jota_0_5Hz.append(new_entry)

print(Jota_0_5Hz) #Para que me imprima la lista y ver si si se guardaron correctamente los datos 

#crear el Json 
def escritura_json ():
    with open('data_base.json', 'w') as archivo: 
        json.dump(Jota_0_5Hz, archivo)
        print("Archivo exportado con éxito")
    return 

escritura_json() #pedirle a la compu que me cree el json