#This programs triggers all the other scripts.
import os
import function_type
import file_reader
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
        print("Something went wrong! \nError: {}".format(error))

def menu():
    #This function is the main menu for the program.
    banner()
    read_files()
    #Determine if the function is an homogeneous or a non-homogeneous function
    try:
        if function_type.type() == "homogeneous":
            print("The equation is homogeneous")

        elif function_type.type() == "nonhomogeneous":
            print("The equation is non-homogeneous")

    except:
        print("Error in type function: {}".format(Exception))
        print("There is an error in file: {}".format(function_type.type()))


menu()