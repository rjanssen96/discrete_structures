# from sympy import *

# from hom_step1 import *
from hom_step2 import *
# from hom_step3 import *
from hom_step4 import *
from hom_step5 import *


""""
Add as little as possible to the bottom part
Try to put everything in functions
Also add excepts for several errors
Print except errors to a file with the name: commas(nr) errors / output?
"""


def solve_homog_relation():
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

    # Step 2: Obtaining the characteristic equation
    try:
        characteristic_equation = char_equation_2(coefficients)
        print("Step 2: The characteristic equation is: \n" + str(characteristic_equation) + "=0" + "\n")
    except:
        print("2 doesnt work, shocker dude")

    # Step 3: Obtain the roots
    try:
        r = symbols('r')
        r_and_m_found = roots(characteristic_equation, r)  # returns root:multiplicity
        print("Step 3:  The roots of this equation are:")
        print(r_and_m_found)  # root:multiplicity
        print()
    except:
        print("3 doesnt work, shocker dude")

    # Step 4: Obtain general solution
    try:
        general_solution = find_general_solution_2(r_and_m_found)
        general_solution = general_solution.replace("s(n)=+", "s(n)=")
        print("Step 4:  The general solution of this equation is: \n" + str(general_solution) + "\n")
    except:
        print("4 doesnt work, shocker dude")

    # Step 5.1: Obtain alpha values
    try:
        outcome = find_alpha_values(initial_terms, r_and_m_found)
        print("Step 5.1: The value of the Alphas:")
        print(outcome)
    except:
        print("5.1 doesnt work, shocker dude")

    # Step 5.2: Obtain specific solution
    try:
        specific_solution = gimme_specific_solution(general_solution, outcome)
        print("\nStep 5.2: The specific solution for this equation is: \n" + str(specific_solution) + "\n")
    except Exception as error:
        print("5.2 doesnt work, shocker dude: ERROR: {}".format(error))


solve_homog_relation()
