# Project 6
# Aaron Fox, Abby Spalding, Sai Chinthala
# CECS 545-01
# Dr. Yampolskiy

import math  # Need math for math.ceil for indices size (ceil)
import random  # Needed for random.shuffle for indices
import sys  # For exiting program when string is found
import time  # For timing functions

indices_solutions = []

# Chromosome is the indices of the pancakes that can be flipped
# Each population contains population_size amount of the chromosomes
# INPUT:
# original_unordered_string: the string array read from the .string file by read_string
# population_size: the size of each feneration
# number_of_generations: the number of generations to be run
# mutation_probability: The probability of a mutation occurring, normally 0.01 or 0.001
# crossover_probability: The probability of a crossover occurring, normally around 0.7


class genetic_pancake_algorithm:
    def __init__(self, original_unordered_string, population_size, number_of_generations, mutation_probability, crossover_probability, distance_weight, subarray_weight):
        self.original_unordered_string = original_unordered_string
        # Initial population of (randomly generated) chromosomes is placed in current_population
        self.current_population = []
        # Keep track of evaluations for each generation (each population of chromosomes)
        self.generation_evaluations = []
        # Keep track of the number of flips required to reach the string
        self.number_of_flips = 0
        self.number_of_flips_to_solve = []
        self.successful_indices = []
        # So the GA will stop running once the string has been found
        self.found_sorted_string = False

        self.plot_deets = []
        self.subarray_weight = subarray_weight
        self.distance_weight = distance_weight

        # Max number of indices required is found by 18*n / 11 according to Chittri
        self.indices_chromosome_size = math.ceil(
            18 * len(self.original_unordered_string) / 11)

        # Generate list of all possible indices that can be included in chromosome
        # Exclude 0 because a flip of 0 would simply flip the first char in the string and would
        # be pointless
        self.all_possible_indices = list(
            range(1, len(self.original_unordered_string)))

        # Create number of initial chromosomes in population as specified by population_size
        for i in range(population_size):
            # For each chromosome, place every possible index to flip for the first n, then fill remaining
            # spots with any number within the bounds of indices

            # Add all possible indices to flip for beginning n of 18n/11 indices
            chromosome = random.sample(
                self.all_possible_indices, len(self.all_possible_indices))

            # Add in remaining indices randomly until 18n/11 indices are in chromosome
            while len(chromosome) != self.indices_chromosome_size:
                chromosome.extend(random.sample(self.all_possible_indices, 1))

            # Shuffle once more to ensure randomness
            chromosome = random.sample(chromosome, len(chromosome))

            # Place chromosome into population
            self.current_population.append(chromosome)

        # Append initial population (stored in current_population) into the generation_evaluations
        self.generation_evaluations.append(
            self.evaluate_generation(self.current_population))

        # Keep track of which generation the program is currently on
        current_generation = 1
        # Step 4-10 here:
        while current_generation != number_of_generations and self.found_sorted_string == False:
            if current_generation % 1000 == 0:
                print('In generation ' + str(current_generation))
            current_generation = current_generation + 1

            self.new_population = []  # Holds newly created offspring
            # Run while loop until length of new population equals the old population
            while len(self.current_population) != len(self.new_population):
                # self.roulette_wheel_index stores the fitness ratio of each chromosome in the population for
                # later selections of which city will be chosen for the crossover operators to perform on
                self.roulette_wheel = self.get_roulette_wheel()

                ### Crossover Operation ###

                # Pick two parents for the crossover operator to occur
                parent_one, parent_two = random.choices(
                    population=self.current_population, weights=self.roulette_wheel, k=2)

                # Check Crossover Probablity to make sure a crossover should occur
                crossover_check = random.random()

                # Since random.random is between [0.0, 1.0), a crossover_probability of 1.0
                # will always be a crossover as expected
                if crossover_check < crossover_probability:
                    # Crossover two parents to produce offspring
                    offspring = self.crossover_operator(
                        parent_one=parent_one, parent_two=parent_two)
                # Else, skip crossover if the crossover probability variable is smaller than the random crossover_check
                else:
                    # Pick just one parent to copy exactly without any crossover operation
                    offspring = parent_one

                # Check if mutation operator should be performed
                mutation_check = random.random()

                if mutation_check < mutation_probability:
                    # Simply mutate the value of one index to become another index
                    rand_index = random.choice(list(range(len(offspring))))

                    # Remove currently indexed element from possible indices so that the element isn't set to the same char again
                    possible_indices = self.all_possible_indices.copy()
                    possible_indices.remove(offspring[rand_index])
                    offspring[rand_index] = random.sample(
                        possible_indices, 1)[0]

                #  Once offspring has been created through possible crossover and possible mutation, add it to new population
                self.new_population.append(offspring)
            #
            self.generation_evaluations.append(
                self.evaluate_generation(self.new_population))
            self.current_population = self.new_population.copy()

        print("self.generation_evaluations == " +
              str(self.generation_evaluations))
        print("self.generation_evaluations[len(self.generation_evaluations) - 1] == " + str(
            self.generation_evaluations[len(self.generation_evaluations) - 1]))

        print("final ordered string should be: " +
              str(sorted(self.original_unordered_string)))

        final_string = self.original_unordered_string.copy()
        for i in range(len(self.current_population[0])):
            final_string = self.flip_prefix(
                final_string, self.current_population[0][i])

        print("GA produced string is: " + str(final_string))

        average_costs = [x for x, y, z, a in self.generation_evaluations]

        self.plot_deets = [list(range(len(average_costs))), average_costs]

        # import matplotlib.pyplot as plt
        # plt.plot(list(range(len(average_costs))), average_costs)
        # plt.ylabel('Average Cost')
        # plt.xlabel('Generation')
        # plt.show()

    # Returns the "cost" of a chromosome by applying flips to the unordered string, finding the "fitness" of that string,
    # and then finding the inverse of that fitness as the cost
    # INPUT: chromosome: the chromosome of indices to apply to the unordered string
    # OUTPUT: the float cost value, between (0.0, 1]

    def evaluate_cost(self, chromosome):
        # First, apply all flips from indices to copy of original string
        temp_string_array = self.original_unordered_string.copy()

        for i in range(len(chromosome)):
            if temp_string_array == sorted(temp_string_array):
                self.number_of_flips = i
                self.number_of_flips_to_solve.append(i)
                self.successful_indices.append(chromosome[:i + 1])
            temp_string_array = self.flip_prefix(
                temp_string_array, chromosome[i])

        # Then find number of subarrays in string and the length of those subarrays
        # and find the fitness of a function by multiplying the number of subarrays of a certain length
        # by that certain length and adding them all together.
        # e.g. if we have 3 subarrays of length 4 and 5 subsequences of length 2,
        # the fitness of the function would 3(4) + 5(2) = 22
        sorted_string = sorted(self.original_unordered_string)

        # Find subsequences by creating two for loops to find the number of subarrays (contiguous arrays)
        subarray_length_and_occurrences = self.find_sub_arrays_length_and_occ(
            sorted_string, temp_string_array)

        # Find cost by finding the inverse of the result of multiplying all subarray lengths with their occurrences
        fitness = 0
        for length, occurrences in subarray_length_and_occurrences.items():
            fitness = fitness + length * occurrences

        # Make cost just inverse of the fitness
        if fitness == 0:  # Make sure fitness isn't zero to avoid divide by zero exception
            return 1
        else:
            cost = 1 / fitness

        # Let the distance cost  be the amount the letters are away from where
        # they should be in the sorted string
        distance_cost = 0
        # temp_string_array = ['b', 'a', 'c', 'd', 'a']
        # sorted_string = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for i in range(len(temp_string_array)):
            # print("temp_string_array[i] == " + str(temp_string_array[i]))
            # print("abs(sorted_string.index(temp_string_array[i])) == " + str(abs(sorted_string.index(temp_string_array[i]))))
            distance_cost = distance_cost + \
                abs(sorted_string.index(temp_string_array[i]) - i)

        if distance_cost == 0:
            print("temp_string_array == " + str(temp_string_array))
            print("Found finished string!!!")
            self.found_sorted_string = True
        # print("distance_cost = " + str(distance_cost))

        subsequence_weight = self.subarray_weight
        distance_weight = self.distance_weight
        extra_weight = 1

        # Find greatest possible distance so that the cost can be put in a fraction over 1
        greatest_poss_distance = 0
        reverse_string = sorted_string[::-1]
        for i in range(len(reverse_string)):
            greatest_poss_distance = greatest_poss_distance + \
                abs(sorted_string.index(reverse_string[i]) - i)

        distance_cost = extra_weight * distance_weight * \
            (distance_cost / greatest_poss_distance)
        subsequence_cost = extra_weight * subsequence_weight * cost
        if distance_cost * subsequence_cost == 0:
            return 0.0000000000000000000001
        return subsequence_cost * distance_cost

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
                            subarray_and_occurrences_dict[current_subarray_length +
                                                          current_subarray_length_same_letter] = 1
                        else:
                            subarray_and_occurrences_dict[current_subarray_length + current_subarray_length_same_letter -
                                                          1] = subarray_and_occurrences_dict[current_subarray_length + current_subarray_length_same_letter - 1] + 1
                    else:
                        if current_subarray_length not in subarray_and_occurrences_dict:
                            subarray_and_occurrences_dict[current_subarray_length] = 1
                        else:
                            subarray_and_occurrences_dict[current_subarray_length] = subarray_and_occurrences_dict[current_subarray_length] + 1

                current_subarray_length = 1
                current_subarray_length_same_letter = 1

            index = index - 1

        # Account for case where ['1', '1', '2', '1', '1'] i.e. where same letters are found at beginning/end of processed string
        # Account for if current subarray was at end
        if current_subarray_length > 1:
            if current_subarray_length_same_letter > 1:
                if current_subarray_length + current_subarray_length_same_letter not in subarray_and_occurrences_dict:
                    subarray_and_occurrences_dict[current_subarray_length +
                                                  current_subarray_length_same_letter] = 1
                else:
                    subarray_and_occurrences_dict[current_subarray_length +
                                                  current_subarray_length_same_letter] = subarray_and_occurrences_dict[current_subarray_length + current_subarray_length_same_letter] + 1
            else:
                if current_subarray_length not in subarray_and_occurrences_dict:
                    subarray_and_occurrences_dict[current_subarray_length] = 1
                else:
                    subarray_and_occurrences_dict[current_subarray_length] = subarray_and_occurrences_dict[current_subarray_length] + 1

        return subarray_and_occurrences_dict

    # Returns roulette wheel of the chromosome based on roulette wheel selection strategy for selecting chromosomes
    # INPUT: none. Everything is covered in the class already using self.
    # OUTPUT: list array of the resulting roulette wheel percentage, e.g. [0.454545, 0.363636, 0.181818] for a population with 3 chromosomes
    def get_roulette_wheel(self):
        roulette_wheel = []
        # Append cost of chromsome to populations when done
        for chromosome in self.current_population:
            self.number_of_flips = 0
            cost = self.evaluate_cost(chromosome)
            roulette_wheel.append(cost)

        # Find sum of costs for each chromosome in the population
        costs_summed = sum(roulette_wheel)

        # Divide the summed costs by the amount of each so that the "fitness"
        # for the chromosome will be higher for a more fit chromosome than a less than fit chromosome
        # (i.e. a chromosome with more and better subarrays will have a higher fitness)
        for i in range(len(roulette_wheel)):
            roulette_wheel[i] = costs_summed / roulette_wheel[i]

        # Place ratio of the chromosome's fitness to the population's total fitness in roulette_wheel
        costs_inverted_sum = sum(roulette_wheel)
        for i in range(len(roulette_wheel)):
            roulette_wheel[i] = roulette_wheel[i] / costs_inverted_sum

        # For testing, make sure the sum is equal to 1.0 as expected
        # self.sum = 0
        # for i in range(len(roulette_wheel)):
        #     self.sum = self.sum + roulette_wheel[i]

        return roulette_wheel

    # Using simple one point crossover, and selecting the better of the two offspring to return
    # INPUT: parent_one: one chromosome selected by roulette selection
    #        parent_two: another chromosome selected by roulette selection
    def crossover_operator(self, parent_one, parent_two):
        index = random.sample(range(0, len(parent_one)), 1)[0]

        # Initial offspring to potentially to return
        offspring_1 = parent_one[:index] + parent_two[index:]
        offspring_2 = parent_two[:index] + parent_one[index:]

        offspring = offspring_1

        return offspring

    # Takes in a given population of chromosomes and returns the average (cost) of traveling through every chromosome in the generation
    # INPUT: A population of chromosomes, i.e. a generation
    # OUTPUT: Returns a list of [average_cost, worst_in_generation, best_in_generation, standard_deviation], where:
    # average_cost is the average cost of every chromosome in the generation
    # worst_in_generation is the worst costing chromosome of the generation
    # best_in_generation is the best costing chromosome of the generation
    # standard_deviation is the standard deviation of all the chromosomes in the generation
    def evaluate_generation(self, population):
        if len(population) < 1:
            raise ValueError("Size of this generation's population is zero.")
        population_costs = []  # Stores all population costs for use in standard deviation
        total_cost = 0
        # Since chromosome's costs can never be negative, this is safe to start with
        worst_in_generation = -1
        # Make worst cost of chromosome infinity large at first
        best_in_generation = float('inf')
        for chromosome in population:
            this_cost = self.evaluate_cost(chromosome)
            population_costs.append(this_cost)
            total_cost = total_cost + this_cost
            if this_cost > worst_in_generation:
                worst_in_generation = this_cost
            if this_cost < best_in_generation:
                best_in_generation = this_cost

        # Calculate average
        average_cost = total_cost / len(population)

        # Calculate standard deviation of the generation
        sum = 0
        for i in range(len(population_costs)):
            sum = sum + (population_costs[i] - average_cost) ** 2
        standard_deviation = math.sqrt(sum / len(population_costs))

        return [average_cost, worst_in_generation, best_in_generation, standard_deviation]

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

    string_array = read_string(r'string_5.string')
    # string_array = read_string(r'string_50.string')

    print("string_array from input .string file == " + str(string_array))

    # mutation_probability should typically be in the range between 0.001 and 0.01
    # crossover_probability can be around 0.7 typically, but can vary depending on the problem
    # ga = genetic_pancake_algorithm(original_unordered_string=string_array, population_size=25, number_of_generations=5000, mutation_probability=.01, crossover_probability=0.8)
    # print("ga.number_of_flips_to_solve == " + str(ga.number_of_flips_to_solve))

    ### Wisdom of Crowds Approach ###

    # Just take minimum number of each GA and

    import matplotlib.pyplot as plt
    begin = time.time()

    number_of_flips_to_solve_array = []
    number_of_woc_iterations = 1
    for i in range(number_of_woc_iterations):
        # ga_begin = time.time()

        ga = genetic_pancake_algorithm(original_unordered_string=string_array, population_size=50, number_of_generations=150,
                                       mutation_probability=.01, crossover_probability=0.8, distance_weight=1.0, subarray_weight=1.)
        # ga_end = time.time()
        # print("GA took + " + str(ga_end - ga_begin) + " seconds to run")

        plt.plot(ga.plot_deets[0], ga.plot_deets[1], label='d_w=1.0, s_w=1.0')

        # For plotting different parameters in fitness function
        ga = genetic_pancake_algorithm(original_unordered_string=string_array, population_size=50, number_of_generations=150,
                                       mutation_probability=.01, crossover_probability=0.8, distance_weight=1.0, subarray_weight=0.7)
        plt.plot(ga.plot_deets[0], ga.plot_deets[1], label='d_w=1.0, s_w=0.7')

        ga = genetic_pancake_algorithm(original_unordered_string=string_array, population_size=50, number_of_generations=150,
                                       mutation_probability=.01, crossover_probability=0.8, distance_weight=1.0, subarray_weight=0.5)
        plt.plot(ga.plot_deets[0], ga.plot_deets[1], label='d_w=1.0, s_w=0.5')

        ga = genetic_pancake_algorithm(original_unordered_string=string_array, population_size=50, number_of_generations=150,
                                       mutation_probability=.01, crossover_probability=0.8, distance_weight=1.0, subarray_weight=0.3)
        plt.plot(ga.plot_deets[0], ga.plot_deets[1], label='d_w=1.0, s_w=0.3')

        ga = genetic_pancake_algorithm(original_unordered_string=string_array, population_size=50, number_of_generations=150,
                                       mutation_probability=.01, crossover_probability=0.8, distance_weight=0.7, subarray_weight=1.0)
        plt.plot(ga.plot_deets[0], ga.plot_deets[1], label='d_w=0.7, s_w=1.0')

        ga = genetic_pancake_algorithm(original_unordered_string=string_array, population_size=50, number_of_generations=150,
                                       mutation_probability=.01, crossover_probability=0.8, distance_weight=0.5, subarray_weight=1.0)
        plt.plot(ga.plot_deets[0], ga.plot_deets[1], label='d_w=0.5, s_w=1.0')

        ga = genetic_pancake_algorithm(original_unordered_string=string_array, population_size=50, number_of_generations=150,
                                       mutation_probability=.01, crossover_probability=0.8, distance_weight=0.3, subarray_weight=1.0)
        plt.plot(ga.plot_deets[0], ga.plot_deets[1], label='d_w=0.3, s_w=1.0')

        ga = genetic_pancake_algorithm(original_unordered_string=string_array, population_size=50, number_of_generations=150,
                                       mutation_probability=.01, crossover_probability=0.8, distance_weight=0.3, subarray_weight=1.0)
        plt.plot(ga.plot_deets[0], ga.plot_deets[1], label='d_w=0.7, s_w=0.7')

        # number_of_flips_to_solve_array.append(ga.number_of_flips_to_solve)

        # indices_solutions.append(ga.number_of_flips_to_solve)
        # print("For iteration " + str(i) + ", ga.number_of_flips_to_solve == " + str(ga.number_of_flips_to_solve))

    print("number_of_flips_to_solve_array == " +
          str(number_of_flips_to_solve_array))

    # minimum_number_of_flips is the final answer that the GA and WoC find
    minimum_number_of_flips = float("inf")
    for x in number_of_flips_to_solve_array:
        if len(x) > 0:
            if min(x) < minimum_number_of_flips:
                minimum_number_of_flips = min(x)

    end = time.time()
    print("Time taken for WoC & GA: " + str(end - begin) + " seconds")
    # import matplotlib.pyplot as plt
    # plt.plot(list(range(len(average_costs))), average_costs)
    print("Minimum number of flips as determined by our GA and WoC: " +
          str(minimum_number_of_flips))
    print("Keep in mind the maximum bound for this is 18 * n / 11, or " +
          str(math.ceil(18 * len(string_array) / 11)))
    plt.legend(loc="upper right")
    print("indices_solutions == " + str(indices_solutions))
    plt.title('Average Cost with distance_weight=0.1 and subarray_weight=0.1')
    plt.ylabel('Average Cost')
    plt.xlabel('Generation')
    plt.show()
