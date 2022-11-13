# Main file for the backtrack algorithm.
from typing import Union, Callable

from models import CSP
from .variables_choosing_algorithms import naive_variable_choosing
from .values_ordering_algorithms import naive_values_ordering


class BacktrackSetup:
    """
    This is a wrapper around the backtrack function in itself to be able to choose
    different methods of selecting next node, value, etc.
    It has the following properties:
        - next_variable_choosing_method (Callable): the function used to select the next variable
            we want to put in the state. It takes the CSP and current state as input. It defaults to the
            naive choice where we just take the next variable in the CSP's order.
        - next_values_ordering_method (Callable): the function used to order the values and know in
            which order to test them.. It takes the CSP and new variable as input. It defaults to the
            naive order where we just take the next varaible's domain.

    """

    next_variable_choosing_method: Callable
    next_values_ordering_method: Callable

    def __init__(
        self,
        next_variable_choosing_method: Callable = naive_variable_choosing,
        next_values_ordering_method: Callable = naive_values_ordering,
    ) -> None:
        self.next_variable_choosing_method = next_variable_choosing_method
        self.next_values_ordering_method = next_values_ordering_method
        return

    def check_new_state_constraint_violation(
        self, csp_instance: CSP, state: dict, new_variable: str
    ):
        """
        If the previous state was valid, only constraints between the variable which now has a value
        and the previous ones can be violated.
        """
        new_variable_value = state[new_variable]
        # At the start, no variable was added and thus no constraint is wrong.
        if new_variable is None:
            return True

        else:
            # For each variable (including the new one but this isn't an issue)
            for variable in state.keys:
                # Try to get the constraint, it can be stored either with the key (variable, new_variable) or the
                # (new_variable, variable) one.
                if (
                    constraint_to_check := csp_instance.constraints.get(
                        (variable, new_variable), None
                    )
                ) is not None:
                    # If the constraint exists, see if it holds
                    variable_value = state[variable]
                    if not (variable_value, new_variable_value) in constraint_to_check:
                        return False

                elif (
                    constraint_to_check := csp_instance.constraints.get(
                        (new_variable, variable), None
                    )
                ) is not None:
                    # If the constraint exists, see if it holds
                    variable_value = state[variable]
                    if not (new_variable_value, variable_value) in constraint_to_check:
                        return False
            # At the end if no new constraint is False, then they are all True.
            return True

    def backtrack(
        self, csp_instance: CSP, state: dict, new_variable: str = None
    ) -> Union[bool, dict]:
        """
        A backtrack takes a CSP and a current state (variables that currently hold values). We also put the
        last added variable in new_variable because it makes check violations easier.

        The backtrack first checks if the current state is valid, and if not returns False.
        Otherwise it appends a new value for the next variable to the state and moves on recursively.

        The state is depicted as a dict, in which keys are variables names and values the value of
        each variable. A variable which currently holds no value is not in the dict.

        It returns a boolean and the current state.
        """
        # Check if a constraint is invalid
        if self.check_new_state_constraint_violation(
            csp_instance=csp_instance, state=state, new_variable=new_variable
        ):
            return False, state
        # If the current state is complete (all variables have values), then return it
        if len(state) == len(csp_instance.variables):
            return True, state

        # Otherwise, choose a new variable to add to state
        new_variable = self.next_variable_choosing_method(
            csp_instance=csp_instance, state=state
        )
        # Compute the order in which to test the possible values
        new_variable_values_order = self.next_values_ordering_method(
            csp_instance=csp_instance, new_variable=new_variable
        )

        for new_variable_possible_value in new_variable_values_order:
            # Copy the state dict to be able to call recurisvely without issue
            new_state = state.copy()
            new_state.update({new_variable: new_variable_possible_value})
            if self.backtrack(
                csp_instance=csp_instance, state=new_state, new_variable=new_variable
            ):
                # If a sub node has a solution, go back up and return true
                return True, new_state

        # If no sub nodes was true, return false
        return False, state
