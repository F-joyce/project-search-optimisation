import random
import numpy as np
import config

percentages_ranges = config.percentages_ranges
nmaterials = config.nmaterials
parameters = config.parameters
shape = config.shape

def function_that_calculate_percentages(percentages_range):
    # example of percentages range [(10,50),(40,60),(10,50)]
    percentages = []
    for i, _range in enumerate(percentages_range):
        to_add = random.randint(_range[0],_range[1])
        percentages.append(to_add)

    if sum(percentages) != 100:
        to_adjust = (sum(percentages) - 100)//len(percentages_range)
        remainder = (sum(percentages) - 100)%len(percentages_range)
        percentages = [percent - to_adjust for percent in percentages]
        to_modify = random.randint(0,len(percentages)-1)
        percentages[to_modify] -= remainder
        for i, value in enumerate(percentages):
            if value < 0:
                percentages[i] = 0
                percentages[percentages.index(max(percentages))] += value
    else:
        pass

    percentages = [percent/100 for percent in percentages]

    return percentages

def function_that_build_seed(icls):
    array = np.random.choice([4,5], 500, p=[0.5,0.5])
    #assert(array.shape[0] == (shape[0]*shape[1])), "parameters number do not match shape"
    array_shaped = array.reshape(25, 20)
    new_configuration = icls(array_shaped.tolist())
    return new_configuration

def function_that_builds_configuration(icls):
    assert(len(percentages_ranges)==nmaterials), "Number of materials and percentages ranges should be the same"
    instance_percentages = function_that_calculate_percentages(percentages_ranges)
    print("PERCENTAGES ARE ", instance_percentages)
    array = np.random.choice(nmaterials, parameters, p=instance_percentages)
    #assert(array.shape[0] == (shape[0]*shape[1])), "parameters number do not match shape"
    #array_shaped = array.reshape(shape[0], shape[1])
    new_configuration = icls(array.tolist())
    return new_configuration