import json 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor 
from sklearn.metrics import r2_score
from sklearn import decomposition

#cargando los datos del Json
with open ('W_1_0Hz.json', 'r') as archivo:
    base_de_datos = json.load(archivo)
    print("Archivo exportado con exito")

Jref = []
Jdet = []
Width = []
Error = []

for i in range (len(base_de_datos)):
    Jref.append(base_de_datos[i]["Jref"])

for j in range (len(base_de_datos)):
    Jdet.append(base_de_datos[j]["Jdet"])

for k in range (len(base_de_datos)):
    Width.append(base_de_datos[k]["Width"])


for l in range(len(base_de_datos)):
    Error.append(base_de_datos[l]["Error"])

#reshape
Yerror = np.array(Error).reshape(201,1) #201 filas por una columna para y (Error)

Jdet1 = np.array(Jdet).reshape(201,1)#haciendo los arrays de las listas 
Jref1 = np.array(Jref).reshape(201,1)
Width1 = np.array(Width).reshape(201,1)


X = np.array([Jref1,Jdet1,Width1]).reshape(-1,3)#ya esta listo mi array de x (Jref, Jdet, Width)

#reduccion de dimensionalidad
#pca = decomposition.PCA(n_components=2)
#X = pca.fit_transform(X)

#división de datos 70/30 
X_train, X_test, y_train, y_test = train_test_split(X, Yerror, test_size=0.30, random_state=40)

#La red ahora si 
lichi = MLPRegressor(solver='adam', alpha=1e-4, hidden_layer_sizes=(4,3),  max_iter=200, tol=1e-4, random_state=1)
lichi.fit(X_train,y_train) #para que entrene
predict_train = lichi.predict(X_train)
predict_test = lichi.predict(X_test)

#ver la r2
print(r2_score(y_test,predict_test)) #la r2 de los datos de prueba a ver que da 
print(lichi.score(X_train,y_train)) #la r2 de la regresion con los datos de entrenamiento
