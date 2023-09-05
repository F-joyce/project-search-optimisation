import os
import random
import shutil
import visualise
from multiprocessing import Pool

import numpy as np
from PIL import Image

import neat
from common import eval_mono_image, eval_gray_image, eval_color_image

from CNN_eaSimple import batch_fitness_simulation

width, height = 15, 30
full_scale = 1
MAX_BATCH = 10

path = os.getcwd()
for loopar in range(MAX_BATCH):
		shutil.rmtree(path+'/'+str(loopar), ignore_errors=True)
		os.mkdir(path+'/'+str(loopar))
		shutil.copyfile(path+'/supernova.py', path+'/'+str(loopar)+'/supernova.py')


# evaluate_lowres() calls function to create new images
def evaluate_lowres(genome, config, scheme):
    if scheme == 'gray':
        return eval_gray_image(genome, config, width, height)
    elif scheme == 'color':
        return eval_color_image(genome, config, width, height)
    elif scheme == 'mono':
        return eval_mono_image(genome, config, width, height)

    raise Exception('Unexpected scheme: {0!r}'.format(scheme))


class NoveltyEvaluator(object):
    def __init__(self, num_workers, scheme):
        self.num_workers = num_workers
        self.scheme = scheme
        self.pool = Pool(num_workers)
        self.archive = []
        self.out_index = 1
    
    # visualise an image from an array
    def image_from_array(self, image):
        if self.scheme == 'color':
            return Image.fromarray(image, mode="RGB")

        return Image.fromarray(image, mode="L")

    def evaluate(self, genomes, config):

        jobs = []
        # create this list of jobs/images for each genome_id, genome in genomes
        for genome_id, genome in genomes:
            jobs.append(self.pool.apply_async(evaluate_lowres, (genome, config, self.scheme)))

        population = []
        for j in jobs:
            image = np.clip(np.array(j.get()), 0, 255).astype(np.uint8)
            float_image = image.astype(np.float32) / 255.0
            array_ind = float_image.reshape(450)
            population.append(array_ind)
        
        fitnesses = batch_fitness_simulation(population, MAX_BATCH)

        new_archive_entries = []
        for (genome_id, genome), j, fitness in zip(genomes, jobs, fitnesses):
            image = np.clip(np.array(j.get()), 0, 255).astype(np.uint8)
            float_image = image.astype(np.float32) / 255.0

            ### This is where the fitness for each genome gets evaluated

            genome.fitness = fitness[0]
            #genome.fitness = (width * height) ** 0.5
            #for a in self.archive:
            #    adist = np.linalg.norm(float_image.ravel() - a.ravel())
            #    genome.fitness = min(genome.fitness, adist)
            
            ### This is done in a for loop where each genome/image is evaluated (one at a time)

            if random.random() < 0.02:
                new_archive_entries.append(float_image)
                # im = self.image_from_array(image)
                # im.save("novelty-{0:06d}.png".format(self.out_index))

                if self.scheme == 'gray':
                    image = eval_gray_image(genome, config, full_scale * width, full_scale * height)
                elif self.scheme == 'color':
                    image = eval_color_image(genome, config, full_scale * width, full_scale * height)
                elif self.scheme == 'mono':
                    image = eval_mono_image(genome, config, full_scale * width, full_scale * height)
                else:
                    raise Exception('Unexpected scheme: {0!r}'.format(self.scheme))

                im = np.clip(np.array(image), 0, 255).astype(np.uint8)
                im = self.image_from_array(im)
                im.save('novelty-{0:06d}.png'.format(self.out_index))

                self.out_index += 1

        self.archive.extend(new_archive_entries)
        print('{0} archive entries'.format(len(self.archive)))


def run():
    # Determine path to configuration file.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'novelty_config')
    # Note that we provide the custom stagnation class to the Config constructor.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    ne = NoveltyEvaluator(1, 'mono')
    if ne.scheme == 'color':
        config.output_nodes = 3
    else:
        config.output_nodes = 1

    pop = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    checkpoint = neat.Checkpointer()
    pop.add_reporter(checkpoint)

    while 1:
        pop.run(ne.evaluate, 50)

        winner = stats.best_genome()
        if ne.scheme == 'gray':
            image = eval_gray_image(winner, config, full_scale * width, full_scale * height)
        elif ne.scheme == 'color':
            image = eval_color_image(winner, config, full_scale * width, full_scale * height)
        elif ne.scheme == 'mono':
            image = eval_mono_image(winner, config, full_scale * width, full_scale * height)
        else:
            raise Exception('Unexpected scheme: {0!r}'.format(ne.scheme))

        im = np.clip(np.array(image), 0, 255).astype(np.uint8)
        im = ne.image_from_array(im)
        im.save('winning-novelty-{0:06d}.png'.format(pop.generation))

        if ne.scheme == 'gray':
            image = eval_gray_image(winner, config, width, height)
        elif ne.scheme == 'color':
            image = eval_color_image(winner, config, width, height)
        elif ne.scheme == 'mono':
            image = eval_mono_image(winner, config, width, height)
        else:
            raise Exception('Unexpected scheme: {0!r}'.format(ne.scheme))

        float_image = np.array(image, dtype=np.float32) / 255.0
        ne.archive.append(float_image)
        stats.save()

        visualize.plot_stats(stats, ylog=False, view=True)
        visualize.plot_species(stats, view=True)
        


if __name__ == '__main__':
    run()
