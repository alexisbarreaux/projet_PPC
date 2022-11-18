# This file contains several heuristics to choose the next variable to choose
# when resolving a CSP
from models import CSP
from constants import Variable


def naive_variable_choosing(csp_instance: CSP, state: dict) -> Variable:
    """
    This is the most naive way of choosing the next variable.
    You just take the next one in the list of variables.
    """
    return len(state)
