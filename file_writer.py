"""This script can be used to write files. Each function can write different files"""
import os
from shutil import copyfile #Library to copy files
from colorama import Fore as color



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
    print("We will write the following data to the file {} \nCoefficients: {} \nPolynomials: {}\n".format(filename, coefficients,polynomials))
    coef_filename = str(filename).strip('.txt') #Remove .txt from the filename
    coef_file = open((coef_filename + "_coefficients.txt"), 'w') #Add _coefficients.txt to the filename
    coef_file.write("{},{}".format(coefficients,polynomials)) #Write the ordered sets to the file
    coef_file.close()

def write_degree_to_file(filename, degree, homogeneous):
    print("We will write the following data to the file {} \nDegree: {}\n".format(filename,degree))
    """The if statements determine the correct folder for the files"""
    folder = locate_folder(homogeneous=homogeneous)
    try:
        coef_filename = str(str(filename).strip('.txt')).replace("/{}/".format(folder), "/{}/step1/".format(folder))  # Remove .txt from the filename
        coef_file = open((coef_filename + "_degree.txt"), 'w')  # Add _degree.txt to the filename
        coef_file.write("{}".format(degree))  # Write the ordered sets to the file
        coef_file.close()
    except Exception as error:
        print("Cannot write the degree to a file.\nERROR: {}".format(error))

def write_equation(filename, equation):
    try:
        print(color.CYAN + "FILENAME AND EQUATION: {}, {}\n".format(filename, equation), color.RESET)
        equation = str(equation).strip("s(n)=")
        file = str(str(filename).strip('.txt') +"_equation.txt")
        equation_file = open(file, 'w')
        equation_file.write(equation)
        equation_file.close()
    except Exception as error:
        print(color.RED + "ERROR while write equation file: {}\n".format(error), color.RESET)

"""This function determs if the homogeneous parameter is True or False.
Based on this parameter the foldername will be decided by the other functions."""
def locate_folder(homogeneous):
    try:
        if homogeneous == True:
            folder = "homogeneous"
        elif homogeneous == False:
            folder = "nonhomogeneous"
    except Exception as error:
        print("ERROR, add the homogeneous parameter to the function call. {}\n".format(error))

    return folder

def move_files_based_on_type(filename, homogeneous):
    folder = locate_folder(homogeneous=homogeneous)
    #find commass files for that homogeneous equation
    commass_file = filename
    commass_file_homogeneous = str(filename).replace("/input_files", "/output_files/{}/".format(folder))
    print("We move the homogeneous file: {}\nTo: {}\n".format(commass_file, commass_file_homogeneous))

    """The strip statement removes .txt from the input file, which is the comass[0-9][0-9].txt file.
    Then adds the different variations to the filenames to locate these other files."""
    coefficients_file = str(filename).strip('.txt') + "_coefficients.txt"
    coefficients_file_type = str(str(filename).strip('.txt') +"_coefficients.txt").replace("/input_files", "/output_files/{}/".format(folder))
    print("We move the {} file: {}\nTo: {}\n".format(folder, coefficients_file, coefficients_file_type))


    initial_file = str(filename).strip('.txt') + "_init.txt"
    initial_file_type = str(str(filename).strip('.txt') +"_init.txt").replace("/input_files", "/output_files/{}/".format(folder))
    print("We move the {} file: {}\nTo: {}\n".format(folder, initial_file, initial_file_type))


    degree_file = str(filename).strip('.txt') + "_degree.txt"
    degree_file_type = str(str(filename).strip('.txt') +"_degree.txt").replace("/input_files", "/output_files/{}/".format(folder))
    print("We move the {} file: {}\nTo: {}\n".format(folder, degree_file, degree_file_type))

    equation_file = str(filename).strip('.txt') + "_equation.txt"
    equation_file_type = str(str(filename).strip('.txt') +"_equation.txt").replace("/input_files", "/output_files/{}/".format(folder))
    print("We move the {} file: {}\nTo: {}\n".format(folder, equation_file, equation_file_type))

    #Copy the files to the homogeneous folder
    copyfile(commass_file, commass_file_homogeneous)
    copyfile(coefficients_file, coefficients_file_type)
    copyfile(initial_file, initial_file_type)
    copyfile(degree_file, degree_file_type)
    copyfile(equation_file, equation_file_type)

"""Move homogeneous files to step 1."""
def move_to_step(filename, homogeneous, step):
    folder = locate_folder(homogeneous=homogeneous)
    try:
        """Move the comass file to the given step folder."""
        step1_comass_file = str(filename).replace("/{}/".format(folder), "/{}/{}/".format(folder, step))
        copyfile(filename, step1_comass_file)

        """Move the associated coefficients file to given step folder."""
        step1_coef_file = str(filename).replace("/{}/".format(folder), "/{}/{}/".format(folder,step))
        orinial_coef_file = str(filename).replace(".txt", "_coefficients.txt")
        step1_coef_file = step1_coef_file.replace(".txt", "_coefficients.txt")
        copyfile(orinial_coef_file, step1_coef_file)

        """Move the associated init file to the given step folder."""
        step1_init_file = str(filename).replace("/{}/".format(folder), "/{}/{}/".format(folder,step))
        orinial_init_file = str(filename).replace(".txt", "_init.txt")
        step1_init_file = step1_init_file.replace(".txt", "_init.txt")
        copyfile(orinial_init_file, step1_init_file)

        """Move the associated equation file to the given step folder."""
        step1_equation_file = str(filename).replace("/{}/".format(folder), "/{}/{}/".format(folder, step))
        orinial_equation_file = str(filename).replace(".txt", "_equation.txt")
        step1_equation_file = step1_equation_file.replace(".txt", "_equation.txt")
        copyfile(orinial_equation_file, step1_equation_file)

    except IOError:
        print(color.RED + "File missing {}\n".format(filename), color.RESET)
    except Exception as error:
        print(color.RED + "General error when moving file from {} folder to {}: \n{}".format(folder, error, step), color.RESET)


"""Move nonhomogeneous files to the nonhomogeneous folder."""
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

    equation_file = str(filename).strip('.txt') + "_equation.txt"
    equation_file_nonhomogeneous = str(str(filename).strip('.txt') + "_equation.txt").replace("/input_files","/output_files/nonhomogeneous/")
    print("We move the nonhomogeneous file: {}\nTo: {}\n".format(equation_file, equation_file_nonhomogeneous))

    #Copy the files to the non-homogeneous folder
    copyfile(commass_file, commass_file_nonhomogeneous)
    copyfile(coefficients_file, coefficients_file_nonhomogeneous)
    copyfile(initial_file, initial_file_nonhomogeneous)
    copyfile(degree_file, degree_file_nonhomogeneous)
    copyfile(equation_file, equation_file_nonhomogeneous)


"""This function moves the error files to the error folder and adds the error to the file."""
def error_in_file(filename, homogeneous, step, error):
    folder = locate_folder(homogeneous=homogeneous)
    error_file = open(filename, 'a')
    error_file.write("""Error in step: {}""".format(step))
    error_file.write("""Error: {}""".format(error))
    error_file.close()
    """Specify the error folder"""
    error_folder = str(filename).replace("/{}/".format(folder),"/{}/error/".format(folder))
    copyfile(filename, error_folder)



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
