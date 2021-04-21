import numpy as np
import json 

Jota_0_5Hz = [] #lista donde guardar los datos 

def new_data (J, d, E): #Escribir los datos que quiero dentro del diccionario 
    dato_n = {}
    
    dato_n['Jref'] = J
    dato_n['Jdet'] = d
    dato_n['Width'] = 3
    dato_n['Error'] = E 
    return dato_n

#variables que quiero meter 
Error = np.linspace(0.1, 0.5, 5)
jotas = np.linspace(0.5, 12.0, 5)
#W = np.linspace(0.3, 9.0, 5)
#s_n = np.linspace(0.5, 4.0, 5)
Determinada = np.linspace(0.5, 3, 5)

#ciclo para que me guarde cada conjunto de datos en un diccionario para el Json
for a, b, c in zip(jotas, Determinada, Error):
    new_entry = new_data(a, b, c)
    Jota_0_5Hz.append(new_entry)

print(Jota_0_5Hz) #Para que me imprima la lista y ver si si se guardaron correctamente los datos 

#crear el Json 
def escritura_json ():
    with open('data_base.json', 'w') as archivo: 
        json.dump(Jota_0_5Hz, archivo)
        print("Archivo exportado con éxito")
    return 

escritura_json() #pedirle a la compu que me cree el json