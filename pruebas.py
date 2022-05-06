import numpy as np 
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt

dataset_clean = pd.read_json("J_Concatenadas\J12_0Hz_Concatenado.json")

"""fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)

ye = "Error"

ax1.plot(dataset_clean['Width'], dataset_clean[ye], "kx")
ax1.set_title("Ancho de Señal (HZ)")
ax2.plot(dataset_clean['1Subharmonic'], dataset_clean[ye], "kx")
ax2.set_title("Subarmónico (Hz)")
ax3.plot(dataset_clean['Distance'], dataset_clean[ye], "kx")
ax3.set_title("Distancia (Hz)")
ax4.plot(dataset_clean['S/n'], dataset_clean[ye], "kx")
ax4.set_title("S/n ratio")
fig.tight_layout()
plt.show()"""

plt.plot(dataset_clean["S/n"], dataset_clean["Error"], "kx")
plt.show()
