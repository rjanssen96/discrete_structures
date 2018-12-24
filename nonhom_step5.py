# Find the particular solution of a non-homogeneous part


def find_part_sol_non_homog(fn_part, sn, highest_power, roots_multiples):
    # print("Have a nice day!!!")
    smile = fn_part
    s_root_check = False
    s = 111111111

    # t = highest_power
    next_power = highest_power
    for t in range(0, highest_power+1):  # +1 because not including the boundaries
        print(next_power)
        next_power = next_power - 1

    # checks if s is a root or not
    for x in roots_multiples:
        if s == x:
            s_root_check = True
        # print("root value:")
        # print(x)

    # decides if n**m needs to be added infront or not
    if s_root_check == True:
        a = "Happy boy"
    elif s_root_check == False:
        a = "Sad boy"

    # smile = ":-)"
    # See theorem 6 of the book

    return smile

