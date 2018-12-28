import os, file_writer
from colorama import Fore as color

"""This function removes al the files associated to the given comass file."""
def remove_file(filename):# homogeneous, step):
    # folder = file_writer.locate_folder(homogeneous=homogeneous)
    #
    # try:
    #     if step == None and homogeneous == None:
    #         #If no step or type is specified, then take the input filename
    #         filename = filename
    #     elif step != None:
    #         filename = str(filename).replace("")
    #
    #     filename = str(filename).replace("/")
    #     print(color.BLUE +"The filename is: {}\n".format(filename), color.RESET)
    # except Exception as error:
    #     print("Error while removing file: {}\n{}\n".format(filename, error))
    try:
        comass_file = filename
        coefficients_file = str(filename).replace(".txt", "_coefficients.txt")
        init_file = str(filename).replace(".txt", "_init.txt")
        equation = str(filename).replace(".txt", "_equation.txt")
        degree = str(filename).replace(".txt", "_degree.txt")
        os.remove(comass_file)
        os.remove(coefficients_file)
        os.remove(init_file)
        os.remove(equation)
        os.remove(degree)

    except IOError:
        print(color.RED + "Cannot remove file, because it cannot be found\nFILE:{}".format(filename), color.RESET)
    except Exception as error:
        print(color.RED + "Error when removing file: {}\nERROR:{}".format(filename, error), color.RESET)