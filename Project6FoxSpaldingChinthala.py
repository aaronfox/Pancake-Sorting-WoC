# Project 6
# Aaron Fox, Abby Spalding, Sai Chinthala
# CECS 545-01
# Dr. Yampolskiy

import math # Need math for math.ceil for indices size (ceil)

class genetic_pancake_algorithm:
    def __init__(self, original_unordered_string, population_size):
        self.original_unordered_string = original_unordered_string
        self.initial_population = []
        # self.

        # Max number of indices required is found by 18*n / 11 according to Chittri 
        indices_chromosome_size = math.ceil(18 * len(self.original_unordered_string) / 11)
        print("indices_chromosome_size == " + str(indices_chromosome_size))

        # For initial population, place every possible index to flip for the first n, then fill remaining
        # spots with any number within the bounds of indices


        # Generate list of all possible indices that can be included in chromosome
        self.all_possible_indices = list(range(0, len(self.original_unordered_string)))

        # Create number of initial populations as specified by population_size
        for i in range(population_size):
            self.


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









