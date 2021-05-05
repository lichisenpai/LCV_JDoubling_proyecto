import numpy as np
import json 
import random

#Programa que genera la base de datos random para meterle ruido a las señales RMN 

Random_Noise = [] #lista donde guardar los datos 

def new_data (J): #Escribir los datos que quiero dentro del diccionario 
    dato_n = {}
    
    dato_n['Random'] = J 
    return dato_n


#crear el Json 
def escritura_json ():
    with open('RandomNoise.json', 'w') as archivo: 
        json.dump(Random_Noise, archivo)
        print("Archivo exportado con éxito")
    return 

random.seed(123)
Randoms = [random.random() for i in range(100000)]


#ciclo para que me guarde cada conjunto de datos en un diccionario para el Json
for a in (Randoms):
    new_entry = new_data(a)
    Random_Noise.append(new_entry)


escritura_json() #pedirle a la compu que me cree el json