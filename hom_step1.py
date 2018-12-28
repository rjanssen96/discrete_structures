import glob
import os
# global homogeneous
# global path

# #pathstring = str(os.path.dirname(os.path.realpath(__file__)) + "/input_files/comass[0-9][0-9].txt")
# pathstring = str(os.path.dirname(os.path.realpath(__file__)) + "/input_files/comass33.txt")
# path = glob.glob(pathstring)
#
# def find_degree():
#     string = "(n-"
#     file = open(str(pathstring), 'r')
#     for i in
#
#
#     print("yay")
#
# find_degree()


def find_degree(filename):
    file = open(filename, 'r')
    degree = 0
    j = 0

    for i, line in enumerate(file):
        if i == 2:
            print(line)
            num = 15  # hardcoded 15 which is getting looped over untill it hits 0

            while j < num:
                string = "(n-" + str(num) + ")"
                print("string =" + string)
                print("FOUND = " + str(line.find(string)))
                if line.find(string) is not -1:
                    if num > degree:
                        degree = num
                        num = num - 1
                    else:
                        num = num - 1
                    print(string)
                    num = int(num) - 1
                else:
                    num = num - 1
            print("Degree = {}\n".format(degree))
            break
        else:
            continue
    #Write degree to file using file_writer.py
