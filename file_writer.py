"""This script can be used to write files. Each function can write different files"""

import file_reader
"""This function writes the initial terms to commass[0-9][0-9]_init.txt"""
def write_init_terms(filename, conditions):
    print(filename, conditions)
    init_filename = str(filename).strip('.txt') #Remove .txt from the filename
    init_file = open((init_filename + "_init.txt"), 'w') #Add _init.txt to the filename
    init_file.write(str(conditions)) #write the dictionary as a string to the file
    init_file.close()

"""Transforms the string equation, that is of the right side of the form "s(n) = ...",
    and wirtes it towards the file "filename", which also needs to contain the desired path."""
def write_output_to_file(filename, equation):
    nr_written_chars = 0
    with open(filename, "w") as output_file:
        nr_written_chars = output_file.write("sdir := n -> {0};\n".format(equation))
    # debug_print("Wrote {0} characters to file {1}.".format(str(nr_written_chars), filename))

"""This file writes the coefficients (given by file_reader.py) to a file"""
def write_coefficents_to_file(filename, coefficients):
    print(filename, coefficients)
    coef_filename = str(filename).strip('.txt') #Remove .txt from the filename
    coef_file = open((coef_filename + "_coefficents.txt"), 'w') #Add _init.txt to the filename
    coef_file.write(str(coefficients)) #write the dictionary as a string to the file
    coef_file.close()

"""Reformats the for Python needed syntax of equations back to specified output format:
    - "**" is transformed back to "^";
    - "sqrt(...)" is transformed back to "(...)^(1/2)".
    The return value is a string of the modified equation."""
def reformat_equation(equation):
    equation = equation.replace("**", "^")
    pos_sqrt = equation.find("sqrt(")
    while pos_sqrt >= 0:
        pos_end = file_reader.search_right_term_end(equation, pos_sqrt, ["+", "-", "*", "/"])
        equation = "{0}^(1/2){1}".format(equation[0:pos_end + 1], equation[pos_end + 1:])
        equation = equation.replace("sqrt", "", 1)
        pos_sqrt = equation.find("sqrt(")
    return equation

#This function reformats the equation to its original form and writes it to a file.
def write_dir_files(final_equation, filename):
    #First transform the equation to its original form
    reformat_equation(equation=final_equation)

    file = open(filename, 'w')

    file.write(str(final_equation))
    file.close()
