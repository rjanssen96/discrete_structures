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
    newline = ""
    print("path = " + str(path))
    print("pathstring = " + str(pathstring))
    with open(str(pathstring), "r") as f:
        for i in range(3):
            line = f.readline()
        print("line = " + line)

    eq = line.split("=", 1)[0]
    num = eq.split(")",1)[1]

    if num != " ":
        newline = line
        num = int(num)
        totalcount = line.count("(n-")
        if num < 0:
            loopcount = 1
            while loopcount < totalcount:
                split = line.split("(n-")[loopcount].split(")")[0]
                newnum = int(split) + num
                print("newnum = " + str(newnum))
                oldstring = ("(n-"+split+")")
                newstring = ("(n-"+str(newnum)+")")
                print((oldstring))
                print(newstring)
                newline = newline.replace(oldstring, newstring)
                loopcount = loopcount+1
        else:
            loopcount = 1
            while loopcount < totalcount:
                split = line.split("(n-")[totalcount].split(")")[0]
                newnum = int(split) + num
                print("newnum = " + str(newnum))
                oldstring = ("(n-"+split+")")
                newstring = ("(n-"+str(newnum)+")")
                print((oldstring))
                print(newstring)
                newline = newline.replace(oldstring, newstring)
                totalcount = totalcount-1

        print("oldline = " + line)
        newline = newline.replace("s(n)" + str(num), "s(n)")
        print("newline = " + newline)
    else:
        print("Not needed to higher/lower the n- values")
    print(eq)
    print("num = " + str(num))

    if newline == "":
        newline = line

    index = find_n(newline, "n")

    s_pos = []
    count = 0

    for j in index:
        s_pos.append(count)
        s_pos[count] = j - 2
        count = count+1
    print(index)
    print(s_pos)

    for k in s_pos:
        if newline[k] == "s":
            print("CORRECT " + str(k))
            homogeneous = True
            continue

        else:
            print("NOPE " + str(k))
            homogeneous = False
            break

    return homogeneous

homogeneous = find_type(homogeneous=False, path=os.path.dirname(os.path.realpath(__file__)) + "/input_files/comass16.txt")
print(homogeneous)