from constants import domain, constraint


def alldiff(domain_1: domain, domain_2: domain) -> constraint:
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
