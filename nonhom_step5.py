# Find the particular solution of a non-homogeneous part

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
    #ordered_relation = "s(n-3) = s(n-4) + 3*s(n-5)"
    an_replace = "s(n) = " + str(particular_sol)

    degree = 6
    for d in range(degree):
        if d == 1:
            an_replace = an_replace.replace("n", "n-" + str(d))
            an_equation = an_replace.split("=",1)
            if "s(n-"+str(d) in ordered_relation:
                ordered_relation.replace("s(n-"+str(d)+")","("+an_equation+")").replace(" ","")
        else:
            an_replace = an_replace.replace("n-" + (str(d - 1)), "n-" + str(d))
            an_equation = an_replace.split("=")[1]
            if "s(n-"+str(d) in ordered_relation:
                ordered_relation = ordered_relation.replace("s(n-"+str(d)+")","("+an_equation+")").replace(" ","")
                print("s(n-"+str(d)+")")

        print(an_replace)
        print("oredered = " + ordered_relation)





    """
    RCIO BEGIN HIER:
    """





    # return smile
    return particular_sol