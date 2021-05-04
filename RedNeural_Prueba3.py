import matplotlib.pyplot as plt
import pandas as pd

import tensorflow as tf
"""
from tensorflow import keras
from tensorflow.keras import layers
"""
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

def Normalize_Data ():
    train_stats = statistics()
    train_dataset, test_dataset = Division_data()
    
    train_labels = train_dataset.pop('Error')
    test_labels = test_dataset.pop('Error')

    normalizing = lambda x: (x - train_stats['mean'])/ train_stats['std'] 
    normed_train_data = normalizing(train_dataset)
    normed_test_data = normalizing(test_dataset)
    return normed_train_data, normed_test_data