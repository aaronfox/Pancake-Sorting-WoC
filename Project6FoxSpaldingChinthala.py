# Project 6
# Aaron Fox, Abby Spalding, Sai Chinthala
# CECS 545-01
# Dr. Yampolskiy

import math # Need math for math.ceil for indices size (ceil)
import random # Needed for random.shuffle for indices

# Chromosome is the indices of the pancakes that can be flipped
# Each population contains population_size amount of the chromosomes
# INPUT:
# original_unordered_string:
# population_size:
#
class genetic_pancake_algorithm:
    def __init__(self, original_unordered_string, population_size, number_of_generations, mutation_probability, crossover_probability):
        self.original_unordered_string = original_unordered_string
        self.initial_population = []
        # self.

        # Max number of indices required is found by 18*n / 11 according to Chittri 
        self.indices_chromosome_size = math.ceil(18 * len(self.original_unordered_string) / 11)

        # Generate list of all possible indices that can be included in chromosome
        # Exclude 0 because a flip of 0 would simply flip the first char in the string and would
        # be pointless
        self.all_possible_indices = list(range(1, len(self.original_unordered_string)))


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

            # Place chromosome into population
            self.initial_population.append()

            print("chromosome == " + str(chromosome))
            print("cost of chromosome == " + str(self.evaluate_cost(chromosome)))

    # Returns the "cost" of a chromosome by applying flips to the unordered string, finding the "fitness" of that string,
    # and then finding the inverse of that fitness as the cost
    # INPUT: chromosome: the chromosome of indices to apply to the unordered string
    # OUTPUT: the float cost value, between (0.0, 1]

    def evaluate_cost(self, chromosome):
        # First, apply all flips from indices to copy of original string
        temp_string_array = self.original_unordered_string.copy()
        for i in range(len(chromosome)):
            temp_string_array = self.flip_prefix(temp_string_array, chromosome[i])

        
        # Then find number of subarrays in string and the length of those subarrays
        # and find the fitness of a function by multiplying the number of subarrays of a certain length
        # by that certain length and adding them all together.
        # e.g. if we have 3 subarrays of length 4 and 5 subsequences of length 2,
        # the fitness of the function would 3(4) + 5(2) = 22
        sorted_string = sorted(self.original_unordered_string)

        # Find subsequences by creating two for loops to find the number of subarrays (contiguous arrays)
        subarray_length_and_occurrences = self.find_sub_arrays_length_and_occ(sorted_string, temp_string_array)

        # Find cost by finding the inverse of the result of multiplying all subarray lengths with their occurrences
        fitness = 0
        for length, occurrences in subarray_length_and_occurrences.items():
            fitness = fitness + length * occurrences

        # Make cost just inverse of the fitness
        if fitness == 0: # Make sure fitness isn't zero to avoid divide by zero exception
            return 1
        else:
            cost = 1 / fitness

        return cost


    # Flips string array from 0 to index (where 0 is) 
    # INPUT: string: the string array to have a prefix flipped
    #        index: the index for the prefix of the char array to be flipped
    # OUTPUT: a new char array representing the string with its prefix flipped with the remaining unflipped postfix at the end
    def flip_prefix(self, string, index):
        prefix_string = string[:index + 1]
        prefix_string.reverse()
        return prefix_string + string[index + 1:] 

    # Returns a dict of the form {subarray_length: number_of_occurrences}
    # e.g. if we have 3 subarrays of length 4 and 5 subsequences of length 2, the output would be {4: 3, 2: 5}
    # INPUT: ordered_string: the correctly ordered version of the chromosome_string
    #        chromosome_string: the resulting chromosome string after applying the flip indices
    def find_sub_arrays_length_and_occ(self, ordered_string, chromosome_string):
        # Store each char with its corresponding "value" into dict. E.g. for ordered
        # string of {'a', 'f', 'j'}, the dict would be {'a': 0, 'f': 1, 'j': 2}
        string_with_value_dict = {}
        # Value to store with each char
        char_value = 0
        # Assign each sorted char in ordered string array a value
        for i in range(len(ordered_string)):
            if ordered_string[i] not in string_with_value_dict:
                string_with_value_dict[ordered_string[i]] = char_value
                char_value = char_value + 1

        # Create dictionary of subarray sizes and their number of occurrences.
        # E.g. for string_with_value_dict of {'a': 0, 'f': 1, 'j': 2, 'z': 3} and
        # a chromosome_string of ['a', 'f', 'j', 'a', 'f', 'j', 'z', 'a', 'f', 'z', 'j', 'a', 'a'], the subarray_and_occurrences_dict
        # would be {2: 3, 3: 1, 4: 1}, because {'a', 'f'}, {'a', 'a'}, {'z', 'j'}, and {'z', 'j'} are three subarrays of length 2,
        # {'a', 'f', 'j'} is one subarray of length 3, and {'a', 'f', 'j', 'z'} is one subarray of length 4
        subarray_and_occurrences_dict = {} 
        
        # TODO: REMOVE THIS it's for testing
        # Chromosome String tests
        # string_with_value_dict = {'a': 0, 'f': 1, 'j': 2, 'z': 3}
        # string_with_value_dict = {'1': 0, '2': 1, '3': 2, '4': 3}
        # chromosome_string = ['a', 'f', 'j', 'a', 'f', 'j', 'z', 'a', 'f', 'z', 'j', 'a', 'a']
        # tests on 
        # chromosome_string = ['z', 'j', 'a', 'a', 'f', 'j', 'z', 'z', 'j', 'f', 'a'] {6: 1, 5: 1, 2: 1}
        # chromosome_string = ['a', 'f', 'j', 'f', 'a', 'a', 'f', 'a']# 'j', 'z', 'a', 'f', 'z', 'j', 'a', 'a'] {3: 1, 2: 2, 4:1}
        # chromosome_string = ['2', '1', '1', '1', '2', '2', '4', '4']
        # chromosome_string = ['1', '2', '3', '2', '1', '1', '2', '1']
        # chromosome_string = ['4', '2', '1', '1', '1', '2', '4', '2']#, '4', '4']
        # chromosome_string = ['1', '4', '2', '3', '2', '2', '2', '1']#, #, '2']#, '4', '4'] DONE: Make sure this works
        # chromosome_string = ['2', '2', '2', '1'] # DONE: Make sure this yields {3: 1, 4: 1}

        # END testing TODO
        index = 0
        current_subarray_length = 1
        # First while loop: just check for subarrays like ['a', 'f'] and ['a', 'a'] above (NOT for ['z', 'j'] yet)
        while index != len(chromosome_string) - 1:
            if string_with_value_dict[chromosome_string[index]] == string_with_value_dict[chromosome_string[index + 1]] or string_with_value_dict[chromosome_string[index]] + 1 == string_with_value_dict[chromosome_string[index + 1]]:
                current_subarray_length = current_subarray_length + 1
            else:
                if current_subarray_length > 1:
                    if current_subarray_length not in subarray_and_occurrences_dict:
                        subarray_and_occurrences_dict[current_subarray_length] = 1
                    else:
                        subarray_and_occurrences_dict[current_subarray_length] = subarray_and_occurrences_dict[current_subarray_length] + 1

                current_subarray_length = 1
            index = index + 1
        
        # Account for if current subarray was at end
        if current_subarray_length > 1:
            if current_subarray_length not in subarray_and_occurrences_dict:
                subarray_and_occurrences_dict[current_subarray_length] = 1
            else:
                subarray_and_occurrences_dict[current_subarray_length] = subarray_and_occurrences_dict[current_subarray_length] + 1

        # Reset current_subarray_length for second while loop
        current_subarray_length = 1

        # Check for same letter too to avoid counting it twice
        current_subarray_length_same_letter = 1

        # Second while loop: just check for subarrays like ['z', 'j'] = subarray of length 2 and ['z', 'j', 'j'] = subarray of length 3 above (NOT for ['a', 'f'] and ['a', 'a'] yet)
        index = len(chromosome_string) - 1
        while index != 0:
            if string_with_value_dict[chromosome_string[index]] + 1 == string_with_value_dict[chromosome_string[index - 1]]:
                current_subarray_length = current_subarray_length + 1
            # Account for subarrays of same letters to add in with overall subarray, but don't add to main subarray length on its own like in first while
            # loop to avoid counting for double array twice
            elif string_with_value_dict[chromosome_string[index]] == string_with_value_dict[chromosome_string[index - 1]]:
                current_subarray_length_same_letter = current_subarray_length_same_letter + 1
            else:
                if current_subarray_length > 1:
                    if current_subarray_length_same_letter > 1:
                        if current_subarray_length + current_subarray_length_same_letter - 1 not in subarray_and_occurrences_dict:
                            subarray_and_occurrences_dict[current_subarray_length + current_subarray_length_same_letter] = 1
                        else:
                            subarray_and_occurrences_dict[current_subarray_length + current_subarray_length_same_letter - 1] = subarray_and_occurrences_dict[current_subarray_length + current_subarray_length_same_letter - 1] + 1
                    else:
                        if current_subarray_length not in subarray_and_occurrences_dict:
                            subarray_and_occurrences_dict[current_subarray_length] = 1
                        else:
                            subarray_and_occurrences_dict[current_subarray_length] = subarray_and_occurrences_dict[current_subarray_length] + 1

                current_subarray_length = 1
                current_subarray_length_same_letter = 1

            index = index - 1

        # TODO: Account for case where ['1', '1', '2', '1', '1'] i.e. where same letters are found at beginning/end of processed string
        # Account for if current subarray was at end
        if current_subarray_length > 1:
            if current_subarray_length_same_letter > 1:
                if current_subarray_length + current_subarray_length_same_letter not in subarray_and_occurrences_dict:
                    subarray_and_occurrences_dict[current_subarray_length + current_subarray_length_same_letter] = 1
                else:
                    subarray_and_occurrences_dict[current_subarray_length + current_subarray_length_same_letter] = subarray_and_occurrences_dict[current_subarray_length + current_subarray_length_same_letter] + 1
            else:
                if current_subarray_length not in subarray_and_occurrences_dict:
                    subarray_and_occurrences_dict[current_subarray_length] = 1
                else:
                    subarray_and_occurrences_dict[current_subarray_length] = subarray_and_occurrences_dict[current_subarray_length] + 1


        return subarray_and_occurrences_dict


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

    # string_array = read_string(r'string_10.string')
    string_array = read_string(r'string_5.string')

    print("string_array == " + str(string_array))

    ga = genetic_pancake_algorithm(original_unordered_string=string_array, population_size=3, number_of_generations=10, mutation_probability=1.0, crossover_probability=1.0)









