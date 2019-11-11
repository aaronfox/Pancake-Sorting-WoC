import random
# Generates test string files
number_of_letters = 50
f = open(str("string_" + str(number_of_letters) + ".string"), "w")
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
for i in range(number_of_letters):
    f.write(str(random.choice(alphabet)) + "\n")
