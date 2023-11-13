import neat
import numpy as np
import config

nmaterials = config.nmaterials

categories = np.linspace(0,255, num=nmaterials)
categories = [int(x) for x in categories]
mapper = {v:i for i,v in enumerate(categories)}

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
            for i,value in enumerate(categories):
                if i == len(categories) - 1:
                    gray = 255
                elif pixel >= value and pixel < categories[i+1]:
                    gray = max(0, min(255, value))
                    break
            row.append(gray)
        image.append(row)

    return image

def decode_image_to_categories(image):
    for i, row in enumerate(image):
        for ii, column in enumerate(row):
            image[i][ii] = mapper[column]
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