# This file implements the AC3 algorithms for PPC
from models import CSP
from constants import Constraint


def restrict_domain_with_constraint(
    csp_instance: CSP,
    index_variable_1: int,
    index_variable_2: int,
    constraint: Constraint,
) -> bool:
    """
    This function attempts to restrict the domain of the first variable.
    It returns a boolean stating wether it managed to restrict the domains or not.
    """
    # We "de-pile/re-pile" as pop and append are in O(1) but removing isn't
    updated_domain_1 = list()
    domain_1, domain_2 = (
        csp_instance.domains[index_variable_1],
        csp_instance.domains[index_variable_2],
    )
    base_domain_1_len = len(domain_1)

    # First check the domain of the first variable
    for _ in range(base_domain_1_len):
        value_1 = domain_1.pop()
        for value_2 in domain_2:
            if constraint(index_variable_1, index_variable_2, value_1, value_2):
                updated_domain_1.append(value_1)
                break
        # At the end of the loop, if it didn't break, the variable was "removed"
        # as it wasn't added back

    # Finally update the CSP and return the booleans
    csp_instance.domains[index_variable_1] = updated_domain_1

    return len(updated_domain_1) != base_domain_1_len


def AC3_current_state(csp_instance: CSP) -> None:
    """
    This function performs arc consistency by the AC3 algorithm in place
    """
    # Store the variables couples to be tested, at first these are all the ones for which
    # a constraint exists. We use a set to avoid duplicates
    to_be_tested = set(csp_instance.constraints.keys())

    while len(to_be_tested) > 0:
        (index_variable_1, index_variable_2) = to_be_tested.pop()
        constraint: Constraint = csp_instance.constraints[
            (index_variable_1, index_variable_2)
        ]
        # We check both x through y and y through x at once.
        domain_was_restricted = restrict_domain_with_constraint(
            csp_instance=csp_instance,
            index_variable_1=index_variable_1,
            index_variable_2=index_variable_2,
            constraint=constraint,
        )
        if domain_was_restricted:
            for linked_variable_index in csp_instance.variable_is_constrained_by[
                index_variable_1
            ]:
                if linked_variable_index != index_variable_2:
                    to_be_tested.add((linked_variable_index, index_variable_1))

    return
