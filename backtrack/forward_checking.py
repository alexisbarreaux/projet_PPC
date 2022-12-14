# This file implements forward checking algorithm for PPC
from models import CSP
from constants import Constraint, VariableValue, Domain


def forward_checking_current_state(
    csp_instance: CSP, state: dict, last_variable_index: int, shrinking_operations: dict, domains_last_valid_index: list
) -> bool:
    """
    This function performs a forward checking on the current state of the csp instance,
    meaning it attempts to cut the domains of the variables linked to the last variable
    added to the state.
    It returns a boolean stating wether a domain became empty or not.
    """
    if last_variable_index is None:
        return False
    last_variable_value: VariableValue = state[last_variable_index]

    for linked_variable_index in csp_instance.variable_is_constrained_by[
        last_variable_index
    ]:
        # If the linked variable is already instanciated, do nothing
        if state.get(linked_variable_index, None) is not None:
            continue

        else:
            shrunk_domain_of = 0
            # Get the associated constraint
            constraint: Constraint = csp_instance.constraints[
                (last_variable_index, linked_variable_index)
            ]
            # Get the current domain of the linked variable
            linked_variable_domain: Domain = csp_instance.domains[linked_variable_index]
            linked_domain_last_index = domains_last_valid_index[
                linked_variable_index
            ]

            index = 0
            while index <= linked_domain_last_index:
                # Get a value for the linked variable
                linked_variable_value: VariableValue = linked_variable_domain[index]

                if not constraint(
                    last_variable_index,
                    linked_variable_index,
                    last_variable_value,
                    linked_variable_value,
                ):
                    shrunk_domain_of += 1

                    # If a constraint is invalid, if possible swap the last valid value with the current one and decrement
                    # the last valid index.
                    if not linked_domain_last_index == 0:
                        linked_variable_domain[index] = linked_variable_domain[
                            linked_domain_last_index
                        ]
                        linked_variable_domain[
                            linked_domain_last_index
                        ] = linked_variable_value
                        linked_domain_last_index -= 1
                    # Otherwise we know that we have an empty domain, just stop there
                    else:
                        return True

                # Otherwise just go check next possible value
                else:
                    index += 1
            # At the end update the csp and store the shrunking op??ration if it exists.
            domains_last_valid_index[
                linked_variable_index
            ] = linked_domain_last_index

            if shrunk_domain_of > 0:
                shrinking_operations[
                    linked_variable_index
                ] = shrunk_domain_of + shrinking_operations.get(
                    linked_variable_index, 0
                )

    return False
