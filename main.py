#This programs triggers all the other scripts.
import os
import function_type
import file_reader, file_writer
import glob
import hom_step1, hom_step2, hom_step3, hom_step4, hom_step5
from colorama import Fore as color

def banner():
    path = os.path.dirname(os.path.realpath(__file__))
    print("This program is written by ...\n")
    print("This program derives a direct formula from a recurrence relation\n")
    print("\nWe have two categories; homogeneous equations and non-homogeneous equations:\n")

    print("For homogeneous equations we follow the following steps:\n")
    print("Step 1: \n")
    print("Step 2: \n")
    print("Step 3: \n")
    print("Step 4: \n")
    print("Step 5: \n")

    print("\nFor non-homogeneous equations we follow the following steps:\n")
    print("Step 1: \n")
    print("Step 2: \n")
    print("Step 3: \n")
    print("Step 4: \n")
    print("Step 5: \n")
    print("Step 6: \n")
    print("Step 7: \n")

    print("\n**Note that the input files should be in {}/input_files\n".format(path))

def read_files():
    print("We are going to read all the files...\n")
    try:
        file_reader.read_files()
    except Exception as error:
        print(color.RED + "Something went wrong! \nError: {}".format(error),color.RESET)

def menu():
    #This function is the main menu for the program.
    banner()

    read_files()

    #For loop to find all commass files, then find the degree of all these files.
    # find_degree.find_degree(pathstring=)

    """Find all the commass files in the homogeneous folder"""

    hom_comass_path = str(os.path.dirname(os.path.realpath(__file__)) + "/output_files/homogeneous/comass[0-9][0-9].txt")
    # print("\n\n\n\n\n This is the hom_comass path: {}\n\n\n\n".format(hom_comass_path))
    #Find every comass file in the /homogeneous/ folder. Then process the 5 steps for every file.
    for hom_comass_file in glob.glob(hom_comass_path):
        print(color.GREEN + "\nHomogeneous file {} found!\n".format(hom_comass_file), color.RESET)

        """Step 1"""
        try:
            """Determine the degree and write it to /output_files/homogeneous/step1/"""
            degree = hom_step1.find_degree(filename=hom_comass_file)
            file_writer.write_degree_to_file(filename=hom_comass_file, degree=degree, homogeneous=True)
            file_writer.move_homogeneous_step1(filename=hom_comass_file)
        except Exception as error:
            print(color.RED + "Error when determing the degree, file moved to error folder {}\n".format(error), color.RESET)


        """Step 2"""
        file = open(hom_comass_file, 'r')
        lines = file.readlines()
        equation = lines[0].strip("")
        if degree == 1:
            hom_step2.char_equation_1(first_term_in=equation)

    # #Determine if the function is an homogeneous or a non-homogeneous function
    # try:
    #     if function_type.type() == "homogeneous":
    #         print("The equation is homogeneous")
    #
    #     elif function_type.type() == "nonhomogeneous":
    #         print("The equation is non-homogeneous")

    # except:
    #     print("Error in type function: {}".format(Exception))
    #     print("There is an error in file: {}".format(function_type.type()))


menu()