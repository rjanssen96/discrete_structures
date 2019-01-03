import os
from colorama import Fore as color
# from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from hom_step2 import *

def manual_mode():
    hom_or_non = input("Is it a homogeneous (h) or non-homogeneous (n) relation?\n")

    if hom_or_non == "h":
        print("You choose homogeneous")
        manual_mod_homog_0()
    elif hom_or_non == "n":
        print("You choose non-homogeneous")
        manual_mode_non_homog_0()
    else:
        print("Wrong input m8...")

    # print("Hey Boiiii")


def manual_mod_homog_0():
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
        manual_mod_homog_1(coefficients, initial_terms, degree)
    elif continue_or_not == "no":
        print("Ok let's try again")
        manual_mod_homog_0()
    else:
        print("Neither yes nor no was input...")


# Step 1
def manual_mod_homog_1(coefficients, initial_terms, degree):
    # Step 1: Rewriting the sequence
    # Maybe replace this part with now Rico's read parts added together from the dictionary sort result?
    try:
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

        continue_or_not = input("Is this correct? (yes or no)\n")
        if continue_or_not == "yes":
            # print("Great!")
            manual_mode_homg_2(coefficients, initial_terms, degree, sequence)
        elif continue_or_not == "no":
            sequence = input("Give the relation manually:")
            manual_mode_homg_2(coefficients, initial_terms, degree, sequence)
        else:
            print("Neither yes nor no given")

    except Exception as error:
        print("1 doesnt work, ERROR: {}\n".format(error))
    #     print(color.RED + "Error occurs in file: {}\n".format(filename), color.RESET)
    #     try:
    #         file_writer.error_in_file(filename=filename, homogeneous=True, step="Step 1", automatic=True, error=error)
    #     except Exception as error:
    #         print(color.RED + "Error during writing error file.\nHere is the data:\nFile: {}\nHomogeneous: {}\nStep: {}\nAutomatic: {}\nOrginal error: {}\n".format(filename, True, "Step 1", True, error))


def manual_mode_homg_2(coefficients, initial_terms, degree, sequence):
    # Step 2: Obtaining the characteristic equation
    try:
        characteristic_equation = char_equation_2(coefficients)
        print("Step 2: The characteristic equation is: \n" + str(characteristic_equation) + "=0" + "\n")
    except Exception as error:
        print("2 doesnt work, shocker dude")
        print("1 doesnt work, ERROR: {}\n".format(error))

    continue_or_not = input("Is this correct? (yes or no)\n")
    if continue_or_not == "yes":
        print("Great!")
        # manual_mode_homg_2(coefficients, initial_terms, degree, sequence)
    elif continue_or_not == "no":
        print("Damn!")
    else:
        print("Neither yes nor no given")


def manual_mode_non_homog_0():
    print("Go away!")

