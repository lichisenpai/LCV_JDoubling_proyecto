import pandas as pd 
import json

a = pd.read_json('J1_0Hz\J1HzW0_5a5_5Hz.json')
b = pd.read_json('J1_0Hz\J1HzW5_6a12_0HzARREGLADO.json')


dataset = pd.concat([a, b], axis=0)

print("El tamaño del Df es: " ,dataset.shape)

dataset_Sampled = dataset.sample(n=3000, random_state=1)

lichi= dataset_Sampled.to_json("J1_0Hz_Concatenado.json", orient="records")

"""
dataset = pd.concat([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p], axis=0)
#crear el Json 
def escritura_json (x):
    nombre = f"{x}.json"
    with open(nombre, 'w') as archivo: 
        json.dump(parsed, archivo)
        #print("Archivo exportado con éxito")
    return 

result = dataset.to_json(orient="records")
parsed = json.loads(result)
escritura_json("J10_8y10_6HzW10_3a12_0Hz")"""

