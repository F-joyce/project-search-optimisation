from ga_2d import function_that_builds_configuration

from deap import creator, base, tools
import numpy as np


def function_that_build_seed(icls):
    array = np.random.choice([4,5], 500, p=[0.5,0.5])
    #assert(array.shape[0] == (shape[0]*shape[1])), "parameters number do not match shape"
    array_shaped = array.reshape(25, 20)
    new_configuration = icls(array_shaped.tolist())
    return new_configuration

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register("individual", function_that_builds_configuration, creator.Individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("seeded_ind", function_that_build_seed, creator.Individual)
toolbox.register("seeded_pop", tools.initRepeat, list, toolbox.seeded_ind)

# pop = toolbox.population(n=10)
# pop2 = toolbox.seeded_pop(n=10)

# print(len(pop))
# print(len(pop2))

# pop[:5] = pop2[:5]

# #print(pop)

ind = np.loadtxt("./processes/0/data.txt")
print(type(ind))

i = creator.Individual(ind.tolist())

print(type(i))
print(i)