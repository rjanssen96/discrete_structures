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
    print("path = " + str(path))
    print("pathstring = " + str(pathstring))
    with open(str(pathstring), "r") as f:
        for i in range(3):
            line = f.readline()
        print("line = " + line)

    index = find_n(line, "n")

    eq = line.split("=", 1)[0]
    num = eq.split(")",1)[1]

    if num != " ":
        newline = line
        num = int(num)
        totalcount = line.count("(n-")
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
        print("oldline = " + line)
        newline = newline.replace("s(n)" + str(num), "s(n)")
        print("newline = " + newline)
    else:
        print("AWH")
    print(eq)
    print("num = " + str(num))

    print(index)
    bracket_pos = []
    minus_pos = []
    count = 0

    for j in index:
        #print("number = " + str(j))
        #print("number -1 = " + str(j-1))
        #print("number +1 = " + str(j+1))
        bracket_pos.append(count)
        bracket_pos[count] = j - 1
        minus_pos.append(count)
        minus_pos[count] = j + 1
        count = count+1
    print(index)
    print(bracket_pos)

    for k in bracket_pos:
        if line[k] == "(":
            print(color.MAGENTA + "CORRECT " + str(k))
            homogeneous = True
            continue

        else:
            print("NOPE " + str(k))
            homogeneous = False
            break
    file_writer.move_files_based_on_type(filename=pathstring, homogeneous=homogeneous)

def read_lists_from_files(file_type, filename, homogeneous, automatic, step):
    """the folder will be the map where the files are located. If homogeneous is True and automatic is also true, the files will be
    in /output_files/homogeneous/automatic/"""
    if homogeneous == True and automatic == True:
        filename = str(filename).replace("output_files/homogeneous/", "/output_files/homogeneous/automatic/")
    elif homogeneous == False and automatic == True:
        filename = str(filename).replace("output_files/nonhomogeneous/", "/output_files/nonhomogeneous/automatic/")
    elif homogeneous == True and automatic == False:
        if step == None:
            print(color.RED + "Error: you must specify a step to read files manually!", color.RESET)
        else:
            filename = str(filename).replace("output_files/homogeneous/", "/output_files/homogeneous/{}/".format(step))
    elif homogeneous == False and automatic == False:
        if step == None:
            print(color.RED + "Error: you must specify a step to read files manually!", color.RESET)
        else:
            filename = str(filename).replace("output_files/nonhomogeneous/", "/output_files/nonhomogeneous/{}/".format(step))

    # print(color.RED + "The requested folder is: {}\n".format(folder), color.RESET)

    error_banner = """File name is the name of the file,\n
    if file_type = comass, the comass[0-9][0-9].txt will be the file type.\n
    if file type = coefficients, the comass[0-9][0-9]_coefficients.txt will be the file type.\n
    if file type = degree, the comass[0-9][0-9]_degree.txt will be the file type.\n
    if file type = equation, the comass[0-9][0-9]_equation.txt will be the file type.\n
    if file type = init, the comass[0-9][0-9]_init.txt will be the file type.\n
    if file type = parts, the comass[0-9][0-9]_parts.txt will be the file type.\n"""
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
    except Exception:
        print(color.RED + "Wrong file_type specified!\n{}".format(error_banner))

    try:
        file = open(filename, 'r')
        readed_list = str(str(str(str(file.readline()).strip("[")).strip("]").strip("'")))
        readed_list = readed_list.strip("'")
        readed_list = readed_list.split("""', '""")
        print(color.BLUE + "The line is: {}\nThe type is: {}\n".format(readed_list, type(readed_list)))
        file.close()
    except Exception as error:
        print(color.RED +"Error during opening requested file!\nERROR: {}".format(error), color.RESET)


    """Convert degree, coefficients and initial terms from strings to integers"""
    try:
        if file_type == ("coefficients" or "degree" or "init"):
            integer_list = []
            for string in readed_list:
                try:
                    integer_list = integer_list.append(int(string))
                except Exception:
                    """This exepction catches NoneType errors"""
                    continue
            readed_list = integer_list
            print("The new readed list is: {}".format(readed_list))
    except Exception as error:
        print(color.RED + "Error during converting strings in {} list to integers.\nERROR: {}".format(file_type, error))


    return readed_list

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