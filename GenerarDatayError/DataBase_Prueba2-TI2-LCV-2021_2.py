import numpy as np
import json  

class Data_Base ():
    Jota_0_5Hz = []

    def new_data(self):
        dato_n = {}

        self.dato_n['E'] = E 
        self.dato_n['J'] = J
        self.dato_n['S_n'] = S_n
        self.dato_n['d'] = d
        self.dato_n['w'] = w
        return dato_n
    
    def int_data (self, Error, jotas, s_n, D, W):
        for a, b, c, e, f in zip(Error, jotas, s_n, D, W):
            self.new_entry = new_data(a, b, c, e, f)
            self.Jota_0_5Hz.append(self.new_entry)
        return 

    
    def escritura_json ():
        with open('data_base.json', 'w') as archivo: 
            json.dump(Jota_0_5Hz, archivo)
            print("Archivo exportado con éxito")
        return 

Error = np.linspace(0.1, 0.5, 5)
jotas = np.linspace(0.5, 12.0, 5)
W = np.linspace(0.3, 9.0, 5)
s_n = np.linspace(0.5, 4.0, 5)
D = np.linspace(0.5, 3, 5)

prueba = Data_Base()
prueba.int_data(Error, jotas, s_n, D, W)
prueba.escritura_json()