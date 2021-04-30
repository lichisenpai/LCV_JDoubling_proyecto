from platform import platform
import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor 
from sklearn.metrics import r2_score
from sklearn import decomposition
import matplotlib.pyplot as plt 


#leer el Json y acomodarlo a matriz
def leer_Json ():
    prueba = pd.read_json('W_1_0Hz.json')
    Y = prueba['Error'].values.reshape(-1, 1) #valor a predecir
    X = prueba[['Jref', 'Jdet', 'Width']].values.reshape(-1, 3) #Variables explicatorias
    X1 = prueba['Jdet'].values.reshape(-1,1)
    return X, Y,X1

X, Y, X1 = leer_Json()
#print (Y)
plt.plot(X1, Y)
plt.xlabel("Jdet")
plt.ylabel("Error")
plt.title("Reducción de dimensionalidad para una W= 1.0 Hz")
plt.show()

"""
#remuestreo 70/30 
def remuestreo70_30 ():
    X, Y = leer_Json()
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=40)
    return X_train, X_test, y_train, y_test

#Esta es la red neuronal
def lichi ():
    while True: 
        X_train, X_test, y_train, y_test = remuestreo70_30()
        lichi = MLPRegressor(solver='adam', alpha=1e-5, hidden_layer_sizes=(4,3), tol=1e-4, random_state=1)
        lichi.fit(X_train,y_train) #para que entrene
        #predict_train = lichi.predict(X_train)
        #predict_test = lichi.predict(X_test)
        #ver r2
        #print("La r2 con la data de prueba: ", r2_score(y_test,predict_test)) #la r2 de los datos de prueba a ver que da 
        Score = lichi.score(X_train,y_train)
        print(Score)
        if Score > 0.98:
            break
        return lichi, Score

lichi()
    
"""