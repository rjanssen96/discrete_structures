import os
import glob

global homogeneous
global path

#pathstring = str(os.path.dirname(os.path.realpath(__file__)) + "/input_files/comass[0-9][0-9].txt")
#pathstring = str(os.path.dirname(os.path.realpath(__file__)) + "/input_files/comass33.txt")
#path = glob.glob(pathstring)

def find_n(s,ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def find_type(homogeneous, path):
    pathstring = str(path)
    print("path = " + str(path))
    print("pathstring = " + str(pathstring))
    with open(str(pathstring), "r") as f:
        for i in range(3):
            line = f.readline()
        print("line = " + line)

    index = find_n(line, "n")
    print(index)
    s_pos = []
    count = 0

    for j in index:
        print("number = " + str(j))
        print("number -2 = " + str(j-2))
        s_pos.append(count)
        s_pos[count] = j - 2
        count = count+1
    print(index)
    print(s_pos)

    for k in s_pos:
        if line[k] == "s":
            print("CORRECT " + str(k))
            homogeneous = True
            continue

        else:
            print("NOPE " + str(k))
            homogeneous = False
            break

    pluscount = line.count("+")
    minuscount = line.count("-")
    print("pluscount = " + str(pluscount))
    print("minuscount = " + str(minuscount))
    plusend = line.split("+")[pluscount]
    minusend = line.split("-")[minuscount]

    print("minusend = " + minusend)
    print("plususend = " + plusend)

    if plusend.find("s(n") == -1 and minusend.find("s(n") == -1:
        homogeneous = False
    else:
        homogeneous = True

    return homogeneous

homogeneous = find_type(homogeneous=False, path=os.path.dirname(os.path.realpath(__file__)) + "/input_files/comass33.txt")
print(homogeneous)