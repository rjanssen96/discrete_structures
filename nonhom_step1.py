import sympy

# Step 1: rewrite the relation to its default form: a_n = homog + F(n)
homogeneous_part = ""
fn_part = ""

degree = 2
initial_terms = [1, 1]
homogeneous_coeffs = [1, 1]


# degree = 2
# initial_terms = [1, 1]  # List of all initial terms
# coefficients = [1, 1]  # if n+1 in s():=, then make every n -1 (so one add a -1 to the n's)
# parts = ["*s(n-1)", "*s(n-2)", "*s(n-3)"]  # If terms come from read.txt function, then comment this line