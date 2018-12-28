import os
import glob # Library for filename pattern-matching
import file_writer
import re
from colorama import Fore as color
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

    print("The conditions are: {}\n".format(conditions)) #This line can be removed.

    conditions_list = []
    for key in sorted(conditions.keys()): #Sort the initial terms in the dictionary
        init_value = str(conditions.get(key)[0])  #Get the values of the inital terms
        print("Added:\tInitial term number: {}\t value: {} to list.".format(key, init_value))
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
    print("We are going to find the coefficients for: {}".format(str(equation)))
    # print("We have te find coefficients in the following lines: {} \n".format(lines))
    expression = re.compile("((-?\(-?\d+/\d+\)|-?\d+|\d?-?\(-?\d+/\d+\)|-?\d+|\d?)\*s(\(n-\d+\)))")
    results = expression.findall(str(equation))
    if results == None:
        print(color.RED + "No coefficients found!\n", color.RESET)
        print(equation)
    else:
        print("We found the following coefficients:\n")
        print(results)
        coeff_dict = {}
        coeff_sorted_list = []
        polynomial_sorted_list = []
        for item in results:
            # print(item)
            print("coefficient: {} \t macht: {} \t position: {}\n".format(item[0], item[1], item[2]))
            stripped_position = item[2].strip("(n").strip(")")
            print("\n new: \ncoefficient: {} \t macht: {} \t position: {}\n".format(item[0], item[1], stripped_position))
            coeff_dict[stripped_position] = item[0],item[1]

        for key in sorted(coeff_dict.keys()):
            print(coeff_dict)
            print(coeff_dict.get(key)[0])
            polynomial = str(coeff_dict.get(key)[0]) #*s(n-2) from the ordered dictionary.

            pos_s_bracket = polynomial.find("*s(")  # Position of "*s("
            start_index_nr = pos_s_bracket + 0  # First index of x-value, when changing the 0 to 1. The * will be excluded!
            pos_bracket_equal = polynomial.find(")", pos_s_bracket)  # Position of ")="
            end_index_nr = pos_bracket_equal + 1 #includes the ) back in the polynomial
            # x_value = str(polynomial[start_index_nr:pos_bracket_equal]) #Assign the characters between *s( and ) to the x_value variable
            x_value = str(polynomial[start_index_nr:end_index_nr]) #Assign the characters between *s( and ) to the x_value variable

            print("The polynomial is: {}\n".format(x_value))
            coeff_sorted_list.append(key) #Add the coefficients in order to the list
            polynomial_sorted_list.append(x_value)#Add *s(n-2) to a list in the sequence of the coefficients
            # print(coeff_sorted_dict)
            print(key)

        file_writer.write_coefficients_to_file(filename=filename, coefficients=coeff_sorted_list, polynomials=polynomial_sorted_list)
        print(coeff_sorted_list)



#These two function determ if the equation is homogeneous or not.
# Then moves the homogeneous equations to the homogeneous folder and the nonhomogeneous to the nonhomogeneous folder.

def find_n(s,ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def find_type(homogeneous, path):
    pathstring = str(path)
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
        file_writer.move_homogeneous_files(filename=pathstring)
        homogeneous = False
    else:
        file_writer.move_nonhomogeneous_files(filename=pathstring)
        homogeneous = True

    return homogeneous

def read_files():
        # def write_coefficents_to_file(filename, coefficients):
    path = str(os.path.dirname(os.path.realpath(__file__)) + "/input_files/comass[0-9][0-9].txt")
    global filename #The filename needs to be available in every function.
    for filename in glob.glob(path):
        print("File: " + filename)
        # next_symbolic_var_index = 0  # Reset this index for every file
        # debug_print("Beginning for file \"{0}\"".format(filename))
        lines = read_file(filename)
        lines = clear_commas(lines)
        lines = fix_syntax(lines)
        print("Len lines: " + str(len(lines)))
        print(lines)
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