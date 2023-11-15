import os


import os
import random
import shutil
from multiprocessing import Pool
import visualise

import numpy as np
from PIL import Image

import neat
from shared import eval_scale_image, decode_image_to_categories

from evaluation import function_that_batches
from dict_utils import save_dictionary_data_compress
import config


height, width = config.shape
full_scale = config.full_scale
MAX_BATCH = config.MAX_BATCH
parameters = config.parameters
GENERATIONS = config.GENERATIONS
experiment_path = config.experiment_path
name_process = config.name_process
barriers_dict = config.barriers_dict
backup_dict = config.backup_dict
evaluated = config.evaluated
dummy_dict_path = config.dummy_dict_path
backup_dict_path = config.backup_dict_path

# creating the folder structure for the batcher to work with the simulator, the number
# of folders depends on the MAX_BATCH which represent how many processes the system will 
# be able to run simultaneously

for batch_number in range(MAX_BATCH):
    shutil.rmtree(f"{experiment_path}/processes/{batch_number}", ignore_errors=True)
    os.mkdir(f"{experiment_path}/processes/{batch_number}")
    shutil.copyfile(f"{experiment_path}/{name_process}", f"{experiment_path}/processes/{batch_number}/{name_process}")

# evaluate_lowres() calls function to create new images

# wrapper function that accepts parameters required by NEAT and send them to
# eval_scale_image(), this create a genome/network and output a widthXheight array
# with value between 0 and 1 that gets converted in different shade of gray 
# depending how many materials the simulation is using 

def evaluate_lowres(genome, config):
    return eval_scale_image(genome, config, width, height)

class NoveltyEvaluator(object):
    def __init__(self, num_workers):
        self.num_workers = num_workers
        self.pool = Pool(num_workers)
        self.archive = []
        self.out_index = 1
    
    # visualise an image from an array
    def image_from_array(self, image):
        return Image.fromarray(image, mode="L")

    def evaluate(self, genomes, config):

        jobs = []
        # create this list of jobs/images for each genome_id, genome in genomes
        for genome_id, genome in genomes:
            jobs.append(self.pool.apply_async(evaluate_lowres, (genome, config)))

        # the population list is initialised, this get sent to the batcher
        # the batcher divide the population in batches and run the simulation
        population = []

        # for each genome the array drawn is flattened to be ready for the batcher
        for j in jobs:
            image = np.clip(np.array(j.get()), 0, 255).astype(np.uint8)
            image = decode_image_to_categories(image)
            float_image = image.astype(np.float32)
            array_ind = float_image.reshape(parameters)
            population.append(array_ind)
        
        # a list of fitnesses is returned
        fitnesses = function_that_batches(population, MAX_BATCH)

        new_archive_entries = []

        # for each genome, fitness is added
        for (genome_id, genome), j, fitness in zip(genomes, jobs, fitnesses):
            image = np.clip(np.array(j.get()), 0, 255).astype(np.uint8)
            float_image = image.astype(np.float32) / 255.0

            ### This is where the fitness for each genome gets evaluated

            genome.fitness = fitness[0]

            """
            Below is the original fitness evaluation, which calculate novelty of an image using
            this adist criteria, it has been substituted with the fitness calculate by the simulation
            """
            #genome.fitness = (width * height) ** 0.5
            #for a in self.archive:
            #    adist = np.linalg.norm(float_image.ravel() - a.ravel())
            #    genome.fitness = min(genome.fitness, adist)
            
            ### This is done in a for loop where each genome/image is evaluated (one at a time)

            # below only certain images are saved, in NEAT documentation they say not all images are saved to 
            # new_archive_entries to avoid memory issues, but the best genomes should be accessible 
            # from the reporter object

            if random.random() < 0.02:
                new_archive_entries.append(float_image)
                # im = self.image_from_array(image)
                # im.save("novelty-{0:06d}.png".format(self.out_index))


                image = eval_scale_image(genome, config, full_scale * width, full_scale * height)

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
    # Below is parsing the config file
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # Class built above on the same file, include the evaluate function
    # which append a fitness value calculated through a custom function 
    # to each genome

    # 1 represent the number of worker, a bug happens when more than one is used
    ne = NoveltyEvaluator(1)

    pop = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    
    pop.run(ne.evaluate,GENERATIONS)

    # this save the best genome of the whole population
    # this should be accessible in each generation
    # but from another module
     
    winner = stats.best_genome()

    image = eval_scale_image(winner, config, full_scale * width, full_scale * height)

    im = np.clip(np.array(image), 0, 255).astype(np.uint8)
    im = ne.image_from_array(im)
    im.save('winning-novelty-{0:06d}.png'.format(pop.generation))


    image = eval_scale_image(winner, config, width, height)
    float_image = np.array(image, dtype=np.float32) / 255.0
    ne.archive.append(float_image)

    # visualise statistics with max and average fitnesses 
    
    visualise.plot_stats(stats, ylog=False, view=True)

    try:
        shutil.copyfile(dummy_dict_path, backup_dict_path)
    except:
        pass
    save_dictionary_data_compress(barriers_dict, dummy_dict_path)

    with open('total-num-eval.txt', 'w') as f:
        f.write('%d' % len(evaluated))

    print(f"Added {len(backup_dict)} new configurations/fitness pair to dictionary")
    

if __name__ == '__main__':
    run()
