# Find the particular solution of a non-homogeneous part
from sympy import *
from sympy.parsing.sympy_parser import parse_expr

def find_part_sol_non_homog(fn_parts, s, highest_power, roots_multiples, degree, ordered_relation):
    # print("Have a nice day!!!")
    # smile = fn_parts
    s_root_check = False
    particular_sol = "("
    highest_power = int(highest_power)

    # # puts the non_homog part into b_t*n^t form
    # next_power = highest_power
    # for t in range(0, highest_power+1):  # +1 because not including the boundaries
    #     if t != highest_power:
    #         particular_sol = particular_sol + "(" + str(fn_parts[next_power]) + ")*(n)**(" + str(next_power) + ")+"
    #     elif t == highest_power:
    #         particular_sol = particular_sol + "(" + str(fn_parts[next_power]) + ")*(n)**(" + str(next_power) + ")"
    #     next_power = next_power - 1
    #
    # particular_sol = particular_sol + ")*(" + str(s) + ")**(n)"  # () to prevent wrong order of operations with weird n

    # puts the non_homog part into b_t*n^t form
    next_power = highest_power
    for t in range(0, highest_power+1):  # +1 because not including the boundaries
        if t != highest_power:
            particular_sol = particular_sol + "(p" + str(next_power) + ")*(n)**(" + str(next_power) + ")+"
        elif t == highest_power:
            particular_sol = particular_sol + "(p" + str(next_power) + ")*(n)**(" + str(next_power) + ")"
        next_power = next_power - 1

    particular_sol = particular_sol + ")*(" + str(s) + ")**(n)"  # () to prevent wrong order of operations with weird n

    # checks if s is a root or not
    for x in roots_multiples:
        if s == x:
            s_root_check = True

    # decides if n**m needs to be added infront or not
    if s_root_check == True:
        particular_sol = "(n)**(" + str(roots_multiples[s]) + ")*" + particular_sol  # n^m infront if s=root
        # print(fn_parts[s])
        # print(roots_multiples[s])
    elif s_root_check == False:
        a = "Sad boy"  # no need to do anything here, have a nice day :-)

    # smile = ":-)"
    # See theorem 6 of the book


    """
    RIK BEGIN HIER:
     """
    # #ordered_relation = "s(n-3) = s(n-4) + 3*s(n-5)"
    # an_replace = "s(n) = " + str(particular_sol)
    # an_symbols = ()
    #
    # degree = 6
    # for d in range(degree):
    #     an_symbols = an_symbols+("p"+str(d),)
    #     if d == 1:
    #         an_replace = an_replace.replace("n", "n-" + str(d))
    #         an_equation = an_replace.split("=",1)
    #         if "s(n-"+str(d) in ordered_relation:
    #             ordered_relation.replace("s(n-"+str(d)+")","("+an_equation+")").replace(" ","")
    #     else:
    #         an_replace = an_replace.replace("n-" + (str(d - 1)), "n-" + str(d))
    #         an_equation = an_replace.split("=")[1]
    #         if "s(n-"+str(d) in ordered_relation:
    #             ordered_relation = ordered_relation.replace("s(n-"+str(d)+")","("+an_equation+")").replace(" ","")
    #             print("s(n-"+str(d)+")")
    #
    #     print(an_replace)
    #     print("oredered = " + ordered_relation)
    #     print(an_symbols)



    """
    RICO BEGIN HIER:
    """
    ordered_relation = ordered_relation.replace("s(n)", "s(n)=")

    print("Before ordered relation adjusted")
    print(ordered_relation)

    print("Particular solution after mine, before R&R")
    print(particular_sol)

    ordered_relation = str(ordered_relation.replace("^", "**"))
    # ordered_relation = "s(n-3) = s(n-4) + 3*s(n-5)"
    # an_replace = "s(n) = " + str(particular_sol)
    an_replace = str(particular_sol)
    # an_replace = "p0+p1*n"
    an_symbols = ()

    # takes the absolute value of the degree
    degree = abs(degree)

    # print("Value of degree before loop")
    # print(degree)

    # degree = 6
    for d in range(0, degree+1):
        # print("Reached 1")
        # print(" Value of d = " + str(d))
        an_symbols = an_symbols + ("p" + str(d),)
        if d != 0:
            # print("Reached 2")
            an_replace = an_replace.replace("n", "n-" + str(d))
            an_equation = an_replace
            if "s(n-" + str(d) in ordered_relation:
                ordered_relation = ordered_relation.replace("s(n-" + str(d) + ")", "(" + an_equation + ")").replace(" ", "")
                # print("Reached 3")
                # print(ordered_relation)
                # print("s(n-" + str(d) + ")")
        elif d == 0:
            # print("Reached 4")
            an_replace = an_replace.replace("n-" + (str(d - 1)), "n-" + str(d))
            an_equation = an_replace
            if "s(n)" in ordered_relation:
            # if "s(n-" + str(d) in ordered_relation:
            #     print("Reached`44")
                # ordered_relation = ordered_relation.replace("s(n-" + str(d) + ")", "(" + an_equation + ")").replace(" ",
                ordered_relation = ordered_relation.replace("s(n)", "(" + an_equation + ")").replace(" ",
                                                                                                                    "")
                # print(ordered_relation)
                #print("s(n-" + str(d) + ")")
        else:
            print("Reached line 127 in step 4 non_homog, it should never get here!")

        #print(an_replace)
        #print("ordered = " + ordered_relation)
        #print(an_symbols)

    # print("Reached 5")
    print("After ordered relation adjusted 1")
    print(ordered_relation)

    # p0, p1, p2, p3, p4 = symbols('p0 p1 p2 p3 p4')
    x, y, n = symbols('x y n')
    # part1 = x+y*n-3
    # part2 = (x+y*n-4)+3*(x+y*n-5)

    # (p0+p1*n-3)=(p0+p1*n-4)+3*(p0+p1*n-5)
    init_printing(use_unicode=True)
    par1 = ordered_relation.split("=")[0]
    part1 = parse_expr(par1)
    #print("The eq is: {}".format(part1))
    par2 = ordered_relation.split("=")[1]
    part2 = parse_expr(par2)
    # test = (x,y)
    equation = solve(Eq(part1, part2), *an_symbols)
    # equation = solveset(Eq(part1, part2), *test)
    # equation = solve(Eq(part1, part2), *test)

    # print("Reached 6")
    equation = equation[0]  # removes the dictionary out of a list
    # print(equation)

    # print(equation)

    for key in equation.keys():
        #print("The key is: {}".format(key))
        particular_sol = particular_sol.replace(str(key), str(equation.get(key)))
        #print("particular solution is: {}".format(particular_sol))

    print("After ordered relation adjusted 2")
    print(particular_sol)

    return particular_sol

