import numpy as np

Bshape=np.loadtxt('./data.txt')

sample_fitness = -1.40e-08

flat = Bshape.flatten()
sum_ = np.sum(flat)
sample_fitness = sum_

with open('min.txt', 'w') as f:
	print(sample_fitness,file=f)

