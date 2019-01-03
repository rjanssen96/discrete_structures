import os
from colorama import Fore as color
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from hom_step2 import *
from hom_step4 import *
from hom_step5 import *
import file_writer


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

    # print("Hey Boiiii")


def manual_mod_homog_0(filename):
    # Gathering correct input
    print("Make sure you add the following information in the correct order!!!")
    print("So coefficient of part one, then of part two, etc.")
    print("Also give fractions as 5/4 not (5/4)!!!")

    degree = int(input("What is the DEGREE of this relation?\n"))
    coefficients = []

    for x in range(0, degree):
        coefficients = coefficients + [input("What is coefficients number " + str(x) + "\n")]

    print("List of coeffs:")
    print(coefficients)

    initial_terms = []

    for x in range(0, degree):
        initial_terms = initial_terms + [parse_expr(input("What is initial_terms number " + str(x) + "\n"))]

    print("List of initial_terms:")
    print(initial_terms)

    continue_or_not = input("Are these lists correct? (yes or no)\n")
    if continue_or_not == "yes":
        print("Ok next")
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
            manual_mode_homog_2(coefficients, initial_terms, degree, sequence, filename)
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
            manual_mode_homog_3(coefficients, initial_terms, degree, characteristic_equation, filename)
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
            r_and_m_found = input("Manually input the root and multiplicity values:\n")
            manual_mode_homog_4(coefficients, initial_terms, degree, r_and_m_found, filename)
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
            manual_mode_homog_51(coefficients, initial_terms, degree, r_and_m_found, general_solution, filename)
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
        outcome = find_alpha_values(initial_terms, r_and_m_found)
        print("\nStep 5.1: The value of the Alphas:")
        print(outcome)

        # Ask if altering is needed
        continue_or_not = input("Is this correct? (yes or no)\n")
        if continue_or_not == "yes":
            manual_mode_homog_52(general_solution, outcome, filename)
        elif continue_or_not == "no":
            outcome = input("Manually input the alpha values:\n")
            manual_mode_homog_52(general_solution, outcome, filename)
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


def manual_mode_non_homog_0():
    print("Go away!")

