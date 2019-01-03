#This programs triggers all the other scripts.
import os
import function_type
import file_reader, file_writer, file_remover
import glob
import hom_calling_test, nonhom_calling_test
import hom_step1, hom_step2, hom_step3, hom_step4, hom_step5
from colorama import Fore as color
import time

def banner():
    path = os.path.dirname(os.path.realpath(__file__))
    print("This program is written by ...\n")
    print("This program derives a direct formula from a recurrence relation\n")
    print("\nWe have two categories; homogeneous equations and non-homogeneous equations:\n")

    print("For homogeneous equations we follow the following steps:\n")
    print("Step 1: Write the equation in general form, determine the degree and the coefficients. \n")
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
        print(color.RED + "Something went wrong in the file reader! \nError: {}".format(error),color.RESET)


def menu():
    #This function is the main menu for the program.
    banner()
    try:
        print("""Menu, choose a number:\n
        1) Solve the equations automatically.\n
        2) Solve manually equations (NOT READY).\n
        3) Remove some files.\n
        4) Exit the program.\n""")
        choice = int(input("Enter your choice: "))
        # choice = 1
        if choice == 1:

            read_files()

            #For loop to find all commass files, then find the degree of all these files.
            # find_degree.find_degree(pathstring=)

            """Find all the commass files in the homogeneous folder"""

            hom_comass_path = str(os.path.dirname(os.path.realpath(__file__)) + "/output_files/homogeneous/comass[0-9][0-9].txt")
            # print("\n\n\n\n\n This is the hom_comass path: {}\n\n\n\n".format(hom_comass_path))
            #Find every comass file in the /homogeneous/ folder. Then process the 5 steps for every file.
            for hom_comass_file in glob.glob(hom_comass_path):
                print(color.GREEN + "\nHomogeneous file {} found!\n".format(hom_comass_file), color.RESET)

                """The automatic mode uses the hom_calling_test.py file.
                THIS IS THE HOMOGENEOUS PART!"""

                """Move the files from the root folder, to the automatic folder."""
                file_writer.move_to_step(filename=hom_comass_file, homogeneous=True, step="automatic")
                # degree = file_reader.read_lists_from_files(file_type="degree", filename=hom_comass_file, homogeneous=True, automatic=True, step=None)
                coefficients = file_reader.read_lists_from_files(file_type="coefficients", filename=hom_comass_file, homogeneous=True, automatic=True, step=None)
                initial_terms = file_reader.read_lists_from_files(file_type="init", filename=hom_comass_file, homogeneous=True, automatic=True, step=None)
                parts = file_reader.read_lists_from_files(file_type="parts", filename=hom_comass_file, homogeneous=True, automatic=True, step=None)

                print(color.MAGENTA + "Degree is: {}\nInitial terms are: {}\nCoefficients are: {}\nParts are: {}".format("unknown",initial_terms,coefficients,parts),color.RESET)

                try:
                    hom_calling_test.solve_homog_relation(degree="", initial=initial_terms, parts=parts, coefficients=coefficients, filename=hom_comass_file)

                except Exception as error:
                    print(color.RED + "Error in hom_calling_test, try manually!\nERROR: {}".format(error), color.RESET)
                    try:
                        file_writer.error_in_file(filename=hom_comass_file, homogeneous=True, step=None, error=error, automatic=True)
                        print(color.LIGHTGREEN_EX + "Error file created!\n", color.RESET)
                    except Exception as error:
                        print(color.RED + "Can not create error file for: {}\nERROR: {}".format(hom_comass_file, error))

                # try:
                #     """Determine the degree and write it to /output_files/homogeneous/step1/"""
                #     degree = hom_step1.find_degree(filename=hom_comass_file)
                #     file_writer.write_degree_to_file(filename=hom_comass_file, degree=degree, homogeneous=True)
                #     file_writer.move_to_step(filename=hom_comass_file, homogeneous=True, step="step1")
                #     #Remove all the moved files
                #     try:
                #         print("")
                #         file_remover.remove_file(filename=hom_comass_file)
                #     except Exception:
                #         continue
                # except Exception as error:
                #     print(color.RED + "Error when determine the degree, file moved to error folder {}\n".format(error), color.RESET)


                """Step 2"""
                # file = open(hom_comass_file, 'r')
                # lines = file.readlines()
                # equation = lines[0].strip("")
                # if degree == 1:
                #     hom_step2.char_equation_1(first_term_in=equation)

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

        elif choice == 2:
            print("You entered manual mode.\nThis mode is not implemented yet.\n")
        elif choice == 3:
            print("Which files do you want to remove?.\n")
            print("""1) All files, including solutions.\n
            2) Error files.\n
            3) All files in a particular step.""")
            delete_choice = int(input("Enter your choice: "))
            if delete_choice == 1:
                file_remover.remove_all()
            elif delete_choice == 2:
                file_remover.remove_error()
            elif delete_choice == 3:
                homogeneous = bool(input("Is de folder homogeneous (True or False)?: "))
                folder = input("Type folder name: ")
                file_remover.remove_files_in_folder(homogeneous=homogeneous, folder=folder)

        elif choice == 4:
            print("Closing program, BYE!\n")
            exit()
        else:
            print("This number is unknown.\n")
            exit()

    except IOError as error:
        print(color.RED + "Cannot find file: {}\n".format(error), color.RESET)
        time.sleep(2)
        menu()
    except ValueError:
        print(color.RED + "Only integers allowed!\n", color.RESET)
        time.sleep(2)
        menu()
while True:
    menu()