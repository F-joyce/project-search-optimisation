import numpy as np

Bshape=np.loadtxt('./data.csv')

sample_fitness = np.sum(Bshape)/450*(-0.00000001)


with open('min.txt', 'w') as f:
	print(sample_fitness,file=f)
