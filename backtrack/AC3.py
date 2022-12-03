# This file implements the AC3 algorithms for PPC
from typing import Tuple

from models import CSP
from constants import Constraint, Domain


def restrict_domain_with_constraint(
    csp_instance: CSP,
    index_variable_1: int,
    index_variable_2: int,
    constraint: Constraint,
    shrinking_operations: dict,
    domains_last_valid_index: list,
) -> Tuple[bool, bool]:
    """
    This function attempts to restrict the domain of the first variable.
    It returns a tuple of booleans:
    - the first stating wether it emptied the domain
    - the second stating if it restricted the domain
    """
    domain_1_last_valid = domains_last_valid_index[index_variable_1]
    domain_2_last_valid = domains_last_valid_index[index_variable_2]
    domain_1: Domain = csp_instance.domains[index_variable_1]
    domain_2: Domain = csp_instance.domains[index_variable_2]
    shrunk_domain_of = 0

    # Try for each value in domain 1 if it is supported by at least one in domain 2
    index = 0
    while index <= domain_1_last_valid:
        value_1 = domain_1[index]
        found_valid_value = False

        for index_2 in range(domain_2_last_valid + 1):
            value_2 = domain_2[index_2]
            # If a value is valid stop and go to next value
            if constraint(index_variable_1, index_variable_2, value_1, value_2):
                found_valid_value = True
                break

        if found_valid_value:
            index += 1
            continue
        else:
            # At the end of the loop, if no valid linked value was found, update domain 1
            shrunk_domain_of += 1
            if not domain_1_last_valid == 0:
                domain_1[index] = domain_1[domain_1_last_valid]
                domain_1[domain_1_last_valid] = value_1
                domain_1_last_valid -= 1
            # Otherwise we know that we have an empty domain, just stop there
            else:
                return True, True

    # At the end update the csp and store the shrunking opération if it exists.
    domains_last_valid_index[index_variable_1] = domain_1_last_valid
    if shrunk_domain_of > 0:
        shrinking_operations[
            index_variable_1
        ] = shrunk_domain_of + shrinking_operations.get(index_variable_1, 0)
        return False, True
    else:
        return False, False


def AC3_current_state(
    csp_instance: CSP, shrinking_operations: dict, domains_last_valid_index: list
) -> bool:
    """
    This function performs arc consistency by the AC3 algorithm in place and returns a
    boolean stating wether it emptied a domain.
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
        domain_was_emptied, domain_was_restricted = restrict_domain_with_constraint(
            csp_instance=csp_instance,
            index_variable_1=index_variable_1,
            index_variable_2=index_variable_2,
            constraint=constraint,
            shrinking_operations=shrinking_operations,
            domains_last_valid_index=domains_last_valid_index,
        )
        if domain_was_emptied:
            return True
        elif domain_was_restricted:
            for linked_variable_index in csp_instance.variable_is_constrained_by[
                index_variable_1
            ]:
                if linked_variable_index != index_variable_2:
                    to_be_tested.add((linked_variable_index, index_variable_1))
        else:
            continue

    return False
