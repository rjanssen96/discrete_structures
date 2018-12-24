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
        # if degree == 1:
        #     characteristic_equation = char_equation_1(coefficients[0])
        #     print("Step 2:  The characteristic equation is: \n" + str(characteristic_equation) + "=0" + "\n")
        # elif degree >= 2:
        #     characteristic_equation = char_equation_2(coefficients)
        #     print("Step 2: The characteristic equation is: \n" + str(characteristic_equation) + "=0" + "\n")
        # else:
        #     print("Step 2: Wrong degree value or incorrect characteristic equation" + "\n")
        #     characteristic_equation = ""
        characteristic_equation = char_equation_2(coefficients)
        print("Step 2: The characteristic equation is: \n" + str(characteristic_equation) + "=0" + "\n")
    except:
        print("2 doesnt work, shocker dude")

    # Step 3: Obtain the roots
    # if degree >= 1:  # find out how to obtain the multiplicity, find root() or search in list for doubles an m=2 for every
    try:
        r = symbols('r')
        new_findings = roots(characteristic_equation, r)  # returns root:multiplicity
        print("Step 3:  The roots of this equation are:")
        print(new_findings)  # root:multiplicity
        print()
    except:
        print("3 doesnt work, shocker dude")

    # Step 4: Obtain general solution
    # if degree >= 1:  # multiplicity is important!!! Also build this to support more then 2 roots
    try:
        general_solution = find_general_solution_2(new_findings)
        # general_solution = "Sup Nerd!"
        print("Step 4:  The general solution of this equation is: \n" + str(general_solution) + "\n")
    except:
        print("4 doesnt work, shocker dude")

    # Step 5.1: Obtain alpha values
    try:
        outcome = find_alpha_values(initial_terms, new_findings)
        print("Step 5.1: The value of the Alphas:")
        print(outcome)
    except:
        print("5.1 doesnt work, shocker dude")

    # Step 5.2: Obtain specific solution
    try:
        specific_solution = general_solution
        for x in range(0, len(outcome)):
            specific_solution = specific_solution.replace("Alpha_" + str(x + 1), "(" + str(outcome.get(x)) + ")")
        specific_solution = specific_solution.replace("**", "^")
        specific_solution = specific_solution.replace("s(n)=", "sdir := n -> ")
        specific_solution = specific_solution.replace(")(", ")*(")
        specific_solution = specific_solution + ";"
        print("\nStep 5.2: The specific solution for this equation is: \n" + str(specific_solution) + "\n")
    except:
        print("5.2 doesnt work, shocker dude")


solve_homog_relation()
