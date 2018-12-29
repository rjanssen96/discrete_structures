# from sympy import *

# from hom_step1 import *
from hom_step2 import *
# from hom_step3 import *
from hom_step4 import *
from hom_step5 import *
from find_degree import find_degree
from colorama import Fore as color

import file_writer

""""
Add as little as possible to the bottom part
Try to put everything in functions
Also add excepts for several errors
Print except errors to a file with the name: commas(nr) errors / output?
"""


def solve_homog_relation(degree, initial, coefficients, parts, filename):
    # Step 0: Read .txt and obtain initial terms (list?), degree and each C_1*A_n-1
    """
    IMPORTANT:
    if a_1 and a_3 are the used terms, then list needs 3 coeffs, one for a_2 as well, which is 0!!!
    if there's no coeff in front of a_x then 1 needs to be written as a coeff in the list
    """
    # degree = find_degree(pathstring=pathstring, degree=0)
    # initial_terms = [1, 1]  # List of all initial terms
    # coefficients = [1, 1]  # if n+1 in s():=, then make every n -1 (so one add a -1 to the n's)
    # parts = ["*s(n-1)", "*s(n-2)", "*s(n-3)"]  # If terms come from read.txt function, then comment this line
    # # fill in all parts and coeffs, if n-2 and n-4 only, then still fill in 0*n-3, etc.

    """Where do you use this degree??"""
    degree = degree
    initial_terms = initial
    coefficients = coefficients
    parts = parts

    print(color.GREEN, "Degree is: {}\nInitial terms are: {}\nCoefficients are: {}\nParts are: {}\n".format(type(degree), initial_terms, coefficients,parts), color.RESET)
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
        print(color.GREEN + "Step 1: The rewritten sequence is: \n" + str(sequence) + "\n", color.RESET)
    except Exception as error:
        print("1 doesnt work, ERROR: {}\n".format(error))
        print(color.RED + "Error occurs in file: {}\n".format(filename), color.RESET)
        try:
            file_writer.error_in_file(filename=filename, homogeneous=True, step="Step 1", automatic=True, error=error)
        except Exception as error:
            print(color.RED + "Error during writing error file.\nHere is the data:\nFile: {}\nHomogeneous: {}\nStep: {}\nAutomatic: {}\nOrginal error: {}\n".format(filename, True, "Step 1", True, error))

    # Step 2: Obtaining the characteristic equation
    try:
        characteristic_equation = char_equation_2(coefficients)
        print("Step 2: The characteristic equation is: \n" + str(characteristic_equation) + "=0" + "\n")
    except:
        print("2 doesnt work, shocker dude")
        print(color.RED + "Error occurs in file: {}".format(filename), color.RESET)
        try:
            file_writer.error_in_file(filename=filename, homogeneous=True, step="Step 2", automatic=True, error=error)
        except Exception as error:
            print(
                color.RED + "Error during writing error file.\nHere is the data:\nFile: {}\nHomogeneous: {}\nStep: {}\nAutomatic: {}\nOrginal error: {}\n".format(
                    filename, True, "Step 2", True, error))

    # Step 3: Obtain the roots
    try:
        r = symbols('r')
        r_and_m_found = roots(characteristic_equation, r)  # returns root:multiplicity
        print("Step 3:  The roots of this equation are:")
        print(r_and_m_found)  # root:multiplicity
        print()
    except:
        print("3 doesnt work, shocker dude")
        print(color.RED + "Error occurs in file: {}".format(filename), color.RESET)
        try:
            file_writer.error_in_file(filename=filename, homogeneous=True, step="Step 3", automatic=True, error=error)
        except Exception as error:
            print(
                color.RED + "Error during writing error file.\nHere is the data:\nFile: {}\nHomogeneous: {}\nStep: {}\nAutomatic: {}\nOrginal error: {}\n".format(
                    filename, True, "Step 3", True, error))

    # Step 4: Obtain general solution
    try:
        general_solution = find_general_solution_2(r_and_m_found)
        general_solution = general_solution.replace("s(n)=+", "s(n)=")
        print("Step 4:  The general solution of this equation is: \n" + str(general_solution) + "\n")
    except:
        print("4 doesnt work, shocker dude")
        print(color.RED + "Error occurs in file: {}".format(filename), color.RESET)
        try:
            file_writer.error_in_file(filename=filename, homogeneous=True, step="Step 4", automatic=True, error=error)
        except Exception as error:
            print(
                color.RED + "Error during writing error file.\nHere is the data:\nFile: {}\nHomogeneous: {}\nStep: {}\nAutomatic: {}\nOrginal error: {}\n".format(
                    filename, True, "Step 4", True, error))

    # Step 5.1: Obtain alpha values
    try:
        outcome = find_alpha_values(initial_terms, r_and_m_found)
        print("Step 5.1: The value of the Alphas:")
        print(outcome)
    except:
        print("5.1 doesnt work, shocker dude")
        print(color.RED + "Error occurs in file: {}".format(filename), color.RESET)
        try:
            file_writer.error_in_file(filename=filename, homogeneous=True, step="Step 5.1", automatic=True, error=error)
        except Exception as error:
            print(
                color.RED + "Error during writing error file.\nHere is the data:\nFile: {}\nHomogeneous: {}\nStep: {}\nAutomatic: {}\nOrginal error: {}\n".format(
                    filename, True, "Step 5.1", True, error))

    # Step 5.2: Obtain specific solution
    try:
        specific_solution = gimme_specific_solution(general_solution, outcome)
        print("\nStep 5.2: The specific solution for this equation is: \n" + str(specific_solution) + "\n")
    except Exception as error:
        print("5.2 doesnt work, shocker dude: ERROR: {}".format(error))
        print(color.RED + "Error occurs in file: {}".format(filename), color.RESET)
        try:
            file_writer.error_in_file(filename=filename, homogeneous=True, step="Step 5.2", automatic=True, error=error)
        except Exception as error:
            print(
                color.RED + "Error during writing error file.\nHere is the data:\nFile: {}\nHomogeneous: {}\nStep: {}\nAutomatic: {}\nOrginal error: {}\n".format(
                    filename, True, "Step 5.2", True, error))