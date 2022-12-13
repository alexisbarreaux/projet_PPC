# This file contains several heuristics to choose the next variable to choose
# when resolving a CSP
import numpy as np
import math

from models import CSP
from constants import Variable


def naive_variable_choosing(
    csp_instance: CSP, state: dict, domains_last_valid_index: list
) -> Variable:
    """
    This is the most naive way of choosing the next variable.
    You just take the next one in the list of variables.
    """
    return len(state)


def smallest_domain_variable_choosing(
    csp_instance: CSP, state: dict, domains_last_valid_index: list
) -> Variable:
    """
    Here, we choose the variable with the smallest domain to take next.
    return np.argmin(domains_sizes)
    """
    domains_sizes = [
        domains_last_valid_index[i] if state.get(i, None) is None else math.inf
        for i in range(len(csp_instance.variables))
    ]
    return np.argmin(domains_sizes)
