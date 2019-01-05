import os
import glob
import re

global homogeneous
global path

#pathstring = str(os.path.dirname(os.path.realpath(__file__)) + "/input_files/comass[0-9][0-9].txt")
#pathstring = str(os.path.dirname(os.path.realpath(__file__)) + "/input_files/comass33.txt")
#path = glob.glob(pathstring)

def find_n(s,ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def find_type(homogeneous, path):
    pathstring = str(path) #path to the equation
    newline = ""

    #The RegEx to find all homogeneous parts of the equation.
    hom = re.compile("((?:-|\+|)(?:|\d|\d\d|\d\d\d).s\(n-(?:\d|\d\d)\)|\S\((?:\d|\d\d|\d\d\d).(?:\d|\d\d|\d\d\d)\).s\(n-(?:\d|\d\d)\))")

    print("path = " + str(path))
    print("pathstring = " + str(pathstring))

    #Reads the whole file and sets line 3 (the equation) as variable "line"
    with open(str(pathstring), "r") as f:
        for i in range(3):
            line = f.readline()
        print("line = " + line)

    #Splits the first string on the = symbol, only the s(n)..= part remains
    eq = line.split("=", 1)[0]
    num = eq.split(")",1)[1]

    #This if checks if there is a number in front of the = symbol. If so it highers/lowers all n-x parts with that amount
    if num != " ":
        newline = line
        num = int(num)
        totalcount = line.count("(n-")
        #If it is a negative number, it starts in the back of the string with highering the numbers
        if num < 0:
            loopcount = 1
            while loopcount < totalcount:
                split = line.split("(n-")[loopcount].split(")")[0]
                newnum = int(split) + num
                #print("newnum = " + str(newnum))
                oldstring = ("(n-"+split+")")
                newstring = ("(n-"+str(newnum)+")")
                #print((oldstring))
                #print(newstring)
                newline = newline.replace(oldstring, newstring)
                loopcount = loopcount+1
        #Else if it is a positive number it starts lowering all n-x's starting in the front
        else:
            loopcount = 1
            while loopcount < totalcount:
                split = line.split("(n-")[totalcount].split(")")[0]
                newnum = int(split) + num
                #print("newnum = " + str(newnum))
                oldstring = ("(n-"+split+")")
                newstring = ("(n-"+str(newnum)+")")
                #print((oldstring))
                #print(newstring)
                newline = newline.replace(oldstring, newstring)
                totalcount = totalcount-1

        print("oldline = " + line)
        newline = newline.replace("s(n)" + str(num), "s(n)")
        print("newline = " + newline)
    else:
        print("Not needed to higher/lower the n- values")

    #If the values didnt need highering/lowering it sets newline to just line
    if newline == "":
        newline = line

    newline = newline.replace(" ", "") #Remove spaces in new line
    homogeneous = re.findall(hom, newline.strip())#Finds all the homogeneous parts using the RegEx at the top of the function
    print("homogeneous parts are : " + str(homogeneous))

    nonhomogeneous_string = newline.replace("s(n)","") #Created the nonhomstring variable with s(n) removed from the string newline
    fn_part_sn_string = re.findall(("\d\^n|\d\d\^n|\d\d\d\^n"),nonhomogeneous_string) #Finds the sn part in the nonhom string
    fn_part_sn_string = ''.join(fn_part_sn_string).replace('^n','') #changes the variable to a string instead of a list

    #If the nonhom string didnt have a part like this, it sets it to -1
    if not fn_part_sn_string:
        fn_part_sn_string = -1
    print("fn_part_sn_string = " + str(fn_part_sn_string))

    theorem_boolean = True #The boolean which checks if theorem 6 is applicable

    #This if statement checks if theorem 6 is applicable on the equation.
    if "^(n-" in nonhomogeneous_string:
        theorem_boolean = False
    print(theorem_boolean)

    #This loop removes the nonhomogenous string from the whole equation, leaving just the homogeneous part
    for strings in homogeneous:
        nonhomogeneous_string = nonhomogeneous_string.replace(strings,"").replace(',',"").replace("=","").strip()

    print("nonhomogeneous_string = " + nonhomogeneous_string)
    #This variable pastes the nonhom string after the hom string, correctly ordering the equation
    homogeneous_string = newline.replace(nonhomogeneous_string,"").replace(',',"").strip()
    print("homogeneous_string = " + homogeneous_string)

    ordered_relation = homogeneous_string + nonhomogeneous_string
    print("ordered relation = " + ordered_relation)

    index = find_n(newline, "n")

    s_pos = []
    count = 0

    #Finds all positions of the "n" characters, subtracts 2 from that position to find al "s" positions
    for j in index:
        s_pos.append(count)
        s_pos[count] = j - 2
        count = count+1

    #This loops checks every second postition before every "n" character
    for k in s_pos:
        if newline[k] == "s" and homogeneous is not False:
            homogeneous = True
            continue
        if newline[k] == "s":
            continue
        else:
            homogeneous = False
            #print("nonhom = " + str(splitline))
    return homogeneous

homogeneous = find_type(homogeneous=True, path=os.path.dirname(os.path.realpath(__file__)) + "/input_files/nonhomtest")
print("homogeneous = " + str(homogeneous))