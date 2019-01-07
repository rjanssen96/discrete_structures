import os
import glob
import re
from sympy.parsing.sympy_parser import parse_expr
from sympy import simplify

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
    hom = re.compile("((?:-|\+|)(?:|\d|\d\d|\d\d\d).s\((?:n-|n--)(?:\d|\d\d)\)|\S\((?:\d|\d\d|\d\d\d).(?:\d|\d\d|\d\d\d)\).s\((?:n-|n--)(?:\d|\d\d)\))")

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

        #print("oldline = " + line)
        newline = newline.replace("s(n)" + str(num), "s(n)")
        #print("newline = " + newline)
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

    for strings in homogeneous:
        nonhomogeneous_string = nonhomogeneous_string.replace(str(strings),"").replace(',',"").replace("=","").strip()

    nonhomogeneous_string = str(simplify(nonhomogeneous_string))
    nonhomogeneous_string =  nonhomogeneous_string.replace("**", "^").replace(" ","")

    print("noonhom =" + nonhomogeneous_string)
    fn_parts_regex = re.compile("(?:(?:-|\+|(?:-|\+|)(?:\d\/|\d\d\/|\d\d\d\/))(?:\d|\d\d|\d\d\d|\d\d\d\d)\*n(?:\^|)(?:\d|\d\d|\d\d\d|\d\d\d\d)|(?:-|\+|(?:-|\+)(?:\d\/|\d\d\/|\d\d\d\/))(?:\d|\d\d|\d\d\d)\*n|(?:(?:-|\+)n\^(?:\d\d\d|\d\d|\d)))")
    all_fn_parts = re.findall(fn_parts_regex,nonhomogeneous_string)
    #print("all_fn_parts = " + str(all_fn_parts))

    fn_parts_dict = {}
    fn_parts_list = []
    fn_parts_list_coeffs = []
    fn_parts_list_powers = []

    #This for loop creates a dictionary of all the fn parts for nonhom_calling_test
    for parts in all_fn_parts:
        print(parts)
        coeff = parts.split('*')[0]
        if '-n' in coeff:
            coeff=-1
        elif 'n' in coeff:
            coeff=1
        else:
            coeff = parse_expr(str(coeff))

        fn_parts_list_coeffs.append(coeff)

        if "^" in parts:
            power = parts.split('^')[1]
            power = parse_expr(str(power))
            fn_parts_list_powers.append(power)
        else:
            fn_parts_list_powers.append(1)

    #print("fn_parts_list_powers = " + str(fn_parts_list_powers))
    #print("fn_parts_list_coeffs = " + str(fn_parts_list_coeffs))

    if not fn_parts_list_powers:
        maxpower = 0
    else:
        maxpower = max(fn_parts_list_powers) #Finds the highest power in the list of powers

    #print("maxpower = " + str(maxpower))

    #If fn_parts_list_powers = empty, this fails and it continues as normal
    try:
        #This loop fills the list with powers which are not there F.I if it is 3,5,6 it will append 1,2,4
        for c in range(maxpower):
            if maxpower in fn_parts_list_powers:
                maxpower = maxpower-1
            else:
                fn_parts_list_powers.append(maxpower)
                maxpower= maxpower-1

        if 0 not in fn_parts_list_powers:
            fn_parts_list_powers.append(0)

        #This is the difference between the amount of powers and coeffs in both lists after appending
        power_difference = len(fn_parts_list_powers)-len(fn_parts_list_coeffs)

        #This loop appends 1's for coeffs that are missing, making both power and coeffs lists equal in length/numbers
        for p in range(power_difference):
            fn_parts_list_coeffs.append(0)

        #Resetting the power count
        power_count = max(fn_parts_list_powers)+1
        counter = 0

        #The next three lines create a list and fills it with as many 1's as the powers length. These will be substituted later.
        ordered_coeff_list = []
        for l in range(power_count):
            ordered_coeff_list.append(1)

        ordered_power_list = fn_parts_list_powers
        print(ordered_power_list)

        #Finds the position/combinations of coeffs with the powers and sorts both so they still align, after the powers get sorted from 1-6.
        while counter < power_count:
            power_number = fn_parts_list_powers[counter]
            power_index = fn_parts_list_powers.index(power_number)
            ordered_coeff_list[power_number]=fn_parts_list_coeffs[power_index]
            counter = counter+1

        #print("powers = " + str(fn_parts_list_powers))
        #print("coeffs = " + str(fn_parts_list_coeffs))
        ordered_coeff_list = reversed(ordered_coeff_list)
        ordered_power_list.sort(reverse=True)
        #print("ordered powers = " + str(ordered_power_list))
        #print("ordered coeffs = " + str(ordered_coeff_list))

        #This is the dict that is needed for nonhom_calling_test.py
        fn_parts_dict = dict(zip(ordered_power_list, ordered_coeff_list))
        print(fn_parts_dict)
    except:
        pass

    print(fn_parts_dict)

    #print(fn_parts_dict)

    #If the nonhom string didnt have a part like this, it sets it to -1
    if not fn_part_sn_string:
        fn_part_sn_string = -1

    #print("fn_part_sn_string = " + str(fn_part_sn_string))

    theorem_boolean = True #The boolean which checks if theorem 6 is applicable

    print("nonhomogeneous string === " + nonhomogeneous_string)

    #This if statement checks if theorem 6 is applicable on the equation.
    if "^(n-" in nonhomogeneous_string or "^(n+" in nonhomogeneous_string:
        theorem_boolean = False
    #print(theorem_boolean)

    #This loop removes the nonhomogenous string from the whole equation, leaving just the homogeneous part
    #for strings in homogeneous:
    #    nonhomogeneous_string = nonhomogeneous_string.replace(str(strings),"").replace(',',"").replace("=","").strip()

    #This variable pastes the nonhom string after the hom string, correctly ordering the equation
    #print("newline = " + newline)

    print("non homogeneous = " + nonhomogeneous_string)
    #homogeneous_string = newline.replace(nonhomogeneous_string,"").replace(',',"").strip()
    homogeneous_string = "s(n)" + ''.join(homogeneous)
    print("homogeneous_string = " + homogeneous_string)

    ordered_relation = homogeneous_string + "+" + nonhomogeneous_string
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