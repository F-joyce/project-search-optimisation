import neat
import numpy as np

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

def eval_scale_image(genome, config, width, height, nmaterials=6):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    image = []
    categories = np.linspace(0,255, num=nmaterials)
    categories = [int(x) for x in categories]
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


def eval_gray_image(genome, config, width, height):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    image = []
    for r in range(height):
        y = -1.0 + 2.0 * r / (height - 1)
        row = []
        for c in range(width):
            x = -1.0 + 2.0 * c / (width - 1)
            output = net.activate([x, y])
            gray = int(round((output[0] + 1.0) * 255 / 2.0))
            gray = max(0, min(255, gray))
            row.append(gray)
        image.append(row)

    return image


def eval_color_image(genome, config, width, height):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    image = []
    for r in range(height):
        y = -1.0 + 2.0 * r / (height - 1)
        row = []
        for c in range(width):
            x = -1.0 + 2.0 * c / (width - 1)
            output = net.activate([x, y])
            red = int(round((output[0] + 1.0) * 255 / 2.0))
            green = int(round((output[1] + 1.0) * 255 / 2.0))
            blue = int(round((output[2] + 1.0) * 255 / 2.0))
            red = max(0, min(255, red))
            green = max(0, min(255, green))
            blue = max(0, min(255, blue))
            row.append((red, green, blue))
        image.append(row)

    return image
