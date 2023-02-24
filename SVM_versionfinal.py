#Radial 

from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

#Data preprocessing

import pandas as pd 
import json
import matplotlib.pyplot as plt
import numpy as np

dataset = pd.read_json('J_Concatenadas_Final.json')

def max_aceptado (x):
  return x * 0.95

def min_aceptado (x):
  return x * 1.05 

#haciendo limpieza de los datos
dataset_clean = dataset.loc[dataset.loc[:, '1Subharmonic'] != 0.0] #quitando los valores cuando subarmonico dif a cero 
dataset_clean['Max_acept'] = dataset_clean['Jref'].apply(max_aceptado)
dataset_clean['Min_acept'] = dataset_clean['Jref'].apply(min_aceptado)

print("Dataset limpio\n", dataset_clean.tail())

# define your data
X = dataset_clean[['S/n', 'Jdet']]
#Y = dataset_clean['Cluster'] = [0 if s >= 0.15 or a <= 100 else 1 for s, a in zip(X['Error'], X['S/n'])]
condiciones = [(dataset_clean.Jdet >= dataset_clean.Max_acept) & (dataset_clean.Jdet <= dataset_clean.Min_acept), 
               (dataset_clean.Jdet <= dataset_clean.Max_acept)& (dataset_clean.Jdet >= dataset_clean.Min_acept)]
elecciones = np.array((0, 1), dtype="int8")
Y = dataset_clean['Cluster'] = np.select(condiciones, elecciones, -1)

#Grafica
colores = ["#00cc44", "#ff0000"]   # Green & Red 
plt.scatter(X['S/n'], X['Jdet'], c=np.take(colores, Y), s=10)
plt.xlabel("S/n ratio")
plt.ylabel("Jdet (Hz)")
plt.show()



#sepparating data
train_dataset, test_dataset ,train_labels, test_labels = train_test_split(X, Y, test_size=0.30, random_state=40)


# Grid de hiperparámetros
# ==============================================================================
param_grid = {'C': np.logspace(-5, 7, 20)}

# Búsqueda por validación cruzada
# ==============================================================================
grid = GridSearchCV(
        estimator  = SVC(kernel= "rbf", gamma='scale'),
        param_grid = param_grid,
        scoring    = 'accuracy',
        n_jobs     = -1,
        cv         = 3, 
        verbose    = 0,
        return_train_score = True
      )

_ = grid.fit(train_dataset, train_labels)

# Resultados del grid
# ==============================================================================
resultados = pd.DataFrame(grid.cv_results_)
resultados.filter(regex = '(param.*|mean_t|std_t)')\
    .drop(columns = 'params')\
    .sort_values('mean_test_score', ascending = False) \
    .head(5)

# Mejores hiperparámetros por validación cruzada
# ==============================================================================
print("----------------------------------------")
print("Mejores hiperparámetros encontrados (cv)")
print("----------------------------------------")
print(grid.best_params_, ":", grid.best_score_, grid.scoring)

modelo = grid.best_estimator_

# Representación gráfica de los límites de clasificación
# ==============================================================================

# Grid de valores
x = np.linspace(np.min(train_dataset['S/n']), np.max(train_dataset['S/n']), 50)
y = np.linspace(np.min(train_dataset['Jdet']), np.max(train_dataset['Jdet']), 50)
Y, X = np.meshgrid(y, x)
grid = np.vstack([X.ravel(), Y.ravel()]).T

# Predicción valores grid
pred_grid = modelo.predict(grid)

fig, ax = plt.subplots(figsize=(12,8))
#ax.scatter(grid[:,0], grid[:,1], c=pred_grid, alpha = 0.2)
ax.scatter(train_dataset['S/n'], train_dataset['Jdet'], c=train_labels, alpha = 1, s =9)

"""# Vectores soporte
ax.scatter(
    modelo.support_vectors_[:, 0],
    modelo.support_vectors_[:, 1],
    s=5, linewidth=1,
    facecolors='none', edgecolors='black'
)"""

# Hiperplano de separación
ax.contour(
    X, Y,modelo.decision_function(grid).reshape(X.shape),
    colors='k',
    levels=[0],
    alpha=0.5,
    linestyles='-'
)
#s=str(modelo.decision_function(grid).reshape(X.shape)[0,2])

#ax.text(0.5, 0.5, s, bbox=dict(facecolor='white', alpha=0.5))

ax.set_title("Resultados clasificación SVM radial");

#Guardando el modelo 
import joblib

joblib_file = "LichiSVM.pkl"
joblib.dump(modelo, joblib_file)