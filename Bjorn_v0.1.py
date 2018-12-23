from sympy import *
from math import sqrt  # for testing our specific solutions initial terms
init_printing(use_unicode=False, wrap_line=False)


# (Step 2) Obtaining char equation with degree 1
def char_equation_1(first_term_in):
    if first_term_in >= 0:
        equation = "r-" + str(first_term_in) #+ "=0"
    elif first_term_in < 0:
        first_term_in = int(first_term_in*-1)
        equation = "r+" + str(first_term_in) #+ "=0"
    return equation


# (Step 2) Obtaining char equation with degree 2+
def char_equation_2(coeffs):
    total_equation = "r**" + str(len(coeffs))
    i = 0
    next_power = len(coeffs)-1
    for x in range(len(coeffs)):
        next_coeff = coeffs[i]
        if next_coeff >= 0:
            next_coeff = "-" + str(next_coeff)
        elif next_coeff < 0:
            next_coeff = next_coeff * -1
            next_coeff = "+" + str(next_coeff)
        else:
            print("Smth went wrong in char_equation_2")

        # Finds out if the next power is 0, if so, then just add the coeff and not r^0 cuz r^0 = 1 = coeff
        if next_power != 0:
            total_equation = total_equation + str(next_coeff) + "*r**" + str(next_power)
        elif next_power == 0:
            total_equation = total_equation + str(next_coeff)
        i = i + 1
        next_power = next_power - 1

    # total_equation = total_equation + "=0"
    return total_equation


# (Step 4) Obtain the general solution of degree 2+, nvm 1+
def find_general_solution_2(all_r_and_m_test):
    test_general_sol = "s(n)="
    u = 1  # counter for adding a + between root sections
    a = 1

    # chose which theorem to use based on the multiplicities
    # loop through all multiplicities, if any of them is > 1, then set boolean equal to True, default is false
    difficult_theorem = False
    for x in all_r_and_m_test.values():
        if x > 1:
            difficult_theorem = True
    # print(difficult_theorem)

    if difficult_theorem == True:  # if some multiplicitie(s) > 1
        for x in all_r_and_m_test:  # x is the values of the roots
            i = 0  # power of the n in every root section counter, resets for every root
            test_general_sol = test_general_sol + "("
            for y in range(0, all_r_and_m_test[x]):  # for the length of the multiplicity excluding the boundaries
                if y == 0:  # to prevent one to many +
                    test_general_sol = test_general_sol + "Alpha_" + str(a) + "*n**" + str(i)
                else:
                    test_general_sol = test_general_sol + "+Alpha_" + str(a) + "*n**" + str(i)
                i = i + 1  # power counter
                a = a + 1  # alpha counter
            # prevents one to many * at the end
            if u == len(all_r_and_m_test):
                test_general_sol = test_general_sol + ")(" + str(x) + ")**n"
            elif u != len(all_r_and_m_test):
                test_general_sol = test_general_sol + ")(" + str(x) + ")**n+"
            else:
                print("Never lucky m8")
            u = u + 1
    elif difficult_theorem == False:  # when all multiplicities are 1
        for x in all_r_and_m_test:
            if x == 0:  # So that the equation doesn't start with +
                test_general_sol = test_general_sol + "Alpha_" + str(a) + "*(" + str(x) + ")**n"
            elif x != 0:
                test_general_sol = test_general_sol + "+Alpha_" + str(a) + "*(" + str(x) + ")**n"
            a = a + 1

    # replace all the *n**0 with "", cuz anything to the 0th power is 1
    # and replace anything to the power 1 to just that thing
    test_general_sol = test_general_sol.replace("*n**0", "")
    test_general_sol = test_general_sol.replace("**1", "")

    return test_general_sol


# (Step 5.1) solving every systems with no matter the used theorem (cuz theorem 4 also contains theorem 3)
def find_alpha_values(my_initial_terms, all_r_and_m):
    """
    SECTION 0: NEEDED INFORMATION
    """
    nr_of_initial_terms = len(my_initial_terms)
    alpha_coeffs = {}
    matrix_input = ()
    solve_variable = ()

    """
    SECTION 1: GATHERING ALPHA COEFFS + INITIAL TERM VALUE ROWS 
    """
    for n in range(0, nr_of_initial_terms):  # a_0, a_1, ..., a_n
        row_of_coeffs = ()  # resets the tuples with the previous alphas coeff values

        for r in all_r_and_m:  # r holds the value of each root one by one for all initial terms
            m = all_r_and_m[r]  # m is the value of the multiplicty of the current root

            for p in range(0, m):  # p is the power to raise n to. For every root from 0 to m-1
                next_coeff = (n ** p) * (r ** n)
                row_of_coeffs = row_of_coeffs + (next_coeff,)

        matrix_row = row_of_coeffs + (my_initial_terms[n],)  # adds the answer of the initial term to the row
        alpha_coeffs[
            "row_{0}".format(n)] = matrix_row  # adds all the coeffs+answers of each initial term to a dictionary

    """
    SECTION 2: CREATE ALL NEEDED MATRIX SOLVE INPUT
    """
    amount_of_rows = len(alpha_coeffs)
    for x in range(0, amount_of_rows):  # makes a list with lists in it for every row of the matrix
        matrix_input = matrix_input + ((alpha_coeffs["row_" + str(x)]),)

    system = Matrix(matrix_input)  # creates correct syntax

    for x in range(0,
                   len(alpha_coeffs["row_0"]) - 1):  # Calculates how many different alpha coeffs need to be solved for
        solve_variable = solve_variable + (x,)

    """
    SECTION 3: SOLVE THE SYSTEM
    """
    matrix_result = solve_linear_system(system, *solve_variable)

    return matrix_result


# # (Step 5.2) Obtain the specific solution
# def find_specific_solution_1(alpha_1_in, root_1_in):
#     solution = "A_n = " + str(alpha_1_in) + " * " + str(root_1_in) + "^n"
#     return solution


""""
Add as little as possible to the bottom part
Try to put everything in functions
Also add excepts for several errors
Print except errors to a file with the name: commas(nr) errors / output?
"""

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
    if degree == 1:
        characteristic_equation = char_equation_1(coefficients[0])
        print("Step 2:  The characteristic equation is: \n" + str(characteristic_equation) + "=0" + "\n")
    elif degree >= 2:
        characteristic_equation = char_equation_2(coefficients)
        print("Step 2: The characteristic equation is: \n" + str(characteristic_equation) + "=0" + "\n")
    else:
        print("Step 2: Wrong degree value or incorrect characteristic equation" + "\n")
        characteristic_equation = ""
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

"""
TEST
TEST
TEST
COMMA VS MY ALG
"""

# outcomes = []
#
# for n in range(0, 20):
#     outcomes.append(1/10*(5-5**(1/2))*(1/2-1/2*5**(1/2))**n+1/10*(1/2*5**(1/2)+1/2)**n*(5+5**(1/2)))
#
# print(outcomes)
#
# outcomes = []
#
# # My answer
# my_formula = 5
#
# for n in range(0, 20):
#     outcomes.append((-sqrt(5)/10 + 1/2)*(-sqrt(5)/2 + 1/2)**n+(sqrt(5)/10 + 1/2)*(1/2 + sqrt(5)/2)**n)
#
# print(outcomes)
#
# # allowed diversion
# print(1/1000)
