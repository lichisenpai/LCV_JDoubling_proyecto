import matplotlib.pyplot as plt
import pandas as pd

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

def leer_Json ():
    readjson = pd.read_json('W_1_0Hz.json')
    dataset = readjson.copy()
    return dataset

def Division_data ():
    dataset = leer_Json()
    train_dataset = dataset.sample(frac=0.8,random_state=0)
    test_dataset = dataset.drop(train_dataset.index)
    return train_dataset, test_dataset 

def statistics ():
    train_dataset, test_dataset = Division_data()
    train_stats = train_dataset.describe()
    train_stats.pop("Error") #quite la columna de error por que solo quiero los valores de entrada
    train_stats = train_stats.transpose()
    return train_stats

"""
def prueba (x):
    train_stats = statistics()
    desvest = train_stats['std']
    if desvest > 0:
        normalizado = (x - train_stats['mean'])/ train_stats['std']
    else:
        return x 

"""

def Normalize_Data ():
    train_stats = statistics()
    train_dataset, test_dataset = Division_data()
    
    train_labels = train_dataset.pop('Error')
    test_labels = test_dataset.pop('Error')
    
    normalizing = lambda x: (x - train_stats['mean'])/ train_stats['std'] 
    normed_train_data = normalizing(train_dataset[['Jref', 'Jdet']])
    normed_test_data = normalizing(test_dataset[['Jref', 'Jdet']])
    normed_train_data['Width']= 1 #parche en lo que averiguo como hacer que no tome en cuenta el error 
    normed_test_data['Width']= 1

    return normed_train_data, normed_test_data, train_labels, test_labels

def NeuralNetwork ():
    train_dataset, test_dataset = Division_data()
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=[len(train_dataset.keys())]),
        layers.Dense(64, activation='relu'),
        layers.Dense(1)
        ])

    optimizer = tf.keras.optimizers.RMSprop(0.001)

    model.compile(loss='mse',optimizer=optimizer, metrics=['mae', 'mse'])
    return model

"""
Notas Licha: 
-Batch size: tamaño del lote de los datos que se mandaran cada vez a la red neuronal 
-iteracion: una pasada hacia adelante y hacia atras para los valores del lote 
-one epoch: una pasada hacia adelante y hacoa atras para todos los valores del entrenamiento 
"""
def TryingModel (): #aqui no entiendo como prueban el modelo abtes de entrenarlo 
    normed_train_data, normed_test_data = Normalize_Data()
    model = NeuralNetwork()
    example_batch = normed_train_data[:10]
    example_result = model.predict(example_batch)
    print(example_result) 

def TrainModel ():
    normed_train_data, normed_test_data, train_labels, test_labels = Normalize_Data ()
    model = NeuralNetwork()
    history = model.fit(
        normed_train_data, train_labels, #segun yo train evels es la Y 
        epochs=300,
        validation_split = 0.2, verbose=0
        )
    return history 

def TrainmentProgress (): #Esta ni se usa realmente 
    history = TrainModel()
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch
    print(hist.tail())
    return hist, history

def plot_history():
    history = TrainModel() 
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [MPG]')
    plt.plot(hist['epoch'], hist['mae'],label='Train Error')
    plt.plot(hist['epoch'], hist['val_mae'], label = 'Val Error')
    plt.legend()

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Square Error [$MPG^2$]')
    plt.plot(hist['epoch'], hist['mse'], label='Train Error')
    plt.plot(hist['epoch'], hist['val_mse'], label = 'Val Error')
    plt.legend()
    plt.show()

plot_history()


    