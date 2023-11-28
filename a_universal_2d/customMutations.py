import random
import config

nmaterials = config.nmaterials

######################################
# GA Custom Mutation                 #
######################################

def mutFlipBitCustom(individual, indpb):
    """Flip the value of the attributes of the input individual and return the
    mutant. The *individual* is expected to be a :term:`sequence` and the values of the
    attributes shall stay valid after the ``not`` operator is called on them.
    The *indpb* argument is the probability of each attribute to be
    flipped. This mutation is usually applied on boolean individuals.

    :param individual: Individual to be mutated.
    :param indpb: Independent probability for each attribute to be flipped.
    :returns: A tuple of one individual.

    This function uses the :func:`~random.random` function from the python base
    :mod:`random` module.
    """
    for i in range(len(individual)):
        if random.random() < indpb:
            individual[i] = type(individual[i])(not individual[i])

    individual[450:455] = [1,1,1,1,1]

    return individual,

def mutSwapMaterialCustom(individual, indpb):
    """Flip the value of the attributes of the input individual and return the
    mutant. The *individual* is expected to be a :term:`sequence` and the values of the
    attributes shall stay valid after the ``not`` operator is called on them.
    The *indpb* argument is the probability of each attribute to be
    flipped. This mutation is usually applied on boolean individuals.

    :param individual: Individual to be mutated.
    :param indpb: Independent probability for each attribute to be flipped.
    :returns: A tuple of one individual.

    This function uses the :func:`~random.random` function from the python base
    :mod:`random` module.
    """
    list_ = [x for x in range(nmaterials)]
    for i in range(len(individual)):
        try:
            for ii in range(len(individual[i])):
                if random.random() < indpb:
                    temp_list = list_.copy()
                    temp_list.remove(individual[i][ii])
                    individual[i][ii] = random.choice(temp_list)
        except TypeError: # avoid two-dimensional iteration for flattened arrays
            if random.random() < indpb:
                    temp_list = list_.copy()
                    temp_list.remove(individual[i])
                    individual[i] = random.choice(temp_list)

    return individual,