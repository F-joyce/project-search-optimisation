import unittest

from Data_wrangling_functions import get_new_barriers
from dict_utils import add_to_dictionary, get_fitness, add_to_dictionary_from_list

class create_barrier(unittest.TestCase):

    def test_new(self):
        barrier = get_new_barriers()
        self.assertEqual(barrier.shape, (450,), "Should be 450")

    #def test_sum_tuple(self):
    #ß    self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")
    
class adding_to_dictionary(unittest.TestCase):
    
    def setUp(self):
        self.dictionary = {}
        self.list_known_barriers = []
        self.list_new_barriers = []
        self.list_new_fitness = []
        for i in range(10):
            barr = get_new_barriers()
            self.list_known_barriers.append(barr)
            tup_k = tuple(barr)
            self.dictionary[tup_k] = i

        for i in range(10,20):
            barr = get_new_barriers()
            self.list_new_barriers.append(barr)
            self.list_new_fitness.append(i)
    
    def test_dict_size(self):
        self.assertEqual(len(self.dictionary), 10, "Test dictionary of wrong size")
        
    def test_add_new(self):
        add_to_dictionary(self.dictionary, self.list_new_barriers[0], self.list_new_fitness[0])
        self.assertEqual(len(self.dictionary), 11, "Test dictionary did not add new barrier")
        
    def test_add_old(self):
        add_to_dictionary(self.dictionary, self.list_known_barriers[0], 0)
        self.assertEqual(len(self.dictionary), 10, "Test dictionary did ADD an already known barrier")
        
    def test_get_fitness_array(self):
        to_check = self.list_known_barriers[5]
        fitness_expected = 5
        fitness_extracted = get_fitness(self.dictionary, to_check)
        self.assertEqual(fitness_expected, fitness_extracted, f"The fitness extracted was {fitness_extracted}, but expected was {fitness_expected}")
    
    def test_get_fitness_tuple(self):
        to_check = tuple(self.list_known_barriers[5])
        fitness_expected = 5
        fitness_extracted = get_fitness(self.dictionary, to_check)
        self.assertEqual(fitness_expected, fitness_extracted, f"The fitness extracted was {fitness_extracted}, but expected was {fitness_expected}")
    
    def test_get_fitness_not_there(self):
        to_check = self.list_new_barriers[5]
        expected = False
        extracted = get_fitness(self.dictionary, to_check)
        self.assertEqual(expected, extracted, f"The output was {extracted}, but expected was False")


    def test_add_from_list_new(self):
        add_to_dictionary_from_list(self.dictionary, self.list_new_barriers, self.list_new_fitness)
        self.assertEqual(len(self.dictionary), 20, "It did not added all new elements")
    
    def test_add_from_list_old(self):
        add_to_dictionary_from_list(self.dictionary, self.list_known_barriers, self.list_new_fitness)
        self.assertEqual(len(self.dictionary), 10, "It added known elements")
    
    def test_add_from_list_mix(self):
        mixed_list = self.list_new_barriers[:5] + self.list_known_barriers[5:]
        add_to_dictionary_from_list(self.dictionary, mixed_list, self.list_new_fitness)
        self.assertEqual(len(self.dictionary), 15, "It did not add all the new elements or added some of the old one")
        
if __name__ == '__main__':
    unittest.main()