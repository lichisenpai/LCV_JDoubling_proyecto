
import pandas as pd
import matplotlib.pyplot as plt

a = pd.read_json('J1_0Hz\J1HzW0_5a5_5Hz.json')
b = pd.read_json('J1_0Hz\J1HzW5_6a12_0HzARREGLADO.json')

dataset = pd.concat([a, b], axis=0) #llamando al dataset en bruto

#haciendo limpieza de los datos
dataset_clean = dataset.loc[dataset.loc[:, '1Subharmonic'] != 0.0] #quitando los valores cuando subarmonico dif a cero 

print("Dataset limpio\n", dataset_clean.tail())

#separando X|Y

X = dataset_clean['1Subharmonic'].values.reshape(-1,1) #ahora son array 444, 1
Y = dataset_clean['Jdet'].values.reshape(-1,1)

plt.hist(X, bins = 10)
plt.xlabel("Subarmonico (Hz)")
plt.ylabel("Count")
plt.show()
