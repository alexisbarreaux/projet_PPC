# This file contains several heuristics to choose in which order to choose
# the next values for the next variable to be instantiated.
from models import CSP


def naive_values_ordering(
    csp_instance: CSP, last_variable_index: int, domain_last_valid_index: int
) -> list:
    """
    This is the most naive way of choosing the order for the values.
    We just return the possible indices in the base order.
    """
    return [i for i in range(domain_last_valid_index + 1)]
