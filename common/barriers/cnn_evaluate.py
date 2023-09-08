import keras
import numpy as np
from cnn_utils import denormalise

m = keras.models.load_model("simple_CNN.keras")

high = -1.347716529e-08
low = -4.232721913e-08

def cal_pop_fitness_CNN(pop):
    pop_array = np.asarray(pop.copy())
    pop = pop_array.reshape(pop_array.shape[0], 30, 15, 1)
    fitness = m.predict(pop)
    fitness = denormalise(fitness, high,low)
    print("pause")
    return fitness