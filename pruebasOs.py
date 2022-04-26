import os
import pandas as pd
import glob
  
folder_path = 'J6_0Hz'
archivos = glob.glob(folder_path + "/*.json")

#archivos =  os.listdir('J6_0Hz')
#print(type(archivos[0]))


main_dataset = pd.DataFrame(pd.read_json(archivos[0]))

for i in range(1 ,len(archivos)):
    a = pd.read_json(archivos[i])
    main_dataset= pd.concat([main_dataset, a], axis=0)

print(main_dataset.tail)
print("El tamaño del Df es: " ,main_dataset.shape)
