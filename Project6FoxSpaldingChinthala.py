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
    def __init__(self, original_unordered_string, population_size):
        self.original_unordered_string = original_unordered_string
        self.initial_population = []
        # self.

        # Max number of indices required is found by 18*n / 11 according to Chittri 
        self.indices_chromosome_size = math.ceil(18 * len(self.original_unordered_string) / 11)
        print("indices_chromosome_size == " + str(self.indices_chromosome_size))

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

            print("chromosome == " + str(chromosome))
            print("cost of chromosome == " + str(self.evaluate_cost(chromosome)))


    def evaluate_cost(self, chromosome):
        # First, apply all flips from indices to original string
        temp_string_array = self.original_unordered_string.copy()


        print("Initially, temp_string_array == " + str(temp_string_array))
        for i in range(len(chromosome)):
            temp_string_array = self.flip_prefix(temp_string_array, chromosome[i])
            # print("flipping at chromosome[i] == " + str(chromosome[i]) + " yields string of " + str(temp_string_array))

        
        print("After, temp_string_array == " + str(temp_string_array))


        # Then find number of subsequences in string and the length of those subsequences
        # and find the fitness of a function by multiplying the number of subsequences of a certain length
        # by that certain length and adding them all together.
        # e.g. if we have 3 subsequences of length 4 and 5 subsequences of length 2,
        # the fitness of the function would 3(4) + 5(2) = 22

        sorted_string = sorted(self.original_unordered_string)
        print("sorted_string == " + str(sorted_string))

        subarray_length_and_occurences = []
        # Find subsequences by creating two for loops to find the number of subarrays (contiguous arrays)
        self.find_sub_arrays(sorted_string, temp_string_array, chromosome)

        return 0


    # Flips string array from 0 to index (where 0 is) 
    # INPUT: string: the string array to have a prefix flipped
    #        index: the index for the prefix of the char array to be flipped
    # OUTPUT: a new char array representing the string with its prefix flipped with the remaining unflipped postfix at the end
    def flip_prefix(self, string, index):
        prefix_string = string[:index + 1]
        prefix_string.reverse()
        return prefix_string + string[index + 1:] 

    def find_sub_arrays(self, ordered_string, chromosome_string, chromosome):
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

        print("string_with_value_dict == " + str(string_with_value_dict))
        print("chromosome_string == " + str(chromosome_string))

        # Create dictionary of subarray sizes and their number of occurences.
        # E.g. for string_with_value_dict of {'a': 0, 'f': 1, 'j': 2, 'z': 3} and
        # a chromosome_string of ['a', 'f', 'j', 'a', 'f', 'j', 'z', 'a', 'f', 'z', 'j', 'a', 'a'], the subarray_and_occurences_dict
        # would be {2: 3, 3: 1, 4: 1}, because {'a', 'f'}, {'a', 'a'}, {'z', 'j'}, and {'z', 'j'} are three subarrays of length 2,
        # {'a', 'f', 'j'} is one subarray of length 3, and {'a', 'f', 'j', 'z'} is one subarray of length 4
        subarray_and_occurences_dict = {} 
        
        # TODO: REMOVE THIS it's for testing
        string_with_value_dict = {'a': 0, 'f': 1, 'j': 2, 'z': 3}
        # string_with_value_dict = {'1': 0, '2': 1, '3': 2, '4': 3}
        chromosome_string = ['a', 'f', 'j', 'a', 'f', 'j', 'z', 'a', 'f', 'z', 'j', 'a', 'a']
        chromosome_string = ['a', 'f', 'j', 'f', 'a', 'a', 'f', 'a']# 'j', 'z', 'a', 'f', 'z', 'j', 'a', 'a']
        # chromosome_string = ['2', '1', '1', '1', '2', '2', '4', '4']

        print("\n\n=================\n\nNEW string_with_value_dict == " + str(string_with_value_dict))
        print("NEW chromosome_string == " + str(chromosome_string))
        # END TODO
        index = 0
        current_subarray_length = 1
        # First while loop: just check for subarrays like ['a', 'f'] and ['a', 'a'] above (NOT for ['z', 'j'] yet)
        while index != len(chromosome_string) - 1:
            if string_with_value_dict[chromosome_string[index]] == string_with_value_dict[chromosome_string[index + 1]] or string_with_value_dict[chromosome_string[index]] + 1 == string_with_value_dict[chromosome_string[index + 1]]:
                current_subarray_length = current_subarray_length + 1
            else:
                if current_subarray_length > 1:
                    if current_subarray_length not in subarray_and_occurences_dict:
                        subarray_and_occurences_dict[current_subarray_length] = 1
                    else:
                        subarray_and_occurences_dict[current_subarray_length] = subarray_and_occurences_dict[current_subarray_length] + 1

                current_subarray_length = 1
            index = index + 1
        
        # Account for if current subarray was at end
        if current_subarray_length > 1:
            if current_subarray_length not in subarray_and_occurences_dict:
                subarray_and_occurences_dict[current_subarray_length] = 1
                print("!!!AT END Updating subarray_and_occurences_dict to one! " + str(subarray_and_occurences_dict))
            else:
                subarray_and_occurences_dict[current_subarray_length] = subarray_and_occurences_dict[current_subarray_length] + 1
                print("!!!AT END Updating subarray_and_occurences_dict to more than one! " + str(subarray_and_occurences_dict))

        # Reset current_subarray_length for second while loop
        current_subarray_length = 1

        # Check for same letter too to avoid counting it twice
        current_subarray_length_same_letter = 1
        number_of_same_letters = 0

        # Second while loop: just check for subarrays like ['z', 'j'] above (NOT for ['a', 'f'] and ['a', 'a'] yet)
        index = len(chromosome_string) - 1
        while index != 0:
            print("chromosome_string[index] == " +
                  str(chromosome_string[index]))
            print("chromosome_string[index - 1] == " +
                  str(chromosome_string[index - 1]))

            print("string_with_value_dict[chromosome_string[index]] == " +
                  str(string_with_value_dict[chromosome_string[index]]))
            print("string_with_value_dict[chromosome_string[index - 1]] == " + str(
                string_with_value_dict[chromosome_string[index - 1]]))

            if string_with_value_dict[chromosome_string[index]] + 1 == string_with_value_dict[chromosome_string[index - 1]]:
                current_subarray_length = current_subarray_length + 1
                # current_subarray_length_same_letter = 1
                print("incrementing current_subarray_length to " + str(current_subarray_length))
            # Account for subarrays of same letters to add in with overall subarray, but don't add to main subarray length on its own like in first while
            # loop to avoid counting for double array twice
            if string_with_value_dict[chromosome_string[index]] == string_with_value_dict[chromosome_string[index - 1]]:
                current_subarray_length_same_letter = current_subarray_length_same_letter + 1
                print("incrementing SAME LETTER")
            else:
                if current_subarray_length > 1:
                    if current_subarray_length_same_letter > 1:
                        print("IN SAME LETTER LENGTH")
                        if current_subarray_length + current_subarray_length_same_letter - 1 not in subarray_and_occurences_dict:
                            subarray_and_occurences_dict[current_subarray_length + current_subarray_length_same_letter - 1] = 1
                            print("!!!REVERSE Updating subarray_and_occurences_dict to 1! " + str(subarray_and_occurences_dict))
                        else:
                            subarray_and_occurences_dict[current_subarray_length + current_subarray_length_same_letter - 1] = subarray_and_occurences_dict[current_subarray_length+ current_subarray_length_same_letter - 1] + 1
                            print("!!!REVERSE Updating subarray_and_occurences_dict to more than one! " + str(subarray_and_occurences_dict))
                    else:
                        if current_subarray_length not in subarray_and_occurences_dict:
                            subarray_and_occurences_dict[current_subarray_length] = 1
                        else:
                            subarray_and_occurences_dict[current_subarray_length] = subarray_and_occurences_dict[current_subarray_length] + 1

                current_subarray_length = 1
                current_subarray_length_same_letter = 1

            index = index - 1

        # Account for if current subarray was at end
        if current_subarray_length > 1:
            if current_subarray_length not in subarray_and_occurences_dict:
                subarray_and_occurences_dict[current_subarray_length] = 1
                print("!!!AT END REVERSE Updating subarray_and_occurences_dict to one! " + str(subarray_and_occurences_dict))

            else:
                subarray_and_occurences_dict[current_subarray_length] = subarray_and_occurences_dict[current_subarray_length] + 1
                print("!!!AT END REVERSE Updating subarray_and_occurences_dict to more than one! " + str(subarray_and_occurences_dict))


        print("subarray_and_occurences_dict == " +
              str(subarray_and_occurences_dict))


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

    ga = genetic_pancake_algorithm(original_unordered_string=string_array, population_size=1)









