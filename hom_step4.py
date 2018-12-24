# (Step 4) Obtain the general solution of degree 2+, nvm 1+
def find_general_solution_2(all_r_and_m_test):
    test_general_sol = "s(n)="
    u = 1  # counter for adding a + between root sections
    a = 1

    # chose which theorem to use based on the multiplicities
    # loop through all multiplicities, if any of them is > 1, then set boolean equal to True, default is false
    difficult_theorem = False
    for x in all_r_and_m_test.values():
        if x > 1:
            difficult_theorem = True
    # print(difficult_theorem)

    if difficult_theorem == True:  # if some multiplicitie(s) > 1
        for x in all_r_and_m_test:  # x is the values of the roots
            i = 0  # power of the n in every root section counter, resets for every root
            test_general_sol = test_general_sol + "("
            for y in range(0, all_r_and_m_test[x]):  # for the length of the multiplicity excluding the boundaries
                print(y)
                # if y == 0:  # to prevent one to many +
                #     test_general_sol = test_general_sol + "Alpha_" + str(a) + "*n**" + str(i)
                # elif y > 0:
                test_general_sol = test_general_sol + "+Alpha_" + str(a) + "*n**" + str(i)
                i = i + 1  # power counter
                a = a + 1  # alpha counter
            # prevents one to many * at the end
            if u == len(all_r_and_m_test):
                test_general_sol = test_general_sol + ")(" + str(x) + ")**n"
            elif u != len(all_r_and_m_test):
                test_general_sol = test_general_sol + ")(" + str(x) + ")**n+"
            else:
                print("Never lucky m8")
            u = u + 1
    elif difficult_theorem == False:  # when all multiplicities are 1
        for x in all_r_and_m_test:
            if x == 0:  # So that the equation doesn't start with +
                test_general_sol = test_general_sol + "Alpha_" + str(a) + "*(" + str(x) + ")**n"
            elif x != 0:
                test_general_sol = test_general_sol + "+Alpha_" + str(a) + "*(" + str(x) + ")**n"
            a = a + 1

    # replace all the *n**0 with "", cuz anything to the 0th power is 1
    # and replace anything to the power 1 to just that thing
    test_general_sol = test_general_sol.replace("*n**0", "")
    test_general_sol = test_general_sol.replace("**1", "")

    return test_general_sol

