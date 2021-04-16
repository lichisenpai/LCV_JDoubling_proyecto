import numpy as np
import json 

Jota_0_5Hz = [
    {
        'E': 0.5,
        'J': 5.0,
        'S_n': 3.0,
        'd': 0.3,
        'w': 0.5
    }

]

def new_data (E, J, S_n, d, w):
    dato_n = {}

    dato_n['E'] = E 
    dato_n['J'] = J
    dato_n['S_n'] = S_n
    dato_n['d'] = d
    dato_n['w'] = w
    return dato_n


#Jota_0_5Hz.append(new_data())
Error = np.linspace(0.1, 0.5, 5)

jotas = np.linspace(0.5, 12.0, 5)

W = np.linspace(0.3, 9.0, 5)

s_n = np.linspace(0.5, 4.0, 5)

D = np.linspace(0.5, 3, 5)

for a, b, c, e, f in zip(Error, jotas, s_n, D, W):
    new_entry = new_data(a, b, c, e, f)
    Jota_0_5Hz.append(new_entry)


print(Jota_0_5Hz)