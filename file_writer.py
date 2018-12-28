"""This script can be used to write files. Each function can write different files"""
import os
from shutil import copyfile #Library to copy files

"""This function writes the initial terms to commass[0-9][0-9]_init.txt"""
def write_init_terms(filename, conditions):
    print(filename, conditions)
    init_filename = str(filename).strip('.txt') #Remove .txt from the filename
    init_file = open((init_filename + "_init.txt"), 'w') #Add _init.txt to the filename
    init_file.write(str(conditions)) #write the ordere list of initial terms to a file
    init_file.close()

"""Transforms the string equation, that is of the right side of the form "s(n) = ...",
    and wirtes it towards the file "filename", which also needs to contain the desired path."""
def write_output_to_file(filename, equation):
    nr_written_chars = 0
    with open(filename, "w") as output_file:
        nr_written_chars = output_file.write("sdir := n -> {0};\n".format(equation))
    # debug_print("Wrote {0} characters to file {1}.".format(str(nr_written_chars), filename))

"""This file writes the coefficients (given by file_reader.py) to a file"""
def write_coefficients_to_file(filename, coefficients, polynomials):
    print("We will write the following data to the file {} \nCoefficients: {} \nPolynomials: {}".format(filename, coefficients,polynomials))
    coef_filename = str(filename).strip('.txt') #Remove .txt from the filename
    coef_file = open((coef_filename + "_coefficients.txt"), 'w') #Add _coefficients.txt to the filename
    coef_file.write("{},{}".format(coefficients,polynomials)) #Write the ordered sets to the file
    coef_file.close()

def write_degree_to_file(filename, degree):
    print("We will write the following data to the file {} \nDegree: {}\n".format(filename,degree))
    coef_filename = str(filename).strip('.txt')  # Remove .txt from the filename
    coef_file = open((coef_filename + "_degree.txt"), 'w')  # Add _degree.txt to the filename
    coef_file.write("{}".format(degree))  # Write the ordered sets to the file
    coef_file.close()

def move_homogeneous_files(filename):
    #find commass files for that homogeneous equation
    commass_file = filename
    commass_file_homogeneous = str(filename).replace("/input_files", "/output_files/homogeneous/")
    print("We move the homogeneous file: {}\nTo: {}".format(commass_file, commass_file_homogeneous))

    coefficients_file = str(filename).strip('.txt') + "_coefficients.txt"
    coefficients_file_homogeneous = str(str(filename).strip('.txt') +"_coefficients.txt").replace("/input_files", "/output_files/homogeneous/")
    print("We move the homogeneous file: {}\nTo: {}".format(coefficients_file, coefficients_file_homogeneous))


    initial_file = str(filename).strip('.txt') + "_init.txt"
    initial_file_homogeneous = str(str(filename).strip('.txt') +"_init.txt").replace("/input_files", "/output_files/homogeneous/")
    print("We move the homogeneous file: {}\nTo: {}".format(initial_file, initial_file_homogeneous))


    degree_file = str(filename).strip('.txt') + "_degree.txt"
    degree_file_homogeneous = str(str(filename).strip('.txt') +"_degree.txt").replace("/input_files", "/output_files/homogeneous/")
    print("We move the homogeneous file: {}\nTo: {}".format(degree_file, degree_file_homogeneous))


    #Copy the files to the homogeneous folder
    copyfile(commass_file, commass_file_homogeneous)
    copyfile(coefficients_file, coefficients_file_homogeneous)
    copyfile(initial_file, initial_file_homogeneous)
    copyfile(degree_file, degree_file_homogeneous)


def move_nonhomogeneous_files(filename):
    #find commass files for that non-homogeneous equation
    commass_file = filename
    commass_file_nonhomogeneous = str(filename).replace("/input_files", "/output_files/nonhomogeneous/")
    print("We move the non-homogeneous file: {}\nTo: {}".format(commass_file, commass_file_nonhomogeneous))

    coefficients_file = str(filename).strip('.txt') + "_coefficients.txt"
    coefficients_file_nonhomogeneous = str(str(filename).strip('.txt') +"_coefficients.txt").replace("/input_files", "/output_files/nonhomogeneous/")
    print("We move the non-homogeneous file: {}\nTo: {}".format(coefficients_file, coefficients_file_nonhomogeneous))


    initial_file = str(filename).strip('.txt') + "_init.txt"
    initial_file_nonhomogeneous = str(str(filename).strip('.txt') +"_init.txt").replace("/input_files", "/output_files/nonhomogeneous/")
    print("We move the non-homogeneous file: {}\nTo: {}".format(initial_file, initial_file_nonhomogeneous))


    degree_file = str(filename).strip('.txt') + "_degree.txt"
    degree_file_nonhomogeneous = str(str(filename).strip('.txt') +"_degree.txt").replace("/input_files", "/output_files/nonhomogeneous/")
    print("We move the nonhomogeneous file: {}\nTo: {}".format(degree_file, degree_file_nonhomogeneous))


    #Copy the files to the non-homogeneous folder
    copyfile(commass_file, commass_file_nonhomogeneous)
    copyfile(coefficients_file, coefficients_file_nonhomogeneous)
    copyfile(initial_file, initial_file_nonhomogeneous)
    copyfile(degree_file, degree_file_nonhomogeneous)

"""Reformats the for Python needed syntax of equations back to specified output format:
    - "**" is transformed back to "^";
    - "sqrt(...)" is transformed back to "(...)^(1/2)".
    The return value is a string of the modified equation."""
# def reformat_equation(equation):
#     equation = equation.replace("**", "^")
#     pos_sqrt = equation.find("sqrt(")
#     while pos_sqrt >= 0:
#         pos_end = file_reader.search_right_term_end(equation, pos_sqrt, ["+", "-", "*", "/"])
#         equation = "{0}^(1/2){1}".format(equation[0:pos_end + 1], equation[pos_end + 1:])
#         equation = equation.replace("sqrt", "", 1)
#         pos_sqrt = equation.find("sqrt(")
#     return equation

#This functions writes homogeneous files to the homogeneous folder and nonhomogeneous to the nonhomogeneous folder
# def write_type_file():

#This function reformats the equation to its original form and writes it to a file.
# def write_dir_files(final_equation, filename):
#     #First transform the equation to its original form
#     reformat_equation(equation=final_equation)
#
#     file = open(filename, 'w')
#
#     file.write(str(final_equation))
#     file.close()
