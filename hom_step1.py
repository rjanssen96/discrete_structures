from file_writer import *

# Step 0: Read .txt and obtain initial terms (list?), degree and each C_1*A_n-1
"""
IMPORTANT:
if a_1 and a_3 are the used terms, then list needs 3 coeffs, one for a_2 as well, which is 0!!!
if there's no coeff in front of a_x then 1 needs to be written as a coeff in the list
"""
degree = 2
initial_terms = [1, 1]  # List of all initial terms
coefficients = [1, 1]  # if n+1 in s():=, then make every n -1 (so one add a -1 to the n's)
parts = ["*s(n-1)", "*s(n-2)", "*s(n-3)"]  # If terms come from read.txt function, then comment this line
# fill in all parts and coeffs, if n-2 and n-4 only, then still fill in 0*n-3, etc.

# Step 1: Rewriting the sequence
# Maybe replace this part with now Rico's read parts added together from the dictionary sort result?
try:
    sequence = "s(n)="
    i = 0
    for x in coefficients:
        if coefficients[i] >= 0 and i == 0:
            sequence = sequence + str(coefficients[i]) + str(parts[i])
        # add a + for the positive coefficients
        elif coefficients[i] >= 0:
            sequence = sequence + "+" + str(coefficients[i]) + str(parts[i])
        elif coefficients[i] < 0:
            sequence = sequence + str(coefficients[i]) + str(parts[i])
        else:
            print("wrong sequence step 1")
        i = i + 1
    print("Step 1: The rewritten sequence is: \n" + str(sequence) + "\n")
except:
    print("1 doesnt work, shocker dude")