# UNUSED

from typing import Tuple

from models import CSP
from constants import Variable


def get_variables_tuples(csp_instance: CSP) -> list[Tuple[Variable, Variable]]:
    """
    Returns the tuples of (Var_i, Var_j) for i != j. (which is equal and built as
    i < j).
    """
    number_of_variables = len(csp_instance.variables)
    variables_tuples = [
        (csp_instance.variables[i], csp_instance.variables[j])
        for i in range(number_of_variables)
        for j in range(i + 1, number_of_variables)
    ]
    return variables_tuples


def get_variables_tuples_i_smaller_than_j(
    csp_instance: CSP,
) -> list[Tuple[Variable, Variable]]:
    return get_variables_tuples(csp_instance=csp_instance)
