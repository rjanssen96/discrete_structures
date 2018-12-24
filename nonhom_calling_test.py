from sympy import *

# from hom_step1 import *
from hom_step2 import *
from hom_step4 import *
from nonhom_step5 import *


def solve_nonhom_relations():
    # Step 1: rewrite the relation to its default form: a_n = homog + F(n)
    homogeneous_part = ""
    # fn_part = "3**2"  # Needs to be in the right order, so biggest power to lowest power
    # fn_parts = [0, 3]  # every elemts in this list is the next b in fn, so bn**0, bn**1, bn**2
    # all powers from max up to and including 0
    fn_parts = {3:1, 2:0, 1:0, 0:0}  # power:coeff, so n^2 = 2:1, cuz power=2 ^ coeff=1. SORTED FROM HIGH TO LOW
    fn_part_sn = 2  # the s in s**n, if no s**n part in fn, then put 1 here
    highest_power_fn_part = next(iter(fn_parts))  # represents the "t" in the particular solution of non-hom part (step 5)

    degree = 2
    initial_terms = [4, 5]
    homogeneous_coeffs = [2, 3]

    # Step 2: Obtaining the characteristic equation  of the associated homog part
    try:
        characteristic_equation = char_equation_2(homogeneous_coeffs)
        print("Step 2: The characteristic equation is: \n" + str(characteristic_equation) + "=0" + "\n")
    except:
        print("2 doesnt work, shocker dude")

    # Step 3: Obtain the roots  of the associated homog part
    # if degree >= 1:  # find out how to obtain the multiplicity, find root() or search in list for doubles an m=2 for every
    try:
        r = symbols('r')
        r_and_m_found = roots(characteristic_equation, r)  # returns root:multiplicity
        print("Step 3: The roots of this equation are:")
        print(r_and_m_found)  # root:multiplicity
        print()
    except:
        print("3 doesnt work, shocker dude")

    # Step 4: Obtain general solution of the associated homog part
    # if degree >= 1:  # multiplicity is important!!! Also build this to support more then 2 roots
    try:
        general_solution = find_general_solution_2(r_and_m_found)
        general_solution = general_solution.replace("s(n)=+", "s(n)=")
        # general_solution = "Sup Nerd!"
        print("Step 4: The general solution of this equation is: \n" + str(general_solution) + "\n")
    except:
        print("4 doesnt work, shocker dude")

    # Step 5: Obtain the particular solution of the non-homog part
    # try:
    #     # smth smth big spin
    #     particular_solution = find_part_sol_non_homog(fn_parts, fn_part_sn, highest_power_fn_part, r_and_m_found)
    #     print("Step 5: The particular solution of the non-homog part is: \n" + str(particular_solution) + "\n")
    # except:
    #     print("5 doesnt work, shocker dude")
    particular_solution = find_part_sol_non_homog(fn_parts, fn_part_sn, highest_power_fn_part, r_and_m_found)
    print("Step 5: The particular solution of the non-homog part is: \n" + str(particular_solution) + "\n")

    # Step 6: Obtain the solution a_n = a_n(p) + a_n(h)
    general_solution = general_solution.replace("s(n)=", "")
    print("Step 6: a_n = a_n(p) + a_n(h):\n" + "s(n):=" + particular_solution + "+" + general_solution + "\n")

    # Step 7: Obtain the alpha values and the particular solution


solve_nonhom_relations()
