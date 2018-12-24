from sympy import *
from sympy.parsing.sympy_parser import parse_expr


# (Step 5.1) solving every systems with no matter the used theorem (cuz theorem 4 also contains theorem 3)
def find_alpha_values(my_initial_terms, all_r_and_m, parti_sol_in):
    """
    SECTION 0: NEEDED INFORMATION
    """
    nr_of_initial_terms = len(my_initial_terms)
    alpha_coeffs = {}
    matrix_input = ()
    solve_variable = ()

    """
    SECTION 1: GATHERING ALPHA COEFFS + INITIAL TERM VALUE ROWS 
    """
    for n in range(0, nr_of_initial_terms):  # a_0, a_1, ..., a_n
        row_of_coeffs = ()  # resets the tuples with the previous alphas coeff values
        parti_sol = parti_sol_in  # resets parti sol to what it was input as, to determine new answ for matrix row
        parti_sol = parti_sol.replace("n", str(n))  # replaces the string n with an actual value n
        answ_parti_sol = parse_expr(parti_sol)  # gives an answer for parti sol with n replaced to value n
        new_init_term = my_initial_terms[n] - answ_parti_sol  # calculates answer for matrix row

        for r in all_r_and_m:  # r holds the value of each root one by one for all initial terms
            m = all_r_and_m[r]  # m is the value of the multiplicty of the current root

            for p in range(0, m):  # p is the power to raise n to. For every root from 0 to m-1
                next_coeff = (n ** p) * (r ** n)
                row_of_coeffs = row_of_coeffs + (next_coeff,)

        matrix_row = row_of_coeffs + (new_init_term,)  # adds the answer of the initial term to the row
        alpha_coeffs[
            "row_{0}".format(n)] = matrix_row  # adds all the coeffs+answers of each initial term to a dictionary

    """
    SECTION 2: CREATE ALL NEEDED MATRIX SOLVE INPUT
    """
    amount_of_rows = len(alpha_coeffs)
    for x in range(0, amount_of_rows):  # makes a list with lists in it for every row of the matrix
        matrix_input = matrix_input + ((alpha_coeffs["row_" + str(x)]),)

    system = Matrix(matrix_input)  # creates correct syntax

    for x in range(0,
                   len(alpha_coeffs["row_0"]) - 1):  # Calculates how many different alpha coeffs need to be solved for
        solve_variable = solve_variable + (x,)

    """
    SECTION 3: SOLVE THE SYSTEM
    """
    matrix_result = solve_linear_system(system, *solve_variable)

    return matrix_result
