from constants import Domain, Domains, Constraint, Constraints
from models import CSP


def diff(domain_1: Domain, domain_2: Domain) -> Constraint:
    """
    Returns all elements in the cartesian product of domain_1 x domain_2
    where the first and last elements are different.
    """
    return [
        (value_1, value_2)
        for value_1 in domain_1
        for value_2 in domain_2
        if value_1 != value_2
    ]


def alldiff(csp_instance: CSP) -> Constraints:
    """
    Builds diff constraints for each couple of variables.
    """
    constraints: Constraints = {}
    number_of_variables = len(csp_instance.variables)
    for i in range(number_of_variables):
        for j in range(i + 1, number_of_variables):
            variable_1 = csp_instance.variables[i]
            variable_2 = csp_instance.variables[j]
            # Adding new constraint
            constraints[(variable_1, variable_2)] = diff(
                domain_1=csp_instance.domains[variable_1],
                domain_2=csp_instance.domains[variable_2],
            )

    return constraints
