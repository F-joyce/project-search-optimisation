import pickle
import gzip
import pandas
import numpy as np

class DataRun(object):
    def __init__(self, name):
        self.name = name
        self.generation = 0
        self.data = {}
    
    def increaseGen(self):
        self.generation += 1
        self.NewGen()
    
    def NewGen(self):
        self.temp_high_f = None
        self.temp_low_f = None
        self.temp_conf_h = None
        self.temp_conf_l = None
        self.full_fitness = []

    def updateHighLow(self, fitness, config):
        self.full_fitness.append(fitness)

        if self.temp_high_f is None:
            self.temp_high_f = fitness
            self.temp_conf_h = config
            self.temp_low_f = fitness
            self.temp_conf_l = config

        elif self.temp_high_f < fitness:
            self.temp_high_f = fitness
            self.temp_conf_h = config

        elif self.temp_low_f > fitness:
            self.temp_low_f = fitness
            self.temp_conf_l = config
        
    def saveGeneration(self, evaluations):

        data = {"generation":self.generation, "avg_fit": np.average(self.full_fitness),
                 "high_fit": self.temp_high_f, "high_conf": self.temp_conf_h,
                 "low_fit": self.temp_low_f, "low_conf": self.temp_conf_l,  
                 "unique_eval": evaluations}
        self.data[self.generation] = data
    
    def saveData(self):
        with gzip.open(self.name, 'w', compresslevel=1) as file:
            pickle.dump(self.data, file, protocol=pickle.HIGHEST_PROTOCOL)

    def saveDataCsv(self):
        df = pandas.DataFrame.from_dict(self.data, orient="index") #, columns= [column for column in self.data[1].keys()], )
        df.to_csv(f"{self.name}.csv")