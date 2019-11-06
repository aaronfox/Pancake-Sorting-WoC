# Project 6
# Aaron Fox, Abby Spalding, Sai Chinthala
# CECS 545-01
# Dr. Yampolskiy

class genetic_pancake_algorithm:
    def __init__(self, original_unordered_string):
        self.original_unordered_string = original_unordered_string

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

    ga = genetic_pancake_algorithm(string_array)









