# import synpy #


# (Step 2) Obtaining char equation with degree 1
def char_equation_1(first_term_in):
    # Only works atm if the coefficient is negative. Make if elif for coefficient > 0 and < 0
    if first_term_in >= 0:
        equation = "r - " + str(first_term_in) + " = 0"
    elif first_term_in < 0:
        first_term_in = int(first_term_in*-1)
        equation = "r + " + str(first_term_in) + " = 0"
    return equation


# (Step 2) Obtaining char equation with degree 2
def char_equation_2(coeffs):
    #print("The coeffs are:")
    #print(coeffs)
    total_equation = "r^" + str(len(coeffs))
    #print(total_equation)
    i = 0
    next_power = len(coeffs)-1
    for x in range(len(coeffs)):
        next_coeff = coeffs[i]
        if next_coeff >= 0:
            next_coeff = "-" + str(next_coeff)
        elif next_coeff < 0:
            next_coeff = next_coeff * -1
            next_coeff = "+" + str(next_coeff)
        else:
            print("Smth went wrong in char_equation_2")

        # Finds out if the next power is 0, if so, then just add the coeff and not r^0 cuz r^0 = 1 = coeff
        if next_power != 0:
            total_equation = total_equation + str(next_coeff) + "r^" + str(next_power)
        elif next_power == 0:
            total_equation = total_equation + str(next_coeff)
        #print(total_equation)
        i = i + 1
        next_power = next_power - 1

    total_equation = total_equation + "=0"
    return total_equation


# (Step 3) Obtain the root of degree 1 equations
def find_root_1(first_term_in):
    first_root = str(first_term_in)
    return first_root


# (Step 4) Obtain the general solution of degree 1
def find_general_solution_1(root_in):
    solution = "A_n = Alpha_1 * " + root_in + "^n"
    return solution


# (Step 5.1) Obtain the alpha values
def find_alpha_1(initial_term_1_in, root_in, n_value_in):
    root_value = int(root_in)**int(n_value_in)
    alpha_in_1 = int(initial_term_1_in) / int(root_value)
    return alpha_in_1


# (Step 5.2) Obtain the specific solution
def find_specific_solution_1(alpha_1_in, root_1_in):
    solution = "A_n = " + str(alpha_1_in) + " * " + str(root_1_in) + "^n"
    return solution


# Step 0: Read .txt and obtain initial terms (list?), degree and each C_1*A_n-1
degree = 2
initial_terms = [3, 5, 6]  # List of all initial terms
coefficients = [2, 5, 6, 8]
parts = ["*s(n-1)", "*s(n-2)", "*s(n-3)", "*s(n-4)"]  # If terms come from read.txt function, then comment this line

# Step 1: Rewriting the sequence
if degree == 1:
    sequence = "s(n)=" + str(coefficients[0]) + str(parts[0])
    print("Step 1: The rewritten sequence is: \n" + str(sequence) + "\n")
elif degree >= 2:
    sequence = "s(n)="
    i = 0
    for x in coefficients:
        if coefficients[i] >= 0 and i == 0:
            sequence = sequence + str(coefficients[i]) + str(parts[i])
        # add a + for the positive coefficients
        elif coefficients[i] >= 0:
            sequence = sequence + "+" + str(coefficients[i]) + str(parts[i])
        elif coefficients[i] < 0:
            sequence = sequence + str(coefficients[i]) + str(parts[i])
        else:
            print("wrong sequence step 1")
        i = i + 1
    print("Step 1: The rewritten sequence is: \n" + str(sequence) + "\n")

# Step 2: Obtaining the characteristic equation
if degree == 1:
    characteristic_equation = char_equation_1(coefficients[0])
    print("Step 2:  The characteristic equation is: \n" + str(characteristic_equation) + "\n")
elif degree >= 2:
    characteristic_equation = char_equation_2(coefficients)
    print("Step 2: The characteristic equation is: \n" + str(characteristic_equation) + "\n")
else:
    print("Step 2: Wrong degree value or incorrect characteristic equation" + "\n")
    characteristic_equation = ""

# Step 3: Obtain the roots
if degree == 1:
    root_1 = find_root_1(coefficients[0])
    print("Step 3:  The root of this equation is: \n" + str(root_1) + "\n")

# Step 4: Obtain general solution
if degree == 1:
    general_solution = find_general_solution_1(root_1)
    print("Step 4:  The general solution of this equation is: \n" + str(general_solution) + "\n")

# Step 5.1: Obtain alpha values
if degree == 1:
    alpha_1 = find_alpha_1(initial_terms[0], root_1, 0)  # 0 for A_n when n = 0, aka the first term of the sequence
    print("Step 5.1: The value of Alpha_1 is: \n" + str(alpha_1) + "\n")

# Step 5.2: Obtain specific solution
if degree == 1:
    specific_solution = find_specific_solution_1(alpha_1, root_1)
    print("Step 5.2: The specific solution for this equation is: \n" + str(specific_solution) + "\n")

