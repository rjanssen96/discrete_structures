import os
import glob # Library for filename pattern-matching
import file_writer
import re
import time
from colorama import Fore as color
import re
from sympy.abc import a, n
from sympy.solvers import solve
from sympy import simplify
from sympy.parsing.sympy_parser import parse_expr
from pathlib import Path


import sympy
from sympy import Poly
import numpy
from sympy.abc import s, n


"""First checks if debug printing is allowed.
   Then checks the type of the input of the function.
   Then prints the input based on the type of input."""
# def debug_print(debug_information):
#     global print_debug_information
#     if print_debug_information:
#         if type(debug_information) == dict:
#             print_dict(debug_information)
#         elif type(debug_information) == list:
#             print_list(debug_information)
#         else:
#             print(str(debug_information))

"""Reads in all lines of the file except the first, second and last one.
    The lines are returned as list of strings."""
def read_file(filename):
    lines = []
    with open(filename, "r") as input_file:
        for index, line in enumerate(input_file):
            if not (index in [0, 1]) and line != "];\n": # Filter out first and second row and the last that contains "];\n"
                lines.append(line.strip()) # Append and remove leading and closing whitspaces
    return lines

"""Goes through all rows except the last and delete the "," at the end.
    The result is returned (again as list of strings)."""
def clear_commas(lines):
    for index, line in enumerate(lines):
        if index < len(lines) - 1: # This is not the last line
            comma_pos = len(line) - 1 # The last index position where the "," stands
            lines[index] = line[:comma_pos]
    return lines

"""Deletes all remaining whitespace and converts "^" to "**".
    The result is returned (again as list of strings)."""
def fix_syntax(lines):
    for index, line in enumerate(lines):
        line = str.replace(line, " ", "")
        line = str.replace(line, "^", "**")
        lines[index] = line
    return lines


"""Determines for each line in lines:
    The x-value of s(x) and the corresponding y-value of s(x)=y.
    This is returned as dictionary where x is the integer-key and y the string-value."""
def det_init_conditions(lines):
    conditions = {}
    for line in lines:
        pos_s_bracket = line.find("s(") # Position of "s("
        start_index_nr = pos_s_bracket + 2 # First index of x-value
        pos_bracket_equal = line.find(")=", pos_s_bracket) # Position of ")="
        start_index_y = pos_bracket_equal + 2 # First position after the "=" symbol
        x_value = int(line[start_index_nr:pos_bracket_equal])
        y_value = line[start_index_y:]
        conditions[x_value] = y_value

    # print("The conditions are: {}\n".format(conditions)) #This line can be removed.

    conditions_list = []
    for key in sorted(conditions.keys()): #Sort the initial terms in the dictionary
        init_value = str(conditions.get(key))  #Get the values of the inital terms
        conditions_list.append(init_value)  # Add the values of the initial terms to a list
    file_writer.write_init_terms(filename=filename, conditions=conditions_list)
    return conditions


"""Searches for the left begin of the term (beginning at start) and returns the first position belonging to the term, where the symbols are still
    counted as part of the term (may be handy for "+" and "-", but REMIND THIS if the symbols list also contains "*" and "/")..
    The begin of a new term is indicated with one of the symbols in the list "symbols", but only if there are no opened brackets at this position."""
def search_left_term_begin(equation, start, symbols):
    bracket_count = 0 # Indicating the number of opened bracket-scopes
    index = start
    while index >= 0:
        if equation[index] == ")":
            bracket_count += 1
        elif equation[index] == "(":
            bracket_count -= 1
        elif bracket_count == 0 and equation[index] in symbols:
            return index
        index -= 1
    return 0 # If we got until here the term starts at the begin of equation

"""Searches for the right end of the term (beginning at start) and returns the last position belonging to the term.
    The begin of a new term is indicated with one of the symbols in the list "symbols", but only if there are no opened brackets at this position."""
def search_right_term_end(equation, start, symbols):
    bracket_count = 0 # Indicating the number of opened bracket-scopes
    index = start
    while index < len(equation):
        if equation[index] == "(":
            bracket_count += 1
        elif equation[index] == ")":
            bracket_count -= 1
        elif bracket_count == 0 and equation[index] in symbols and index > 0:
            return index - 1
        index += 1
    return len(equation) - 1 # If we got until here the term ends at the end of equation

"""Determines and returns:
    1. The value of x in s(n-x) as integer, where pos_s should be the index of "s" in equation
    2. equation where "s(n-x)" is replaced by "1"."""
def recurrent_step_length(equation, pos_s):
    exclusive_end_pos = equation.find(")", pos_s)
    value = equation[pos_s + 4:exclusive_end_pos]
    equation = equation.replace("s(n-" + value + ")", "1") # Replace "s(n-x)" with "1"
    return int(value), equation


"""Determines and returns:
    1. A dictionary of the associated homogeneous recurrence relation in default form, where:
        -The integer-key is x of s(n-x) (thus without minus)
        -The string-value is y of y*s(n-x)
    2. A list of string-terms of F(n)."""
def analyze_recurrence_equation(equation):
    associated = {}
    f_n_list = []
    equation = equation[5:len(equation)] # Remove the "s(n)="-part
    pos_s = equation.find("s(n-") # First position of recurrent part
    while pos_s >= 0: # There is another recurrent s(n-x) part
        # debug_print(equation)
        step_length, equation = recurrent_step_length(equation, pos_s) # Determines step length and replaces recurrent part with a "1"
        # debug_print(step_length)
        left_pos = search_left_term_begin(equation, pos_s, ["+", "-"])
        right_pos = search_right_term_end(equation, pos_s, ["+", "-"])
        c_n = equation[left_pos:right_pos + 1] # Substring with both indexes inclusive
        # debug_print("c_n "+ c_n)
        equation = equation.replace(c_n, "", 1) # Remove the actual c_n from the equation (only once)
        associated[step_length] = c_n # Add the recursive step length and factor to the dictionary
        pos_s = equation.find("s(n-") # First position of recurrent part (because other "s(n-"-part is already removed)
    # Sorry, but you will have to implement the treatment of F(n) yourself!
    return associated, f_n_list


"""This functions checks what the coefficients are for each eaquation, this is only for homogeneous equations."""

def det_coefficients(equation):
    # print("We are going to find the coefficients for: {}".format(str(equation)))
    # print("We have te find coefficients in the following lines: {} \n".format(lines))
    expression = re.compile("((-?\(-?\d+/\d+\)|-?\d+|\d?-?\(-?\d+/\d+\)|-?\d+|\d?)\*?s(\(n-\d+\)))")
    results = expression.findall(str(equation))

    """Find all the "s(" combinations, put them in a list. Those who do not occur in the results, insert an 1"""

    if results == None:
        print(color.RED + "No coefficients found!\n", color.RESET)
        print(equation)
    else:
        # print("We found the following coefficients:\n")
        # print(results)
        coeff_dict = {}
        coeff_sorted_list = []
        polynomial_sorted_list = []
        for item in results:
            print(item)
            if item[1] == "":
                # print("coefficient: {} \t macht: {} \t position: {}\n".format(item[0], "1", item[2]))
                stripped_position = item[2].strip("(n").strip(")")
                # print("\n new: \ncoefficient: {} \t macht: {} \t position: {}\n".format(item[0], "1", stripped_position))
                coeff_dict[stripped_position] = item[0], "1"
            else:
                # print("coefficient: {} \t macht: {} \t position: {}\n".format(item[0], item[1], item[2]))
                stripped_position = item[2].strip("(n").strip(")")
                # print("\n new: \ncoefficient: {} \t macht: {} \t position: {}\n".format(item[0], item[1], stripped_position))
                coeff_dict[stripped_position] = item[0], item[1]

        # print(coeff_dict)

        for key in sorted(coeff_dict.keys()):
            # print(coeff_dict)
            # print(coeff_dict.get(key)[0])
            #
            # print("The key is: {}".format(key))
            # polynomial = str(coeff_dict.get(str(key))[0])  # *s(n-2) from the ordered dictionary.
            #
            # pos_s_bracket = polynomial.find("*s(")  # Position of "*s("
            # start_index_nr = pos_s_bracket + 0  # First index of x-value, when changing the 0 to 1. The * will be excluded!
            # pos_bracket_equal = polynomial.find(")", pos_s_bracket)  # Position of ")="
            # end_index_nr = pos_bracket_equal + 1  # includes the ) back in the polynomial
            # # x_value = str(polynomial[start_index_nr:pos_bracket_equal]) #Assign the characters between *s( and ) to the x_value variable
            # x_value = str(polynomial[start_index_nr:end_index_nr])  # Assign the characters between *s( and ) to the x_value variable
            #
            # # """Insert the 1 coefficients."""
            # # if str(coeff_dict.get(str(key))[1]) == "1": #If the coefficients from the polynomial = 1, then s(n-1) does not need to be formatted.
            # #     print("hello")
            # #     # coeff_unsorted_dict[key] = (x_value, (coeff_dict.get(str(key))[0]), "1") #ADD the degree (key) and (x_value(part), polynomial, coefficient) to a dict.
            # #     # x_value = str(coeff_dict.get(str(key))[0])

            """Insert the 0 coefficients."""
            #If the previous key is -1, then no action. Otherwise add 0
            degree_list = list(reversed(sorted(coeff_dict)))
            degree = int(degree_list[0])
            # print(color.BLUE + "The degree is: {}".format(degree), color.RESET)

            """Write the degree to a file."""
            file_writer.write_degree_to_file(filename=filename, degree=degree, homogeneous=True)

            # print("The range is: {}\n".format((range(degree, 0))))
            for number in range(degree, 0):
                # key = n # % 10
                # print("We will check: {}\n".format(number))
                if str(number) in coeff_dict:
                    pass
                    # print("Degree {} found in dict.\n".format(number))

                else:
                    # print("Degree {} not found in dict.\n".format(number))
                    zero_tuple = (("0*s(n-{})".format(abs(number)), "0"))
                    # print("tuple[0] {}, tuple[1]: {}\n".format(zero_tuple[0], zero_tuple[1]))
                    x_value = "(n-{})".format(abs(number))

                    # print("This is the data before adding \nNumber: {}, tuple: {}, coeff_dic:{}".format(number, zero_tuple, coeff_dict))
                    coeff_dict[str(number)] = zero_tuple[0], zero_tuple[1] #The key is the degree, ten the part and the 0 coefficients is added to the dictionary.
                    # print("This is the data after adding \nNumber: {}, tuple: {}, coeff_dic:{}".format(number, zero_tuple, coeff_dict))
                    # print(color.RED + "The keys are: {}\n".format(coeff_dict.keys()), color.RESET)
                    # print(color.RED + "The dictionary is: {}\n".format(coeff_dict), color.RESET)

        # print("\n\nEntering write fucniton\n\n")
        print(sorted(coeff_dict.values()))
        for all_keys in sorted(coeff_dict.keys()):
            coefficient = str(coeff_dict.get(str(all_keys))[1])
            """if a coefficient is 1, then there is no *s, so the find_parts function is not needed."""
            if coefficient == "1":
                polynomial = str(coeff_dict.get(str(all_keys))[0])
            else:
                polynomial = find_parts(polynomial=str(coeff_dict.get(str(all_keys))[0]))

            coeff_sorted_list.append(coefficient) #Add the coefficients in order to the list
            polynomial_sorted_list.append(polynomial)#Add *s(n-2) to a list in the sequence of the coefficients

        file_writer.write_coefficients_to_file(filename=filename, coefficients=coeff_sorted_list, polynomials=polynomial_sorted_list)
        print(coeff_sorted_list)

"""This function finds the parts from the polynomials, it removes the coefficients"""
def find_parts(polynomial):
    pos_s_bracket = polynomial.find("*s(")  # Position of "*s("
    start_index_nr = pos_s_bracket + 0  # First index of x-value, when changing the 0 to 1. The * will be excluded!
    pos_bracket_equal = polynomial.find(")", pos_s_bracket)  # Position of ")="
    end_index_nr = pos_bracket_equal + 1  # includes the ) back in the polynomial
    # x_value = str(polynomial[start_index_nr:pos_bracket_equal]) #Assign the characters between *s( and ) to the x_value variable
    return str(polynomial[start_index_nr:end_index_nr])  # Assign the characters between *s( and ) to the x_value variable


#These two function determ if the equation is homogeneous or not.
# Then moves the homogeneous equations to the homogeneous folder and the nonhomogeneous to the nonhomogeneous folder.

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
                print("maxpower = " + str(maxpower))
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
            """When the theorem cannot be used, the c^n = A * C^n principle is used."""
            if theorem_boolean == False:
                """This regular expression finds 43^(n-1), this is c^n"""
                regex_cn = re.compile("(\d*)\^(\([n]-\d*\))")
                input = nonhomogeneous_string
                find_cn = re.findall(regex_cn, input)
                match = re.search(regex_cn, input)
                print(match)
                print(find_cn)
                constant = find_cn[0][0]
                power = find_cn[0][1]

                old = "{}^{}".format(constant, power)
                a_formula = "a*{}**{}".format(constant, power)
                new_formula = (input.replace(old, a_formula)).replace("^", "**").replace(" ", "")
                print("The nonhomogeneous new formula is: {}\n".format(new_formula))
                print("The equation is: {}**{}".format(constant, power))

                new_fn_part = solve(new_formula, a)
                print("We found the F(n) solution: {}\n".format(new_fn_part))
                file_writer.write_fn_part_to_file(filename=pathstring, fn_parts=new_fn_part, fn_part_sn=fn_part_sn_string)
            else:
                file_writer.write_fn_part_to_file(filename=pathstring, fn_parts=fn_parts_dict, fn_part_sn=fn_part_sn_string)
            #print("nonhom = " + str(splitline))

    file_writer.move_files_based_on_type(filename=pathstring, homogeneous=homogeneous)

def read_lists_from_files(file_type, filename, homogeneous, automatic, step):
    """the folder will be the map where the files are located. If homogeneous is True and automatic is also true, the files will be
    in /output_files/homogeneous/automatic/"""
    if homogeneous == True and automatic == True:
        filename = str(filename).replace(str(Path("output_files/homogeneous/")), str(Path("/output_files/homogeneous/automatic/")))
    elif homogeneous == False and automatic == True:
        filename = str(filename).replace(str(Path("output_files/nonhomogeneous/")), str(Path("/output_files/nonhomogeneous/automatic/")))
    elif homogeneous == True and automatic == False:
        if step == None:
            print(color.RED + "Error: you must specify a step to read files manually!", color.RESET)
        else:
            filename = str(filename).replace(str(Path("output_files/homogeneous/")), str(Path("/output_files/homogeneous/{}/))".format(step))))
    elif homogeneous == False and automatic == False:
        if step == None:
            print(color.RED + "Error: you must specify a step to read files manually!", color.RESET)
        else:
            filename = str(filename).replace(str(Path("output_files/nonhomogeneous/")), str(Path("/output_files/nonhomogeneous/{}/".format(step))))

    # print(color.RED + "The requested folder is: {}\n".format(folder), color.RESET)

    error_banner = """File name is the name of the file,\n
    if file_type = comass, the comass[0-9][0-9].txt will be the file type.\n
    if file type = coefficients, the comass[0-9][0-9]_coefficients.txt will be the file type.\n
    if file type = degree, the comass[0-9][0-9]_degree.txt will be the file type.\n
    if file type = equation, the comass[0-9][0-9]_equation.txt will be the file type.\n
    if file type = init, the comass[0-9][0-9]_init.txt will be the file type.\n
    if file type = parts, the comass[0-9][0-9]_parts.txt will be the file type.\n
    if file type = fn_parts or fn_part_sn, the comass[0-9][0-9]_fn_parts.txt will be the file type.\n"""
    try:
        if file_type == "comass":
            filename = str(filename)
        elif file_type == "coefficients":
            filename = str(filename).replace(".txt", "_coefficients.txt")
        elif file_type == "degree":
            filename = str(filename).replace(".txt", "_degree.txt")
        elif file_type == "equation":
            filename = str(filename).replace(".txt", "_equation.txt")
        elif file_type == "init":
            filename = str(filename).replace(".txt", "_init.txt")
        elif file_type == "parts":
            filename = str(filename).replace(".txt", "_parts.txt")
        elif file_type == "fn_parts" or "fn_part_sn":
            filename = str(filename).replace(".txt", "_fn_parts.txt")
    except Exception:
        print(color.RED + "Wrong file_type specified!\n{}".format(error_banner), color.RESET)

    try:
        file = open(filename, 'r')
        readed_list = str(str(str(str(file.readline()).strip("[")).strip("]").strip("'")))
        readed_list = readed_list.strip("'")
        readed_list = readed_list.split("""', '""")
        # print(color.BLUE + "The line is: {}\nThe type is: {}\n".format(readed_list, type(readed_list)))
        file.close()
        """The coefficients, degree and init needs to be returned as integers, the parts as strings."""
        if file_type == "fn_parts":
            readed_list = str(readed_list).split(" | ")
            readed_list = str(str(readed_list[0]).strip("['")).strip("]")
        elif file_type == "fn_part_sn":
            readed_list = str(readed_list).split(" | ")
            readed_list = str(str(readed_list[1]).strip("']")).strip("[")
        return readed_list

    except Exception as error:
        print(color.RED + "Error during opening requested file!\nERROR: {}".format(error), color.RESET)

def read_files():
        # def write_coefficents_to_file(filename, coefficients):
    path = str(os.path.dirname(os.path.realpath(__file__)) + str(Path("/input_files/comass[0-9][0-9].txt")))
    global filename #The filename needs to be available in every function.
    for filename in glob.glob(path):
        # print("File: " + filename)
        # next_symbolic_var_index = 0  # Reset this index for every file
        # debug_print("Beginning for file \"{0}\"".format(filename))
        lines = read_file(filename)
        lines = clear_commas(lines)
        lines = fix_syntax(lines)
        # print("Len lines: " + str(len(lines)))
        # print(lines)
        """Write the equation to a file"""
        file_writer.write_equation(equation=lines[0], filename=filename)
        # debug_print(lines)
        # # The following quick fix was done because some input files had two newlines at their end and the list "lines" thus may contain one empty line "" at the end
        tmp = len(lines)
        if lines[len(lines) - 1] == "":
            tmp -= 1
        init_conditions = det_init_conditions(
            [lines[index] for index in range(1, tmp)])  # Determine initial conditions with all but the first line as input
        associated, f_n_list = analyze_recurrence_equation(lines[0])

        det_coefficients(equation=lines)

        # find_degree(filename=filename)
        try:
            find_type(path=filename, homogeneous=False)
        except Exception as error:
            """Replace the filename with the error name."""
            error_name = str(filename).replace("commass", "ERROR_commass")
            os.rename(filename, error_name)
            print(color.RED + "Cannot determine the equation type, ERROR: {}\nFile renamed to: {}\n".format(error, error_name), color.RESET)

        # # Print debugging information:
        # debug_print(filename)
        # debug_print("Initial conditions:")
        # debug_print(init_conditions)
        # debug_print("Associated homogeneous recurrence relation:")
        # debug_print(associated)
        # debug_print("F(n):")
        # debug_print(f_n_list)
        #
        # output_filename = filename.replace(".txt", "-dir.txt")
        # resulting_equ = ""
        # # Check if the equation is a homogeneous relation
        # if not f_n_list:  # The list is empty
        #     resulting_equ = solve_homogeneous_equation(init_conditions, associated)
        # else:
        #     resulting_equ = solve_nonhomogeneous_equation(init_conditions, associated, f_n_list)
        # resulting_equ = reformat_equation(resulting_equ)
        # write_output_to_file(output_filename, resulting_equ)
        #
        # debug_print("#################################\n")