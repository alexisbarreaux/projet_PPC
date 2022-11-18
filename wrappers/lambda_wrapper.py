from typing import Tuple

from models import CSP
from constants import Constraint, Constraints, Variable


def lambda_wrapper_for_a_couple_of_variables(
    csp_instance: CSP, i: int, j: int, boolean_lambda
) -> Tuple[Tuple[Variable, Variable], Constraint]:
    """
    This function takes a CSP instance and returns a new constraint for two variables
    based on a condition given as a lambda function for each possible (var_i, var_j)
    The lambda function takes a tuple whose values is :
        - current value of i
        - current value of j
        - current value of var i
        - current value of var j
    The result of the lambda is a boolean
    """

    var_i: Variable = csp_instance.variables[i]
    var_j: Variable = csp_instance.variables[j]
    domain_i = csp_instance.domains[var_i]
    domain_j = csp_instance.domains[var_j]
    # Adding new constraint
    return (var_i, var_j), set(
        (value_var_i, value_var_j)
        for value_var_i in domain_i
        for value_var_j in domain_j
        if boolean_lambda(i, j, value_var_i, value_var_j)
    )


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
            # Adding new constraint
            variables_tuple, new_constraint = lambda_wrapper_for_a_couple_of_variables(
                csp_instance=csp_instance,
                i=i,
                j=j,
                boolean_lambda=boolean_lambda,
            )
            constraints[variables_tuple] = new_constraint

    return constraints
