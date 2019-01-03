from sympy.parsing.sympy_parser import parse_expr


# (Step 2) Obtaining char equation with degree 1
def char_equation_1(first_term_in):
    if parse_expr(first_term_in) >= 0:
        equation = "r-" + str(first_term_in) #+ "=0"
    elif parse_expr(first_term_in) < 0:
        first_term_in = int(first_term_in*-1)
        equation = "r+" + str(first_term_in) #+ "=0"
    return equation


# (Step 2) Obtaining char equation with degree 2+
def char_equation_2(coeffs):
    total_equation = "r**" + str(len(coeffs))
    i = 0
    next_power = len(coeffs)-1
    for x in range(len(coeffs)):
        next_coeff = parse_expr(coeffs[i])
        if next_coeff >= 0:
            next_coeff = "-" + str(next_coeff)
        elif next_coeff < 0:
            next_coeff = next_coeff * -1
            next_coeff = "+" + str(next_coeff)
        else:
            print("Smth went wrong in char_equation_2")

        # Finds out if the next power is 0, if so, then just add the coeff and not r^0 cuz r^0 = 1 = coeff
        if next_power != 0:
            total_equation = total_equation + str(next_coeff) + "*r**" + str(next_power)
        elif next_power == 0:
            total_equation = total_equation + str(next_coeff)
        i = i + 1
        next_power = next_power - 1

    # total_equation = total_equation + "=0"
    return total_equation
