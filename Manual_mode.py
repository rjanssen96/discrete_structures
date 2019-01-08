import os
from colorama import Fore as color
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from hom_step2 import *
from hom_step4 import *
from hom_step5 import *
from nonhom_step5 import *
from nonhom_step7 import *
# from file_writer import *
import file_writer


# Chosing homog or non-homog
def manual_mode(filename):
    hom_or_non = input("Is it a homogeneous (h) or non-homogeneous (n) relation?\n")

    if hom_or_non == "h":
        print("You choose homogeneous")
        manual_mod_homog_0(filename)
    elif hom_or_non == "n":
        print("You choose non-homogeneous")
        manual_mode_non_homog_0(filename)
    else:
        print("Wrong input m8...")


# Gathering correct input
def manual_mod_homog_0(filename):
    print("Make sure you add the following information in the correct order!!!")
    print("So coefficient of part one, then of part two, etc.")
    print("Also give fractions as 5/4 not (5/4)!!!")

    degree = int(input("What is the DEGREE of this relation?\n"))
    coefficients = []

    for x in range(0, degree):
        coefficients = coefficients + [str(input("What is coefficients number " + str(x) + "\n"))]

    print("List of coeffs:")
    print(coefficients)

    initial_terms = []

    for x in range(0, degree):
        initial_terms = initial_terms + [str(parse_expr(input("What is initial_terms number " + str(x) + "\n")))]

    print("List of initial_terms:")
    print(initial_terms)

    continue_or_not = input("Are these lists correct? (yes or no)\n")
    if continue_or_not == "yes":
        manual_mod_homog_1(coefficients, initial_terms, degree, filename)
    elif continue_or_not == "no":
        print("Ok let's try again")
        manual_mod_homog_0(filename)
    else:
        print("Neither yes nor no was input...")


# Step 1: Rewriting the sequence
def manual_mod_homog_1(coefficients, initial_terms, degree, filename):
    try:
        # First try this step automated
        sequence = "s(n)="
        i = 0
        for x in coefficients:
            if parse_expr(coefficients[i]) >= 0 and i == 0:
                sequence = sequence + "(" + str(coefficients[i]) + ")*s(n-" + str(i+1) + ")"
            # add a + for the positive coefficients
            elif parse_expr(coefficients[i]) >= 0:
                sequence = sequence + "+(" + str(coefficients[i]) + ")*s(n-" + str(i+1) + ")"
            elif parse_expr(coefficients[i]) < 0:
                sequence = sequence + "(" + str(coefficients[i]) + ")*s(n-" + str(i+1) + ")"
            else:
                print("wrong sequence step 1")
            i = i + 1
        print(color.GREEN + "Step 1: The rewritten sequence is: \n" + str(sequence) + "\n", color.RESET)

        # Ask if altering is needed
        continue_or_not = input("Is this correct? (yes or no)\n")
        if continue_or_not == "yes":
            # print("Great!")
            manual_mode_homog_2(coefficients, initial_terms, degree, sequence, filename)
        elif continue_or_not == "no":
            sequence = input("Give the relation manually:\n")

            # Confirm manual input or quit
            confirm_or_exit = input("Is this correct? (yes or no)\n")
            if confirm_or_exit == "yes":
                manual_mode_homog_2(coefficients, initial_terms, degree, sequence, filename)
            else:
                print("Ending manual mode")
        else:
            print("Neither yes nor no given")

    except Exception as error:
        print("1 doesnt work, ERROR: {}\n".format(error))
        print(color.RED + "Error occurs in file: {}\n".format(filename), color.RESET)
        try:
            file_writer.error_in_file(filename=filename, homogeneous=True, step="Step 1", automatic=True, error=error)
        except Exception as error:
            print(color.RED + "Error during writing error file.\nHere is the data:\nFile: {}\nHomogeneous: {}\nStep: {}\nAutomatic: {}\nOrginal error: {}\n".format(filename, True, "Step 1", True, error))


# Step 2: Obtaining the characteristic equation
def manual_mode_homog_2(coefficients, initial_terms, degree, sequence, filename):
    try:
        # First try this step automated
        characteristic_equation = char_equation_2(coefficients)
        print("\nStep 2: The characteristic equation is: \n" + str(characteristic_equation) + "=0" + "\n")

        # Ask if altering is needed
        continue_or_not = input("Is this correct? (yes or no)\n")
        if continue_or_not == "yes":
            manual_mode_homog_3(coefficients, initial_terms, degree, characteristic_equation, filename)
        elif continue_or_not == "no":
            characteristic_equation = input("Manually input the characteristic equation:\n")

            # Confirm manual input or quit
            confirm_or_exit = input("Is this correct? (yes or no)\n")
            if confirm_or_exit == "yes":
                manual_mode_homog_3(coefficients, initial_terms, degree, characteristic_equation, filename)
            else:
                print("Ending manual mode")
        else:
            print("Neither yes nor no given")
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
def manual_mode_homog_3(coefficients, initial_terms, degree, characteristic_equation, filename):
    try:
        # First try this step automated
        r = symbols('r')
        r_and_m_found = roots(characteristic_equation, r)  # returns root:multiplicity
        print("\nStep 3: The roots of this equation are:")
        print(r_and_m_found)  # root:multiplicity
        print()

        # Ask if altering is needed
        continue_or_not = input("Is this correct? (yes or no)\n")
        if continue_or_not == "yes":
            manual_mode_homog_4(coefficients, initial_terms, degree, r_and_m_found, filename)
        elif continue_or_not == "no":
            r_and_m_found = {}
            nr_of_roots = input("How many roots should there be?:\n")
            for x in range(0, int(nr_of_roots)):
                root_value = int(input("What is root " + str(x) + "'s value?:\n"))
                root_multiplicity = int(input("What is that root's multiplicity?\n"))
                r_and_m_found[root_value] = root_multiplicity
            print("Manually input the root and multiplicity values:")
            print(r_and_m_found)

            # Confirm manual input or quit
            confirm_or_exit = input("Is this correct? (yes or no)\n")
            if confirm_or_exit == "yes":
                manual_mode_homog_4(coefficients, initial_terms, degree, r_and_m_found, filename)
            else:
                print("Ending manual mode")
        else:
            print("Neither yes nor no given")
    except Exception as error:
        print(
            color.RED + "Error during writing error file.\nHere is the data:\nFile: {}\nHomogeneous: {}\nStep: {}\nAutomatic: {}\nOrginal error: {}\n".format(
                filename, True, "Step 3", True, error))


# Step 4: Obtain general solution
def manual_mode_homog_4(coefficients, initial_terms, degree, r_and_m_found, filename):
    try:
        # First try this step automated
        general_solution = find_general_solution_2(r_and_m_found)
        general_solution = general_solution.replace("s(n)=+", "s(n)=")
        print("\nStep 4: The general solution of this equation is: \n" + str(general_solution) + "\n")

        # Ask if altering is needed
        continue_or_not = input("Is this correct? (yes or no)\n")
        if continue_or_not == "yes":
            manual_mode_homog_51(coefficients, initial_terms, degree, r_and_m_found, general_solution, filename)
        elif continue_or_not == "no":
            general_solution = input("Manually input the general solution:\n")

            # Confirm manual input or quit
            confirm_or_exit = input("Is this correct? (yes or no)\n")
            if confirm_or_exit == "yes":
                manual_mode_homog_51(coefficients, initial_terms, degree, r_and_m_found, general_solution, filename)
            else:
                print("Ending manual mode")
        else:
            print("Neither yes nor no given")
    except Exception as error:
        print(
            color.RED + "Error during writing error file.\nHere is the data:\nFile: {}\nHomogeneous: {}\nStep: {}\nAutomatic: {}\nOrginal error: {}\n".format(
                filename, True, "Step 4", True, error))


# Step 5.1: Obtain alpha values
def manual_mode_homog_51(coefficients, initial_terms, degree, r_and_m_found, general_solution, filename):
    try:
        # First try this step automated
        outcome = hom_find_alpha_values(initial_terms, r_and_m_found)
        print("\nStep 5.1: The value of the Alphas:")
        print(outcome)

        # Ask if altering is needed
        continue_or_not = input("Is this correct? (yes or no)\n")
        if continue_or_not == "yes":
            manual_mode_homog_52(general_solution, outcome, filename)
        elif continue_or_not == "no":

            outcome = {}
            nr_of_roots = input("How many alphas should there be?:\n")
            for x in range(0, int(nr_of_roots)):
                alpha_value = int(input("What is alpha " + str(x) + "'s value?:\n"))
                # root_multiplicity = int(input("What is that root's multiplicity?\n"))
                outcome[x] = alpha_value
            print("Manually input the alpha values:")
            print(outcome)

            # Confirm manual input or quit
            confirm_or_exit = input("Is this correct? (yes or no)\n")
            if confirm_or_exit == "yes":
                manual_mode_homog_52(general_solution, outcome, filename)
            else:
                print("Ending manual mode")

        else:
            print("Neither yes nor no given")
    except Exception as error:
        print(
            color.RED + "Error during writing error file.\nHere is the data:\nFile: {}\nHomogeneous: {}\nStep: {}\nAutomatic: {}\nOrginal error: {}\n".format(
                filename, True, "Step 5.1", True, error))


# Step 5.2: Obtain specific solution
def manual_mode_homog_52(general_solution, outcome, filename):
    try:
        # First try this step automated
        specific_solution = gimme_specific_solution(general_solution, outcome)
        print(color.BLUE + "\nStep 5.2: The specific solution for this equation is: \n" + str(specific_solution) + "\n",
              color.RESET)
        # time.sleep(10)

        # Ask if altering is needed
        continue_or_not = input("Is this correct? (yes or no)\n")
        if continue_or_not == "yes":
            life = "great"
        elif continue_or_not == "no":
            specific_solution = input("Manually input the alpha values:\n")
            print(specific_solution)
        else:
            print("Neither yes nor no given")
    except Exception as error:
        print(
            color.RED + "Error during writing error file.\nHere is the data:\nFile: {}\nHomogeneous: {}\nStep: {}\nAutomatic: {}\nOrginal error: {}\n".format(
                filename, True, "Step 5.2", True, error))


"""
NON-HOMOGENEOUS PARTS
"""


# gathering information
def manual_mode_non_homog_0(filename):
    # print("Go away!")
    print("Make sure you add the following information in the correct order!!!")
    print("So coefficient of part one, then of part two, etc.")
    print("Also give fractions as 5/4 not (5/4)!!!")

    degree = int(input("What is the DEGREE of this relation?\n"))
    coefficients_homog = []

    print("Coeffeicients of the associated homogeneous system:")
    for x in range(0, degree):
        coefficients_homog = coefficients_homog + [input("What is coefficients number " + str(x) + "\n")]

    print("List of coeffs:")
    print(coefficients_homog)

    initial_terms = []

    for x in range(0, degree):
        initial_terms = initial_terms + [parse_expr(input("What is initial_terms number " + str(x) + "\n"))]

    print("List of initial_terms:")
    print(initial_terms)

    highest_power_fn_part = str(input("what is the highest power of the F(n) part?:\n"))

    fn_parts = {}
    next_power = int(highest_power_fn_part)

    for x in range(0, int(highest_power_fn_part)+1):
        fn_parts[next_power] = str(parse_expr(input("What is the coeff of power " + str(next_power) + "?\n")))
        next_power = next_power - 1

    # fn_part = input("What is the F(n) part of this relation?:\n")
    print("Chosen F(n) part:")
    print(fn_parts)

    # First ask for the highest power and then loop to fill in all dict powers
    # must be
    # in a
    # dictionary

    fn_part_sn = str(input("What is the value of s in this F(n) part? s**n, if not given, then fill in 1\n"))

    continue_or_not = input("Are all these input values correct? (yes or no)\n")
    if continue_or_not == "yes":
        manual_mode_non_homog_1(coefficients_homog, degree, initial_terms, fn_parts, highest_power_fn_part, filename, fn_part_sn)
    elif continue_or_not == "no":
        print("Ok let's try again")
        manual_mod_homog_0(filename)
    else:
        print("Neither yes nor no was input...")


# Step 1: rewrite the relation
def manual_mode_non_homog_1(coefficients, degree, initial_terms, fn_part, highest_power_fn_part, filename, fn_part_sn):
    try:
        # First try this step automated
        sequence = "s(n)="
        i = 0
        for x in coefficients:
            if parse_expr(coefficients[i]) >= 0 and i == 0:
                sequence = sequence + "(" + str(coefficients[i]) + ")*s(n-" + str(i+1) + ")"
            # add a + for the positive coefficients
            elif parse_expr(coefficients[i]) >= 0:
                sequence = sequence + "+(" + str(coefficients[i]) + ")*s(n-" + str(i+1) + ")"
            elif parse_expr(coefficients[i]) < 0:
                sequence = sequence + "(" + str(coefficients[i]) + ")*s(n-" + str(i+1) + ")"
            else:
                print("wrong sequence step 1")
            i = i + 1

        sequence = sequence + "+" + str(fn_part) ################### loop and add with +
        print(color.GREEN + "Step 1: The rewritten sequence is: \n" + str(sequence) + "\n", color.RESET)

        # Ask if altering is needed
        print("Ignore the dictionary at the end pf the rewritten sequence")
        continue_or_not = input("Is this correct? (yes or no)\n")
        if continue_or_not == "yes":
            # print("Great!")
            manual_mode_non_homog_2(coefficients, degree, initial_terms, fn_part, filename, sequence, highest_power_fn_part, fn_part_sn)
        elif continue_or_not == "no":
            sequence = input("Give the relation manually:\n")

            # Confirm manual input or quit
            confirm_or_exit = input("Is this correct? (yes or no)\n")
            if confirm_or_exit == "yes":
                manual_mode_non_homog_2(coefficients, degree, initial_terms, fn_part, filename, sequence, highest_power_fn_part, fn_part_sn)
            else:
                print("Ending manual mode")
        else:
            print("Neither yes nor no given")

    except Exception as error:
        print("1 doesnt work, ERROR: {}\n".format(error))
        print(color.RED + "Error occurs in file: {}\n".format(filename), color.RESET)
        try:
            file_writer.error_in_file(filename=filename, homogeneous=True, step="Step 1", automatic=True, error=error)
        except Exception as error:
            print(color.RED + "Error during writing error file.\nHere is the data:\nFile: {}\nHomogeneous: {}\nStep: {}\nAutomatic: {}\nOrginal error: {}\n".format(filename, True, "Step 1", True, error))


# Step 2: Obtaining the characteristic equation  of the associated homog part
def manual_mode_non_homog_2(coefficients, degree, initial_terms, fn_part, filename, sequence, highest_power_fn_part, fn_part_sn):
    try:
        characteristic_equation = char_equation_2(coefficients)
        print("Step 2: The characteristic equation is: \n" + str(characteristic_equation) + "=0" + "\n")

        # Ask if altering is needed
        continue_or_not = input("Is this correct? (yes or no)\n")
        if continue_or_not == "yes":
            manual_mode_non_homog_3(coefficients, degree, initial_terms, fn_part, filename, sequence,
                                    highest_power_fn_part, fn_part_sn, characteristic_equation)
        elif continue_or_not == "no":
            characteristic_equation = input("Give the characteristic equation manually:\n")

            # Confirm manual input or quit
            confirm_or_exit = input("Is this correct? (yes or no)\n")
            if confirm_or_exit == "yes":
                manual_mode_non_homog_3(coefficients, degree, initial_terms, fn_part, filename, sequence,
                                        highest_power_fn_part, fn_part_sn, characteristic_equation)
            else:
                print("Ending manual mode")
        else:
            print("Neither yes nor no given")
    except Exception as error:
        print("2 doesnt work, shocker dude: ERROR: {}".format(error))


# Step 3: Obtain the roots  of the associated homog part
def manual_mode_non_homog_3(coefficients, degree, initial_terms, fn_part, filename, sequence, highest_power_fn_part,
                            fn_part_sn, characteristic_equation):
        try:
            r = symbols('r')
            r_and_m_found = roots(characteristic_equation, r)  # returns root:multiplicity
            print("Step 3: The roots of this equation are:")
            print(r_and_m_found)  # root:multiplicity
            print()

            # Ask if altering is needed
            continue_or_not = input("Is this correct? (yes or no)\n")
            if continue_or_not == "yes":
                manual_mode_non_homog_4(coefficients, degree, initial_terms, fn_part, filename, sequence,
                                        highest_power_fn_part, fn_part_sn, r_and_m_found)
            elif continue_or_not == "no":
                r_and_m_found = input("Give the roots and multiplicities manually:\n")
                confirm_or_exit = input("Is this correct? (yes or no)\n")
                if confirm_or_exit == "yes":
                    manual_mode_non_homog_4(coefficients, degree, initial_terms, fn_part, filename, sequence,
                                            highest_power_fn_part, fn_part_sn, r_and_m_found)
                else:
                    print("Ending manual mode")
            else:
                print("Neither yes nor no given")

        except Exception as error:
            print("3 doesnt work, shocker dude: ERROR: {}".format(error))


# Step 4: Obtain general solution of the associated homog part
def manual_mode_non_homog_4(coefficients, degree, initial_terms, fn_part, filename, sequence,
                                        highest_power_fn_part, fn_part_sn, r_and_m_found):
    try:
        general_solution = find_general_solution_2(r_and_m_found)
        general_solution = general_solution.replace("s(n)=+", "s(n)=")
        print("Step 4: The general solution of this equation is: \n" + str(general_solution) + "\n")

        # Ask if altering is needed
        continue_or_not = input("Is this correct? (yes or no)\n")
        if continue_or_not == "yes":
            manual_mode_non_homog_5(coefficients, degree, initial_terms, fn_part, filename, sequence,
                                    highest_power_fn_part, general_solution, r_and_m_found, fn_part_sn)
        elif continue_or_not == "no":
            general_solution = input("Give the general solution manually:\n")

            # Confirm manual input or quit
            confirm_or_exit = input("Is this correct? (yes or no)\n")
            if confirm_or_exit == "yes":
                manual_mode_non_homog_5(coefficients, degree, initial_terms, fn_part, filename, sequence,
                                        highest_power_fn_part, general_solution, r_and_m_found, fn_part_sn)
            else:
                print("Ending manual mode")
        else:
            print("Neither yes nor no given")

    except Exception as error:
        print("4 doesnt work, shocker dude: ERROR: {}".format(error))


# Step 5: Obtain the particular solution of the non-homog part
def manual_mode_non_homog_5(coefficients, degree, initial_terms, fn_parts, filename, sequence,
                                        highest_power_fn_part, general_solution, r_and_m_found, fn_part_sn):
    try:
        particular_solution = find_part_sol_non_homog(fn_parts, fn_part_sn, highest_power_fn_part, r_and_m_found,
                                                      degree, ordered_relation)
        print(
            "Step 5: The particular solution of the non-homog part is: \n" + "s(n)=" + str(particular_solution) + "\n")

        # Ask if altering is needed
        continue_or_not = input("Is this correct? (yes or no)\n")
        if continue_or_not == "yes":
            manual_mode_non_homog_6(coefficients, degree, initial_terms, fn_parts, filename, sequence,
                                    highest_power_fn_part, general_solution, r_and_m_found, particular_solution)
        elif continue_or_not == "no":
            particular_solution = input("Give the particular solution manually:\n")

            # Confirm manual input or quit
            confirm_or_exit = input("Is this correct? (yes or no)\n")
            if confirm_or_exit == "yes":
                manual_mode_non_homog_6(coefficients, degree, initial_terms, fn_parts, filename, sequence,
                                        highest_power_fn_part, general_solution, r_and_m_found, particular_solution)
            else:
                print("Ending manual mode")
        else:
            print("Neither yes nor no given")

    except Exception as error:
        print("5 doesnt work, shocker dude: ERROR: {}".format(error))


# Step 6: Obtain the solution a_n = a_n(p) + a_n(h)
def manual_mode_non_homog_6(coefficients, degree, initial_terms, fn_parts, filename, sequence,
                                        highest_power_fn_part, general_solution, r_and_m_found, particular_solution):
    try:
        general_solution = general_solution.replace("s(n)=", "")
        setup_spec_sol = "s(n)=" + particular_solution + "+" + general_solution  # for step 7.2
        print("Step 6: a_n = a_n(p) + a_n(h):\n" + "s(n)=" + particular_solution + "+" + general_solution + "\n")

        # Ask if altering is needed
        continue_or_not = input("Is this correct? (yes or no)\n")
        if continue_or_not == "yes":
            manual_mode_non_homog_71(coefficients, degree, initial_terms, r_and_m_found, filename, sequence,
                                    highest_power_fn_part, general_solution, setup_spec_sol, particular_solution)
        elif continue_or_not == "no":
            setup_spec_sol = input("Give the a_n solution manually:\n")

            # Confirm manual input or quit
            confirm_or_exit = input("Is this correct? (yes or no)\n")
            if confirm_or_exit == "yes":
                manual_mode_non_homog_71(coefficients, degree, initial_terms, r_and_m_found, filename, sequence,
                                        highest_power_fn_part, general_solution, setup_spec_sol, particular_solution)
            else:
                print("Ending manual mode")
        else:
            print("Neither yes nor no given")

    except Exception as error:
        print("6 doesnt work, shocker dude: ERROR: {}".format(error))


# Step 7.1: Obtain the alpha values with a_n(p) + a_n(h)
def manual_mode_non_homog_71(coefficients, degree, initial_terms, r_and_m_found, filename, sequence,
                                        highest_power_fn_part, general_solution, setup_spec_sol, particular_solution):
    try:
        outcome = find_alpha_values(initial_terms, r_and_m_found, particular_solution)
        print("Step 7.1: The value of the Alphas:")
        print(outcome)

        # Ask if altering is needed
        continue_or_not = input("Is this correct? (yes or no)\n")
        if continue_or_not == "yes":
            manual_mode_non_homog_72(setup_spec_sol, outcome)
        elif continue_or_not == "no":
            outcome = input("Give the a_n solution manually:\n")

            # Confirm manual input or quit
            confirm_or_exit = input("Is this correct? (yes or no)\n")
            if confirm_or_exit == "yes":
                manual_mode_non_homog_72(setup_spec_sol, outcome)
            else:
                print("Ending manual mode")
        else:
            print("Neither yes nor no given")

    except Exception as error:
        print("7.1 doesnt work, shocker dude: ERROR: {}".format(error))


# Step 7.2: Obtain specific solution
def manual_mode_non_homog_72(setup_spec_sol, outcome):
    try:
        # specific_solution = setup_spec_sol
        specific_solution = get_specific_solution(setup_spec_sol, outcome)
        print("\nStep 7.2: The specific solution for this equation is: \n" + str(specific_solution) + "\n")

        # Ask if altering is needed
        continue_or_not = input("Is this correct? (yes or no)\n")
        if continue_or_not == "yes":
            # manual_mode_non_homog_72(setup_spec_sol, outcome)
            print("Thanks for playing!")
        elif continue_or_not == "no":
            specific_solution = input("Give the a_n solution manually:\n")

            # Confirm manual input or quit
            confirm_or_exit = input("Is this correct? (yes or no)\n")
            if confirm_or_exit == "yes":
                print("given specific solution:\n")
                print(specific_solution)
            else:
                print("Ending manual mode")
        else:
            print("Neither yes nor no given")

    except Exception as error:
        print("7.2 doesnt work, shocker dude: ERROR: {}".format(error))

