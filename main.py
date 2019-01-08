#This programs triggers all the other scripts.
import os
import function_type
import file_reader, file_writer, file_remover
import glob
import answer_checker
from pathlib import Path
import hom_calling_test, nonhom_calling_test
import hom_step1, hom_step2, hom_step3, hom_step4, hom_step5
from Manual_mode import *
from colorama import Fore as color
import time
from answer_checker import *

def banner():
    path = os.path.dirname(os.path.realpath(__file__))
    print("This program is written by Rik van Brakel, Bjorn Kraal and Rico Janssen\n")
    print("This program derives a direct formula from a recurrence relation\n")
    print("\nWe have two categories; homogeneous equations and non-homogeneous equations:\n")

    print("For homogeneous equations we follow the following steps:\n")
    print("Step 1: Write the equation in general form, determine the degree and the coefficients.\n")
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
        print(color.RED + "Something went wrong in the file reader! \nError: {}\n".format(error),color.RESET)


def menu():
    #This function is the main menu for the program.
    # banner()
    try:
        print("""Menu, choose a number:\n
        1) Solve the equations automatically.\n
        2) Solve manually equations.\n
        3) Remove some files.\n
        4) Check outcomes of solutions and relations.\n
        5) Exit the program.\n""")
        choice = int(input("Enter your choice: "))
        # choice = 1
        if choice == 1:

            read_files()

            #For loop to find all commass files, then find the degree of all these files.
            # find_degree.find_degree(pathstring=)

            """Find all the commass files in the homogeneous folder"""

            hom_comass_path = str(os.path.dirname(os.path.realpath(__file__)) + str(Path("/output_files/homogeneous/comass[0-9][0-9].txt")))

            print(color.CYAN + "\n\nAUTOMATC READING HOMOGENEOUS EQUATION.\n\n", color.RESET)
            time.sleep(1)

            #Find every comass file in the /homogeneous/ folder. Then process the 5 steps for every file.
            for hom_comass_file in glob.glob(hom_comass_path):
                print(color.GREEN + "\nHomogeneous file {} found!\n".format(hom_comass_file), color.RESET)

                """The automatic mode uses the hom_calling_test.py file.
                THIS IS THE HOMOGENEOUS PART!"""
                """Move the files from the root folder, to the automatic folder."""
                file_writer.move_to_step(filename=hom_comass_file, homogeneous=True, step="automatic")
                degree = file_reader.read_lists_from_files(file_type="degree", filename=hom_comass_file, homogeneous=True, automatic=True, step=None)
                coefficients = file_reader.read_lists_from_files(file_type="coefficients", filename=hom_comass_file, homogeneous=True, automatic=True, step=None)
                initial_terms = file_reader.read_lists_from_files(file_type="init", filename=hom_comass_file, homogeneous=True, automatic=True, step=None)
                parts = file_reader.read_lists_from_files(file_type="parts", filename=hom_comass_file, homogeneous=True, automatic=True, step=None)

                print(color.MAGENTA + "Degree is: {}\nInitial terms are: {}\nCoefficients are: {}\nParts are: {}\n".format(degree,initial_terms,coefficients,parts),color.RESET)

                try:
                    hom_solution = hom_calling_test.solve_homog_relation(degree=degree, initial=initial_terms, parts=parts, coefficients=coefficients, filename=hom_comass_file)
                    try:
                        pass
                        # answer_checker.automatic_check_full_automatic(degree=degree, initial_terms=initial_terms,all_coefficient=coefficients, fn_part=None,homogeneous=True,specific_solution=hom_solution)
                    except IOError:
                        pass  # if there exist no comass file then continue because there are only few dir files.
                    except Exception as error:
                        print(color.RED + "Cannot check if answer is correct!\nERROR: {}\n".format(error))
                except Exception as error:
                    print(color.RED + "Error in hom_calling_test, try manually!\nERROR: {}\n".format(error), color.RESET)
                    try:
                        file_writer.error_in_file(filename=hom_comass_file, homogeneous=True, step=None, error=error, automatic=True)
                        print(color.LIGHTGREEN_EX + "Error file created!\n", color.RESET)
                    except Exception as error:
                        print(color.RED + "Can not create error file for: {}\nERROR: {}\n".format(hom_comass_file, error))


                """Find all the commass files in the nonhomogeneous folder"""
                nonhom_comass_path = str(os.path.dirname(os.path.realpath(__file__)) + str(Path("/output_files/nonhomogeneous/comass[0-9][0-9].txt")))

                print(color.CYAN + "\n\nAUTOMATC READING NON-HOMOGENEOUS EQUATION.\n\n", color.RESET)
                time.sleep(1)
                # Find every comass file in the /homogeneous/ folder. Then process the 5 steps for every file.
                for nonhom_comass_file in glob.glob(nonhom_comass_path):
                    print(color.GREEN + "\nNon-Homogeneous file {} found!\n".format(nonhom_comass_file), color.RESET)

                    """The automatic mode uses the hom_calling_test.py file.
                    THIS IS THE NON-HOMOGENEOUS PART!"""
                    """Move the files from the root folder, to the automatic folder."""
                    file_writer.move_to_step(filename=nonhom_comass_file, homogeneous=False, step="automatic")
                    degree = file_reader.read_lists_from_files(file_type="degree", filename=nonhom_comass_file,
                                                               homogeneous=False, automatic=True, step=None)
                    coefficients = file_reader.read_lists_from_files(file_type="coefficients", filename=nonhom_comass_file,
                                                                     homogeneous=False, automatic=True, step=None)
                    initial_terms = file_reader.read_lists_from_files(file_type="init", filename=nonhom_comass_file,
                                                                      homogeneous=False, automatic=True, step=None)
                    parts = file_reader.read_lists_from_files(file_type="parts", filename=nonhom_comass_file,
                                                              homogeneous=False, automatic=True, step=None)

                    fn_parts = file_reader.read_lists_from_files(file_type="fn_parts", filename=nonhom_comass_file,
                                                              homogeneous=False, automatic=True, step=None)

                    fn_parts_sn = file_reader.read_lists_from_files(file_type="fn_part_sn", filename=nonhom_comass_file,
                                                              homogeneous=False, automatic=True, step=None)

                    ordered_relation = file_reader.read_lists_from_files(file_type="ordered_relation", filename=nonhom_comass_file,
                                                              homogeneous=False, automatic=True, step=None)
                    print(
                        color.MAGENTA + "Degree is: {}\nInitial terms are: {}\nCoefficients are: {}\nParts are: {}\nfn_parts are: {}\nfn_parts_sn is: {}\nOrdered Realtion: {}\n".format(
                            degree, initial_terms, coefficients, parts, fn_parts, fn_parts_sn, ordered_relation), color.RESET)

                    try:
                        nonhom_solution = nonhom_calling_test.solve_nonhom_relations(filename=nonhom_comass_file, fn_parts=fn_parts, fn_part_sn=fn_parts_sn, degree=degree, initial_terms=initial_terms, homogeneous_coeffs=coefficients, ordered_relation=ordered_relation)

                        try:
                            pass
                            # answer_checker.automatic_check_full_automatic(degree=degree, initial_terms=initial_terms, all_coefficient=coefficients, fn_part=fn_parts, homogeneous=False, specific_solution=nonhom_solution)
                        except IOError:
                            pass #if there exist no comass file then continue because there are only few dir files.
                        except Exception as error:
                            print(color.RED + "Cannot check if answer is correct!\nERROR: {}\n".format(error))
                    except Exception as error:
                        print(color.RED + "Error in nonhom_calling_test, try manually!\nERROR: {}\n".format(error),
                              color.RESET)
                        try:
                            file_writer.error_in_file(filename=nonhom_comass_file, homogeneous=False, step=None,
                                                      error=error, automatic=True)
                            print(color.LIGHTGREEN_EX + "Error file created!\n", color.RESET)
                        except Exception as error:
                            print(color.RED + "Can not create error file for: {}\nERROR: {}\n".format(nonhom_comass_file,
                                                                                                    error))

        elif choice == 2:
            manual_mode(filename="empty")  # Is filename needed here? since it's manual

        elif choice == 3:
            print("Which files do you want to remove?.\n")
            print("""1) All files, including solutions.\n
            2) Error files.\n
            3) All files in a particular step.\n
            4) Remove all solutions.\n""")

            delete_choice = int(input("Enter your choice: "))
            if delete_choice == 1:
                file_remover.remove_all()
            elif delete_choice == 2:
                file_remover.remove_error()
            elif delete_choice == 3:
                homogeneous = bool(input("Is de folder homogeneous (True or False)?: "))
                folder = input("Type folder name: ")
                file_remover.remove_files_in_folder(homogeneous=homogeneous, folder=folder)
            elif delete_choice == 4:
                file_remover.remove_all_solutions()
        elif choice == 4:
            answer_check_manual_or_auto()

        elif choice == 5:
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