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
    for variable_1 in csp_instance.domains.keys:
        for variable_2 in csp_instance.domains.keys:
            if variable_1 != variable_2:
                constraints[(variable_1, variable_2)] = diff(
                    domain_1=csp_instance.domains[variable_1],
                    domain_2=csp_instance.domains[variable_2],
                )

    return constraints
