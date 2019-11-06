# Project 6
# Aaron Fox, Abby Spalding, Sai Chinthala
# CECS 545-01
# Dr. Yampolskiy

import math # Need math for math.ceil for indices size (ceil)
import random # Needed for random.shuffle for indices

# Chromosome is the indices of the pancakes that can be flipped
# Each population contains population_size amount of the chromosomes
class genetic_pancake_algorithm:
    def __init__(self, original_unordered_string, population_size):
        self.original_unordered_string = original_unordered_string
        self.initial_population = []
        # self.

        # Max number of indices required is found by 18*n / 11 according to Chittri 
        self.indices_chromosome_size = math.ceil(18 * len(self.original_unordered_string) / 11)
        print("indices_chromosome_size == " + str(self.indices_chromosome_size))

        # Generate list of all possible indices that can be included in chromosome
        self.all_possible_indices = list(range(0, len(self.original_unordered_string)))


        # Create number of initial chromosomes in population as specified by population_size
        for i in range(population_size):
            # For each chromosome, place every possible index to flip for the first n, then fill remaining
            # spots with any number within the bounds of indices

            # Add all possible indices to flip for beginning n of 18n/11 indices
            chromosome = random.sample(self.all_possible_indices, len(self.all_possible_indices))

            # Add in remaining indices randomly until 18n/11 indices are in chromosome
            while len(chromosome) != self.indices_chromosome_size:
                chromosome.extend(random.sample(self.all_possible_indices, 1))

            # Shuffle once more to ensure randomness
            chromosome = random.sample(chromosome, len(chromosome))

            print("chromosome == " + str(chromosome))
            print("cost of chromosome == " + str(self.evaluate_cost(chromosome)))


    def evaluate_cost(self, chromosome):
        return 0
        # First, apply all flips from indices to original string

        # Then find number of subsequences in string and the length of those subsequences
        # and find the fitness of a function by multiplying the number of subsequences of a certain length
        # by that certain length and adding them all together.
        # e.g. if we have 3 subsequences of length 4 and 5 subsequences of length 2,
        # the fitness of the function would 3(4) + 5(2) = 22



# Reads in .string files made to be sorted using the pancake sorting algorithm
# INPUT: a filepath to the location of the string file
# OUTPUT: a char array of each letter of the strings
def read_string(string_filepath):
    string_file = open(string_filepath, 'r')
    string_array = []
    for char in string_file:
        string_array.append(char[0])
    
    return string_array


if __name__ == "__main__":
    print("Starting up Project6FoxSpaldingChinthala.py")

    string_array = read_string(r'string_10.string')

    print("string_array == " + str(string_array))

    ga = genetic_pancake_algorithm(string_array, 3)









