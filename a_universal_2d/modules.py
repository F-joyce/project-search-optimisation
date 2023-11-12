def function_that_builds_configuration(icls):
    assert(len(percentages_ranges)==nmaterials), "Number of materials and percentages ranges should be the same"
    instance_percentages = function_that_calculate_percentages(percentages_ranges)
    print("PERCENTAGES ARE ", instance_percentages)
    array = np.random.choice(nmaterials, parameters, p=instance_percentages)
    #assert(array.shape[0] == (shape[0]*shape[1])), "parameters number do not match shape"
    array_shaped = array.reshape(shape[0], shape[1])
    new_configuration = icls(array_shaped.tolist())
    return new_configuration

def function_that_builds_configuration_global(icls):
    global percentages_ranges
    global nmaterials
    global parameters
    global shape
    assert(len(percentages_ranges)==nmaterials), "Number of materials and percentages ranges should be the same"
    instance_percentages = function_that_calculate_percentages(percentages_ranges)
    print("PERCENTAGES ARE ", instance_percentages)
    array = np.random.choice(nmaterials, parameters, p=instance_percentages)
    #assert(array.shape[0] == (shape[0]*shape[1])), "parameters number do not match shape"
    array_shaped = array.reshape(shape[0], shape[1])
    new_configuration = icls(array_shaped.tolist())
    return new_configuration