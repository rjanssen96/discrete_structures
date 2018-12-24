from sympy import *

# from hom_step1 import *
from hom_step2 import *
from hom_step4 import *
from nonhom_step5 import *


def solve_nonhom_relations():
    # Step 1: rewrite the relation to its default form: a_n = homog + F(n)
    homogeneous_part = ""
    fn_part = ""

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
        new_findings = roots(characteristic_equation, r)  # returns root:multiplicity
        print("Step 3:  The roots of this equation are:")
        print(new_findings)  # root:multiplicity
        print()
    except:
        print("3 doesnt work, shocker dude")

    # Step 4: Obtain general solution of the associated homog part
    # if degree >= 1:  # multiplicity is important!!! Also build this to support more then 2 roots
    try:
        general_solution = find_general_solution_2(new_findings)
        # general_solution = "Sup Nerd!"
        print("Step 4:  The general solution of this equation is: \n" + str(general_solution) + "\n")
    except:
        print("4 doesnt work, shocker dude")

    # Step 5: Obtain the particular solution of the non-homog part
    try:
        # smth smth big spin
        particular_solution = find_part_sol_non_homog()
        print("Step 5:  The particular solution of the non-homog part is: \n" + str(particular_solution) + "\n")
    except:
        print("5 doesnt work, shocker dude")

    # Step 6: Obtain the solution a_n = a_n(p) + a_n(h)

    # Step 7: Obtain the alpha values and the particular solution


solve_nonhom_relations()
