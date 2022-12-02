# This file contains several heuristics to choose in which order to choose
# the next values for the next variable to be instantiated.
from models import CSP
from constants import Domain


def naive_values_ordering(csp_instance: CSP, last_variable_index: int) -> Domain:
    """
    This is the most naive way of choosing the order for the values.
    We just return the domain.
    """
    return csp_instance.domains[last_variable_index][
        : csp_instance.domains_last_valid_index[last_variable_index] + 1
    ]
