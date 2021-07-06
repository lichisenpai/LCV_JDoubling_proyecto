import numpy as np 

signal = np.array([1,2,3,4,5,6])

r1 = 3
r2 = 5

subsetter = np.where((signal <= int(r2)) & (signal >= int(r1)))
print(subsetter)