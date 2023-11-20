import neat
import numpy as np
import config

nmaterials = config.nmaterials

categories_image = np.linspace(0,255, num=nmaterials)
categories_image = [int(x) for x in categories_image]
mapper_image_to_material = {v:i for i,v in enumerate(categories_image)}

categories_array = np.linspace(0,1, num=nmaterials)

row_bias = -2
column_bias = -2

def create_array_configuration(genome, config, width, height, nmaterials=nmaterials):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    configuration = []
    for row_index in range(height):
        y = row_bias + ((4*row_index)/(height-1))
        row_values = []
        for column_index in range(width):
            x = column_bias + ((4*column_index)/(width-1))
            
            output = net.activate([x,y])
            for index,value in enumerate(categories_array):
                if index == (len(categories_array)-1):
                    cell_value = nmaterials-1
                elif output[0] >= value and output[0] < categories_array[index+1]:
                    cell_value = index
                    break
            row_values.append(cell_value)
        configuration.append(row_values)

    return configuration

def eval_scale_image(genome, config, width, height, nmaterials=nmaterials):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    image = []
    for r in range(height):
        y = -2.0 + 4.0 * r / (height - 1)
        row = []
        for c in range(width):
            x = -2.0 + 4.0 * c / (width - 1)
            output = net.activate([x, y])
            pixel = int(round((output[0] + 1.0) * 255 / 2.0))
            for i,value in enumerate(categories_image):
                if i == len(categories_image) - 1:
                    gray = 255
                elif pixel >= value and pixel < categories_image[i+1]:
                    gray = max(0, min(255, value))
                    break
            row.append(gray)
        image.append(row)

    return image

def decode_image_to_categories(image):
    for i, row in enumerate(image):
        for ii, column in enumerate(row):
            image[i][ii] = mapper_image_to_material[column]
    return image

def encode_array_to_image(array):
    array = np.asarray(array, dtype=np.int16)
    image = np.vectorize(categories_image.__getitem__)(array)
    print(image)
    return image

# Original mono function
def eval_mono_image(genome, config, width, height):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    image = []
    for r in range(height):
        y = -2.0 + 4.0 * r / (height - 1)
        row = []
        for c in range(width):
            x = -2.0 + 4.0 * c / (width - 1)
            output = net.activate([x, y])
            gray = 255 if output[0] > 0.0 else 0
            row.append(gray)
        image.append(row)

    return image