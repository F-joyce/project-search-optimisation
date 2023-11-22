import neat
import numpy as np
import config

nmaterials = config.nmaterials



row_bias = -2
column_bias = -2

categories_array = np.linspace(0,1, num=nmaterials)
mapper_material_to_pixel = {i:int(v) for i,v in enumerate(np.linspace(0,255, num=nmaterials))}


def create_array_configuration(genome, config, width, height, nmaterials=nmaterials):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    configuration = []
    for row_index in range(height):
        y = row_bias + 4 * row_index / (height-1)
        row_values = []
        for column_index in range(width):
            x = column_bias + 4 * column_index / (width-1)
            
            output = net.activate([x,y])
            network_output = output[0]
            for index,value in enumerate(categories_array):
                if index == (len(categories_array)-1):
                    cell_value = nmaterials-1
                elif network_output >= value and network_output < categories_array[index+1]:
                    cell_value = index
                    break
            row_values.append(cell_value)
        configuration.append(row_values)

    return configuration

def encode_array_to_image(array):
    array = np.asarray(array, dtype=np.int16)
    image = np.vectorize(mapper_material_to_pixel.__getitem__)(array)
    return image

def encode_array_to_image_loop(array):
    for row in range(len(array)):
        for cell in range(len(array[row])):
            array[row][cell] = mapper_material_to_pixel[array[row][cell]]
    return array