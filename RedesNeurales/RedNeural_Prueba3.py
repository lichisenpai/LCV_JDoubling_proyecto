import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

def leer_Json ():
    prueba = pd.read_json('W_1_0Hz.json')
    Y = prueba['Error'].values.reshape(-1, 1) #valor a predecir
    X = prueba[['Jref', 'Jdet', 'Width']].values.reshape(-1, 3) #Variables explicatorias
    #X1 = prueba['Jdet'].values.reshape(-1,1)
    return X, Y