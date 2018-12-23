import os
import glob

global homogeneous
global path

#pathstring = str(os.path.dirname(os.path.realpath(__file__)) + "/input_files/comass[0-9][0-9].txt")
pathstring = str(os.path.dirname(os.path.realpath(__file__)) + "/input_files/comass16.txt")
path = glob.glob(pathstring)
degree = 0

def find_degree(pathstring, degree):
    file = open(pathstring, 'r')
    j = 0

    for i, line in enumerate(file):
        if i == 2:
            print(line)
            num = 15 #hardcoded 15 which is getting looped over untill it hits 0

            while j < num:
                string = "(n-" + str(num) + ")"
                print("string =" + string)
                print("FOUND = " + str(line.find(string)))
                if line.find(string) is not -1:
                    if num > degree:
                        degree = num
                        num = num-1
                    else:
                        num = num-1
                    print(string)
                    num = int(num)-1
                else:
                    num = num-1
            print("degree = " + str(degree))
            break
        else:
            continue
    return degree

the_degree = find_degree(pathstring=pathstring, degree=0)
print("found degree = " + str(the_degree))
