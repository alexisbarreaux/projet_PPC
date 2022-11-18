# Main file for the backtrack algorithm.
from typing import Callable, Tuple

from models import CSP
from constants import Variable
from .variables_choosing_algorithms import naive_variable_choosing
from .values_ordering_algorithms import naive_values_ordering


class BacktrackClass:
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
        - optimization_state_evaluation (Callable): a function to choose between two states when working on an optimization
            (and not decision) problem.

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

    def check_if_new_state_is_valid(
        self, csp_instance: CSP, state: dict, last_variable_index: int
    ):
        """
        If the previous state was valid, only constraints between the variable which now has a value
        and the previous ones can be violated.
        """
        # At the start, no variable was added and thus no constraint is wrong.
        if last_variable_index is None:
            return True

        else:
            linked_constraints = csp_instance.get_linked_constraints(
                variable_index=last_variable_index
            )
            last_variable_value = state[csp_instance.variables[last_variable_index]]

            # For each constraint check it, if one is false directly return false
            for is_last_index_first, other_index, constraint in linked_constraints:
                other_variable_value = state[csp_instance.variables[other_index]]
                if is_last_index_first:
                    if constraint(
                        last_variable_index,
                        other_index,
                        last_variable_value,
                        other_variable_value,
                    ):
                        # If the constraint was valid in this order, go to next constraint
                        continue
                elif constraint(
                    other_index,
                    last_variable_index,
                    other_variable_value,
                    last_variable_value,
                ):
                    # If the constraint was valid in this order, go to next constraint
                    continue
                else:
                    # If the constraint was not valid, directly return False
                    return False

            return True

    def _backtrack(
        self, csp_instance: CSP, state: dict, last_variable_index: int = None
    ) -> Tuple[bool, dict]:
        """
        This backtrack will return back the first possible solution.
        A backtrack takes a CSP and a current state (variables that currently hold values). We also put the
        last added variable in last_variable because it makes check violations easier.

        The backtrack first checks if the current state is valid, and if not returns False.
        Otherwise it appends a new value for the next variable to the state and moves on recursively.

        The state is depicted as a dict, in which keys are variables names and values the value of
        each variable. A variable which currently holds no value is not in the dict.

        It returns a boolean and the current state.
        """
        # Check if a constraint is invalid
        if not self.check_if_new_state_is_valid(
            csp_instance=csp_instance,
            state=state,
            last_variable_index=last_variable_index,
        ):
            return False, state
        # If the current state is complete (all variables have values), then return it
        if len(state) == len(csp_instance.variables):
            return True, state

        # Otherwise, choose a new variable to add to state
        last_variable_index = self.next_variable_choosing_method(
            csp_instance=csp_instance, state=state
        )
        # Compute the order in which to test the possible values
        new_variable_values_order = self.next_values_ordering_method(
            csp_instance=csp_instance, last_variable_index=last_variable_index
        )

        for new_variable_possible_value in new_variable_values_order:
            # Copy the state dict to be able to call recurisvely without issue
            new_state = state.copy()
            new_state.update(
                {
                    csp_instance.variables[
                        last_variable_index
                    ]: new_variable_possible_value
                }
            )

            child_result, child_state = self._backtrack(
                csp_instance=csp_instance,
                state=new_state,
                last_variable_index=last_variable_index,
            )
            if child_result:
                # If a sub node has a solution, go back up and return true
                return True, child_state

        # If no sub nodes was true, return false
        return False, state

    def run_backtrack(self, csp_instance: CSP) -> Tuple[bool, dict]:
        return self._backtrack(csp_instance=csp_instance, state=dict())
