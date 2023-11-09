from ga_2d import function_that_calculate_percentages, function_that_builds_configuration
from ga_2d import function_that_evaluate_population
from ga_2d import function_that_creates_folders_structure
from ga_2d import function_that_batches
import random 
from deap import creator, base

def test_percentages(n):
    r = random.randint
    for n in range(n):
        percentages = function_that_calculate_percentages([(80,90),(0,10),(0,10)])
        if sum(percentages) == 1:
            continue
        else:
            ValueError("Something is wrong")
    print("All good")
    return True

passed = test_percentages(1000)

def test_create_icls_individual(n):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    toolbox.register("individual", function_that_builds_configuration, creator.Individual)
    a = toolbox.individual()
    #print(a)
    #print(type(a))
    return a

#test_create_icls_individual(1)

def test_evaluate_population(n):
    function_that_creates_folders_structure(n)
    pop = []
    for n in range(n):
        i = test_create_icls_individual(1)
        pop.append(i)
        if n == 1:
            print(i)

    fitnesses = function_that_evaluate_population(pop)
    print(fitnesses)
    assert(len(pop) == len(fitnesses)), "Number of fitness value does not correspond to number of individuals"

#test_evaluate_population(2)

def test_batches(n,m):
    function_that_creates_folders_structure(m)
    pop = []
    for n in range(n):
        i = test_create_icls_individual(1)
        pop.append(i)
        if n == 1:
            #print(i)
            pass
    total_fit = function_that_batches(pop,m)
    print(total_fit)
    assert(len(total_fit) == n), "total fitness and total population don't match"

#test_batches(100,10)