# This file contains several heuristics to choose in which order to choose
# the next values for the next variable to be instantiated.
from models import CSP
from constants import Variable, Domain


def naive_values_ordering(csp_instance: CSP, new_variable: Variable) -> Domain:
    """
    This is the most naive way of choosing the order for the values.
    We just return the domain.
    """
    return csp_instance.domains[new_variable]
