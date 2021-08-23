import numpy as np 
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt
"""nose = [1,2,3,4,5,6,7,8.2,8.4,9,8.3]

vacio =[]

for i in range (len(nose)):
    lol = nose[i]
    if lol < 9:
        vacio.append(lol)
        if lol >= 8.0 and lol <= 8.9:
            print(nose.index(lol))

print("la lista es", vacio)"""

df = pd.read_json("J10_8yW12_0ruido.json")

menor200 = df.loc[df.loc[:, 'S/n'] <= 200.0]
mayor200 = df.loc[df.loc[:, 'S/n'] >= 200.0]
#print("menor a 200", menor200.tail())
#print("mayor a 200", mayor200.tail())


print("menor a 200:", len(menor200))
print("mayor a 200:", len(mayor200))

"""RelacionVariables = sns.pairplot(menor200[['Jdet', 'Width', '1Subharmonic', 'Distance', 'S/n', "Error"]])
RelacionVariables1 = sns.pairplot(mayor200[['Jdet', 'Width', '1Subharmonic', 'Distance', 'S/n', "Error"]])"""

plt.scatter(menor200['Jdet'], menor200['Distance'])
plt.show()

