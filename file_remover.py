import os, file_writer, glob, os.path
from colorama import Fore as color
from pathlib import Path

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

"""This function removes all files. This includes files in the non and homogeneous folder, error folders and step folders"""
def remove_all():
    homogeneous_folder = str(Path("/homogeneous/"))
    homogeneous_automatic = homogeneous_folder + str(Path("automatic/"))
    homogeneous_error = homogeneous_folder + str(Path("error/"))
    homogeneous_step1 = homogeneous_folder + str(Path("step1/"))
    homogeneous_step2 = homogeneous_folder + str(Path("step2/"))
    homogeneous_step3 = homogeneous_folder + str(Path("step3/"))
    homogeneous_step4 = homogeneous_folder + str(Path("step4/"))
    homogeneous_step5 = homogeneous_folder + str(Path("step5/"))

    nonhomogeneous_folder = str(Path("/nonhomogeneous/"))
    nonhomogeneous_automatic = homogeneous_folder + str(Path("automatic/"))
    nonhomogeneous_error = nonhomogeneous_folder + str(Path("error/"))
    nonhomogeneous_step1 = nonhomogeneous_folder + str(Path("step1/"))
    nonhomogeneous_step2 = nonhomogeneous_folder + str(Path("step2/"))
    nonhomogeneous_step3 = nonhomogeneous_folder + str(Path("step3/"))
    nonhomogeneous_step4 = nonhomogeneous_folder + str(Path("step4/"))
    nonhomogeneous_step5 = nonhomogeneous_folder + str(Path("step5/"))
    nonhomogeneous_step6 = nonhomogeneous_folder + str(Path("step6/"))
    nonhomogeneous_step7 = nonhomogeneous_folder + str(Path("step7/"))

    solution_folder = str(Path("/solutions/"))
    folder_list = [homogeneous_folder, homogeneous_automatic, homogeneous_error, solution_folder, homogeneous_step1, homogeneous_step2, homogeneous_step3, homogeneous_step4, homogeneous_step5, nonhomogeneous_folder, nonhomogeneous_automatic, nonhomogeneous_error, nonhomogeneous_step1, nonhomogeneous_step2, nonhomogeneous_step3, nonhomogeneous_step4, nonhomogeneous_step5, nonhomogeneous_step6, nonhomogeneous_step7]

    for folder in folder_list:
        path = str(os.path.dirname(os.path.realpath(__file__)) + str(Path("/output_files/{}/comass[0-9][0-9]*.txt".format(folder))))

        for file in glob.glob(path):
            os.remove(file)
            print(color.GREEN +"File deleted: {}".format(file), color.RESET)

    input_files = str(os.path.dirname(os.path.realpath(__file__)) + str(Path("/input_files/comass[0-9][0-9]_*.txt")))
    for file in glob.glob(input_files):
        os.remove(file)
        print(color.GREEN + "File deleted: {}".format(file), color.RESET)

def remove_error():
    homogeneous_folder = str(Path("/homogeneous/"))
    homogeneous_error = str(Path(homogeneous_folder + "error/"))
    nonhomogeneous_folder = str(Path("/nonhomogeneous/"))
    nonhomogeneous_error = str(Path(homogeneous_folder + "error/"))


    folder_list = [homogeneous_error, nonhomogeneous_error]

    for folder in folder_list:
        path = str(os.path.dirname(os.path.realpath(__file__)) + str(Path("/output_files/{}/comass[0-9][0-9]*.txt".format(folder))))
        for file in glob.glob(path):

            os.remove(file)
            print(color.GREEN +"File deleted: {}".format(file), color.RESET)

def remove_files_in_folder(homogeneous, folder):
    if homogeneous == True:
        hom_folder = str(Path("/homogeneous/"))
    elif homogeneous == False:
        hom_folder = str(Path("/nonhomogeneous/"))
    else:
        print(color.RED + "ERROR: wrong homogeneous value\n", color.RESET)

    delete_folder = hom_folder + "{}".format(folder)
    path = str(os.path.dirname(os.path.realpath(__file__)) + str(Path("/output_files/{}/comass[0-9][0-9]*.txt".format((delete_folder)))))
    for file in glob.glob(path):
        os.remove(file)
        print(color.GREEN + "File deleted: {}\n".format(file), color.RESET)

def remove_all_solutions():
    input_files = str(os.path.dirname(os.path.realpath(__file__)) + str(Path("/output_files/solutions/comass[0-9][0-9]*.txt")))
    for file in glob.glob(input_files):
        os.remove(file)
        print(color.GREEN + "File deleted: {}".format(file), color.RESET)