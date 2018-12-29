from sympy import *
from sympy.parsing.sympy_parser import parse_expr

"""
smth is from with finding the particular solution
how can we implement it so that 10^(n-1) etc will be used correctly as well?

part sol depends on the form?
Sometimes theorem can be used, but not always!!

The current code below always uses the theorem
"""

# from hom_step1 import *
from hom_step2 import *
from hom_step4 import *
from nonhom_step5 import *
from nonhom_step7 import *


def solve_nonhom_relations():
    # Step 1: rewrite the relation to its default form: a_n = homog + F(n)
    homogeneous_part = ""
    # fn_part = "3**2"  # Needs to be in the right order, so biggest power to lowest power
    # fn_parts = [0, 3]  # every elemts in this list is the next b in fn, so bn**0, bn**1, bn**2

    # all powers from max up to and including 0
    fn_parts = {1:1, 0:0}  # power:coeff, so n^2 = 2:1, cuz power=2 ^ coeff=1. SORTED FROM HIGH TO LOW 2:1, 1:3, 0:2
    fn_part_sn = 3  # the s in s**n, if no s**n part in fn, then put 1 here
    highest_power_fn_part = next(iter(fn_parts))  # represents the "t" in the particular solution of non-hom part (step 5)

    degree = 2
    initial_terms = [1, 4]
    homogeneous_coeffs = [8, 2]  # coeffs of the associated homogeneous relation

    # Step 2: Obtaining the characteristic equation  of the associated homog part
    try:
        characteristic_equation = char_equation_2(homogeneous_coeffs)
        print("Step 2: The characteristic equation is: \n" + str(characteristic_equation) + "=0" + "\n")
    except Exception as error:
        print("2 doesnt work, shocker dude: ERROR: {}".format(error))

    # Step 3: Obtain the roots  of the associated homog part
    try:
        r = symbols('r')
        r_and_m_found = roots(characteristic_equation, r)  # returns root:multiplicity
        print("Step 3: The roots of this equation are:")
        print(r_and_m_found)  # root:multiplicity
        print()
    except Exception as error:
        print("3 doesnt work, shocker dude: ERROR: {}".format(error))

    # Step 4: Obtain general solution of the associated homog part
    try:
        general_solution = find_general_solution_2(r_and_m_found)
        general_solution = general_solution.replace("s(n)=+", "s(n)=")
        # general_solution = "Sup Nerd!"
        print("Step 4: The general solution of this equation is: \n" + str(general_solution) + "\n")
    except Exception as error:
        print("4 doesnt work, shocker dude: ERROR: {}".format(error))

    # Step 5: Obtain the particular solution of the non-homog part
    try:
        particular_solution = find_part_sol_non_homog(fn_parts, fn_part_sn, highest_power_fn_part, r_and_m_found)
        print("Step 5: The particular solution of the non-homog part is: \n" + "s(n)=" + str(particular_solution) + "\n")
    except Exception as error:
        print("5 doesnt work, shocker dude: ERROR: {}".format(error))

    # Step 6: Obtain the solution a_n = a_n(p) + a_n(h)
    try:
        general_solution = general_solution.replace("s(n)=", "")
        setup_spec_sol = "s(n)=" + particular_solution + "+" + general_solution  # for step 7.2
        print("Step 6: a_n = a_n(p) + a_n(h):\n" + "s(n)=" + particular_solution + "+" + general_solution + "\n")
    except Exception as error:
        print("6 doesnt work, shocker dude: ERROR: {}".format(error))

    # Step 7.1: Obtain the alpha values with a_n(p) + a_n(h)
    try:
        outcome = find_alpha_values(initial_terms, r_and_m_found, particular_solution)
        print("Step 7.1: The value of the Alphas:")
        print(outcome)
    except Exception as error:
        print("7.1 doesnt work, shocker dude: ERROR: {}".format(error))

    # Step 7.2: Obtain specific solution
    try:
        # specific_solution = setup_spec_sol
        specific_solution = get_specific_solution(setup_spec_sol, outcome)
        print("\nStep 7.2: The specific solution for this equation is: \n" + str(specific_solution) + "\n")
    except Exception as error:
        print("7.2 doesnt work, shocker dude: ERROR: {}".format(error))


solve_nonhom_relations()


# Testing specific solutions:
my_spec_sol = "((1)*(n)^(3)+(0)*(n)^(2)+(0)*(n)^(1)+(0)*(n)^(0))*(1)^(n)+(+(3/4)+(-9/8)*n)*(2)^n+(+(-3/4)+(3/8)*n)*(-2)^n"
my_spec_sol = my_spec_sol.replace("^", "**")
my_answer_list = []

for x in range(0, 20):
    my_new_spec_sol = my_spec_sol.replace("n", str(x))
    my_new_spec_sol = parse_expr(my_new_spec_sol)
    my_answer_list.append(my_new_spec_sol)

print(my_answer_list)

comma_spec_sol = "161/162*(-1)^(n+1)*2^n-47*2^(n-1)+1/648*(417*(-1)^n*n+3321*n)*2^n+1/9*n^3+16/9*n^2+32/3*n+1984/81"
comma_spec_sol = comma_spec_sol.replace("^", "**")
comma_answer_list = []

for x in range(0, 20):
    comma_new_spec_sol = comma_spec_sol.replace("n", str(x))
    comma_new_spec_sol = parse_expr(comma_new_spec_sol)
    comma_answer_list.append(comma_new_spec_sol)

print(comma_answer_list)

# tested with:
# assignment 3, (correct)
# commas16, (first 4 terms are correct, then its different... first 4 are initial terms)
# commas33 (watch out for this one, put n-5 as a string in the coeff list),
# commas36 doesnt work cuz key of dict will be str(n-4) :-/

