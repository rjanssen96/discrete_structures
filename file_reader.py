import os
path = os.path.dirname(os.path.realpath(__file__))
for filename in (path + "\input_files\comass[0-9][0-9].txt"):
    print("File: " + filename)
    next_symbolic_var_index = 0  # Reset this index for every file
    debug_print("Beginning for file \"{0}\"".format(filename))
    lines = read_file(filename)
    lines = clear_commas(lines)
    lines = fix_syntax(lines)
    print("Len lines: " + str(len(lines)))
    debug_print(lines)
    # The following quick fix was done because some input files had two newlines at their end and the list "lines" thus may contain one empty line "" at the end
    tmp = len(lines)
    if lines[len(lines) - 1] == "":
        tmp -= 1
    init_conditions = det_init_conditions(
        [lines[index] for index in range(1, tmp)])  # Determine initial conditions with all but the first line as input
    associated, f_n_list = analyze_recurrence_equation(lines[0])

    # Print debugging information:
    debug_print(filename)
    debug_print("Initial conditions:")
    debug_print(init_conditions)
    debug_print("Associated homogeneous recurrence relation:")
    debug_print(associated)
    debug_print("F(n):")
    debug_print(f_n_list)

    output_filename = filename.replace(".txt", "-dir.txt")
    resulting_equ = ""
    # Check if the equation is a homogeneous relation
    if not f_n_list:  # The list is empty
        resulting_equ = solve_homogeneous_equation(init_conditions, associated)
    else:
        resulting_equ = solve_nonhomogeneous_equation(init_conditions, associated, f_n_list)
    resulting_equ = reformat_equation(resulting_equ)
    write_output_to_file(output_filename, resulting_equ)

    debug_print("#################################\n")