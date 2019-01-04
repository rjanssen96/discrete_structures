from sympy.parsing.sympy_parser import parse_expr


# Checking if the user wants to automatically check every ccomma file or do one (or more) manually
def answer_check_manual_or_auto():
    manual_or_auto = input("Do you want to check everything automatically (a) or manually (m)?\n")

    # Ask if homog or non-homog

    if manual_or_auto == "a":
        print("Automatically selected\n")
        automatic_check()
        # nothing made for automated checks yet
    elif manual_or_auto == "m":
        print("Manual selected")
        manual_check_input()
    else:
        print("Neither a nor m given\n")


# Works for homogeneous, ask f(n) part separate?
# Collecting the relation data from the given comma file and our specific solution
def manual_check_input():
    degree = int(input("What is the degree of this relation?\n"))
    initial_terms = []

    for x in range(0, degree):
        initial_term = [input("what is initial term number " + str(x) + "?\n")]
        initial_terms = initial_terms + initial_term

    all_coefficient = []

    for x in range(0, degree):
        coefficient = [input("What is the coefficient of term " + str(x) + "\n")]
        all_coefficient = all_coefficient + coefficient

    # Ask for specific solution
    # print it like the rest below

    print("All coefficients")
    print(all_coefficient)

    print("All initial terms")
    print(initial_terms)

    correct_or_not = input("Are these values correct? (yes or no)\n")
    if correct_or_not == "yes":
        manual_check_rewrite_and_get_spec_sol(all_coefficient, initial_terms, degree)
    elif correct_or_not == "no":
        manual_check_input()


# rewrite the expression of the comma file relation to check before calculating and get our specific formula
def manual_check_rewrite_and_get_spec_sol(all_coefficient, initial_terms, degree):
    comma_spec_sol = ""
    i = 1
    for coeff in all_coefficient:
        # to prevent one to many + at the end
        if i != len(all_coefficient):
            comma_spec_sol = comma_spec_sol + str(coeff) + "*s(n-" + str(i) + ")+"
        elif i == len(all_coefficient):
            comma_spec_sol = comma_spec_sol + str(coeff) + "*s(n-" + str(i) + ")"
        i = i + 1

    our_specific_solution = input("What is our specific solution?\n")

    print("\nOur specific solution given:")
    print(our_specific_solution)

    print("Comma relation given:")
    print(comma_spec_sol)

    correct_or_not = input("Are these values correct? (yes or no)\n")
    if correct_or_not == "yes":
        manual_check_values_comma_relation(comma_spec_sol, our_specific_solution, initial_terms, degree)
    elif correct_or_not == "no":
        manual_check_input()


def manual_check_values_comma_relation(comma_spec_sol, our_specific_solution, initial_terms, degree):
    comma_answer_list = initial_terms

    # counter = int(degree)
    for x in range(0, 20-len(initial_terms)):  # to 18 terms cuz initial terms are already there, maybe 20-len(init_terms?)
        # reset it to terms with n
        change_specific_solution = comma_spec_sol

        # replaces ever n-x with the value of the term. So first with initial terms, then with new terms
        for y in range(1, degree+1):  # because range doesn't include the right boundary
            change_specific_solution = change_specific_solution.replace("s(n-" + str(y) + ")",
                                                                        str(comma_answer_list[degree+x-y]))
            # degree - y to keep going down the list by one for every n-x cuz the x keeps going one up (n-1, n-2, ...)
            # +x to keep moving one position further to the right in the list

        # adds the new value to the list of outcomes
        new_value = parse_expr(change_specific_solution)
        comma_answer_list = comma_answer_list + [str(new_value)]

    print("\nFirst 20 outcomes of the comma file relation")
    print(comma_answer_list)

    manual_check_values_our_solution(our_specific_solution, comma_answer_list)


# Put the results from our specific solutions in a list
def manual_check_values_our_solution(our_specific_solution, comma_answer_list):
    try:
        my_spec_sol = str(our_specific_solution)
        my_spec_sol = my_spec_sol.replace("^", "**")
    except:
        print("Not needed")

    my_answer_list = []

    for x in range(0, 20):
        my_new_spec_sol = my_spec_sol.replace("n", str(x))
        my_new_spec_sol = parse_expr(my_new_spec_sol)
        my_answer_list.append(my_new_spec_sol)

    print("\nFirst 20 outcomes of our specific solution")
    print(my_answer_list)

    compare_results(my_answer_list, comma_answer_list)


# Compare the two lists
def compare_results(my_answer_list, comma_answer_list):
    same_lists = True

    for x in range(0, len(my_answer_list)):
        if my_answer_list[x] != comma_answer_list[x]:
            same_lists = False

    if same_lists == True:
        print("\nThese lists are the same")
    elif same_lists == False:
        print("\nThese lists are NOT the same")


# rewrite the expression of the comma file relation to check before calculating and get our specific formula
def automatic_check_rewrite_and_get_spec_sol(all_coefficient, initial_terms, degree, our_specific_solution):
    comma_spec_sol = ""
    i = 1
    for coeff in all_coefficient:
        # to prevent one to many + at the end
        if i != len(all_coefficient):
            comma_spec_sol = comma_spec_sol + str(coeff) + "*s(n-" + str(i) + ")+"
        elif i == len(all_coefficient):
            comma_spec_sol = comma_spec_sol + str(coeff) + "*s(n-" + str(i) + ")"
        i = i + 1

    print("\nOur specific solution given:")
    print(our_specific_solution)
#
    print("Comma relation given:")
    print(comma_spec_sol)

    manual_check_values_comma_relation(comma_spec_sol, our_specific_solution, initial_terms, degree)


def automatic_check():
    degree = 4
    initial_terms = ['2', '3', '3', '6']
    all_coefficient = ['4', '5', '2', '4']
    # our_specific_solution = parse_expr("55+n^4")
    our_specific_solution = "55+n^4"

    # different from manual... give spec sol
    # manual_check_rewrite_and_get_spec_sol(all_coefficient, initial_terms, degree)
    automatic_check_rewrite_and_get_spec_sol(all_coefficient, initial_terms, degree, our_specific_solution)


answer_check_manual_or_auto()

