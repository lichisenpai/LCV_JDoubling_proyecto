import pandas as pd 
import json

b = pd.read_json('J1yW6_1ruido.json')
c = pd.read_json('J1yW6_2ruido.json')
d = pd.read_json('J1yW6_3ruido.json')
e = pd.read_json('J1yW6_4ruido.json')
f = pd.read_json('J1yW6_5ruido.json')
g = pd.read_json('J1yW6_6ruido.json')
h = pd.read_json('J1yW6_7ruido.json')
i = pd.read_json('J1yW6_8ruido.json')
j = pd.read_json('J1yW6_9ruido.json')
k = pd.read_json('J1yW7_0ruido.json')


previo = pd.read_json('J1HzW5_6a12_0Hz.json')
dataset = pd.concat([previo, b, c, d, e, f, g, h, i, j, k], axis=0)
#crear el Json 
def escritura_json (x):
    nombre = f"{x}.json"
    with open(nombre, 'w') as archivo: 
        json.dump(parsed, archivo)
        #print("Archivo exportado con éxito")
    return 

result = dataset.to_json(orient="records")
parsed = json.loads(result)
escritura_json("J1HzW5_6a12_0HzARREGLADO")
