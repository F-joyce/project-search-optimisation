import numpy as np
from random import random as chance


def get_configuration(tuple_, shape=(30,15)):
    """get a configuration in tuple format and transform it in 
       one array of selected shape, default is (30,15)"""
    array_form = np.array(tuple_)
    configuration = array_form.reshape(shape[0], shape[1])
    return configuration


def extract_configurations_and_fitness(dictionary, shape_=(30,15)):
    '''gets all the configurations and fitnesses from a dictionary and save
       them in two lists, such as at list_fitnesses[n] there is the fitness 
       for list_configurations[n]'''
    list_configurations = []
    list_fitnesses = []
    for k,v in dictionary.items():
        conf_ = get_configuration(k, shape_)
        fitness_ = v
        list_configurations.append(conf_)
        list_fitnesses.append(fitness_)    
    return list_configurations, list_fitnesses

def extract_unseen_configurations_and_fitness(dictionary_used,new_dictionary, shape_=(30,15)):
    '''gets all the configurations and fitnesses from a dictionary and save
       them in two lists, such as at list_fitnesses[n] there is the fitness 
       for list_configurations[n]'''
    list_configurations = []
    list_fitnesses = []
    for k,v in new_dictionary.items():
        if k not in dictionary_used.keys():
            conf_ = get_configuration(k, shape_)
            fitness_ = v
            list_configurations.append(conf_)
            list_fitnesses.append(fitness_)    
    return list_configurations, list_fitnesses


def load_data_train_test_first_version(dictionary, split = (80,20), shape_=(30,15)):
    list_full_x,list_full_y = extract_configurations_and_fitness(dictionary, 
                                                                shape_)
    for index in range(len(train_list_x)):
        pass
    for index in range(len(test_list_x)):
        pass
    threshold_index = int(len(list_full_x)/100*split[0])
    train_list_x = list_full_x[:threshold_index]
    test_list_x = list_full_x[threshold_index:]
    train_list_y = np.array(list_full_y[:threshold_index])
    test_list_y = np.array(list_full_y[threshold_index:])
    return (train_list_x,train_list_y),(test_list_x,test_list_y)


def load_data_train_test(dictionary, split = (80,20), shape_=(30,15)):
    """From a dictionary where keys are tuples of binary strings, and values
       are the fitnesses computed for such tuples/individuals, return a 
       splitted dataset where each individual gets shaped in an array of
       shape <shape_>, returns a training set of x,y and a validation set"""
    list_full_x,list_full_y = extract_configurations_and_fitness(dictionary, 
                                                                shape_)
    train_list_x = []
    train_list_y = []
    test_list_x = []
    test_list_y = []
    for index in range(len(list_full_x)):
        if chance() < split[0]/100:
            train_list_x.append(list_full_x[index])
            train_list_y.append(list_full_y[index])
        else:
            test_list_x.append(list_full_x[index])
            test_list_y.append(list_full_y[index])
    assert len(train_list_x) == len(train_list_y),\
                                 "Train fitness do not correspond"
    assert len(test_list_x) == len(test_list_y),\
                                  "Test fitness do not correspond"
    assert (len(train_list_x)+len(test_list_x))==len(list_full_x),\
                                "Some item has not been extracted"
    return (train_list_x,train_list_y),(test_list_x,test_list_y)

def load_new_test(dictionary_seen,dictionary_unseen, shape_=(30,15)):
    """From a dictionary where keys are tuples of binary strings, and values
       are the fitnesses computed for such tuples/individuals, return a 
       splitted dataset where each individual gets shaped in an array of
       shape <shape_>, returns a training set of x,y and a validation set"""
    list_full_x,list_full_y = extract_unseen_configurations_and_fitness(
                                dictionary_seen,dictionary_unseen,shape_)
    X_new = preprocess_shape(list_full_x)
    y_new = np.array(list_full_y)
    return X_new,y_new


def preprocess_shape(training_list):
    """takes a list of arrays cast it as numpy ndarray of arrays, add a
       channel parameter and cast values to float32 to the array of arrays
       for compatibility with keras"""
    train_no_extra_channel = np.array(training_list)
    original_shape = list(train_no_extra_channel.shape)
    original_shape.append(1)
    keras_shape = tuple(original_shape)
    train_w_extra_channel = train_no_extra_channel.reshape(keras_shape).astype('float32')
    return train_w_extra_channel


def normalise(array, maximum, minimum):
    dividend = maximum-minimum
    normalised = (array-minimum)/dividend
    return normalised
def denormalise(array, maximum, minimum):
    multiplier = maximum-minimum
    actual_value = (array*multiplier) + minimum
    return actual_value


def load_train_test(data, split=(80,20), shape_=(30,15)):
    (X_train,y_train),(X_test,y_test) = load_data_train_test(data,split,shape_)
    print(f"There are {len(X_train)} samples in the training dataset")
    y_train = np.array(y_train)
    y_test = np.array(y_test)
    X_train = preprocess_shape(X_train)
    X_test = preprocess_shape(X_test)
    return (X_train,y_train),(X_test,y_test)