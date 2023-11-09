import numpy as np

Bshape=np.loadtxt('./data.csv')

sample_fitness = -1.40e-08


with open('min.txt', 'w') as f:
	print(sample_fitness,file=f)
