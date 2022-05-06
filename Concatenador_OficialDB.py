
import pandas as pd
import glob
import matplotlib.pyplot as plt
import json


folder_path = 'J_Concatenadas'
archivos = glob.glob(folder_path + "/*.json")


main_dataset = pd.DataFrame(pd.read_json(archivos[0]))

for i in range(1 ,len(archivos)):
    a = pd.read_json(archivos[i])
    main_dataset= pd.concat([main_dataset, a], axis=0)

#print(main_dataset.tail)
print("El tamaño del Df es: " ,main_dataset.shape)

#plt.scatter(main_dataset["1Subharmonic"], main_dataset["Error"])
#plt.show()


lichi= main_dataset.to_json(f"{folder_path}_Final.json", orient="records")