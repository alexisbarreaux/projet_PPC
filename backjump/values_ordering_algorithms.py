# This file contains several heuristics to choose in which order to choose
# the next values for the next variable to be instantiated.
from models import CSP
from constants import Domain
from random import shuffle


def naive_values_ordering(
    csp_instance: CSP, last_variable_index: int, domain_last_valid_index: int
) -> Domain:
    """
    This is the most naive way of choosing the order for the values.
    We just return the domain.
    """
    return csp_instance.domains[last_variable_index][: domain_last_valid_index + 1]


def random_values_ordering(
    csp_instance: CSP, last_variable_index: int, domain_last_valid_index: int
) -> Domain:
    """
    Here, we choose the value randomly in the ones currently choosable.
    We return the domain shuffled.
    """
    order = csp_instance.domains[last_variable_index][: domain_last_valid_index + 1]
    shuffle(order)
    return order
