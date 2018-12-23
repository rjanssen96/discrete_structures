import glob
import os
global homogeneous
global path

#pathstring = str(os.path.dirname(os.path.realpath(__file__)) + "/input_files/comass[0-9][0-9].txt")
pathstring = str(os.path.dirname(os.path.realpath(__file__)) + "/input_files/comass33.txt")
path = glob.glob(pathstring)

def find_degree():
    string = "(n-"
    file = open(str(pathstring), 'r')
    for i in


    print("yay")

find_degree()