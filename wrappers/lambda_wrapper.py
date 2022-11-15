from models import CSP
from constants import Constraints


def lambda_wrapper_all_vars_tuples(csp_instance: CSP, boolean_lambda) -> Constraints:
    """
    This function takes a CSP instance and returns constraints based on a condition given
    as a lambda function for each possible (var_i, var_j)
    The lambda function takes a tuple whose values is :
        - current value of i
        - current value of j
        - current value of var i
        - current value of var j
    The result of the lambda is a boolean
    """
    number_of_variables = len(csp_instance.variables)

    constraints: Constraints = {}
    for i in range(number_of_variables):
        for j in range(i + 1, number_of_variables):
            var_i = csp_instance.variables[i]
            var_j = csp_instance.variables[j]
            domain_i = csp_instance.domains[var_i]
            domain_j = csp_instance.domains[var_j]
            # Adding new constraint
            constraints[(var_i, var_j)] = set(
                (value_var_i, value_var_j)
                for value_var_i in domain_i
                for value_var_j in domain_j
                if boolean_lambda(i, j, value_var_i, value_var_j)
            )

    return constraints
